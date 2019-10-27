from typing import Dict, List
from datetime import datetime, timedelta

from session import Session


class Schedule:
    def __init__(self, sessions: Dict[str, Dict[str, List[Session]]]):
        self._schedule = {x: 0 for x in range(0, 24)}
        for system_name, system in sessions.items():
            for game_name, game in system.items():
                for session in game:
                    self.add_session(system, game, session.start, session.end)

    def add_session(self, system: str, game: str, start: datetime, end: datetime):
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

        self.add_session(system, game, bucket_end, end)

    def print(self):
        gradient = " ░░░▒▒▒▒▒▒▓▓▓▓▓▓▓▓▓████████████"
        max_value = max(self._schedule.values())
        increment = max_value / (len(blocks) - 1)
        result_num = ""
        result_blk = ""
        for hour in sorted(self._schedule):
            block = int(self._schedule[hour] // increment)
            result_num += " {} ".format(str(hour).rjust(2))
            result_blk += blocks[block] * 4
        print(result_num)
        print(result_blk)
