import pygame, sys
from pygame.locals import *
import json
from operator import itemgetter
from chicken_invaders import ChickenInvaders
from settings import Settings
from game_stats import GameStats
from sound_effect import SFx
from data import Data

class Menu:
    def __init__(self):
        #Import other class
        self.core = ChickenInvaders()
        self.settings = Settings()
        self.stats = GameStats(self)
        self.data = Data()

        #Thiết lập kích thước màn hình
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Chicken Invaders 4 - Ultimate Omelette")
        self.mainClock = pygame.time.Clock()

        #Color
        self.BG_COLOR = pygame.Color('gray12')
        self.BLUE = pygame.Color('dodgerblue')

        #Font 
        self.font = pygame.font.SysFont(None, 32)
        self.font_title = pygame.font.Font(None, 40)
        self.font_input = pygame.font.Font(None, 32)

        self.img_mouse = pygame.transform.scale(pygame.image.load('images/mouse.png'),(46,49))
        self.mouse_rect = self.img_mouse.get_rect()

        self.sfx = SFx()

    def main_menu(self):
        self.title_music = pygame.mixer.Channel(0)
        self.title_music.play(self.sfx.getSFx('title_music'), loops=-1)
        click = False
        while True:
            pygame.mouse.set_visible(False)

            #Vẽ màu nền đăng nhập
            self.screen.fill((255,255,255))

            #Vẽ background trên menu
            backGroundMenu=pygame.image.load('images/menu/bg.jpg')
            self.bg=pygame.transform.scale(backGroundMenu,(self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(self.bg,(0,0))

            mx, my = pygame.mouse.get_pos()

            #Play button
            # button_1 = pygame.Rect(410, 375, 198, 85)
            # pygame.draw.rect(self.screen, (0, 0, 0), button_1)
            # surface2rect = pygame.Surface((375, 50))
            # surface2rect=pygame.image.load('images/menu/play.png')

            button_1 = pygame.Rect(410, 340, 198, 85)
            pygame.draw.rect(self.screen, (0, 0, 0), button_1, -1)
            play_img = pygame.image.load('images/menu/play.png')
            self.screen.blit(play_img, (410, 340))
            
            #Guide button
            button_2 = pygame.Rect(410, 440, 198, 85)
            pygame.draw.rect(self.screen, (0, 0, 0), button_2, -1)
            guide_img=pygame.image.load('images/menu/guide.png')
            self.screen.blit(guide_img, (410, 440))

            #Quit button
            quit_button = pygame.Rect(75, 550, 100, 41)
            pygame.draw.rect(self.screen, (0, 0, 0), quit_button, -1)
            quit_img=pygame.image.load('images/menu/quit.png')
            self.screen.blit(quit_img, (75, 550))

            #Nút thao tác trên màn hình menu
            if button_1.collidepoint((mx, my)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.player()
            if button_2.collidepoint((mx, my)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.guide()
            if quit_button.collidepoint((mx, my)):
                if click:
                    pygame.quit()
                    sys.exit()
            click = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.update()
            self.mainClock.tick(self.settings.game_speed)

    def draw_text(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x,y)
        surface.blit(textobj, textrect)

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
    
    #Nhap ten nguoi choi
    def player(self):
        input_box = pygame.Rect(250, 90, 515, 40)
        color_inactive = pygame.Color(255,255,255)
        color_active = self.BLUE
        color = color_inactive
        active = False
        text = ''
        hold=0
        self.highscores = self.load()  # Load the json file.
        running = True
        click = False

        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if active == True:
                        if event.key == pygame.K_BACKSPACE:
                            text = text[:-1]
                        else:
                            if len(text)<=30:
                                text += event.unicode
                    else:
                        if event.key == pygame.K_DOWN:
                            if hold<len(self.highscores)-1:
                                pygame.mixer.Sound.play(self.sfx.getSFx('selector'))
                                hold=hold+1
                        elif event.key == pygame.K_UP:
                            if hold>0:
                                pygame.mixer.Sound.play(self.sfx.getSFx('selector'))
                                hold=hold-1
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # If the user clicked on the input_box rect.
                    if event.button == 1:
                        click = True
                    if input_box.collidepoint(event.pos):
                        if click:
                            pygame.mixer.Sound.play(self.sfx.getSFx('selector'))
                            active = True
                    elif button_next.collidepoint(event.pos):
                        active=active
                    else:
                        active = False
                    # if event.button == 1:
                    #     click = True
                    # Change the current color of the input box.
                    color = color_active if active else color_inactive
            
            self.screen.fill((30, 30, 50))
            #Vẽ nền
            backGroundGuide=pygame.image.load('images/menu/bg2.jpg')
            bg2=pygame.transform.scale(backGroundGuide,
                (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bg2,(0,0))
            
            #Input box
            self.draw_text("Enter your name", self.font_title, (255,0,0), self.screen, 250, 50)
            txt_surface = self.font_input.render(text, True, color)
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            
            # Display the text high-scores.
            self.draw_text('Name', self.font_title, (255,0,0), self.screen, 250, 160)
            self.draw_text('Highscore', self.font_title, (255,0,0), self.screen, 600, 160)

            #Chon player cu
            if active == False:
                l_picker = pygame.image.load('images/menu/l_picker.png')
                self.screen.blit(l_picker, (180,hold*40+190))
                r_picker = pygame.image.load('images/menu/r_picker.png')
                self.screen.blit(r_picker, (785,hold*40+190))

            #In tên player cũ
            for i in range(len(self.highscores)):
                self.draw_text(self.highscores[i][0], self.font, (255,255,255), self.screen, 250, i*40+200)
                self.draw_text(f"{self.highscores[i][1]}", self.font, (255,255,255), self.screen, 600, i*40+200)

            #Display next button
            button_next = pygame.Rect(825, 550, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_next,-1)
            surface_nextrect = pygame.image.load('images/menu/next.png')
            self.screen.blit(surface_nextrect, (825, 550))

            #Display back button
            button_back = pygame.Rect(75, 550, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_back,-1)
            surface_backrect = pygame.image.load('images/menu/back.png')
            self.screen.blit(surface_backrect, (75, 550))

            m1, m2 = pygame.mouse.get_pos()
            if button_next.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    if active:
                        if text != "":
                            self.highscores.append([text, 0, 0])
                            self.save(self.highscores)
                            self.playerId=len(self.highscores)-1
                            self.core.name_player=text
                            self.core.player_id=self.playerId
                            self.pick_ship()
                    else:
                        self.playerId=hold
                        self.core.name_player=self.highscores[self.playerId][0]
                        self.core.player_id=self.playerId
                        self.pick_ship()
            if button_back.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.main_menu()
            click = False
            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.flip()   
            self.mainClock.tick(self.settings.game_speed)
    #Tàu trái
    def pick_ship1(self):
            running = True
            click = False
            while running:
                self.screen.fill((0,0,0))

                #Vẽ nền game chọn tàu
                backGroundGuide=pygame.image.load('images/menu/bg3.jpg')
                bG=pygame.transform.scale(backGroundGuide,
                    (self.settings.screen_width, self.settings.screen_height))
                self.screen.blit(bG,(0,0))
                self.draw_text('Choose a Spaceship', self.font_title, (255, 255, 255), self.screen, 370, 50)
                self.draw_text(f'{self.settings.cost_ship_1}', self.font, (255, 255, 255), self.screen, 480,485)

                #Vẽ tàu chiến ở giữa
                surface2rect=pygame.image.load('images/menu/love.png')
                surface2rect=pygame.transform.scale(surface2rect, (142, 120))
                self.screen.blit(surface2rect, (440,180))

                #Vẽ nút ấn tam giác bên phải và tương tác
                button_4 = pygame.Rect(680, 200, 75, 80)
                pygame.draw.rect(self.screen, (135,206,235), button_4,-1)
                surface4rect=pygame.image.load('images/menu/right_Button.png')
                self.screen.blit(surface4rect, (680, 200))

                #Vẽ đùi gà hiện có
                surface6rect=pygame.image.load('images/menu/drumstick.png')
                self.screen.blit(surface6rect, (self.settings.screen_width/5*4,
                 self.settings.screen_height/5*2))
                self.draw_text(f"{self.highscores[self.playerId][2]}", self.font, (255, 255, 255),
                 self.screen, self.settings.screen_width/5*4+50, self.settings.screen_height/5*2+5)

                #Vẽ giá tiền
                surface7rect=pygame.image.load('images/menu/drumstick.png')
                self.screen.blit(surface7rect, (535,480))

                #Vẽ nút mua
                button_buy = pygame.Rect(485, 515, 100, 47)
                pygame.draw.rect(self.screen, (255, 0, 0), button_buy,-1)
                surface_playrect = pygame.image.load('images/menu/buy2.png')
                self.screen.blit(surface_playrect, (485, 515))

                #Display back button
                button_back = pygame.Rect(75, 550, 100, 47)
                pygame.draw.rect(self.screen, (255, 0, 0), button_back,-1)
                surface_backrect = pygame.image.load('images/menu/back.png')
                self.screen.blit(surface_backrect, (75, 550))
                
                #Nút thao tác trên màn hình menu
                m1, m2 = pygame.mouse.get_pos()
                if button_4.collidepoint((m1, m2)):
                    if click:
                        pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                        self.pick_ship()
                if button_buy.collidepoint((m1, m2)):
                    if click:
                        pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                        if self.highscores[self.playerId][2] >= self.settings.cost_ship_1:
                            #Tạo biến để kiểm tra chọn phi thuyền và vào game
                            chon_phi_thuyen = 1
                            self.save(self.highscores)
                            self.core.run_game(chon_phi_thuyen, self.data)
                        else:
                            self.notification()
                if button_back.collidepoint((m1, m2)):
                    if click:
                        pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                        self.player()
                click = False
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == KEYDOWN:
                        if event.key == K_RIGHT:
                            self.pick_ship()
                    if event.type == MOUSEBUTTONDOWN:
                        if event.button == 1:
                            click = True
                px,py = pygame.mouse.get_pos()
                self.screen.blit(self.img_mouse, (px-10,py-10))
                pygame.display.update()
                self.mainClock.tick(self.settings.game_speed) 
    #Tàu giữa
    def pick_ship(self):
        running = True
        click = False
        while running:
            self.screen.fill((0,0,0))
            
            #Vẽ nền game chọn tàu
            backGroundGuide=pygame.image.load('images/menu/bg3.jpg')
            bG=pygame.transform.scale(backGroundGuide,
                (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bG,(0,0))
            self.draw_text('Choose a Spaceship', self.font_title, (255, 255, 255), self.screen, 370, 50)

            #Vẽ tàu chiến ở giữa
            surface2rect=pygame.image.load('images/ship/ship.png')
            self.screen.blit(surface2rect, (440, 180))

            #Vẽ nút tam giác bên trái và tương tác
            button_3 = pygame.Rect(292, 200, 75, 80)
            pygame.draw.rect(self.screen, (135,206,235), button_3,-1)
            # surface3rect = pygame.Surface((150, 50))
            surface3rect=pygame.image.load('images/menu/left_Button.png')
            self.screen.blit(surface3rect, (292, 200))

            #Vẽ nút ấn tam giác bên phải và tương tác
            button_4 = pygame.Rect(680, 200, 75, 80)
            pygame.draw.rect(self.screen, (135,206,235), button_4,-1)
            # surface4rect = pygame.Surface((150, 50))
            surface4rect=pygame.image.load('images/menu/right_Button.png')
            self.screen.blit(surface4rect, (680, 200))

            #Display play button
            button_play = pygame.Rect(825, 550, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_play,-1)
            surface_playrect = pygame.image.load('images/menu/play1.png')
            self.screen.blit(surface_playrect, (825, 550))

            #Display back button
            button_back = pygame.Rect(75, 550, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_back,-1)
            surface_backrect = pygame.image.load('images/menu/back.png')
            self.screen.blit(surface_backrect, (75, 550))

            #Nút thao tác trên màn hình menu
            m1, m2 = pygame.mouse.get_pos()
            if button_3.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.pick_ship1()
            if button_4.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.pick_ship2()
            if button_play.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    #Tạo biến để kiểm tra chọn phi thuyền và vào game
                    self.title_music.stop()
                    chon_phi_thuyen = 2
                    self.core.run_game(chon_phi_thuyen, self.data)
            if button_back.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.player()
            click = False
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.pick_ship1()
                    if event.key == K_RIGHT:
                        self.pick_ship2()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.update()
            self.mainClock.tick(self.settings.game_speed)
    #Tàu phải
    def pick_ship2(self):
        running = True
        click = False
        while running:
            self.screen.fill((0,0,0))

            #Vẽ nền game chọn tàu
            backGroundGuide=pygame.image.load('images/menu/bg3.jpg')
            bG=pygame.transform.scale(backGroundGuide,
                (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bG,(0,0))
            self.draw_text('Choose a Spaceship', self.font_title, (255, 255, 255), self.screen, 370, 50)
            self.draw_text(f'{self.settings.cost_ship_2}', self.font, (255, 255, 255), self.screen, 465,485)

            #Vẽ tàu chiến ở giữa
            surface2rect=pygame.image.load('images/menu/phi_thuyen.png')
            surface2rect=pygame.transform.scale(surface2rect, (142, 124))
            self.screen.blit(surface2rect, (440, 180))

            #Vẽ giá tiền
            surface7rect=pygame.image.load('images/menu/drumstick.png')
            self.screen.blit(surface7rect, (520,480))

            #Vẽ nút tam giác bên trái và tương tác
            button_3 = pygame.Rect(292, 200, 75, 80)
            pygame.draw.rect(self.screen, (135,206,235), button_3,-1)
            surface3rect=pygame.image.load('images/menu/left_Button.png')
            self.screen.blit(surface3rect, (292, 200))

            #Vẽ đùi gà hiện có
            surface6rect=pygame.image.load('images/menu/drumstick.png')
            self.screen.blit(surface6rect, (self.settings.screen_width/5*4,
             self.settings.screen_height/5*2))
            self.draw_text(f"{self.highscores[self.playerId][2]}", self.font, (255, 255, 255),
             self.screen, self.settings.screen_width/5*4+50, self.settings.screen_height/5*2+5)

            #Vẽ nút mua
            button_buy = pygame.Rect(470, 515, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_buy,-1)
            surface_playrect = pygame.image.load('images/menu/buy2.png')
            self.screen.blit(surface_playrect, (470, 515))

            #Display back button
            button_back = pygame.Rect(75, 550, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_back,-1)
            surface_backrect = pygame.image.load('images/menu/back.png')
            self.screen.blit(surface_backrect, (75, 550))

            m1, m2 = pygame.mouse.get_pos()
            if button_3.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.pick_ship()
            if button_buy.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    if self.highscores[self.playerId][2] >= self.settings.cost_ship_2:
                        #Tạo biến để kiểm tra chọn phi thuyền và vào game
                        chon_phi_thuyen = 3
                        self.save(self.highscores)
                        self.core.run_game(chon_phi_thuyen, self.data) 
                    else:
                        self.notification()
            if button_back.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.player()
            click = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_LEFT:
                        self.pick_ship()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.update()
            self.mainClock.tick(self.settings.game_speed)
    
    def notification(self):
        running = True
        click = False
        while running:
            self.screen.fill((0,0,0))

            #Vẽ nền thông báo
            backGroundGuide=pygame.image.load('images/menu/bg3.jpg')
            bG=pygame.transform.scale(backGroundGuide,
                (self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bG,(0,0))
            self.draw_text('You do not have enough roast', self.font, (255, 255, 255), self.screen, 330, 300)
            surface2rect=pygame.image.load('images/menu/money.png')
            self.screen.blit(surface2rect, (440, 200))

            #Display back button
            button_back = pygame.Rect(100, 515, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_back,-1)
            surface_backrect = pygame.image.load('images/menu/back.png')
            self.screen.blit(surface_backrect, (100, 515))

            #Nút thao tác trên màn hình menu
            m1, m2 = pygame.mouse.get_pos()
            if button_back.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    running = False
            click = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True
            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.update()
            self.mainClock.tick(self.settings.game_speed)   
    #Hướng dẫn chơi game
    def guide(self):
        click=False
        running = True
        while running:
            self.screen.fill((0,0,0))
            #Tạo nền cho phần hướng dẫn
            backGroundGuide=pygame.image.load('images/menu/bg4.png')
            bG=pygame.transform.scale(backGroundGuide,(self.settings.screen_width, self.settings.screen_height))
            self.screen.blit(bG,(0,0))
            #text hướng dẫn chơi
            self.draw_text("Guide", self.font_title, (255, 0, 0), self.screen, 450, 50) 
            f=open("guide.txt","r",encoding="utf8")
            lines = f.read().split("\n")
            i=100
            for line in lines:
                self.draw_text(line,pygame.font.Font('arial.ttf',24),(255,255,255),self.screen,50,i)
                i+=40

            #Display back button
            button_back = pygame.Rect(825, 550, 100, 47)
            pygame.draw.rect(self.screen, (255, 0, 0), button_back,-1)
            surface_backrect = pygame.image.load('images/menu/back.png')
            self.screen.blit(surface_backrect, (825, 550))

            m1, m2 = pygame.mouse.get_pos()
            if button_back.collidepoint((m1, m2)):
                if click:
                    pygame.mixer.Sound.play(self.sfx.getSFx('click'))
                    self.main_menu()
            click = False

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1:
                        click = True

            px,py = pygame.mouse.get_pos()
            self.screen.blit(self.img_mouse, (px-10,py-10))
            pygame.display.update()
            self.mainClock.tick(self.settings.game_speed)
         
if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    ci = Menu()
    ci.main_menu()