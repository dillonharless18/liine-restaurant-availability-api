import csv
import http.server
import json
from collections import defaultdict
from urllib.parse import urlparse, parse_qs

# Loads restaurant hours from CSV file
def load_restaurant_hours(filename):
    restaurant_hours = defaultdict(list)
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header row
        for row in reader:
            name, hours = row
            restaurant_hours[name].append(hours)
    return restaurant_hours

class RequestHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        pass

def run(server_class=http.server.HTTPServer, handler_class=RequestHandler, port=3000):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)

    print(f'Serving HTTP on port {port}...')
    httpd.serve_forever()

run()