from typing import List, Dict, Callable, Any
import datetime

from stats import Stats
from title import get_title


class TopList:
    def __init__(self, stats: Dict[str, List[Stats]]):
        self._stats = stats

    def _get_top_times_played(self) -> List[Stats]:
        return self._get_sorted(lambda x: x.times_played)

    def _get_top_total_time(self) -> List[Stats]:
        return self._get_sorted(lambda x: x.total_time)

    def _get_top_average(self) -> List[Stats]:
        return self._get_sorted(lambda x: x.average)

    def _get_top_median(self) -> List[Stats]:
        return self._get_sorted(lambda x: x.median)

    def _get_sorted(self, key: Callable[[Stats], Any]) -> List[Stats]:
        stats = [x for y in list(self._stats.values()) for x in y]
        return sorted(stats, key=key, reverse=True)

    @staticmethod
    def _trim_microseconds(td: datetime.timedelta) -> datetime.timedelta:
        return td - datetime.timedelta(microseconds=td.microseconds)

    def _get_top(self, criteria: str):
        if criteria == "total" or criteria is None:
            return self._get_top_total_time()
        elif criteria == "times":
            return self._get_top_times_played()
        elif criteria == "average":
            return self._get_top_average()
        elif criteria == "median":
            return self._get_top_median()

    def print_bar_chart(self, criteria: str, bar_length: int, list_length: int):
        top_list = self._get_top(criteria)
        f = None
        if criteria == "total" or criteria is None:

            def g(x):
                r = x.get_total_time_played()
                return r, str(datetime.timedelta(seconds=r))

            f = g
        elif criteria == "times":

            def g(x):
                r = x.get_times_played()
                return r, str(r)

            f = g
        elif criteria == "average":

            def g(x):
                r = x.get_average_session_time()
                return r, str(self._trim_microseconds(datetime.timedelta(seconds=r)))

            f = g
        elif criteria == "median":

            def g(x):
                r = x.get_median_session_time()
                return r, str(self._trim_microseconds(datetime.timedelta(seconds=r)))

            f = g

        max_value = max(f(x)[0] for x in top_list[:list_length])
        increment = max_value / bar_length
        longest_label_length = max(
            len(get_title(g.get_game(), g.get_system())) for g in top_list[:list_length]
        )
        longest_value_length = max(len(f(g)[1]) for g in top_list[:list_length])

        for g in top_list[:list_length]:
            value, value_string = f(g)
            bar_chunks, remainder = divmod(int(value * 8 / increment), 8)
            bar = "█" * bar_chunks
            title = get_title(g.get_game(), g.get_system())
            if remainder > 0:
                bar += chr(ord("█") + (8 - remainder))
            bar = bar or "▏"
            print(
                "{} ▏ {} {}".format(
                    title.rjust(longest_label_length),
                    value_string.rjust(longest_value_length),
                    bar,
                )
            )

    def print_list_entries(self, criteria, length: int):
        top_list = self._get_top(criteria)

        for i, g in enumerate(top_list[:length], start=1):
            list_entry = (
                "{} for {}, played {} times, " "time played: {}, avg: {}, median: {}"
            )
            title = get_title(g.get_game(), g.get_system())

            list_entry = list_entry.format(
                title,
                g.get_system(),
                g.get_times_played(),
                datetime.timedelta(seconds=g.get_total_time_played()),
                self._trim_microseconds(
                    datetime.timedelta(seconds=g.get_average_session_time())
                ),
                datetime.timedelta(seconds=g.get_median_session_time()),
            )
            print(i, list_entry)
