import random
x = -508
y = 1075
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame, sys
pygame.init()
screenSize = (500, 400)
screen = pygame.display.set_mode(screenSize)
# screen = pygame.display.set_mode(screenSize, pygame.NOFRAME)
screenClock = pygame.time.Clock()
framesPerSecond = 10
mainSurface = pygame.display.get_surface()
AE = []
CurExp = "happy1"
Rcount = 100
with open('AvailableExpressions.txt', 'r') as f:
	for line in f:
		AE.append(line.strip().lower())

def changeExpression(fileExName):
	global mainSurface
	# print(mainSurface)
	mainSurface.fill((0,255,0))
	expression = pygame.image.load("Nabi/" + fileExName + ".png")
	mainSurface.blit(expression, (0,0))
	pygame.display.update()

def readFile():
	global CurExp
	with open("CurrentExpression.txt", "r") as f:
		EXP = f.readline().strip().lower()
		if EXP in AE:
			changeExpression(EXP)
			CurExp = EXP
	
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
	exScrollTestInc = random.randrange(0,29)
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

# changeExpression("23")
while True:
	screenClock.tick(framesPerSecond)
	readFile()
	if Rcount == 100:
		with open('CurrentExpression.txt', 'w') as f:
			f.write("happy1")
		Rcount = 0
	elif CurExp != "happy1":
		print CurExp
		# print Rcount
		Rcount += 1
	CheckInput()
	# exScrollTest()
	
	
	
	
	
	
	
	
	
	
	