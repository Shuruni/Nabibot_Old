#coding: utf-8
from Tkinter import *
from PIL import Image, ImageTk
import ttk, tkFont, random, os, sys, csv, time, subprocess, ctypes, datetime
from YTMPlayer.YTD import *
from GUI.GUIvariables import *
print("variables loaded")
from GUI.GUIfunctions import *
print("functions loaded")
log("successfully initiated GUI, 今日は　＾ｗ＾/")

# winID = 'NabiGUI' 
# ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(winID)

#top fun displaying:
TopBody = Canvas(top, height = 726, width = 1074, bd = 0, bg = "red", highlightthickness = 0)
TopBody.pack()
topRaw = Image.open("GUI/GUIPreview.jpg")
topImg = ImageTk.PhotoImage(topRaw)
TopBody.create_image((0, 0), anchor = NW, image = topImg)

def resetWindow():
	if curDisplay == "none":
		return False
	elif curDisplay == "main":
		Body.delete(MainBG)
		Body.delete(MainInfo)
		Body.delete(MainNabi1)
		Body.delete(MainNabi2)
		Body.delete(MainNabi3)
		LogSimple.pack_forget()
		Log.pack_forget()
		logScroll.pack_forget()
		VerboseCheckBox.place_forget()
		NabiClose.place_forget()
		NabiStart.place_forget()
		OverlayStart.place_forget()
		OverlayClose.place_forget()
		return True
	elif curDisplay == "commands":
		Body.delete(CommandsBG)
		CommandsInfo.pack_forget()
		CommandsList.pack_forget()
		# CommandsTree.pack_forget()
		return True
	elif curDisplay == "user":
		Body.delete(UserBG)
		UserInfo.pack_forget()
		UserList.pack_forget()
		return True
	elif curDisplay == "expressions":
		Body.delete("all")
		Body.config(height = 300, scrollregion = (0,0,0,0))
		Body.unbind_all("<MouseWheel>")
		# ExpCanvas.pack_forget()
		# ExpScroll.pack_forget()

#Main
class MainMenu(object):
	def display(self):
		global curDisplay, MainInfo, MainBG
		resetWindow()
		curDisplay = "main"
		MainBG = Body.create_image((0, 0), anchor = NW, image = MainBGIMG)
		MainInfo = Body.create_text((75,75), anchor = NW, font = dFont, width = 300, fill = "#00eeff", text = "こんにちは, Nabi welcomes you to her very own personal GUI interface (^o^)/. Currently, it is still under development, but will hopefully replace the old CMD output so Nabi will look cuter >w<")
		MainNabi1 = Body.create_image((400, 0), anchor = NW, image = MainNabiIMG)
		MainNabi2 = Body.create_image((600, 0), anchor = NW, image = MainNabi2IMG)
		MainNabi3 = Body.create_image((800, 0), anchor = NW, image = MainNabi3IMG)
		if not CoreClosed:
			NabiClose.place(x = 10, y = 250)
		else:
			NabiStart.place(x = 10, y = 250)
		if not OverlayClosed:
			OverlayClose.place(x = 105, y = 250)
		else:
			OverlayStart.place(x = 105, y = 250)
		VerboseCheckBox.place(x = 975, y = 267)
		logScroll.pack(side = RIGHT, fill = Y)
		Verbose(LogSimple, Log, logScroll, VerboseCheck)
		# Log.pack(side = BOTTOM, fill = X, expand = 1)

def startNabiCode(NabiStart, NabiClose):
	global CoreClosed
	NabiStart.place_forget()
	NabiClose.place(x = 10, y = 250)
	CoreClosed = False
	with open("GUI/close.nabi", "w") as f:
		f.write("0")
	subprocess.Popen(["RUN.cmd"])
def closeNabiCode(NabiStart, NabiClose):
	global CoreClosed
	NabiClose.place_forget()
	NabiStart.place(x = 10, y = 250)
	CoreClosed = True
	with open("GUI/close.nabi", "w") as f:
		f.write("1")
	
def startOverlayCode(OverlayStart, OverlayClose):
	global OverlayClosed
	OverlayStart.place_forget()
	OverlayClose.place(x = 105, y = 250)
	OverlayClosed = False
	with open("GUI/closeO.nabi", "w") as f:
		f.write("0")
	subprocess.Popen(["OVERLAY.cmd"])
def closeOverlayCode(OverlayStart, OverlayClose):
	global OverlayClosed
	OverlayClose.place_forget()
	OverlayStart.place(x = 105, y = 250)
	OverlayClosed = True
	with open("GUI/closeO.nabi", "w") as f:
		f.write("1")

#Commands
class CommandsMenu(object):
	def display(self):
		global curDisplay
		resetWindow()
		curDisplay = "commands"
		CommandsBG = Body.create_image((0, 0), anchor = NW, image = MainBGIMG)
		CommandsInfo = Body.create_text((75,75), anchor = NW, font = dFont, width = 300, fill = "#00eeff", text = "This is the commands section... yea.... where everyone finds their commands to spam in chat... Idk what else to say XD")
		CommandsList.pack(side = BOTTOM, fill = X)
		# CommandsTree.pack(side = BOTTOM, fill = X)

#Users
class UserMenu(object):
	def display(self):
		global curDisplay
		resetWindow()
		curDisplay = "user"
		UserBG = Body.create_image((0, 0), anchor = NW, image = MainBGIMG)
		UserInfo = Body.create_text((75,75), anchor = NW, font = dFont, width = 300, fill = "#00eeff", text = "User list:")
		UserList.pack(side = BOTTOM, fill = X)

#Expressions
class ExpressionsMenu(object):
	def __init__(self):
		self.buttons = []
		self.placed = []
		self.images = {}
		self.loadedButtons = False
		with open("Expressions/NabiLaunchboard128x128/AvailableExpressions.nabi", "r") as f:
			self.available = f.readlines()
		for i in self.available:
			tRaw = Image.open("Expressions/NabiLaunchboard128x128/resized/" + i.strip() + ".png")
			tRaw = tRaw.resize((96,96))
			self.images[i.strip()] = ImageTk.PhotoImage(tRaw)
			# self.buttons.append(Button(self.ExpFrame, bd = 0, cursor = "hand2", command = lambda: self.changeExp(i.strip()), image = self.images[i.strip()]))
	
	def makeButtons(self):
		for i in range(len(self.available)):
			self.buttons.append(Button(window, bd = 0, cursor = "hand2", bg = "#1f1f2e", command = lambda i=i: self.changeExp(i), image = self.images[self.available[i].strip()]))
		self.loadedButtons = True
	
	def changeExp(self, expName):
		print(expName)
		with open("Expressions/NabiV2/CurrentExpression.nabi", "w") as f:
			f.write(self.available[expName])
			f.truncate()
	
	def display(self):
		global curDisplay
		resetWindow()
		curDisplay = "expressions"
		if not self.loadedButtons:
			self.makeButtons()
		# Body.config(height = 700, yscrollcommand = ExpScroll.set)
		ExpBG = Body.create_image((0, 0), anchor = NW, image = MainBGIMG)
		# Body.create_window((0, 0), anchor = NW, window = ExpFrame)
		# ExpScroll.pack(side = LEFT, fill = Y, expand = True)
		# ExpScroll.place(x = 1000, y = 0)
		index = 0
		for row in range(7):
			for column in range(10):
				temp = self.buttons[index]
				# self.placed.append(temp.place(((96*column)+(column*10)+10, (96*row)+(row*10)+10), anchor = NW)
				# temp.place(x = 0, y = 0, anchor = NW)
				Body.create_window(((96*column)+(column*10)+10, (96*row)+(row*10)+10), anchor = NW, window = temp)
				# Body.create_image(((96*column)+(column*10)+10, (96*row)+(row*10)+10), anchor = NW, image = self.images[index])
				index += 1
		Body.config(height = 700, scrollregion= Body.bbox("all"))
		def _on_mousewheel(event):
			Body.yview_scroll(int(-1*(event.delta/120)), "units")
		Body.bind_all("<MouseWheel>", _on_mousewheel)
		# ExpCanvas.place()
		# ExpScroll.pack(side = RIGHT, fill = Y)
		
#Class calling
mainMenu = MainMenu()
commandsMenu = CommandsMenu()
userMenu = UserMenu()
expressionsMenu = ExpressionsMenu()

#custom window motion
windowX = None
windowY = None
def StartMove(event):
	global windowX, windowY
	windowX = event.x
	windowY = event.y

def StopMove(event):
	global windowX, windowY
	windowX = None
	windowY = None

def OnMotion(event):
	deltax = event.x - windowX
	deltay = event.y - windowY 
	x = root.winfo_x() + deltax
	y = root.winfo_y() + deltay
	root.geometry("+%s+%s" % (x, y))

#menuBar
titleBar = Frame(root, height = 30, bd = 1, bg = bgColor, padx = 2, pady = 2)
titleBar.pack(side = TOP, fill = X)
titleBar.bind("<B1-Motion>", OnMotion)
titleBar.bind("<ButtonPress-1>", StartMove)
titleBar.bind("<ButtonRelease-1>", StopMove)
exitM = Button(titleBar, cursor = "hand2", bd = 0, text = "X", width = 2, bg = "red", command = lambda: endGUI(root), padx = 2, pady = 2)
exitM.pack(side = RIGHT)
menu = Frame(root, height = 30, bd = 1, bg = bgColor, padx = 2, pady = 0)
menu.pack(side = TOP, fill = X)
menu01 = Button(menu, cursor = "hand2", width = 4+2, anchor = S, bd = 0, text = "Main", bg = bgColor, fg = "#00eeff", command = mainMenu.display, padx = 2, pady = 1)
menu01.pack(side = LEFT, anchor = S)
menu02 = Button(menu, cursor = "hand2", width = 8+2, anchor = S, bd = 0, text = "Commands", bg = bgColor, fg = "#00eeff", command = commandsMenu.display, padx = 2, pady = 1)
menu02.pack(side = LEFT, anchor = S)
menu03 = Button(menu,  cursor = "hand2", width = 5+2, anchor = S, bd = 0, text = "Users", bg = bgColor, fg = "#00eeff", command = userMenu.display, padx = 2, pady = 1)
menu03.pack(side = LEFT, anchor = S)
menu04 = Button(menu,  cursor = "hand2", width = 8+2, anchor = S, bd = 0, text = "Expressions", bg = bgColor, fg = "#00eeff", command = expressionsMenu.display, padx = 2, pady = 1)
menu04.pack(side = LEFT, anchor = S)

#mediaOptions
mediaProgressBar = Label(titleBar, width = 98, anchor = NW, bd = 0, text = "", bg = bgColor, fg = "#00eeff", padx = 0, pady = 0)
mediaProgressBar.pack(side = RIGHT)
mediaNext = Button(menu, cursor = "hand2", width = 4, anchor = CENTER, bd = 0, text = u"►", bg = bgColor, fg = "#00eeff", command = nextSong, padx = 2, pady = 1)
mediaNext.pack(side = RIGHT)
mediaPlay = Button(menu, cursor = "hand2", width = 4, anchor = CENTER, bd = 0, text = u"▶", bg = bgColor, fg = "#00eeff", command = player.play, padx = 2, pady = 1)
mediaPlay.pack(side = RIGHT)
mediaPause = Button(menu, cursor = "hand2", width = 4, anchor = CENTER, bd = 0, text = u"| |", bg = bgColor, fg = "#00eeff", command = player.pause, padx = 2, pady = 1)
mediaPrevious = Button(menu, cursor = "hand2", width = 4, anchor = CENTER, bd = 0, text = u"◄", bg = bgColor, fg = "#00eeff", command = prevSong, padx = 2, pady = 1)
mediaPrevious.pack(side = RIGHT)
mediaNP = Button(menu, cursor = "hand2", width = 80, anchor = S, bd = 2, relief = RIDGE, text = getCurSong(), bg = bgColor, fg = "#00eeff", command = playCurSong, padx = 2, pady = 1)
mediaNP.pack(side = RIGHT, anchor = S)
mediaMode = Button(menu, cursor = "hand2", width = 3, anchor = CENTER, bd = 0, text = "↻", bg = bgColor, fg = "#00eeff", command = toggleMode, padx = 2, pady = 1)
mediaMode.pack(side = RIGHT)

def playPause(arg):
	if player.is_playing():
		player.pause()
	else:
		player.play()
root.bind("<space>", playPause)
root.bind("<Left>", prevSong)
root.bind("<Right>", nextSong)
root.bind("<Down>", playCurSong)
root.bind("<Up>", toggleMode)
def checkMediaState():
	if player.is_playing():
		mediaPlay.pack_forget()
		mediaPause.pack_forget()
		mediaPrevious.pack_forget()
		mediaPause.pack(side = RIGHT)
		mediaPrevious.pack(side = RIGHT)
	else:
		mediaPlay.pack_forget()
		mediaPause.pack_forget()
		mediaPrevious.pack_forget()
		mediaPlay.pack(side = RIGHT)
		mediaPrevious.pack(side = RIGHT)
	mediaMode.pack_forget()
	tgM = toggleMode(returnOnly = True)
	if tgM == "default":
		tgM = bgColor
	mediaMode.config(bg = tgM)
	mediaMode.pack(side = RIGHT)
	mediaNP.pack_forget()
	mediaNP.config(text = getCurSong())
	mediaProgressBar.config(text = progressBarUpdate())
	mediaNP.pack(side = RIGHT)

#windowborder
window = Frame(root, height = 802, width = 1072, highlightthickness = 2, highlightbackground = bgColor, bg = bgColor)
window.pack(side = BOTTOM)

#statusBar
StatusBar = Frame(window, height = 20, bd = 1, relief = SUNKEN)
StatusBar.pack(fill = X, side = BOTTOM)
StatusL = Label(StatusBar, text = "Status: ", width = 30, anchor = W)
StatusL.pack(side = LEFT)
UptimeL = Label(StatusBar, text = "Uptime: ", width = 25, anchor = W)
UptimeL.pack(side = LEFT)
OverlayStatusL = Label(StatusBar, text = "Overlay: ", width = 30, anchor = W)
OverlayStatusL.pack(side = LEFT)

#body
Body = Canvas(window, height = 300, width = 1070, bd = 0, bg = bgColor, highlightthickness = 0)
Body.pack(side = TOP, fill = BOTH)
Body.pack_propagate(False)
logFrame = Frame(window, bd = 0, bg = bgColor)
logFrame.pack(side = BOTTOM, fill = X)

#images
MainBGRAW = Image.open("GUI/starry.jpg")
MainBGRAW = MainBGRAW.resize((1080,753), Image.ANTIALIAS)
MainBGIMG = ImageTk.PhotoImage(MainBGRAW)

MainNabiRAW = Image.open("Expressions/NabiV2/12.png")
MainNabiRAW = MainNabiRAW.resize((190,300), Image.ANTIALIAS)
MainNabiIMG = ImageTk.PhotoImage(MainNabiRAW)

MainNabi2RAW = Image.open("Expressions/NabiV2/00.png")
MainNabi2RAW = MainNabi2RAW.resize((190,300), Image.ANTIALIAS)
MainNabi2IMG = ImageTk.PhotoImage(MainNabi2RAW)

MainNabi3RAW = Image.open("Expressions/NabiV2/eh7.png")
MainNabi3RAW = MainNabi3RAW.resize((190,300), Image.ANTIALIAS)
MainNabi3IMG = ImageTk.PhotoImage(MainNabi3RAW)

#widgets
MainBG = None
MainInfo = None
MainNabi1 = None
MainNabi2 = None
MainNabi3 = None
NabiStart = Button(Body, bd = 0, cursor = "hand2", text = "Start Nabi", bg = "dark green", fg = "black", font = dFont, command = lambda: startNabiCode(NabiStart, NabiClose), padx = 2, pady = 2)
NabiClose = Button(Body, bd = 0, cursor = "hand2", text = "Stop Nabi", bg = "dark red", fg = "black", font = dFont, command = lambda: closeNabiCode(NabiStart, NabiClose), padx = 2, pady = 2)
OverlayStart = Button(Body, bd = 0, cursor = "hand2", text = "Start Overlay", bg = "dark green", fg = "black", font = dFont, command = lambda: startOverlayCode(OverlayStart, OverlayClose), padx = 2, pady = 2)
OverlayClose = Button(Body, bd = 0, cursor = "hand2", text = "Stop Overlay", bg = "dark red", fg = "black", font = dFont, command = lambda: closeOverlayCode(OverlayStart, OverlayClose), padx = 2, pady = 2)
VerboseCheck = BooleanVar()
VerboseCheckBox = Checkbutton(Body, bd = 0, selectcolor= "black", activebackground="black", bg = "black", activeforeground="white", fg = "white", font = dFont, text="Verbose", variable=VerboseCheck, onvalue = True, offvalue = False, command = lambda: Verbose(LogSimple, Log, logScroll, VerboseCheck))
VerboseCheckBox.select()
logScroll = Scrollbar(logFrame, orient = VERTICAL)
Log = Listbox(logFrame, bd = 0, highlightthickness = 0, height = 15, font = dFont, bg = "#1a1a1a", fg = "white", yscrollcommand=logScroll.set, activestyle = NONE)
logScroll.config(command=Log.yview)
LogSimple = Listbox(logFrame, bd = 0, highlightthickness = 0, height = 15, font = dFont, bg = "#1a1a1a", fg = "white", yscrollcommand=logScroll.set, activestyle = NONE)

CommandsBG = None
CommandsInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "This is the commands section... yea.... where everyone finds their commands to spam in chat... Idk what else to say XD")
CommandsList = Listbox(logFrame, height = 20, font = mFont, bg = "#1a1a1a", fg = "white")
PopulateCommands(CommandsList)

UserBG = None
UserInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "User list:")
UserList = Listbox(logFrame, height = 20, font = mFont, bg = "#1a1a1a", fg = "white")
PopulateUsers(UserList)

ExpressionsBG = None

#VLC Video player
videoPanel = Frame(window, height = 300, width = 1070, bd = 0, highlightthickness = 0)
setHandle(videoPanel)
videoPanel.pack(side = TOP, fill = BOTH)
videoPanel.pack_propagate(False)


#clock updates
def UDClock():
	global UpCurrent, UpStart
	updateLog(Log, LogSimple)
	UpCurrent, UpStart = StatusUpdate(StatusL, UpStart, UpCurrent)
	UptimeUpdate(UptimeL, UpStart, UpCurrent)
	OverlayStatus(OverlayStatusL)
	checkMediaState()
	CrashLogging(Log)
	# updateCommands()
	nextSongCheck()
	root.after(100, UDClock)
root.after(100, UDClock)

#mainLoop
mainMenu.display()
win.mainloop()