
import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, ai_game):
        """Initialize scorekeeping attributes."""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # Color of wrap
        self.color_bg_wrap = (1, 43, 81)
        self.color_border_wrap = (10, 95, 145)


        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('snapitc', 20)

        # Prepare the initial score image.
        self.prep_score()
        self.prep_high_score()
        self.prep_ship_heart()
        self.prep_level()
        self.prep_roast()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        score_str = self.ai_game.name_player + ":  " + score_str
        self.score_image = self.font.render(score_str, True,
                (242, 100, 100))
        # self.score_image = self.font.render(score_str, True,
        #         self.text_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.x = 5
        self.score_rect.y = 32 + 25

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = round(self.stats.high_score, -1)
        high_score_str = "High Score:  " + "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                self.text_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.x = 5
        self.high_score_rect.y = 5

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()


    def prep_ship_heart(self):
        """ Show heart """
        self.heart_image = pygame.image.load('images\img_score\heart1.png')
        heart_width, heart_height = self.heart_image.get_rect().size
        ratio = heart_width / heart_height
        self.heart_image = pygame.transform.scale(self.heart_image, (round(ratio * 24), 24))
        self.heart_rect = self.heart_image.get_rect()
        self.heart_rect.x = 15
        self.heart_rect.y = self.settings.screen_height - 32

        """Show how many ships are left.""" 
        ships_str = str(self.stats.ships_left)
        self.ships_image = self.font.render(ships_str, True,
                self.text_color)

        # Position the ships_left at left bottom
        self.ships_rect = self.ships_image.get_rect()
        self.ships_rect.x = self.heart_rect.x + self.heart_rect.size[0] + 10 
        self.ships_rect.y = self.heart_rect.y + round((self.heart_rect.size[1] - self.ships_rect.size[1]) / 2 + 1)

    
    def prep_level(self):
        """ Show flag """
        self.flag_image = pygame.image.load('images/img_score/flag.png')
        heart_width, heart_height = self.flag_image.get_rect().size
        ratio = heart_width / heart_height
        self.flag_image = pygame.transform.scale(self.flag_image, (round(ratio * 24), 24))
        self.flag_rect = self.flag_image.get_rect()
        self.flag_rect.x = self.ships_rect.x + 24 + 10 + 4
        self.flag_rect.y = self.settings.screen_height - 32


        """Turn the level into a rendered image."""
        level_str =  str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                self.text_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.x = self.flag_rect.x + 35
        self.level_rect.y = self.ships_rect.y

        self.prep_roast()

    def prep_roast(self):
        """ Show roast """
        self.roast_image = pygame.image.load('images\Present\\roast.png')
        roast_width, roast_height = self.roast_image.get_rect().size
        ratio = roast_width / roast_height
        self.roast_image = pygame.transform.scale(self.roast_image, (round(ratio * 24), 24))
        self.roast_rect = self.roast_image.get_rect()
        self.roast_rect.x = self.level_rect.x + self.level_rect.size[0] +  17
        # self.roast_rect.x = self.level_rect.x + self.level_image.get_width +  17
        self.roast_rect.y = self.settings.screen_height - 32

        """Show how many roast.""" 
        amount_roast_str = str(self.stats.roast)
        self.amount_roast_image = self.font.render(amount_roast_str, True,
                self.text_color)

        self.amount_roast_rect = self.amount_roast_image.get_rect()
        self.amount_roast_rect.x = self.roast_rect.x + self.roast_rect.size[0] + 10
        self.amount_roast_rect.y = self.roast_rect.y + round((self.roast_rect.size[1] - self.amount_roast_rect.size[1]) / 2 + 1)
        

    def show_score(self):
        """Draw scores, level, and ships to the screen."""

        """ Draw border for score """ 
        rectBorderScore =  pygame.Rect(-5, self.score_rect.y - 4, self.score_rect.size[0] + 35, 36)
        pygame.draw.rect(self.screen, (70, 7,97), rectBorderScore, border_top_right_radius=45, border_bottom_right_radius=45)
        pygame.draw.rect(self.screen, (97, 8, 122), rectBorderScore, 3, border_top_right_radius=45, border_bottom_right_radius=45)
        # pygame.draw.rect(self.screen, self.color_bg_wrap, rectBorderScore, border_top_right_radius=45, border_bottom_right_radius=45)
        # pygame.draw.rect(self.screen, self.color_border_wrap, rectBorderScore, 4, border_top_right_radius=45, border_bottom_right_radius=45)
        self.screen.blit(self.score_image, self.score_rect)

        """ Draw border for high score """ 
        rectBorderHighScore =  pygame.Rect(-5, -5, self.high_score_rect.size[0] + 40, 49)
        pygame.draw.rect(self.screen, self.color_bg_wrap, rectBorderHighScore, border_bottom_right_radius=38)
        pygame.draw.rect(self.screen, self.color_border_wrap, rectBorderHighScore, 3, border_bottom_right_radius=38)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        
        """ Draw border for ship heart """ 
        rectBorderHeart = pygame.Rect(-10, self.ships_rect.y - 15, 219 + self.level_rect.size[0] + self.amount_roast_rect.size[0], 50)
        # pygame.draw.rect(self.screen, self.color_bg_wrap, rectBorderHeart, border_top_right_radius = 45)
        # pygame.draw.rect(self.screen, self.color_border_wrap, rectBorderHeart, 4, border_top_right_radius = 45)
        pygame.draw.rect(self.screen, (1, 30, 71), rectBorderHeart, border_top_right_radius = 45)
        pygame.draw.rect(self.screen, (10, 85, 165), rectBorderHeart, 3, border_top_right_radius = 45)

        self.screen.blit(self.heart_image, self.heart_rect)
        self.screen.blit(self.ships_image, self.ships_rect)

        self.screen.blit(self.flag_image, self.flag_rect)
        self.screen.blit(self.level_image, self.level_rect)

        self.screen.blit(self.roast_image, self.roast_rect)
        self.screen.blit(self.amount_roast_image, self.amount_roast_rect)

