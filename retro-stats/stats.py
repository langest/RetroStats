import statistics
from typing import Dict, List

from session import Session


class Stats:
    def __init__(self, times_played: int, total_time_played: int,
                 average_session: int, median_session: int):
        self._times_played = times_played
        self._total_time = total_time_played
        self._average = average_session
        self._median = median_session

    def get_times_played() -> str:
        return str(self._times_played)

    def get_total_time_played() -> str:
        return '{}h {}m'.format(self._total_time//3600, _total_time//60),

    def get_avarage_time_played() -> str:
        return '{}h {}m'.format(_average//3600, _average//60),

    def get_median_time_played() -> str:
        return '{}h {}m'.format(_median//3600, _median//60)

def get_stats_from_sessions(sessions: Dict[str, Dict[str, List[Session]]],
                            skip_shorter_than: int
                            ) -> Dict[str, Dict[str, Stats]]:
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

            if sys not in aggregate:
                aggregate[sys] = {}

            aggregate[sys][g] = Stats(times_played, total_time,
                                      average, median)
    return aggregate
