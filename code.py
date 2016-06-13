import pygame
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

red = (200, 0, 0)
light_red = (255, 0, 0)

green = (34, 177, 76)
light_green = (0, 255, 0)

yellow = (200, 200, 0)
light_yellow = (255, 255, 0)

display_width = 800
display_height = 600

ground_height = 35

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Tanks')

# icon = pygame.image.load('apple.png')
# pygame.display.set_icon(icon)

pygame.display.update()

# snake_head_image = pygame.image.load('snake.png')
# apple_image = pygame.image.load('apple.png')

clock = pygame.time.Clock()

FPS = 15

tankWidth = 40
tankHeight = 20

turretWidth = 5
wheelWidth = 5

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
		
		button("Play", 150, 500, 100, 50, green, light_green, action = "play")
		button("Controls", 350, 500, 100, 50, yellow, light_yellow, action = "controls")
		button("Quit", 550, 500, 100, 50, red, light_red, action = "quit")
		
		pygame.display.update()
		clock.tick(5)
		
def gameControls():
	gcont = True
	
	while gcont:
	
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		gameDisplay.fill(white)
		message_to_screen("Controls", green, y_displace = -100, size = "large")
		message_to_screen("Fire: Spacebar", black, y_displace = -30)
		message_to_screen("Move Turret: Up and Down arrows", black, y_displace = 10)
		message_to_screen("Move Tank: Left and Right arrows", black, y_displace = 50)
		message_to_screen("Pause: P", black, y_displace = 90)
		
		button("Play", 150, 500, 100, 50, green, light_green, action = "play")
		button("Main", 350, 500, 100, 50, yellow, light_yellow, action = "main")
		button("Quit", 550, 500, 100, 50, red, light_red, action = "quit")
		
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

def button(text, x, y, width, height, inactive_color, active_color, action = None):
	cur = pygame.mouse.get_pos()
	click = pygame.mouse.get_pressed()
	
	if x + width > cur[0] > x and y + height > cur[1] > y:
		pygame.draw.rect(gameDisplay, active_color, (x, y, width, height))
		if click[0] == 1 and action != None:
			if action == "quit":
				pygame.quit()
				quit()
			elif action == "controls":
				gameControls()
			elif action == "play":
				gameLoop()
			elif action == "main":
				gameIntro()
	else:
		pygame.draw.rect(gameDisplay, inactive_color, (x, y, width, height))
	
	text_to_button(text, black, x, y, width, height)

def tank(x, y, turPos):
	x = int(x)
	y = int(y)
	
	possibleTurrets = [ (x - 27, y - 2),
						(x - 26, y - 5),
						(x - 25, y - 8),
						(x - 23, y - 12),
						(x - 20, y - 14),
						(x - 18, y - 15),
						(x - 15, y - 17),
						(x - 13, y - 19),
						(x - 11, y - 21)
						]
	
	pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight / 2))
	pygame.draw.rect(gameDisplay, black, (x - tankHeight, y, tankWidth, tankHeight))
	
	pygame.draw.line(gameDisplay, black, (x, y), possibleTurrets[turPos], turretWidth)

	startX = int(tankWidth / 2) - wheelWidth
	for _ in range(7):
		pygame.draw.circle(gameDisplay, black, (x - startX, y + tankHeight), wheelWidth)
		startX -= wheelWidth
	
	return possibleTurrets[turPos]

def enemy_tank(x, y, turPos):
	x = int(x)
	y = int(y)
	
	possibleTurrets = [ (x + 27, y - 2),
						(x + 26, y - 5),
						(x + 25, y - 8),
						(x + 23, y - 12),
						(x + 20, y - 14),
						(x + 18, y - 15),
						(x + 15, y - 17),
						(x + 13, y - 19),
						(x + 11, y - 21)
						]
	
	pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight / 2))
	pygame.draw.rect(gameDisplay, black, (x - tankHeight, y, tankWidth, tankHeight))
	
	pygame.draw.line(gameDisplay, black, (x, y), possibleTurrets[turPos], turretWidth)

	startX = int(tankWidth / 2) - wheelWidth
	for _ in range(7):
		pygame.draw.circle(gameDisplay, black, (x - startX, y + tankHeight), wheelWidth)
		startX -= wheelWidth
	
	return possibleTurrets[turPos]
  
def barrier(xlocation, randomHeight, barrier_width):
	pygame.draw.rect(gameDisplay, black, [xlocation, display_height - randomHeight, barrier_width, randomHeight])
	
def explosion(x, y, size = 50):
	explode = True
	
	while explode:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
				
		startPoint = x, y
		
		colorChoices = [red, light_red, yellow, light_yellow]
		
		magnitude = 1
		
		while magnitude < size:
			exploding_bit_x = x + random.randrange(-1*magnitude, magnitude)
			exploding_bit_y = y + random.randrange(-1*magnitude, magnitude)
			pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0, 4)], (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
			magnitude += 1
			
			pygame.display.update()
			clock.tick(100)
			
		explode = False

def	fireShell(xy, tankx, tanky, turPos, gun_power, x_location, barrier_width, randomHeight, enemyTankX, enemyTankY):
	damage = 0
	
	fire = True
	startingShell = list(xy)
	
	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
		
		startingShell[0] -= (10 - turPos) * 2
		
		# y = x ** 2
		startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (gun_power / 50)) ** 2) - (turPos + turPos / (12 - turPos)) )
		
		check_x_1 = startingShell[0] <= x_location + barrier_width
		check_x_2 = startingShell[0] >= x_location
		
		check_y_1 = startingShell[1] <= display_height
		check_y_2 = startingShell[1] >= display_height - randomHeight
		
		if startingShell[1] > display_height - ground_height:
			hit_x = int(startingShell[0] * (display_height - ground_height) / startingShell[1])
			hit_y = int(display_height - ground_height)
			if enemyTankX + 15 > hit_x > enemyTankX - 15:
				damage = 25
			explosion(hit_x, hit_y)
			fire = False
			
		if (check_x_1 and check_x_2 and check_y_1 and check_y_2):
			hit_x = int(startingShell[0])
			hit_y = int(startingShell[1])
			explosion(hit_x, hit_y)
			fire = False

		pygame.display.update()
		
		clock.tick(100)
	return damage

def	e_fireShell(xy, tankx, tanky, turPos, gun_power, x_location, barrier_width, randomHeight, ptankX, ptankY):
	
	damage = 0
	
	currentPower = 1
	power_found = False
	
	while not power_found:
		currentPower += 1
		fire = True
		
		startingShell = list(xy)
		
		while fire:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			#pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
			
			startingShell[0] += (10 - turPos) * 2
			
			# y = x ** 2
			startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (currentPower / 50)) ** 2) - (turPos + turPos / (12 - turPos)) )
			
			check_x_1 = startingShell[0] <= x_location + barrier_width
			check_x_2 = startingShell[0] >= x_location
			
			check_y_1 = startingShell[1] <= display_height
			check_y_2 = startingShell[1] >= display_height - randomHeight
			
			if startingShell[1] > display_height - ground_height:
				hit_x = int(startingShell[0] * (display_height - ground_height) / startingShell[1])
				hit_y = int(display_height - ground_height)
				#explosion(hit_x, hit_y)
				if ptankX + 15 > hit_x > ptankX - 15:
					power_found = True
				fire = False
				
			if (check_x_1 and check_x_2 and check_y_1 and check_y_2):
				hit_x = int(startingShell[0])
				hit_y = int(startingShell[1])
				#explosion(hit_x, hit_y)
				fire = False

	
	fire = True
	startingShell = list(xy)
	
	while fire:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
		pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
		
		startingShell[0] += (10 - turPos) * 2
		
		# y = x ** 2
		startingShell[1] += int((((startingShell[0] - xy[0]) * 0.015 / (currentPower / 50)) ** 2) - (turPos + turPos / (12 - turPos)) )
		
		check_x_1 = startingShell[0] <= x_location + barrier_width
		check_x_2 = startingShell[0] >= x_location
		
		check_y_1 = startingShell[1] <= display_height
		check_y_2 = startingShell[1] >= display_height - randomHeight
		
		if startingShell[1] > display_height - ground_height:
			hit_x = int(startingShell[0] * (display_height - ground_height) / startingShell[1])
			hit_y = int(display_height - ground_height)
			if ptankX + 15 > hit_x > ptankX - 15:
				damage = 25
			explosion(hit_x, hit_y)
			fire = False
			
		if (check_x_1 and check_x_2 and check_y_1 and check_y_2):
			hit_x = int(startingShell[0])
			hit_y = int(startingShell[1])
			explosion(hit_x, hit_y)
			fire = False


		pygame.display.update()
		
		clock.tick(100)
	return damage

def power(level):
	message_to_screen("Power: " + str(level) + "%", black, y_displace = -270)

def health_bars(player_health, enemy_health):
	if player_health > 75:
		player_health_color = green
	elif player_health >50:
		player_health_color = yellow
	else:
		player_health_color = red
		
	if enemy_health > 75:
		enemy_health_color = green
	elif enemy_health >50:
		enemy_health_color = yellow
	else:
		enemy_health_color = red
		
	pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
	pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))
	
def gameLoop():	
	gameExit = False
	gameOver = False

	player_health = 100
	enemy_health = 100
	
	mainTankX = display_width * 0.9
	mainTankY = display_height * 0.9

	tankMove = 0
	
	currentTurPos = 0
	changeTur = 0
	
	enemyTankX = display_width * 0.1
	enemyTankY = display_height * 0.9
	
	fire_power = 50
	power_change = 0
	
	xlocation = int(display_width / 2) + random.randint(-0.2 * display_width, 0.2 * display_width)
	randomHeight = random.randrange(display_height * 0.1, display_height * 0.6)
	
	barrier_width = 50
	
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
					tankMove = -5
				elif event.key == pygame.K_RIGHT:
					tankMove = 5
				elif event.key == pygame.K_UP:
					changeTur = 1
				elif event.key == pygame.K_DOWN:
					changeTur = -1
				elif event.key == pygame.K_p:
					pause()
				elif event.key == pygame.K_SPACE:
					damage = fireShell(gun, mainTankX, mainTankY, currentTurPos, fire_power, xlocation, barrier_width, randomHeight, enemyTankX, enemyTankY)
					enemy_health -= damage
					damage = e_fireShell(enemy_gun, enemyTankX, enemyTankY, 8, 50, xlocation, barrier_width, randomHeight, mainTankX, mainTankY)
					player_health -= damage
				elif event.key == pygame.K_a:
					power_change = -1
				elif event.key == pygame.K_d:
					power_change = 1

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					tankMove = 0
				elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
					changeTur = 0
				elif event.key == pygame.K_a or event.key == pygame.K_d:
					power_change = 0

		mainTankX += tankMove
		
		currentTurPos += changeTur
		
		if currentTurPos > 8:
			currentTurPos = 8
		elif currentTurPos < 0:
			currentTurPos = 0
			
		if mainTankX - (tankWidth / 2) < xlocation + barrier_width:
			mainTankX += 5
		if mainTankX + (tankWidth / 2) > display_width:
			mainTankX -= 5
	
		gameDisplay.fill(white)
		health_bars(player_health, enemy_health)
		gun = tank(mainTankX, mainTankY, currentTurPos)
		
		enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
		
		fire_power += power_change
		power(fire_power)

		barrier(xlocation, randomHeight, barrier_width)
		gameDisplay.fill(green, rect = [0, display_height - ground_height, display_width, ground_height])
		pygame.display.update()
		
		clock.tick(FPS)

	pygame.quit()
	quit()

gameIntro()
gameLoop()