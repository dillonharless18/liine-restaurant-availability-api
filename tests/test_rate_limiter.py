import unittest
from time import sleep
from src.rate_limiter.rate_limiter import RateLimiter

class TestRateLimiter(unittest.TestCase):
    def test_requests_within_limit(self):
        rate_limiter = RateLimiter(5, 60)
        for _ in range(5):
            self.assertTrue(rate_limiter.is_allowed("test_client"))

    def test_requests_exceed_limit(self):
        rate_limiter = RateLimiter(1, 60)
        self.assertTrue(rate_limiter.is_allowed("test_client"))
        self.assertFalse(rate_limiter.is_allowed("test_client"))

    def test_reset_after_time_window(self):
        rate_limiter = RateLimiter(1, 1)
        self.assertTrue(rate_limiter.is_allowed("test_client"))
        sleep(1)
        # The limit should get reset after 1 second elapses
        self.assertTrue(rate_limiter.is_allowed("test_client"))

if __name__ == '__main__':
    unittest.main()
