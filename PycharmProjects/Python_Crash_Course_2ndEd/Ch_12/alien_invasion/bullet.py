# alien_invasion/bullet.py

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """ A class to manage bullets fired from the ship"""

    def __init__(self, ai_game):
        """Create a bullet object at the ship's current position."""
        super().__init__()  #inherits from Sprite, so need super()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

    # Create a bullet rect at (0, 0) and then set correct position.
        # bullet built from scratch.image, so need rect attr. created
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop  # so bullet comes from top of ship

    # Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):   # update, manages bullet position
        """ Move the bullet up the screen."""
        self.y -= self.settings.bullet_speed
        # Update the rect position
        self.rect.y = self.y

        def draw_bullet(self):
            """ Draw the bullet to the screen."""
            pygame.draw.rect(self.screen, self.color, self.rect)


