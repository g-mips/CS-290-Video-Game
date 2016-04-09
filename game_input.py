import pygame

import objects
import logger

class Input(object):
    '''
    Generic Input Class
    '''
    def __init__(self):
        self.events = []

    def update(self, game_object):
        pass

class FireBallInput(Input):
    '''
    FireBall Input class
    '''
    def __init__(self, direction):
        self.direction = direction
        self.acceleration = 12.0
        
    def update(self, game_object):
        '''
        This defines the direction the fireball is being launched.
        '''
        if self.direction:
            game_object.x += -self.acceleration
            game_object.dirty = True
        else:
            game_object.x += self.acceleration
            game_object.dirty = True

class HealthInput(Input):
    '''
    Health HUD Input class
    '''
    def __init__(self, id):
        super(HealthInput, self).__init__()
        self.id = id
        self.current_health = 2

    def get_health_change(self, event):
        '''
        This should be registered to the event_handler. It will observe
        whenever the player gets hurt and change the HealthInput's health.
        '''
        if self.id*3 <= event.__dict__["health"] < self.id*3+2:
            self.current_health = event.__dict__["health"] % 3
        
    def update(self, game_object):
        '''
        Change the game_object (should be a health HUD icon) health
        '''
        game_object.health = self.current_health
    
class EnemyInput(Input):
    '''
    Enemy Input class
    '''
    def __init__(self):
        super(EnemyInput, self).__init__()
        self.acceleration = 4.0

    def update(self, game_object):
        '''
        This will change the direction of the game_object if they stopped moving or
        can't move any further in the direction they were moving.
        '''
        if game_object.dx == 0 or game_object.oldx == game_object.x:
            self.acceleration = -self.acceleration
        game_object.dx = self.acceleration

class PlayerInput(Input):
    '''
    Player Input Class.
    '''
    ACCELERATION = 7.0
    AVAILABLE_KEYS = [ pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_SPACE ]
    ATTACK_KEY = None
    
    def __init__(self):
        super(PlayerInput, self).__init__()

    def register_event(self, event):
        '''
        This should be registered by the event_handler.
        '''
        self.events.append(event)

    def define_attack(self, attack):
        '''
        This defines which key is the attack key.
        '''
        if attack == "A":
            self.AVAILABLE_KEYS.append(pygame.K_a)
            self.ATTACK_KEY = pygame.K_a
        elif attack == "B":
            self.AVAILABLE_KEYS.append(pygame.K_b)
            self.ATTACK_KEY = pygame.K_b
        elif attack == "C":
            self.AVAILABLE_KEYS.append(pygame.K_c)
            self.ATTACK_KEY = pygame.K_c
        elif attack == "D":
            self.AVAILABLE_KEYS.append(pygame.K_d)
            self.ATTACK_KEY = pygame.K_d
        elif attack == "E":
            self.AVAILABLE_KEYS.append(pygame.K_e)
            self.ATTACK_KEY = pygame.K_e
        elif attack == "F":
            self.AVAILABLE_KEYS.append(pygame.K_f)
            self.ATTACK_KEY = pygame.K_f
        elif attack == "G":
            self.AVAILABLE_KEYS.append(pygame.K_g)
            self.ATTACK_KEY = pygame.K_g

    def update(self, game_object):
        '''
        This will update the game_object's movement by checking the keys that are up and down.
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

        # Execute the keys that are up
        for event in game_object.keys_up:
            if event == pygame.K_RIGHT:
                game_object.dx = 0
            elif event == pygame.K_LEFT:
                game_object.dx = 0
            elif event == pygame.K_SPACE:
                game_object.air_time = 10
            elif event == self.ATTACK_KEY:
                game_object.attacking = False

        game_object.keys_up = []
        
        # Execute the keys that are down
        for event in game_object.keys_down:
            if event == pygame.K_RIGHT:
                game_object.dx = self.ACCELERATION
            elif event == pygame.K_LEFT:
                game_object.dx = -self.ACCELERATION
            elif event == pygame.K_SPACE and game_object.dy == 0 and game_object.air_time == 0:
                game_object.dy = -self.ACCELERATION
                game_object.on_land = False
                game_object.air_time = 1
                game_object.keys_down.remove(event)
            elif event == self.ATTACK_KEY:
                game_object.attacking = True

