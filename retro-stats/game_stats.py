import argparse

from parse_log import parse_log
from stats import get_stats_from_sessions
from top_list import TopList

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='path to the stats file')
    parser.add_argument('-s', '--skip-shorter-than', type=int, default=120,
                        help='skip sessions shorter than this number of '
                             'seconds, defaults to 120')

    args = vars(parser.parse_args())
    sessions = parse_log(args['file'])
    stats = get_stats_from_sessions(sessions, args['skip_shorter_than'])
    top = TopList(stats)
    for g in top.get_top_total_time():
        print('{} for {}, time played: {}, avg: {}, median: {}'.format(
            g.get_game(), g.get_system(), g.get_total_time_played(),
            g.get_average_session_time(), g.get_median_session_time()))

if __name__ == "__main__":
    main()
