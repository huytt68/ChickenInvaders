import pygame
import random
from pygame.sprite import Sprite
from os import listdir
from os.path import isfile, join

CHICKEN_HP = {'baby_chicken': 30, 'pilot_chicken': 50}
CHICKEN_SIZE = {'baby_chicken': (40,40), 'pilot_chicken': (50,50)}
LOAD_CHICKEN_IMAGES = {'baby_chicken': [pygame.image.load('images/Chicken/baby_chicken/'+f) for f in listdir('images/Chicken/baby_chicken/')],
                'pilot_chicken': [pygame.image.load('images/Chicken/pilot_chicken/'+f) for f in listdir('images/Chicken/pilot_chicken/')]}
CHICKEN_IMAGES = {'baby_chicken': [pygame.transform.scale(i, CHICKEN_SIZE['baby_chicken']) for i in LOAD_CHICKEN_IMAGES['baby_chicken']],
                 'pilot_chicken': [pygame.transform.scale(i, CHICKEN_SIZE['pilot_chicken']) for i in LOAD_CHICKEN_IMAGES['pilot_chicken']]}

class Chicken(Sprite):
    """ A class to represent a signgle chicken in the fleet. """
    width_default = 50
    height_default = 50
    
    def __init__(self, ai_game, typeof='baby_chicken'):
        """Initialize the chicken and set its starting position."""
        super().__init__()
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        self.type = typeof
        self.width = CHICKEN_SIZE[self.type][0]
        self.height = CHICKEN_SIZE[self.type][1]
        self.hp = CHICKEN_HP[self.type]

        # Load the chicken images and set its rect attribute.
        self.images = CHICKEN_IMAGES[self.type]
        self.loop = [0]*len(self.images) if self.type == 'baby_chicken' else [0]*len(self.images)
        self.rect = self.images[0].get_rect()


        #set status of image
        self.current_image = random.randrange(1,12,6)
        self.image = self.images[self.current_image-1]

        # Start each new chicken near the top left of the screen.
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.rect.top+=10; self.rect.bottom-=10; self.rect.left+=10; self.rect.right-=10

        # Store the chicken's exact horizontal position.
        self.x = float(self.rect.x)

        self.timer_drop_eggs = 4000
        self.timer_hidden = None


    def check_edges(self):
        """Return True if chicken is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.ai_game.active_boss_dame:
            if self.rect.right >= screen_rect.right or self.rect.left <= 0:
                return True
                
    def update_image(self):
        """ Status of chicken"""
        if self.loop[self.current_image]>0:
            self.loop[self.current_image]-=1
        else:
            self.current_image += 1
            if self.current_image >= len(self.images):
                self.current_image = 0
                self.loop = [0]*len(self.images) if self.type == 'baby_chicken' else [0]*len(self.images)
        self.image = self.images[self.current_image]

    def update(self, dt):
        if self.timer_hidden is not None:
            self.timer_hidden -= dt

            # if self.timer_hidden <= 0:
            #     self.ai_game.active_dame = True

        self.update_image()

        """Move the chicken right or left."""
        if self.ai_game.active_dame:
            if self.ai_game.active_boss_dame:
                self.timer_drop_eggs -= dt

                self.x += (self.settings.chicken_speed *
                            self.settings.fleet_direction)
                self.rect.x = self.x
        else:
            self.rect.y += 5
    

    # def check_move_fleet_chicken_boss(self):
    #     for chicken in self.ai_game.chickens:
    #         if(not issubclass(chicken.__class__, self.ai_game.chickenBoss.__class__)):
    #             if chicken.rect.x < 0 or chicken.rect.x > self.settings.screen_width:
    #                 return True
    #             if(self.rect.x < self.settings.screen_width / 2):
    #                 self.rect.x += 5
    #             else:
    #                 self.rect.x -= 5
    #             self.x = float(self.rect.x)
    #     return False
