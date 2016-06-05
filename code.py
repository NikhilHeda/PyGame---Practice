import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 155, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slither')

icon = pygame.image.load('apple.png')
pygame.display.set_icon(icon)

pygame.display.update()

snake_head_image = pygame.image.load('snake.png')
apple_image = pygame.image.load('apple.png')

clock = pygame.time.Clock()

FPS = 15

block_size = 20
appleThickness = 30

direction = "right"

smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 80)

def pause():
	paused = True
	
	message_to_screen("Paused", black, -100, size = 'large')
	message_to_screen("Press C to continue or Q to Quit", black, 25)
	pygame.display.update()
	
	while paused:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					paused = False
				elif event.key == pygame.K_q:
					pygame.quit()
					quit()				
		# gameDisplay.fill(white)

		clock.tick(5)
		
def score(score):
	text = smallfont.render("Score: " + str(score), True, black)
	gameDisplay.blit(text, [0, 0])

def gameIntro():
	intro = True
	
	while intro:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					intro = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()

		gameDisplay.fill(white)
		message_to_screen("Welcome to Slither", green, y_displace = -100, size = "large")
		message_to_screen("The objective is to eat apples", black, y_displace = -30)
		message_to_screen("The more apples you eat the longer you get !", black, y_displace = 10)
		message_to_screen("If you run into the edges, or yourself, you die !", black, y_displace = 50)
		message_to_screen("Press C to play, P to pause or Q to quit.", black, y_displace = 180)
		pygame.display.update()
		clock.tick(5)

def randAppleGen():
	randAppleX = round( random.randrange(0, display_width - appleThickness) ) # / 10.0 ) * 10 
	randAppleY = round( random.randrange(0, display_height - appleThickness) ) # / 10.0 ) * 10 
	return randAppleX, randAppleY

def snake(block_size, snakelist):
	
	if direction == "right":
		head = pygame.transform.rotate(snake_head_image, 270)
	elif direction == "left":
		head = pygame.transform.rotate(snake_head_image, 90)
	elif direction == "up":
		head = snake_head_image
	elif direction == "down":
		head = pygame.transform.rotate(snake_head_image, 180)
	
	gameDisplay.blit(head, (snakelist[-1][0], snakelist[-1][1]))
	
	for XnY in snakelist[:-1]:
		pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, color, size):
	if size == "small":
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)
	return textSurface, textSurface.get_rect()

def message_to_screen(msg, color, y_displace = 0, size = "small"):
	textSurf, textRect = text_objects(msg, color, size)
	textRect.center = (display_width / 2), (display_height / 2) + y_displace
	gameDisplay.blit(textSurf, textRect)

def gameLoop():
	global direction
	
	direction = "right"
	
	gameExit = False
	gameOver = False
	
	lead_x = display_width / 2
	lead_y = display_height / 2
	lead_x_change = 10
	lead_y_change = 0
	
	randAppleX, randAppleY = randAppleGen()

	snakeList = []
	snakeLength = 1
	
	while not gameExit:
	
		if gameOver:
			message_to_screen("Game Over.", red, y_displace = -50, size = "large")
			message_to_screen("Press C to Continue, Q to quit.", black, y_displace = 50, size = "medium")
			pygame.display.update()
			
		while gameOver:
			# gameDisplay.fill(white)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameExit = True
					gameOver = False
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_q:
						gameExit = True
						gameOver = False
					elif event.key == pygame.K_c:
						gameLoop()
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				gameExit = True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					direction = "left"
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					direction = "right"
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					direction = "up"
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					direction = "down"
					lead_y_change = block_size
					lead_x_change = 0
				elif event.key == pygame.K_p:
					pause()
		
		if lead_x >= display_width or lead_x < 0 or  lead_y >= display_height or lead_y < 0:
			gameOver = True
		
		lead_x += lead_x_change
		lead_y += lead_y_change
		
		gameDisplay.fill(white)
		
		gameDisplay.blit(apple_image, (randAppleX, randAppleY))
		
		snakeHead = []
		snakeHead.append(lead_x)
		snakeHead.append(lead_y)
		snakeList.append(snakeHead)
		
		if len(snakeList) > snakeLength:
			del snakeList[0]
			
		for eachSegment in snakeList[:-1]:
			if eachSegment == snakeHead:
				gameOver = True
		
		snake(block_size, snakeList)
		
		score(snakeLength - 1)
		
		pygame.display.update()
		
		if  randAppleX < lead_x < randAppleX + appleThickness or randAppleX < lead_x + block_size < randAppleX + appleThickness:
			if  randAppleY < lead_y < randAppleY + appleThickness or randAppleY < lead_y + block_size < randAppleY + appleThickness:
				snakeLength += 1
				randAppleX, randAppleY = randAppleGen()
		
		clock.tick(FPS)

	pygame.quit()
	quit()

gameIntro()
gameLoop()