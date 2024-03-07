import csv
import os
import re
from datetime import datetime
import pprint


# '%a' looks for Tue instead of Tues - used when checking open restaurants
# Another option is to replace it in the dataset which has the benefit of 
# addressing the issue for other apps using the data
day_map = {
    'Mon': 'Mon', 
    'Tue': 'Tues', 
    'Wed': 'Wed', 
    'Thu': 'Thu', 
    'Fri': 'Fri', 
    'Sat': 'Sat', 
    'Sun': 'Sun'
}

def has_numbers(inputString):
    '''
    Check if the input string contains any digits.

    Args:
    inputString (str): The string to check for digits.

    Returns:
    bool: True if the input string contains any digits, False otherwise.
    '''
    return any(char.isdigit() for char in inputString)

def get_data_file_path(filename='restaurants.csv'):
    '''
    Construct the file path for a given data file residing in the data directory,
    two levels up from the current directory.

    Args:
    filename (str, optional): The name of the file. Defaults to 'restaurants.csv'.

    Returns:
    str: The absolute file path to the data file.
    '''
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '../..', 'data')
    file_path = os.path.join(data_dir, filename)
    return file_path

# Function to expand day ranges like "Mon-Fri" into individual days
def expand_day_range(day_range):
    '''
    Expand a range of days (e.g., "Mon-Fri") into a list of individual days.

    Args:
    day_range (str): A string representing a range of days.

    Returns:
    list: A list of days expanded from the range. If the input is not a range,
          returns the input day as a single-element list.
    '''
    # Return early if not a range
    if "-" not in day_range:
        return [day_range]
    days = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start_day, end_day = day_range.split('-')
    start_index = days.index(start_day)
    end_index = days.index(end_day)
    return days[start_index:end_index + 1] if start_index <= end_index else days[start_index:] + days[:end_index + 1]

def read_csv(filepath):
    '''
    Reads a CSV file and yield each row, excluding the header.

    This generator function opens a CSV file located at the given filepath, skips the header row,
    and yields each row.

    Args:
    filepath (str): The path to the CSV file.

    Yields:
    list: The next row from the CSV file, with each element in the row as a separate list item.
    '''
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skipping the header row
        for row in csvreader:
            yield row

def parse_hours_string(hours_string):
    '''
    Parses a string representing the opening hours of a restaurant into a structured format.

    This function takes a string that represents the opening hours of a single restaurant
    and parses it into a more structured form.

    Args:
    hours_string (str): The string representing the opening hours, in a specific format.

    Returns:
    list of tuples: A list where each tuple represents a group of days with the same opening
                    hours. Each tuple contains a list of days (or day ranges expanded into
                    individual days), the start time, and the end time for those days.
    '''
    structured_hours = []
    for hours_group in hours_string.split(" / "):
        days = []
        start = None
        end = None
        for day_part in hours_group.split(","):
            day_part = day_part.strip()
            day_or_day_range = None

            if has_numbers(day_part):
                day_part_and_start, end = day_part.split(" - ")  # Assumption: Hours have spaces around the hyphen
                day_or_day_range, start = day_part_and_start.split(' ', 1)
                days.append(day_or_day_range)
                start = add_colon_if_missing(start)
                end = add_colon_if_missing(end)
            else:
                days.append(day_part)

        for day_part in days:
            structured_hours.append((expand_day_range(day_part), start, end))
    return structured_hours

def add_colon_if_missing(time_string):
    '''Ensures time strings are in the 'HH:MM' format.'''
    return time_string if ":" in time_string else time_string.replace(" ", ":00 ")

def update_structured_data(structured_data, restaurant, structured_hours):
    '''
    Updates the structured data dictionary by adding the restaurant's information
    under each relevant day and time slot.

    Args:
    structured_data (dict): The structured data holding restaurant information, keyed by day and time slots.
    restaurant (str): The name of the restaurant to add.
    structured_hours (list of tuples): Each tuple contains a list of days, start time, and end time for the restaurant.

    Returns:
    None: The function modifies the structured_data dictionary in place.
    '''

    def add_restaurant(day, start, end):
        """ Helper function to add the restaurant to the structured data for a specific day and time slot. """
        if day not in structured_data:
            structured_data[day] = {}
        if (start, end) not in structured_data[day]:
            structured_data[day][(start, end)] = []
        structured_data[day][(start, end)].append(restaurant)

    for day_parts, start, end in structured_hours:
        for day in day_parts:
            preserved_start, preserved_end = start, end  # Preserving original times for when hours cross midnight

            # This handles restaurants whose hours span midnight
            if datetime.strptime(preserved_start, '%I:%M %p').time() > datetime.strptime(preserved_end, '%I:%M %p').time():
                add_restaurant(day, preserved_start, '11:59 PM')
                next_day = get_next_day(day)  # Function to get the next day of the week
                add_restaurant(next_day, '12:00 AM', preserved_end)
            else:
                add_restaurant(day, preserved_start, preserved_end)

def get_next_day(day):
    '''
    Returns the next day of the week given a day.

    Args:
    day (str): A string representing a day of the week.

    Returns:
    str: The next day of the week.
    '''
    days_of_week = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
    next_day_index = (days_of_week.index(day) + 1) % len(days_of_week)
    return days_of_week[next_day_index]

def preprocess_data(filepath):
    '''Main function to preprocess data from the given CSV file.'''
    structured_data = {}
    for row in read_csv(filepath):
        restaurant, hours_string = row
        structured_hours = parse_hours_string(hours_string)
        update_structured_data(structured_data, restaurant, structured_hours)
    return structured_data

# Function to check if a restaurant is open
def get_open_restaurants(structured_data, datetime_str):
    dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
    dt = dt.replace(second=0) # Assuming if they're open on a minute it's the whole minute
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
