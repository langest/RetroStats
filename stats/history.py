from typing import Dict, List

from session import Session
from title import get_title


class History:
    def __init__(
        self, sessions: Dict[str, Dict[str, List[Session]]], list_length: int = -1
    ):
        history = []
        for system, g in sessions.items():
            for game, s in g.items():
                for session in s:
                    info = {
                        "system": system,
                        "game": get_title(game, system),
                        "session": session,
                    }
                    history.append(info)
        history.sort(key=lambda x: x["session"].start, reverse=True)
        self._history = history[:list_length]

    def print_history(self):
        for session in self._history:
            print(session["session"].start, session["system"], session["game"])
