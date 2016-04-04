import pygame

import display
import xml_parser

class TileCollision:
    TOP    = 1 # 0000 0001
    LEFT   = 2 # 0000 0010
    BOTTOM = 4 # 0000 0100
    RIGHT  = 8 # 0000 1000

class Tile(display.Renderable):
    def __init__(self, sprite_sheet_xml, sprite_sheet, tile_name, x, y,
                 scale_factor, collision, mult_frames, z_index):
        super(Tile, self).__init__(display.get_image(sprite_sheet),
                                   xml_parser.load_sprite_map_info(sprite_sheet_xml), z_index)
        self.x = x*scale_factor[0]
        self.y = y*scale_factor[1]
        self.scale_factor = scale_factor
        self.collision = collision

        self.mult_frames = mult_frames

        self.sprite_name = tile_name
        self.tile_is_set = False
        self.set_rect()

        
    def update(self, *args):
        '''
        Sprite update.

        sprite_info: (x, y), (width, height)
        '''
        if not self.tile_is_set:
            sprite_info = self.get_sprite_info(self.sprite_name, self.mult_frames)
            self.set_image(sprite_info[0][0], sprite_info[0][1], sprite_info[1][0], sprite_info[1][1])
            self.set_rect()
            self.tile_is_set = True
