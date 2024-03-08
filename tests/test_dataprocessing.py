import unittest
from src.helpers.data_processing import has_numbers, expand_day_range, add_colon_if_missing, get_next_day  # Import your functions here

class TestUtilityFunctions(unittest.TestCase):

    def test_has_numbers_true(self):
        self.assertTrue(has_numbers("abc123"))

    def test_has_numbers_false(self):
        self.assertFalse(has_numbers("abcdef"))

    def test_expand_day_range_single_day(self):
        self.assertEqual(expand_day_range("Mon"), ["Mon"])

    def test_expand_day_range_multiple_days(self):
        self.assertEqual(expand_day_range("Mon-Wed"), ["Mon", "Tues", "Wed"])

    def test_add_colon_if_missing_with_colon(self):
        self.assertEqual(add_colon_if_missing("10:30"), "10:30")

    def test_add_colon_if_missing_without_colon_am(self):
        self.assertEqual(add_colon_if_missing("10 pm"), "10:00 pm")

    def test_add_colon_if_missing_without_colon_pm(self):
        self.assertEqual(add_colon_if_missing("10 pm"), "10:00 pm")

    def test_get_next_day_midweek(self):
        self.assertEqual(get_next_day("Mon"), "Tues")

    def test_get_next_day_end_of_week(self):
        self.assertEqual(get_next_day("Sun"), "Mon")

if __name__ == '__main__':
    unittest.main()
