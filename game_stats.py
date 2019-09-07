import argparse
import statistics

from parse_log import parse_log

def get_stats(sessions, skip_shorter_than):
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
            avarage = total_time / times_played
            median = statistics.median(session_lengths)

            if sys not in aggregate:
                aggregate[sys] = {}
            aggregate[sys][g] = {
                    'times_played': times_played,
                    'total_time_played': f'{total_time//3600}h '
                                         f'{total_time//60}m',
                    'avarage_session_length': f'{avarage//3600}h '
                                              f'{avarage//60}m',
                    'median_session_length': f'{median//3600}h '
                                             f'{median//60}m'
                }
    return aggregate

def main():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-f', '--file', type=str, required=True,
                        help='path to the stats file')
    parser.add_argument('-s', '--skip-shorter-than', type=int, default=120,
                        help='skip sessions shorter '
                             'than this number of seconds')

    args = vars(parser.parse_args())
    sessions = parse_log(args['file'])
    stats = get_stats(sessions, args['skip_shorter_than'])
    print(stats)

if __name__ == "__main__":
    main()
