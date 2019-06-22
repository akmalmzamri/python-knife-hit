import arcade
import math

class Obstacle(arcade.Sprite):
    """ Obstacle class """

    def __init__(self, GAME_CONFIG, rotation_speed, rotation_radius, rotation_center, initial_rotation_position, rotation_mode=None):
        """ Initialize obstacle """

        self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["sprite_scaling"]
        self.KNIFE_IMAGE = GAME_CONFIG["assets_path"]["images"]["knife"]

        super().__init__(self.KNIFE_IMAGE, self.SPRITE_SCALING/2)

        self.center_x = 0
        self.center_y = 0
        self.rotation = 0
        self.rotation_speed = rotation_speed
        self.rotation_radius = rotation_radius
        self.rotation_center = rotation_center
        self.initial_rotation_position = initial_rotation_position

    def update(self):
        """ Movement and game logic """
        
        # Rotation angle must be added with the initial rotation and 90 degress
        self.rotation += self.rotation_speed
        self.angle = self.rotation+self.initial_rotation_position+90
        self.center_x = (self.rotation_radius * math.cos(math.radians(self.rotation+self.initial_rotation_position))) + self.rotation_center[0]
        self.center_y = (self.rotation_radius * math.sin(math.radians(self.rotation+self.initial_rotation_position))) + self.rotation_center[1]
