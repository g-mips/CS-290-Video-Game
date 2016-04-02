import pygame

import logger
import objects

class PlayerGraphics(object):
    '''

    '''
    def __init__(self):
        pass

    def update(self, game_object):
        '''

        '''

        # Are we moving left or right?
        if game_object.dx > 0:
            game_object.x_flip = False
        elif game_object.dx < 0:
            game_object.x_flip = True

        # Are we in the air?
        if game_object.dy > 0 or game_object.dy < 0:
            game_object.current_action = objects.Actions.JUMP
        else:
            # Are we walking? standing? or ducking?
            if game_object.dx != 0:
                game_object.current_action = objects.Actions.WALK
            elif len(game_object.keys_down) == 0:
                game_object.current_action = objects.Actions.STAND
            elif game_object.keys_down[0] == pygame.K_DOWN:
                game_object.current_action = objects.Actions.DUCK
