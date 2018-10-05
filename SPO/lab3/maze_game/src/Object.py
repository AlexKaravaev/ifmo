import pygame

class Object:
    
    def __init__(self, scene, x, y, width, height, texture):
        self.scene = scene
        self.texture = texture
        self.pos = (x,y)
        self.size = (width, height)
        self.rectangle = pygame.Rect(x,y,width,height)

    def render(self):
        self.scene.gameEngine.screen.blit(self.texture,(self.pos[0]*self.size[0]-10,
                                                        self.pos[1]*self.size[1]-10))
