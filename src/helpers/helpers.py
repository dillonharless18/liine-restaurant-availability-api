import csv
import os
import re
from datetime import datetime

# '%a' looks for Tue instead of Tues - used when checking open restaurants
# Another option is to replace it in the dataset which has the benefit of 
# addressing the issue for other apps using the data
day_map = {
    'Mon': 'Mon', 
    'Tue': 'Tues', 
    'Wed': 'Wed', 'Thu': 
    'Thu', 'Fri': 'Fri', 
    'Sat': 'Sat', 
    'Sun': 'Sun'
}

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_data_file_path(filename='restaurants.csv'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '../..', 'data')
    file_path = os.path.join(data_dir, filename)
    return file_path

# Function to expand day ranges like "Mon-Fri" into individual days
def expand_day_range(day_range):
    # Return early if not a range
    if "-" not in day_range:
        return [day_range]
    days = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start_day, end_day = day_range.split('-')
    start_index = days.index(start_day)
    end_index = days.index(end_day)
    return days[start_index:end_index + 1] if start_index <= end_index else days[start_index:] + days[:end_index + 1]

def preprocess_data(filepath):
    structured_data = {}
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            restaurant = row[0]
            hours_string = row[1]
            for hours_group in hours_string.split(" / "):
                days  = []
                start = None
                end   = None
                for day_part in hours_group.split(","):
                    day_part = day_part.strip()
                    day_or_day_range = None

                    if has_numbers(day_part):
                        # Assumption: Restaurants don't close and re-open during the middle of the day.
                        # If they do, this would need to be revised.
                        day_part_and_start, end = day_part.split(" - ") # the hours hyphen has surrounding spaces
                        day_or_day_range, start = day_part_and_start.split(' ', 1)
                        days.append(day_or_day_range)
                        # ensure all top of the hour entries have :00 to de-dupe
                        if ":" not in start:
                            start = start.replace(" ", ":00 ")
                        if ":" not in end:
                            end = end.replace(" ", ":00 ")
                    else:
                        days.append(day_part)
                
                for day_part in days:
                    day_part = expand_day_range(day_part)

                    for day in day_part:
                        if day not in structured_data:
                            structured_data[day] = {}
                        if (start, end) not in structured_data[day]:
                            structured_data[day][(start, end)] = []
                        structured_data[day][(start, end)].append(restaurant)
    return structured_data

# Function to check if a restaurant is open
def get_open_restaurants(structured_data, datetime_str):
    dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
    day_abbr = dt.strftime('%a')
    time = dt.time()
    day = day_map.get(day_abbr)

    open_restaurants = []
    for (start, end), restaurants in structured_data.get(day, {}).items():
        start_time = datetime.strptime(start, '%I:%M %p').time()
        end_time = datetime.strptime(end, '%I:%M %p').time()

        if start_time <= time <= end_time:
            open_restaurants.extend(restaurants)
    return open_restaurants
