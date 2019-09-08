from typing import List, Dict, Callable, Any

from stats import Stats

class TopList:
    def __init__(self, stats: Dict[str, List[Stats]]):
        self._stats = stats

    def get_top_times_played(self, system: str = None) -> List[Stats]:
        return self._get_sorted(system, lambda x : x.time_played)

    def get_top_total_time(self, system: str = None) -> List[Stats]:
        return self._get_sorted(system, lambda x : x.total_time)

    def get_top_average(self, system: str = None) -> List[Stats]:
        return self._get_sorted(system, lambda x : x.average)

    def get_top_median(self, system: str = None) -> List[Stats]:
        return self._get_sorted(system, lambda x : x.median)

    def _get_sorted(self, system: str, key: Callable[[Stats], Any]) -> List[Stats]:
        if system is None:
            stats = [x for y in list(self._stats.values()) for x in y]
        else:
            assert system in self._stats
            stats = self._stats[system]

        return sorted(stats, key=key, reverse=True)
