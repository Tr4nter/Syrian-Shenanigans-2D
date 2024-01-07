import pygame
import sys
import time
import math
from Utils.Utils import *
import Beings
import Tools


pygame.font.init()


class Instance:
    listOfInstances = []
    isPaused = False

    def __init__(self, image: str, x: int, y: int, screen):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image).convert_alpha()
        self.originalimage = self.image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.ix, self.iy = self.originalimage.get_size()
        self.screen = screen
        self.sx, self.sy = self.screen.get_size()
        if "Projectile" not in str(type(self)):
            Instance.listOfInstances.append(self)

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.__dict__ == other.__dict__

    def __ne__(self, other):
        if other is None:
            return True
        else:
            return self.__dict__ != other.__dict__

    def __hash__(self):
        return hash(repr(self))

    def kill(self):
        if self in Instance.listOfInstances:
            Instance.listOfInstances.remove(self)

        self = None

    def update(self, dt):
        if "speed" in self.__dict__:
            # Limits the being from going outside of the screen
            speedDeltaTime = self.speed*dt
            if not "Projectile" in str(type(self)):
                if (self.y-(speedDeltaTime)) < 0:
                    self.y += speedDeltaTime
                if (self.y+(speedDeltaTime)) > self.sy-(self.iy*2):
                    self.y -= speedDeltaTime
                if (self.x-(speedDeltaTime)) < 0:
                    self.x += speedDeltaTime
                if (self.x+(speedDeltaTime)) > self.sx-self.ix:
                    self.x -= speedDeltaTime

        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.screen.blit(self.image, (self.x, self.y))
        if "stopFillTime" in self.__dict__:
            if "tagged" in self.__dict__ and self.tagged and time.time()-self.stopFillTime >= self.blinkTime:
                self.return_old_colour(self.beforeCChange)
                self.tagged = False
        if "textList" in self.__dict__:
            for k in list(self.textList):
                appearedOrder = list(self.textList).index(k)+1
                positionSupposedToBeAt = (len(self.textList)-appearedOrder)*self.posIncreasement+self.initPos

                if (time.time()-self.textList[k]["time"]) >= self.textBlinkTime:
                    del self.textList[k]
                    continue

                elif k != self.newAppearedText and self.textList[k]["pos"] < positionSupposedToBeAt:
                    self.textList[k]["pos"] = positionSupposedToBeAt
                    normalized = normalize(appearedOrder, 0, self.maxTextDamage)
                    alphaToUpdate = 255 * (normalized if normalized > 0 else 0.8)
                    if alphaToUpdate <= 0:
                        alphaToUpdate = 0
                    elif alphaToUpdate >= 255:
                        alphaToUpdate = 255
                    self.textList[k]["alpha"] = alphaToUpdate
                if len(list(self.textList)) == self.maxTextDamage:
                    del self.textList[list(self.textList)[0]]

    def rotate_to_mouse(self, mouseLocation):
        mx, my = mouseLocation[0], mouseLocation[1]
        angle = int((180 / math.pi) * -math.atan2(my-self.y, mx-self.x))
        if (angle > 90 or (angle > -180 and angle < -90)) and "Weapon" in str(type(self)):
            self.rect = self.flippedImage.get_rect(center=(self.x, self.y))
            self.image = pygame.transform.rotate(self.flippedImage, 180+angle)
            self.isFlipped = True
        else:
            self.rect = self.originalimage.get_rect(center=(self.x, self.y))
            self.image = pygame.transform.rotate(self.originalimage, angle)
            self.isFlipped = False
