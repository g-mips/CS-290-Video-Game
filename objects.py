import pygame
import os

import xml_parser
import display

MAIN_SPRITE_SHEET = os.path.join('imgs', 'spritesheet_complete.png')
MAIN_XML_SHEET    = os.path.join('xmlsheets', 'spritesheet_complete.xml')

class Players(object):
    BEIGE  = 0
    BLUE   = 1
    GREEN  = 2
    PINK   = 3
    YELLOW = 4

    NUM_PLAYERS = 5

class Actions(object):
    CLIMB = 0
    DUCK  = 1
    FRONT = 2
    HIT   = 3
    JUMP  = 4
    STAND = 5
    SWIM  = 6
    WALK  = 7

PLAYER_INFO = [ {
    # The array will contain two tuples as such: (x, y), (width, height)
    Actions.CLIMB: [],
    Actions.DUCK:  [],
    Actions.FRONT: [],
    Actions.HIT:   [],
    Actions.JUMP:  [],
    Actions.STAND: [],
    Actions.SWIM:  [],
    Actions.WALK:  []
} for x in range(0, Players.NUM_PLAYERS) ]

xml_parser.load_xml(MAIN_XML_SHEET)
PLAYER_INFO = xml_parser.load_players(PLAYER_INFO, Players, Actions)

class GameObject(display.Renderable):
    def __init__(self, input):
        super(GameObject, self).__init__(display.get_image(MAIN_SPRITE_SHEET))
        self.input = input
        self.isAlive  = True
        self.velocity = 0
        self.x = 0
        self.y = 0
        self.current_action = 0;
        self.frame = 0
        self.scale_factor = None

    def update(self):
        pass

    def render(self, screen):
        pass


class Alien(GameObject):
    def __init__(self, input):
        super(Alien, self).__init__(input)
        self.current_player = Players.GREEN
        self.current_action = Actions.JUMP
        s_width = 50
        s_height = s_width * 2
        self.scale_factor   = (s_width, s_height)

    def render(self, screen):
        screen.blit(
            pygame.transform.scale(
                self.sprite_map.subsurface(
                    pygame.Rect(
                        PLAYER_INFO[self.current_player][self.current_action][self.frame][0],
                        PLAYER_INFO[self.current_player][self.current_action][self.frame][1]
                    ),
                ),
                self.scale_factor
            ),
            (self.x, self.y)
        )

if __name__ == "__main__":
    xml_parser.load_xml(MAIN_XML_SHEET)
    PLAYER_INFO = xml_parser.load_players(PLAYER_INFO, Players, Actions)
    print(PLAYER_INFO)

