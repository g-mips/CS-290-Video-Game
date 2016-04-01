import pygame

class PlayerInput(object):
    ACCELERATION = 1
    MAX_ACCELERATION = 5
    AVAILABLE_KEYS = { "MOVE": [ pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN ] }
    MOVE_KEYS_DOWN = []
    
    def __init__(self):
        pass

    def update(self, gameObject, event):
        if event.type == pygame.KEYDOWN:
            if event.key in AVAILABLE_KEYS["MOVE"]:
                self.MOVE_KEYS_DOWN.append(event)
            
            if event.key == pygame.K_RIGHT and self.MOVE_KEYS_DOWN.__len__() == 0:
                game_object.velocity += self.ACCELERATION
            elif event.key == pygame.K_LEFT and self.MOVE_KEYS_DOWN.__len__() == 0:
                game_object.velocity -= self.ACCELERATION
            elif event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                game_object.velocity = 0
            elif event.key == pygame.K_LEFT:
                game_object.velocity = 0
            elif event.key == pygame.K_UP:
                pass
            elif event.key == pygame.K_DOWN:
                pass
        
