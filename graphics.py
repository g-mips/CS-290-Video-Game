import pygame

class PlayerActions(object):
    DUCK  = "_duck"
    FRONT = "_front"
    HIT   = "_hurt"
    JUMP  = "_jump"
    STAND = "_stand"
    WALK  = "_walk"

class EnemyActions(object):
    STAND = "\."
    DEAD  = "_dead"
    MOVE  = "_move"

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
        if game_object.dx != 0 or game_object.dy != 0:
            game_object.pre_rendered = False
        else:
            game_object.pre_rendered = True
        
        if game_object.dx > 0:
            game_object.x_flip = False
        elif game_object.dx < 0:
            game_object.x_flip = True

        # Are we in the air?
        if game_object.health != game_object.prev_health or game_object.hit_time != 0:
            game_object.current_action = PlayerActions.HIT
            game_object.pre_rendered = False
            game_object.dirty = True
            game_object.prev_health = game_object.health
            if game_object.hit_time == 0:
                game_object.hit_time = 30
            else:
                game_object.hit_time -= 1
        elif game_object.dy != 0:
            game_object.current_action = PlayerActions.JUMP
        else:
            # Are we walking? standing? or ducking?
            if game_object.dx != 0:
                game_object.current_action = PlayerActions.WALK
            elif len(game_object.keys_down) == 0:
                game_object.current_action = PlayerActions.STAND
                game_object.pre_rendered = False
                game_object.dirty = True
            elif game_object.keys_down[0] == pygame.K_DOWN:
                game_object.current_action = PlayerActions.DUCK
                game_object.pre_rendered = False
                game_object.dirty = True
                
class EnemyGraphics(Graphics):
    def __init__(self):
        pass

    def update(self, game_object):
        if game_object.dx != 0 or game_object.dy != 0:
            game_object.pre_rendered = False
        else:
            game_object.pre_rendered = True
            
        if game_object.dx > 0:
            game_object.x_flip = True
        elif game_object.dx < 0:
            game_object.x_flip = False

        game_object.current_action = EnemyActions.MOVE

        
