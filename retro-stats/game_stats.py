import argparse

from parse_log import parse_log
from stats import get_stats_from_sessions

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
    print(stats)

if __name__ == "__main__":
    main()
