from datetime import datetime
from datetime import timedelta

from stats.log import Log

class LogCache:
    def __init__(self, path, refresh_interval):
        self._path = path
        self._update_cache()
        self._refresh_interval = timedelta(minutes=refresh_interval)

    def _update_cache(self):
        self._log = Log(self._path)
        self._time = datetime.now()

    def get_log(self):
        if self._time - datetime.now() < self._refresh_interval:
            self._update_cache()
        return self._log
