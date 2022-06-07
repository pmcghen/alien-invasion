"""Gameplay and asset settings for Alien Invasion."""
class Settings:
    """All the settings for Alien Invasion"""

    def __init__(self):
        """Initialize the game's settings."""
        self.screen_width = 1024
        self.screen_height = 768
        self.bg_color = (33,26,33)

        self.ship_speed = 1.5
        self.ship_limit = 3

        self.bullet_speed = 1.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (66,66,66)
        self.bullets_allowed = 5

        self.alien_speed = 1.0
        self.fleet_drop_speed = 10
        # fleet_direction = 1: move right. -1, move left.
        self.fleet_direction = 1
