import csv
from datetime import datetime
from typing import Dict, List, Callable, Optional

from session import Session

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def parse_log(path: str,) -> Dict[str, Dict[str, List[Session]]]:
    with open(path, "r") as f:
        fieldnames = ["date", "type", "system", "emulator", "path", "command"]
        rows = csv.DictReader(f, fieldnames, delimiter="|", skipinitialspace=True)
        sessions = {}
        current_session = None
        for row in rows:
            system = row["system"]
            game = row["path"]

            if row["type"] == "start":
                # Overwrite previous start if we didn't find an end tag
                d = datetime.strptime(row["date"], DATE_FORMAT)
                current_session = Session(game, row["system"], d)
            elif current_session is not None and row["type"] == "end":
                if not game == current_session.game:
                    # Start and end mismatch, discard both
                    current_session = None
                    continue
                end = datetime.strptime(row["date"], DATE_FORMAT)
                duration = (end - current_session.start).total_seconds()
                current_session.duration = duration
                if system in sessions:
                    if game in sessions[system]:
                        sessions[system][game].append(current_session)
                    else:
                        sessions[system][game] = [current_session]
                else:
                    sessions[system] = {game: [current_session]}
                current_session = None
            else:
                raise ValueError("Bad type")
    return sessions
