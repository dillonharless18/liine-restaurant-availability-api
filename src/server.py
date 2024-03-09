from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from functools import partial
from helper_functions.data_processing import get_data_file_path, preprocess_data
from helper_functions.query import get_open_restaurants
from helper_functions.utility_functions import validate_datetime
from rate_limiter.rate_limiter import RateLimiter

class RequestHandler(BaseHTTPRequestHandler):
    rate_limiter = RateLimiter(100, 600)

    def __init__(self, restaurant_hours, *args, **kwargs):
        # BaseHTTPRequestHandler calls do_GET inside __init__
        # so required fields must be set before calling super
        # More details here: https://tinyurl.com/mr27s2hw
        self.restaurant_hours = restaurant_hours
        super().__init__(*args, **kwargs)

    def send_error_response(self, status_code, message):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = {'error': message}
        self.wfile.write(json.dumps(response).encode())
    
    def do_HEAD(self, content_length=0):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        if content_length > 0:
            self.send_header('Content-Length', str(content_length))
        self.end_headers()

    def do_GET(self):
        try:
            # simple rate limiting
            client_ip = self.client_address[0]
            if not self.rate_limiter.is_allowed(client_ip):
                self.send_error_response(429, 'Too Many Requests')
                return
            
            parsed_path = urlparse(self.path)
            path = parsed_path.path

            if path != '/restaurants':
                self.send_error_response(404, 'Not Found')
                return

            query_params = parse_qs(parsed_path.query)
            datetime_param = query_params.get('datetime', [None])[0]
            
            if not datetime_param:
                self.send_error_response(400, 'Query parameter `datetime` is required. Please use YYYY-MM-DDTHH:MM:SS format.')
                return

            if not validate_datetime(datetime_param):
                self.send_error_response(400, 'Invalid datetime format. Please use YYYY-MM-DDTHH:MM:SS format.')
                return

            open_restaurants = get_open_restaurants(self.restaurant_hours, datetime_param)
            json_response = json.dumps(open_restaurants)
            content_length = len(json_response.encode())
            
            self.do_HEAD(content_length=content_length)
            self.wfile.write(json_response.encode())
        except Exception as e:
            print(f"Error handling request: {e}")
            # TODO - After enhancing error handling, can send appropriate messages back to client as well
            self.send_error_response(500, 'Internal Server Error')


def run(server_class=HTTPServer, handler_class=RequestHandler, port=3000, data=None):
    custom_handler = partial(handler_class, data) # alternative to class factory - makes extra args availabe to the RequestHandler
    server_address = ('0.0.0.0', port)
    httpd = server_class(server_address, custom_handler)

    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    data_filepath = get_data_file_path('restaurants.csv')
    structured_data = preprocess_data(data_filepath)
    run(data=structured_data)