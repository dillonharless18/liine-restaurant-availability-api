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
    def __init__(self, restaurants, *args, **kwargs):
        self.restaurants = restaurants

        # BaseHTTPRequestHandler calls do_GET insideinit
        # Required fields must be set before calling super
        # More details here: https://tinyurl.com/mr27s2hw
        super().__init__(*args, **kwargs)
    
    def do_HEAD(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        if self.path == '/restaurants':
            self.do_HEAD()
            response_data = {'x': 'z'}
            json_response = json.dumps(response_data)
            self.wfile.write(json_response.encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=3000, data=None):
    # Using partial to make the restaurant data available inside the RequestHandler
    # An alternative to a class factory with a few advantages
    custom_handler = partial(handler_class, data)
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, custom_handler)

    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    data_filepath = get_data_file_path()
    restaurant_hours = load_restaurant_hours(data_filepath)
    run(data=restaurant_hours)