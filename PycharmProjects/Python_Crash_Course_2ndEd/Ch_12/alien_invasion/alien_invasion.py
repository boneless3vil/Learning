# alien_invasion.py
# CREATING A PYGAME WINDOW AND RESPONDING TO USER INPUT

import sys  # tools to exit game when player quits

import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from character import Character
from alien import Alien

class AlienInvasion:
    """ Overall class to manage game assets in behavior."""

    def __init__(self):
        """ Initialize the game, and create game resources."""

        pygame.init()   # initialize game engine background settings
        self.settings = Settings()
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()
        self.ship = Ship(self)
        self.character = Character(self)

        # run game in full screen
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

        # display settings
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        # 2 create a display window
        self.screen = pygame.display.set_mode((self.settings.screen_width,
                                              self.settings.screen_height))
        #    self.screen also called a "surface"
        pygame.display.set_caption("Alien Invasion")
        # set the background color
        self.bg_color = (230, 230, 230)

    def _create_fleet(self):
        """ Create the fleet of aliens."""
        # Make an alien.
        alien = Alien(self)
        self.aliens.add(alien)

    def run_game(self):
        """ Start the main loop for the game."""

        while True:
            self._check_events()    # helper method, page 235, 6512
            self.ship.update()
            self.bullets.update()
            self._update_screen()

    def _check_events(self):
    # watch for keyboard and mouse events. "events" = actions user performs while playing game
        for event in pygame.event.get():    # returns list of events since last time function was called
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        """ Respond to keypresses"""
        if event.key == pygame.K_RIGHT:
            # move the ship to the right.
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # move the ship to the left.
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

        # to quit game
        elif event.key == pygame.K_q:
            sys.exit()

    def _check_keyup_events(self, event):
        """ respond to key releases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """ Create a new bullet and add it to the bullets group."""
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_screen(self):
    # Redraw the screen during each pass through the loop.
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()  # draw ship on screen
        self.character.blitme()
        for bullet in self.bullets.sprites(): # returns list of all sprites in group bullets
            bullet.draw_bullet()

    # Make the most recently drawn screen visible.
        pygame.display.flip()   # continually updates positions of game elements, hiding old ones
        # and creating the illusion of smooth movement.

if  __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()