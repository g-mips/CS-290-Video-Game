import game

import sys

WIDTH  = 800
HEIGHT = 600
TITLE  = "Musical Alien"
FPS    = 60

def main():
    '''
    This is the starting function to start the game

    PARAMETERS:
        NONE

    RETURN:
        NONE
    '''

    game.initialize(WIDTH, HEIGHT, TITLE)
    
    game.load_level(1)

    game.game_loop(FPS)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
