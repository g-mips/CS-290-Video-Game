import pygame

import objects

class Graphics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        pass

class MapGraphics(Graphics):
    def __init__(self):
        pass

    def update(self, game_object):
        if game_object.current_action != "":
            game_object.pre_rendered = False
        game_object.current_action = ""

class PlayerGraphics(Graphics):
    '''

    '''
    def __init__(self):
        pass

    def update(self, game_object):
        '''

        '''
        # Are we moving left or right?
        if game_object.dx > 0:
            if game_object.x_flip:
                game_object.pre_rendered = False
            game_object.x_flip = False
        elif game_object.dx < 0:
            if not game_object.x_flip:
                game_object.pre_rendered = False
            game_object.x_flip = True

        # Are we in the air?
        if game_object.dy != 0:
            if game_object.current_action != objects.PlayerActions.JUMP:
                game_object.pre_rendered = False
            game_object.current_action = objects.PlayerActions.JUMP
        else:
            # Are we walking? standing? or ducking?
            if game_object.dx != 0:
                if game_object.current_action != objects.PlayerActions.WALK:
                    game_object.pre_rendered = False
                game_object.current_action = objects.PlayerActions.WALK
            elif len(game_object.keys_down) == 0:
                if game_object.current_action != objects.PlayerActions.STAND:
                    game_object.pre_rendered = False
                game_object.current_action = objects.PlayerActions.STAND
            elif game_object.keys_down[0] == pygame.K_DOWN:
                if game_object.current_action != objects.PlayerActions.DUCK:
                    game_object.pre_rendered = False
                game_object.current_action = objects.PlayerActions.DUCK

class EnemyGraphics(Graphics):
    def __init__(self):
        pass

    def update(self, game_object):
        if game_object.dx > 0:
            if not game_object.x_flip:
                game_object.pre_rendered = False
            game_object.x_flip = True
        elif game_object.dx < 0:
            if game_object.x_flip:
                game_object.pre_rendered = False            
            game_object.x_flip = False

        #if game_object.dx != 0:
        if game_object.current_action != objects.EnemyActions.MOVE:
            game_object.pre_rendered = False
        game_object.current_action = objects.EnemyActions.MOVE
        #else:
        #    game_object.current_action = objects.EnemyActions.MOVE

        
