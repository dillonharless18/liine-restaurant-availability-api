import unittest
from collections import defaultdict
import csv
import os
from src.main import load_restaurant_hours

class TestLoadRestaurantHours(unittest.TestCase):

    def setUp(self):
        # Temp csv
        self.filename = 'test_restaurant_hours.csv'
        restaurants = [
            ["The Cowfish Sushi Burger Bar", "Mon-Sun 11:00 am - 10 pm"],
            ["Morgan St Food Hall", "Mon-Sun 11 am - 9:30 pm"],
            ["Beasley's Chicken + Honey", "Mon-Fri, Sat 11 am - 12 pm  / Sun 11 am - 10 pm"],
            ["Garland", "Tues-Fri, Sun 11:30 am - 10 pm  / Sat 5:30 pm - 11 pm"]
        ]

        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Restaurant Name', 'Hours'])  # Header row
            writer.writerows(restaurants)  # Write all restaurant data

    def tearDown(self):
        os.remove(self.filename)

    def test_load_restaurant_hours(self):
        expected_result = defaultdict(list, {
            "The Cowfish Sushi Burger Bar": ["Mon-Sun 11:00 am - 10 pm"],
            "Morgan St Food Hall": ["Mon-Sun 11 am - 9:30 pm"],
            "Beasley's Chicken + Honey": ["Mon-Fri, Sat 11 am - 12 pm  / Sun 11 am - 10 pm"],
            "Garland": ["Tues-Fri, Sun 11:30 am - 10 pm  / Sat 5:30 pm - 11 pm"]
        })

        result = load_restaurant_hours(self.filename)
        self.assertEqual(result, expected_result)

    def test_empty_file(self):
        # Empty csv file test should return empty defaultdict - only have a header row here
        with open(self.filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Restaurant Name', 'Hours'])

        expected_result = defaultdict(list)

        result = load_restaurant_hours(self.filename)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()

