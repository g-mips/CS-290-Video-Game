import pygame
import sys

import logger
import event_handler
import display
import scenes
import physics

LEVEL = {
    "OBJECTS":  [],
    "RENDERED": False,
    "LOADED":   False
}

CLOCK  = pygame.time.Clock()
LEVEL_NUM  = 1

GAME_OVER = False
WON = False

def quit(event):
    '''
    This will quit the game
    '''
    pygame.quit()
    sys.exit(0)

def key_quit(event):
    '''
    If the Escape key was pressed, this will quit the game
    '''
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

    event_handler.register("QUIT", quit)
    event_handler.register("KEYDOWN", key_quit)
    
    pygame.mouse.set_visible(False)

def game_loop(fps):
    '''
    Game loops here indefinitely
    '''
    global CLOCK
    global GAME_OVER
    global LEVEL
    global WON

    logger.debug("Start game loop")

    while True:
        # Handle any and all events
        event_handler.handle_events()

        # Is there a reason to quit the game?
        if not GAME_OVER:
            # Update the game state
            update()

            # Render the game state to the screen
            objects_to_remove, exist_enemies = display.render(LEVEL)

            # Remove the items from the game that are dead
            for layer in objects_to_remove:
                for id in objects_to_remove[layer]:
                    index = 0
                    for game_object in LEVEL["OBJECTS"][layer]:
                        if id == game_object.id:
                            LEVEL["OBJECTS"][layer].pop(index)
                            break
                        index += 1

            # If there are no more enemies, the level has been beaten
            if not exist_enemies:
                event_handler.remove_all()
                LEVEL["OBJECTS"] = []
                LEVEL["LOADED"]  = False
        else:
            display.game_over(WON)

        # We only want the game to go as fast as fps
        CLOCK.tick(fps)


def load_level(level):
    '''
    This will load in all the objects of the level 'level' into OBJECTS
    '''
    global OBJECTS
    global LEVEL
    global LEVEL_NUM

    logger.debug("Loading level: " + str(level))

    # Level 8 is the last level
    if LEVEL_NUM != 8:
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
    global GAME_OVER
    global WON

    # Was there a level change?
    if not LEVEL["LOADED"] and LEVEL_NUM != 8:
        event_handler.register("QUIT", quit)
        event_handler.register("KEYDOWN", key_quit)
        load_level(LEVEL_NUM)
    elif not LEVEL["LOADED"] and LEVEL_NUM == 8:
        GAME_OVER = True
        WON = True
        return

    # Load the current objects into the physics system
    physics.PHYSICS_SYSTEM.load_objects(LEVEL["OBJECTS"])

    # Update each object in each layer
    for layer in LEVEL["OBJECTS"]:
        for object in layer:
            object.update()
            object.pre_render()

            # Did the player die? Did the player attack?
            if object.type == "Player" and not object.is_alive:
                GAME_OVER = True
            elif object.type == "Player" and object.attacking and object.buffer_attack == 0:
                startx = 0

                if object.x_flip:
                    startx = object.x - 1
                else:
                    startx = object.x+object.width+1
                    
                LEVEL["OBJECTS"][0].append(scenes.add_fire_ball(len(LEVEL["OBJECTS"]),
                                                              startx, object.y,
                                                              object.x_flip))
                object.buffer_attack = 15



