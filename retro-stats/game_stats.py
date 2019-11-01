import argparse
import os.path
from typing import Dict, Any

from parse_log import parse_log
from stats import get_stats_from_sessions, Stats
from top_list import TopList
from schedule import Schedule


def parse_args() -> Dict[str, Any]:
    desc = "Calculate some play statistics for your retro gaming"
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        "-n",
        "--list-length",
        type=int,
        default=25,
        help="how many entries to print int the top list, defaults to 25",
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        default="/home/pi/RetroPie/game_stats.log",
        help="path to the stats file, defaults to /home/pi/RetroPe/game_stats.log",
    )
    parser.add_argument(
        "-c",
        "--criteria",
        type=str,
        default=None,
        help="which criteria to order by, disabled for schedule option, "
        "available options "
        "are: total (time), times (played), "
        "average (session length), "
        "median (session length), "
        "defaults to total",
    )
    parser.add_argument(
        "-m",
        "--minimum-session-length",
        type=int,
        default=120,
        help="skip sessions shorter than this number of seconds, defaults to 120",
    )
    parser.add_argument(
        "-s",
        "--systems",
        type=str,
        default=None,
        nargs="+",
        help="the systems you want statistics for, default will use all systems",
    )
    parser.add_argument(
        "-e",
        "--exclude-systems",
        type=str,
        default=None,
        nargs="+",
        help="skip the listed systems, default no systems",
    )
    parser.add_argument(
        "-l",
        "--lookback",
        type=int,
        default=0,
        help="Number of days lookback to use for the stats, defaults to no limit (0)",
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-w",
        "--weekly-schedule",
        action="store_true",
        help="display weekly time schedule",
    )
    group.add_argument(
        "-b",
        "--bar-chart",
        type=int,
        help="display bar chart instead of numbers, integer sets bar length",
    )

    return vars(parser.parse_args())


def main():
    args = parse_args()

    sessions = {}
    sessions = parse_log(
        args["file"],
        args["systems"],
        args["exclude_systems"],
        args["minimum_session_length"],
        args["lookback"],
    )
    if len(sessions) == 0:
        print("No sessions found")

    if args["weekly_schedule"]:
        schedule = Schedule(sessions)
        schedule.print_schedule()
        return

    stats = get_stats_from_sessions(sessions)
    top = TopList(stats)

    criteria = args["criteria"]

    if not args["bar_chart"] is None:
        top.print_bar_chart(
            criteria if args["bar_chart"] else None,
            args["bar_chart"],
            args["list_length"],
        )
        return

    top.print_list_entries(criteria, args["list_length"])


if __name__ == "__main__":
    main()
