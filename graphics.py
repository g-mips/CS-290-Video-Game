import pygame

import logger
import objects

class PlayerGraphics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        if game_object.dx > 0 and game_object.dy == 0:
            game_object.current_action = objects.Actions.WALK
            game_object.x_flip = False
        elif game_object.dx < 0 and game_object.dy == 0:
            game_object.current_action = objects.Actions.WALK
            game_object.x_flip = True
        elif game_object.dy > 0 or game_object.dy < 0:
            game_object.current_action = objects.Actions.JUMP
        elif game_object.dx == 0 and game_object.dy == 0:
            if len(game_object.keys_down) == 0:
                game_object.current_action = objects.Actions.STAND
            elif game_object.keys_down[0] == pygame.K_DOWN:
                game_object.current_action = objects.Actions.DUCK
            else:
                game_object.current_action = objects.Actions.STAND
