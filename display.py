import pygame
import re

import logger
import physics

SCREEN = None

COLORS = {
    "WHITE": (255, 255, 255),
    "RED":   (255,   0,   0),
    "GREEN": (  0, 255,   0),
    "BLUE":  (  0,   0, 255),
    "BLACK": (  0,   0,   0)
}

IMAGES = {}


class Renderable(object):
    def __init__(self, sprite_map, sprite_map_xml, z_index=0):
        self.image = None
        self.rect = None
        self.oldrect = None
        self.dirty = True
        
        self.sprite_map = sprite_map
        self.sprite_map_xml = sprite_map_xml

        self.z_index = z_index

        self.clock = pygame.time.Clock()
        self.frame = 0.0

        self.x_flip = False
        self.y_flip = False

    def get_sprite_info(self, sprite_name):
        sprites_info = {}

        sprite_re = "^" + sprite_name
        compile   = re.compile(sprite_re)

        for sprite in self.sprite_map_xml.keys():
            if compile.match(sprite) is not None:
                sprites_info[sprite] = self.sprite_map_xml[sprite]
        
        return sprites_info

    def render(self, screen):
        pass
    
    def pre_render(self):
        pass

    def __lt__(self, other):
        return self.z_index < other.z_index

    def __le__(self, other):
        return self.z_index <= other.z_index
    
    def __eq__(self, other):
        return self.z_index == other.z_index
    
    def __ne__(self, other):
        return self.z_index != other.z_index
    
    def __gt__(self, other):
        return self.z_index > other.z_index

    def __ge__(self, other):
        return self.z_index >= other.z_index
    
def init(width, height, title):
    global SCREEN

    if SCREEN is None:
        SCREEN = pygame.display.set_mode((width, height))

    pygame.display.set_caption(title)

def render(level):
    '''
    This draws everything found in the level.
    '''
    global SCREEN
    global COLORS

    objects = level["OBJECTS"]
    objects_to_remove = { 0: [], 1: [], 2: [] }

    SCREEN.fill(COLORS["WHITE"])

    rect_list = []

    layer_i = 0
    for layer in objects:
        index = 0
        for object in layer:
            if object.dirty:
                rect_list.append(object.oldrect)
                rect_list.append(object.rect)
            if not object.is_alive:
                if not object.dirty:
                    rect_list.append(object.oldrect)
                    rect_list.append(object.rect)
                objects_to_remove[layer_i].append(index)
            index += 1
        layer_i += 1
        
    for layer in objects:
        for object in layer:
            for rect in rect_list:
                if object.rect.colliderect(rect) and object.hit_time % 2 == 0 and object.is_alive:
                    object.render(SCREEN)
                    break
        
    pygame.display.update(rect_list)

    return objects_to_remove

def game_over():
    global SCREEN
    global COLORS

    SCREEN.fill(COLORS["WHITE"])

    game_over = pygame.font.Font(None, 48)
    game_over_text = game_over.render("GAME OVER", 1, COLORS["BLACK"])
    SCREEN.blit(game_over_text, game_over_text.get_rect())

    pygame.display.flip()
    
def get_image(filename):
    global IMAGES

    if filename in IMAGES:
        image = IMAGES[filename]

        return image
    else:
        image = pygame.image.load(filename)
        image.convert_alpha()
        
        IMAGES[filename] = image
        
        return image;
