import csv
import os
import re
from datetime import datetime

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

def get_data_file_path(filename='restaurants.csv'):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_dir, '../..', 'data')
    file_path = os.path.join(data_dir, filename)
    return file_path

# Function to expand day ranges like "Mon-Fri" into individual days
def expand_day_range(day_range):
    if "-" not in day_range:
        return [day_range]
    days = ["Mon", "Tues", "Wed", "Thu", "Fri", "Sat", "Sun"]
    start_day, end_day = day_range.split('-')
    start_index = days.index(start_day)
    end_index = days.index(end_day)
    return days[start_index:end_index + 1] if start_index <= end_index else days[start_index:] + days[:end_index + 1]

# Preprocess and structure the data
def preprocess_data(filepath):
    structured_data = {}
    with open(filepath, mode='r', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip the header row
        print()
        for row in csvreader:
            restaurant = row[0]  # Assuming the first column is the restaurant name
            print(restaurant)
            hours_string = row[1]  # Assuming the second column is the operating hours
            print(hours_string)
            for hours_group in hours_string.split(" / "):
                print("group: " + hours_group)
                # matches = re.findall(r'([a-zA-Z]{3,4}?:-([a-zA-Z]{3,4})?) ([0-9]{1,2}:[0-9]{2} [ap]m) - ([0-9]{1,2} [ap]m)', hours_group)
                # for match in matches:
                #     print("match")
                #     print(match)
                #     days, start, end = match
                    # if '-' in days:
                    #         days = expand_day_range(days)
                    #         print("expnaded days")
                    #         print(days)
                    #     else:
                    #         days = [days]

                    #     for day in days:
                    #         if day not in structured_data:
                    #             structured_data[day] = {}
                    #         if (start, end) not in structured_data[day]:
                    #             structured_data[day][(start, end)] = []
                    #         structured_data[day][(start, end)].append(restaurant)
                days  = []
                start = None
                end   = None
                for day_part in hours_group.split(","):
                    day_part = day_part.strip()
                    day_or_day_range = None
                    print("day_part: " + day_part)
                    if has_numbers(day_part):
                        # Assumption: Restaurants don't close and re-open during the middle of the day.
                        # If they do, this would need to be revised.
                        day_part_and_start, end = day_part.split(" - ") # the hours hyphen has surrounding spaces
                        print("day part and start")
                        print(day_part_and_start)
                        print("end")
                        print(end)
                        day_or_day_range, start = day_part_and_start.split(' ', 1)
                        print("day or day range")
                        print(day_or_day_range)
                        days.append(day_or_day_range)
                        # ensure all top of the hour entries have :00 to de-dupe
                        if ":" not in start:
                            start = start.replace(" ", ":00 ")
                        if ":" not in end:
                            end = end.replace(" ", ":00 ")

                    else:
                        days.append(day_part)
                
                for day_part in days:
                    print("day_part in days")
                    print(day_part) 
                    # if '-' in day_part:
                    day_part = expand_day_range(day_part)
                    print("expanded day_part")
                    print(day_part)
                    # else:
                    #     day_part = list(day_part)
                    #     print("day_part")
                    #     print(day_part)

                    for day in day_part:
                        print("day in day_parts")
                        print(day) 
                        if day not in structured_data:
                            structured_data[day] = {}
                        if (start, end) not in structured_data[day]:
                            structured_data[day][(start, end)] = []
                        structured_data[day][(start, end)].append(restaurant)
                        # print(structured_data)

                        


                    
                        
                    # for day in days:
                    #     if day not in structured_data:
                    #         structured_data[day] = {}
                    #     # Convert start and end times to strings that can be easily converted back to datetime objects later
                    #     start_str = datetime.strptime(start, '%I %p').strftime('%I %p')
                    #     end_str = datetime.strptime(end, '%I %p').strftime('%I %p')

                    #     if (start_str, end_str) not in structured_data[day]:
                    #         structured_data[day][(start_str, end_str)] = []
                    #     structured_data[day][(start_str, end_str)].append(restaurant)
                        # print(structured_data)
                    print()
                print()
    return structured_data

# Function to check if a restaurant is open
# def is_open(structured_data, datetime_str):
#     dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
#     day = dt.strftime('%a')  # Get the day in short format: Mon, Tue, etc.
#     print(day)
#     time = dt.strftime('%I %p')  # Convert time to the 12-hour format with AM/PM
#     print(time.lower())

#     open_restaurants = []
#     for (start, end), restaurants in structured_data.get(day, {}).items():
#         print(type(start))
#         if start <= time <= end:
#             open_restaurants.extend(restaurants)
#     return open_restaurants

# Function to check if a restaurant is open
def is_open(structured_data, datetime_str):
    dt = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    day = dt.strftime('%a')
    time = dt.time()

    open_restaurants = []
    for (start, end), restaurants in structured_data.get(day, {}).items():
        start_time = datetime.strptime(start, '%I:%M %p').time()
        end_time = datetime.strptime(end, '%I:%M %p').time()

        if start_time <= time <= end_time:
            print(restaurants)
            open_restaurants.extend(restaurants)
    return open_restaurants

# Load the data and preprocess
filepath = get_data_file_path('smaller_list_of_restaurants.csv')
structured_data = preprocess_data(filepath)

# Example usage
datetime_str = "2024-03-12 13:00:00"
print(structured_data)
open_restaurants = is_open(structured_data, datetime_str)
print(f"Open restaurants at {datetime_str}: {open_restaurants}")
