from Tkinter import *
# from PIL import Image, ImageTk
import ttk, tkFont, random, os, sys, csv, time, subprocess, ctypes, datetime


def Nothing():
	print("k")
	
def endGUI(root):
	root.quit()
		
def Verbose(LogSimple, Log, logScroll, VerboseCheck):
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
		
def junkLog(Log):
	with open("GUI/Log.nabi", "w") as f:
		junk = random.choice(["mayo", "Kappa", "Maji?", "Lolis", "Nabi", "Error", "42", "PogChamp", "what is going on?", "spam", "LOG RAID!", "WTF!", "!shurucode"])
		Log.insert(END, junk)
		
def updateLog(Log, LogSimple):
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

def PopulateCommands(CommandsList):
	"""populates commands in CommandsList from Comamnds file"""
	file = "Commands/CommandList.csv"
	commands = []
	comLoaded = 0
	currentRow = 1
	maxLength = [0, 0, 0]
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if currentRow == 1:
				pass
			else:
				name = row[0]
				if maxLength[0] < len(name):
					maxLength[0] = len(name)
				if row[2][-5:].lower() == " sec.":
					cooldown = int(row[2][:-5])
				elif row[2] != "":
					cooldown = int(row[2])
				else:
					cooldown = 10
				# if maxLength[2] < len(str(cooldown)):
					# maxLength[2] = len(str(cooldown))
				function = row[4].decode("utf-8", "replace").encode("utf-8", "replace")
				description = row[3].decode("utf-8", "replace").encode("utf-8", "replace")
				commandSyntax = row[1].split("  ")
				if maxLength[1] < len(",".join(commandSyntax[:])):
					maxLength[1] = len(",".join(commandSyntax[:]))
				# for i, o in enumerate(commandSyntax):
					# if o == "str" or o == "int" or o == "float":
						# commandSyntax[i] = eval(o)
				commands.append([name, ",".join(commandSyntax[:]), description]) #, str(cooldown)
				comLoaded += 1
			currentRow += 1
	for command in commands:
		if len(command[0]) < maxLength[0]:
			space = ""
			for i in range(len(command[0]), maxLength[0]):
				space += " "
			command[0] = command[0] + space
		if len(command[1]) < maxLength[1]:
			space = ""
			for i in range(len(command[1]), maxLength[1]):
				space += " "
			command[1] = command[1] + space
		# if len(command[2]) < maxLength[2]:
			# space = ""
			# for i in range(len(command[2]), maxLength[2]+1):
				# space += " "
			# command[2] = command[2] + space
		CommandsList.insert(END, "   ".join(command))
		
	
def PopulateUsers(UserList):
	"""populates users in UserList from User file (eventually, active users from twitchAPI or Nabi's active user list)"""
	file = "Users/UserList.csv"
	users = []
	usersLoaded = 0
	currentRow = 1
	maxLength = [0, 0, 0]
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '' or row[5] == '':
				log("failed to load user on row " + str(currentRow) + "! please check that the syntax in the csv file is correct.")
			else:
				name = row[0]
				# walletRaw = eval(row[1])
				# wallet = Coins.Wallet(walletRaw[0], walletRaw[1], walletRaw[2])
				# level = row[2]
				# exp = row[3]
				standing = row[4]
				occupation = row[5]
				if maxLength[0] < len(name):
					maxLength[0] = len(name)
				if maxLength[1] < len(standing):
					maxLength[1] = len(standing)
				if maxLength[2] < len(occupation):
					maxLength[2] = len(occupation)
				users.append([name, standing, occupation])
				usersLoaded += 1
			currentRow += 1
	for user in users:
		if len(user[0]) < maxLength[0]:
			space = ""
			for i in range(len(user[0]), maxLength[0]):
				space += " "
			user[0] = user[0] + space
		if len(user[1]) < maxLength[1]:
			space = ""
			for i in range(len(user[1]), maxLength[1]):
				space += " "
			user[1] = user[1] + space
		if len(user[2]) < maxLength[2]:
			space = ""
			for i in range(len(user[2]), maxLength[2]):
				space += " "
			user[2] = user[2] + space
		UserList.insert(END, "   ".join(user))

def UptimeUpdate(UptimeL, UpStart, UpCurrent):
	cTime = UpCurrent - UpStart
	m, sec = divmod(cTime, 60)
	h, m = divmod(m, 60)
	Uptime = "%d hours %d min. %d sec." % (h, m, sec)
	if Uptime[8] == "0": Uptime = Uptime[15:]
	elif Uptime[0] == "0": Uptime = Uptime[8:]
	UptimeL.configure(text = "Uptime: " + Uptime)
	
def StatusUpdate(StatusL, UpStart, UpCurrent):
	with open("GUI/Status.nabi", "r") as f:
		data = f.read()
		StatusL.configure(text = "Status: " + data)
	if data != "Running":
		UpStart = time.clock()
	UpCurrent = time.clock()
	return UpCurrent, UpStart
	
def OverlayStatus(OverlayStatusL):
	with open("GUI/OverlayStatus.nabi", "r") as f:
		data = f.read()
		OverlayStatusL.configure(text = "Overlay: " + data)
		
def CrashLogging(Log):
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
		except IndexError:
			for line in d:
				Log.insert(END, line)
				Log.see(END)
		Log.selection_clear(0,END)
		f.seek(0)
		f.truncate()
		

	
#






























