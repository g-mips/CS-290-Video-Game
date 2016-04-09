import pygame

class Collision:
    TOP    = 1 # 0000 0001
    LEFT   = 2 # 0000 0010
    BOTTOM = 4 # 0000 0100
    RIGHT  = 8 # 0000 1000
    
class PhysicsSystem(object):
    def __init__(self, objects=None):
        self.objects = objects
        self.objects_to_update = []
        self.width = 0
        self.height = 0
        self.buffer = 3

    def load_objects(self, objects):
        self.objects = objects

    def edge_collisions(self, game_object):
        '''
        This checks to see if the game_object provided has gone past any of the four edges of the screen.
        '''
        # RIGHT edge
        if game_object.dx > 0:
            if game_object.x + game_object.width > self.width:
                game_object.x -= game_object.dx

        # LEFT edge
        elif game_object.dx < 0:
            if game_object.x < 0:
                game_object.x -= game_object.dx

        # BOTTOM edge
        if game_object.dy > 0:
            if game_object.y + game_object.height > self.height:
                game_object.y -= game_object.dy
                

        # TOP edge
        elif game_object.dy < 0:
            if game_object.rect.y < 0:
                game_object.y -= game_object.dy

    def block_collisions(self, game_object, group):
        rect = pygame.Rect((game_object.x, game_object.y), (game_object.width, game_object.height))
        for layer in group:
            for tile in layer:
                if tile.id != game_object.id and tile.rect.colliderect(rect):
                    if tile.type == "Enemy" and game_object.type == "Player" and \
                       game_object.hit_time == 0:
                        game_object.health -= 1

                        if game_object.health % 3 == 2:
                            game_object.health -= 1

                        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                             { "health": game_object.health }))

                        game_object.hit_time = 30
                    elif tile.type == "Player" and game_object.type == "Enemy" and \
                        tile.hit_time == 0:
                        tile.health -= 1

                        if tile.health % 3 == 2:
                            tile.health -= 1

                        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                             { "health": tile.health }))

                        tile.hit_time = 30
                    elif tile.type == "Item" and game_object.type == "Enemy":
                        game_object.health -= 1
                        tile.is_alive = False
                    else:
                        overlapx = 0
                        overlapy = 0
                        solid_x = False
                        solid_y = False

                        if game_object.x > tile.x:
                            if game_object.x + game_object.width > tile.x + tile.width:
                                overlapx = (tile.x + tile.width) - game_object.x
                            elif tile.x + tile.width > game_object.x + game_object.width:
                                overlapx = game_object.width - game_object.x
                        elif tile.x > game_object.x:
                            if game_object.x + game_object.width > tile.x + tile.width:
                                overlapx = tile.width - tile.x
                            elif tile.x + tile.width > game_object.x + game_object.width:
                                overlapx = (game_object.x + game_object.width) - tile.x

                        if game_object.y > tile.y:
                            if game_object.y + game_object.height > tile.y + tile.height:
                                overlapy = (tile.y + tile.height) - game_object.y
                            elif tile.y + tile.height > game_object.y + game_object.height:
                                overlapy = game_object.height - game_object.y
                        elif tile.y > game_object.y:
                            if game_object.y + game_object.height > tile.y + tile.height:
                                overlapy = tile.height - tile.y
                            elif tile.y + tile.height > game_object.y + game_object.height:
                                overlapy = (game_object.y + game_object.height) - tile.y

                        if game_object.x - game_object.oldx > 0 and \
                           tile.collision & Collision.LEFT == Collision.LEFT:
                            solid_x = True
                            overlapx *= -1
                        elif game_object.x - game_object.oldx < 0 and \
                             tile.collision & Collision.RIGHT == Collision.RIGHT:
                            solid_x = True

                        if game_object.y - game_object.oldy > 0  and \
                           tile.collision & Collision.TOP == Collision.TOP:
                            solid_y = True
                            game_object.on_land = True
                            overlapy *= -1
                        elif game_object.y - game_object.oldy < 0 and \
                             tile.collision & Collision.BOTTOM == Collision.BOTTOM:
                            solid_y = True

                        if solid_y and abs(overlapy) < abs(overlapx):
                            game_object.y += overlapy
                            rect = pygame.Rect((game_object.x, game_object.y),
                                               (game_object.width, game_object.height))
                        elif solid_x and abs(overlapx) < abs(overlapy):
                            game_object.x += overlapx
                            rect = pygame.Rect((game_object.x, game_object.y),
                                               (game_object.width, game_object.height))
                    

    def mobile_collisions(self, game_object, group):
        tile_underneath = False
        checked_both = [ False, False ]

        # Check each tile that is colliding with game_object
        for layer in group:
            for tile in layer:
                # Did we collide with the tile and was it not ourself?
                if tile.id != game_object.id and tile.rect.colliderect(game_object.rect):
                    # Did we collide with an enemy?
                    if tile.type == "Enemy" and game_object.type == "Player" and \
                       game_object.hit_time == 0:
                        game_object.health -= 1

                        if game_object.health % 3 == 2:
                            game_object.health -= 1
                            
                        pygame.event.post(pygame.event.Event(pygame.USEREVENT,
                                                             { "health": game_object.health }))
                    
                    # Check dx
                    if not checked_both[0]:
                        # Are we moving right?
                        if game_object.dx > 0 and tile.collision & Collision.LEFT == Collision.LEFT:
                            if game_object.rect.y + game_object.rect.height >= \
                               tile.rect.y + self.buffer and \
                               game_object.rect.x < tile.rect.x:
                                print("GO: " + str(game_object.rect.y + game_object.rect.height))
                                print("TI: " + str(tile.rect.y + self.buffer))
                                game_object.dx = 0
                                checked_both[0] = True

                        # Are we moving left?
                        elif game_object.dx < 0 and tile.collision & Collision.RIGHT == Collision.RIGHT:
                            if game_object.rect.y + game_object.rect.height >= \
                               tile.rect.y + self.buffer and \
                               game_object.rect.x < tile.rect.x + tile.rect.width:
                                game_object.dx = 0
                                checked_both[0] = True
            

                    # Check dy
                    if not checked_both[1]:
                        # Are we moving down?
                        if game_object.dy > 0 and tile.collision & Collision.TOP == Collision.TOP:
                            if not \
                               (game_object.rect.x + self.buffer > tile.rect.x + tile.rect.width and \
                                game_object.rect.x + self.buffer + game_object.rect.width >
                                tile.rect.x + tile.rect.width) or \
                               (game_object.rect.x + game_object.rect.width < \
                                tile.rect.x + self.buffer and \
                                game_object.rect.x < tile.rect.x + self.buffer):
                                game_object.dy = 0
                                checked_both[1] = True
                                game_object.on_land = True

                        # Are we moving up?
                        elif game_object.dy < 0 and tile.collision & Collision.BOTTOM == Collision.BOTTOM:
                            if game_object.rect.y + self.buffer > tile.rect.y + tile.rect.height:
                                pass#game_object.dy 

                        # Are we not moving?
                        elif game_object.dy == 0:
                            if tile.collision & Collision.TOP == Collision.TOP:
                                game_object.on_land = True
                                tile_underneath = True
                                checked_both[1] = True
                            elif not tile_underneath:
                                game_object.on_land = False
                                game_object.dy = 7.0

PHYSICS_SYSTEM = PhysicsSystem()

class Physics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        pass

class FireBallPhysics(Physics):
    def __init__(self):
        pass

    def update(self, game_object):
        if game_object.life_counter != 0:
            game_object.life_counter -= 1
        else:
            game_object.is_alive = False
            
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

        # Save old information
        game_object.oldx = game_object.rect.x
        game_object.oldy = game_object.rect.y
        game_object.oldwidth = game_object.rect.width
        game_object.oldheight = game_object.rect.height

        # Air time for next time
        if game_object.air_time == 0 and not game_object.on_land:
            game_object.dy = 5.0
        elif game_object.air_time > 0 and game_object.air_time < 10 and not game_object.on_land:
            game_object.air_time += 1
            
        elif game_object.air_time >= 10 and not game_object.on_land:
            if game_object.dy < 5.0:
                game_object.dy += 1.0
            else:
                game_object.dy = 5.0
            game_object.air_time += 1

        # Create new stuff
        game_object.x += game_object.dx
        game_object.y += game_object.dy

        # Collision Detection
        PHYSICS_SYSTEM.edge_collisions(game_object)
        PHYSICS_SYSTEM.block_collisions(game_object, PHYSICS_SYSTEM.objects)
        #PHYSICS_SYSTEM.mobile_collisions(game_object, PHYSICS_SYSTEM.objects)

        if game_object.on_land:
            game_object.dy = 0
            game_object.air_time = 0

        if game_object.buffer_attack != 0:
            game_object.buffer_attack -= 1

