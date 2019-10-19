import statistics
import datetime
from typing import Dict, List

from session import Session


class Stats:
    def __init__(
        self,
        game: str,
        system: str,
        times_played: int,
        total_time_played: int,
        average_session: int,
        median_session: int,
    ):
        self.game = game
        self.system = system
        self.times_played = times_played
        self.total_time = total_time_played
        self.average = average_session
        self.median = median_session

    def get_game(self) -> str:
        return self.game

    def get_system(self) -> str:
        return self.system

    def get_times_played(self) -> str:
        return str(self.times_played)

    def get_total_time_played(self) -> str:
        return str(datetime.timedelta(seconds=self.total_time))

    def get_average_session_time(self) -> str:
        return str(datetime.timedelta(seconds=self.average))

    def get_median_session_time(self) -> str:
        return str(datetime.timedelta(seconds=self.median))


def get_stats_from_sessions(
    sessions: Dict[str, Dict[str, List[Session]]], skip_shorter_than: int
) -> Dict[str, List[Stats]]:
    aggregate = {}
    for sys in sessions:
        system = sessions[sys]
        for g in system:
            game = system[g]
            times_played = len(game)
            total_time = 0
            session_lengths = []
            for session in game:
                if skip_shorter_than and session.duration < skip_shorter_than:
                    times_played -= 1
                    continue
                session_lengths.append(session.duration)
                total_time += session.duration
            average = 0
            median = 0
            if times_played > 0:
                average = total_time / times_played
                median = statistics.median(session_lengths)

            stats = Stats(g, sys, times_played, total_time, average, median)
            if sys in aggregate:
                aggregate[sys].append(stats)
            else:
                aggregate[sys] = [stats]
    return aggregate
