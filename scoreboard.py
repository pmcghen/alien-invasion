"""Implement scoring and high scores."""
import pygame.font
from pygame.sprite import Group
import json
import math

from ship import Ship


class Scoreboard:
    """Report scoring information."""
    def __init__(self, ai_game):
        """Initialize score keeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        self.new_high_score_set = False

        self.text_color = (233, 233, 233)
        self.font = pygame.font.SysFont(None, 24)

        self.prep_images()

    def prep_images(self):
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """Turn the score into a rendered image."""
        score_str = "{:,}".format(self.stats.score)
        self.score_image = self.font.render(score_str, True, self.text_color, self.settings.bg_color)

        # Display the score at the top right of screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 10
        self.score_rect.top = 10

    def prep_high_score(self):
        """Turn the high score into an image."""
        high_score_str = "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(high_score_str, True, self.text_color, self.settings.bg_color)

        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into an image."""
        level_str = f'Level {str(self.stats.level)}'
        self.level_image = self.font.render(level_str, True, self.text_color, self.settings.bg_color)

        self.level_rect = self.level_image.get_rect()
        self.level_rect.left = self.screen_rect.left + 10
        self.level_rect.top = 10

    def prep_ships(self):
        """Show how many ships are left."""
        self.ships = Group()

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)
            ship.image = ship.image_small
            ship.rect.x = (self.level_rect.right + 10) + ship_number * (ship.rect.width * .66)
            ship.rect.y = 10
            self.ships.add(ship)

    def check_extra_life_award(self):
        """If the player reaches the extra life threshold, add to their available ships."""
        current_bonus = math.floor(self.stats.score / self.settings.extra_life_award)
        bonus_sound_effect = pygame.mixer.Sound('sounds/bonus.wav')

        if current_bonus > self.stats.extra_lives_awarded:
            self.stats.ships_left += 1
            self.stats.extra_lives_awarded += 1
            self.settings.extra_life_award = self.settings.extra_life_award * self.settings.extra_life_scale
            self.prep_ships()
            bonus_sound_effect.play()

    def show_score(self):
        """Draw the score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            high_score_leaderboard = 'data/high_scores.json'

            if not self.new_high_score_set:
                new_high_score_sound_effect = pygame.mixer.Sound('sounds/high-score.wav')
                self.new_high_score_set = True
                new_high_score_sound_effect.play()

            try:
                with open(high_score_leaderboard, 'w', encoding='utf-8') as hs:
                    json.dump(self.stats.score, hs)
            except:
                # TODO: Proper error handling is needed here.
                pass

            self.prep_high_score()
