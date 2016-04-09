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
    '''
    Renderable class. An object that can be rendered onto the screen
    '''
    
    def __init__(self, sprite_map, sprite_map_xml, z_index=0):
        # Image and Rect
        self.image = None
        self.rect = None
        self.oldrect = None

        # If it needs to be rendered again
        self.dirty = True

        # Sprite information
        self.sprite_map = sprite_map
        self.sprite_map_xml = sprite_map_xml

        # Z location on layer
        self.z_index = z_index

        # Frame information
        self.clock = pygame.time.Clock()
        self.frame = 0.0

        # Flipping of sprite
        self.x_flip = False
        self.y_flip = False

    def get_sprite_info(self, sprite_name):
        '''
        This gets all the different sprites information from the sprite_map_xml
        based on the sprite_name
        '''
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
    '''
    This initializes the SCREEN
    '''
    global SCREEN

    if SCREEN is None:
        SCREEN = pygame.display.set_mode((width, height))

    pygame.display.set_caption(title)

def render(level):
    '''
    This draws everything found in the level that is dirty.
    '''
    global SCREEN
    global COLORS

    objects = level["OBJECTS"]
    objects_to_remove = { 0: [], 1: [], 2: [] }
    exist_enemies = False

    # Just need to start out with a blank slate.
    SCREEN.fill(COLORS["WHITE"])

    rect_list = []

    # Gather all the necessary rectangles
    layer_i = 0
    for layer in objects:
        index = 0
        for object in layer:
            # Object needs updating
            if object.dirty:
                rect_list.append(object.oldrect)
                rect_list.append(object.rect)

            # Object needs to be removed and needs it's spot to be updated
            if not object.is_alive:
                if not object.dirty:
                    rect_list.append(object.oldrect)
                    rect_list.append(object.rect)
                objects_to_remove[layer_i].append(object.id)

            # Are there still enemies found in the level?
            if object.type == "Enemy":
                exist_enemies = True    
            index += 1
        layer_i += 1

    # Render all the rectangles
    for layer in objects:
        for object in layer:
            for rect in rect_list:
                if object.rect.colliderect(rect) and object.hit_time % 2 == 0 and object.is_alive:
                    object.render(SCREEN)
                    break
        
    pygame.display.update(rect_list)

    return (objects_to_remove, exist_enemies)

def game_over(won):
    '''
    Is there a game over state? This will display the GAME OVER message if won == False and
    the WON message if won == True
    '''
    global SCREEN
    global COLORS

    text = ""
    
    if won:
        text = "YOU WON!"
    else:
        text = "GAME OVER! YOU LOST! :("
        
    SCREEN.fill(COLORS["WHITE"])

    game_over = pygame.font.Font(None, 48)
    game_over_text = game_over.render(text, 1, COLORS["BLACK"])
    
    SCREEN.blit(game_over_text, game_over_text.get_rect())

    pygame.display.flip()
    
def get_image(filename):
    '''
    Gets the image specified at the filename and puts it in the global variable
    '''
    global IMAGES

    if filename in IMAGES:
        image = IMAGES[filename]

        return image
    else:
        image = pygame.image.load(filename)
        image.convert_alpha()
        
        IMAGES[filename] = image
        
        return image;
