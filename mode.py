import pygame, random, math
from settings import Settings
from pygame.sprite import Sprite
from os import listdir

# EGG = pygame.transform.scale(pygame.image.load('images/Present/egg.png'),(20,20))
# DROP_EGG = pygame.transform.scale(pygame.image.load('images/Present/drop_egg.png'),(33,15))
# HEART = pygame.transform.scale(pygame.image.load('images/Present/heart1.png'), (20,20))
# ROAST = pygame.transform.scale(pygame.image.load('images/Present/roast.png'), (40, 40))
# DRUMSTICK = pygame.transform.scale(pygame.image.load('images/Present/drumstick.png'), (25,30))
# BIG_BULLET = pygame.transform.scale(pygame.image.load('images/boss_stone/big_bullet.png'),(45,85))
# RED_GIFT = [pygame.transform.scale(pygame.image.load('images/Present/red/'+f),(25,25)) for f in listdir('images/Present/red/')]
# GREEN_GIFT = [pygame.transform.scale(pygame.image.load('images/Present/green/'+f),(25,25)) for f in listdir('images/Present/green/')]
# FLASH_GIFT = [pygame.transform.scale(pygame.image.load('images/Present/flash/'+f),(25,25)) for f in listdir('images/Present/flash/')]
# UPGRADE = [pygame.transform.scale(pygame.image.load('images/Present/upgrade/'+f),(25,31)) for f in listdir('images/Present/upgrade/')]
# LOAD_EXPLOSION = [pygame.image.load('images/Present/1s_explosion/'+f) for f in listdir('images/Present/1s_explosion/')]
# EXPLOSION = [pygame.transform.scale(i, (int(i.get_width()*2.5), int(i.get_height()*2.5))) for i in LOAD_EXPLOSION]
# SMOKE_EXPLOSION = [pygame.image.load('images/Present/smoke_explosion/'+f) for f in listdir('images/Present/smoke_explosion/')]
# FEATHER = [pygame.image.load('images/Present/feather/'+f) for f in listdir('images/Present/feather/')]
# BABY_FEATHER = [pygame.image.load('images/Present/bb_feather/'+f) for f in listdir('images/Present/bb_feather/')]


class Egg(Sprite):
	def __init__(self, pos_x, pos_y, EGG):
		super().__init__()
		self.image = EGG[0]
		self.drop_egg = EGG[1]
		self.rect = self.image.get_rect()

		self.timer = None

		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self, dt):
		if self.timer is None:
			self.rect.y += 6
		else:
			self.image = self.drop_egg
			self.timer -= dt
			if self.timer <= 0:
				self.rect.y += 50


class Heart(Sprite):
	def __init__(self, pos_x, pos_y, HEART):
		super().__init__()

		self.image = HEART
		self.rect = self.image.get_rect()

		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self):
		self.rect.y += 5


class Roast(Sprite):
	def __init__(self, pos_x, pos_y, ROAST):
		super().__init__()
		self.settings = Settings()
		self.image = ROAST
		self.image_copy = self.image
		self.rect = self.image.get_rect()

		self.angle = 0
		self.direction_y = 1
		self.direction_x = random.choice([1, -1])
		self.touch = 1
		self.touch_bottom = False
		self.velocity = 97
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

		if not self.touch_bottom:
			self.rect.x += 4*self.direction_x
			self.rect.y += 1*10*self.direction_y
		else:
			self.rect.x = self.O + self.velocity
			self.rect.y = self.settings.screen_height-self.image.get_height() + (-1/100 * self.velocity**2+100)*self.direction_y
			self.velocity += 3*self.direction_x

		#Rotate the image
		self.angle += -3*self.direction_x
		self.blitRotateCenter(self.angle)

	def blitRotateCenter(self, angle):
		img_center = self.rect.center
		self.image = pygame.transform.rotate(self.image_copy, angle)
		self.rect = self.image.get_rect(center = img_center)

class Drumstick(Sprite):
	def __init__(self, pos_x, pos_y, DRUMSTICK):
		super().__init__()
		self.settings = Settings()

		self.image = DRUMSTICK
		self.image_copy = self.image
		self.rect = self.image.get_rect()

		self.angle = 0
		self.direction_y = 1
		self.direction_x = random.choice([1, -1])
		self.touch = 2
		self.touch_bottom = False
		self.velocity = 96
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
				self.velocity = 96*(-self.direction_x)

		if not self.touch_bottom:
			self.rect.x += 4*self.direction_x
			self.rect.y += 1*10*self.direction_y
		else:
			self.rect.x = self.O + self.velocity
			self.rect.y = self.settings.screen_height-self.image.get_height() + (-1/100 * self.velocity**2+100)*self.direction_y
			self.velocity += 4*self.direction_x

		#Rotate the image
		self.angle += -4*self.direction_x
		self.blitRotateCenter(self.angle)

	def blitRotateCenter(self, angle):
		img_center = self.rect.center
		self.image = pygame.transform.rotate(self.image_copy, angle)
		self.rect = self.image.get_rect(center = img_center)


class Gift(Sprite):
	def __init__(self, pos_x, pos_y, GIFT, type):
		super().__init__()

		self.type = type

		self.images = GIFT
		self.loop = [1]*len(self.images)
		self.rect = self.images[0].get_rect()

		self.rect.x = pos_x
		self.rect.y = pos_y

		self.current_image = 0
		self.image = self.images[self.current_image]

	def update(self):
		# status of image
		if self.loop[self.current_image]>0:
			self.loop[self.current_image]-=1
		else:
			self.current_image += 1
			if self.current_image >= len(self.images):
				self.current_image = 0
		self.image = self.images[self.current_image]

		self.rect.y += 3

class Upgrade(Sprite):
	def __init__(self, pos_x, pos_y, UPGRADE):
		super().__init__()

		self.images = UPGRADE
		self.current_image = 0
		self.image = self.images[self.current_image]
		self.rect = self.image.get_rect()


		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self):
		# status of image
		self.current_image += 1
		if self.current_image >= len(self.images):
			self.current_image = 0
		self.image = self.images[self.current_image]

		self.rect.y += 2

	
class Big_Bullet(Sprite):
	def __init__(self, pos_x, pos_y, BIG_BULLET):
		super().__init__()

		self.image = BIG_BULLET
		self.rect = self.image.get_rect()
		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self):
		self.rect.y += 10

class Explosion(Sprite):
	def __init__(self, pos_x, pos_y, EXPLOSION):
		super().__init__()
		self.images = EXPLOSION
		self.loop = [1]*len(self.images)
		self.current_image = 0
		self.image = self.images[self.current_image]
		self.rect = self.image.get_rect()

		self.rect.x = pos_x - (self.image.get_width()-72)//2
		self.rect.y = pos_y - (self.image.get_height()-60)

	def update(self):
		img_center = self.rect.center

		if self.loop[self.current_image]>0:
			self.loop[self.current_image]-=1
		else:
			self.current_image += 1
			if self.current_image >= len(self.images):
				self.current_image = len(self.images)-1

		self.image = self.images[self.current_image]
		self.rect = self.image.get_rect(center = img_center)

class Smoke_explosion(Sprite):
	def __init__(self, pos_x, pos_y, SMOKE_EXPLOSION):
		super().__init__()
		self.images = SMOKE_EXPLOSION
		self.current_image = 0
		self.image = self.images[self.current_image]
		self.rect = self.image.get_rect()

		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self):
		self.current_image += 1
		if self.current_image >= len(self.images):
			self.current_image = len(self.images)-1
		self.image = self.images[self.current_image]

class Feather(Sprite):
	def __init__(self, pos_x, pos_y, FEATHER):
		super().__init__()
		self.images = FEATHER
		# self.loop = [2]*20+[3]*10
		self.loop = [3]*len(self.images)
		self.current_image = 0
		self.image = self.images[self.current_image]
		self.rect = self.image.get_rect()

		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self):
		if self.loop[self.current_image]==0:
			self.current_image += 1
			if self.current_image == len(self.images):
				self.current_image = 0
		self.loop[self.current_image]-=1

		if self.current_image<10:
			self.rect.x+=1
		else:
			self.rect.x-=1

		self.image = self.images[self.current_image]
		self.rect.y+=4

class Baby_Feather(Sprite):
	def __init__(self, pos_x, pos_y, BABY_FEATHER):
		super().__init__()
		self.images = BABY_FEATHER
		self.loop = [2]*len(self.images)
		self.current_image = 0
		self.image = self.images[self.current_image]
		self.rect = self.image.get_rect()

		self.rect.x = pos_x
		self.rect.y = pos_y

	def update(self):
		if self.loop[self.current_image]==0:
			self.current_image += 1
			if self.current_image == len(self.images):
				self.current_image = 0
		self.loop[self.current_image]-=1

		if self.current_image>=0 and self.current_image<=11:
			self.rect.x+=1
		else:
			self.rect.x-=1

		self.image = self.images[self.current_image]
		self.rect.y+=4