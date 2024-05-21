import pygame
import sys
from agent import train


class Menu:

    def __init__(self) -> None:
        # Initialize Pygame
        pygame.init()

        # Screen settings
        self.screen_width = 900
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Eat or Die")

        # Fonts
        self.font = pygame.font.SysFont(None, 55)
        self.small_font = pygame.font.SysFont(None, 35)

        self.background_image_menu = pygame.image.load('game_menu.jpg')
        self.background_image_menu = pygame.transform.scale(self.background_image_menu, (self.screen_width, self.screen_height))

        self.background_image_ai = pygame.image.load('ai_menu.jpg')
        self.background_image_ai = pygame.transform.scale(self.background_image_ai, (self.screen_width, self.screen_height))



    def label(self,msg, x, y, w, h,mode, action=None):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            if click[0] == 1 and action is not None:
                action(mode)

            self.text_surface, self.text_rect = self.font.render(msg, True, (255,255,255)),self.font.render(msg, True, (255,255,255)).get_rect()
            self.text_rect.center = ((x + (w / 2)), (y + (h / 2)))
            self.screen.blit(self.text_surf, self.text_rect)

        else:
            self.text_surf, self.text_rect = self.font.render(msg, True, (0,0,0)),self.font.render(msg, True, (0,0,0)).get_rect()
            self.text_rect.center = ((x + (w / 2)), (y + (h / 2)))
            self.screen.blit(self.text_surf,self.text_rect)



    def choice_play(self,mode):
        self.choice="PLAY"
        # game=PlayerGame()
        # game.run()


    def choice_ai(self,mode):
        self.choice="AI"
        #train()

    def load_model(self,mode):
        train(mode)

    def train_model(self,mode):
        train(mode)


    def game_menu(self):
        self.choice="MENU"
        while True:
            if self.choice=="MENU":
                self.screen.blit(self.background_image_menu, (0, 0))

                self.label("", 150, 300, 300, 150,0, self.choice_play)
                self.label("", 500, 350, 300, 150,0, self.choice_ai)

            elif self.choice=="AI":
                self.screen.blit(self.background_image_ai, (0, 0))

                self.label("", 10, 180, 300, 150, 1, self.train_model)
                self.label("", 280, 210, 300, 150, 2, self.load_model)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()


if __name__ == "__main__":
    menu=Menu()
    menu.game_menu()
