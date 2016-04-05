import xml.etree.ElementTree
import os

import logger

XML_SPRITE_SHEETS = {}


def load_level(level_xml):
    '''
    LEGIT
    '''
    global XML_SPRITE_SHEETS

    if level_xml not in XML_SPRITE_SHEETS:
        level = xml.etree.ElementTree.parse(level_xml).getroot()
                
        sprites = []
        
        width = int(level.attrib['width'])
        height = int(level.attrib['height'])

        # Go through each child
        for child in level:

            # Are we dealing with a group or non-group?
            if child.tag == "TileGroup":
                min_x = int(child.attrib['minx'])
                max_x = int(child.attrib['maxx'])
                min_y = int(child.attrib['miny'])
                max_y = int(child.attrib['maxy'])

                # Go through the range of the Group
                for x in range(min_x, max_x):
                    for y in range(min_y, max_y):
                        sprites.append({
                            "TYPE":         "Tile",
                            "NAME":         child.attrib['name'],
                            "X":            x,
                            "Y":            y,
                            "SCALE_X":      int(child.attrib['scaleX']),
                            "SCALE_Y":      int(child.attrib['scaleY']),                        
                            "COLLISION":    int(child.attrib['collision'], 2),
                            "SPRITE_SHEET": child.attrib['spriteSheet'],
                            "XML_SHEET":    child.attrib['xmlSheet'],
                            "Z_INDEX":      int(child.attrib['zIndex'])
                        })
            else:
                sprites.append({
                    "TYPE":         child.tag,
                    "NAME":         child.attrib['name'],
                    "X":            int(child.attrib['x']),
                    "Y":            int(child.attrib['y']),
                    "SCALE_X":      int(child.attrib['scaleX']),
                    "SCALE_Y":      int(child.attrib['scaleY']),
                    "COLLISION":    int(child.attrib['collision'], 2),
                    "SPRITE_SHEET": child.attrib['spriteSheet'],
                    "XML_SHEET":    child.attrib['xmlSheet'],
                    "Z_INDEX":      int(child.attrib['zIndex'])                
                })
                
        XML_SPRITE_SHEETS[level_xml] = sprites
    
    return XML_SPRITE_SHEETS[level_xml]

def load_map_info(xml_sheet):
    '''
    LEGIT
    '''

    map_info = {}
        
    root = xml.etree.ElementTree.parse(xml_sheet).getroot()
    for child in root:
        atts = child.attrib
        info = [(int(atts['x']), int(atts['y'])), (int(atts['width']), int(atts['height']))]
        
        map_info[atts['name']] = info

    return map_info

def load_sprite_map_info(sprite_map_xml):
    '''
    LEGIT
    '''
    global XML_SPRITE_SHEETS

    # Load sprite_map__xml
    if sprite_map_xml not in XML_SPRITE_SHEETS:
        sprite_map = xml.etree.ElementTree.parse(sprite_map_xml).getroot()

        map_info = {}
        
        for child in sprite_map:
            atts = child.attrib
            info = [(int(atts['x']), int(atts['y'])), (int(atts['width']), int(atts['height']))]
            
            map_info[atts['name']] = info
            
        XML_SPRITE_SHEETS[sprite_map_xml] = map_info

    return XML_SPRITE_SHEETS[sprite_map_xml]

"""
def load_map(level_xml, tile_size):
    level = xml.etree.ElementTree.parse(level_xml).getroot()
    tiles = []

    width = int(level.attrib['width'])
    height = int(level.attrib['height'])

    for child in level:
        if child.tag == "Tile":
            tiles.append((child.attrib['name'], int(child.attrib['x'])*tile_size,
                          int(child.attrib['y'])*tile_size, int(child.attrib['sheetindex']),
                          int(child.attrib['tileCollision'], 2)))
        elif child.tag == "TileGroup":
            min_x = int(child.attrib['minx'])
            max_x = int(child.attrib['maxx'])
            min_y = int(child.attrib['miny'])
            max_y = int(child.attrib['maxy'])

            for x in range(min_x, max_x):
                for y in range(min_y, max_y):
                    tiles.append((child.attrib['name'], x*tile_size, y*tile_size,
                                  int(child.attrib['sheetindex']), int(child.attrib['tileCollision'], 2)))

    return (tiles, width, height)


def load_players(player_info, players, actions):
    global TREE

    root = TREE.getroot()
    for child in root:
        atts = child.attrib
        
        if 'alienBeige' in atts['name']:
            player_info = load_player(player_info, players.BEIGE, actions, atts)
        elif 'alienBlue' in atts['name']:
            player_info = load_player(player_info, players.BLUE, actions, atts)
        elif 'alienGreen' in atts['name']:
            player_info = load_player(player_info, players.GREEN, actions, atts)
        elif 'alienPink' in atts['name']:
            player_info = load_player(player_info, players.PINK, actions, atts)
        elif 'alienYellow' in atts['name']:
            player_info = load_player(player_info, players.YELLOW, actions, atts)             
                
    return player_info

def load_player(player_info, player_index, actions, atts):
    info = [(int(atts['x']), int(atts['y'])), (int(atts['width']), int(atts['height']))]
    
    if 'climb' in atts['name']:
        player_info[player_index][actions.CLIMB].append(info)
    elif 'duck' in atts['name']:
        player_info[player_index][actions.DUCK].append(info)
    elif 'front' in atts['name']:
        player_info[player_index][actions.FRONT].append(info)
    elif 'hit' in atts['name']:
        player_info[player_index][actions.HIT].append(info)
    elif 'jump' in atts['name']:
        player_info[player_index][actions.JUMP].append(info)
    elif 'stand' in atts['name']:
        player_info[player_index][actions.STAND].append(info)                    
    elif 'swim' in atts['name']:
        player_info[player_index][actions.SWIM].append(info)
    elif 'walk' in atts['name']:
        player_info[player_index][actions.WALK].append(info)

    return player_info

"""
