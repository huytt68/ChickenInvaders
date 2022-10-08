import pygame
from pygame.sprite import Sprite
from settings import Settings
from math import ceil, atan, pi


red = {1:[0], 2:[0.75], 3:[0.25, 0], 4:[0.25, 0.75], 5:[0.35, 0.2, 0], 6:[0.4, 0.2, 0.75]}
green = None
flash = {1:[0], 2:[0.15], 3:[0.4, 0], 4:[0.5, 0.15], 5:[0.85, 0.5, 0], 6:[0.85, 0.5, 0.15]}

TYPE_BULLET = {"red" : red, "green" : green, "flash" : flash}
SIZE_BULLET = {"red": (16,53), "green": (12,65), "flash":(8,64)}
DAME_BULLET = {"red" : 30, "green": 50, "flash": 20}
SPEED_BULLET = {"red" : 20, "green" : 20, "flash" : 40}


class Bullet():
    def __init__(self, ci_game, type):
        self.type = type
        self.width = SIZE_BULLET[self.type][0]
        self.height = SIZE_BULLET[self.type][1]
        self.dame = DAME_BULLET[self.type]
        

        self.url = "images/Bullets/"+str(self.type)+".png"
        self.image = pygame.image.load(self.url)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect()

        self.rect.x = ci_game.ship.x + (ci_game.ship.ship_width-self.width)//2
        self.rect.y = ci_game.ship.y + ci_game.ship.ship_height//2 - self.height//2

class Bullets(Sprite):
    def __init__(self, ci_game):
        super().__init__()
        self.screen = ci_game.screen
        self.type = ci_game.style_bullet
        self.level = ci_game.bullet_level
        
        self.speed = SPEED_BULLET[self.type]
        self.sprites = []

        """set up position of bullet"""
        if self.type == "red":
            for i in range(self.level):
                self.sprites.append(Bullet(ci_game, self.type))

            if self.level%2==0:
                self.sprites[self.level//2-1].rect.x -= self.speed * TYPE_BULLET[self.type][self.level][-1]
                self.sprites[self.level//2].rect.x += self.speed * TYPE_BULLET[self.type][self.level][-1]
            index = 0
            for i in range(ceil(self.level/2)-1):
                self.blitRotateCenter(atan(TYPE_BULLET[self.type][self.level][index])/pi*180, i)
                self.blitRotateCenter(-atan(TYPE_BULLET[self.type][self.level][index])/pi*180, self.level-i-1)
                self.sprites[i].rect.y += (ceil(self.level/2)-index-1)*10
                self.sprites[self.level-i-1].rect.y += (ceil(self.level/2)-index-1)*10
                index+=1

        elif self.type == "green":
            if self.level<3:
                self.sprites.append(Bullet(ci_game, self.type))
                if self.level == 2:
                    self.fix_size_green_bullet(ci_game, 0)
            else:
                for i in range(3):
                    self.sprites.append(Bullet(ci_game, self.type))

                if self.level == 4:
                    self.fix_size_green_bullet(ci_game, 1)

                    self.sprites[0].rect.x -= int(self.speed * 1.4)
                    self.sprites[2].rect.x += int(self.speed * 1.4)
                    self.sprites[1].rect.y -= self.sprites[1].image.get_height()//2
                elif self.level == 5:
                    self.fix_size_green_bullet(ci_game, 0)
                    self.fix_size_green_bullet(ci_game, 2)

                    self.sprites[0].rect.x -= int(self.speed * 1.65)
                    self.sprites[2].rect.x += int(self.speed * 1.65)
                    self.sprites[1].rect.y -= self.sprites[1].image.get_height()//2
                elif self.level == 6:
                    self.fix_size_green_bullet(ci_game, 0)
                    self.fix_size_green_bullet(ci_game, 1)
                    self.fix_size_green_bullet(ci_game, 2)

                    self.sprites[0].rect.x -= int(self.speed * 1.65)
                    self.sprites[2].rect.x += int(self.speed * 1.65)
                    self.sprites[1].rect.y -= self.sprites[1].image.get_height()//2
                else:
                    self.sprites[0].rect.x -= int(self.speed * 1.1)
                    self.sprites[2].rect.x += int(self.speed * 1.1)
                    self.sprites[1].rect.y -= self.sprites[1].image.get_height()//2
        elif self.type == "flash":
            for i in range(self.level):
                self.sprites.append(Bullet(ci_game, self.type))

            if self.level%2==0:
                self.sprites[self.level//2-1].rect.x -= self.speed * TYPE_BULLET[self.type][self.level][-1]
                self.sprites[self.level//2].rect.x += self.speed * TYPE_BULLET[self.type][self.level][-1]

            index = 0
            for i in range(ceil(self.level/2)-1):
                self.sprites[i].rect.x -= int(self.speed * TYPE_BULLET[self.type][self.level][index])
                self.sprites[self.level-i-1].rect.x += int(self.speed * TYPE_BULLET[self.type][self.level][index])
                index+=1


    def fix_size_green_bullet(self, ci_game, index):
        url = self.sprites[0].url.split('.')[0]+'_strong.png'
        self.sprites[index].image = pygame.image.load(url)
        self.sprites[index].image = pygame.transform.scale(self.sprites[index].image, (self.sprites[index].image.get_width()//3, self.sprites[index].image.get_height()//3))
        self.sprites[index].dame = 60

        #set position
        self.sprites[index].rect.x = ci_game.ship.x + (ci_game.ship.ship_width-self.sprites[index].image.get_width())//2
        self.sprites[index].rect.y = ci_game.ship.y


    def blitRotateCenter(self, angle, index):
        img_center = self.sprites[index].rect.center
        self.sprites[index].image = pygame.transform.rotate(self.sprites[index].image, angle)
        self.sprites[index].rect = self.sprites[index].image.get_rect(center = img_center)

    
    def update(self):
        if self.type == "red":
            index = 0
            for i in range(ceil(self.level/2)-1):
                self.sprites[i].rect.x -= int(self.speed * TYPE_BULLET[self.type][self.level][index])
                self.sprites[self.level-i-1].rect.x += int(self.speed * TYPE_BULLET[self.type][self.level][index])
                index+=1
            for i in range(self.level):
                self.sprites[i].rect.y -= self.speed
        elif self.type == "green" or self.type == "flash":
            for i in range(len(self.sprites)):
                self.sprites[i].rect.y -= self.speed
  
    def draw_bullet(self):
        for bullet in self.sprites:
            self.screen.blit(bullet.image, [bullet.rect.x, bullet.rect.y])