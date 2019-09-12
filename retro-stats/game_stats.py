import argparse
import os.path

from parse_log import parse_log
from stats import get_stats_from_sessions
from top_list import TopList
from skyscraper import get_skyscraper_callable

def main():
    desc = 'Calculate some play statistics for your retro gaming'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='path to the stats file')
    parser.add_argument('-c', '--criteria', type=str, required=False,
                        default=None,
                        help='which criteria to order by, available options '
                             'are: total (time), times (played), '
                             'average (session length), '
                             'median (session length), '
                             'defaults to total')
    parser.add_argument('-s', '--system', type=str, default=None,
                        help='the system you want statistics for, '
                             'if omitted, will use all systems')
    parser.add_argument('-m', '--minimum-session-length', type=int, default=120,
                        help='skip sessions shorter than this number of '
                             'seconds, defaults to 120')
    parser.add_argument('-t', '--skyscraper-title-cache', type=str,
                        default=None,
                        help='the path to your skyscraper cache,'
                             'if provided, will use skyscraper db '
                             'to get game titles instead of filenames')

    args = vars(parser.parse_args())

    skyscraper_cache_path = args['skyscraper_title_cache']
    skyscraper_callable = None
    sessions = {}
    if skyscraper_cache_path:
        skyscraper_callable = get_skyscraper_callable(skyscraper_cache_path)
        sessions = parse_log(args['file'], skyscraper_callable)
    else:
        sessions = parse_log(args['file'], lambda x, y: os.path.basename(x))
    stats = get_stats_from_sessions(sessions, args['minimum_session_length'])
    top = TopList(stats)

    sys = args['system']
    criteria = args['criteria']
    top_list = []
    if criteria == 'total' or criteria is None:
        top_list = enumerate(top.get_top_total_time(sys), start=1)
    elif criteria == 'times':
        top_list = enumerate(top.get_top_times_played(sys), start=1)
    elif criteria == 'average':
        top_list = enumerate(top.get_top_average(sys), start=1)
    elif criteria == 'median':
        top_list = enumerate(top.get_top_median(sys), start=1)
    for i, g in top_list:
        list_entry = ('{} for {}, played {} times, '
                      'time played: {}, avg: {}, median: {}')
        list_entry = list_entry.format(g.get_game(),
                                       g.get_system(),
                                       g.get_times_played(),
                                       g.get_total_time_played(),
                                       g.get_average_session_time(),
                                       g.get_median_session_time())
        print(i, list_entry)

if __name__ == "__main__":
    main()
