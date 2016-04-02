import xml.etree.ElementTree
import os

import logger

MAIN_SPRITE_SHEET = os.path.join('imgs', 'spritesheet_complete.png')
MAIN_XML_SHEET    = os.path.join('xmlsheets', 'spritesheet_complete.xml')
TREE = xml.etree.ElementTree.parse(MAIN_XML_SHEET)


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

def load_map_info(xml_sheet=None):
    global TREE

    if xml_sheet is None:
        map_info = {}
    
        root = TREE.getroot()
        for child in root:
            atts = child.attrib
            info = [(int(atts['x']), int(atts['y'])), (int(atts['width']), int(atts['height']))]
        
            if 'grass' in atts['name']:
                map_info[atts['name']] = info
            
        return map_info
    else:
        map_info = {}
        
        root = xml.etree.ElementTree.parse(xml_sheet).getroot()
        for child in root:
            atts = child.attrib
            info = [(int(atts['x']), int(atts['y'])), (int(atts['width']), int(atts['height']))]
            
            map_info[atts['name']] = info

        return map_info
             
def load_map(level_xml, tile_size):
    level = xml.etree.ElementTree.parse(level_xml).getroot()
    tiles = []

    width = int(level.attrib['width'])
    height = int(level.attrib['height'])

    for child in level:
        if child.tag == "Tile":
            tiles.append((child.attrib['name'], int(child.attrib['x'])*tile_size,
                          int(child.attrib['y'])*tile_size, int(child.attrib['sheetindex'])))
        elif child.tag == "TileGroup":
            min_x = int(child.attrib['minx'])
            max_x = int(child.attrib['maxx'])
            min_y = int(child.attrib['miny'])
            max_y = int(child.attrib['maxy'])

            for x in range(min_x, max_x):
                for y in range(min_y, max_y):
                    tiles.append((child.attrib['name'], x*tile_size, y*tile_size,
                                  int(child.attrib['sheetindex'])))

    #{ 0: { 0: [], 50: [] }, 50: }
    sorted_tiles = {}
    
    for tile in tiles:
        if tile[1] in sorted_tiles:
            if tile[2] in sorted_tiles[tile[1]]:
                sorted_tiles[tile[1]][tile[2]].append(tile)
            else:
                sorted_tiles[tile[1]][tile[2]] = [ tile ]
        else:
            sorted_tiles[tile[1]] = {}
            sorted_tiles[tile[1]][tile[2]] = [ tile ]
                                      
    
    return (sorted_tiles, width, height)
