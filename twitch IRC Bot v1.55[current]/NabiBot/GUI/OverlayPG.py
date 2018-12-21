# -*- coding: utf-8 -*-
x = -894
y = 1273
import os
import codecs
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y)
import pygame, sys, random, time
import pygame.freetype
pygame.init()
screenSize = (894, 209)
# screen = pygame.display.set_mode(screenSize)
screen = pygame.display.set_mode(screenSize, pygame.NOFRAME)
screenClock = pygame.time.Clock()
framesPerSecond = 10
mainSurface = pygame.display.get_surface()
pygame.display.set_caption("NabiBotGUIv1.0")
AE = []
NabiES = {}
BG = pygame.image.load("NabiOverlayV2.png").convert_alpha()
DefaultExp = "01"
CurExp = DefaultExp
Rcount = 200
with open('../Expressions/NabiV2/AvailableExpressions.nabi', 'rb') as f:
	for line in f:
		AE.append(line.strip().lower())
		NabiES[line.strip().lower()] = pygame.transform.smoothscale(pygame.image.load("../Expressions/NabiV2/" + line.strip().lower() + ".png"), (162,266))

def vaildDir(npDirLocation, TagsDirLocation, foobarNPDir):
	try:
		with open(npDirLocation + "/np_playing.txt", "rb"):
			print("found np_playing.txt")
		with open(npDirLocation + "/np_listening.txt", "rb"):
			print("found np_listening.txt")
		with open(TagsDirLocation + "/most_recent_donator.txt", "rb"):
			print("found most_recent_donator.txt")
		with open(TagsDirLocation + "/most_recent_follower.txt", "rb"):
			print("found most_recent_follower.txt")
		with open(foobarNPDir + "/FoobarNP.txt"):
			print("found FoobarNP.txt")
		return True
	except:
		return False
		
def inputDir():
	npDirLocation = raw_input("please type the directory that the 'Files' folder in Osu!streaming companion is located at: ")
	TagsDirLocation = raw_input("now, please type the directory that you are saving your Stream labels from Twitch alerts at: ")
	foobarNPDir = raw_input("input the foobar NP directory now please: ")
	check = vaildDir(npDirLocation, TagsDirLocation, foobarNPDir)
	if check:
		return (npDirLocation, TagsDirLocation, foobarNPDir)
	else:
		print("Nabi couldn't find some of the files in one of the directories you listed, please try again DX")
		time.sleep(1)
		return inputDir()
	
def wFile(file, messageLst):
	with open(file, "wb") as f:
		for line in messageLst:
			f.write(line + "\n")

with open('GUIdata.nabi', 'rb') as rf:
	GUIdata = []
	npDirLocation = ""
	TagsDirLocation = ""
	foobarNPDir = ""
	for rline in rf:
		if rline.strip() != "":
			GUIdata.append(rline)
		else:
			break
	if len(GUIdata) == 3:
		# npDirLocation = "Osu/osu!SC/Files/"
		# TagsDirLocation = "Stream Labels/"
		npDirLocation = GUIdata[0].strip()
		TagsDirLocation = GUIdata[1].strip()
		foobarNPDir = GUIdata[2].strip()
	check = vaildDir(npDirLocation, TagsDirLocation, foobarNPDir)
	if check == False:
		print("Nabi welcomes you to her own GUI (^o^)/")
		time.sleep(1)
		print("before you can get started, I need to know a couple of things :/")
		time.sleep(1)
		locations = inputDir()
		npDirLocation = locations[0]
		TagsDirLocation = locations[1]
		foobarNPDir = locations[2]
		print("Nabi has succesfully loaded all the files she needs ^w^")
		time.sleep(1)
		print("Nabi can now run normally (^o^)/")
		time.sleep(1)
wFile("GUIdata.nabi", [npDirLocation, TagsDirLocation, foobarNPDir])

def changeExpression(mainSurface, NabiES, EXP):
	mainSurface.blit(NabiES[EXP], (737,-4))

def updateExpression(mainSurface, NabiES):
	global CurExp
	with open("../Expressions/NabiV2/CurrentExpression.nabi", "rb") as f:
		EXP = f.readline().strip().lower()
		if EXP in AE:
			changeExpression(mainSurface, NabiES, EXP)
			CurExp = EXP

def BGblit(mainSurface, BG):
	mainSurface.fill((150, 150, 150))
	mainSurface.blit(BG, (-34,10))

def fitFont(message, width, font = "Noto Sans", current = 36, smallest = 20):
	f = pygame.font.SysFont(font, current)
	# f.ucs4 = True
	text = f.render(message.decode("utf-8"), 1, (0, 221, 255))
	# Twidth = text[0].get_width()
	Twidth = text.get_width()
	if Twidth > width:
		if current == smallest:
			f = pygame.font.Font(font, current)
			f.ucs4 = True
			text = f.render((message[:-3]+u"...").encode("utf-8"), (0, 221, 255))
			return text#text[0]
		else:
			return fitFont(message, width, font, current-3, smallest)
	else:
		return text#text[0]

def updateNP(mainSurface):
	fh = codecs.open(foobarNPDir + '/FoobarNP.txt', 'r')
	foobar = fh.read().decode("utf-8").strip()#unicode(fb.read(), "utf-8")
	# print(foobar.encode("utf-8"))
	if len(foobar) == 0:
		with open(npDirLocation + '/np_playing.txt', 'rb') as p:
			playing = p.readline().strip()
			if playing == "":
				with open(npDirLocation + '/np_listening.txt') as l:
					listening = l.readline().strip()
					if listening == "":
						message = "Nothing at the moment ^w^;"
					else:
						message = listening
			else:
				message = playing
	else:
		fh.close()
		fh = codecs.open(foobarNPDir + '/FoobarNP.txt', 'r')
		message = fh.readline()
		fh.close()
	mainSurface.blit(fitFont(message, 500), (250, 62))

def updateD(mainSurface):
	with open(TagsDirLocation + '/most_recent_donator.txt', 'rb') as d:
		message = d.readline().strip()
	mainSurface.blit(fitFont(message, 235), (515, 137))

def updateF(mainSurface):
	with open(TagsDirLocation + '/most_recent_follower.txt', 'rb') as f:
		message = f.readline().strip()
	mainSurface.blit(fitFont(message, 235), (140, 137))

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
	if Rcount == 200:
		with open('../Expressions/NabiV2/CurrentExpression.nabi', 'wb') as f:
			f.write(DefaultExp)
		Rcount = 0
	elif CurExp != DefaultExp:
		print(str(Rcount))
		Rcount += 1
	pygame.display.update()
	CheckInput()