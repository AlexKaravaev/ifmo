import pygame
from scene import Scene

class GameOverScene(Scene):

    def render(self):
        screen = self.gameEngine.screen

        font = pygame.font.Font(None,100)

        text = font.render("POBEDA POBEDA VMESTO OBEDA", 1 , (255,255,255))
        screen.blit(text, (self.__center(text),20))

        font2 = pygame.font.Font(None,32)

        text2 = font2.render("NAZHMI SPACE DLYA ZANOGO",1,(255,255,255))
        screen.blit(text2,(self.__center(text2),250))

    def update(self):
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            self.gameEngine.newGame()

    def __center(self, img):
        return (1280 - img.get_width())/2
