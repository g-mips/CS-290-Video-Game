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

    def detect_collisions(self, game_object, group):
        tile_underneath = False
        checked_both = [ False, False ]
        for tile in group:
            
            #print(tile.rect.x)
            #print(tile.rect.y)
            #print(tile.rect.width)
            #print(tile.rect.height)

            
        

        #for tile in player_map_hit_list:
            if checked_both[0] and checked_both[1]:
                break
                
            if len(game_object.keys_down) != 0 and game_object.keys_down[0] == pygame.K_RETURN:
                print(tile)
            
            if not checked_both[0]:
                if game_object.dx > 0:
                    if tile.collision & Collision.RIGHT == Collision.RIGHT:
                        game_object.dx = 0
                        checked_both[0] = True
                elif game_object.dx < 0:
                    if tile.collision & Collision.LEFT == Collision.LEFT:
                        game_object.dx = 0
                        checked_both[0] = True

            # Going DOWN
            if not checked_both[1]:
                if game_object.dy > 0:
                    if tile.collision & Collision.BOTTOM == Collision.BOTTOM:
                        game_object.y = tile.rect.y - 1 - game_object.rect.height
                        game_object.dy = 0
                        game_object.on_land = True
                        checked_both[1] = True
                        
                # Going UP
                elif game_object.dy < 0:
                    if tile.collision & Collision.TOP == Collision.TOP:
                        #game_object.y =
                        game_object.dy = 0
                        game_object.on_land = False
                        checked_both[1] = True
                            
                # Standing still in the Y direction
                else:
                    if tile.collision & Collision.BOTTOM == Collision.BOTTOM:
                        game_object.on_land = True
                        tile_underneath = True
                        checked_both[1] = True
                    elif not tile_underneath:
                        game_object.on_land = False

        return tile_underneath
    
        
PHYSICS_SYSTEM = PhysicsSystem()

class PlayerPhysics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        global PHYSICS_SYSTEM

        # Collision Detection
        player_map_hit_list   = pygame.sprite.spritecollide(game_object, PHYSICS_SYSTEM.objects["MAP"], False)

        print(game_object.dy)

        PHYSICS_SYSTEM.detect_collisions(game_object, player_map_hit_list)

        game_object.x += game_object.dx
        game_object.y += game_object.dy

        if not game_object.on_land and game_object.dy == 0.0:
            game_object.dy = 3.0
            game_object.y += game_object.dy
                        
                #elif tile.collision & 4 != 4:
                #    game_object.dy = 3.0


        # Air Time
        if game_object.air_time > 0 and game_object.air_time < 10:
            game_object.air_time += 1
        elif game_object.air_time >= 10 and game_object.air_time < 30:
            game_object.dy += 0.05
            game_object.air_time += 1
        elif game_object.air_time >= 30:
            game_object.dy = 3.0
            game_object.air_time = 0
