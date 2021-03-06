"""Aliens can't invade if there are no aliens, right?"""
import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """A single alien in the fleet."""

    def __init__(self, ai_game):
        """Initialize the alien and set its starting position."""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.main_image = pygame.image.load('images/alien.png')
        self.alt_image = pygame.image.load('images/alien_out.png')
        self.image = self.main_image
        self.rect = self.image.get_rect()

        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store the alien's exact horizontal position.
        self.x = float(self.rect.x)

    def check_edges(self):
        """Return True if an alien is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """Move the alien to the right or left."""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

        if self.image == self.main_image:
            self.image = self.alt_image
        else:
            self.image = self.main_image
