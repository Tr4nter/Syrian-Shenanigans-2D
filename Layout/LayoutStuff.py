import pygame
import time
from Beings.Instances import Instance
pygame.font.init()

class Layout(object):
    listOfLayouts = []
    def __init__(self, x, y, screen, textContent, **kwargs):
        self.x = x
        self.y = y
        self.screen = screen
        self.font = kwargs["font"]
        self.appearanceTime = kwargs["appearanceTime"]
        self.tick = time.time()
        self.fontSize = kwargs["fontSize"]
        self.textContent = textContent
        self.fontObj = pygame.font.SysFont(self.font, self.fontSize)
        self.colour = kwargs["colour"]
        self.rect = None
        self.onClicked = None
        self.size = pygame.font.Font.size(self.fontObj, self.textContent)
        self.description = kwargs["description"] if "description" in kwargs else None
        self.align = kwargs["align"]
        if "noAdd" not in kwargs:
            Layout.listOfLayouts.append(self)


    @classmethod
    def remove(cls, valToRemove):
        cls.listOfLayouts.remove(valToRemove)
        valToRemove = None

    def is_clicked(self, pos):
        x, y = pos[0], pos[1]
        if self.rect.collidepoint((x, y)):
            return True
        return False

    def click(self):
        if self.onClicked:
            self.onClicked(self)

    def get_size(self):
        return self.size

    def update(self):
        fontSurf = self.fontObj.render(self.textContent, True, self.colour)
        if self.align == "center":
           self.x = self.screen.get_size()[0]/2-(self.size[0]/2)
        elif self.align == "topright":
            self.x = self.screen.get_size()[0]-self.size[0]


        self.screen.blit(fontSurf, (self.x, self.y))
        if (time.time()-self.tick) >= self.appearanceTime:
            Layout.remove(self)
        self.rect = fontSurf.get_rect(topleft=(self.x,self.y))
        self.size = pygame.font.Font.size(self.fontObj, self.textContent)






