import pygame
import math
import time
import random
from pygame.locals import *
from scripts.config import *
# from scripts.ui import *

# from sense_hat import SenseHat
# import RTIMU

# sense = SenseHat()

# initialize variables
screenWidth = 600
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
clock = pygame.time.Clock()
startTicks = pygame.time.get_ticks()
timer_event = pygame.USEREVENT + 1
scrollY = 0
pygame.time.set_timer(timer_event, 1000)
fps = 30

mode = "raw"  # "bounded" or "raw"

# def getOrientation(mode):
# 	orientation = sense.get_accelerometer_raw()
# 	if mode == "bounded":
# 			x = abs(orientation['x'])
# 			y = abs(orientation['y'])
# 			if x > 1:
# 					x = 1
# 			if x < 0:
# 					x = 0
# 			if y > 1:
# 					y = 1
# 			if y < 0:
# 					y = 0
# 	if mode == "raw":
# 			x = (orientation['x'])
# 			y = (orientation['y'])
# 	info = [x, y]
# 	return info

def touchingPos (x1, x2, y1, y2):
	return ((x1 <= x2 + 40 and x1 >= x2 - 40) and (y1 <= y2 + 60 and y1>= y2 - 10))
def calcAngle(self, playerX, playerY):
    angle = math.atan2(-(playerY - self.rect.y), playerX - self.rect.x)
    stepX = (math.cos(angle) * self.speed)
    stepY = (math.sin(angle) * self.speed)
    return stepX, stepY, angle

def background():
	global scrollY
	screen.blit(bg, (0, scrollY))
	screen.blit(bg, (0, scrollY - 600))
	if scrollY >= 600:
			scrollY = 0
	else:
			scrollY += 15
		
class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__()
		self.image = pygame.image.load("assets/player.png")
		self.rect = self.image.get_rect()

		self.image_new = self.image
		self.speed = 0.7
		self.velocity = pygame.math.Vector2(0, 0)
		self.steering = False
		self.rect.x = 250
		self.rect.y = 400
	def movement(self):
		# steerControl = getOrientation("raw")
		# steerX = steerControl[0]
		# steerY = -steerControl[1]

		# Below only needed for non rasp pi version
		steerX = 0
		steerY = 0 
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT] or keys[pygame.K_a] or steerX > 0:
				self.velocity.x -= self.speed
		if keys[pygame.K_RIGHT] or keys[pygame.K_d] or steerX < 0:
				self.velocity.x += self.speed
		if keys[pygame.K_UP] or keys[pygame.K_w] or steerY > 0:
				self.velocity.y -= (self.speed * 3)
		if keys[pygame.K_DOWN] or keys[pygame.K_s] or steerY < 0:
				self.velocity.y += (self.speed * 2)
		if keys[pygame.K_SPACE]:
				if not self.steering:
						self.steering = True
				else:
						self.steering = False
									
	def update(self, dt):
			self.movement()
			self.image_new = pygame.transform.rotate(self.image, -self.velocity.x * 1.5)
			screen.blit(self.image_new, self.rect)
			self.rect.x += round(self.velocity.x) * dt
			self.rect.y += round(self.velocity.y) * dt

			# movement smoothing
			self.velocity.x *= .95
			self.velocity.y *= .9

			self.velocity.y += .24
			# collision
			if self.rect.x <= 10:
					self.rect.x = 10
					self.velocity.x += 1.1 * dt
			if self.rect.x >= 545:
					self.rect.x = 545
					self.velocity.x -= 1.1 * dt
			if self.rect.y <= 0:
					self.rect.y = 0
					self.velocity.y += 1.1 * dt
			if self.rect.y >= 550:
					self.rect.y = 550
					self.velocity.y -= 1.1 * dt


class Boss(pygame.sprite.Sprite):
	def __init__(self):
			super(Boss, self).__init__()
			self.name = "Boss"
			self.image_boss = pygame.image.load("assets/boss.png")
			self.rect = self.image_boss.get_rect()
			self.rect.x = 280
			self.rect.y = 600
			self.speed = 3
			self.image_new = self.image_boss
			self.angle = 0
			self.ramming = False
			self.dt = None
			self.step = [0,0]
			self.rammingCounter = 0
			self.stopX = 0
			self.stopY = 0
			self.appearance = [280,600]
			self.moving = True
			self.swerveCounter = 0
	def ram_car(self, playerX, playerY):
		step = calcAngle(self, playerX, playerY)
		self.angle = step[2]
		self.step = [step[0], step[1]]

	def control(self, x, y):
		self.rect.x += x * self.dt * self.speed
		self.rect.y -= y * self.dt * self.speed
		self.speed += .1
	
	def update(self, dt, playerX, playerY):
		if self.swerveCounter % 2 == 0:
			self.rect.x += 1
			self.speed += .1
		else:
			self.rect.x -= 1
			self.speed -= .1
		
		image = self.image_new
		self.dt = dt

		self.image_new = pygame.transform.rotozoom(self.image_boss, self.step[0] * self.speed * -1.5, 1)
		if self.ramming:
			if self.rammingCounter == 0:
				self.stopX = playerX
				self.stopY = playerY
				self.ram_car(self.stopX, self.stopY)
				self.speed = 0
			self.rammingCounter = 1
		elif not math.isclose(self.rect.x, 280) and not math.isclose(self.rect.y, 500):
			self.rammingCounter = 0
			
			self.swerveCounter += 1
		
			self.ram_car(self.appearance[0], self.appearance[1])
			image = self.image_boss
		# print (touchingPos(self.rect.x, self.stopX, self.rect.y, self.stopY))
		# print (self.stopX, self.stopY)
		# print (self.rect)

		if self.ramming and touchingPos(self.rect.x, self.stopX, self.rect.y, self.stopY):
				self.moving = False
				self.ramming = False
		elif touchingPos(self.rect.x, self.appearance[0],self.rect.y,self.appearance[1]) and not self.ramming:
			self.moving = False
		else:
			self.moving = True
		if self.moving:
			self.control(self.step[0], self.step[1])
		
		screen.blit(image, self.rect)


class Enemy(pygame.sprite.Sprite):
	def __init__(self):
			super(Enemy, self).__init__()
			self.name = "Enemy"
			self.image = pygame.image.load(random.choice(enemyModel))
			self.rect = self.image.get_rect()
			self.rect.x = random.randrange(75, 425)
			self.rect.y = -200
			self.speed = random.randrange(7, 11)

	def update(self, dt, playerX, playerY):
			self.rect.y += self.speed * dt
			screen.blit(self.image, self.rect)

def menu():
	
	click = False
	while True:
		background()
		screen.blit(menuTitle, (screenWidth / 2 - menuTitle.get_width() / 2, 100))
		screen.blit(menuTitle2, (screenWidth / 2 - menuTitle2.get_width() / 2, 160))
		mouse = pygame.mouse.get_pos()
		startButton = pygame.Rect(screenWidth / 2 - 50, 450, 200, 60)

		if startButton.collidepoint((mouse[0], mouse[1])):
			if click:
					game()
		screen.blit(playIco, (screenWidth / 2 - 50, 450))
		# pygame.draw.rect(screen, (255, 255, 255), startButton)
		# screen.blit(playText, (startButton.centerx - playText.get_width() / 2, startButton.y + 5))

		for event in pygame.event.get():
				if event.type == QUIT:
						pygame.quit()
				if event.type == MOUSEBUTTONDOWN:
						if event.button == 1:
								click = True
		pygame.display.flip()



def gameOver():
	click = False
	while True:
		screen.blit(over, (screenWidth / 2 - over.get_width() / 2, 130))
		screen.blit(g, (screenWidth / 2 - g.get_width() / 2, 70))

		mouse = pygame.mouse.get_pos()
		restartButton = pygame.Rect(screenWidth / 2 + 50, 460, 250, 60)
		menuButton = pygame.Rect(screenWidth / 2 - 150, 460, 250, 60)
		if restartButton.collidepoint((mouse[0], mouse[1])):
				if click:
						game()
		if menuButton.collidepoint((mouse[0], mouse[1])):
				if click:
						menu()
		screen.blit(restartIco, (screenWidth / 2 + 50, 460))
		screen.blit(menuIco, (screenWidth / 2 - 150, 460))
		# pygame.draw.rect(screen, (255, 255, 255), restart)
		# screen.blit(restartText, (restart.centerx - restartText.get_width() / 2, restart.y + 7))
		click = False

		for event in pygame.event.get():
				if event.type == QUIT:
						pygame.quit()
				if event.type == MOUSEBUTTONDOWN:
						if event.button == 1:
								click = True
		pygame.display.flip()  


def game():
	gameSpeed = 30
	running = True
	score = 0
	newTick = 0
	
	player = Player()
	player_list = pygame.sprite.Group()
	player_list.add(player)
	enemies = []
	boss = Boss()
	enemies.insert(0, boss)
	# cooldown = 0

	prev_time = time.time()

	while running:
			# print (player.rect)
			background()
			dt = time.time() - prev_time
			dt *= gameSpeed
			prev_time = time.time()
			startTicks = pygame.time.get_ticks()
			print(f"fps {gameSpeed}")
			# steerControl = getOrientation()
			if startTicks > newTick:
					enemies.insert(0, Enemy())
					newTick = startTicks + 2000
					if score % 15 == 0 and score > 0:
							enemies.insert(0, Enemy())
							newTick = startTicks + 1500
							gameSpeed += 10
						
			# if score > 9:
			if score % 10 == 0:
				boss.ramming = True

			# enemy collision
			for count, enemy in enumerate(enemies):
					enemy.update(dt, player.rect.x, player.rect.y)
					if player.rect.colliderect(enemy.rect):
							screen.blit(scoreboardIco, (screenWidth / 2 - scoreboardIco.get_width() / 2, 40))
							scoreValue = font.render(str(score), False, (255, 255, 255))
							screen.blit(scoreText, (screenWidth / 2 - scoreText.get_width() / 2, 245))						
							screen.blit(scoreValue, (screenWidth / 2 - scoreValue.get_width() / 2, 305))
							pygame.mixer.Sound.play(crashSound)
							gameOver()
							running = False
					if enemy.rect.y > 600 and enemy.name == "Enemy":
							del enemies[count]
							break
			# Ends program when x is pressed
			for event in pygame.event.get():
					if event.type == pygame.QUIT:
							running = False
					elif event.type == timer_event:
							score += 1
			# update functions
			screen.blit(font.render(str(score), False, (255, 255, 255)), (50, 25))
			print (player.rect.x, player.rect.y)
			player.update(dt)
			# boss.update(dt, player.rect.x, player.rect.y)
			pygame.display.flip()
			clock.tick(30)

menu()
