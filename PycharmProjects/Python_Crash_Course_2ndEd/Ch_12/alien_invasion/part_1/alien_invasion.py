# PycharmProjects/Python_Crash_Course_2ndEd/Ch_12/alien_invasion/
# Python 3.11
########################################################################
# Filename    : alien_invasion.py
# Description : alien invasion game tutorial
# Author      : Python crash course, 2nd edition, chapter 12
########################################################################

import sys  # for player to exit the game

import pygame
from settings import Settings


class AlienInvasion:
    """ Overall class to manage game assets and behaviors."""

    def __init__(self):     # initialize background settings for pygame
        """ Initialize the game, and create resources."""
        pygame.init()
        self.settings = Settings()

        # create a display window
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Set the background color
        self.screen.fill(self.settings.bg_color)

    def run_game(self):
        """ Start the main loop for the game."""
        while True:
            # Watch for keyboard and mouse events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            # Redraw the screen during each pass through the loop.
            self.screen.fill(self.bg_color)

            # Make the most recently drawn screen visible. updates elements as
            # they move
            pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()

