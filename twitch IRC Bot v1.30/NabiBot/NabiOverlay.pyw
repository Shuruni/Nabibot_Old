x = -876
y = 871
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame, sys
pygame.init()
screenSize = (874, 169)
# screen = pygame.display.set_mode(screenSize)
screen = pygame.display.set_mode(screenSize, pygame.NOFRAME)
screenClock = pygame.time.Clock()
framesPerSecond = 10
mainSurface = pygame.display.get_surface()
pygame.display.set_caption("Nabi Overlay")
npfontSize = 36
dfontSize = 36
ffontSize = 36
npFont = pygame.font.Font(None, npfontSize)
dFont = pygame.font.Font(None, dfontSize)
fFont = pygame.font.Font(None, ffontSize)
npDirLocation = "Osu/osu!SC/Files/"
TagsDirLocation = "Stream Labels/"

def BGblit():
	global mainSurface
	# print(mainSurface)
	mainSurface.fill((50, 50, 50))
	img = pygame.image.load("NabiOverlayV1.png")
	mainSurface.blit(img, (-34,-34))

def fitFont(message, spot):
	global npFont, dFont, fFont, npfontSize, dfontSize, ffontSize
	text = None
	mWidth = None
	if spot == "NP":
		mWidth = 500
		text = npFont.render(message, True, (0, 221, 255))
		width = text.get_width()
		if npfontSize == 20:
			# print "false"
			return False
		elif width > mWidth:
			npfontSize -= 1
			npFont = pygame.font.Font(None, npfontSize)
			return fitFont(message, spot)
		else:
			return True
	elif spot == "D":
		mWidth = 235
		text = dFont.render(message, True, (0, 221, 255))
		width = text.get_width()
		if dfontSize == 20:
			# print "false"
			return False
		elif width > mWidth:
			dfontSize -= 1
			dFont = pygame.font.Font(None, dfontSize)
			return fitFont(message, spot)
		else:
			return True
	elif spot == "F":
		mWidth = 235
		text = fFont.render(message, True, (0, 221, 255))
		width = text.get_width()
		if ffontSize == 20:
			# print "false"
			return False
		elif width > mWidth:
			ffontSize -= 1
			fFont = pygame.font.Font(None, ffontSize)
			return fitFont(message, spot)
		else:
			return True

def updateNP():
	global mainSurface, npFont
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
	if fitFont(message, "NP") == False:
		text = npFont.render(message[:65] + "...", True, (0, 221, 255))
	else:
		text = npFont.render(message, True, (0, 221, 255))
	mainSurface.blit(text, (250, 30))

def updateD():
	global mainSurface, dFont
	with open(TagsDirLocation + 'most_recent_donator.txt', 'r') as d:
		message = d.readline().strip()
	if fitFont(message, "D") == False:
		text = dFont.render(message[:30] + "...", True, (0, 221, 255))
	else:
		text = dFont.render(message, True, (0, 221, 255))
	mainSurface.blit(text, (515, 110))

def updateF():
	global mainSurface, fFont
	with open(TagsDirLocation + 'most_recent_follower.txt', 'r') as f:
		message = f.readline().strip()
	if fitFont(message, "F") == False:
		text = fFont.render(message[:30] + "...", True, (0, 221, 255))
	else:
		text = fFont.render(message, True, (0, 221, 255))
	mainSurface.blit(text, (140, 110))

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
	BGblit()
	updateNP()
	updateD()
	updateF()
	pygame.display.update()
	npfontSize = 36
	dfontSize = 36
	ffontSize = 36
	npFont = pygame.font.Font(None, npfontSize)
	dFont = pygame.font.Font(None, dfontSize)
	fFont = pygame.font.Font(None, ffontSize)
	CheckInput()