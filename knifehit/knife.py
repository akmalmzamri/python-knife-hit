import arcade
import math

class Knife(arcade.Sprite):
    """ Knife class """

    def __init__(self, GAME_CONFIG):
        """ Initialize knife """

        self.SCREEN_WIDTH = GAME_CONFIG["general_settings"]["screen_width"]
        self.SCREEN_HEIGHT = GAME_CONFIG["general_settings"]["screen_height"]
        self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["sprite_scaling"]
        
        self.KNIFE_POSITION = (self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT*(0.2))
        self.KNIFE_IMAGE = GAME_CONFIG["assets_path"]["images"]["knife"]
        self.KNIFE_MOVEMENT_SPEED = GAME_CONFIG["knife_settings"]["speed"]
        
        self.KNIFE_PROPELLED_SOUND = GAME_CONFIG["assets_path"]["sounds"]["knife_propelled"]
        self.KNIFE_PROPELLED_SOUND = arcade.load_sound(self.KNIFE_PROPELLED_SOUND)
        self.TARGET_HITTED_SOUND = GAME_CONFIG["assets_path"]["sounds"]["target_hitted"]
        self.TARGET_HITTED_SOUND = arcade.load_sound(self.TARGET_HITTED_SOUND)

        super().__init__(self.KNIFE_IMAGE, self.SPRITE_SCALING/2)

        self.center_x = self.KNIFE_POSITION[0]
        self.center_y = self.KNIFE_POSITION[1]
        self.rotation = 0
        self.target_hitted = False
        self.knife_hitted = False

        # Reshape the collision
        # self._set_collision_radius(self.collision_radius*0)
        
    
    def shoot_knife(self):
        """ Initialize the "knife shot" state """

        self.change_y  = self.KNIFE_MOVEMENT_SPEED

    def hit_target(self, rotation_speed, rotation_radius, rotation_center):
        """ 
        Initialize the "stuck in target" state 
        Copy the target's rotation speed and set the rotation radius and center
        """

        arcade.play_sound(self.TARGET_HITTED_SOUND)
        self.target_hitted = True
        self.change_y = 0
        self.rotation_speed = rotation_speed
        self.rotation_radius = rotation_radius
        self.rotation_center = rotation_center
    
    def propel_knife(self, rotation_speed):
        """ 
        Initialise the "knife propelled" state
        The propel direction is based on the rotation direction and speed
        """

        arcade.play_sound(self.KNIFE_PROPELLED_SOUND)
        self.rotation_speed = rotation_speed
        self.knife_hitted = True

    def update(self):
        """ Movement and game logic """
        
        # Reshape the collision
        # self.set_points((self.points))
        
        # Play the knife propelled animation
        if self.knife_hitted:
            self.center_y += -30
            self.center_x += self.rotation_speed*20
            self.angle += self.rotation_speed*20
        # Perform shooting animation when "shoot" button is press
        else:
            self.center_y += self.change_y
        
        # Stuck the knife into the target and have it spin together
        # We added 270 to the rotation because the knife must start from the bottom
        if self.target_hitted:
            self.rotation += self.rotation_speed
            self.angle = self.rotation
            self.center_x = (self.rotation_radius * math.cos(math.radians(self.rotation+270))) + self.rotation_center[0]
            self.center_y = (self.rotation_radius * math.sin(math.radians(self.rotation+270))) + self.rotation_center[1]

