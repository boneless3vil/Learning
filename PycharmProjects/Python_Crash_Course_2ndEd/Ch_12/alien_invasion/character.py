# rocket.py
# chapter 12, page 233, 6428

import pygame

class Character:
    """ A class to manage the ship."""

    def __init__(self, ai_game):
        """ Initialize the ship and set it's starting position."""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()    # rect = what pygame calls rectangles

    # Load the ship image and get its rekt
        self.image = pygame.image.load('images/trump_fart_face.bmp')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.center = self.screen_rect.center

    def blitme(self):
        """ Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)