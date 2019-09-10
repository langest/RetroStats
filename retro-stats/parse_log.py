import csv
import os.path
from datetime import datetime
from typing import Dict, List, Callable

from session import Session

def parse_log(path: str,
              get_title: Callable[[str, str], str]
              ) -> Dict[str, Dict[str, List[Session]]]:
    with open(path, 'r') as f:
        fieldnames = ['date', 'type', 'system', 'emulator', 'path', 'command']
        rows = csv.DictReader(f, fieldnames, delimiter='|',
                              skipinitialspace=True)
        sessions = {}
        current_session = None
        for row in rows:
            system = row['system']
            game = get_title(row['path'], system)
            if game is None:
                game = os.path.basename(row['path'])

            if row['type'] == 'start':
                if current_session is not None:
                    print('Mismatch, missing end: ', current_session)
                d = datetime.strptime(row['date'], '%a %d %b %H:%M:%S %Z %Y')
                current_session = Session(game, row['system'], d)
            elif current_session is not None and row['type'] == 'end':
                if not game == current_session.game:
                    # Start and end mismatch, discard both
                    print('Mismatch of start and end:',
                          current_session)
                    current_session = None
                    continue
                end = datetime.strptime(row['date'], '%a %d %b %H:%M:%S %Z %Y')
                duration = (end - current_session.start).total_seconds()
                current_session.duration = duration
                if system in sessions:
                    if game in sessions[system]:
                        sessions[system][game].append(current_session)
                    else:
                        sessions[system][game] = [current_session]
                else:
                    sessions[system] = { game: [current_session] }
                current_session = None
            else:
                raise ValueError('Bad type')
    return sessions
