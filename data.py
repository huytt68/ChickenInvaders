import pygame, random, math
from settings import Settings
from pygame.sprite import Sprite
from os import listdir

class Image():
	EGG = [pygame.transform.scale(pygame.image.load('images/Present/egg.png'),(20,20)),
			pygame.transform.scale(pygame.image.load('images/Present/drop_egg.png'),(33,15))]
	HEART = pygame.transform.scale(pygame.image.load('images/Present/heart1.png'), (20,20))
	ROAST = pygame.transform.scale(pygame.image.load('images/Present/roast.png'), (40, 40))
	DRUMSTICK = pygame.transform.scale(pygame.image.load('images/Present/drumstick.png'), (25,30))
	BIG_BULLET = pygame.transform.scale(pygame.image.load('images/boss_stone/big_bullet.png'),(45,85))
	RED_GIFT = [pygame.transform.scale(pygame.image.load('images/Present/red/'+f),(25,25)) for f in listdir('images/Present/red/')]
	GREEN_GIFT = [pygame.transform.scale(pygame.image.load('images/Present/green/'+f),(25,25)) for f in listdir('images/Present/green/')]
	FLASH_GIFT = [pygame.transform.scale(pygame.image.load('images/Present/flash/'+f),(25,25)) for f in listdir('images/Present/flash/')]
	UPGRADE = [pygame.transform.scale(pygame.image.load('images/Present/upgrade/'+f),(25,31)) for f in listdir('images/Present/upgrade/')]
	LOAD_EXPLOSION = [pygame.image.load('images/Present/1s_explosion/'+f) for f in listdir('images/Present/1s_explosion/')]
	EXPLOSION = [pygame.transform.scale(i, (int(i.get_width()*2), int(i.get_height()*2))) for i in LOAD_EXPLOSION]
	SMOKE_EXPLOSION = [pygame.image.load('images/Present/smoke_explosion/'+f) for f in listdir('images/Present/smoke_explosion/')]
	FEATHER = [pygame.image.load('images/Present/feather/'+f) for f in listdir('images/Present/feather/')]
	BABY_FEATHER = [pygame.image.load('images/Present/bb_feather/'+f) for f in listdir('images/Present/bb_feather/')]

# class Sound():
# 	FLASH = pygame.mixer.Sound('sound/flash.ogg')
# 	RED = pygame.mixer.Sound('sound/laser.wav')
# 	GREEN = pygame.mixer.Sound('sound/shoot1.wav')
# 	EXPLOSION = pygame.mixer.Sound('sound/explosion5.mp3')
# 	EAT = pygame.mixer.Sound('sound/eat.ogg')
# 	CHICK = pygame.mixer.Sound('sound/chick.wav')
# 	POWERUP = pygame.mixer.Sound('sound/powerup.mp3')
# 	CLICK = pygame.mixer.Sound('sound/click.wav')
# 	CLUCK = pygame.mixer.Sound('sound/cluck.wav')
# 	SELECTOR = pygame.mixer.Sound('sound/selector.wav')
# 	MUSIC = pygame.mixer.Sound('sound/Chicken Invaders 4 (Ultimate Omelette) OST - Chapter 3_ Chapter 11 (HQ).ogg')
# 	BOSS_MUSIC = pygame.mixer.Sound('sound/Chicken Invaders 4 (Ultimate Omelette) OST - Boss Theme (HQ).ogg')
# 	TITLE_MUSIC = pygame.mixer.Sound('sound/Chicken Invaders 4 (Ultimate Omelette) OST - Title Theme (HQ).ogg')

# 	RED.set_volume(0.4)
# 	GREEN.set_volume(0.3)
# 	EAT.set_volume(0.2)
# 	MUSIC.set_volume(0.4)
# 	BOSS_MUSIC.set_volume(0.5)
# 	TITLE_MUSIC.set_volume(0.5)

class Data():
	def __init__(self):
		self.image = Image()
		# self.sound = Sound()