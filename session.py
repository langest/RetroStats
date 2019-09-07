class Session:
    def __init__(self, game, system, start, duration = None):
        self.game = game
        self.system = system
        self.start = start
        self.duration = duration
