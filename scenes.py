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
        "HUD":     pygame.sprite.OrderedUpdates(),
        "MAP":     pygame.sprite.OrderedUpdates(),
        "ENEMIES": pygame.sprite.OrderedUpdates(),
        "ITEMS":   pygame.sprite.OrderedUpdates(),
        "PLAYER":  pygame.sprite.GroupSingle()
    }

    level_xml = None
    sprites   = None
    
    if level == 1:
        level_xml = os.path.join('xmlsheets', 'level_one.xml')
        sprites = xml_parser.load_level(level_xml)
        
    for sprite in sprites:
        if sprite["TYPE"] == "Tile":
            tile = objects.Tile(
                os.path.join('xmlsheets', sprite["XML_SHEET"]),
                os.path.join('imgs', sprite["SPRITE_SHEET"]),
                sprite["NAME"],
                sprite["X"],
                sprite["Y"],
                [sprite["SCALE_X"], sprite["SCALE_Y"]],
                sprite["COLLISION"],
                sprite["MULT_FRAMES"],
                sprite["Z_INDEX"],
                game_input.Input(),
                physics.MapPhysics(),
                graphics.MapGraphics()
            )
            game_objects["MAP"].add(tile)
        elif sprite["TYPE"] == "Player":
            player = objects.Mobile(
                os.path.join('xmlsheets', sprite["XML_SHEET"]),
                os.path.join('imgs', sprite["SPRITE_SHEET"]),
                sprite["NAME"],
                sprite["X"],
                sprite["Y"],
                [sprite["SCALE_X"], sprite["SCALE_Y"]],
                sprite["COLLISION"],
                sprite["MULT_FRAMES"],
                sprite["Z_INDEX"],
                game_input.PlayerInput(),
                physics.MobilePhysics(),
                graphics.PlayerGraphics()
            )
            
            event_handler.register("KEYDOWN", player.input.register_event)
            event_handler.register("KEYUP", player.input.register_event)
            
            game_objects["PLAYER"].add(player)
        elif sprite["TYPE"] == "HUD":
            # objects["HUD"].add()
            pass
        elif sprite["TYPE"] == "Enemy":
            # objects["ENEMIES"].add()
            pass
        elif sprite["TYPE"] == "Item":
            # objects["ITEMS"].add()
            pass
        
    return game_objects

if __name__ == "__main__":
    pygame.init()
    pygame.display.set_mode((800, 600))
    print(load_level(1))
