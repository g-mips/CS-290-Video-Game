import scenes

OBJECTS = []
MAP     = None
LEVEL   = 1

def update():
    global MAP
    global OBJECTS
    
    if MAP is None:
        # EVENTUALLY: call run_start()

        # Load first level, and objects
        MAP, OBJECTS = scenes.load_level(LEVEL)
    else:
        # Check if new Map will be loaded (check player's position against goal in map)

        # If yes, increment to next map. If last map, call run_end()
        
        # If yes, remove all objects and load in new objects
        pass

    for object in OBJECTS:
        if object.isAlive:
            object.update()

