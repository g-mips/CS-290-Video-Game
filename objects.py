import pygame
import os

import xml_parser
import display


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

PLAYER_INFO = xml_parser.load_players(PLAYER_INFO, Players, Actions)


class GameObject(display.Renderable):
    def __init__(self, input, physics, graphics):
        super(GameObject, self).__init__(display.get_image(xml_parser.MAIN_SPRITE_SHEET))

        self.input = input
        self.input.game_object = self

        self.physics = physics

        self.graphics = graphics
        
        self.isAlive  = True

        self.dx = 0
        self.dy = 0
        self.x = 40
        self.y = 200

        self.current_action = None
        
        self.clock = pygame.time.Clock()
        self.frame = 0.0
        
        self.scale_factor = None
        
        self.x_flip = False
        self.y_flip = False

        self.events    = []
        self.keys_down = []
        self.keys_up   = []

    def update(self):
        self.input.update(self)
        self.physics.update(self)
        self.graphics.update(self)

    def render(self, screen):
        pass


class Alien(GameObject):
    def __init__(self, input, physics, graphics):
        super(Alien, self).__init__(input, physics, graphics)
        self.current_player = Players.GREEN
        self.current_action = Actions.STAND
        s_width = 50
        s_height = s_width * 2
        self.scale_factor   = (s_width, s_height)
        self.air_time = 0

    def render(self, screen):
        self.frame = (self.frame + (self.clock.tick() / 100.0)) % \
            len(PLAYER_INFO[self.current_player][self.current_action])
        
        screen.blit(
            pygame.transform.scale(
                pygame.transform.flip(
                    self.sprite_map.subsurface(
                        pygame.Rect(
                            PLAYER_INFO[self.current_player][self.current_action][int(self.frame)][0],
                            PLAYER_INFO[self.current_player][self.current_action][int(self.frame)][1]
                        )
                    ),
                    self.x_flip,
                    self.y_flip
                ),
                self.scale_factor
            ),
            (self.x, self.y)
        )

if __name__ == "__main__":
    xml_parser.load_xml(MAIN_XML_SHEET)
    PLAYER_INFO = xml_parser.load_players(PLAYER_INFO, Players, Actions)
    print(PLAYER_INFO)

