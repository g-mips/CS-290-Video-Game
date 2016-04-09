import pygame

    
class Graphics(object):
    def __init__(self):
        pass

    def get_default_action(self):
        return ""
    
    def update(self, game_object):
        pass

class HealthGraphics(Graphics):
    EMPTY = "_empty"
    FULL  = "_full"
    HALF  = "_half"
    
    def __init__(self):
        pass

    def get_default_action(self):
        return self.FULL
    
    def update(self, game_object):
        if game_object.health == 0 and \
           game_object.current_action != self.EMPTY:
            game_object.dirty = True
            game_object.current_action = self.EMPTY

        elif game_object.health == 1 and \
             game_object.current_action != self.HALF:
            game_object.dirty = True
            game_object.current_action = self.HALF

        elif game_object.health == 2 and \
             game_object.current_action != self.FULL:
            game_object.dirty = True
            game_object.current_action = self.FULL

class MapGraphics(Graphics):
    STANDARD = ""
    
    def __init__(self):
        pass

    def get_default_action(self):
        return self.STANDARD
    
    def update(self, game_object):
        if game_object.current_action != self.STANDARD:
            game_object.dirty = True
        game_object.current_action = self.STANDARD

class PlayerGraphics(Graphics):
    '''

    '''
    DUCK  = "_duck"
    FRONT = "_front"
    HIT   = "_hurt"
    JUMP  = "_jump"
    STAND = "_stand"
    WALK  = "_walk"
    
    def __init__(self):
        pass

    def get_default_action(self):
        return self.STAND
    
    def update(self, game_object):
        '''

        '''
        # Are we moving left or right?
        if game_object.dx != 0 or game_object.dy != 0:
            game_object.dirty = True
        
        if game_object.dx > 0:
            game_object.x_flip = False
        elif game_object.dx < 0:
            game_object.x_flip = True

        # Are we in the air?
        if game_object.health != game_object.prev_health or game_object.hit_time != 0:
            game_object.current_action = self.HIT
            game_object.dirty = True
            game_object.prev_health = game_object.health
            if game_object.hit_time == 0:
                game_object.hit_time = 30
            else:
                game_object.hit_time -= 1
        elif game_object.dy != 0:
            game_object.current_action = self.JUMP
        else:
            # Are we walking? standing? or ducking?
            if game_object.dx != 0:
                game_object.current_action = self.WALK
            elif game_object.attacking:
                game_object.current_action = self.FRONT
                game_object.dirty = True
            elif len(game_object.keys_down) == 0:
                game_object.current_action = self.STAND
                game_object.dirty = True
            elif game_object.keys_down[0] == pygame.K_DOWN:
                game_object.current_action = self.DUCK
                game_object.dirty = True

        if game_object.health <= 0:
            game_object.is_alive = False
                
class EnemyGraphics(Graphics):
    STAND = "\."
    DEAD  = "_dead"
    MOVE  = "_move"
    
    def __init__(self):
        pass

    def get_default_action(self):
        return self.MOVE
    
    def update(self, game_object):
        if game_object.dx != 0 or game_object.dy != 0:
            game_object.dirty = True
            
        if game_object.dx > 0:
            game_object.x_flip = True
        elif game_object.dx < 0:
            game_object.x_flip = False

        if game_object.health <= 0:
            game_object.current_action = self.DEAD
            game_object.is_alive = False
        else:
            game_object.current_action = self.MOVE

        
