#coding: utf-8
from Tkinter import *
# import tkMessageBox
from PIL import Image, ImageTk
import ttk
import tkFont
import random
import os
import sys
import csv
import time
import subprocess
import ctypes
import datetime

myappid = 'NabiGUI' # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

def Nothing():
	print("k")

top = Tk()
root = Toplevel(top)
root.overrideredirect(1)
top.attributes("-alpha", 0.0)
top.title("Nabi GUI")
top.wm_iconbitmap(bitmap = "../NabiGUI.ico")
root.resizable(0,0)
# root.geometry('1072x726')
root.geometry('1072x726-1924+428')
# root.attributes("-toolwindow", 1)
curDisplay = "none"
bgColor = "#4d004d"
root.configure(bg = bgColor)
dFont = tkFont.Font(size = 12, family = "Noto Sans")
def onRootLift(event): root.lift()
top.bind("<FocusIn>", onRootLift)


#top fun displaying:
TopBody = Canvas(top, height = 726, width = 1074, bd = 0, bg = "red", highlightthickness = 0)
TopBody.pack()
topRaw = Image.open("GUI/GUIPreview.jpg")
topImg = ImageTk.PhotoImage(topRaw)
TopBody.create_image((0, 0), anchor = NW, image = topImg)


#NabiCode start/end
def endGUI():
	# date = str(datetime.date.today())
	# with open("Chat_Logs/" + date + "(verbose).nabi","a+") as f:
		# f.writelines(Log.get(0, END))
	# with open("Chat_Logs/" + date + "(simple).nabi","a+") as f:
		# f.writelines(LogSimple.get(0, END))
	root.quit()
	
CoreClosed = True
def startNabiCode():
	global CoreClosed
	NabiStart.place_forget()
	NabiClose.place(x = 10, y = 250)
	CoreClosed = False
	with open("GUI/close.nabi", "w") as f:
		f.write("0")
	subprocess.Popen(["RUN.cmd"])
def closeNabiCode():
	global CoreClosed
	NabiClose.place_forget()
	NabiStart.place(x = 10, y = 250)
	CoreClosed = True
	with open("GUI/close.nabi", "w") as f:
		f.write("1")
OverlayClosed = True
def startOverlayCode():
	global OverlayClosed
	OverlayStart.place_forget()
	OverlayClose.place(x = 105, y = 250)
	OverlayClosed = False
	with open("GUI/closeO.nabi", "w") as f:
		f.write("0")
	subprocess.Popen(["OVERLAY.cmd"])
def closeOverlayCode():
	global OverlayClosed
	OverlayClose.place_forget()
	OverlayStart.place(x = 105, y = 250)
	OverlayClosed = True
	with open("GUI/closeO.nabi", "w") as f:
		f.write("1")
#resetDisplay
def resetWindow():
	if curDisplay == "none":
		return False
	elif curDisplay == "main":
		Body.delete(MainBG)
		Body.delete(MainInfo)
		Body.delete(MainNabi1)
		Body.delete(MainNabi2)
		Body.delete(MainNabi3)
		print("k")
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
		# CommandsList.pack_forget()
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

#update Log/Lists
def Verbose():
	if VerboseCheck.get():
		# print(VerboseCheck.get())
		LogSimple.pack_forget()
		Log.pack_forget()
		Log.pack(side = BOTTOM, fill = X, expand = 1)
		logScroll.config(command=Log.yview)
	else:
		# print(VerboseCheck)
		Log.pack_forget()
		LogSimple.pack_forget()
		LogSimple.pack(side = BOTTOM, fill = X, expand = 1)
		logScroll.config(command=LogSimple.yview)

def log(message):
	with open("GUI/Log.nabi", "a") as f:
		f.write(str(message)+"\n")
		
def junkLog():
	with open("GUI/Log.nabi", "w") as f:
		junk = random.choice(["mayo", "Kappa", "Maji?", "Lolis", "Nabi", "Error", "42", "PogChamp", "what is going on?", "spam", "LOG RAID!", "WTF!", "!shurucode"])
		Log.insert(END, junk)
		
def updateLog():
	with open("GUI/Log.nabi", "r+") as f:
		d = f.readlines()
		for line in d:
			if "CILM" in line or "afk" in line:
				# print("simple")
				LogSimple.insert(END, line)
				LogSimple.see(END)
			Log.insert(END, line)
			Log.see(END)
		Log.selection_clear(0,END)
		LogSimple.selection_clear(0,END)
		# LBLog = Log.get(0, END)
		f.seek(0)
		# for i in d:
			# if i.decode("utf-8") not in LBLog:
				# f.write(i)
		f.truncate()

def UptimeUpdate():
	global UptimeL, UpStart, UpCurrent
	cTime = UpCurrent - UpStart
	m, sec = divmod(cTime, 60)
	h, m = divmod(m, 60)
	Uptime = "%d hours %d min. %d sec." % (h, m, sec)
	if Uptime[8] == "0": Uptime = Uptime[15:]
	elif Uptime[0] == "0": Uptime = Uptime[8:]
	UptimeL.configure(text = "Uptime: " + Uptime)
	
def StatusUpdate():
	global StatusL, UpStart, UpCurrent
	with open("GUI/Status.nabi", "r") as f:
		data = f.read()
		StatusL.configure(text = "Status: " + data)
	if data != "Running":
		UpStart = time.clock()
	UpCurrent = time.clock()

def OverlayStatus():
	global OverlayStatusL
	with open("GUI/OverlayStatus.nabi", "r") as f:
		data = f.read()
		OverlayStatusL.configure(text = "Overlay: " + data)
		
def CrashLogging(CoreClosed):
	with open("CrashLog/CrashLog.nabi", "r+") as f:
		d = f.readlines()
		# log(d)
		try:
			if d[4].strip().lower() == "systemexit":
				log("sysExit on 4")
				pass
			elif d[8].strip().lower() == "systemexit":
				log("sysExit on 8")
				pass
			elif d[9].strip().lower() == "systemexit":
				log("sysExit on 9")
				pass
			else:
				for line in d:
					Log.insert(END, line)
					Log.see(END)
					# LogSimple.insert(END, line)
					# LogSimple.see(END)
		except IndexError:
			for line in d:
				Log.insert(END, line)
				Log.see(END)
		Log.selection_clear(0,END)
		LogSimple.selection_clear(0,END)
		# LBLog = Log.get(0, END)
		f.seek(0)
		# for i in d:
			# if i.decode("utf-8") not in LBLog:
				# f.write(i)
		f.truncate()
# def updateCommands():
	# with open("Commands/CommandList.csv", "r") as f:
		# reader = csv.reader(f)
		# first = True
		# commandsLoaded = 0
		# for line in reader:
			# if first:
				# CommandsTree["columns"] = tuple(line[:])
				# continue
			# else:
				# CommandsTree.insert("", "end", values = line[:], background = "#1a1a1a", foreground = "white", font = dFont)
				# commandsLoaded += 1
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
		Verbose()
		# Log.pack(side = BOTTOM, fill = X, expand = 1)
		
#Commands
class CommandsMenu(object):
	def display(self):
		global curDisplay
		resetWindow()
		curDisplay = "commands"
		CommandsBG = Body.create_image((0, 0), anchor = NW, image = MainBGIMG)
		CommandsInfo = Body.create_text((75,75), anchor = NW, font = dFont, width = 300, fill = "#00eeff", text = "This is the commands section... yea.... where everyone finds their commands to spam in chat... Idk what else to say XD")
		# CommandsList.pack(side = BOTTOM, fill = X)
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

#custom Title Code
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
exitM = Button(titleBar, cursor = "hand2", bd = 0, text = "X", width = 2, bg = "red", command = endGUI, padx = 2, pady = 2)
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
# menu = Menu(root)
# menu.add_command(label = "Main", command = mainMenu.display)
# menu.add_command(label = "Commands", command = commandsMenu.display)
# menu.add_command(label = "Users", command = userMenu.display)
# menu.add_command(label = "Exit", command = root.quit)
# root.config(menu = menu)

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
NabiStart = Button(Body, bd = 0, cursor = "hand2", text = "Start Nabi", bg = "dark green", fg = "black", font = dFont, command = startNabiCode, padx = 2, pady = 2)
NabiClose = Button(Body, bd = 0, cursor = "hand2", text = "Stop Nabi", bg = "dark red", fg = "black", font = dFont, command = closeNabiCode, padx = 2, pady = 2)
OverlayStart = Button(Body, bd = 0, cursor = "hand2", text = "Start Overlay", bg = "dark green", fg = "black", font = dFont, command = startOverlayCode, padx = 2, pady = 2)
OverlayClose = Button(Body, bd = 0, cursor = "hand2", text = "Stop Overlay", bg = "dark red", fg = "black", font = dFont, command = closeOverlayCode, padx = 2, pady = 2)
VerboseCheck = BooleanVar()
VerboseCheckBox = Checkbutton(Body, bd = 0, selectcolor= "black", activebackground="black", bg = "black", activeforeground="white", fg = "white", font = dFont, text="Verbose", variable=VerboseCheck, onvalue = True, offvalue = False, command = Verbose)
VerboseCheckBox.select()
logScroll = Scrollbar(logFrame, orient = VERTICAL)
Log = Listbox(logFrame, bd = 0, highlightthickness = 0, height = 15, font = dFont, bg = "#1a1a1a", fg = "white", yscrollcommand=logScroll.set, activestyle = NONE)
logScroll.config(command=Log.yview)
LogSimple = Listbox(logFrame, bd = 0, highlightthickness = 0, height = 15, font = dFont, bg = "#1a1a1a", fg = "white", yscrollcommand=logScroll.set, activestyle = NONE)

CommandsBG = None
CommandsInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "This is the commands section... yea.... where everyone finds their commands to spam in chat... Idk what else to say XD")
# CommandsTree = ttk.Treeview(logFrame, height = 15)

UserBG = None
UserInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "User list:")
UserList = Listbox(logFrame, height = 15, font = dFont, bg = "#1a1a1a", fg = "white")

ExpressionsBG = None
# ExpFrame = Frame(window, height = 750, width = 1070, bg = bgColor)
# ExpressionsInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "User list:")
# ExpScroll = Scrollbar(Body, orient = VERTICAL)
# ExpCanvas = Canvas(window, height = 300, width = 1000, bd = 0, bg = "yellow", highlightthickness = 0, yscrollcommand=ExpScroll.set)
# ExpScroll.config(command=Body.yview)


#clock updates
UpStart = time.clock()
UpCurrent = time.clock()
def UDClock():
	updateLog()
	StatusUpdate()
	UptimeUpdate()
	OverlayStatus()
	CrashLogging(CoreClosed)
	# updateCommands()
	root.after(500, UDClock)
root.after(500, UDClock)

#mainLoop
mainMenu.display()
win = Frame(master = root)
win.mainloop()












#1

# topFrame = Frame(root)
# topFrame.pack()
# bottomFrame = Frame(root)
# bottomFrame.pack(side=BOTTOM)

# button1 = Button(topFrame, text = "Clicky", fg="blue")
# button2 = Button(topFrame, text = "EH?", fg="green")
# button3 = Button(topFrame, text = "Iyanano?", fg="yellow")
# button4 = Button(bottomFrame, text = "Shinebainoni...", fg="red")

# button1.pack(side = LEFT)
# button2.pack(side = LEFT)
# button3.pack(side = LEFT)
# button4.pack(side = BOTTOM)

#2

# one = Label(root, text = "one", bg = "red", fg="white")
# one.pack()
# two = Label(root, text = "two", bg = "green", fg="black")
# two.pack(fill=X)
# three = Label(root, text = "three", bg = "blue", fg="white")
# three.pack(side = LEFT, fill = Y)

#3

# name = Label(root, text = "Name")
# password = Label(root, text = "Password")
# nameEntry = Entry(root)
# passwordEntry = Entry(root)

# name.grid(row = 0, sticky = E)
# password.grid(row = 1, sticky = E)
# nameEntry.grid(row = 0, column = 1)
# passwordEntry.grid(row = 1, column = 1)

# c = Checkbutton(root, text = "Keep me logged in")
# c.grid(columnspan = 2)

#4

# def printName(event):
	# print("Desu, Desu... SUUU!!!")
	
	
# desu = Button(root, text = "Desu?")
# desu.grid()

# desu.bind("<Button-1>", printName)

#5

# def leftClick(event):
	# print("Hidari")
# def rightClick(event):
	# print("Migi")
# def middleClick(event):
	# print("Naka")

# frame = Frame(root, width = 300, height = 250)
# frame.bind("<Button-1>", leftClick)
# frame.bind("<Button-3>", rightClick)
# frame.bind("<Button-2>", middleClick)
# frame.pack()

#6

# class Lolis(object):
	# def __init__(self, master):
		# frame = Frame(master)
		# frame.pack()
		
		# self.printButton = Button(frame, text = "n-nanda...", command = self.printMessage)
		# self.printButton.pack(side = LEFT)
		
		# self.quitButton = Button(frame, text = "NANI!?! owarimasuka? iyada...", command = frame.quit)
		# self.quitButton.pack(side = LEFT)
	# def printMessage(self):
		# print("anta no sei ja nai dakara... >o<")
		
# root = Tk()
# loli = Lolis(root)
# root.mainloop()

#7

# def doNothing():
	# print("k Kappa")

# root = Tk()

# #***** Main Menu *****

# menu =  Menu(root)
# root.config(menu = menu)

# subMenu = Menu(menu, tearoff = 0)
# menu.add_cascade(label = "File", menu = subMenu)
# subMenu.add_command(label = "Nothing here...", command = doNothing)
# subMenu.add_command(label = "Really...", command = doNothing)
# subMenu.add_separator()
# subMenu.add_command(label = "Exit", command = root.quit)

# editMenu = Menu(menu, tearoff = 0)
# menu.add_cascade(label = "Edit", menu = editMenu)
# editMenu.add_command(label = ">o</", command = doNothing)

# #***** Toolbar *****

# toolbar = Frame(root, bg = "blue")
# insertB = Button(toolbar, text = "Insert Nabi :3", command = doNothing)
# insertB.pack(side = LEFT, padx = 2, pady = 2)
# printB = Button(toolbar, text = "Print Loli >w<", command = doNothing)
# printB.pack(side = LEFT, padx = 2, pady = 2)
# toolbar.pack(side = TOP, fill = X)

# #***** Status Bar *****

# status = Label(root, text = "Nabi has hacked this program d(^O^)b", bd = 1, relief = SUNKEN, anchor = W)
# status.pack(side = BOTTOM, fill = X)


# root.mainloop()

#8

# tkMessageBox.showinfo('Nabi ^w^', 'Flat is Justice (>w<)')

# nabi = tkMessageBox.askquestion('Hitotsu', 'is Nabi cute? (^.^)')

# if nabi == 'yes':
	# print(' Arigatou onii~chan (^w^)')
	
#9

# canvas = Canvas(root, width = 200, height = 100)
# canvas.pack()

# blackLine = canvas.create_line(0, 0, 200, 50)
# redLine = canvas.create_line(0, 100, 200, 50, fill = "red")
# greenBox = canvas.create_rectangle(25, 25, 130, 60, fill = "green")

# canvas.delete(redLine)
# canvas.delete(ALL)

#10

