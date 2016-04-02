import os

import xml_parser
import map
import objects
import game_input
import physics
import graphics
import event_handler

def run_start():
    pass

def run_end():
    pass

def load_level(level):
    if level == 1:
        level_map = map.Map(os.path.join('xmlsheets', 'level_one.xml'), True,
                            [ xml_parser.MAIN_SPRITE_SHEET, os.path.join('imgs', 'bg.png') ])
        level_map.add_tiles(os.path.join('xmlsheets', 'bg.xml'))
        
        player    = objects.Alien(game_input.PlayerInput(), physics.PlayerPhysics(),
                                  graphics.PlayerGraphics(), [xml_parser.MAIN_SPRITE_SHEET])

        event_handler.register("KEYDOWN", player.input.register_event)
        event_handler.register("KEYUP", player.input.register_event)

        level_objects = [ player ]

        return { "MAP": level_map, "OBJECTS": level_objects }

    return None
