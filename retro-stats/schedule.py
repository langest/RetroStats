from typing import Dict, List
from datetime import datetime, timedelta

from session import Session


class Schedule:
    def __init__(self, sessions: Dict[str, Dict[str, List[Session]]]):
        self._schedule = {x: 0 for x in range(0, 24)}
        for system_name, system in sessions.items():
            for game_name, game in system.items():
                for session in game:
                    self._add_session(system, game, session.start, session.end)
        local = datetime.now()
        utc = datetime.utcnow()
        diff = (
            int((local - utc).days * 86400 + round((local - utc).seconds, -1)) // 3600
        )
        tmp = {}
        for k, v in self._schedule.items():
            tmp[(k + diff) % 24] = v
        self._schedule = tmp

    def _add_session(self, system: str, game: str, start: datetime, end: datetime):
        bucket = start.hour
        if end.hour == bucket:
            self._schedule[bucket] += (end - start).total_seconds()
            return
        bucket_end = (
            start
            - timedelta(
                minutes=start.minute,
                seconds=start.second,
                microseconds=start.microsecond,
            )
            + timedelta(hours=1)
        )
        self._schedule[bucket] += (bucket_end - start).total_seconds()

        self._add_session(system, game, bucket_end, end)

    def print_daily_schedule(self):
        gradient = " ░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓████████████"
        max_value = max(self._schedule.values())
        increment = max_value / (len(gradient) - 1)
        result_num = ""
        result_blk = ""
        for hour in sorted(self._schedule):
            block = int(self._schedule[hour] // increment)
            result_num += " {} ".format(str(hour).rjust(2))
            result_blk += gradient[block] * 4
        print(result_num)
        print(result_blk)
