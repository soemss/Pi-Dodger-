import pygame
import math
import time
import random
from pygame.locals import *

# from sense_hat import SenseHat
# import RTIMU

# sense = SenseHat()

# initialize variables

pygame.init()
pygame.font.init()
pygame.display.set_caption("Vehicle Dodger")
screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
font = pygame.font.Font("assets/arcade_font.TTF", 50)
clock = pygame.time.Clock()
startTicks = pygame.time.get_ticks()
timer_event = pygame.USEREVENT + 1
scrollY = 0
pygame.time.set_timer(timer_event, 1000)
bg = pygame.image.load("assets/background.png")
enemyModel = ["assets/enemyRed.png", "assets/enemyWhite.png", "assets/enemyOrange.png"]
crashSound = pygame.mixer.Sound("assets/explosion.wav")
fps = 30


def background():
    global scrollY
    screen.blit(bg, (0, scrollY))
    screen.blit(bg, (0, scrollY - 600))
    if scrollY >= 600:
        scrollY = 0
    else:
        scrollY += 15


mode = "raw"  # "bounded" or "raw"


# def getOrientation(mode):
#     orientation = sense.get_accelerometer_raw()
#     if mode == "bounded":
#         x = abs(orientation['x'])
#         y = abs(orientation['y'])
#         if x > 1:
#             x = 1
#         if x < 0:
#             x = 0
#         if y > 1:
#             y = 1
#         if y < 0:
#             y = 0
#     if mode == "raw":
#         x = (orientation['x'])
#         y = (orientation['y'])
#     info = [x, y]
#     return info


class Player(pygame.sprite.Sprite):
    # steerControl = getOrientation()

    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()

        self.image_new = self.image
        self.speed = 0.7
        self.velocity = pygame.math.Vector2(0, 0)
        self.steering = False

    # def control(self):
    #     steerControl = getOrientation("raw")
    #     steerX = steerControl[0]
    #     steerY = steerControl[1]

    def movement(self):
        steerX = 0
        steerY = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or steerX > 0:
            self.velocity.x -= self.speed
            print(steerX)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d] or steerX < 0:
            self.velocity.x += self.speed
            print(steerX)
        if keys[pygame.K_UP] or keys[pygame.K_w] or steerY > 0:
            self.velocity.y -= (self.speed * 3)
            print(steerY)
        if keys[pygame.K_DOWN] or keys[pygame.K_s] or steerY < 0:
            self.velocity.y += (self.speed * 2)
            print(steerY)
        if keys[pygame.K_SPACE]:
            if not self.steering:
                self.steering = True
            else:
                self.steering = False

    def update(self, dt):
        self.movement()
        # while self.steering:
        #     self.control

        self.image_new = pygame.transform.rotate(self.image, -self.velocity.x * 1.5)

        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

        # movement smoothing
        self.velocity.x *= .95
        self.velocity.y *= .9

        self.velocity.y += .24
        # collision
        if self.rect.x <= 10:
            self.rect.x = 10
            self.velocity.x += 1.1 * dt
        if self.rect.x >= 525:
            self.rect.x = 525
            self.velocity.x -= 1.1 * dt
        if self.rect.y <= 0:
            self.rect.y = 0
            self.velocity.y += 1.1 * dt
        if self.rect.y >= 550:
            self.rect.y = 550
            self.velocity.y -= 1.1 * dt
