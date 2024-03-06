import csv
import http.server
import socketserver
import ssl
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
