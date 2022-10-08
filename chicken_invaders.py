import sys
import time
import pygame
import random
import json
from pygame.locals import *
from operator import itemgetter
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from ship import Ship
from bullet import Bullets
from chicken import Chicken
from rock import Rock
from chicken_boss import Chicken_Boss, Bullet_Follow
from mode import *
from sound_effect import SFx
from data import Data
clock = pygame.time.Clock()

#Tạo biến để bắt các lựa chọn ship trong start
truong = 0

class ChickenInvaders:
    """ Overall class to manage game assets and behavior. """
    #Tạo biến để kiểm tra qua màn mới
    quaMan = False
    time_start = 0

    def __init__(self):
        """ Initialize the game, and create game resources. """
        pygame.init()
        self.settings = Settings()

        # The position start plotting background
        self.pos_background = 0

        # Set name for player
        self.name_player =  self.settings.name_player
        self.player_id = -1

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        # self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Chicken Invaders")
        pygame.display.set_icon(pygame.image.load("images/icon.png"))

        self.BG_COLOR = pygame.Color('gray12')
        self.BLUE = pygame.Color('dodgerblue')
        self.mainClock = pygame.time.Clock()

        self.font = pygame.font.SysFont(None, 32)
        self.font_title = pygame.font.Font(None, 40)
        self.font_input = pygame.font.Font(None, 32)
        self.font_noti = pygame.font.Font('snap itc.ttf', 30)

        self.music_on = True

        # Create an instance to store game statistics,
        # and create a scoreboard.
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        # self.ship = Ship(self)
        # self.shield = False
        # self.bullets = pygame.sprite.Group()
        # self.style_bullet = "flash"
        # self.bullet_level = 1
        # self.chickens = pygame.sprite.Group()
        # self.modes = pygame.sprite.Group()
        # self.effect = pygame.sprite.Group()
        # self.rocks = pygame.sprite.Group()
        # self.rocks_size = 7
        # self.rocks_times = 7 * self.stats.level
        # self.rock_active = False

        # self.bullet_follows = pygame.sprite.Group()
        # self.chickenBoss = None
        # self.createAnemy()
        # self.active_dame = False 
        # self.timer = None

        # self.active_boss_dame = False
        # self.img_mouse = pygame.transform.scale(pygame.image.load('images/mouse.png'),(46,49))
        # self.mouse_rect = self.img_mouse.get_rect()

        # self.sfx = SFx()
        # self.music = pygame.mixer.Channel(0)
        # self.boss_music = pygame.mixer.Channel(1)

    def save(self, highscores):
        with open('highscores.txt', 'w') as file:
            json.dump(highscores, file)  # Write the list to the json file.

    def load(self):
        try:
            with open('highscores.txt', 'r') as score_file:
                highscores = json.load(score_file)  # Read the json file.
        except FileNotFoundError:
            return []  # Return an empty list if the file doesn't exist.
        # Sorted by the score.
        return highscores

    def run_game(self, chon_phi_thuyen, data):
        """ Start the main loop for the game. """
        #Thay đổi lại lựa chọn của biến chọn ship
        global truong
        truong = chon_phi_thuyen
        self.data = data

        self.ship = Ship(self)
        self.shield = False
        self.bullets = pygame.sprite.Group()
        self.style_bullet = "flash"
        self.bullet_level = 1
        self.chickens = pygame.sprite.Group()
        self.modes = pygame.sprite.Group()
        self.effect = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.rocks_size = 7
        self.rocks_times = 5 * self.rocks_size
        self.rock_appear_time = 1000
        self.rock_active = False

        self.bullet_follows = pygame.sprite.Group()
        self.chickenBoss = None
        self.createAnemy()
        self.active_dame = False 
        self.timer = None

        self.active_boss_dame = False
        self.img_mouse = pygame.transform.scale(pygame.image.load('images/mouse.png'),(46,49))
        self.mouse_rect = self.img_mouse.get_rect()

        self.sfx = SFx()
        self.music = pygame.mixer.Channel(0)
        self.boss_music = pygame.mixer.Channel(1)
        self.music.play(self.sfx.getSFx('music'), loops=-1)

        while True:
            # Setting speed game
            self.timer = clock.tick(self.settings.game_speed)

            self.plot_background()
            self._check_events()
            self.sb.prep_score()
            if self.stats.game_active:
                # Hiện thông báo qua màn 
                if self.quaMan == True:
                    self.level_up = pygame.image.load('images/menu/level_up.png')
                    self.screen.blit(self.level_up, (330,40))
                    time_end = time.time()
                    if time_end - self.time_start >= 1.5:
                        self.quaMan = False
                        self.time_start = 0

                self.show_pause_button()
                self.active_damage()
                if self.ship.respawn_timer is None:
                    self.ship.update()
                else:
                    self.shield = self.ship.spawn_update(self.timer)
                self._update_bullets()
                self._update_chickens()
                self.update_effect()

                self.update_bullet_follower()
                self.update_Rocks()
                self.chikenBossAttack()
                
            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            self._update_screen()
    
    def plot_background(self):
        self.screen.fill((0,0,0))
        self.screen.blit(self.settings.screen_bg, (0,self.pos_background))
        self.screen.blit(self.settings.screen_bg, (0,self.pos_background-self.settings.screen_height))

        if (self.pos_background == self.settings.screen_height):
            self.screen.blit(self.settings.screen_bg, (0,self.pos_background-self.settings.screen_height))
            self.pos_background = 0
        self.pos_background += 5

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_click_button(mouse_pos)
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
    
    def show_pause_button(self):
        #pause button
        self.pause_button = pygame.Rect(self.settings.screen_width-75, 25, 50, 47)
        pygame.draw.rect(self.screen, (255, 0, 0), self.pause_button, -1)
        pause_img = pygame.image.load('images/menu/pause.png')
        self.screen.blit(pause_img, (self.settings.screen_width-80, 20))

    def replay(self):
        # Reset the game settings.
            self.settings.initialize_dynamic_settings()

            # Reset the game statistics.
            self.stats.reset_stats()
            self.stats.game_active = True  
            self.sb.prep_roast()
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ship_heart()

            # Get rid of any remaining chickens and bullets.
            self.chickens.empty()
            self.bullets.empty()

            self.rocks.empty()
            self.chickenBoss = None
            self.bullet_follows.empty()

            # Create a new Anemy and center the ship.
            self.createAnemy()
            self.ship.center_ship()

             # Hide the mouse cursor.
            # pygame.mouse.set_visible(False)
            self.music.stop()
            self.boss_music.stop()
            self.music.play(self.sfx.getSFx('music'), loops=-1)

            self.active_dame = False
            self.active_boss_dame = False
            self.shield = True
            if self.chickenBoss:
                self.chickenBoss.fleet_active = False

    def _check_click_button(self, mouse_pos):
        # Pause button to pause game
        pause_click = self.pause_button.collidepoint(mouse_pos)
        if pause_click and self.stats.game_active:
            pygame.mixer.Sound.play(self.sfx.getSFx('click'))
            self.paused()

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            if self.rock_active == False:
                self.ship.fire = True
                self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            if self.stats.game_active:
                self.paused()

    def _check_keyup_events(self, event):
        """Respond to key releases."""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False
        elif event.key == pygame.K_SPACE:
            if self.rock_active == False:
                self.ship.fire = False
                self.ship.y -= 8

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if self.stats.game_active and self.ship.fire:
            new_bullet = Bullets(self)
            pygame.mixer.Sound.play(self.sfx.getSFx(new_bullet.type))

            self.bullets.add(new_bullet)
            if self.ship.respawn_timer is None:
                self.ship.update()
            else:
                self.shield = self.ship.spawn_update(self.timer)
            self.ship.fire = False

    def createAnemy(self):
        self.rock_active = False
        self.rocks_times = -1
        if(self.stats.level % 5 == 0):  
            self.createChickenBoss()
        elif(self.stats.level % 5 == 3):
            self.rocks_times = 5 * self.rocks_size
            self.rock_active = True
            self.createRockRain(147)
        else:
            self.active_boss_dame = True
            self._create_fleet()
        # self.createChickenBoss()
        # # self.createRockRain(174)
        # # self.rock_active = True

    def createChickenBoss(self):
        self.chickenBoss = Chicken_Boss(self)
        self.chickenBoss.timer_hidden = 2000
        self.chickens.add(self.chickenBoss)
        self.music.stop()
        if self.music_on == True:
            self.boss_music.play(self.sfx.getSFx('boss_music'), loops=-1)
       
    def chikenBossAttack(self):
        if(self.chickenBoss and self.active_dame): 
            if (self.chickenBoss.timer_bullets <= 0 ):
                if self.ship.rect.y < self.settings.screen_height / 2: 
                    return
                if(len(self.bullet_follows) < self.chickenBoss.num_bullets):
                    x = (self.chickenBoss.rect.center[0] - self.ship.rect.center[0])
                    y =  (self.chickenBoss.rect.center[1] - self.ship.rect.center[1])
                    # direction = x / y
                    bullet_follow = Bullet_Follow(self, self.chickenBoss)
                    bullet_follow.direction = x / y
                    self.bullet_follows.add(bullet_follow)
            
            if self.chickenBoss.timer_bullets > 0:
                self.chickenBoss.timer_bullets -= 1
            else:
                self.chickenBoss.timer_bullets = 10
            if self.chickenBoss.fleet_active == False:
                self.active_boss_dame = False
                # self.chickenBoss.fleet_active = False
                self.create_fleet_chicken_for_boss()

        
    def createRockRain(self, max_width):
        if self.quaMan == False:
            if(self.rocks_times >= 0):
                if len(self.rocks) < self.rocks_size:
                    width = random.randint(22, max_width)
                    pos_x = width + 10 + random.randint(0, self.settings.screen_width - 10 - width) 
                    pos_y = 1
                    self.createRock(pos_x, pos_y, width) 
                    self.rocks_times -= 1


    def createRock(self, pos_x, pos_y, width):
        self.rocks.add(Rock(pos_x, pos_y, width))

    def create_fleet_chicken_for_boss(self):
        for row_number in range(3):
            for chicken_number in range(6):
                self.create_chicken_for_boss(chicken_number, row_number, 6)
        self.chickenBoss.fleet_active = True

    def create_chicken_for_boss(self, chicken_number, row_number, number_chickens_x):
        """Create an chicken and place it in the row."""
        chicken = Chicken(self,"baby_chicken")
        if chicken_number < number_chickens_x / 2:
            chicken.rect.x = Chicken.width_default + 2 * Chicken.width_default * chicken_number - self.settings.screen_width / 2
        else:
            chicken.rect.x =  self.settings.screen_width / 2 + self.settings.screen_width - 2 * Chicken.width_default - 2 * Chicken.width_default * (number_chickens_x - chicken_number - 1)
        chicken.rect.y = self.chickenBoss.rect.y + chicken.rect.height + 2 * chicken.rect.height * row_number
        chicken.timer_hidden = -1
        self.chickens.add(chicken)

    def check_move_fleet_chicken_boss(self):
        if(self.active_boss_dame == False):
            flag = 1
            for chicken in self.chickens:
                if(not issubclass(chicken.__class__, Chicken_Boss)):
                    if chicken.rect.x <= Chicken.width_default or chicken.rect.x >= self.settings.screen_width - 2 * Chicken.width_default:
                        flag = -1
                    if(chicken.rect.x < self.settings.screen_width / 2):
                        chicken.rect.x += 5
                    else:
                        chicken.rect.x -= 5
                    chicken.x = float(chicken.rect.x)
            if(flag == 1 and len(self.chickens) > 1):
                self.active_boss_dame = True
    

    def _create_fleet(self):
        """Create the fleet of chickens."""
        # Create an chicken and find the number of chickens in a row.
        # Spacing between each chicken is equal to one chicken width.
        chicken_width, chicken_height = (50,50)
        available_space_x = self.settings.screen_width - (2 * chicken_width)
        number_chickens_x = available_space_x // (2 * chicken_width)

        # Determine the number of rows of chickens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                (3 * chicken_height) - ship_height)
        # number_rows = available_space_y // (2 * chicken_height)
        number_rows = 3
        
        # Create the full fleet of chickens.
        for row_number in range(number_rows):
            for chicken_number in range(number_chickens_x):
                if chicken_number%2:
                    typeof = 'baby_chicken'
                else:
                    typeof = 'pilot_chicken'
                self._create_chicken(chicken_number, row_number, typeof)

    def _create_chicken(self, chicken_number, row_number, typeof):
        """Create an chicken and place it in the row."""
        chicken = Chicken(self, typeof)
        chicken_width, chicken_height = (50,50)
        chicken.x = chicken_width + 2 * chicken_width * chicken_number
        if typeof == 'baby_chicken':
            chicken.x += 10
        chicken.rect.x = chicken.x
        chicken.rect.y = chicken_height + 2 * chicken_height * row_number - self.screen.get_height()
        chicken.timer_hidden = 2000
        self.chickens.add(chicken)

    def _check_fleet_edges(self):
        """Respond appropriately if any chickens have reached an edge."""
        if self.active_dame and self.active_boss_dame:
            for chicken in self.chickens.sprites():
                if chicken.check_edges():
                    self._change_fleet_direction()
                    break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        if self.active_dame and self.active_boss_dame:
            for chicken in self.chickens.sprites():
                chicken.rect.y += self.settings.fleet_drop_speed
            self.settings.fleet_direction *= -1

    def active_damage(self):
        time_is_up_to = sum(1 for chicken in self.chickens.sprites() if chicken.timer_hidden<=0)
        if time_is_up_to == len(self.chickens):
            # count = sum(1 for chicken in self.chickens.sprites() if chicken.rect.y >= chicken.height)
            count = sum(1 for chicken in self.chickens.sprites() if chicken.rect.y >= Chicken.height_default)
            self.active_dame = (count == len(self.chickens))
   
    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()
        # Get rid of bullets that have disappeared.
        for bullet in self.bullets.copy():
            count = sum(1 for i in bullet.sprites if i.rect.bottom <= 0)
            if count == len(bullet.sprites):
                self.bullets.remove(bullet)

        self._check_bullet_chicken_collisions()
  
    def _check_bullet_chicken_collisions(self):
        """Respond to bullet-chicken collisions."""
        # Remove any bullets and chickens that have collided.
        for bullet in self.bullets.copy():
            for one_bullet in bullet.sprites:
                collisions = pygame.sprite.spritecollideany(one_bullet, self.chickens)
                # if type(collisions) is Chicken_Boss and self.chickenBoss:
                #     self.drop_mode(self.chickenBoss.rect.center[0], self.chickenBoss.rect.center[1])               

                if collisions and self.active_dame:
                    collisions.hp -= one_bullet.dame
                    
                    if collisions.hp<=0:
                        pos_x = collisions.rect.x
                        pos_y = collisions.rect.y
                        typeOf = collisions.type
                        collisions.kill()
                        self.drop_mode(pos_x, pos_y)
                        if typeOf == "baby_chicken":
                            self.effect.add(Baby_Feather(pos_x, pos_y, self.data.image.BABY_FEATHER))
                            pygame.mixer.Sound.play(self.sfx.getSFx('chick'))
                        else:
                            self.effect.add(Feather(pos_x, pos_y, self.data.image.FEATHER))
                            pygame.mixer.Sound.play(self.sfx.getSFx('cluck'))
                        self.effect.add(Smoke_explosion(pos_x, pos_y, self.data.image.SMOKE_EXPLOSION))

                        self.stats.score += self.settings.chicken_points
                        self.sb.prep_score()
                        self.sb.check_high_score()

                        if type(collisions) is Chicken_Boss:
                            self.drop_mode(self.chickenBoss.rect.center[0], self.chickenBoss.rect.center[1])
                            self.drop_mode(self.chickenBoss.rect.center[0], self.chickenBoss.rect.center[1])
                            self.drop_mode(self.chickenBoss.rect.center[0], self.chickenBoss.rect.center[1])
                            self.chickenBoss = None
                            # self.chickens = None
                            # for chicken in self.chickens:
                            #     randomDrop = random.randint(0, 1)
                            #     if randomDrop == 1:
                            #         self.drop_mode(chicken.rect.center[0], chicken.rect.center[1])
                            #     self.chickens.remove(chicken)

                    one_bullet.rect.y -= self.settings.screen_height

            self.sb.prep_score()
            self.sb.check_high_score()
   
        if self.quaMan == False and  not self.chickens and not self.modes and (not self.rocks and self.rocks_times < 0):
            self.active_dame = False
            self.active_boss_dame = False
            if(self.chickenBoss):
                self.chickenBoss.fleet_active = False
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self.bullet_follows.empty()

            # Increase level.
            # if self.quaMan == False:
            self.stats.level += 1

            # Kiểm tra qua màn
            self.quaMan = True
            self.time_start = time.time()

            self.sb.prep_level()
            self.createAnemy()
            if self.stats.level%5==1:
                self.boss_music.stop()
                if self.music_on == True:
                    self.music.play(self.sfx.getSFx('music'), loops=-1)
            self.settings.increase_speed()

        if len(self.chickens) == 1 and self.chickenBoss and self.chickenBoss.rect.x == int(self.settings.screen_width / 2 - self.chickenBoss.width / 2):
            self.active_boss_dame = False
            self.chickenBoss.fleet_active = False
            

    def update_bullet_follower(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet_follow positions.
        self.bullet_follows.update()
        # Get rid of bullets that have disappeared.
        for bullet_follow in self.bullet_follows.copy():
            if (bullet_follow.rect[1] > self.settings.screen_height
                or bullet_follow.rect[0] > self.settings.screen_width
                or bullet_follow.rect[0] < 0):
                self.bullet_follows.remove(bullet_follow)

        self.check_bullet_follow_ship_collision()

    def check_bullet_follow_ship_collision(self):
        # Look for bullet_follows-ship collisions.
        collision = pygame.sprite.spritecollideany(self.ship, self.bullet_follows)
        if collision and self.shield==False:
            self.shield = True
            self.effect.add(Explosion(self.ship.rect.x, self.ship.rect.y, self.data.image.EXPLOSION))
            pygame.mixer.Sound.play(self.sfx.getSFx('explosion'))
            self.ship.y += self.settings.screen_height

            collision.kill()
            # self._ship_hit()

                    

    def check_rock_ship_collision(self):
        collisionRect = pygame.sprite.spritecollideany(self.ship, self.rocks)
        # collision = pygame.sprite.spritecollide(self.ship, self.rocks, False, pygame.sprite.collide_circle)
        collisionCircle = pygame.sprite.spritecollide (
                self.ship, self.rocks, dokill = False,
                collided = pygame.sprite.collide_circle_ratio(0.65)
            )
        if collisionCircle and collisionRect and self.shield==False:
            self.shield = True
            self.effect.add(Explosion(self.ship.rect.x, self.ship.rect.y, self.data.image.EXPLOSION))
            pygame.mixer.Sound.play(self.sfx.getSFx('explosion'))
            self.ship.y += self.settings.screen_height
            
            collisionRect.kill() 

    def update_Rocks(self):
        if self.rock_active == True:
            self.createRockRain(147)

            self.check_rock_ship_collision()
            # self.check_rock_bullet_collision()
            self.rocks.update()

            for rock in self.rocks.copy():
                if rock.rect.top>self.settings.screen_height or rock.rect.bottom<0 or rock.rect.right<0 or rock.rect.left>self.settings.screen_width:
                    self.rocks.remove(rock)

    def update_mode(self): 
        # self.modes.update()
        for mode in self.modes:
            if type(mode) is Egg:
                mode.update(self.timer)
            else:
                mode.update()

        for mode in self.modes.copy():
            if type(mode) is Egg and mode.rect.bottom >= self.settings.screen_height and mode.timer is None:
                mode.timer = 1000
                mode.rect.y -= 10
            if mode.rect.top>self.settings.screen_height or mode.rect.bottom<0 or mode.rect.right<0 or mode.rect.left>self.settings.screen_width:
                self.modes.remove(mode)

    def update_effect(self):
        self.effect.update()

        # print(sum(1 for i in self.effect if type(i) is Explosion))

        for e in self.effect.copy():
            # if type(e) is Explosion and e.current_image>len(e.images)-24:
            #     self.effect.remove(e)
            #     self._ship_hit()
            if e.current_image == len(e.images)-1:
                if type(e) is Explosion:
                    self._ship_hit()
                self.effect.remove(e)

    def drop_mode(self, pos_x, pos_y):
        # set ratio drop items
        choice_mode = random.randint(1,100)

        if choice_mode>=1 and choice_mode<=25:      #25% Roast and Drumstick
            self.modes.add(Drumstick(pos_x, pos_y, self.data.image.DRUMSTICK))
            self.modes.add(Roast(pos_x+20, pos_y+5, self.data.image.ROAST))
        elif choice_mode>25 and choice_mode<=55:    #30% Roast
            self.modes.add(Roast(pos_x, pos_y, self.data.image.ROAST))
        elif choice_mode>55 and choice_mode<=95:    #40% Drumstick
            self.modes.add(Drumstick(pos_x, pos_y, self.data.image.DRUMSTICK))
        elif choice_mode>0 and choice_mode<=97:    #2% Upgrade
            self.modes.add(Upgrade(pos_x, pos_y, self.data.image.UPGRADE))
        elif choice_mode>97 and choice_mode<=98:    #1% Heart
            self.modes.add(Heart(pos_x, pos_y, self.data.image.HEART))
        elif choice_mode>98 and choice_mode<=100:   #2% Change bullet
            choice_gift = random.randint(1,3)
            if choice_gift==1:
                self.modes.add(Gift(pos_x, pos_y, self.data.image.RED_GIFT, "red"))
            elif choice_gift==2:
                self.modes.add(Gift(pos_x, pos_y, self.data.image.GREEN_GIFT, "green"))
            else:
                self.modes.add(Gift(pos_x, pos_y, self.data.image.FLASH_GIFT, "flash"))

    def _update_chickens(self):
        """
        Check if the fleet is at an edge,
            then update the positions of all chickens in the fleet.
        """
        self._check_fleet_edges()
    
        self.check_move_fleet_chicken_boss()

        """drop eggs after particular time"""
        self.chickens.update(self.timer)
        if len(self.chickens):
            ratio = random.randint(1,len(self.chickens))
            start = 0
            check = False
            for chicken in self.chickens:
                start += 1
                if not check:
                    if chicken.timer_drop_eggs<=0 and start==ratio:
                        # self.modes.add(Egg(chicken.rect.x, chicken.rect.y))
                        if(issubclass(chicken.__class__, Chicken_Boss)):
                            self.modes.add(Big_Bullet(chicken.rect.x + chicken.rect.width / 2 - 10, chicken.rect.y + chicken.rect.height, self.data.image.BIG_BULLET) )
                        else:
                            self.modes.add(Egg(chicken.rect.x + chicken.rect.width / 2 - 10, chicken.rect.y + chicken.rect.height, self.data.image.EGG))
                       
                        check = True
                        chicken.timer_drop_eggs = 6000
                else:
                    chicken.timer_drop_eggs = 4000
        self.update_mode()

        # Look for chicken-ship collisions.
        collision = pygame.sprite.spritecollideany(self.ship, self.chickens)
        if collision and self.shield==False:
            self.shield = True
            self.effect.add(Explosion(self.ship.rect.x, self.ship.rect.y, self.data.image.EXPLOSION))
            pygame.mixer.Sound.play(self.sfx.getSFx('explosion'))
            self.ship.y += self.settings.screen_height
            
            collision.kill()

        # Look for items-ship collisions.
        collisions = pygame.sprite.spritecollideany(self.ship, self.modes)
        if collisions:
            # print(type(collisions))
            if (type(collisions) is Egg or type(collisions) is Big_Bullet) and self.shield==False:
                self.shield = True
                self.effect.add(Explosion(self.ship.rect.x, self.ship.rect.y, self.data.image.EXPLOSION))
                pygame.mixer.Sound.play(self.sfx.getSFx('explosion'))
                self.ship.y += self.settings.screen_height

                self.stats.score -= self.settings.collisions
                if self.stats.score<0:
                    self.stats.score = 0
            elif type(collisions) is Gift:
                pygame.mixer.Sound.play(self.sfx.getSFx('powerup'))
                if collisions.type == self.style_bullet:
                    self.bullet_level += 1
                    if self.bullet_level>6:
                        self.bullet_level = 6
                self.style_bullet = collisions.type
                self.stats.score += self.settings.gift_points
            elif type(collisions) is Roast:
                pygame.mixer.Sound.play(self.sfx.getSFx('eat'))
                self.stats.score += self.settings.roast_points
                self.stats.roast += 2
            elif type(collisions) is Drumstick:
                pygame.mixer.Sound.play(self.sfx.getSFx('eat'))
                self.stats.roast += 1
                self.stats.score += self.settings.drumstick_points
            elif type(collisions) is Heart:
                self.stats.ships_left += 1
                self.stats.score += self.settings.heart_points
            elif type(collisions) is Upgrade:
                pygame.mixer.Sound.play(self.sfx.getSFx('powerup'))
                self.bullet_level += 1
                if self.bullet_level>6:
                    self.bullet_level = 6
                self.stats.score += self.settings.gift_points

            self.sb.prep_score()
            self.sb.check_high_score()
            self.sb.prep_roast()
            self.sb.prep_ship_heart()

            collisions.kill()

        # Look for chickens hitting the bottom of the screen.
        self._check_chickens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an chicken."""
        if self.stats.ships_left > 0:
            # Decrement ships_left, and update scoreboard.
            self.stats.ships_left -= 1
            self.bullet_level -=2
            if self.bullet_level <= 0:
                self.bullet_level = 1
            self.sb.prep_ship_heart()
            self.ship.respawn_timer = 3000
            self.shield = True
            self.ship.spawn = True
            self.ship.spawn_ship()
        else:
            self.savestats()

    def savestats(self):
        self.highscores = self.load()
        if self.highscores[self.player_id][1]<self.stats.high_score:
            self.highscores[self.player_id][1]=self.stats.high_score
        current_roast=self.highscores[self.player_id][2]
        self.highscores[self.player_id][2]=current_roast+self.stats.roast
        self.save(sorted(self.highscores, key=itemgetter(1), reverse=True))

        self.modes.empty()
        self.effect.empty()
        self.shield = False
        self.stats.game_active = False

    def _check_chickens_bottom(self):
        """Check if any chickens have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        for chicken in self.chickens.sprites():
            if chicken.rect.bottom >= screen_rect.bottom:
                # Treat this the same as if the ship got hit.
                self._ship_hit()
                break
    def sound_settings(self):
        self.plot_background()
        self._update_screen()
        running = True
        click = False
        while running:
            self.screen.blit(self.settings.screen_bg, (0,0))
            #border
            rectBorder =  pygame.Rect(312, 170, 400, 300)   
            pygame.draw.rect(self.screen, (1, 30, 71), rectBorder, border_radius=20)
            pygame.draw.rect(self.screen, (10, 85, 165), rectBorder, 3, border_radius=20)
            #pause text
            text_surface = self.font_noti.render('SOUND', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-65, 175))
            
            #volumn text
            text_surface = self.font.render('MUSIC', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-33, 235))
            #volumn up button
            musicup_button = pygame.Rect(654, 255, 50, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), musicup_button, -1)
            musicup_img = pygame.image.load('images/menu/cong.png')
            self.screen.blit(musicup_img, (654, 255))
            #volumn down button
            musicdown_button = pygame.Rect(320, 255, 50, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), musicdown_button, -1)
            musicdown_img = pygame.image.load('images/menu/tru.png')
            self.screen.blit(musicdown_img, (320, 255))
            
            #volumn text
            text_surface = self.font.render('SFX', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-18, 325))
            #volumn up button
            sfxup_button = pygame.Rect(654, 345, 50, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), sfxup_button, -1)
            sfxup_img = pygame.image.load('images/menu/cong.png')
            self.screen.blit(sfxup_img, (654, 345))
            #volumn down button
            sfxdown_button = pygame.Rect(320, 345, 50, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), sfxdown_button, -1)
            sfxdown_img = pygame.image.load('images/menu/tru.png')
            self.screen.blit(sfxdown_img, (320, 345))

            #back button
            back_button = pygame.Rect(462, 400, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), back_button, -1)
            back_img = pygame.image.load('images/menu/back.png')
            self.screen.blit(back_img, (462, 400))

            #tuong tac voi cac button
            m1, m2 = pygame.mouse.get_pos()
            if musicdown_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.sfx.music_down()
            if musicup_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.sfx.music_up()
            if sfxdown_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.sfx.sfx_down()
            if sfxup_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.sfx.sfx_up()
            if back_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    running = False

            if self.sfx.ms_lv == 0:
                music_img = pygame.image.load('images/menu/vol_0.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 1:
                music_img = pygame.image.load('images/menu/vol_1.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 2:
                music_img = pygame.image.load('images/menu/vol_2.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 3:
                music_img = pygame.image.load('images/menu/vol_3.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 4:
                music_img = pygame.image.load('images/menu/vol_4.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 5:
                music_img = pygame.image.load('images/menu/vol_5.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 6:
                music_img = pygame.image.load('images/menu/vol_6.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 7:
                music_img = pygame.image.load('images/menu/vol_7.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 8:
                music_img = pygame.image.load('images/menu/vol_8.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 9:
                music_img = pygame.image.load('images/menu/vol_9.png')
                self.screen.blit(music_img, (380, 270))
            if self.sfx.ms_lv == 10:
                music_img = pygame.image.load('images/menu/vol_10.png')
                self.screen.blit(music_img, (380, 270))

            if self.sfx.sfx_lv == 0:
                sfx_img = pygame.image.load('images/menu/vol_0.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 1:
                sfx_img = pygame.image.load('images/menu/vol_1.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 2:
                sfx_img = pygame.image.load('images/menu/vol_2.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 3:
                sfx_img = pygame.image.load('images/menu/vol_3.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 4:
                sfx_img = pygame.image.load('images/menu/vol_4.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 5:
                sfx_img = pygame.image.load('images/menu/vol_5.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 6:
                sfx_img = pygame.image.load('images/menu/vol_6.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 7:
                sfx_img = pygame.image.load('images/menu/vol_7.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 8:
                sfx_img = pygame.image.load('images/menu/vol_8.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 9:
                sfx_img = pygame.image.load('images/menu/vol_9.png')
                self.screen.blit(sfx_img, (380, 360))
            if self.sfx.sfx_lv == 10:
                sfx_img = pygame.image.load('images/menu/vol_10.png')
                self.screen.blit(sfx_img, (380, 360))
            click=False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.flip()
            # clock.tick(self.settings.game_speed)

    def paused(self):
        self.plot_background()
        self._update_screen()
        running = True
        click = False
        while running:
            self.screen.blit(self.settings.screen_bg, (0,0))
            #border
            rectBorder =  pygame.Rect(312, 170, 400, 300)   
            pygame.draw.rect(self.screen, (1, 30, 71), rectBorder, border_radius=20)
            pygame.draw.rect(self.screen, (10, 85, 165), rectBorder, 3, border_radius=20)
            #pause text
            text_surface = self.font_noti.render('PAUSE', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-65, 175))
            
            #button Resume
            resume_button = pygame.Rect(430, 240, 164, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), resume_button, -1)
            resume_img = pygame.image.load('images/menu/resume.png')
            self.screen.blit(resume_img, (430, 240))

            #button Back to menu
            menu_button = pygame.Rect(428, 310, 168, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), menu_button, -1)
            menu_img = pygame.image.load('images/menu/menu.png')
            self.screen.blit(menu_img, (428, 310))

            #button sound settings to menu
            sound_button = pygame.Rect(428, 380, 168, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), sound_button, -1)
            sound_img = pygame.image.load('images/menu/sound.png')
            self.screen.blit(sound_img, (428, 380))

            #tuong tac voi cac button
            m1, m2 = pygame.mouse.get_pos()
            if resume_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    running = False
            if menu_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.savestats()
                    self.music.stop()
                    self.boss_music.stop()
                    from start import Menu
                    menu=Menu()
                    menu.main_menu()
            if sound_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.sound_settings()
            click=False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.flip()
            # clock.tick(self.settings.game_speed)

    def over(self):
        running = True
        click = False
        while running:
            self.plot_background()
            #border
            rectBorder =  pygame.Rect(312, 145, 400, 350)   
            pygame.draw.rect(self.screen, (1, 30, 71), rectBorder, border_radius=20)
            pygame.draw.rect(self.screen, (10, 85, 165), rectBorder, 3, border_radius=20)

            #pause text
            text_surface = self.font_noti.render('GAME OVER', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-110, 155))

            #score
            text_surface = self.font.render('SCORE', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-140, 220))
            text_surface = self.font.render(f'{self.stats.score}', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2+75, 220))

            #high_score
            text_surface = self.font.render('HIGH SCORE', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-140, 270))
            text_surface = self.font.render(f'{self.stats.high_score}', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2+75, 270))

            #roast
            text_surface = self.font.render('ROAST', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2-140, 320))
            text_surface = self.font.render(f'{self.stats.roast}', True, (255, 255, 255))
            self.screen.blit(text_surface, (self.settings.screen_width/2+75, 320))

            #menu button
            menu_button = pygame.Rect(351, 400, 122, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), menu_button, -1)
            resume_img = pygame.image.load('images/menu/menu1.png')
            self.screen.blit(resume_img, (351, 400))

            #again button
            again_button = pygame.Rect(551, 400, 122, 50)
            pygame.draw.rect(self.screen, (255, 0, 0), again_button, -1)
            resume_img = pygame.image.load('images/menu/again.png')
            self.screen.blit(resume_img, (551, 400))

            #tuong tac voi cac button
            m1, m2 = pygame.mouse.get_pos()
            if again_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.replay()
                    running = False
            if menu_button.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.savestats()
                    self.music.stop()
                    self.boss_music.stop()
                    from start import Menu
                    menu=Menu()
                    menu.main_menu()
            click=False

            #get event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.replay()
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.flip()
            clock.tick(self.settings.game_speed)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        # self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.chickens.draw(self.screen)
        self.modes.draw(self.screen)
        if(self.chickenBoss):
            self.chickenBoss.draw_hp()
        self.modes.draw(self.screen)
        if len(self.effect):
            self.effect.draw(self.screen)

        self.bullet_follows.draw(self.screen)

        self.rocks.draw(self.screen)

        # Draw the score information.
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.over()
        
        px,py = pygame.mouse.get_pos()
        self.screen.blit(self.img_mouse, (px-10,py-10))
        # Make the most recently drawn screen visible.
        pygame.display.flip()