import statistics

def get_stats_from_sessions(sessions, skip_shorter_than):
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
            average = total_time / times_played
            median = statistics.median(session_lengths)

            if sys not in aggregate:
                aggregate[sys] = {}

            time_played_str = '{}h {}m'.format(total_time//3600, total_time//60),
            average_str = '{}h {}m'.format(average//3600, average//60),
            median_str = '{}h {}m'.format(median//3600, median//60)
            aggregate[sys][g] = {
                    'times_played': times_played,
                    'total_time_played': time_played_str,
                    'average_session_length': average_str,
                    'median_session_length': median_str
                }
    return aggregate
