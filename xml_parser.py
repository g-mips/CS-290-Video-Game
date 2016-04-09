import xml.etree.ElementTree
import os

import logger

XML_SPRITE_SHEETS = {}


def load_level(level_xml):
    '''
    This loads the level given by the level_xml.
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
                            "SCALE_FACT":   float(child.attrib['scaleFactor']),
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
                    "SCALE_FACT":   float(child.attrib['scaleFactor']),
                    "COLLISION":    int(child.attrib['collision'], 2),
                    "SPRITE_SHEET": child.attrib['spriteSheet'],
                    "XML_SHEET":    child.attrib['xmlSheet'],
                    "Z_INDEX":      int(child.attrib['zIndex'])                
                })

                if child.tag == "Player":
                    sprites[len(sprites)-1]["ATTACK"] = child.attrib['attack']

        XML_SPRITE_SHEETS[level_xml] = sorted(sprites, key=lambda k: k['Z_INDEX']) 
    
    return XML_SPRITE_SHEETS[level_xml]

def load_sprite_map_info(sprite_map_xml):
    '''
    This loads all the information found in sprite_map_xml, which regards sprites found
    on its companion "PNG" file.
    '''
    global XML_SPRITE_SHEETS

    # Load sprite_map__xml
    if sprite_map_xml not in XML_SPRITE_SHEETS:
        sprite_map = xml.etree.ElementTree.parse(sprite_map_xml).getroot()

        map_info = {}
        
        for child in sprite_map:
            atts = child.attrib
            info = [[int(atts['x']), int(atts['y'])], [int(atts['width']), int(atts['height'])]]
            
            map_info[atts['name']] = info
            
        XML_SPRITE_SHEETS[sprite_map_xml] = map_info

    return XML_SPRITE_SHEETS[sprite_map_xml]
