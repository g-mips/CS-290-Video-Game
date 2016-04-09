import game

import sys

WIDTH  = 800
HEIGHT = 600
TITLE  = "Musical Alien"
FPS    = 30

def main():
    '''
    This is the starting function to start the game
    '''

    game.initialize(WIDTH, HEIGHT, TITLE)
    
    game.game_loop(FPS)
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
