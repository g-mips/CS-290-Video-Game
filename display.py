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


class Renderable(pygame.sprite.Sprite):
    def __init__(self, sprite_map, sprite_map_xml, z_index=0):
        pygame.sprite.Sprite.__init__(self)
        self.image = None
        self.rect = None
        
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
    
    #if not level["RENDERED"]:
    rect_list = objects.draw(SCREEN)
        #for group in objects:
        #    objects[group].draw(SCREEN)
    level["RENDERED"] = True
    pygame.display.update(rect_list)
    #else:
    #    map_draw_list = pygame.sprite.OrderedUpdates()

    #rect_list = [ objects["PLAYER"].sprite.rect ]
    #    rect_list.extend(objects["ENEMIES"].sprites())

    #    map_hit_list = pygame.sprite.groupcollide(objects["MAP"], objects["HUD"], False, False)
    #    map_hit_list.update(pygame.sprite.groupcollide(objects["PLAYER"], objects["MAP"], False, False))
    #    map_hit_list.update(pygame.sprite.groupcollide(objects["ENEMIES"], objects["MAP"], False, False))

    #    for group in map_hit_list:
    #        for tile in sorted(map_hit_list[group]):
    #            map_draw_list.add(tile)

    #    for object in sorted(physics.PHYSICS_SYSTEM.objects_to_update):
    #        map_draw_list.add(object)

    #    map_hit_list = pygame.sprite.groupcollide(map_draw_list, objects["MAP"], False, False)

    #    for main_tile in map_hit_list:
    #        for tile in sorted(map_hit_list[main_tile]):
    #            map_draw_list.add(tile)
        
    #    rect_list.extend(map_draw_list.draw(SCREEN))
    #    rect_list.extend(objects["HUD"].draw(SCREEN))
    #    objects["ENEMIES"].draw(SCREEN)
    #    objects["PLAYER"].draw(SCREEN)
        
    #    pygame.display.update(rect_list)

    #    physics.PHYSICS_SYSTEM.objects_to_update = []

    #else:
    #objects["MAP"].draw(SCREEN)
    #objects["ITEMS"].draw(SCREEN)
    #objects["ENEMIES"].draw(SCREEN)
    #objects["PLAYER"].draw(SCREEN)
    #objects["HUD"].draw(SCREEN)
    
    #if not objects["MAP"].rendered:
    #    objects["MAP"].render(SCREEN)
        
    #    for object in sorted(objects["OBJECTS"]):
    #        object.render(SCREEN)
    
    
    
    #else:
    #    rects = []

    #    for object in sorted(objects["OBJECTS"]):
    #        rects.append(object.get_rect())

    #    objects["MAP"].render_part(SCREEN, rects)

    #    for object in sorted(objects["OBJECTS"]):
    #        object.render(SCREEN)
            
    #    pygame.display.update(rects)              

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
