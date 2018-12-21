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
#

class Command(object):
	def __init__(self, command, commandFunct, commandSyntax):
		self.command = command #Name of the command to look for ex. "!loli" ex. "!keyboard" ex. "!hello"
		self.function = commandFunct #pass in function that excecutes said command in str format
		self.syntax = commandSyntax #List of the types and keywords to pass into the function for said command
		if self.syntax == [""]:
			self.syntax = []
		self.nLength = len(self.command)
		self.sIter = range(len(self.syntax))
	
	def getName(self):
		return self.command
	
	def getFunction(self):
		return self.function
	
	def getSyntax(self):
		return self.syntax[:]
		
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
						continue
					elif int == self.syntax[oIndex] or float == self.syntax[oIndex]:
						try:
							float(options[oIndex])
						except:
							return False
					else:
						if self.syntax[oIndex] == options[oIndex]:
							return True
						else:
							return False
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
	
	def getListFromFile(self):
		file = self.file
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
					if "str" in commandSyntax or "int" in commandSyntax:
						for i in range(len(commandSyntax)):
							if commandSyntax[i] == "str" or commandSyntax[i] == "int":
								commandSyntax[i] = eval(commandSyntax[i])
					commands.append([row[0],Command(row[0], row[1], commandSyntax[:])])
					comLoaded += 1
				currentRow += 1
		print(str(comLoaded) + " commands succesfully loaded from file! (^o^)/")
		return commands[:]
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		