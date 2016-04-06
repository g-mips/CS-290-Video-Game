import pygame
import os

import xml_parser
import display


class GameObject(display.Renderable):
    def __init__(self, id, sprite_map_xml, sprite_map, sprite_name, x, y,
                 scale_factor, collision, z_index, type,
                 input, physics, graphics):
        super(GameObject, self).__init__(display.get_image(sprite_map),
                                         xml_parser.load_sprite_map_info(sprite_map_xml), z_index)
        self.id = id
        self.type = type

        # Components
        self.input = input
        self.physics = physics
        self.graphics = graphics

        # Status of GameObject
        self.isAlive  = True
        self.health   = 0
        self.prev_health = 0
        self.hit_time = 0

        # Scaling Factor (width, height)
        self.scale_factor = scale_factor
        
        # Position Change
        self.dx = 0
        self.dy = 0

        # Position
        self.oldx = x*self.scale_factor[0]
        self.oldy = y*self.scale_factor[1]
        self.x = x*self.scale_factor[0]
        self.y = y*self.scale_factor[1]

        self.dirty = False
        
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

        self.air_time = 0
        self.pre_rendered = False
        
    def update(self):
        self.input.update(self)
        self.physics.update(self)
        self.graphics.update(self)

    def pre_render(self):
        if not self.pre_rendered:
            sprites_info = self.get_sprite_info(self.sprite_name + self.current_action)
            self.frame = (self.frame + (self.clock.tick() / 100.0)) % len(sprites_info)
            sprite_info = sprites_info[int(self.frame)]
            self.set_image(sprite_info[0][0], sprite_info[0][1], sprite_info[1][0], sprite_info[1][1])
            self.set_rect()
            self.pre_rendered = True

if __name__ == "__main__":
    xml_parser.load_xml(MAIN_XML_SHEET)
    PLAYER_INFO = xml_parser.load_players(PLAYER_INFO, Players, Actions)
    print(PLAYER_INFO)

