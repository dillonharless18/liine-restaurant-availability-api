import unittest
from src.helper_functions.data_processing import *

class TestHelpersDataProcessing(unittest.TestCase):

    ###########################
    # Begin has_numbers tests #
    ###########################

    def test_has_numbers_true(self):
        self.assertTrue(has_numbers("abc123"))

    def test_has_numbers_false(self):
        self.assertFalse(has_numbers("abcdef"))

    ################################
    # Begin expand_day_range tests #
    ################################

    def test_expand_day_range_single_day(self):
        self.assertEqual(expand_day_range("Mon"), ["Mon"])

    def test_expand_day_range_multiple_days(self):
        self.assertEqual(expand_day_range("Mon-Wed"), ["Mon", "Tues", "Wed"])

    ####################################
    # Begin add_colon_if_missing tests #
    ####################################
        
    def test_add_colon_if_missing_with_colon(self):
        self.assertEqual(add_colon_if_missing("10:30 am"), "10:30 am")

    def test_add_colon_if_missing_without_colon_am(self):
        self.assertEqual(add_colon_if_missing("10 am"), "10:00 am")

    def test_add_colon_if_missing_without_colon_pm(self):
        self.assertEqual(add_colon_if_missing("5 pm"), "5:00 pm")

    def test_add_colon_if_missing_invalid_format(self):
        with self.assertRaises(ValueError):
            add_colon_if_missing("invalid time")

    def test_add_colon_if_missing_without_minutes_am(self):
        self.assertEqual(add_colon_if_missing("3 am"), "3:00 am")

    def test_add_colon_if_missing_without_minutes_pm(self):
        self.assertEqual(add_colon_if_missing("12 pm"), "12:00 pm")

    def test_add_colon_if_missing_with_full_minute(self):
        self.assertEqual(add_colon_if_missing("11:45 pm"), "11:45 pm")

    def test_add_colon_if_missing_with_leading_zero(self):
        self.assertEqual(add_colon_if_missing("09 am"), "09:00 am")

    def test_add_colon_if_missing_with_space_after_am_pm(self):
        self.assertEqual(add_colon_if_missing("7 pm "), "7:00 pm")

    ############################
    # Begin get_next_day tests #
    ############################
        
    def test_get_next_day_midweek(self):
        self.assertEqual(get_next_day("Mon"), "Tues")

    def test_get_next_day_end_of_week(self):
        self.assertEqual(get_next_day("Sun"), "Mon")

    ##################################
    # Begin parse_hours_string tests #
    ##################################
        
    def test_parse_hours_string_with_day_range(self):
        input_string = "Mon-Fri 9:00 am - 5:00 pm"
        expected_output = [(['Mon', 'Tues', 'Wed', 'Thu', 'Fri'], '9:00 am', '5:00 pm')]
        self.assertEqual(parse_hours_string(input_string), expected_output)
    
    def test_parse_hours_string_with_one_day(self):
        input_string = "Mon 12:00 pm - 10:00 pm"
        expected_output = [(['Mon'], '12:00 pm', '10:00 pm')]
        self.assertEqual(parse_hours_string(input_string), expected_output)
    
    def test_parse_hours_string_with_two_separate_days_in_same_day_group(self):
        input_string = "Mon, Fri 3:00 am - 7:00 am"
        expected_output = [
            (['Mon', 'Fri'], '3:00 am', '7:00 am'),
        ]
        self.assertEqual(parse_hours_string(input_string), expected_output)

    def test_parse_hours_string_with_date_range_and_two_separate_days_in_same_day_group(self):
        input_string = "Mon-Thu, Sun 11 am - 10 pm"
        expected_output = [
            (['Mon', 'Tues', 'Wed', 'Thu', 'Sun'], '11:00 am', '10:00 pm'),
        ]
        self.assertEqual(parse_hours_string(input_string), expected_output)

    def test_parse_hours_string_with_date_range_two_day_groups(self):
        input_string = "Mon-Thu, Sun 11:30 am - 9:30 pm  / Fri-Sat 11:30 am - 10 pm"
        expected_output = [
            (['Mon', 'Tues', 'Wed', 'Thu', 'Sun'], '11:30 am', '9:30 pm'),
            (['Fri', 'Sat'], '11:30 am', '10:00 pm'),
        ]
        self.assertEqual(parse_hours_string(input_string), expected_output)
    
    ########################
    # Begin read_csv tests #
    ########################
    
    # TODO - Add tests for read_csv to handle errors gracefully
        
    ######################################
    # Begin update_structured_data tests #
    ######################################
        
    def test_update_structured_data_add_single_restaurant_hours_not_crossing_midnight(self):
        self.maxDiff = None
        structured_data = {}
        restaurant = "Test Diner"
        structured_hours = [(["Mon"], "9:00 am", "5:00 pm")]

        expected = {
            "Mon": {("9:00 am", "5:00 pm"): [restaurant]}
        }

        update_structured_data(structured_data, restaurant, structured_hours)

        self.assertEqual(structured_data, expected)
    
    def test_update_structured_data_add_single_restaurant_hours_crossing_midnight(self):
        self.maxDiff = None
        structured_data = {}
        restaurant = "Test Diner"
        structured_hours = [
            (["Fri"], "11:00 am", "12:30 am"),
            (["Sat"], "11:00 am", "12:30 am")
        ]

        expected = {
            "Fri": {("11:00 am", "11:59 pm"): [restaurant]},
            "Sat": {
                ("12:00 am", "12:30 am"): [restaurant],
                ("11:00 am", "11:59 pm"): [restaurant],
            },
            "Sun": {("12:00 am", "12:30 am"): [restaurant]},

        }

        update_structured_data(structured_data, restaurant, structured_hours)

        self.assertEqual(structured_data, expected)

if __name__ == '__main__':
    unittest.main()
