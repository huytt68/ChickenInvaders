import pygame 

class Rocket():
    def __init__(self, screen,check):
        # super().__init__()
        self.screen = screen
        self.check = check

        self.sprites = []
        for i in range(1,13):
            self.sprites.append(pygame.image.load("images/ship/rocket/"+str(i)+"_1.png"))
        if self.check==2:
            self.sprites = [pygame.transform.scale(i,(24,100)) for i in self.sprites]
        else:
            self.sprites = [pygame.transform.scale(i,(40,120)) for i in self.sprites]

        self.current_image = 0
        self.rocket_image = self.sprites[self.current_image]
    
    def update(self):
        self.current_image += 1

        if self.current_image >= len(self.sprites):
            self.current_image = 0

        self.rocket_image = self.sprites[self.current_image]

    def draw(self, ship):
        if self.check==1 or self.check==3:
            if ship.moving_left:
                self.screen.blit(self.rocket_image, [ship.x + (ship.ship_width - self.rocket_image.get_width()) // 2 +6, ship.y + ship.ship_height-18])
            elif ship.moving_right:
                self.screen.blit(self.rocket_image, [ship.x + (ship.ship_width - self.rocket_image.get_width()) // 2 -6, ship.y + ship.ship_height-18])
            else:
                self.screen.blit(self.rocket_image, [ship.x + (ship.ship_width - self.rocket_image.get_width()) // 2, ship.y + ship.ship_height-18])
        else:
            self.screen.blit(self.rocket_image, [ship.x + (ship.ship_width - self.rocket_image.get_width()) // 2 -21, ship.y + ship.ship_height-22])
            self.screen.blit(self.rocket_image, [ship.x + (ship.ship_width - self.rocket_image.get_width()) // 2 +22, ship.y + ship.ship_height-22])