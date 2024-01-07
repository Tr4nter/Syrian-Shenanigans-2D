from Beings.Character import Character
import pygame
import time
from Tools.Weapon import Weapon

from Layout.LayoutStuff import Layout
textConfig = {"font": "dejavusans",
              "appearanceTime": 0.7,
              "fontSize": 15,
              "colour": (255, 255, 255),
              "align": None}
pygame.font.init()


class Player(Character):
    listOfPlayers = []

    def __init__(self, image: str, x: int, y: int, screen):
        super().__init__(image, x, y, screen)
        self.up = False
        self.down = False
        self.left = False
        self.right = False
        self.health = 200
        self.speed = 75
        self.fillToAdd = 150

        Player.listOfPlayers.append(self)

    def keyChange(self, typeOfChange: str, key):
        isPressed = True if typeOfChange == "down" else False

        if key == pygame.K_w:
            self.up = isPressed
        if key == pygame.K_s:
            self.down = isPressed
        if key == pygame.K_a:
            self.left = isPressed

        if key == pygame.K_d:
            self.right = isPressed

        if isPressed:
            try:
                keyPressed = int(pygame.key.name(key))
                if keyPressed in self.equipSlots and keyPressed != self.currentEquipSlot:
                    if self.equipSlots[self.currentEquipSlot]:
                        self.equipSlots[self.currentEquipSlot].parent = None
                    self.currentEquipSlot = keyPressed
                    if self.equipSlots[self.currentEquipSlot]:
                        self.currentWeapon = self.equipSlots[self.currentEquipSlot]
                        self.equipSlots[self.currentEquipSlot].parent = self
                        nofText = f"Slot {keyPressed}: {self.currentWeapon.name}"
                    else:
                        self.currentWeapon = None
                        nofText = f"Slot {keyPressed}: Empty"

                    for i in Layout.listOfLayouts:
                        if i.textContent.startswith("Slot"):
                            Layout.remove(i)
                    noftificeSlotChange = Layout(
                        0, self.sy*0.9, self.screen, nofText, **textConfig, noAdd=True)
                    noftificeSlotChange.x = (
                        self.sx/2)-(noftificeSlotChange.get_size()[0]/2)
                    Layout.listOfLayouts.append(noftificeSlotChange)
            except ValueError:
                pass

    def drop(self):
        if self.currentWeapon:
            self.lastDropped[self.currentWeapon] = time.time()
            self.equipSlots[self.currentEquipSlot] = None
            self.currentWeapon.parent = None

            self.currentWeapon.isDropped = True
            self.currentWeapon = None

    def kill(self):
        if self in Player.listOfPlayers:

            Player.listOfPlayers.remove(self)
        super().kill()

