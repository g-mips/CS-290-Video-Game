import pygame

import objects
import logger

class PlayerInput(object):
    ACCELERATION = 1
    MAX_ACCELERATION = 1
    AVAILABLE_KEYS = { "MOVE": [ pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_SPACE ] }
    
    def __init__(self):
        self.event = None

    def register_event(self, event):
        self.event = event
    
    def update(self, game_object):
        if self.event is not None:
            print(game_object.events)
            
            if self.event.type == pygame.KEYDOWN and self.event.key in self.AVAILABLE_KEYS["MOVE"]:
                game_object.events.append(self.event)
                game_object.keys_down.append(self.event.key)

            elif self.event.type == pygame.KEYUP and self.event.key in game_object.keys_down:
                game_object.events.append(self.event)
                game_object.keys_down.remove(self.event.key)

        self.event = None

        index = 0
        events_to_remove = {}
        
        for event in game_object.events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT and game_object.dx <= self.MAX_ACCELERATION:
                    game_object.dx = self.ACCELERATION
                elif event.key == pygame.K_LEFT and game_object.dx >= -self.MAX_ACCELERATION:
                    game_object.dx = -self.ACCELERATION
                elif event.key == pygame.K_SPACE and game_object.dy == 0:
                    game_object.dy = -self.ACCELERATION
                    game_object.air_time = 1
                    
                events_to_remove[event.key] = index
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    game_object.dx = 0
                elif event.key == pygame.K_LEFT:
                    game_object.dx = 0
                elif event.key == pygame.K_UP:
                    game_object.dy = self.ACCELERATION
                    game_object.air_time = 0
                game_object.events.pop(index)
                game_object.events.pop(events_to_remove[event.key])
                index -= 2
            
            index += 1

