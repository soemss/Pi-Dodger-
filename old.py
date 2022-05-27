import pygame
import math
import time
import random
from pygame.locals import *

from sense_hat import SenseHat
import RTIMU

sense = SenseHat()

# initialize variables
pygame.init()
pygame.font.init()
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

def getOrientation(mode):
    orientation = sense.get_accelerometer_raw()
    if mode == "bounded":
        x = abs(orientation['x'])
        y = abs(orientation['y'])
        if x > 1:
            x = 1
        if x < 0:
            x = 0
        if y > 1:
            y = 1
        if y < 0:
            y = 0
    if mode == "raw":
        x = (orientation['x'])
        y = (orientation['y'])
    info = [x, y]
    return info


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load("assets/player.png")
        self.rect = self.image.get_rect()

        self.image_new = self.image
        self.speed = 0.7
        self.velocity = pygame.math.Vector2(0, 0)
        self.steering = False

        

    def movement(self):
        steerControl = getOrientation("raw")
        steerX = steerControl[0]
        steerY = -steerControl[1]
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
        if self.rect.x >= 445:
            self.rect.x = 445
            self.velocity.x -= 1.1 * dt
        if self.rect.y <= 0:
            self.rect.y = 0
            self.velocity.y += 1.1 * dt
        if self.rect.y >= 550:
            self.rect.y = 550
            self.velocity.y -= 1.1 * dt

def calcAngle(self, playerX, playerY):
    angle = math.atan2(-(playerY - self.rect.y), playerX - self.rect.x)
    stepX = (math.cos(angle) * self.speed)
    stepY = (math.sin(angle) * self.speed)
    return stepX, stepY, angle

class Boss(pygame.sprite.Sprite):
	def __init__(self):
			super(Boss, self).__init__()
			self.image_boss = pygame.image.load("assets/boss.png")
			self.rect = self.image_boss.get_rect()
			self.rect.x = 280
			self.rect.y = 600
			self.speed = 5
			self.image_new = self.image_boss
			self.angle = 0
			self.ramming = False
			self.dt = None
			self.step = [0,0]
			self.rammingCounter = 0

	def ram_car(self, playerX, playerY):
		step = calcAngle(self, playerX, playerY)
		self.angle = step[2]
		self.step = [step[0], step[1]]
		print(math.degrees(self.angle))

	def control(self, x, y):
			self.rect.x += x * self.dt * 3
			self.rect.y -= y * self.dt * 3

	def update(self, dt, playerX, playerY, score):
		image = self.image_new
		self.dt = dt
		print (self.rect)
		print(self.rammingCounter)
		self.image_new = pygame.transform.rotozoom(self.image_boss, self.angle, 1)
		if self.ramming:
			if self.rammingCounter == 0:
				self.ram_car(playerX, playerY)
			self.rammingCounter += 1

		elif not math.isclose(self.rect.x, 280) and not math.isclose(self.rect.y, 500):
			self.rammingCounter = 0
			# step = calcAngle(self, 280, 500)
			# self.control(step[0], step[1])
			self.ram_car(280, 500)
			image = self.image_boss
		if not ((self.rect.x <= 290 and self.rect.x >= 270)and (self.rect.y <= 510 and self.rect.y >= 490)) or self.ramming:
			self.control(self.step[0], self.step[1])
		screen.blit(image, self.rect)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load(random.choice(enemyModel))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(75, 550)
        self.rect.y = -200
        self.speed = random.randrange(7, 11)

    def draw_enemy(self):
        screen.blit(self.image, self.rect)

    def update(self, dt):
        self.rect.y += self.speed * dt


def menu():
    click = False
    menuTitle = font.render('Vehicle', False, (255, 255, 255))
    menuTitle2 = font.render('Dodge', False, (255, 255, 255))
    playText = font.render('Play', False, (0, 0, 0))
    while True:
        background()
        screen.blit(menuTitle, (90, 100))
        screen.blit(menuTitle2, (140, 160))
        mouseX, mouseY = pygame.mouse.get_pos()
        startButton = pygame.Rect(150, 450, 200, 60)

        if startButton.collidepoint((mouseX, mouseY)):
            if click:
                game()
        pygame.draw.rect(screen, (255, 255, 255), startButton)
        screen.blit(playText, (startButton.x + 5, startButton.y + 5))
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.flip()



def gameOver():
    click = False
    g = font.render('Game ', False, (255, 0, 0))
    over = font.render("Over", False, (255, 0, 0))
    restartText = font.render("Retry", False, (0, 0, 0))
    while True:
        screen.blit(over, (160, 130))
        screen.blit(g, (160, 70))

        mouseX, mouseY = pygame.mouse.get_pos()
        restart = pygame.Rect(125, 460, 250, 60)

        if restart.collidepoint((mouseX, mouseY)):
            if click:
                game()
        pygame.draw.rect(screen, (255, 255, 255), restart)
        screen.blit(restartText, (restart.x + 8, restart.y + 7))
        click = False

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        pygame.display.flip()


def game():
    player = Player()

    gameSpeed = 30

    running = True
    player_list = pygame.sprite.Group()
    player_list.add(player)
    score = 0
    newTick = 0

    duration = 0

    player.rect.x = 210
    player.rect.y = 500

    enemies = []
    prev_time = time.time()

    while running:
        background()
        dt = time.time() - prev_time
        dt *= gameSpeed
        prev_time = time.time()
        startTicks = pygame.time.get_ticks()
        screen.blit(player.image_new, player.rect)
        # steerControl = getOrientation()

        if startTicks > newTick:
                enemies.insert(0, Enemy())
                newTick = startTicks + 2000
                if score == 20:
                        enemies.insert(0, Enemy())
                        newTick = startTicks + 1500
                        gameSpeed = 30
                if score == 35:
                        enemies.insert(0, Enemy())
                        gameSpeed = 40
                if score == 45:
                        gameSpeed = 45
    # if score % 10 == 0:
    # 	print("boss")
        
#         boss.update(dt, player.rect.x, player.rect.y)
            
        for count, enemy in enumerate(enemies):
                enemy.update(dt)
                enemy.draw_enemy()
                if player.rect.colliderect(enemy.rect):
                        print("crashed")
                        screen.blit(font.render(f"Score", False, (255, 255, 255)), (140, 225))
                        screen.blit(font.render(f"{score}", False, (255, 255, 255)), (225, 300))
                        gameOver()
                        pygame.mixer.Sound.play(crashSound)
                        running = False
                if enemy.rect.y > 600:
                        del enemies[count]
                        break

        # Ends program when x is pressed
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                        running = False
                elif event.type == timer_event:
                        score += 1
                        print(score)
        # updates positions
        screen.blit(font.render(f"{score}", False, (255, 255, 255)), (50, 25))
        player.update(dt)
        pygame.display.flip()
        # clock.tick(30)


menu()

