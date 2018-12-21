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


def showMain():
	print("k")

top = Tk()
root = Toplevel(top)
root.overrideredirect(1)
top.attributes("-alpha", 0.0)
top.wm_title("Nabi GUI")
root.resizable(0,0)
root.geometry('-1924+428')
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
def startNabiCode():
	subprocess.Popen(["RUN.cmd"])
def closeNabiCode():
	with open("GUI/close.nabi", "w") as f:
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
		Log.pack_forget()
		logScroll.pack_forget()
		NabiClose.place_forget()
		NabiStart.place_forget()
		return True
	elif curDisplay == "commands":
		CommandsInfo.pack_forget()
		# CommandsList.pack_forget()
		# CommandsTree.pack_forget()
		return True
	elif curDisplay == "user":
		UserInfo.pack_forget()
		UserList.pack_forget()
		return True

#update Log/Lists
def junkLog():
	with open("GUI/Log.nabi", "w") as f:
		junk = random.choice(["mayo", "Kappa", "Maji?", "Lolis", "Nabi", "Error", "42", "PogChamp", "what is going on?", "spam", "LOG RAID!", "WTF!", "!shurucode"])
		Log.insert(END, junk)
		
def updateLog():
	with open("GUI/Log.nabi", "r+") as f:
		d = f.readlines()
		for line in d:
			Log.insert(END, line)
			Log.see(END)
		Log.selection_clear(0,END)
		LBLog = Log.get(0, END)
		f.seek(0)
		for i in d:
			if i.decode("utf-8") not in LBLog:
				f.write(i)
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
		# logMenu.pack(side = TOP, fill = X)
		NabiStart.place(x = 10, y = 250)
		NabiClose.place(x = 70, y = 250)
		logScroll.pack(side = RIGHT, fill = Y)
		Log.pack(side = BOTTOM, fill = X, expand = 1)
		
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
	
#Class calling
mainMenu = MainMenu()
commandsMenu = CommandsMenu()
userMenu = UserMenu()

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
exitM = Button(titleBar, cursor = "hand2", bd = 0, text = "X", width = 2, bg = "red", command = root.quit, padx = 2, pady = 2)
exitM.pack(side = RIGHT)
menu = Frame(root, height = 30, bd = 1, bg = bgColor, padx = 2, pady = 0)
menu.pack(side = TOP, fill = X)
menu01 = Button(menu, cursor = "hand2", width = 4+2, anchor = S, bd = 0, text = "Main", bg = bgColor, fg = "#00eeff", command = mainMenu.display, padx = 2, pady = 1)
menu01.pack(side = LEFT, anchor = S)
menu02 = Button(menu, cursor = "hand2", width = 8+2, anchor = S, bd = 0, text = "Commands", bg = bgColor, fg = "#00eeff", command = commandsMenu.display, padx = 2, pady = 1)
menu02.pack(side = LEFT, anchor = S)
menu03 = Button(menu,  cursor = "hand2", width = 5+2, anchor = S, bd = 0, text = "Users", bg = bgColor, fg = "#00eeff", command = userMenu.display, padx = 2, pady = 1)
menu03.pack(side = LEFT, anchor = S)
# menu = Menu(root)
# menu.add_command(label = "Main", command = mainMenu.display)
# menu.add_command(label = "Commands", command = commandsMenu.display)
# menu.add_command(label = "Users", command = userMenu.display)
# menu.add_command(label = "Exit", command = root.quit)
# root.config(menu = menu)

#windowborder
window = Frame(root, height = 802, width = 1072, highlightthickness = 2, highlightbackground = bgColor, bg = bgColor)
window.pack()

#statusBar
StatusBar = Frame(window, height = 20, bd = 1, relief = SUNKEN)
StatusBar.pack(fill = X, side = BOTTOM)
StatusL = Label(StatusBar, text = "Status: ", width = 30, anchor = W)
StatusL.pack(side = LEFT)
UptimeL = Label(StatusBar, text = "Uptime: ", width = 30, anchor = W)
UptimeL.pack(side = LEFT)

#body
Body = Canvas(window, height = 300, width = 1070, bd = 0, bg = bgColor, highlightthickness = 0)
Body.pack(side = TOP, fill = BOTH)
Body.pack_propagate(False)
logFrame = Frame(window, bd = 0, bg = bgColor)
logFrame.pack(side = BOTTOM, fill = X)

#images
MainBGRAW = Image.open("GUI/starry.jpg")
MainBGRAW = MainBGRAW.resize((1080,510), Image.ANTIALIAS)
MainBGIMG = ImageTk.PhotoImage(MainBGRAW)

MainNabiRAW = Image.open("Expressions/NabiV2/11.png")
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

# logMenu = Frame(logFrame, height = 20, bg = None, bd = 1, padx = 2, pady = 2)
NabiStart = Button(Body, bd = 0, cursor = "hand2", text = "Start", bg = "dark green", fg = "black", font = dFont, command = startNabiCode, padx = 2, pady = 2)
NabiClose = Button(Body, bd = 0, cursor = "hand2", text = "Stop", bg = "dark red", fg = "black", font = dFont, command = closeNabiCode, padx = 2, pady = 2)

logScroll = Scrollbar(logFrame, orient = VERTICAL)
Log = Listbox(logFrame, bd = 0, highlightthickness = 0, height = 15, font = dFont, bg = "#1a1a1a", fg = "white", yscrollcommand=logScroll.set, activestyle = NONE)
logScroll.config(command=Log.yview)

CommandsBG = None
CommandsInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "This is the commands section... yea.... where everyone finds their commands to spam in chat... Idk what else to say XD")
# CommandsTree = ttk.Treeview(logFrame, height = 15)

UserBG = None
UserInfo = Message(Body,font = dFont, width = 300, bg = bgColor, fg = "white", text = "User list:")
UserList = Listbox(logFrame, height = 15, font = dFont, bg = "#1a1a1a", fg = "white")

#clock updates
UpStart = time.clock()
UpCurrent = time.clock()
def UDClock():
	updateLog()
	StatusUpdate()
	UptimeUpdate()
	# updateCommands()
	root.after(500, UDClock)
root.after(500, UDClock)

#mainLoop
# subprocess.call([sys.executable, "run.py"])
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

