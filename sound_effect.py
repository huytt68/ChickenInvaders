import pygame

pygame.mixer.init()

FLASH = pygame.mixer.Sound('sound/flash.ogg')
RED = pygame.mixer.Sound('sound/laser.wav')
GREEN = pygame.mixer.Sound('sound/shoot1.wav')
EXPLOSION = pygame.mixer.Sound('sound/explosion5.mp3')
EAT = pygame.mixer.Sound('sound/eat.ogg')
CHICK = pygame.mixer.Sound('sound/chick.wav')
POWERUP = pygame.mixer.Sound('sound/powerup.mp3')
CLICK = pygame.mixer.Sound('sound/click.wav')
CLUCK = pygame.mixer.Sound('sound/cluck.wav')
SELECTOR = pygame.mixer.Sound('sound/selector.wav')
MUSIC = pygame.mixer.Sound('sound/Chicken Invaders 4 (Ultimate Omelette) OST - Chapter 3_ Chapter 11 (HQ).ogg')
BOSS_MUSIC = pygame.mixer.Sound('sound/Chicken Invaders 4 (Ultimate Omelette) OST - Boss Theme (HQ).ogg')
TITLE_MUSIC = pygame.mixer.Sound('sound/Chicken Invaders 4 (Ultimate Omelette) OST - Title Theme (HQ).ogg')

music_volume = 0.5
sfx_volume = 1.0
red_volume = 0.8
green_volume = 0.6
eat_volume = 0.4

RED.set_volume(red_volume)
GREEN.set_volume(green_volume)
EAT.set_volume(eat_volume)
MUSIC.set_volume(music_volume)
BOSS_MUSIC.set_volume(music_volume)
TITLE_MUSIC.set_volume(music_volume)

class SFx:
    def __init__(self):
        self.ms_lv=5
        self.sfx_lv=10
        self.music_vol = music_volume
        self.sfx_vol = sfx_volume
        self.red_vol = red_volume
        self.green_vol = green_volume
        self.eat_vol = eat_volume
        self.ms = {'flash':FLASH,
            'red':RED,
            'green':GREEN,
            'explosion':EXPLOSION,
            'eat':EAT,
            'chick':CHICK,
            'cluck':CLUCK,
            'powerup':POWERUP,
            'click':CLICK,
            'selector':SELECTOR,
            'music':MUSIC,
            'boss_music':BOSS_MUSIC,
            'title_music':TITLE_MUSIC}

    def getSFx(self,s):
        return self.ms[s]
    
    def music_down(self):
        if self.ms_lv > 0:
            self.ms_lv -= 1
            self.music_vol -=0.1

            MUSIC.set_volume(self.music_vol)
            BOSS_MUSIC.set_volume(self.music_vol)
            TITLE_MUSIC.set_volume(self.music_vol)

    def music_up(self):
        if self.ms_lv <10:
            self.ms_lv += 1
            self.music_vol +=0.1

            MUSIC.set_volume(self.music_vol)
            BOSS_MUSIC.set_volume(self.music_vol)
            TITLE_MUSIC.set_volume(self.music_vol)

    def sfx_down(self):
        if self.sfx_lv > 0:
            self.sfx_lv -= 1
            self.sfx_vol -= 0.1
            self.red_vol -= 0.08
            self.green_vol -= 0.06
            self.eat_vol -= 0.04

            FLASH.set_volume(self.sfx_vol)
            RED.set_volume(self.red_vol)
            GREEN.set_volume(self.green_vol)
            EXPLOSION.set_volume(self.sfx_vol)
            EAT.set_volume(self.eat_vol)
            CHICK.set_volume(self.sfx_vol)
            POWERUP.set_volume(self.sfx_vol)
            CLICK.set_volume(self.sfx_vol)
            CLUCK.set_volume(self.sfx_vol)
            SELECTOR.set_volume(self.sfx_vol)

    def sfx_up(self):
        if self.sfx_lv < 10:
            self.sfx_lv += 1
            self.sfx_vol += 0.1
            self.red_vol += 0.08
            self.green_vol += 0.06
            self.eat_vol += 0.04

            FLASH.set_volume(self.sfx_vol)
            RED.set_volume(self.red_vol)
            GREEN.set_volume(self.green_vol)
            EXPLOSION.set_volume(self.sfx_vol)
            EAT.set_volume(self.eat_vol)
            CHICK.set_volume(self.sfx_vol)
            POWERUP.set_volume(self.sfx_vol)
            CLICK.set_volume(self.sfx_vol)
            CLUCK.set_volume(self.sfx_vol)
            SELECTOR.set_volume(self.sfx_vol)