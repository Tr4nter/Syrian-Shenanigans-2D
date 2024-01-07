import pygame
from Beings.Instances import Instance
from Beings.Character import Character
from Tools.Weapon import Weapon
from Beings.Player import Player
from Utils.Utils import *
import math

import time


class Enemy(Character):
    listOfEnemies = []

    def __init__(self, image: str, x: int, y: int, screen):
        super().__init__(image, x, y, screen)
        self.speed = 50
        self.health = 500
        self.damage = 25
        self.damageDelayTime = 3
        self.lastTimeDealtDamage = 0
        self.equipSlots = {1: None}
        self.target = None
        Enemy.listOfEnemies.append(self)

    def move_towards_player(self, player, dt):
        group = [i for i in Enemy.listOfEnemies if i != self]
        listOfCols = pygame.sprite.spritecollide(self, group+Player.listOfPlayers, False)
        if player:
            if len(listOfCols) < 1:
                dx, dy = get_direction(player.x, self.x, player.y, self.y)
                if not self.currentWeapon:
                    for i in Weapon.listOfWeapons:
                        if not i.parent and i.pickingUp == None or i.pickingUp == self and i.isDropped:
                            i.pickingUp = self
                            dx, dy = get_direction(i.x, self.x, i.y, self.y)
                            break
                self.x += dx*self.speed*dt
                self.y += dy*self.speed*dt
            else:
                for i in listOfCols:
                    if isinstance(i, Player):
                        if (time.time()-self.lastTimeDealtDamage) >= self.damageDelayTime:
                            i.deal_damage(self.damage)

                            self.lastTimeDealtDamage = time.time()

                    else:
                        ptcx, ptcy = get_direction(player.x, i.x, player.y, i.y)
                        self.x += ptcx*self.speed*dt
                        self.y += ptcy*self.speed*dt
                # self.x += -dx*self.speed*dt
                # self.y += -dy*self.speed*dt

    def update(self, dt):
        players = [i for i in Instance.listOfInstances if isinstance(i, Player)]
        players = {distance(self.x,i.x,self.y,i.y):i for i in players}
        if len(players) < 1:
            return
        self.target = players[min(set(list(players)))]
        player = self.target
        listOfCols = pygame.sprite.spritecollide(self, Player.listOfPlayers, False)
        for i in listOfCols:
            if isinstance(i, Player):
                if player.up:
                    if self.y < player.y and self.x-player.x < self.ix/1.5: # The less the number after "<" is, the more
                                                                            # the enemy is going to be pushed, set to 0
                                                                            # and then he can be push anywhere
                        self.y -= player.speed*dt
                if player.down:
                    if self.y > player.y and self.x-player.x < self.ix/1.5:
                        self.y += player.speed*dt
                if player.left:
                    if self.x < player.x and (self.y-player.y) < self.iy/2.5:
                        self.x -= player.speed*dt
                if player.right:
                    if self.x > player.x and (self.y-player.y) < self.iy/2.5:
                        self.x += player.speed*dt
                break
        if self.currentWeapon and player:
            dis = distance(self.x, player.x, self.y, player.y)
            if dis <= self.currentWeapon.maxDistance:
                self.currentWeapon.shoot((player.x, player.y))
            else:
                self.move_towards_player(self.target, dt)

        super().update(dt)


    def kill(self):
        if self in Enemy.listOfEnemies:
            Enemy.listOfEnemies.remove(self)
        super().kill()
