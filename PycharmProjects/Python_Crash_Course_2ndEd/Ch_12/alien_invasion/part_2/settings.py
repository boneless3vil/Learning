# PycharmProjects/Python_Crash_Course_2ndEd/Ch_12/alien_invasion/part_1
# Python 3.11
########################################################################
# Filename    : settings.py
# Description : alien invasion game settings, tutorial
# Author      : Python crash course, 2nd edition, chapter 12
########################################################################

class Settings:
    """ A class to store game settings for Alien Invasion"""

    def __init__(self):
        """ Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
