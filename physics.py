import pygame

class PhysicsSystem(object):
    def __init__(self, objects=None):
        self.objects = objects

    def load_objects(self, objects):
        self.objects = objects

PHYSICS_SYSTEM = PhysicsSystem()

class PlayerPhysics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        global PHYSICS_SYSTEM

        # Collision Detection
        player_map_hit_list   = pygame.sprite.groupcollide(PHYSICS_SYSTEM.objects["PLAYER"],
                                                           PHYSICS_SYSTEM.objects["MAP"], False, False)

        game_object.x += game_object.dx
        game_object.y += game_object.dy

        tile_underneath = False
        checked_both = [ False, False ]
        
        for player in player_map_hit_list:
            for tile in player_map_hit_list[player]:
                if checked_both[0] and checked_both[1]:
                    break
                
                if len(game_object.keys_down) != 0 and game_object.keys_down[0] == pygame.K_RETURN:
                    print(tile)

                if not checked_both[0]:
                    if game_object.dx > 0:
                        checked_both[0] = True
                    elif game_object.dx < 0:
                        checked_both[0] = True

                # Going DOWN
                if not checked_both[1]:
                    if game_object.dy > 0:
                        if tile.collision & 4 == 4:
                            #game_object.y -= game_object.dy
                            game_object.dy = 0
                            game_object.on_land = True
                            checked_both[1] = True

                    # Going UP
                    elif game_object.dy < 0:
                        if tile.collision & 1 == 1:
                            #game_object.y -= game_object.dy
                            game_object.dy = 0
                            game_object.on_land = False
                            checked_both[1] = True

                    # Standing still in the Y direction
                    else:
                        if tile.collision & 4 == 4:
                            game_object.on_land = True
                            tile_underneath = True
                            checked_both[1] = True
                        elif not tile_underneath:
                            game_object.on_land = False
    
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
