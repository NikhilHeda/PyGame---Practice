import pygame

pygame.init()

red = (255, 0, 0)
white = (255, 255, 255)
black = (0, 0, 0)

gameDisplay = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Slither')

pygame.display.update()

gameExit = False

while not gameExit:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			gameExit = True
			
	gameDisplay.fill(white)
	pygame.draw.rect(gameDisplay, black, [400, 300, 10, 10])
	# gameDisplay.fill(red, rect = [30, 30, 100, 100])
	pygame.display.update()
		
pygame.quit()
quit()