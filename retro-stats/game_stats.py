import argparse
import os.path
import datetime

from parse_log import parse_log
from stats import get_stats_from_sessions
from top_list import TopList
from title_info import get_title


def print_list_entries(top_list, length):
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
            datetime.timedelta(seconds=g.get_average_session_time()),
            datetime.timedelta(seconds=g.get_median_session_time()),
        )
        print(i, list_entry)


def main():
    desc = "Calculate some play statistics for your retro gaming"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-n",
        "--list-length",
        type=int,
        default=25,
        help="how many entries to print int the top list",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="/home/pi/RetroPie/game_stats.log",
        help="path to the stats file",
    )
    parser.add_argument(
        "-c",
        "--criteria",
        type=str,
        default=None,
        help="which criteria to order by, available options "
        "are: total (time), times (played), "
        "average (session length), "
        "median (session length), "
        "defaults to total",
    )
    parser.add_argument(
        "-s",
        "--system",
        type=str,
        default=None,
        help="the system you want statistics for, if omitted, will use all systems",
    )
    parser.add_argument(
        "-m",
        "--minimum-session-length",
        type=int,
        default=120,
        help="skip sessions shorter than this number of seconds, defaults to 120",
    )
    parser.add_argument(
        "-b",
        "--bar-chart",
        default=False,
        help="display bar chart instead of numbers",
        action="store_true",
    )

    args = vars(parser.parse_args())

    sessions = {}
    sessions = parse_log(args["file"])
    stats = get_stats_from_sessions(sessions, args["minimum_session_length"])
    top = TopList(stats)

    sys = args["system"]
    criteria = args["criteria"]
    top_list = []
    if criteria == "total" or criteria is None:
        top_list = top.get_top_total_time(sys)
    elif criteria == "times":
        top_list = top.get_top_times_played(sys)
    elif criteria == "average":
        top_list = top.get_top_average(sys)
    elif criteria == "median":
        top_list = top.get_top_median(sys)

    if args["bar_chart"] is None:
        print_list_entries(top_list, args["list_length"])
    else:
        print_bar_chart(
            top_list, criteria if args["bar_chart"] else None, args["list_length"]
        )


if __name__ == "__main__":
    main()
