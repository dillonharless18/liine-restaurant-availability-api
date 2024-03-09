from datetime import datetime
import sqlite3
from contextlib import closing

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


def get_open_restaurants(structured_data, datetime_str):
    '''Main function to get open restaurants from in-memory data store.'''
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



def get_open_restaurants_from_db(conn, datetime_str):
    '''Main function used to get restaurants from local db.'''
    dt = datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S')
    dt = dt.replace(second=0)
    day_abbr = dt.strftime('%a')
    time_str = dt.strftime('%H:%M:%S')
    day = day_map.get(day_abbr)
    print(day)
    print(time_str)

    open_restaurants = []
    with closing(conn.cursor()) as cursor:
        query = '''
        SELECT name FROM restaurant_hours
        WHERE day = ? AND open_time <= ? AND close_time >= ?
        '''

        cursor.execute(query, (day, time_str, time_str))
        open_restaurants = [row[0] for row in cursor.fetchall()]

    return open_restaurants
