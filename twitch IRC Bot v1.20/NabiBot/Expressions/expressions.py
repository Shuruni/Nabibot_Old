x = -800
y = 575
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame, sys
pygame.init()
screenSize = (500, 900)
screen = pygame.display.set_mode(screenSize)
# screen = pygame.display.set_mode(screenSize, pygame.NOFRAME)
screenClock = pygame.time.Clock()
framesPerSecond = 1
mainSurface = pygame.display.get_surface()

def changeExpression(fileExName):
	global mainSurface
	print(mainSurface)
	mainSurface.fill((0,255,0))
	expression = pygame.image.load("IMGEXP/" + fileExName + ".png")
	mainSurface.blit(expression, (0,0))
	pygame.display.update()

def CheckInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.display.quit()
                sys.exit()

exScrollTestInc = 0				
def exScrollTest():
	global exScrollTestInc
	exScrollTestInc += 1
	if exScrollTestInc < 10:
		try:
			changeExpression("0" + str(exScrollTestInc))
		except:
			return None
	elif exScrollTestInc > 28:
		exScrollTestInc = 0
	else:
		try:
			changeExpression(str(exScrollTestInc))
		except:
			return None

changeExpression("23")
while True:
	screenClock.tick(framesPerSecond)
	CheckInput()
	# exScrollTest()