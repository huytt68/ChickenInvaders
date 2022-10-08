import pygame
import random

from pygame.sprite import Sprite
from chicken import Chicken


class Chicken_Boss(Chicken):

    images = [

        pygame.image.load('images/boss_stone/boss_temp/boss1-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss2-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss3-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss4-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss5-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss6-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss7-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss8-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss9-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss_temp/boss10-removebg-preview.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss10.png'),
        pygame.image.load('images/boss_stone/boss_temp/boss11-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/2-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/3-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/4-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/5-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/6-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/7-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/8-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/9-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/10-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/11-removebg-preview.png'),
        # pygame.image.load('images/boss_stone/boss/12-removebg-preview.png')

        
    ]

    def __init__(self, ai_game):
        super().__init__(ai_game)

        self.hp = 774 * self.settings.score_scale
        self.images = Chicken_Boss.images
        self.image = self.images[0]
        width, height = self.image.get_rect().size
        ratio = width / height
        self.height = 174
        self.width = round(ratio * self.height)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

        # Start each new chicken near the top center of the screen.
        self.rect.x = self.settings.screen_width / 2 - self.width / 2
        # self.rect.y = 10
        # self.rect.center = self.screen.get_rect().center
        self.rect.y = 10 - self.screen.get_height()

        # bullet following
        self.num_bullets = 5
        self.timer_bullets = 10

        # fleet chicken is active, isn't it?
        self.fleet_active = False

        self.x = self.rect.x

        # HP
        self.widthHP = 220
        self.heightHP = 30
        self.distanceHP = 27
        self.borderRadius = 22
        self.borderWidth = 4
        self.ratio =  self.widthHP / self.hp
        self.bgColorHP =    (212, 0, 0)
        self.borderColorHP = (2, 85, 142)

    def check_edges(self):
        """Return True if chicken is at edge of screen."""
        screen_rect = self.screen.get_rect()
        if self.ai_game.active_boss_dame:
            if self.rect.right >= screen_rect.right - 220 or self.rect.left <= 0 + 220:
                return True

    def update_image(self):
        """ Status of chicken"""
        self.current_image += 1
        if self.current_image % 2 == 0:
            if self.current_image >= 2 * len(self.images):
                self.current_image = 0
            self.image = self.images[int(self.current_image / 2)]

    def draw_hp(self):
        wHP = self.hp * self.ratio
        rectBorderHP =  pygame.Rect(self.rect.center[0] - int(self.widthHP / 2), self.rect.bottom + self.distanceHP, self.widthHP, self.heightHP)
        rectBgHP =  pygame.Rect(self.rect.center[0] - int(self.widthHP / 2) +  self.borderWidth, 
                            self.rect.bottom + self.distanceHP +  self.borderWidth, wHP - self.borderWidth * 2, self.heightHP -  self.borderWidth * 2)
        # print(wHP, self.hp)
        if(wHP > 8):
            if self.widthHP - wHP < self.borderRadius:
                pygame.draw.rect(self.screen, self.bgColorHP, rectBgHP, border_top_right_radius=self.borderRadius, border_bottom_right_radius=self.borderRadius, 
                                                                        border_top_left_radius=self.borderRadius, border_bottom_left_radius=self.borderRadius)
            else:
                pygame.draw.rect(self.screen,  self.bgColorHP, rectBgHP, border_top_left_radius=self.borderRadius, border_bottom_left_radius=self.borderRadius)

        pygame.draw.rect(self.screen,  self.borderColorHP, rectBorderHP, self.borderWidth, self.borderRadius)

        hp_number_str = str(round(wHP / self.widthHP * 100)) + '%'
        x = rectBorderHP.center[0] - 10
        y = rectBorderHP.center[1] - 6
        # hp_number_rect.x -= 
        hp_number_image =  pygame.font.SysFont(None, 21).render(hp_number_str, True, (255, 255, 255))
        self.screen.blit(hp_number_image, (x, y))


class Bullet_Follow(Sprite):
    """ Create a single bullet following"""

    def __init__(self, ci_game, boss):
        super().__init__()
        self.ci_game = ci_game
        self.screen = ci_game.screen
        self.settings = ci_game.settings
        self.boss = boss


        # Set default width and height for bullet following
        self.width = 47
        self.height = 47

        # Set default speed for bullet following
        self.speed = 3

        # Set direction for bullet following
        self.direction = None

        self.images = []
        self.images.append(pygame.image.load('images/boss_stone/fire_ball_1.png'))
        self.images.append(pygame.image.load('images/boss_stone/fire_ball_2.png'))
        self.images.append(pygame.image.load('images/boss_stone/fire_ball_3.png'))
        self.images.append(pygame.image.load('images/boss_stone/fire_ball_4.png'))
        self.images = [pygame.transform.scale(self.images[i], (self.width, self.height)) for i in range(4)]

        # Load image for bullet following
        self.current_image = random.randint(0, 3)
        self.image = self.images[self.current_image]

        self.rect = self.image.get_rect()

        self.rect.x = self.boss.rect.x + self.boss.rect.width / 2 - 10
        self.rect.y = self.boss.rect.y + self.boss.rect.height

        # Store the chicken's exact horizontal verhical position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        self.current_image += 1
        if(self.current_image >= len(self.images)) :
            self.current_image = 0
        self.image = self.images[self.current_image]
        y = self.speed
        self.x += y * self.direction 
        self.y += y
        self.rect.x = self.x
        self.rect.y = self.y
        
