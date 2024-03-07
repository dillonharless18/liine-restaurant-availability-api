import csv
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from collections import defaultdict
from socketserver import BaseServer
from urllib.parse import urlparse, parse_qs
from functools import partial

def get_data_file_path(filename='restaurants.csv'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '..', 'data')
    file_path = os.path.join(data_dir, filename)
    return file_path

def load_restaurant_hours(filename):
    restaurant_hours = defaultdict(list)
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header row
        for row in reader:
            name, hours = row
            restaurant_hours[name].append(hours)
    return restaurant_hours

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
            # response_data = self.restaurant_hours
            response_data = {'datetime_received': datetime_param}
            json_response = json.dumps(response_data)

            # Calculate the content length
            content_length = len(json_response.encode())
            
            self.do_HEAD(content_length=content_length)
            self.wfile.write(json_response.encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=3000, data=None):
    # Using partial application as alternative to a class factory
    custom_handler = partial(handler_class, data)
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, custom_handler)

    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    data_filepath = get_data_file_path()
    restaurant_hours = load_restaurant_hours(data_filepath)
    run(data=restaurant_hours)