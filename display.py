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
OBJECTS = []

def init(width, height, title):
    global SCREEN

    if SCREEN is None:
        SCREEN = pygame.display.set_mode((width, height))

    pygame.display.set_caption(title)


def render():
    global SCREEN
    global COLORS
    global OBJECTS

    SCREEN.fill(COLORS["WHITE"])

    for object in OBJECTS:
        pass
    
    pygame.display.flip()

def get_image(filename):
    global IMAGES
    image = pygame.image.load(filename)
    image.convert_alpha()

    IMAGES[filename] = image

    return image
