from typing import List, Dict, Callable, Any

from stats import Stats


class TopList:
    def __init__(self, stats: Dict[str, List[Stats]]):
        self._stats = stats

    def get_top_times_played(
        self, system: str = None, exclude_systems: List[str] = None
    ) -> List[Stats]:
        return self._get_sorted(system, lambda x: x.times_played, exclude_systems)

    def get_top_total_time(
        self, system: str = None, exclude_systems: List[str] = None
    ) -> List[Stats]:
        return self._get_sorted(system, lambda x: x.total_time, exclude_systems)

    def get_top_average(
        self, system: str = None, exclude_systems: List[str] = None
    ) -> List[Stats]:
        return self._get_sorted(system, lambda x: x.average, exclude_systems)

    def get_top_median(
        self, system: str = None, exclude_systems: List[str] = None
    ) -> List[Stats]:
        return self._get_sorted(system, lambda x: x.median, exclude_systems)

    def _get_sorted(
        self,
        system: str,
        key: Callable[[Stats], Any],
        exclude_systems: List[str] = None,
    ) -> List[Stats]:
        if system is None:
            stats = [x for y in list(self._stats.values()) for x in y]
            if exclude_systems is not None:
                stats = filter(lambda x: x.get_system() not in exclude_systems, stats)
        else:
            if system not in self._stats:
                msg = "System {}, does not seem to have any valid stats"
                print(msg.format(system))
                return []
            stats = self._stats[system]

        return sorted(stats, key=key, reverse=True)
