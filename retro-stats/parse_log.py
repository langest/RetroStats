import csv
from datetime import datetime
from typing import Dict, List, Callable, Optional
from collections import namedtuple
from collections import defaultdict

from session import Session

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def parse_log(
    path: str, skip_shorter_than: int = 0
) -> Dict[str, Dict[str, List[Session]]]:
    with open(path, "r") as f:
        fieldnames = ["date", "type", "system", "emulator", "path", "command"]
        rows = csv.DictReader(f, fieldnames, delimiter="|", skipinitialspace=True)
        sessions = defaultdict(lambda: defaultdict(lambda: []))
        SessionStart = namedtuple("SessionStart", "date system game")
        start = None
        for row in rows:
            date = datetime.strptime(row["date"], DATE_FORMAT)
            system = row["system"]
            game = row["path"]

            if row["type"] == "start":
                # Overwrite previous values if we didn't find an end tag
                start = SessionStart(date, system, game)

            elif row["type"] == "end":
                if not start.system == system or not start.game == start.game:
                    # Start and end mismatch, discard data
                    start = None
                    continue

                # Start and end matches
                end = datetime.strptime(row["date"], DATE_FORMAT)
                session = Session(start.date, end)
                if session.duration >= skip_shorter_than:
                    sessions[system][game].append(session)
                start = None
            else:
                raise ValueError("Bad type")
    return sessions
