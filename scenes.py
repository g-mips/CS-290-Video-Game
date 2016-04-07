import pygame
import os

import xml_parser
import objects
import game_input
import physics
import graphics
import event_handler

def load_level(level):
    game_objects = [ [], [], [] ]

    level_xml = None
    sprites   = None
    id = 0
    
    if level == 1:
        level_xml = os.path.join('xmlsheets', 'level_one.xml')
        sprites = xml_parser.load_level(level_xml)

    health_tile_id = 0
    
    for sprite in sprites:
        health      = 0
        prev_health = 0
        
        layer = 0

        # Components of the sprite
        input_comp    = None
        physics_comp  = None
        graphics_comp = None

        # Are we dealing with a map tile?
        if sprite["TYPE"] == "Tile":
            input_comp    = game_input.Input()
            physics_comp  = physics.MapPhysics()
            graphics_comp = graphics.MapGraphics()

            layer = 0
        # Are we dealing with a player?
        elif sprite["TYPE"] == "Player":
            input_comp    = game_input.PlayerInput()
            physics_comp  = physics.MobilePhysics()
            graphics_comp = graphics.PlayerGraphics()

            health = 8
            prev_health = 8

            event_handler.register("KEYDOWN", input_comp.register_event)
            event_handler.register("KEYUP", input_comp.register_event)

            layer = 2
        # Are we dealing with a HUD tile?
        elif sprite["TYPE"] == "Hud":
            if sprite["NAME"] == "hudHeart":
                input_comp    = game_input.HealthInput(health_tile_id)
                graphics_comp = graphics.HealthGraphics()

                event_handler.register("USEREVENT", input_comp.get_health_change)
                health_tile_id += 1
            else:
                input_comp = game_input.Input()
                graphics_comp = graphics.Graphics()
            physics_comp = physics.Physics()

            layer = 1
        # Are we dealing with an enemy?
        elif sprite["TYPE"] == "Enemy":
            input_comp = game_input.EnemyInput()
            physics_comp = physics.MobilePhysics()
            graphics_comp = graphics.EnemyGraphics()

            layer = 2

        # Create the tile
        tile = objects.GameObject(
            id,
            os.path.join('xmlsheets', sprite["XML_SHEET"]),
            os.path.join('imgs', sprite["SPRITE_SHEET"]),
            sprite["NAME"],
            sprite["X"]*sprite["SCALE_X"],
            sprite["Y"]*sprite["SCALE_Y"],
            sprite["SCALE_FACT"],
            sprite["COLLISION"],
            sprite["Z_INDEX"],
            sprite["TYPE"],
            input_comp,
            physics_comp,
            graphics_comp
        )

        tile.health      = health
        tile.prev_health = prev_health

        id += 1
        
        game_objects[layer].append(tile)
        
    return game_objects

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    print(load_level(1))
