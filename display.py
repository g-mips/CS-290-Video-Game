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
    def __init__(self, sprite_maps, z_index=0):
        self.sprite_maps = sprite_maps
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

    if not objects["MAP"].rendered:
        objects["MAP"].render(SCREEN)
        
        for object in sorted(objects["OBJECTS"]):
            object.render(SCREEN)
    
            pygame.display.flip()
    else:
        rects = []

        for object in sorted(objects["OBJECTS"]):
            rects.append(object.get_rect())

        objects["MAP"].render_part(SCREEN, rects)

        for object in sorted(objects["OBJECTS"]):
            object.render(SCREEN)
            
        pygame.display.update(rects)              

def get_image(filenames):
    global IMAGES

    images = []

    for filename in filenames:
        if filename in IMAGES:
            images.append(IMAGES[filename])
        else:
            image = pygame.image.load(filename)
            image.convert_alpha()

            IMAGES[filename] = image
            images.append(image)

    return images;
