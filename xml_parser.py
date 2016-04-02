import xml.etree.ElementTree
import os

import logger

MAIN_SPRITE_SHEET = os.path.join('imgs', 'spritesheet_complete.png')
MAIN_XML_SHEET    = os.path.join('xmlsheets', 'spritesheet_complete.xml')
TREE = xml.etree.ElementTree.parse(MAIN_XML_SHEET)

#def load_xml(xml_sheet):
#    global TREE
#    TREE = xml.etree.ElementTree.parse(xml_sheet)

def load_players(player_info, players, actions):
    global TREE

    #   if TREE is None:
    #       logger.error("Please call load_xml(xml_sheet) first!")
    #   else:
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

def load_map_info():
    global TREE

    map_info = {}
    
    #    if TREE is None:
    #    logger.error("Please call load_xml(xml_sheet) first!")
    #else:
    root = TREE.getroot()
    for child in root:
        atts = child.attrib
        info = [(int(atts['x']), int(atts['y'])), (int(atts['width']), int(atts['height']))]
        
        if 'grass' in atts['name']:
            map_info[atts['name']] = info
            
    return map_info

def load_map(level_xml):
    level = xml.etree.ElementTree.parse(level_xml).getroot()
    tiles = []

    width = int(level.attrib['width'])
    height = int(level.attrib['height'])

    for child in level:
        tiles.append((child.attrib['name'], int(child.attrib['x']), int(child.attrib['y'])))
    
    return (tiles, width, height)

            
    
