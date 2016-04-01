import sys
import pygame

import logger

def quit(event):
    # TODO: Ask user if he really wants to quit
    pygame.quit()
    sys.exit(0)

def key_quit(event):
    '''
    This defines how a handler for key's pressed down.

    PARAMETERS:
        event - The event that was pressed down

    RETURN:
        NONE
    '''
    logger.debug(event)
    if event.key == pygame.K_ESCAPE:
        # TODO: Ask user if he really wants to quit
        if True:
            quit(event)
