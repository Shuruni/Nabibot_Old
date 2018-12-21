import sys
import csv


sys.path.append('..')
from Socket import *
from Categories.functions import *
sys.path.remove('..')

# instantiate all of the imported function classes
dummy = dummy()
fun = fun()
level = level()
Nabi = Nabi()
debug = debug()
coin = coin()
command = command()
Osu = Osu()
math = math()
#

class Command(object):
	def __init__(self, command, commandFunct, commandSyntax, cooldown):
		self.command = command #Name of the command to look for ex. "!loli" ex. "!keyboard" ex. "!hello"
		self.function = commandFunct #pass in function that excecutes said command in str format
		self.syntax = commandSyntax #List of the types and keywords to pass into the function for said command
		if self.syntax == [""]:
			self.syntax = []
		self.nLength = len(self.command)
		self.sIter = range(len(self.syntax))
		self.cooldown = cooldown
	
	def getName(self):
		return self.command
	
	def getFunction(self):
		return self.function
	
	def getSyntax(self):
		return self.syntax[:]
		
	def getCooldown(self):
		return self.cooldown
	
	def execute(self, s, options, user, ul, comList):
		#run this if self.check(command, options) == True
		parsed = self.function + "s, options, user, ul, comList)"
		#print parsed
		eval(parsed)
		
	def check(self, command, options):
		#run in main loop; what to look for in comments to excecute said command; returns True if comment matches command, False otherwise
		# print self.command + command
		if self.command == command:
			# print str(len(options)) + str(len(self.syntax))
			if len(options) == len(self.syntax):
				for oIndex in self.sIter:
					if str == self.syntax[oIndex]:
						print("it is a string")
						continue
					elif int == self.syntax[oIndex]:
						try:
							int(options[oIndex])
						except:
							print("it isn't and int")
							return False
						print("it is an int")
					elif float == self.syntax[oIndex]:
						try:
							float(options[oIndex])
						except:
							print("it isn't a float")
							return False
						print("it is a float")
					elif "addCom" == self.syntax[oIndex]:
						return True
					else:
						# print("it ignores everything wtf")
						if self.syntax[oIndex] == options[oIndex]:
							print("syntax matches")
							continue
						else:
							return False
				return True
			elif "addCom" in self.syntax or "remCom" in self.syntax:
				print "this is the Add or Remove Command"
				return True
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
	
	def updateList(self):
		self.commandsList = self.getListFromFile()
	
	def addCom(self, name, message, override = False, cooldown = 60):
		command = self.isInList(name)
		if command == False:
			if override:
				msg = message
			else:
				msg = message.replace("/", "!")
			print("adding Command " + name + " to commands list...")
			self.commandsList.append([name, Command(name, "dummy.dummy(\"" + msg + "\", ", [], cooldown)])
			self.sendToFile()
			print(name + " succesfully added!")
			return True
		else:
			print(name + " already exists in commands list thus cannot be added")
			return False
		
	def remCom(self, name):
		command = self.isInList(name)
		if command != False:
			if "dummy.dummy" in command[1].getFunction():
				print("removing " + name + " from the commands list...")
				self.commandsList.remove(command)
				self.sendToFile()
				print(name + " succesfully removed!")
				return True
			else:
				print("cannot remove non-dummy commands from commands list")
				return "ND"
		else:
			print(name + " is not in the commands list thus cannot be removed")
			return False
	
	def getListFromFile(self):
		file = self.file
		print("Loading Commands list from " + file + "..." )
		commands = []
		comLoaded = 0
		currentRow = 1
		with open(file, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if row[1] == '' or row[0] == '':
					print("failed to load command on row " + str(currentRow) + "! please check that the syntax in the csv file is correct.")
				else:
					commandSyntax = row[2].split(", ")
					if "str" in commandSyntax or "int" in commandSyntax or "float" in commandSyntax:
						for i in range(len(commandSyntax)):
							if commandSyntax[i] == "str" or commandSyntax[i] == "int" or commandSyntax[i] == "float":
								commandSyntax[i] = eval(commandSyntax[i])
					if len(row) == 4:
						try:
							cooldown = int(row[3])
						except:
							cooldown = 60
					else:
						cooldown = 60
					name = row[0]
					function = row[1].decode("utf-8", "replace").encode("utf-8", "replace")
					commands.append([name, Command(name, function, commandSyntax[:], cooldown)])
					comLoaded += 1
				currentRow += 1
		print(str(comLoaded) + " Commands succesfully loaded from file! (^o^)/")
		return commands[:]
	def sendToFile(self):
		print("Writing Commands to file...")
		toFileList = []
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
			function = command[1].getFunction().decode("utf-8", "replace").encode("utf-8", "replace")
			toFileList.append([name, function, ", ".join(syntax)])
		cS = 0
		with open(self.file, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for cmdData in toFileList:
				writer.writerow(cmdData)
				cS +=1
		print(str(cS) + " Commands saved")
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		