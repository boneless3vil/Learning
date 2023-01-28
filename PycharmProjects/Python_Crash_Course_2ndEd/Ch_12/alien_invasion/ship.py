# ship.py --> alien_invasion.py
# Python crash course 2nd edition, page 233, 6428

import pygame

class Ship:
    """ class to manage player ship"""
    def __init__(self):
        """ Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

      # self.image = pygame.image.load('images/butt.bmp')
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
      # Load the ship image and get its rect
        self.image = pygame.image.load('images/butt.bmp')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """ Draw the ship at its current location using blitme()."""
        self.screen.blit(self.image, self.rect)
        
