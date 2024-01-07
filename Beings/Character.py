from Layout.LayoutStuff import Layout
from Tools.Weapon import Weapon
from Beings.Instances import Instance
import pygame
import time
pygame.font.init()
textConfig = {"font": "dejavusans",
              "appearanceTime": 0.7,
              "fontSize": 15,
              "colour": (255, 255, 255),
              "align": None}


class Character(Instance):
    def __init__(self, image: str, x: int, y: int, screen):
        super().__init__(image, x, y, screen)
        self.health = 0
        self.speed = 0
        self.stopFillTime = 0
        self.tagged = False
        self.blinkTime = 0.1
        self.currentWeapon = None
        self.lastDropped = {}
        self.dropPickUpDelay = 3
        self.equipSlots = {1: None, 2: None, 3: None}
        self.currentEquipSlot = 1

        self.beforeCChange = {}
        # Damage Indicator related
        self.textBlinkTime = 0.7
        self.maxTextDamage = 5
        self.initPos = 15
        self.posIncreasement = 10
        self.maxPos = self.initPos+(self.posIncreasement*self.maxTextDamage)
        self.textTagged = False
        self.textList = {}
        self.newAppearedText = None

    def set_colour(self, value, rgb: list):
        for x in range(self.ix):
            self.beforeCChange[x] = {}
            for y in range(self.iy):
                colour = self.image.get_at((x, y))
                colourDict = {"r": colour.r, "g": colour.g, "b": colour.b, "a": colour.a}

                self.beforeCChange[x][y] = colourDict.copy()
                for i in list(rgb):

                    if (colourDict[i] + value) > 255:
                        colourDict[i] = 255
                    else:
                        colourDict[i] += value
                self.image.set_at((x, y), (colourDict["r"], colourDict["g"], colourDict["b"], colourDict["a"]))

    def return_old_colour(self, oldColourDict):
        for x in list(oldColourDict):
            for y in oldColourDict[x]:
                currentPixelRGB = oldColourDict[x][y]
                self.image.set_at(
                    (x, y),
                    (currentPixelRGB["r"],
                     currentPixelRGB["g"],
                     currentPixelRGB["b"],
                     currentPixelRGB["a"]))

    def deal_damage(self, damage):
        self.health -= damage
        if not self.tagged and time.time()-self.stopFillTime >= self.blinkTime:
            self.set_colour(65 if "Player" not in str(self) else 100, ["r"])
            self.stopFillTime = time.time()+self.blinkTime
            self.tagged = True
        if len(self.textList) < self.maxTextDamage:
            font = pygame.font.SysFont("dejavusans", 16)
            self.newAppearedText = font.render(str(damage), True, (255, 0, 0))
            self.textList[self.newAppearedText] = {"time": time.time(), "pos": self.initPos, "alpha": 255}
            self.textTagged = True

    def equip(self, weapon, slot):
        # self.currentWeapon = weapon
        # weapon.parent = self

        self.equipSlots[slot] = weapon
        weapon.isDropped = False
        if slot == self.currentEquipSlot:
            self.currentWeapon = self.equipSlots[self.currentEquipSlot]
            self.currentWeapon.parent = self

    def update(self, dt):
        super().update(dt)
        listOfCollidedWeapons = pygame.sprite.spritecollide(
            self, Weapon.listOfWeapons, False)
        for i in [i for i in listOfCollidedWeapons if i != self.currentWeapon and i.isDropped]:
            if isinstance(i, Weapon):
                if i not in self.lastDropped or (time.time() - self.lastDropped[i]) >= self.dropPickUpDelay:
                    for sn in self.equipSlots:
                        if not self.equipSlots[sn]:
                            self.equip(i, sn)
                            if "Player" in str(self):
                                notificePickup = notificePickup = Layout(
                                    0, self.sy*0.9, self.screen, f"You have picked up {i.name}", **textConfig, noAdd=True)
                                notificePickup.x = (
                                    self.sx/2)-(notificePickup.get_size()[0]/2)
                                Layout.listOfLayouts.append(notificePickup)

                            break
        if self.health <= 0:
            self.kill()
            for i in list(self.equipSlots):
                if self.equipSlots[i]:
                    weapon = self.equipSlots[i]
                    weapon.parent = None
                    weapon.isDropped = True
