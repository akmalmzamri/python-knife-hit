import arcade

class Target(arcade.Sprite):
    """ 
    Target class
    """

    def __init__(self, GAME_CONFIG, scale_ratio=1):
        """ Initialize target """

        self.SCREEN_WIDTH = GAME_CONFIG["general_settings"]["screen_width"]
        self.SCREEN_HEIGHT = GAME_CONFIG["general_settings"]["screen_height"]
        self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["sprite_scaling"]
        self.TARGET_POSITION = (self.SCREEN_WIDTH//2, self.SCREEN_HEIGHT*(0.7))
        self.TARGET_ROTATION_SPEED = GAME_CONFIG["target_settings"]["rotation_speed"]
        self.TARGET_IMAGE = GAME_CONFIG["assets_path"]["images"]["target"]

        super().__init__(self.TARGET_IMAGE, self.SPRITE_SCALING/scale_ratio)
        
        self.center_x = self.TARGET_POSITION[0]
        self.center_y = self.TARGET_POSITION[1]
        # self.angle = random.randrange(360)
        self.change_angle = self.TARGET_ROTATION_SPEED
        
        self.hit_impact_animation = False
        self.original_position = self.center_y
        self.animation_counter = 0

    def update(self):
        """ Movement and game logic """

        # Rotate the target.
        # The arcade.Sprite class has an "angle" attribute that controls
        # the sprite rotation. Change this, and the sprite rotates.
        self.angle += self.change_angle

        # Play the hit impact animation
        if self.hit_impact_animation and self.animation_counter > 0:
            self.center_y += 3
            self.color = (255, 179, 179)
            self.animation_counter -= 1
        else:
            self.color = (255, 255, 255)
            self.hit_impact_animation = False
            self.animation_counter = 0
            self.center_y = self.original_position
    
    def hit_impact(self):
        """ Initialize the "hit impact" state """

        self.hit_impact_animation = True
        self.animation_counter = 3
        
