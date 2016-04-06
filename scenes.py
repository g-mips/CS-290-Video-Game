import pygame
import os

import xml_parser
import objects
import game_input
import physics
import graphics
import event_handler

def load_level(level):
    game_objects = {
        "BACKGROUND": [],
        "HUD": [],
        "MAIN": []
    }

    level_xml = None
    sprites   = None
    id = 0
    
    if level == 1:
        level_xml = os.path.join('xmlsheets', 'level_one.xml')
        sprites = xml_parser.load_level(level_xml)

    for sprite in sprites:
        tile = objects.GameObject(
            id,
            os.path.join('xmlsheets', sprite["XML_SHEET"]),
            os.path.join('imgs', sprite["SPRITE_SHEET"]),
            sprite["NAME"],
            sprite["X"],
            sprite["Y"],
            [sprite["SCALE_X"], sprite["SCALE_Y"]],
            sprite["COLLISION"],
            sprite["Z_INDEX"],
            sprite["TYPE"],
            None,
            None,
            None
        )

        id += 1
        layer = ""
        
        if sprite["TYPE"] == "Tile":
            tile.input = game_input.Input()
            tile.physics = physics.MapPhysics()
            tile.graphics = graphics.MapGraphics()

            layer = "BACKGROUND"
        elif sprite["TYPE"] == "Player":
            tile.input = game_input.PlayerInput()
            tile.physics = physics.MobilePhysics()
            tile.graphics = graphics.PlayerGraphics()

            event_handler.register("KEYDOWN", tile.input.register_event)
            event_handler.register("KEYUP", tile.input.register_event)

            layer = "MAIN"
        elif sprite["TYPE"] == "Hud":
            tile.input = game_input.Input()
            tile.physics = physics.MapPhysics()
            tile.graphics = graphics.MapGraphics()

            layer = "HUD"
        elif sprite["TYPE"] == "Enemy":
            tile.input = game_input.EnemyInput()
            tile.physics = physics.MobilePhysics()
            tile.graphics = graphics.EnemyGraphics()

            layer = "MAIN"

        game_objects[layer].append(tile)
        
    #for sprite in sprites:
    #    if sprite["TYPE"] == "Tile":
    #        tile = objects.Tile(
    #            os.path.join('xmlsheets', sprite["XML_SHEET"]),
    #            os.path.join('imgs', sprite["SPRITE_SHEET"]),
    #            sprite["NAME"],
    #            sprite["X"],
    #            sprite["Y"],
    #            [sprite["SCALE_X"], sprite["SCALE_Y"]],
    #            sprite["COLLISION"],
    #            sprite["Z_INDEX"],
    #            game_input.Input(),
    #            physics.MapPhysics(),
    #            graphics.MapGraphics()
    #        )
    #        game_objects["MAP"].add(tile)
    #    elif sprite["TYPE"] == "Player":
    #        player = objects.Mobile(
    #            os.path.join('xmlsheets', sprite["XML_SHEET"]),
    #            os.path.join('imgs', sprite["SPRITE_SHEET"]),
    #            sprite["NAME"],
    #            sprite["X"],
    #            sprite["Y"],
    #            [sprite["SCALE_X"], sprite["SCALE_Y"]],
    #            sprite["COLLISION"],
    #            sprite["Z_INDEX"],
    #            game_input.PlayerInput(),
    #            physics.MobilePhysics(),
    #            graphics.PlayerGraphics()
    #        )
           
    #        event_handler.register("KEYDOWN", player.input.register_event)
    #        event_handler.register("KEYUP", player.input.register_event)
            
    #        game_objects["PLAYER"].add(player)
    #    elif sprite["TYPE"] == "Hud":
    #        game_objects["HUD"].add(objects.Tile(
    #            os.path.join('xmlsheets', sprite["XML_SHEET"]),
    #            os.path.join('imgs', sprite["SPRITE_SHEET"]),
    #            sprite["NAME"],
    #            sprite["X"],
    #            sprite["Y"],
    #            [sprite["SCALE_X"], sprite["SCALE_Y"]],
    #            sprite["COLLISION"],
    #            sprite["Z_INDEX"],
    #            game_input.Input(),
    #            physics.MapPhysics(),
    #            graphics.MapGraphics()
    #        ))
    #    elif sprite["TYPE"] == "Enemy":
    #        game_objects["ENEMIES"].add(objects.Mobile(
    #            os.path.join('xmlsheets', sprite["XML_SHEET"]),
    #            os.path.join('imgs', sprite["SPRITE_SHEET"]),
    #            sprite["NAME"],
    #            sprite["X"],
    #            sprite["Y"],
    #            [sprite["SCALE_X"], sprite["SCALE_Y"]],
    #            sprite["COLLISION"],
    #            sprite["Z_INDEX"],
    #            game_input.EnemyInput(),
    #            physics.MobilePhysics(),
    #            graphics.EnemyGraphics()
    #        ))
    #    elif sprite["TYPE"] == "Item":
            # objects["ITEMS"].add()
    #        pass
        
    return game_objects

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    print(load_level(1))
