from Tkinter import *
from PIL import Image, ImageTk
import tkFont, time, random
import logging
import ctypes

myappid = 'NabiOverlay' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


LOG_FILENAME = '../CrashLog/CrashLog.nabi'
logging.basicConfig(filename=LOG_FILENAME, level=logging.INFO)

with open("OverlayStatus.nabi", "w") as f:
	f.write("Running")
	f.truncate()

def logit(message):
	with open("../GUI/Log.nabi", "a") as f:
		f.write(str(message)+"\n")

root = Tk()
# root.overrideredirect(1)
root.resizable(0,0)
# root.geometry('894x209-1918+1286')
root.geometry('894x209-1918+1258')
# root.geometry('894x209')
root.wm_title("Nabi Overlay")
# bgColor = "#969696"
bgColor = "#505050"
root.configure(bg = bgColor)
time.clock()

#Startup Checks
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


#Canvas
Body = Canvas(root, bd = 0, bg = bgColor, highlightthickness = 0)
Body.pack(fill = BOTH)
Body.pack_propagate(False)

#Images
OverlayRaw = Image.open("NabiOverlayV2.png")
OverlayImg = ImageTk.PhotoImage(OverlayRaw)
Overlay = Body.create_image((-34, 5), anchor = NW, image = OverlayImg)

#Variables
NPtxt = Body.create_text((0, 0))
Dtxt = Body.create_text((0, 0))
Ftxt = Body.create_text((0, 0))
CurExp = "01"
DefaultExp = "01"
UpStart = None
AE = []
NabiES = {}
with open('../Expressions/NabiV2/AvailableExpressions.nabi', 'rb') as f:
	for line in f:
		AE.append(line.strip().lower())
		tempRaw = Image.open("../Expressions/NabiV2[162x266]/" + line.strip().lower() + ".png")
		# tempRaw = tempRaw.resize((162,266), Image.ANTIALIAS)
		tempImg = ImageTk.PhotoImage(tempRaw)
		NabiES[line.strip().lower()] = tempImg
# CurExpImg = Body.create_image((737, -4), anchor = NW, image = NabiES["01"])
CurExpImg = Body.create_image((737, -4), anchor = NW, image = NabiES[DefaultExp])

#Functions
def fitFont(position, message, width, Body, font = "Noto Sans", current = 25, smallest = 12, truncated = False):
	f = tkFont.Font(size = current, family = font)
	text = Body.create_text(position, anchor = W, font = f, fill = "#00DDFF", text = message.encode("utf-8"))
	bounds = Body.bbox(text)
	Twidth = bounds[2] - bounds[0]
	if Twidth > width:
		Body.delete(text)
		if current == smallest:
			return fitFont(position, message[:-1], width, Body, font, current, smallest, True)
		else:
			return fitFont(position, message, width, Body, font, current-1, smallest, truncated)
	elif truncated == True:
		Body.delete(text)
		return Body.create_text(position, anchor = W, font = f, fill = "#00DDFF", text = (message[:-3]+u"...").encode("utf-8"))
	else:
		return text

def changeExpression(Body, NabiES, EXP):
	return Body.create_image((737, -4), anchor = NW, image = NabiES[EXP])

def updateExpression(Body, NabiES):
	global CurExp, CurExpImg, UpStart
	with open("../Expressions/NabiV2/CurrentExpression.nabi", "r+") as f:
		EXP = f.readline().strip().lower()
		if len(EXP) != 0:
			# print("good")
			if EXP in AE:
				# print("in list")
				Body.delete(CurExpImg)
				ExpImg = changeExpression(Body, NabiES, EXP)
				CurExp = EXP
				f.seek(0)
				f.truncate()
				print("Expression Found!")
				UpStart = time.clock()
				return ExpImg

def updateNP(Body):
	with open(foobarNPDir + '/FoobarNP.txt', 'r') as f:
		foobar = f.read().decode("utf-8")
	if foobar == u"":
		with open("../YTMPlayer/CurSong.txt", "r") as f:
			nowPlayingNabiGUI = f.read().decode("utf-8")
		if nowPlayingNabiGUI == u"":
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
			message = nowPlayingNabiGUI
	else:
		# print(foobar.encode("utf-8"))
		message = foobar
	return fitFont((250, 83), message, 450, Body)

def updateD(Body):
	with open(TagsDirLocation + '/most_recent_donator.txt', 'rb') as d:
		message = d.readline().strip()
	return fitFont((515, 160), message, 235, Body)

def updateF(Body):
	with open(TagsDirLocation + '/most_recent_follower.txt', 'rb') as f:
		message = f.readline().strip()
	return fitFont((140, 160), message, 235, Body)

def ExpRevertCheck(UpStart):
	cTime = int(time.clock() - UpStart)
	print(cTime)
	if cTime >= 20:
		return True
	else:
		return False

def exitCheck():
	with open("CloseO.nabi", "rb") as f:
		tempRead = f.read()
	if tempRead == "1":
		with open("CloseO.nabi", "wb") as f:
			f.write("0")
			logit(" ")
			logit(" ")
			logit("Nabi's Overlay Has been terminated (^w^;)")
			logit(" ")
			logit(" ")
			sys.exit()

def UDClock():
	global UpStart, CurExp, CurExpImg, Rcount, Body, NPtxt, Dtxt, Ftxt
	exitCheck()
	Body.delete(NPtxt)
	NPtxt = updateNP(Body)
	Body.delete(Dtxt)
	Dtxt = updateD(Body)
	Body.delete(Ftxt)
	Ftxt = updateF(Body)
	CurExpImg = updateExpression(Body, NabiES)
	if DefaultExp != CurExp:
		rCheck = ExpRevertCheck(UpStart)
		if rCheck:
			with open('../Expressions/NabiV2/CurrentExpression.nabi', 'wb') as f:
				print("Reverting to normal (-o-;)")
				f.write(DefaultExp)
			UpStart = 0
	root.after(500, UDClock)
root.after(500, UDClock)
root.wm_iconbitmap(bitmap = "../../Overlay.ico")
try:
	root.mainloop()
except:
	logging.exception('Nabi Overlay Crashed (>w<)')	
	# logit("here...")
	with open(LOG_FILENAME, "r") as l:
		d = l.readlines()
		# print(d)
		try:
			if d[8].strip().lower() == "systemexit":
				with open("OverlayStatus.nabi", "w") as f:
					f.write("Not Running")
					f.truncate()
			else:
				with open("OverlayStatus.nabi", "w") as f:
					f.write("Crashed")
					f.truncate()
				# pass
		except IndexError:
			# logit("yea...")
			with open("OverlayStatus.nabi", "w") as f:
				f.write("Crashed")
				f.truncate()
	# print(d)
	# logit("end")
	raise