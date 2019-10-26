class Session:
    def __init__(self, game, system, start, end):
        self.game = game
        self.start = start
        self.end = end
        self.duration = (end - start).total_seconds()
