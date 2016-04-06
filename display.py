import pygame
import re

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
        self.dirty = None
        self.visible = None
        self.blendmode = None
        
        self.sprite_map = sprite_map
        self.sprite_map_xml = sprite_map_xml

        self.z_index = z_index

        self.clock = pygame.time.Clock()
        self.frame = 0.0

        self.x_flip = False
        self.y_flip = False

    def set_image(self, x, y, width, height):
        self.sprite_map.set_clip(pygame.Rect(x, y, width, height))
        self.image = pygame.transform.flip(
            pygame.transform.scale(
                self.sprite_map.subsurface(self.sprite_map.get_clip()),
                self.scale_factor),
            self.x_flip,
            self.y_flip
        )

    def set_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.scale_factor[0], self.scale_factor[1])

    def get_sprite_info(self, sprite_name):
        sprites_info = []

        sprite_re = "^" + sprite_name
        compile   = re.compile(sprite_re)
        
        for sprite in self.sprite_map_xml.keys():
            if compile.match(sprite) is not None:
                sprites_info.append(self.sprite_map_xml[sprite])
        
        return sprites_info
    
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
    
    SCREEN.fill(COLORS["WHITE"])

    #player_item_hit_list  = pygame.sprite.groupcollide(objects["PLAYER"], objects["ITEMS"], False, False)
    #player_enemy_hit_list = pygame.sprite.groupcollide(objects["PLAYER"], objects["ENEMIES"], False, False)
    #enemy_player_hit_list = pygame.sprite.groupcollide(objects["ENEMIES"], objects["PLAYER"], False, False)
    #enemy_map_hit_list    = pygame.sprite.groupcollide(objects["ENEMIES"], objects["MAP"], False, False)
    
    if not level["RENDERED"]:
        for object in objects["BACKGROUND"]:
            SCREEN.blit(object.image, (object.x, object.y))
        
        for object in objects["HUD"]:
            SCREEN.blit(object.image, (object.x, object.y))

        for object in objects["MAIN"]:
            SCREEN.blit(object.image, (object.x, object.y))

        pygame.display.flip()
        level["RENDERED"] = True
    else:
        rect_list = []

        for object in objects["MAIN"]:
            if object.oldx != object.x or object.oldy != object.y or object.dirty:
                rect_list.append(
                    pygame.Rect(
                        (object.oldx, object.oldy),
                        (object.oldwidth, object.oldheight)
                    )
                )
                rect_list.append(
                    pygame.Rect(
                        (object.x, object.y),
                        (object.rect.width, object.rect.height)
                    )
                )
        
        for object in objects["BACKGROUND"]:
            for rect in rect_list:
                if object.rect.colliderect(rect):
                    SCREEN.blit(object.image, (object.x, object.y))

        for object in objects["HUD"]:
            for rect in rect_list:
                if object.rect.colliderect(rect):
                    SCREEN.blit(object.image, (object.x, object.y))

        for object in objects["MAIN"]:
            if (object.oldx != object.x or object.oldy != object.y or object.dirty) and \
               object.hit_time % 2 == 0:
                SCREEN.blit(object.image, (object.x, object.y))
                object.dirty = False
        
        pygame.display.update(rect_list)

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
