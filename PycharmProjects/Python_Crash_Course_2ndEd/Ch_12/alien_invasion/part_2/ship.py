# PycharmProjects/Python_Crash_Course_2ndEd/Ch_12/alien_invasion/part_2
# Python 3.11
########################################################################
# Filename    : ship.py
# Description : alien invasion game ship, tutorial
# Author      : Python crash course, 2nd edition, chapter 12
########################################################################

import pygame

class Ship:
    """ A class to manage the ship"""

    def __init__(self, ai_game):
        """ Initialize the ship and its starting position"""
        self.screen = ai_game.screen

