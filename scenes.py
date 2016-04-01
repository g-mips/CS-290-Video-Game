import map
import objects
import game_input

def run_start():
    pass

def run_end():
    pass

def load_level(level):
    if level == 1:
        level_map = map.Map([])
        level_objects = [objects.Alien(game_input.PlayerInput())]
        return (level_map, level_objects)

    return None
