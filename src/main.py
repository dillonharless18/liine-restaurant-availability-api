from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs
from functools import partial
from helpers.data_processing import get_data_file_path, preprocess_data
from helpers.query import get_open_restaurants

class RequestHandler(BaseHTTPRequestHandler):
    def __init__(self, restaurant_hours, *args, **kwargs):
        # BaseHTTPRequestHandler calls do_GET inside __init__
        # so required fields must be set before calling super
        # More details here: https://tinyurl.com/mr27s2hw
        self.restaurant_hours = restaurant_hours
        super().__init__(*args, **kwargs)
    
    def do_HEAD(self, content_length=0):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        # Set the Content-Length header if content length is provided
        if content_length > 0:
            self.send_header('Content-Length', str(content_length))
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == '/restaurants':
            query_params = parse_qs(parsed_path.query)
            datetime_param = query_params.get('datetime', [''])[0]

            open_restaurants = get_open_restaurants(self.restaurant_hours, datetime_param)
            json_response = json.dumps(open_restaurants)
            content_length = len(json_response.encode())
            
            self.do_HEAD(content_length=content_length)
            self.wfile.write(json_response.encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=3000, data=None):
    custom_handler = partial(handler_class, data) # alternative to class factory
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, custom_handler)

    print(structured_data)
    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    data_filepath = get_data_file_path('smaller_list_of_restaurants.csv')
    structured_data = preprocess_data(data_filepath)
    run(data=structured_data)