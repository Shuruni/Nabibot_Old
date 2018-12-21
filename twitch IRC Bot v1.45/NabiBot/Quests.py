import csv, time
from Socket import *


class Quest(object):
	def __init__(self, name, req, options, effects):
		self.name = name
		self.req = req
		self.options = options   #[["", ""], ["", ""], ["", ""]]
		self.effects = effects   #[[0, 0], [0, 0], [0, 0]]
	
	def getName(self):
		return self.name
	
	def getReq(self):
		return self.req
	
	def canTakeQuest(self, job):
		requirement = self.req
		if requirement == None:
			return False
		elif type(requirement) == list:
			for req in requirement:
				prelimOutcome = self.canTakeQuest(req)
				if prelimOutcome == False:
					return False
			return True
		elif type(requirement) == int:
			if job.getLevel() >= requirement:
				return True
			else:
				return False
		elif type(requirement) == str:
			if requirement in job.getCSQ():
				return True
			else:
				return False
		else:
			log("type error in Quest Using requirements")
			return False
	
	def getOptions(self):
		return self.options.deepCopy()
	
	def getEffects(self):
		return self.effects.deepCopy()
	
	def makeChoice(self, choice):
		"""
		choice: str, response key value
		"""
		work = False
		try:
			work = self.options[choice][1]
		except KeyError:
			log(choice + " is not a valid choice!")
		return work
	
	def possibleChoices(self):
		choices = []
		for option in self.options[1:]:
			choices.append(option[0])
		return choices
	
	def parseSend(self, s, text, user):
		cCharLen = 200
		log(len(text))
		if len(text) > cCharLen :
			temp = text
			temp2 = temp.split(". ")
			# log(temp)
			# log(temp2)
			cLen = 0
			combine = ""
			printList = []
			for sentence in temp2:
				sentence += ". "
				if cLen > cCharLen:
					printList.append(combine)
					combine = sentence
					cLen = 0
				else:
					combine += sentence
					cLen = len(combine)
			if cLen != 0:
				printList.append(combine)
			# print(printList)
			for message in printList:
				# print("/w " + user.getName() + " " + message)
				sendMessage(s, "/w " + user.getName() + " " + message)
				time.sleep(2)
				
		else:
			sendMessage(s, "/w " + user.getName() + " " + text)
			time.sleep(2)
	
	def execute(self, user, sckt, choice = None):
		if user.cQuest == None:
			user.cQuest = self
			self.parseSend(sckt, self.options[0], user)
			choices = user.cQuest.possibleChoices()
			sendMessage(sckt, "/w " + user.getName() + " Possible Choices: " + ", ".join(choices))
		elif choice != None:
			message = self.makeChoice(int(choice))
			if message != False:
				user.cQuest = None
				self.parseSend(sckt, message, user)
				self.ExeEfx(user, sckt, self.effects[int(choice)-1])
			else:
				sendMessage(sckt, "/w " + user.getName() + " That isn't an option >w<")
			
	
	def ExeEfx(self, user, sckt, effects):
		message = "/w " + user.getName() + " You "
		if effects[0] > 0:
			user.recieve(effects[1])
			message += "gained " + str(effects[0]) + " coins, and "
		elif effects[0] < 0:
			if user.canPay(abs(effects[0])):
				user.pay(abs(effects[0]))
				message += "lost " + str(abs(effects[0])) + " coins, and "
			else:
				message += "went Broke, and "
				user.Broke()
		message += "gained " + str(effects[1]) + " exp!"
		user.getOccupation().update(sckt, user, effects[1])
		sendMessage(sckt, message)
		time.sleep(1)
		
#	

	
	
class QuestList(object)	:
	def __init__(self, file):
		# self.CK = {"L":200, "SL":300, "N":400, "SH":500, "H":600}
		# self.EK = {"L":40, "SL":60, "N":80, "SH":100, "H":120}
		self.file = file
		self.questList = self.getFromFile()
	
	def getFile(self):
		return self.file
		
	def getQuestList(self):
		return self.questList
		
	def  sendListToFile(self):
		Rows = [["Name:", "Requirements:", "EffectsA:", "EffectsB:", "EffectsC:", "Quest:", "ChoiceA:", "ChoiceB:", "ChoiceC:", "ResultA:", "ResultB:", "ResultC:"]]
		for quest in self.questList:
			toFileList = [quest.getName(), quest.getReq()]
			for effect in quest.getEffects():
				toFileList.append(str(effect))
			toFileList.append(quest.getOptions()[0])
			for option in quest.getOptions()[1:]:
				toFileList.append(option[0])
			for option in quest.getOptions()[1:]:
				toFileList.append(option[1])
			toFileList.append("#")
			Rows.append(toFileList.deepCopy())
		qS = 0
		with open(self.file, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for questData in Rows:
				writer.writerow(questData)
				qS +=1
		log(str(qS) + " quests saved")
	
	def GQ(self, name):
		for quest in self.questList:
			if quest.getName() == name:
				return quest
		return False
	
	def getFromFile(self):
		# log("Loading Quest list from " + self.file + "...")
		quests = []
		questsLoaded = 0
		currentRow = 1
		with open(self.file, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if currentRow == 1:
					pass
				else:
					name = row[0]
					req = eval(row[1])
					options = [row[5], [row[6], row[9]], [row[7], row[10]], [row[8], row[11]]]
					effects = [eval(row[2]), eval(row[3]), eval(row[4])]
					quests.append(Quest(name, req, options, effects))
					questsLoaded += 1
				currentRow += 1
		log(str(questsLoaded) + " Quests loaded from file")
		return quests[:]
#

# class food(ingredients):
	# def __init__(self, shoppingList):
		# self.ingredients = shoppingList.sort()
		# self.recipie = None
		# self.ChanceOfSucess = 9001.00
		# self.ActualChanceOfSucess = 0.009001
	# def Cook(self):
		# result = ""
		# for ingredient in ingredients:
			# result.append("pie")
		# for rule in recipie:
			# del rule
		# return False



class Event(object):
	def __init__(self, name, effects, event):
		self.name = name
		self.event = event
		self.effects = effects
	
	def getName(self):
		return self.name
		
	def getEvent(self):
		return self.event
		
	def getEffects(self):
		return self.effects[:]
	
	def execute(self, user, sckt):
		self.parseSend(sckt, self.event, user)
		self.ExeEfx(user, sckt)
	
	def parseSend(self, s, text, user):
		cCharLen = 200
		log(len(text))
		if len(text) > cCharLen :
			temp = text
			temp2 = temp.split(". ")
			# print(temp)
			# print(temp2)
			cLen = 0
			combine = ""
			printList = []
			for sentence in temp2:
				sentence += ". "
				if cLen > cCharLen:
					printList.append(combine)
					combine = sentence
					cLen = 0
				else:
					combine += sentence
					cLen = len(combine)
			if cLen != 0:
				printList.append(combine)
			# print(printList)
			for message in printList:
				# print("/w " + user.getName() + " " + message)
				sendMessage(s, "/w " + user.getName() + " " + message)
				time.sleep(2)
				
		else:
			sendMessage(s, "/w " + user.getName() + " " + text)
			time.sleep(2)
	
	def ExeEfx(self, user, sckt):
		message = "/w " + user.getName() + " You "
		if self.effects[0] > 0:
			user.recieve(self.effects[1])
			message += "gained " + str(self.effects[0]) + " coins, and "
		elif self.effects[0] < 0:
			if user.canPay(abs(self.effects[0])):
				user.pay(abs(self.effects[0]))
				message += "lost " + str(abs(self.effects[0])) + " coins, and "
			else:
				message += "went Broke, and "
				user.Broke()
		message += "gained " + str(self.effects[1]) + " exp!"
		user.getOccupation().update(sckt, user, self.effects[1])
		sendMessage(sckt, message)
		time.sleep(1)


class EventList(object)	:
	def __init__(self, file):
		self.CK = {"L":100, "SL":200, "N":300, "SH":400, "H":500}
		self.EK = {"L":20, "SL":40, "N":60, "SH":80, "H":100}
		self.file = file
		self.eventList = self.getFromFile()
	
	def getFile(self):
		return self.file
		
	def getEventList(self):
		return self.eventList
		
	def  sendListToFile(self):
		for event in self.eventList:
			toFileList = [quest.getName(), str(self.getEffects()), quest.getEvent()]
		eS = 0
		with open(self.file, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			first = True
			for eventData in toFileList:
				if first:
					continue
				else:
					writer.writerow(eventData)
					eS +=1
		log(str(eS) + " events saved")
	
	def GE(self, name):
		for event in self.eventList:
			if event.getName() == name:
				return event
		return False
	
	def getFromFile(self):
		# log("Loading Event list from " + self.file + "...")
		events = []
		eventsLoaded = 0
		currentRow = 1
		with open(self.file, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if currentRow == 1:
					pass
				else:
					name = row[0]
					Cs = ""
					temp = row[1]
					if row[1][0] == "-":
						Cs = "-"
						temp = row[1][1:]
					Coins = int(Cs + str(self.CK[temp]))
					Exp = self.EK[row[2]]
					effects = [Coins, Exp]
					event = row[3]
					events.append(Event(name, effects, event))
					eventsLoaded += 1
				currentRow += 1
		log(str(eventsLoaded) + " Events loaded from file")
		return events[:]







































				