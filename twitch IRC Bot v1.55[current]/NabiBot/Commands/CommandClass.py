# -*- coding: utf-8 -*-
import sys, csv, os


sys.path.append('..')
from Socket import *
from Categories.functions import *
sys.path.remove('..')

def convertCSV(csvfile):
	Clist = []
	from xlsxwriter.workbook import Workbook
	workbook = Workbook("D:/Kuroihi_files/OneDrive/CommandsWeb" + csvfile[8:-4] + '.xlsx')
	worksheet = workbook.add_worksheet()
	allFormat = workbook.add_format({'bottom':True, 'border_color':"#808080", 'bg_color':"#262626", 'font_color':"#6666ff"})
	format = workbook.add_format({'font_size':14, 'bottom':True, 'bg_color':"#262626", 'font_color':"#6666ff", 'border_color':"#808080"})
	formatC = workbook.add_format({'align':"center", 'font_size':14, 'bottom':True, 'bg_color':"#262626", 'font_color':"#6666ff", 'border_color':"#808080"})
	formatCH = workbook.add_format({'bold':True, 'align':"center", 'font_size':14, 'bottom':True, 'bg_color':"#262626", 'font_color':"#6666ff", 'border_color':"#808080"})
	formatHead = workbook.add_format({'bold':True, 'font_size':14, 'bottom':True, 'bg_color':"#262626", 'font_color':"#6666ff", 'border_color':"#808080"})
	worksheet.set_default_row(18)
	with open(csvfile, 'rb') as f:
		reader = csv.reader(f)
		comNum = 0
		for i in reader:
			comNum += 1
	with open(csvfile, 'rb') as f:
		reader = csv.reader(f)
		for r, row in enumerate(reader):
			for c, col in enumerate(row):
				if len(row) > len(Clist): #or comNum-1 == r:
					if c == 2:
						# Clist.append(len(col)+5)
						Clist.append(0)
						worksheet.write(r, c, col.decode("utf-8"), formatCH)
					else:
						# Clist.append(len(col)+5)
						Clist.append(0)
						worksheet.write(r, c, col.decode("utf-8"), formatHead)
				elif c == 2:
					# Clist[c] = max(Clist[c], len(col)+5)
					worksheet.write(r, c, col.decode("utf-8"), formatC)
				else:
					# Clist[c] = max(Clist[c], len(col)+5)
					worksheet.write(r, c, col.decode("utf-8"), format)
	# Clist = [16, ]
	Clist = [17, 20, 20, 74, 25]
	for column in range(len(Clist)):
		worksheet.set_column(column, column, Clist[column], allFormat)
	workbook.close()


# instantiate all of the imported function classes
dummy = dummy()
Nabi = Nabi()
level = level(Nabi)
fun = fun(Nabi)
debug = debug()
coin = coin(Nabi)
command = command()
Osu = Osu()
math = math()
Standings = Standings()
Occupations = Occupations()
Quest = Quest()
Event = Event()
#

class Command(object):
	def __init__(self, command, commandFunct, commandSyntax, cooldown, description = "dummy"):
		self.command = command #Name of the command to look for ex. "!loli" ex. "!keyboard" ex. "!hello"
		self.function = commandFunct #pass in function that excecutes said command in str format
		self.syntax = commandSyntax #List of the types and keywords to pass into the function for said command
		if self.syntax == [""]:
			self.syntax = []
		self.nLength = len(self.command)
		self.sIter = range(len(self.syntax))
		self.cooldown = cooldown
		self.description = description
	
	def getName(self):
		return self.command
	
	def getFunction(self):
		return self.function
	
	def getSyntax(self):
		return self.syntax[:]
		
	def addOption(self, option):
		self.syntax.append(option)
	
	def remOption(self, option):
		result = True
		self.syntax.reverse()
		try:
			self.syntax.remove(option)
		except:
			result = False
		self.syntax.reverse()
		return result
		
	def getCooldown(self):
		return self.cooldown
		
	def getDescription(self):
		return self.description
	
	def execute(self, s, options, user, ul, comList):
		#run this if self.check(command, options) == True
		parsed = self.function + "s, options, user, ul, comList)"
		#print parsed
		return eval(parsed)
		
	def check(self, command, options):
		#run in main loop; what to look for in comments to excecute said command; returns True if comment matches command, False otherwise
		# print self.command + command
		if self.command == command:
			# print str(len(options)) + str(len(self.syntax))
			if len(options) == len(self.syntax):
				for oIndex in self.sIter:
					if str == self.syntax[oIndex]:
						# print("it is a string")
						continue
					elif int == self.syntax[oIndex]:
						try:
							int(options[oIndex])
						except:
							# print("it isn't and int")
							return False
						# print("it is an int")
					elif float == self.syntax[oIndex]:
						try:
							float(options[oIndex])
						except:
							# print("it isn't a float")
							return False
						# print("it is a float")
					elif "addCom" == self.syntax[oIndex]:
						return True
					elif "User" == self.syntax[oIndex]:
						continue
					else:
						# print("it ignores everything wtf")
						if self.syntax[oIndex] == options[oIndex]:
							# print("syntax matches")
							continue
						else:
							return False
				return True
			elif "addCom" in self.syntax or "remCom" in self.syntax:
				# print "this is the Add or Remove Command"
				try:
					if options[1] != "":
						return True
					else:
						return False
				except:
					return False
			else:
				return False
		else:
			return False
		
		
class CommandList(object):
	def __init__(self, file):
		self.file = "Commands/" + file
		#self.commandsDict = self.getDictFromFile(self.file)
		self.commandsList = self.getListFromFile()
	
	def getList(self):
		return self.commandsList[:]
	
	def isInList(self, commandName):
		for command in self.commandsList[:]:
			if command[0] == commandName:
				return command
		return False
	
	def isDummy(self, name):
		command = self.isInList(name)
		if command != False:
			if "dummy.dummy" in command[1].getFunction():
				return command[1]
			else:
				return False
		else:
			return False
	
	def updateList(self):
		self.commandsList = self.getListFromFile()
	
	def addCom(self, name, message, override = False, cooldown = 10):
		command = self.isInList(name)
		if command == False:
			msg = message.encode('string-escape')
			print(msg)
			if message[0] == "/":
				msg = "!" + message[1:]
			if "\"" in msg:
				msg = msg.replace("\"", "\\\"")
			if override:
				msg = message
			log("adding Command " + name + " to commands list...")
			self.commandsList.append([name, Command(name, "dummy.dummy(\"" + msg + "\", ", [], cooldown)])
			self.sendToFile()
			log(name + " succesfully added!")
			return True
		else:
			log(name + " already exists in commands list thus cannot be added")
			return False
		
	def remCom(self, name):
		command = self.isInList(name)
		if command != False:
			if "dummy.dummy" in command[1].getFunction():
				log("removing " + name + " from the commands list...")
				self.commandsList.remove(command)
				self.sendToFile()
				log(name + " succesfully removed!")
				return True
			else:
				log("cannot remove non-dummy commands from commands list")
				return "ND"
		else:
			log(name + " is not in the commands list thus cannot be removed")
			return False
	
	def getListFromFile(self):
		file = self.file
		# log("Loading Commands list from " + file + "..." )
		commands = []
		comLoaded = 0
		currentRow = 1
		with open(file, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if currentRow == 1:
					pass
				else:
					name = row[0]
					if row[2][-5:].lower() == " sec.":
						cooldown = int(row[2][:-5])
					elif row[2] != "":
						cooldown = int(row[2])
					else:
						cooldown = 10
					# FunctionList = []
					# SyntaxList = []
					# Funct = True
					# for optionCell in row[2:]:
						# if Funct:
							# FunctionList.append(optionCell.decode("utf-8", "replace").encode("utf-8", "replace"))
							# Funct = False
						# else:
							# commandSyntax = optionCell.split(", ")
							# for i, o in enumerate(commandSyntax):
								# if o == "str" or o == "int" or o == "float":
									# commandSyntax[i] = eval(o)
								# elif o = "User":
									# commandSyntax[i] = str
							# SyntaxList.append(commandSyntax[:])
					# if len(FunctionList) != len(SyntaxList):
						# print("failed to load command on row " + currentRow)
						# currentRow += 1
						# continue
					function = row[4].decode("utf-8", "replace").encode("utf-8", "replace")
					description = row[3].decode("utf-8", "replace").encode("utf-8", "replace")
					commandSyntax = row[1].split("  ")
					for i, o in enumerate(commandSyntax):
						if o == "str" or o == "int" or o == "float":
							commandSyntax[i] = eval(o)
					commands.append([name, Command(name, function, commandSyntax[:], cooldown, description)])
					comLoaded += 1
				currentRow += 1
		log(str(comLoaded) + " Commands loaded from file")
		return commands[:]
	def sendToFile(self):
		# log("Writing Commands to file...")
		toFileList = [["Command:", "Modifiers:", "Cooldown:", "Description:", "CodeCommand:"]]
		for command in self.commandsList:
			syntax = []
			for e in command[1].getSyntax():
				if e == int:
					syntax.append("int")
				elif e == float:
					syntax.append("float")
				elif e == str:
					syntax.append("str")
				else:
					syntax.append(e)
			name = command[0].decode("utf-8", "replace").encode("utf-8", "replace")
			cooldown = str(command[1].getCooldown()) + " sec."
			function = command[1].getFunction().decode("utf-8", "replace").encode("utf-8", "replace")
			description = command[1].getDescription().decode("utf-8", "replace").encode("utf-8", "replace")
			toFileList.append([name, "  ".join(syntax), cooldown, description, function])
		cS = 0
		with open(self.file, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for cmdData in toFileList:
				writer.writerow(cmdData)
				cS +=1
		log(str(cS) + " Commands saved")
		convertCSV(self.file)
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		