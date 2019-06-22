import arcade
import math
import os
import random
import threading
import time
from enum import Enum

from knife import Knife
from knifecount import KnifeCount
from target import Target

class GameState(Enum):
    """ Store game state in enum """

    MENU = 1
    GAME_RUNNING = 2
    TARGET_DEFEATED = 3
    GAME_OVER = 4


class GameManager(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, GAME_CONFIG):
        """ Initializer """

        # Get config data
        self.GAME_CONFIG = GAME_CONFIG
        self.SCREEN_WIDTH = GAME_CONFIG["general_settings"]["screen_width"]
        self.SCREEN_HEIGHT = GAME_CONFIG["general_settings"]["screen_height"]
        self.SCREEN_TITLE = GAME_CONFIG["general_settings"]["screen_title"]
        self.SPRITE_SCALING = GAME_CONFIG["general_settings"]["sprite_scaling"]
        self.GAME_OVER_DELAY = GAME_CONFIG["general_settings"]["game_over_delay"]
        self.BACKGROUND_INGAME = GAME_CONFIG["assets_path"]["images"]["background_ingame"]
        self.BACKGROUND_GAMEOVER = GAME_CONFIG["assets_path"]["images"]["background_gameover"]
        
        # Call the parent class initializer
        super().__init__(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, self.SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Initialize the game state
        self.current_state = GameState.GAME_RUNNING

        # Background image will be stored in this variable
        self.background = None

        # Variables that hold individual sprites
        self.knife = None
        self.target = None
        self.target_collider = None
        self.knife_count_display = None

        # Variables that will hold sprite lists
        self.knife_list = None
        self.target_list = None
        self.target_collider_list = None
        self.knife_count_display_list = None

        # Set up the game score
        self.score = 0
        self.stage = 1
        self.score_text = None
        self.knife_count = None

        # Don't show the mouse cursor
        # self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        self.background_ingame = arcade.load_texture(self.BACKGROUND_INGAME)
        self.background_gameover = arcade.load_texture(self.BACKGROUND_GAMEOVER)

        # Sprite lists
        self.knife_list = arcade.SpriteList()
        self.target_list = arcade.SpriteList()
        self.target_collider_list = arcade.SpriteList()
        self.knife_count_display_list = arcade.SpriteList()

        # Set up the game score and knife count
        self.knife_count = random.randrange(6,10)

        # Set up the knife
        self.create_knife()

        # Set up knife count display
        self.create_knife_count_display()

        # Set up the target
        self.create_target()

        # Set up the target collider
        self.create_target_collider()
    
    def draw_game_over(self):
        """ Draw game over menu across the screen. """

        # Reset the score and stage number
        self.score = 0
        self.stage = 1

        # Draw the background texture
        arcade.draw_texture_rectangle(
            self.SCREEN_WIDTH // 2, 
            self.SCREEN_HEIGHT // 2,
            self.SCREEN_WIDTH, 
            self.SCREEN_HEIGHT, 
            self.background_gameover)

        # Display "Game Over" text
        output = "Game Over"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.5, self.SCREEN_HEIGHT*0.6, arcade.color.WHITE, 54,  align="center", anchor_x="center")

        # Display restart instruction
        output = "Press <ENTER> To Restart"
        arcade.draw_text(output, self.SCREEN_WIDTH*0.5, self.SCREEN_HEIGHT*0.55, arcade.color.WHITE, 24,  align="center", anchor_x="center")
    
    def draw_game(self):
        """ Draw all the sprites, along with the score. """

        # Draw the background texture
        arcade.draw_texture_rectangle(
            self.SCREEN_WIDTH // 2, 
            self.SCREEN_HEIGHT // 2,
            self.SCREEN_WIDTH, 
            self.SCREEN_HEIGHT, 
            self.background_ingame
            )

        # Draw all the sprites.
        self.knife_list.draw()
        self.target_list.draw()
        self.knife_count_display_list.draw()

        # Display score
        output = f"{self.score}"
        arcade.draw_text(
            output, self.SCREEN_WIDTH*0.1, self.SCREEN_HEIGHT*0.95, (239, 182, 90), 28,  
            align="center", anchor_x="center", anchor_y="center",
            )

        # Display stage number
        output = f"STAGE {self.stage}"
        arcade.draw_text(
            output, self.SCREEN_WIDTH*0.5, self.SCREEN_HEIGHT*0.95, arcade.color.WHITE, 28,
            align="center", anchor_x="center", anchor_y="center"
            )

    def on_draw(self):
        """ Render the screen. """

        # This command has to happen before we start drawing
        arcade.start_render()

        # Redirect to main menu
        # if self.current_state == GameState.MENU:
        #     self.draw_menu()
        
        # Redirect to in game screen
        if self.current_state == GameState.GAME_RUNNING:
            self.draw_game()

        # Redirect to game over screen
        else:
            # self.draw_game()
            self.draw_game_over()
        
    def update(self, delta_time):
        """ Movement and game logic """

        # Run update function of every object
        self.target_list.update()
        self.knife_list.update()
        self.target_collider_list.update()

        # Check if knife collided with the knifes stucked in the target.
        knife_hit_list = arcade.check_for_collision_with_list(self.knife, self.knife_list)
        if not self.knife.target_hitted:
            for collided_object in knife_hit_list:
                # Show "knife propelled" animation
                self.knife.propel_knife(self.target.TARGET_ROTATION_SPEED)

                # Put the game over trigger in a thread so we can show the "knife propelled" animation
                game_over_trigger_thread = threading.Thread(target=self.trigger_game_over, args=(self.GAME_OVER_DELAY,))
                game_over_trigger_thread.start()
        
        # Check if knife collided with the target.
        target_hit_list = arcade.check_for_collision_with_list(self.knife, self.target_collider_list)
        if not self.knife.target_hitted and not self.knife.knife_hitted:
            for collided_object in target_hit_list:
                # Add 1 to the score when knife successfully hit the target
                self.score += 1

                # Play the target hit impact animation
                self.target.hit_impact()

                # Calculate the knife angular rotation radius based on collider height
                rotation_radius = (self.target_collider.height/2)+30
                self.knife.hit_target(collided_object.TARGET_ROTATION_SPEED, rotation_radius, collided_object.TARGET_POSITION)
                
                # Spawn new knife
                if self.knife_count > 0:
                    self.create_knife()
                else:
                    # self.current_state = GameState.TARGET_DEFEATED
                    self.create_new_stage()

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """

        # Shoot knife
        if key == arcade.key.SPACE and self.knife_count > 0:
            self.knife_count -= 1
            self.knife.shoot_knife()
            self.knife_count_display_list.pop()

        # Restart game
        if key == arcade.key.ENTER and self.current_state == GameState.GAME_OVER:
            self.setup()
            self.current_state = GameState.GAME_RUNNING
    
    def create_new_stage(self):
        """ Create new stage """
        # Reset these variables
        # Variables that hold individual sprites
        self.knife = None
        self.target = None
        self.target_collider = None
        self.knife_count_display = None

        # Variables that will hold sprite lists
        self.knife_list = None
        self.target_list = None
        self.target_collider_list = None
        self.knife_count_display_list = None

        self.stage += 1
        self.setup()
        self.current_state = GameState.GAME_RUNNING

    def create_target(self):
        """ Create new target """
        self.target = Target(self.GAME_CONFIG, scale_ratio=1.2)
        self.target_list.append(self.target)
    
    def create_target_collider(self):
        """ Create new target collider """
        self.target_collider = Target(self.GAME_CONFIG, scale_ratio=1.5)
        self.target_collider_list.append(self.target_collider)
    
    def create_knife(self):
        """ Create new knife """
        self.knife = Knife(self.GAME_CONFIG)
        self.knife_list.append(self.knife)
    
    def create_knife_count_display(self):
        """ Create knife count display """
        # Create the background display
        for i in range(self.knife_count):
            self.knife_count_display = KnifeCount(self.GAME_CONFIG, "background", i)
            self.knife_count_display_list.append(self.knife_count_display)

        # Create the foreground display
        for i in range(self.knife_count):
            self.knife_count_display = KnifeCount(self.GAME_CONFIG, "foregroud", i)
            self.knife_count_display_list.append(self.knife_count_display)
    
    def trigger_game_over(self, delay):
        """ Trigger game over after certain delay """
        time.sleep(delay)
        self.current_state = GameState.GAME_OVER

