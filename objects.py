import pygame
import game_input

class GameObject(object):
    def __init__(self, input):
        self.input = input
        self.dead  = False
        self.velocity = 0
        self.x = 0
        self.y = 0

    def update(self, event):
        self.input.update(self, event)


class Alien(GameObject):
    def __init(self, input):
        super(Alien, self).__init__(game_input.PlayerInput)
