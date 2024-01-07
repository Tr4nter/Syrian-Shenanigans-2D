import pygame
import sys

from pygame.locals import QUIT
from Beings.Instances import Instance
from Beings.Player import Player
from Beings.Enemy import Enemy
from Tools.Weapon import Weapon
from Layout.LayoutStuff import Layout
from Tools.Pickup import PickupItem
import random as ra
import math

DEBUG = False
clock = pygame.time.Clock()

pygame.init()
pygame.font.init()
if not DEBUG:
    DISPLAYSURF = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
else:
    DISPLAYSURF = pygame.display.set_mode((600, 400))

# gameState

isMouseDown = False
isEndless = False
isClassic = False
isStarted = False
isMenuOn = False
isStartActions = False
isDead = False
isPause = False
spawningWithGunChance = 0.25
textConfig = {"font": "dejavusans",
              "appearanceTime": 3,
              "fontSize": 15,
              "colour": (255, 255, 255)}
pausedLay = None
fps = 0
chancesOfMultiplying = 0.10
WASD = [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]
allowedInput = {"movementKeys": WASD,
                "spawnNewEnemy": pygame.K_f,
                "dropWeapon": pygame.K_q,
                "changeEquipSlot": [pygame.K_1, pygame.K_2, pygame.K_3],
                "pause": pygame.K_p}

x, y = DISPLAYSURF.get_size()

# Weapons
Weapons = {}
PistolConf = {
    "bullet_sprite": "Weapons/Pistol/bullet.png",
    "degree": 90,
    "rateOfFire": 120,
    "spread": 0,
    "maxDistance": 1000,
    "minDamage": 45 if not DEBUG else 999,
    "maxDamage": 55 if not DEBUG else 1000,
    "speed": 300,
    "name": "Pistol"}
Weapons["Pistol"] = lambda: Weapon(
    "Weapons/Pistol/Pistol.png", 0, 0, DISPLAYSURF, **PistolConf)

RifleConf = PistolConf.copy()
RifleConf["bullet_sprite"] = "Weapons/Rifle/bullet.png"
RifleConf["rateOfFire"] = 860
RifleConf["minDamage"] = 35
RifleConf["maxDamage"] = 60
RifleConf["speed"] = 500
RifleConf["name"] = "Rifle"
RifleConf["spread"] = 8

Weapons["Rifle"] = lambda: Weapon(
    "Weapons/Rifle/Rifle.png", 0, 0, DISPLAYSURF, **RifleConf)
pygame.display.set_caption('Syrian Shenanigans 2D')
icon = pygame.image.load("enemy.png")
pygame.display.set_icon(icon)

running = True


def spawnEnemy():
    per = ra.random()
    enemy = Enemy("enemy.png", 999, 999, DISPLAYSURF)
    enemy.x = ra.randint(0, x-enemy.ix)
    enemy.y = ra.randint(0, y-enemy.iy*2)
    if per <= spawningWithGunChance:
        w = Weapons["Pistol"]()
        w.spread = 10 # otherwise they would be too accurate
        w.projectTileSpeed=1000
        w.rateOfFire = 30
        w.maxDistance = 500
        w.name = "ePistol"
        enemy.equip(w, 1)


# kill Count related
enemyCount = 0
scoreCount = pygame.font.SysFont("dejavusans", 16)
lastCount = 0
# healt related
healthCount = pygame.font.SysFont("dejavusans", 16)



listOfPotions = ["Healing Potion", "Speed Potion", "Damage Potion"]


def healingPotionPickup(self, player):
    player.health += 50
    return True


def speedPotionPickup(self, player):
    player.speed += 20
    return True


def damagePotionPickup(self, player):
    if player.currentWeapon:
        player.currentWeapon.minDamage += 10
        player.currentWeapon.maxDamage += 10
        return True
    else:
        return False


def spawnItem(picture, name, onPickup):
    item = PickupItem(picture, 0, 0, DISPLAYSURF, name)
    item.x = ra.randint(0, x - item.ix)
    item.y = ra.randint(0, y - (item.iy * 2))
    item.onPickup = onPickup


def Start():
    player = Player("player.png", 9999, 9999, DISPLAYSURF)
    player.health = 200
    player.equip(Weapons["Rifle"](), 1)
    player.equip(Weapons["Pistol"](), 2)
    player.x = ra.randint(player.ix, x-player.ix)
    player.y = ra.randint(player.iy*2, y-(player.iy*2))
    elText = f"Chances of enemies multiplying on killed: {int(chancesOfMultiplying*100)}%"
    elTextConf = textConfig.copy()
    elTextConf["appearanceTime"] = math.inf
    elTextConf["colour"] = (0, 0, 0)
    elTextConf["description"] = "Chance"
    elTextConf["align"] = "topright"
    Layout(0, y*0.03, DISPLAYSURF, elText, **elTextConf)
    elTextConf['description'] = "FramePerSec"
    Layout(0, y*0.06, DISPLAYSURF, f"FPS: {int(fps)}", **elTextConf)
    elTextConf["description"] = "EnemiesCount"
    Layout(0, y*0.01, DISPLAYSURF,
           f"Amount of enemies killed: {str(enemyCount)}", **elTextConf)


def Menu():
    global isStarted
    global isMenuOn
    global isDead
    isMenuOn = True
    menuConfig = textConfig.copy()
    menuConfig["appearanceTime"] = math.inf
    menuConfig["description"] = "Menu buttons"
    menuConfig["colour"] = (0, 0, 0)
    menuConfig["align"] = "center"
    # Text
    bigTextConfig = menuConfig
    bigTextConfig["fontSize"] = 32
    Layout(0, y*0.30, DISPLAYSURF, "Syrian Shenanigans 2D", **bigTextConfig)

    # Classic
    buttonConfig = bigTextConfig
    buttonConfig["fontSize"] = 24
    buttonConfig["colour"] = (0, 255, 0)
    buttonConfig["align"] = "center"
    classicButton = Layout(0, y*0.45, DISPLAYSURF, "Play", **buttonConfig)
    global isClassic

    def classic(self):
        global isClassic
        global isStarted
        isClassic = True
        isStarted = True
    classicButton.onClicked = classic


percentageAdded = 0
while True:
    if not isMenuOn and not isStarted:
        Menu()
        player = None

    if isStarted:
        if isMenuOn:
            listOfCraps = [
                i for i in Layout.listOfLayouts if i.description and i.description == "Menu buttons"]
            for i in listOfCraps:
                Layout.remove(i)
            isMenuOn = False
        if not isStartActions:
            for i in range(5 if not DEBUG else 0):
                spawnEnemy()
            Start()
            isStartActions = True
        if len(Player.listOfPlayers) > 0:
            player = Player.listOfPlayers[0]
        else:
            isDead = True

    if isDead:
        for i in Instance.listOfInstances:
            Instance.listOfInstances.remove(i)
            i.kill()
        for i in Layout.listOfLayouts:
            Layout.remove(i)

        lastCount = 0
        if len(Instance.listOfInstances) == 0:
            isDead = False
            isEndless = False
            isClassic = False
            isStarted = False
            isStartActions = False
            enemyCount = 0
            chancesOfMultiplying = 0.10
            percentageAdded = 0

    DISPLAYSURF.fill((112, 128, 144))
    dt = clock.tick()/1000
    differenceInECount = lastCount-len(Enemy.listOfEnemies)
    if differenceInECount > 0:
        enemyCount += differenceInECount
        if ra.random() < chancesOfMultiplying:
            differenceInECount *= 2
        if enemyCount % 5 == 0:
            percentageToAdd = (enemyCount/5/10/10)
            chancesOfMultiplying += percentageToAdd-percentageAdded
            percentageAdded = percentageToAdd
        if enemyCount % 10 == 0:
            choice = ra.choice(listOfPotions)
            if choice == "Healing Potion":
                spawnItem("Pickups/healingpotion.png",
                          "Healing Potion", healingPotionPickup)
            elif choice == "Speed Potion":
                spawnItem("Pickups/speedpotion.png",
                          "Speed Potion", speedPotionPickup)
            elif choice == "Damage Potion":
                spawnItem("Pickups/damagepotion.png",
                          "Damage Potion", damagePotionPickup)

        for i in range(differenceInECount):
            spawnEnemy()
    lastCount = len(Enemy.listOfEnemies)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            if event.key in allowedInput["movementKeys"] or event.key in allowedInput["changeEquipSlot"]:
                if player:

                    player.keyChange("down" if event.type ==
                                     pygame.KEYDOWN else "up", event.key)
            if event.type == pygame.KEYDOWN:
                if event.key == allowedInput["spawnNewEnemy"] and not isEndless:
                    spawnEnemy()
                elif event.key == allowedInput["dropWeapon"]:
                    player.drop()

            if event.key == allowedInput["pause"] and event.type == pygame.KEYDOWN:
                isPause = not isPause
                Instance.isPaused = isPause
                if not isPause:
                    Layout.remove(pausedLay)
                else:
                    conf = textConfig.copy()
                    conf["appearanceTime"] = math.inf
                    conf["colour"] = (255, 0, 0)
                    conf["description"] = "Paused"
                    conf["align"] = "center"
                    conf["fontSize"] = 32
                    pausedLay = Layout(0, y*0.35, DISPLAYSURF, "Paused", **conf)
                    # pygame.display.update()
        if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP:
            isLeftclicked = pygame.mouse.get_pressed()[0]
            if isLeftclicked:

                for i in Layout.listOfLayouts:
                    if i.onClicked:
                        if i.is_clicked(pygame.mouse.get_pos()):
                            i.click()
                isMouseDown = True
            else:
                isMouseDown = False

    for t in Layout.listOfLayouts:
        if t.description == "Chance":
            t.textContent = f"Chances of enemies multiplying on killed: {int(chancesOfMultiplying*100)}%"
        if t.description == "FramePerSec":
            t.textContent = f"FPS: {int(fps)}"
        if t.description == "EnemiesCount":
            t.textContent = f"Amount of enemies killed: {str(enemyCount)}"
        t.update()

    if isStarted and player:
        healthLabel = healthCount.render(
            f"Health: {player.health}", True, (255, 0, 0))
        DISPLAYSURF.blit(healthLabel, (0, 0))

    if not running:
        pygame.quit()
        sys.exit()
    if isPause:
        pygame.display.update()
        continue

    # player controller
    if isStarted and player and not isPause:
        if player.up:
            player.y -= player.speed*dt
        if player.down:
            player.y += player.speed*dt

        if player.left:
            player.x -= player.speed*dt

        if player.right:
            player.x += player.speed*dt

        if isMouseDown:
            if player.currentWeapon:
                player.currentWeapon.shoot(pygame.mouse.get_pos())


    # Update
    for i in Instance.listOfInstances:

        if isinstance(i, Weapon):
            i.update_to_parent()
            i.update_projectiles(dt, Enemy.listOfEnemies+Player.listOfPlayers)

        elif isinstance(i, Enemy):
            if not i.currentWeapon:
                i.move_towards_player(player, dt)
            for tl in i.textList:
                txtsurf = tl.copy()
                text_alpha = pygame.Surface(
                    txtsurf.get_size(), pygame.SRCALPHA)

                text_alpha.fill((255, 255, 255, int(i.textList[tl]["alpha"])))
                txtsurf.blit(text_alpha, (0, 0),
                             special_flags=pygame.BLEND_RGBA_MULT)
                DISPLAYSURF.blit(txtsurf, (i.x, i.y-i.textList[tl]["pos"]))

        i.update(dt)

    fps = clock.get_fps()
    pygame.display.update()
