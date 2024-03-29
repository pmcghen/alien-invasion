"""Alien Invasion is a Space Invaders clone written in Python."""
import sys
import pygame

from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """Container class to manage game assets and behavior."""

    def __init__(self):
        """Initialize the game, create game resources."""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                               self.settings.screen_height))
        pygame.display.set_caption('Alien Invasion!')

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.play_button = Button(self, 'PLAY')

    def run_game(self):
        """Start the main loop."""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()

    def start_game(self):
        self.settings.initialize_dynamic_settings()
        self.stats.reset_stats()
        self.stats.game_active = True
        self.stats.first_run = False
        self.stats.game_over = False

        self.sb.prep_images()
        pygame.mixer.music.load('sounds/background.wav')
        pygame.mixer.music.play(-1)

        self.aliens.empty()
        self.bullets.empty()

        self._create_fleet()
        self.ship.center_ship()
        pygame.mouse.set_visible(False)

    def end_game(self):
        last_ship_hit_sound_effect = pygame.mixer.Sound('sounds/game-over.wav')

        last_ship_hit_sound_effect.play()
        self.stats.game_active = False
        self.stats.game_over = True
        pygame.mixer.music.stop()
        pygame.mouse.set_visible(True)

    def _check_events(self):
        """Respond to keyboard and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keydown events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key != pygame.K_q and not self.stats.game_active:
            self.start_game()

    def _check_keyup_events(self, event):
        """Respond to keyup events."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)

        if button_clicked and not self.stats.game_active:
            self.play_button.rect.collidepoint(mouse_pos)
            self.start_game()

    def _update_bullets(self):
        """Update the position of bullets and remove old bullets."""
        self.bullets.update()

        # Delete bullets from group when they leave the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet/alien collisions."""
        alien_hit_sound_effect = pygame.mixer.Sound('sounds/alien-hit.wav')
        # Check for collisions and remove affected elements.
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                alien_hit_sound_effect.play()

            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.check_extra_life_award()

        if not self.aliens:
            # Destroy remaining bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.stats.level += 1
            self.sb.prep_level()

    def _update_aliens(self):
        """
        Check if the fleet is at an edge,
        then update the positions of all aliens in the fleet
        """
        self._check_fleet_edges()
        self.aliens.update()

        # Look for alien/ship collisions.
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        self._check_aliens_bottom()

    def _create_fleet(self):
        """Create the fleet of aliens."""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = self.settings.screen_height - (3 * alien_height) - ship_height
        number_rows = available_space_y // (4 * alien_height)

        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """Create an alien and place it in the row"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number

        self.aliens.add(alien)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()

        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_fleet_edges(self):
        """Respond to aliens reaching the edge of the screen."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet down and change direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to aliens hitting the ship."""
        ship_hit_sound_effect = pygame.mixer.Sound('sounds/ship-explosion.wav')
        if self.stats.ships_left > 0:
            self.stats.ships_left -= 1
            ship_hit_sound_effect.play()

            self.sb.prep_ships()

            self.aliens.empty()
            self.bullets.empty()

            self._create_fleet()
            self.ship.center_ship()

            sleep(0.5)
        else:
            self.end_game()

    def _update_screen(self):
        """Update the screen."""
        self.screen.blit(self.settings.bg_img, (0, 0))
        self.ship.blitme()

        for bullet in self.bullets.sprites():
            bullet.draw_bullet()

        self.aliens.draw(self.screen)

        self.sb.show_score()

        if self.stats.first_run:
            title_img = pygame.image.load('images/title.png')
            self.screen.blit(title_img, (100, 80))

        if self.stats.game_over:
            font = pygame.font.SysFont("Pixeboy", 54)
            game_over_msg = font.render('GAME OVER', True, (255, 255, 255))
            self.screen.blit(game_over_msg, (296, 230))

        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _fire_bullet(self):
        """Fire a bullet when spacebar is pressed."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
