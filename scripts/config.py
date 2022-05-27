import pygame
import math
import time
import random
from pygame.locals import *
pygame.font.init()

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