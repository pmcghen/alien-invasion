"""Gameplay and asset settings for Alien Invasion."""
import pygame


class Settings:
    """All the settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's static settings."""
        self.screen_width = 800
        self.screen_height = 600
        self.bg_color = (0, 0, 0)
        self.bg_img = pygame.image.load('images/bg.png')

        self.ship_limit = 3

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (66, 66, 66)
        self.bullets_allowed = 5

        self.fleet_drop_speed = 10

        self.speedup_scale = 1.1
        self.score_scale = 1.5

        self.extra_life_award = 10000

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that will change as the game progresses."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.0
        self.alien_speed = 0.5
        # fleet_direction = 1: move right. -1, move left.
        self.fleet_direction = 1
        self.alien_points = 10

    def increase_speed(self):
        """Increase the speed settings and point values."""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
