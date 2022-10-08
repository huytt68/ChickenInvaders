import pygame
from pygame.sprite import Sprite
from rocket import Rocket
import chicken_invaders

class Ship(Sprite):

    """ A class to manage the ship. """
    def __init__(self, ai_game):
        """ Initialize the ship and set its starting position. """
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        self.ship_width = 72
        self.ship_height = 60
        self.game_stats = ai_game.stats
    

        #Tạo biến và kiểm tra lựa chọn phi thuyền
        self.ship_image = None
        self.ship_image_right = None
        self.ship_image_left = None
        self.check = chicken_invaders.truong
        self.rocket = Rocket(self.screen, self.check)
        
        #Kiểm tra lựa chọn phi thuyền vào game
        #Chọn ship chính
        if self.check == 2:
            self.ship_image = pygame.image.load("images/ship/ship.png")
            self.ship_image_right = pygame.image.load("images/ship/rship.png")
            self.ship_image_left = pygame.image.load("images/ship/lship.png")
        #Chọn ship bên trái ship chính
        elif self.check == 1:
            self.ship_image = pygame.image.load("images/menu/love.png")
            self.ship_image_right = pygame.image.load("images/menu/love.png")
            self.ship_image_left = pygame.image.load("images/menu/love.png")
        #Chọn ship bên phải ship chính    
        elif self.check == 3:
            self.ship_image = pygame.image.load("images/menu/phi_thuyen.png")
            self.ship_image_right = pygame.image.load("images/menu/phi_thuyen_phai.png")
            self.ship_image_left = pygame.image.load("images/menu/phi_thuyen_trai.png")

        # Scale size of image
        self.ship_image = pygame.transform.scale(self.ship_image,(self.ship_width,self.ship_height))
        self.ship_image_right = pygame.transform.scale(self.ship_image_right,(self.ship_width,self.ship_height))
        self.ship_image_left = pygame.transform.scale(self.ship_image_left,(self.ship_width,self.ship_height))
        
        self.r = 150
        self.inc = True
        self.shield = pygame.transform.scale(pygame.image.load('images/Present/s1.png'), (self.r, self.r))

        self.rect = self.ship_image.get_rect()
        self.rect_shield = self.shield.get_rect(center = self.rect.center)

        # Status of the ship: mid, left, right
        self.status_image = self.ship_image # Default mid position

        # Start each new ship at the bottom center of the screen.
        self.rect.x = self.screen_rect.midbottom[0] - self.ship_width // 2
        self.rect.y = self.screen_rect.midbottom[1] - self.ship_height*2

        # Store a decimal value for the ship's horizontal position.
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # Ship fire bullet
        self.fire = False

        self.respawn_timer = None
        self.spawn = False

        # Movement flag
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """Center the ship on the screen."""
        self.rect.x = self.screen_rect.midbottom[0] - self.ship_width//2
        self.rect.y = self.screen_rect.midbottom[1] - self.ship_height*2
       
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def spawn_ship(self):
        self.rect.y = self.screen_rect.midbottom[1]
       
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def spawn_update(self, dt):
        if self.y > self.screen_rect.bottom - (self.ship_height)*2 and self.spawn:
            self.y -= 5
            # if self.y <= self.screen_rect.bottom - (self.ship_height)*2 or self.moving_right or self.moving_left or self.moving_up or self.moving_down:
            if self.y <= self.screen_rect.bottom - (self.ship_height)*2 and self.spawn:
                self.spawn = False 
        else:
            self.respawn_timer -= dt

            if self.moving_right and self.rect.right < self.screen_rect.right:
                self.status_image = self.ship_image_right
                self.x += self.settings.ship_speed
            if self.moving_left and self.rect.left > 0:
                self.status_image = self.ship_image_left
                self.x -= self.settings.ship_speed
            if self.moving_up and self.y > 0:
                self.y -= self.settings.ship_speed
            if self.moving_down and self.y < self.screen_rect.bottom - (self.ship_height)*2:
                self.y += self.settings.ship_speed
            if self.fire:
                self.y += 8

            # Update rect object from self.x.
            self.rect.x = self.x
            self.rect.y = self.y

            if self.r==150:
                self.inc = True
            elif self.r == 220:
                self.inc = False

            if self.inc:
                self.r+=5
            else:
                self.r-=5
            self.shield = pygame.transform.scale(pygame.image.load('images/Present/s1.png'), (self.r, self.r))
            self.rect_shield = self.shield.get_rect(center = self.rect.center)

        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

        # Update rocket
        self.rocket.update()
        if self.respawn_timer < 0:
            return False
        else:
            return True

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.status_image = self.ship_image_right
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.status_image = self.ship_image_left
            self.x -= self.settings.ship_speed
        if self.moving_up and self.y > 0:
            # if(self.game_stats.level % 5 == 0 and self.y < self.settings.screen_height / 2):
            #     self.y = self.y
            # else:
                self.y -= self.settings.ship_speed
        if self.moving_down and self.y < self.screen_rect.bottom - (self.ship_height)*2:
            self.y += self.settings.ship_speed
        if self.fire:
            self.y += 8

        # Update rect object from self.x.
        self.rect.x = self.x
        self.rect.y = self.y

        # Update rocket
        self.rocket.update()
        # self.rocket.draw(self)
 
    def blitme(self):
        """ Draw the ship at its current location. """
        self.rocket.draw(self)
        self.screen.blit(self.status_image, self.rect)
        # self.rocket.draw(self)
        if self.respawn_timer is not None and self.respawn_timer >= 0 and self.respawn_timer != 3000:
            self.screen.blit(self.shield, (self.rect_shield.x, self.rect_shield.y))
        self.status_image = self.ship_image