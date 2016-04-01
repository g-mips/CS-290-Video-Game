import pygame


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
    def __init__(self, sprite_map, z_index=0):
        self.sprite_map = sprite_map
        self.z_index = z_index
        
    def render(self, screen):
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

def render(objects):
    global SCREEN
    global COLORS

    SCREEN.fill(COLORS["WHITE"])

    for object in sorted(objects):
        object.render(SCREEN)
    
    pygame.display.flip()

def get_image(filename):
    global IMAGES
    image = pygame.image.load(filename)
    image.convert_alpha()

    IMAGES[filename] = image

    return image
