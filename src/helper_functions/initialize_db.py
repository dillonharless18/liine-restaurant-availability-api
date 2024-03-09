import sqlite3
import csv
import re
from datetime import datetime
from .data_processing import expand_day_range, add_colon_if_missing, get_next_day

MIDNIGHT_CLOSE_TIME = '23:59:00'
MIDNIGHT_OPEN_TIME  = '00:00:00'

def initialize_db(filepath):
    '''
    Initializes the database and imports restaurant opening hours from a CSV file.
    
    This function creates a new SQLite database named 'restaurants.db'. It reads a CSV file specified by the 'filepath' parameter, 
    parses the opening hours, and inserts the data into the database. It handles cases where restaurant hours span past midnight 
    by splitting the entry intotwo records.
    
    Parameters:
        filepath (str): The file path to the CSV file containing restaurant names and their corresponding opening hours.
    '''
    conn = sqlite3.connect('restaurants.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS restaurant_hours
                (name TEXT, day TEXT, open_time TEXT, close_time TEXT)''')
    c.execute('DELETE FROM restaurant_hours')  # refreshing db every time
    
    def parse_hours(hours_str):
        days_pattern = r'\b(?:Mon|Tues|Wed|Thu|Fri|Sat|Sun)(?:-(?:Mon|Tues|Wed|Thu|Fri|Sat|Sun))?\b'
        days_list  = re.findall(days_pattern, hours_str)
        expanded_days = []
        for day in days_list:
            expanded_days.extend(expand_day_range(day))

        hours_pattern = r'\b(?:1[0-2]|0?[1-9]):?(?:[0-5][0-9])? ?[ap]m - (?:1[0-2]|0?[1-9]):?(?:[0-5][0-9])? ?[ap]m\b'
        hours_list = re.findall(hours_pattern, hours_str)
        hours_str  = ''.join(hours_list).split('-')
        open_time  = hours_str[0].strip()
        close_time = hours_str[1].strip()

        return (expanded_days, open_time, close_time)
        
    # TODO See how I can make this cleaner - going to hold off on this in interest of time
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skipping header row
        for row in reader:
            name, hours = row
            for hours_string in hours.split('/'):
                days, open_time, close_time = parse_hours(hours_string)
                open_time  = add_colon_if_missing(open_time)
                close_time = add_colon_if_missing(close_time)
                open_time = datetime.strptime(open_time, '%I:%M %p').time()
                close_time = datetime.strptime(close_time, '%I:%M %p').time()
                open_time_str = open_time.strftime('%H:%M:%S')
                close_time_str = close_time.strftime('%H:%M:%S')
                query_string = 'INSERT INTO restaurant_hours (name, day, open_time, close_time) VALUES (?, ?, ?, ?)'
                for day in days:
                    if close_time <= open_time:
                        # hours cross midnight, split amongst the day and the succeeding date
                        next_day = get_next_day(day)
                        c.execute(query_string,
                                (name, day, open_time_str, MIDNIGHT_CLOSE_TIME))
                        c.execute(query_string,
                                (name, next_day, MIDNIGHT_OPEN_TIME, close_time_str))
                    else:
                        c.execute(query_string,
                                (name, day, open_time_str, close_time_str))

    conn.commit()
    conn.close()
