import pygame

class Collision:
    TOP    = 1 # 0000 0001
    LEFT   = 2 # 0000 0010
    BOTTOM = 4 # 0000 0100
    RIGHT  = 8 # 0000 1000
    
class PhysicsSystem(object):
    def __init__(self, objects=None):
        self.objects = objects

    def load_objects(self, objects):
        self.objects = objects

    def mobile_collisions(self, game_object, group):
        tile_underneath = False
        checked_both = [ False, False ]

        # Check each tile that is colliding with game_object
        for tile in group:
            # Did we define what happens with both dx and dy?
            if checked_both[0] and checked_both[1]:
                break

            # Check dx
            if not checked_both[0]:
                # Are we moving right?
                if game_object.dx > 0:
                    if tile.collision & Collision.LEFT == Collision.LEFT:
                        if game_object.rect.y + game_object.rect.height >= tile.rect.y + 5 and \
                           game_object.rect.x < tile.rect.x:
                            game_object.dx = 0
                            checked_both[0] = True

                # Are we moving left?
                elif game_object.dx < 0:
                    if tile.collision & Collision.RIGHT == Collision.RIGHT:
                        if game_object.rect.y + game_object.rect.height >= tile.rect.y + 5 and \
                           game_object.rect.x < tile.rect.x + tile.rect.width:
                            game_object.dx = 0
                            checked_both[0] = True
                            
            # Check dy
            if not checked_both[1]:
                # Are we moving down?
                if game_object.dy > 0:
                    if tile.collision & Collision.TOP == Collision.TOP:                            
                        if not \
                           (game_object.rect.x + 3 > tile.rect.x + tile.rect.width and \
                            game_object.rect.x + 3 + game_object.rect.width >
                            tile.rect.x + tile.rect.width) or \
                           (game_object.rect.x + game_object.rect.width < tile.rect.x + 3 and \
                            game_object.rect.x < tile.rect.x + 3):
                            game_object.dy = 0
                            checked_both[1] = True
                            game_object.on_land = True

                # Are we moving up?
                elif game_object.dy < 0:
                    if tile.collision & Collision.BOTTOM == Collision.BOTTOM:
                        if game_object.rect.y + 3 > tile.rect.y + tile.rect.height:
                            game_object.dy

                # Are we not moving?
                elif game_object.dy == 0:
                    if tile.collision & Collision.TOP == Collision.TOP:
                        game_object.on_land = True
                        tile_underneath = True
                        checked_both[1] = True
                    elif not tile_underneath:
                        game_object.on_land = False
                        game_object.dy = 3.0

PHYSICS_SYSTEM = PhysicsSystem()

class Physics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        pass

class MapPhysics(Physics):
    def __init__(self):
        pass

    def update(self, game_object):
        pass

class MobilePhysics(Physics):
    def __init__(self):
        pass

    def update(self, game_object):
        global PHYSICS_SYSTEM

        # Collision Detection
        map_hit_list   = pygame.sprite.spritecollide(game_object, PHYSICS_SYSTEM.objects["MAP"], False)

        PHYSICS_SYSTEM.mobile_collisions(game_object, map_hit_list)

        game_object.x += game_object.dx
        game_object.y += game_object.dy

        # Air Time
        if game_object.air_time > 0 and game_object.air_time < 10:
            game_object.air_time += 1
        elif game_object.air_time >= 10 and game_object.air_time < 30:
            game_object.dy += 0.05
            game_object.air_time += 1
        elif game_object.air_time >= 30:
            game_object.dy = 3.0
            game_object.air_time = 0
