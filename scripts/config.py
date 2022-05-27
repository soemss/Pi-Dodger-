import pygame
import math
import time
import random
from pygame.locals import *
pygame.init()
pygame.font.init()

bg = pygame.image.load("assets/background.png")
enemyModel = ["assets/enemyRed.png", "assets/enemyWhite.png", "assets/enemyOrange.png"]
restartIco = pygame.image.load("assets/restartIco.png")
playIco = pygame.image.load("assets/playIco.png")
menuIco = pygame.image.load("assets/menuIco.png")
scoreboardIco = pygame.image.load("assets/scoreboard.png")
crashSound = pygame.mixer.Sound("assets/explosion.wav")
crashSound.set_volume(0.4)
font = pygame.font.Font("assets/arcade_font.TTF", 50)
menuTitle = font.render('Vehicle', False, (255, 255, 255))
menuTitle2 = font.render('Dodge', False, (255, 255, 255))
g = font.render("Game", False, (255, 0, 0))
over = font.render("Over", False, (255, 0, 0))
restartText = font.render("Retry", False, (0, 0, 0))
scoreText = font.render("Score", False, (255, 255, 255))
# font = pygame.font.Font("assets/arcade_font.TTF", 50)
# def calcAngle(self, playerX, playerY):
#     angle = math.atan2(-(playerY - self.rect.y), playerX - self.rect.x)
#     stepX = (math.cos(angle) * self.speed)
#     stepY = (math.sin(angle) * self.speed)
#     return stepX, stepY, angle

# def background():
# 	global scrollY
# 	screen.blit(bg, (0, scrollY))
# 	screen.blit(bg, (0, scrollY - 600))
# 	if scrollY >= 600:
# 			scrollY = 0
# 	else:
# 			scrollY += 15