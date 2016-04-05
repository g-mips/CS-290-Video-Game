import pygame
import os

import xml_parser
import display


class PlayerActions(object):
    CLIMB = "_climb"
    DUCK  = "_duck"
    FRONT = "_front"
    HIT   = "_hit"
    JUMP  = "_jump"
    STAND = "_stand"
    SWIM  = "_swim"
    WALK  = "_walk"

class EnemyActions(object):
    STAND = "\."
    DEAD  = "_dead"
    MOVE  = "_move"

class GameObject(display.Renderable):
    def __init__(self, input, physics, graphics, sprite_map, sprite_map_xml, z_index, x, y, sprite_name,
                 scale_factor, collision):
        super(GameObject, self).__init__(display.get_image(sprite_map),
                                         xml_parser.load_sprite_map_info(sprite_map_xml), z_index)
        # Components
        self.input = input
        self.physics = physics
        self.graphics = graphics

        # Status of GameObject
        self.isAlive  = True

        # Scaling Factor (width, height)
        self.scale_factor = scale_factor
        
        # Position Change
        self.dx = 0
        self.dy = 0

        # Position
        self.x = x*self.scale_factor[0]
        self.y = y*self.scale_factor[1]

        # Action of Sprite
        self.current_action = None

        self.collision = collision
        self.on_land = False

        # Flip or not
        self.x_flip = False
        self.y_flip = False

        # Keys that are down and up that affect the game object
        self.keys_down = []
        self.keys_up   = []

        # The name of the sprite (as found on the sprite sheet. Unless it is a multiple framed sprite
        #   then this represents a unquie sub string of all the frames).
        self.sprite_name = sprite_name

        self.set_rect()

    def update(self):
        self.input.update(self)
        self.physics.update(self)
        self.graphics.update(self)

    def pre_render(self):
        pass


class Mobile(GameObject):
    def __init__(self, sprite_sheet_xml, sprite_sheet, sprite_name, x, y,
                 scale_factor, collision, z_index,
                 input, physics, graphics):
        super(Mobile, self).__init__(input, physics, graphics, sprite_sheet, sprite_sheet_xml,
                                     z_index, x, y, sprite_name, scale_factor, collision)

        self.air_time = 0

    def pre_render(self):
        sprites_info = self.get_sprite_info(self.sprite_name + self.current_action)
        self.frame = (self.frame + (self.clock.tick() / 100.0)) % len(sprites_info)
        sprite_info = sprites_info[int(self.frame)]
        self.set_image(sprite_info[0][0], sprite_info[0][1], sprite_info[1][0], sprite_info[1][1])
        self.set_rect()
    
    def get_rect(self):
        return pygame.Rect((self.x-self.dx, self.y-self.dy), (self.scale_factor[0], self.scale_factor[1]))

class Tile(GameObject):
    def __init__(self, sprite_sheet_xml, sprite_sheet, tile_name, x, y,
                 scale_factor, collision, z_index,
                 input, physics, graphics):
        super(Tile, self).__init__(input, physics, graphics, sprite_sheet, sprite_sheet_xml,
                                   z_index, x, y, tile_name, scale_factor, collision)
        self.tile_is_set = False
        self.set_rect()

        
    def pre_render(self):
        '''
        Sprite update.

        sprite_info: (x, y), (width, height)
        '''
        if not self.tile_is_set:
            sprites_info = self.get_sprite_info(self.sprite_name)
            self.frame = (self.frame + (self.clock.tick() / 100.0)) % len(sprites_info)
            sprite_info = sprites_info[int(self.frame)]
            self.set_image(sprite_info[0][0], sprite_info[0][1], sprite_info[1][0], sprite_info[1][1])
            self.set_rect()
            self.tile_is_set = True

if __name__ == "__main__":
    xml_parser.load_xml(MAIN_XML_SHEET)
    PLAYER_INFO = xml_parser.load_players(PLAYER_INFO, Players, Actions)
    print(PLAYER_INFO)

