

class Game:
    def __init__(self):
        self._score = 0
        self._Ships_saved = 0
        self._lives = 3
        self._difficulty = 0

        self._lives_updated = False
        self._score_updated = False
        self._ships_saved_updated = False

    def set_difficulty(self, difficulty):
        self._difficulty = difficulty

    def update_lives(self, amount):
        self._lives += amount
        self._lives_updated = True

    def get_lives(self):
        return self._lives

    def update_score(self, amount):
        self._score += amount
        self._score_updated = True

    def get_score(self):
        return self._score

    def update_ships_saved(self):
        self._Ships_saved += 1
        self._ships_saved_updated = True

    def get_ships_saved(self):
        return self._Ships_saved

    def get_updated_variables(self):
        return [self._lives_updated, self._score_updated, self._ships_saved_updated]
