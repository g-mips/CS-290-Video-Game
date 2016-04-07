import pygame
import sys

import logger
import event_handler
import display
import scenes
import physics

LEVEL = {
    "OBJECTS":  {},
    "RENDERED": False,
    "LOADED":   False,
    "BACKGROUND": None,
    "HUD": None
}

CLOCK  = pygame.time.Clock()
LEVEL_NUM  = 1

def quit(event):
    # TODO: Ask user if he really wants to quit
    pygame.quit()
    sys.exit(0)

def key_quit(event):
    if event.key == pygame.K_ESCAPE:
        quit(event)

def initialize(width, height, title):
    '''
    Starts pygame, initializes the display, makes the mouse invisible, and registers quit events.
    '''
    global LEVEL
    
    num_successes, num_fails = pygame.init()

    logger.debug("Number of modules initialized: " + str(num_successes))
    logger.debug("Number of modules failed: " + str(num_fails))

    # Initialize display
    display.init(width, height, title)
    physics.PHYSICS_SYSTEM.width = width
    physics.PHYSICS_SYSTEM.height = height

    LEVEL["BACKGROUND"] = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()
    LEVEL["HUD"] = pygame.Surface((width, height), pygame.SRCALPHA, 32).convert_alpha()

    event_handler.register("QUIT", quit)
    event_handler.register("KEYDOWN", key_quit)

    pygame.mouse.set_visible(False)

def game_loop(fps):
    '''
    Game loops here indefinitely
    '''
    global CLOCK

    logger.debug("Start game loop")

    while True:
        event_handler.handle_events()
        update()
        display.render(LEVEL)

        CLOCK.tick(fps)


def load_level(level):
    '''
    This will load in all the objects of the level 'level' into OBJECTS
    '''
    global OBJECTS

    logger.debug("Loading level: " + str(level))
    
    LEVEL["OBJECTS"]  = scenes.load_level(level)
    LEVEL["RENDERED"] = False
    LEVEL["LOADED"]   = True
    LEVEL_NUM         = level + 1

def update():
    '''
    This goes through LEVEL and updates all the objects in each group. An update to an object is
    through input, physics, and graphics. It does NOT draw/render the image of the object to the
    screen.
    '''
    global LEVEL
    global LEVEL_NUM

    if not LEVEL["LOADED"]:
        LEVEL["OBJECTS"] = scenes.load_level(LEVEL_NUM)

    physics.PHYSICS_SYSTEM.load_objects(LEVEL["OBJECTS"])
        
    for layer in LEVEL["OBJECTS"]:
        for object in layer:
            object.update()
            object.pre_render()

