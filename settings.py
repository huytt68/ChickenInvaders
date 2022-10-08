import pygame

class Settings:
    """ A class to store all settings for Alien Invasion. """

    def __init__(self):
        """Initialize the game's static settings."""
        # Screen settings
        self.screen_width = 1024
        self.screen_height = 640
        self._load_bg = pygame.image.load('images/Background/jbg4.jpg')
        self.screen_bg = pygame.transform.scale(self._load_bg, (self.screen_width, self.screen_height))
        self.name_player = ''
        
        #setting game's speed
        self.game_speed = 30

        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (255, 0, 0)

        # Chicken settings
        self.fleet_drop_speed = 10

        # How quickly the game speeds up
        self.speedup_scale = 1.1

        # How quickly the chicken point values increase
        self.score_scale = 1.5
        #Cost of ship
        self.cost_ship_1 =6000
        self.cost_ship_2 =2000

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 15
        self.bullet_speed = 20.0
        self.chicken_speed = 1.5
        # fleet_direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1

        # Scoring
        self.collisions = 10000
        self.chicken_points = 50
        self.roast_points = 30
        self.drumstick_points = 15
        self.gift_points = 500
        self.heart_points = 1000

    def increase_speed(self):
        """Increase speed settings and chicken point values."""
        # self.ship_speed *= self.speedup_scale
        # self.bullet_speed *= self.speedup_scale
        self.chicken_speed *= self.speedup_scale

        self.chicken_points = int(self.chicken_points * self.score_scale)