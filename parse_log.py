import csv
import os.path
from datetime import datetime

from session import Session

def parse_log(path):
    with open(path, 'r') as f:
        fieldnames = ['date', 'type', 'system', 'emulator', 'path', 'command']
        rows = csv.DictReader(f, fieldnames, delimiter='|',
                              skipinitialspace=True)
        sessions = {}
        current_session = None
        for row in rows:
            game = os.path.basename(row['path'])
            if row['type'] == 'start':
                if current_session is not None:
                    print(f'Mismatch: {current_session}')
                d = datetime.strptime(row['date'], '%a %d %b %H:%M:%S %Z %Y')
                current_session = Session(game, row['system'], d)
            elif current_session is not None and row['type'] == 'end':
                if not game == current_session.game:
                    # Start and end mismatch, discard both
                    print(f'Mismatch: {current_session} and {row}')
                    current_session = None
                    continue
                end = datetime.strptime(row['date'], '%a %d %b %H:%M:%S %Z %Y')
                duration = (end - current_session.start).total_seconds()
                current_session.duration = duration
                if game in sessions:
                    sessions[game].append(current_session)
                else:
                    sessions[game] = [current_session]
                current_session = None
            else:
                raise ValueError('Bad type')
    for k in sessions:
        for i in sessions[k]:
            print(i.__dict__)
    return sessions
