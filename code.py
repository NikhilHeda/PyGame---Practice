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
pygame.display.update()

snake_head_image = pygame.image.load('snake.png')

clock = pygame.time.Clock()

FPS = 15

block_size = 20

font = pygame.font.SysFont(None, 25)

def snake(block_size, snakelist):
	
	gameDisplay.blit(snake_head_image, (snakelist[-1][0], snakelist[-1][1]))
	
	for XnY in snakelist[:-1]:
		pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], block_size, block_size])

def text_objects(text, color):
	textSurface = font.render(text, True, color)
	return textSurface, textSurface.get_rect()
		
def message_to_screen(msg, color):
	# screen_text = font.render(msg, True, color)
	# gameDisplay.blit(screen_text, [display_width / 2, display_height / 2])
	textSurf, textRect = text_objects(msg, color)
	textRect.center = (display_width / 2), (display_height / 2)
	gameDisplay.blit(textSurf, textRect)

def gameLoop():
	gameExit = False
	gameOver = False
	
	lead_x = display_width / 2
	lead_y = display_height / 2
	lead_x_change = 0
	lead_y_change = 0
	
	randAppleX = round( random.randrange(0, display_width - block_size) ) # / 10.0 ) * 10 
	randAppleY = round( random.randrange(0, display_height - block_size) ) # / 10.0 ) * 10 

	snakeList = []
	snakeLength = 1
	
	while not gameExit:
	
		while gameOver:
			gameDisplay.fill(white)
			message_to_screen("Press C to Continue, Q to quit.", red)
			pygame.display.update()
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
					lead_x_change = -block_size
					lead_y_change = 0
				elif event.key == pygame.K_RIGHT:
					lead_x_change = block_size
					lead_y_change = 0
				elif event.key == pygame.K_UP:
					lead_y_change = -block_size
					lead_x_change = 0
				elif event.key == pygame.K_DOWN:
					lead_y_change = block_size
					lead_x_change = 0
		
		if lead_x >= display_width or lead_x < 0 or  lead_y >= display_height or lead_y < 0:
			gameOver = True
		
		lead_x += lead_x_change
		lead_y += lead_y_change
		
		gameDisplay.fill(white)
		
		appleThickness = 30
		pygame.draw.rect(gameDisplay, red, [randAppleX, randAppleY, appleThickness, appleThickness])
		
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
		
		pygame.display.update()
		
		'''
		if lead_x == randAppleX and lead_y == randAppleY:
			snakeLength += 1
			randAppleX = round( random.randrange(0, display_width - block_size) / 10.0 ) * 10 
			randAppleY = round( random.randrange(0, display_height - block_size) / 10.0 ) * 10 
		'''
		
		'''
		if  randAppleX <= lead_x <= randAppleX + appleThickness:
			if  randAppleY <= lead_y <= randAppleY + appleThickness:
				snakeLength += 1
				randAppleX = round( random.randrange(0, display_width - block_size) )# / 10.0 ) * 10 
				randAppleY = round( random.randrange(0, display_height - block_size) )# / 10.0 ) * 10 
		'''
		
		if  randAppleX < lead_x < randAppleX + appleThickness or randAppleX < lead_x + block_size < randAppleX + appleThickness:
			if  randAppleY < lead_y < randAppleY + appleThickness or randAppleY < lead_y + block_size < randAppleY + appleThickness:
				snakeLength += 1
				randAppleX = round( random.randrange(0, display_width - block_size) ) # / 10.0 ) * 10 
				randAppleY = round( random.randrange(0, display_height - block_size) ) # / 10.0 ) * 10 
				
		clock.tick(FPS)

	pygame.quit()
	quit()

gameLoop()