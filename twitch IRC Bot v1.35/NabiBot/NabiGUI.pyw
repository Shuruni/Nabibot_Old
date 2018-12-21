x = -894
y = 1313
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame, sys, random
pygame.init()
screenSize = (894, 169)
# screen = pygame.display.set_mode(screenSize)
screen = pygame.display.set_mode(screenSize, pygame.NOFRAME)
screenClock = pygame.time.Clock()
framesPerSecond = 10
mainSurface = pygame.display.get_surface()
pygame.display.set_caption("NabiBotGUIv1.0")
npDirLocation = "Osu/osu!SC/Files/"
TagsDirLocation = "Stream Labels/"
AE = []
NabiES = {}
BG = pygame.image.load("NabiOverlayV2.png").convert_alpha()
CurExp = "happy1"
Rcount = 50
with open('Expressions/AvailableExpressions.txt', 'r') as f:
	for line in f:
		AE.append(line.strip().lower())
		NabiES[line.strip().lower()] = pygame.transform.smoothscale(pygame.image.load("Expressions/Nabi/" + line.strip().lower() + ".png"), (175,350))


def changeExpression(mainSurface, NabiES, EXP):
	mainSurface.blit(NabiES[EXP], (720,15))

def updateExpression(mainSurface, NabiES):
	global CurExp
	with open("Expressions/CurrentExpression.txt", "r") as f:
		EXP = f.readline().strip().lower()
		if EXP in AE:
			changeExpression(mainSurface, NabiES, EXP)
			CurExp = EXP

def BGblit(mainSurface, BG):
	mainSurface.fill((200, 0, 0))
	mainSurface.blit(BG, (-34,-34))

def fitFont(message, width, font = None, current = 36, smallest = 20):
	f = pygame.font.Font(font, current)
	text = f.render(message, True, (0, 221, 255))
	Twidth = text.get_width()
	if Twidth > width:
		if current == smallest:
			f = pygame.font.Font(font, current)
			text = f.render(message[:-3]+"...", True, (0, 221, 255))
			return text
		else:
			return fitFont(message, width, font, current-1, smallest)
	else:
		return text

def updateNP(mainSurface):
	with open(npDirLocation + 'np_playing.txt', 'r') as p:
		playing = p.readline().strip()
		if playing == "":
			with open(npDirLocation + 'np_listening.txt') as l:
				listening = l.readline().strip()
				if listening == "":
					message = "Nothing at the moment ^w^;"
				else:
					message = listening
		else:
			message = playing
	mainSurface.blit(fitFont(message, 500), (250, 30))

def updateD(mainSurface):
	with open(TagsDirLocation + 'most_recent_donator.txt', 'r') as d:
		message = d.readline().strip()
	mainSurface.blit(fitFont(message, 235), (515, 110))

def updateF(mainSurface):
	with open(TagsDirLocation + 'most_recent_follower.txt', 'r') as f:
		message = f.readline().strip()
	mainSurface.blit(fitFont(message, 235), (140, 110))

def CheckInput():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


while True:
	screenClock.tick(framesPerSecond)
	BGblit(mainSurface, BG)
	updateNP(mainSurface)
	updateD(mainSurface)
	updateF(mainSurface)
	updateExpression(mainSurface, NabiES)
	if Rcount == 50:
		with open('Expressions/CurrentExpression.txt', 'w') as f:
			f.write("happy1")
		Rcount = 0
	elif CurExp != "happy1":
		print(str(Rcount))
		Rcount += 1
	pygame.display.update()
	CheckInput()