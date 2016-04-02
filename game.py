import scenes

OBJECTS = {}

def load_level(level):
    global OBJECTS
    
    OBJECTS = scenes.load_level(level)

def update():
    global OBJECTS
    
    # EVENTUALLY: call run_start()

    # Load first level, and objects

    
    # Check if new Map will be loaded (check player's position against goal in map)
    
    # If yes, increment to next map. If last map, call run_end()
    
    # If yes, remove all objects and load in new objects

    OBJECTS["MAP"].update()
    
    for object in OBJECTS["OBJECTS"]:
        if object.isAlive:
            object.update()

