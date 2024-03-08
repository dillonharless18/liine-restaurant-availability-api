import unittest
from src.helpers.data_processing import has_numbers, expand_day_range, add_colon_if_missing, get_next_day  # Import your functions here

class TestHelpersDataProcessing(unittest.TestCase):

    def test_has_numbers_true(self):
        self.assertTrue(has_numbers("abc123"))

    def test_has_numbers_false(self):
        self.assertFalse(has_numbers("abcdef"))

    def test_expand_day_range_single_day(self):
        self.assertEqual(expand_day_range("Mon"), ["Mon"])

    def test_expand_day_range_multiple_days(self):
        self.assertEqual(expand_day_range("Mon-Wed"), ["Mon", "Tues", "Wed"])

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

    def test_get_next_day_midweek(self):
        self.assertEqual(get_next_day("Mon"), "Tues")

    def test_get_next_day_end_of_week(self):
        self.assertEqual(get_next_day("Sun"), "Mon")

if __name__ == '__main__':
    unittest.main()
