import csv
import datetime
from typing import Dict, List, Callable, Optional
from collections import namedtuple
from collections import defaultdict

from session import Session

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"


def parse_log(
    path: str,
    systems: Optional[List[str]] = None,
    exclude_systems: Optional[List[str]] = None,
    skip_shorter_than: Optional[int] = 0,
    lookback: int = 0,
) -> Dict[str, Dict[str, List[Session]]]:
    start_date = datetime.datetime.min
    if lookback > 0:
        start_date = datetime.datetime.now()
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_date -= datetime.timedelta(days=lookback)
    start_date = start_date.replace(tzinfo=datetime.timezone.utc)

    with open(path, "r") as f:
        fieldnames = ["date", "type", "system", "emulator", "path", "command"]
        rows = csv.DictReader(f, fieldnames, delimiter="|", skipinitialspace=True)
        sessions = defaultdict(lambda: defaultdict(lambda: []))
        SessionStart = namedtuple("SessionStart", "date system game")
        start = None
        for row in rows:
            system = row["system"]
            if systems is not None and system not in systems:
                continue
            if exclude_systems is not None and system in exclude_systems:
                continue

            date = datetime.datetime.strptime(row["date"], DATE_FORMAT)
            if date < start_date:
                continue
            game = row["path"]

            if row["type"] == "start":
                # Overwrite previous values if we didn't find an end tag
                start = SessionStart(date, system, game)

            elif row["type"] == "end":
                if start is None:
                    # Missing start for this end
                    continue
                if not start.system == system or not start.game == start.game:
                    # Start and end mismatch, discard data
                    start = None
                    continue

                # Start and end matches
                end = datetime.datetime.strptime(row["date"], DATE_FORMAT)
                session = Session(start.date, end)
                if session.duration >= skip_shorter_than:
                    sessions[system][game].append(session)
                start = None
            else:
                raise ValueError("Bad type")
    return sessions
