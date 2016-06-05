import pygame

pygame.init()

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Slither')

pygame.display.update()

gameExit = False
lead_x = 300
lead_y = 300
lead_x_change = 0

clock = pygame.time.Clock()
FPS = 30

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				lead_x_change = -10
			if event.key == pygame.K_RIGHT:
				lead_x_change = 10

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				lead_x_change = 0

	lead_x += lead_x_change
	gameDisplay.fill(white)
	pygame.draw.rect(gameDisplay, black, [lead_x, lead_y, 10, 10])
	pygame.display.update()
	
	clock.tick(FPS)

pygame.quit()
quit()