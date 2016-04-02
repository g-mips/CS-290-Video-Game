import pygame

import objects
import logger

class PlayerInput(object):
    ACCELERATION = 3
    MAX_ACCELERATION = 1
    AVAILABLE_KEYS = [ pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_SPACE ]
    
    def __init__(self):
        self.events = []

    def register_event(self, event):
        self.events.append(event)
    
    def update(self, game_object):
        '''
        This will update the game_object's movement. by checking the keys that are up and down.
        '''

        # Add the most recent event.
        for event in self.events:
            if event.type == pygame.KEYDOWN and event.key in self.AVAILABLE_KEYS:
                if event.key in game_object.keys_up:
                    game_object.keys_up.remove(event.key)
                if event.key not in game_object.keys_down:
                    game_object.keys_down.append(event.key)

            elif event.type == pygame.KEYUP and event.key in self.AVAILABLE_KEYS:
                if event.key in game_object.keys_down:
                    game_object.keys_down.remove(event.key)
                if event.key not in game_object.keys_up:
                    game_object.keys_up.append(event.key)
        self.events = []

        # Execute the keys that are down
        for event in game_object.keys_down:
            if event == pygame.K_RIGHT:
                game_object.dx = self.ACCELERATION
            elif event == pygame.K_LEFT:
                game_object.dx = -self.ACCELERATION
            elif event == pygame.K_SPACE and game_object.dy == 0:
                game_object.dy = -self.ACCELERATION
                game_object.air_time = 1

        # Execute the keys that are up
        for event in game_object.keys_up:
            if event == pygame.K_RIGHT:
                game_object.dx = 0
            elif event == pygame.K_LEFT:
                game_object.dx = 0
            elif event == pygame.K_SPACE:
                game_object.dy = self.ACCELERATION
                game_object.air_time = 0

        game_object.keys_up = []
