from pygame.sprite import Sprite
from settings import Settings
import math
import random
import pygame

class Rock(Sprite):

	images = [
        pygame.image.load('images/boss_stone/rocks/rock1.png'),
        pygame.image.load('images/boss_stone/rocks/rock2.png'),
        pygame.image.load('images/boss_stone/rocks/rock3.png'),
        pygame.image.load('images/boss_stone/rocks/rock4.png'),
        pygame.image.load('images/boss_stone/rocks/rock5.png'),
        pygame.image.load('images/boss_stone/rocks/rock6.png'),
		
		pygame.image.load('images/boss_stone/rocks/rock_brown1.png'),
        pygame.image.load('images/boss_stone/rocks/rock_brown2.png'),
        pygame.image.load('images/boss_stone/rocks/rock_brown3.png'),
        pygame.image.load('images/boss_stone/rocks/rock_brown4.png'),
        pygame.image.load('images/boss_stone/rocks/rock_brown5.png'),
    ]

	def __init__(self, pos_x, pos_y, width):
		super().__init__()
		self.settings = Settings()

		self.width = width
		self.height = -1
		# self.hp = width * self.settings.speedup_scale / 2
		self.hp = 1

		self.images = Rock.images

		self.current_image = random.randint(0, len(self.images) - 1)
		self.image = self.images[self.current_image]
		w_image, h_image = self.image.get_rect().size
		self.height = int((h_image / w_image) * self.width)
		self.image = pygame.transform.scale(self.image, (self.width, self.height))
		self.image_copy = self.image
		self.rect = self.image.get_rect()

		self.angle = 0
		self.direction_y = 1
		self.direction_x = random.choice([1, -1])
		self.touch = 2
		self.touch_bottom = False
		self.velocity = 47
		self.O = 0

		self.rect.x = float(pos_x)
		self.rect.y = float(pos_y)

	
	def update(self):
		if self.touch:
			
			if self.rect.bottom >= self.settings.screen_height:
				self.direction_y = -1
				self.touch -= 1
				self.touch_bottom = True
				self.O = self.rect.bottomleft[0] + 100*self.direction_x
				self.velocity = 97*(-self.direction_x)
			elif self.rect.top <=0:
				self.direction_y *= -1
				self.touch_bottom = False

		if not self.touch_bottom:
			self.rect.x += 4*self.direction_x
			self.rect.y += 1*10*self.direction_y
		else:
			self.rect.x = self.O + self.velocity
			# self.rect.y = self.settings.screen_height-self.height + (-1/100 * self.velocity**2+100)*self.direction_y
			self.rect.y = self.settings.screen_height-self.height + (self.velocity**2+100)*self.direction_y
			self.velocity += 3*self.direction_x

		#Rotate the image
		self.angle += -3*self.direction_x
		self.blitRotateCenter(self.angle)

	def blitRotateCenter(self, angle):
		img_center = self.rect.center
		self.image = pygame.transform.rotate(self.image_copy, angle)
		self.rect = self.image.get_rect(center = img_center)