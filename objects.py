import pygame
import os
import re

import xml_parser
import display
import logger

class GameObject(display.Renderable):
    def __init__(self, id, sprite_map_xml, sprite_map, sprite_name, x, y, scale_factor,
                 collision, z_index, type, input, physics, graphics):
        super(GameObject, self).__init__(display.get_image(sprite_map),
                                         xml_parser.load_sprite_map_info(sprite_map_xml), z_index)
        # Identification
        self.id = id
        self.type = type

        # The name of the sprite (as found on the sprite sheet. Unless it is a multiple framed sprite
        #   then this represents a unquie sub string of all the frames).
        self.sprite_name = sprite_name
        self.sprites_info = self.get_sprite_info(self.sprite_name)

        # Better to scale here than in the main loop
        for sprite in self.sprites_info:
            self.sprites_info[sprite][1].append(int(self.sprites_info[sprite][1][0] / scale_factor))
            self.sprites_info[sprite][1].append(int(self.sprites_info[sprite][1][1] / scale_factor))
        
        # Components
        self.input = input
        self.physics = physics
        self.graphics = graphics

        # Status of GameObject
        self.isAlive     = True
        self.health      = 0
        self.prev_health = 0
        self.hit_time    = 0
        self.collision   = collision
        self.on_land     = False
        self.air_time    = 0

        # Positions
        self.oldx = x
        self.oldy = y
        self.x    = x
        self.y    = y
        self.dx   = 0
        self.dy   = 0

        # Size
        self.scale_factor = scale_factor
        self.width        = 0
        self.height       = 0
        self.oldwidth     = 0
        self.oldheight    = 0
        
        # Action of Sprite
        self.current_action = self.graphics.get_default_action()
        self.pre_render()

        # Keys that are down and up that affect the game object
        self.keys_down = []
        self.keys_up   = []
        
    def update(self):
        self.input.update(self)
        self.physics.update(self)
        self.graphics.update(self)

    def get_actions_info(self, action_name):
        actions_info = []

        sprite_re = "^" + action_name
        compile   = re.compile(sprite_re)

        for action in self.sprites_info.keys():
            if compile.match(action) is not None:
                actions_info.append(self.sprites_info[action])

        return actions_info
    
    def set_image(self, x, y, width, height):
        self.sprite_map.set_clip(pygame.Rect(x, y, width, height))
        self.image = self.sprite_map.subsurface(self.sprite_map.get_clip())

    def render(self, screen):
        screen.blit(
            pygame.transform.flip(
                pygame.transform.scale(
                    self.image,
                    (self.width, self.height)
                ),
                self.x_flip,
                self.y_flip
            ),
            (self.x, self.y)
        )

        self.dirty = False
        
    def pre_render(self):
        if self.dirty:
            actions_info = self.get_actions_info(self.sprite_name + self.current_action)
            self.frame = (self.frame + (self.clock.tick() / 100.0)) % len(actions_info)
            action_info = actions_info[int(self.frame)]

            self.set_image(action_info[0][0], action_info[0][1], action_info[1][0], action_info[1][1])

            self.oldwidth = self.width
            self.oldheight = self.height
            
            self.width  = action_info[1][2]
            self.height = action_info[1][3]

            # Do we need to adjust our x position?
            if self.width > self.oldwidth and self.oldwidth != 0:
                diff = self.width - self.oldwidth
                self.x -= diff
            elif self.width < self.oldwidth and self.oldwidth != 0:
                diff = self.oldwidth - self.width
                self.x += diff

            # Do we need to adjust our y position?
            if self.height > self.oldheight and self.oldheight != 0:
                diff = self.height - self.oldheight
                self.y -= diff
            elif self.height < self.oldheight and self.oldheight != 0:
                diff = self.oldheight - self.height
                self.y += diff

            self.oldrect = pygame.Rect(
                (self.oldx, self.oldy),
                (self.oldwidth, self.oldheight)
            )
            
            self.rect = pygame.Rect(
                (self.x, self.y),
                (self.width, self.height)
            )
