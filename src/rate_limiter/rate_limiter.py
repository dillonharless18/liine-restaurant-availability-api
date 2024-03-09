import time
from collections import defaultdict

class RateLimiter:
    def __init__(self, quota, window):
        self.REQUEST_QUOTA = quota
        self.TIME_WINDOW = window
        self._request_timestamps = defaultdict(list)

    def is_allowed(self, client_id):
        current_time = time.time()
        timestamps = self._request_timestamps[client_id]

        self._request_timestamps[client_id] = [t for t in timestamps if current_time - t < self.TIME_WINDOW] # could optimize this to stop once it's past a certain point

        if len(self._request_timestamps[client_id]) < self.REQUEST_QUOTA:
            self._request_timestamps[client_id].append(current_time)
            return True
        else:
            return False
