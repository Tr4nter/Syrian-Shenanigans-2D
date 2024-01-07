import pygame
from Beings.Instances import Instance
from Beings.Player import Player

class PickupItem(Instance):
    listOfPickups = []
    def __init__(self, image, x, y, screen, name):
        super().__init__(image, x, y, screen)
        self.name = name
        self.onPickup = None
        PickupItem.listOfPickups.append(self)

    def update(self, dt):
        super().update(dt)

        listOfCols = pygame.sprite.spritecollide(self, [i for i in Instance.listOfInstances if i!=self], False)
        if self.onPickup and len(listOfCols) > 0:
            for i in listOfCols:
                if isinstance(i, Player):
                    if self.onPickup(self, i):
                        self.kill()



