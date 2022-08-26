"""Keep track of game events."""
import json


class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialize statistics."""
        self.settings = ai_game.settings
        self.reset_stats()
        self.first_run = True
        self.game_active = False
        self.game_over = False
        self.high_score = 0
        self.extra_lives_awarded = 0

        high_score_leaderboard = 'data/high_scores.json'

        with open(high_score_leaderboard, encoding='utf-8') as hs:
            high_score = json.load(hs)
            self.high_score = high_score

    def reset_stats(self):
        """Initialize the statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
