import logger
import event_handler
import display
import objects
import overall
import game

import sys
import inspect
import pygame

WIDTH  = 800
HEIGHT = 600
TITLE  = "Musical Alien"
CLOCK  = pygame.time.Clock()
FPS    = 30

def main():
    '''
    This is the starting function to start the game

    PARAMETERS:
        NONE

    RETURN:
        NONE
    '''
    global WIDTH
    global HEIGHT
    global TITLE
    global CLOCK
    global FPS
    
    # Initialize PyGame
    num_successes, num_fails = pygame.init()

    logger.debug("Number of modules initialized: " + str(num_successes))
    logger.debug("Number of modules failed: " + str(num_fails))

    # Initialize display
    display.init(WIDTH, HEIGHT, TITLE)

    event_handler.register("QUIT", overall.quit)
    event_handler.register("KEYDOWN", overall.key_quit)

    game.START_SCREEN = True
    
    # Main game loop
    while True:
        event_handler.handle_events()

        game.update()
        
        display.render(game.OBJECTS)

        #CLOCK.tick(FPS)

    # Should never reach here
    pygame.quit()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
