# alien_invasion/ship.py
# chapter 12, page 233, 6428

import pygame

class Ship:
    """ A class to manage the ship."""

    def __init__(self, ai_game):
        """ Initialize the ship and set it's starting position."""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()    # rect = what pygame calls rectangles

    # Load the ship image and get its rekt
        self.image = pygame.image.load('images/butt.bmp')
        self.rect = self.image.get_rect()
        # Start each new ship at the bottom center of the screen.
        self.rect.midbottom = self.screen_rect.midbottom

        # Store decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # Movement flag
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """ Update the ship's position based on the movement flag"""
        # Update the ship's x value, not the rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.rect.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.screen_rect.left:
            self.rect.x -= self.settings.ship_speed    # -= used to move left

    def blitme(self):
        """ Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)