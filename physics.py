class PlayerPhysics(object):
    def __init__(self):
        pass

    def update(self, game_object):
        game_object.x += game_object.dx
        game_object.y += game_object.dy

        # Collision Detection

        # Air Time
        if game_object.air_time > 0 and game_object.air_time < 100:
            game_object.air_time += 1
        elif game_object.air_time >= 100:
            game_object.dy = 1
            game_object.air_time = 0
