import pygame

import display
import xml_parser

MAP_INFO = xml_parser.load_map_info()

class Map(display.Renderable):
    def __init__(self, level_xml, playable):
        super(Map, self).__init__(display.get_image(xml_parser.MAIN_SPRITE_SHEET), -1)
        self.tiles, self.width, self.height = xml_parser.load_map(level_xml)
        self.playable = playable

    def load_map(self):
        pass

    def update(self):
        pass

    def render(self, screen):
        for tile in self.tiles:
            screen.blit(
                self.sprite_map.subsurface(
                    pygame.Rect(
                        MAP_INFO[tile[0]][0],
                        MAP_INFO[tile[0]][1]
                    )
                ),
                (tile[1], tile[2])
            )
