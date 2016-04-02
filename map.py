import pygame

import display
import xml_parser

MAP_INFO = xml_parser.load_map_info()

class Map(display.Renderable):
    def __init__(self, level_xml, playable, sprite_maps):
        super(Map, self).__init__(display.get_image(sprite_maps), -1)
        self.tiles, self.width, self.height = xml_parser.load_map(level_xml, 50)

        self.playable = playable
        self.scale_factor = (50, 50)
        self.rendered = False

    def add_tiles(self, xml_sheet):
        MAP_INFO.update(xml_parser.load_map_info(xml_sheet))

    def update(self):
        pass

    def render_part(self, screen, rects):
        for x in self.tiles:
            for y in self.tiles[x]:
                for tile in self.tiles[x][y]:
                    tile_rect = pygame.Rect((tile[1], tile[2]),
                                            (self.scale_factor[0], self.scale_factor[1]))

                    if tile_rect.collidelist(rects) != -1:
                        screen.blit(
                            pygame.transform.scale(
                                self.sprite_maps[tile[3]].subsurface(
                                    pygame.Rect(
                                        MAP_INFO[tile[0]][0],
                                        MAP_INFO[tile[0]][1]
                                    )
                                ),
                                self.scale_factor
                            ),
                            (tile[1], tile[2])
                        )
    
    def render(self, screen):
        for x in self.tiles:
            for y in self.tiles[x]:
                for tile in self.tiles[x][y]:
                    screen.blit(
                        pygame.transform.scale(
                            self.sprite_maps[tile[3]].subsurface(
                                pygame.Rect(
                                    MAP_INFO[tile[0]][0],
                                    MAP_INFO[tile[0]][1]
                                )
                            ),
                            self.scale_factor
                        ),
                        (tile[1], tile[2])
                    )
        self.rendered = True

