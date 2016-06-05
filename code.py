import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (34, 177, 76)
light_green = (0, 255, 0)
yellow = (255, 255, 0)

display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')

# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

pygame.display.update()

# snake_head_image = pygame.image.load('snake.png')
# apple_image = pygame.image.load('apple.png')

clock = pygame.time.Clock()

FPS = 15

block_size = 20
appleThickness = 30

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
		message_to_screen("Welcome to Tanks", green, y_displace = -100, size = "large")
		message_to_screen("The objective is to shoot and destroy", black, y_displace = -30)
		message_to_screen("the enemy tank before they destroy you.", black, y_displace = 10)
		message_to_screen("The more enemies you destroy, the harder it gets", black, y_displace = 50)
		# message_to_screen("Press C to play, P to pause or Q to quit.", black, y_displace = 180)
		
		cur = pygame.mouse.get_pos()
		if 150 + 100 > cur[0] > 150 and 500 + 50 > cur[1] > 500:
			pygame.draw.rect(gameDisplay, light_green, (150, 500, 100, 50))
		else:
			pygame.draw.rect(gameDisplay, green, (150, 500, 100, 50))
			
		pygame.draw.rect(gameDisplay, yellow, (350, 500, 100, 50))
		pygame.draw.rect(gameDisplay, red, (550, 500, 100, 50))
		
		text_to_button("Play", black, 150, 500, 100, 50)
		text_to_button("Controls", black, 350, 500, 100, 50)
		text_to_button("Quit", black, 550, 500, 100, 50)
		
		pygame.display.update()
		clock.tick(5)

def text_objects(text, color, size):
	if size == "small":
		textSurface = smallfont.render(text, True, color)
	elif size == "medium":
		textSurface = medfont.render(text, True, color)
	elif size == "large":
		textSurface = largefont.render(text, True, color)
	return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
	textSurf, textRect = text_objects(msg, color, size)
	textRect.center = (buttonx + (buttonwidth / 2)) , (buttony + (buttonheight / 2))
	gameDisplay.blit(textSurf, textRect)

def message_to_screen(msg, color, y_displace = 0, size = "small"):
	textSurf, textRect = text_objects(msg, color, size)
	textRect.center = (display_width / 2), (display_height / 2) + y_displace
	gameDisplay.blit(textSurf, textRect)

def gameLoop():	
	gameExit = False
	gameOver = False
	
	while not gameExit:
	
		if gameOver:
			message_to_screen("Game Over.", red, y_displace = -50, size = "large")
			message_to_screen("Press C to Continue, Q to quit.", black, y_displace = 50, size = "medium")
			pygame.display.update()
			
		while gameOver:
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
					pass
				elif event.key == pygame.K_RIGHT:
					pass
				elif event.key == pygame.K_UP:
					pass
				elif event.key == pygame.K_DOWN:
					pass
				elif event.key == pygame.K_p:
					pause()
		
		gameDisplay.fill(white)
		
		pygame.display.update()
		
		clock.tick(FPS)

	pygame.quit()
	quit()

gameIntro()
gameLoop()