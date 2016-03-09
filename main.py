import logger

import sys
import inspect
import pygame

WIDTH     = 800
HEIGHT    = 600
PLAY_GAME = True
TITLE     = "Musical Alien"

def main():
    # Initialize PyGame
    num_successes, num_fails = pygame.init()

    logger.debug("Number of modules initialized: " + str(num_successes), inspect.stack())
    logger.debug("Number of modules failed: " + str(num_fails), inspect.stack())

    # Set the mode of the display
    game_display = pygame.display.set_mode((WIDTH, HEIGHT))

    # Set the title of the game
    pygame.display.set_caption("Musical Alien")

    while PLAY_GAME:
        pass

    pygame.quit()
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
