import sqlite3
import csv
from datetime import datetime, timedelta
import re
from data_processing import expand_day_range, add_colon_if_missing, get_next_day

MIDNIGHT_CLOSE_TIME = '11:59 pm'
MIDNIGHT_OPEN_TIME  = '12:00 am'

def initialize_db(filepath):
    conn = sqlite3.connect('restaurants.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS restaurant_hours
                (name TEXT, day TEXT, open_time TEXT, close_time TEXT)''')
    
    def parse_hours(hours_str):
        days_pattern = r'\b(?:Mon|Tues|Wed|Thu|Fri|Sat|Sun)(?:-(?:Mon|Tues|Wed|Thu|Fri|Sat|Sun))?\b'
        hours_pattern = r'\b(?:1[0-2]|0?[1-9]):?(?:[0-5][0-9])? ?[ap]m - (?:1[0-2]|0?[1-9]):?(?:[0-5][0-9])? ?[ap]m\b'
        days  = re.findall(days_pattern, hours_str)
        hours = re.findall(hours_pattern, hours_str)
        expanded_days = []
        for day in days:
            expanded_days.extend(expand_day_range(day))
        open_time  = hours.split('-').strip()[0]
        close_time = hours.split('-').strip()[1]
        return (expanded_days, open_time, close_time)
        
    with open(filepath, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip the header row
        for row in reader:
            name, hours = row
            for hours_string in hours.split('/'):
                days, open_time, close_time = parse_hours(hours_string)
                open_time  = add_colon_if_missing(open_time)
                close_time = add_colon_if_missing(close_time)
                open_time = datetime.strptime(open_time, '%I:%M %p').time()
                close_time = datetime.strptime(close_time, '%I:%M %p').time()
                for day in days:
                    if close_time <= open_time:
                        # hours cross midnight, split amongst the day and the succeeding date
                        next_day = get_next_day(day)
                        c.execute('INSERT INTO restaurant_hours (name, day, open_time, close_time) VALUES (?, ?, ?, ?)',
                                (name, day     , open_time         , MIDNIGHT_CLOSE_TIME),
                                (name, next_day, MIDNIGHT_OPEN_TIME, close_time))
                    else:
                        c.execute('INSERT INTO restaurant_hours (name, day, open_time, close_time) VALUES (?, ?, ?, ?)',
                                (name, day, open_time, close_time))


    # Commit and close
    conn.commit()
    conn.close()
