import csv, time
from Socket import *


class Quest(object):
	def __init__(self, name, req, parts, options, choices = []):
		self.name = name
		self.req = req
		self.options = options   #[{"":"", "":"", "":""}, {"":"", "":"", "":""}]
		self.choices = choices
		self.part = 0
		self.parts = parts
	
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
			print("type error in Quest Using requirements")
			return False
	
	def getOptions(self):
		return self.options[:]
	
	def getParts(self):
		return self.parts
	
	def getChoices(self):
		return self.choices[:]
	
	def makeChoice(self, part, choice):
		"""
		part: int, index of current question
		choice: str, response key value
		"""
		work = False
		try:
			work = self.options[part][choice]
			self.choices.append(choice)
		except KeyError:
			print(choice + " is not a valid choice or " + str(part) + " is not a valid part")
		return work
	
	def possibleChoices(self):
		return self.options[self.part].keys()
	
	def parseSend(self, s, text, user):
		cCharLen = 200
		print(len(text))
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
	
	def execute(self, user, sckt, choice = None):
		if user.cQuest == None:
			user.cQuest = self
			self.parseSend(sckt, self.options[0], user)
			self.part += 1
		elif choice != None:
			message = self.makeChoice(self.part, choice.lower())
			if message != False:
				# try:
				data = eval(message)
				self.part += 1
				if type(data) == list:
					msg = data[1]
					effects = data[0]
					user.cQuest = None
					self.part = 0
				self.parseSend(sckt, msg, user)
				self.ExeEfx(user, sckt, effects)
				
			else:
				sendMessage(sckt, "/w " + user.getName() + " That isn't an option >w<")
			
	
	def ExeEfx(self, user, sckt, effects):
		for effect in effects:
			if effect[0] == "coins":
				if effect[1] > 0:
					user.recieve(effect[1])
					sendMessage(sckt, "/w " + user.getName() + " You gained " + str(effect[1]) + " coins!")
					time.sleep(1)
				elif effect[1] < 0:
					if user.canPay(abs(effect[1])):
						user.pay(abs(effect[1]))
						sendMessage(sckt, "/w " + user.getName() + " You lost " + str(effect[1]) + " coins!")
						time.sleep(1)
					else:
						user.Broke()
			elif effect[0] == "exp":
				if effect[1] > 0:
					sendMessage(sckt, "/w " + user.getName() + " You gained " + str(effect[1]) + " exp!")
					user.getOccupation().update(sckt, user, effect[1])
					time.sleep(1)
				else:
					sendMessage(sckt, "/w " + user.getName() + " You lost " + str(effect[1]) + " exp!")
					user.getOccupation().update(sckt, user, effect[1])
					time.sleep(1)
			else:
				print("invalid effect")
		
#	

	
	
class QuestList(object)	:
	def __init__(self, file):
		self.file = file
		self.questList = self.getFromFile()
	
	def getFile(self):
		return self.file
		
	def getQuestList(self):
		return self.questList
		
	def  sendListToFile(self):
		toFileList = []
		for quest in self.questList:
			data = [quest.getName(), quest.getReq(), self.getParts()]
			for option in self.getOptions():
				if type(option) == str:
					toFileList.append(option)
				else:
					for key in option.keys():
						toFileList.append(key)
						toFileList.append(option[key])
			toFileList.append("ENDOFFILESHURUNI")
		qS = 0
		with open(self.file, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			first = True
			for questData in toFileList:
				if first:
					continue
				else:
					writer.writerow(questData)
					qS +=1
		print(str(qS) + " quests saved")
	
	def GQ(self, name):
		for quest in self.questList:
			if quest.getName() == name:
				return quest
		return False
	
	def getFromFile(self):
		print("Loading Quest list from " + self.file + "...")
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
					choices = eval(row[2]) # will not be used atm, maybe later
					options = [row[3]]
					pointer = "key"
					IPointer = 0
					CNum = 4
					parts = 0
					while True:
						try:
							OptionsNum = row[CNum]
							IPointer += int(OptionsNum)
						except:
							break
						parts+= 1
						CNum += 1
						tempDict = {}
						tempKey = None
						print(int(OptionsNum))
						for dictVals in range(int(OptionsNum)):
							# print(dictVals)
							# print row[dictVals + IPointer-1]
							if pointer == "key":
								tempKey = row[dictVals + IPointer-1].lower()
								pointer = "value"
							else:
								tempDict[tempKey[:]] = row[dictVals + IPointer-1]
								tempKey = None
								pointer = "key"
							CNum += 1
						options.append(tempDict.copy())
					quests.append(Quest(name, req, parts, options))
					questsLoaded += 1
				currentRow += 1
		print(str(questsLoaded) + " Quests succesfully loaded from file! ")
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
		print(len(text))
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
		for effect in self.effects:
			if effect[0] == "coins":
				if effect[1] > 0:
					user.recieve(effect[1])
					sendMessage(sckt, "/w " + user.getName() + " You gained " + str(effect[1]) + " coins!")
					time.sleep(1)
				elif effect[1] < 0:
					if user.canPay(abs(effect[1])):
						user.pay(abs(effect[1]))
						sendMessage(sckt, "/w " + user.getName() + " You lost " + str(effect[1]) + " coins!")
						time.sleep(1)
					else:
						user.Broke()
			elif effect[0] == "exp":
				if effect[1] > 0:
					sendMessage(sckt, "/w " + user.getName() + " You gained " + str(effect[1]) + " exp!")
					user.getOccupation().update(sckt, user, effect[1])
					time.sleep(1)
				else:
					sendMessage(sckt, "/w " + user.getName() + " You lost " + str(effect[1]) + " exp!")
					user.getOccupation().update(sckt, user, effect[1])
					time.sleep(1)
			else:
				print("invalid effect")


class EventList(object)	:
	def __init__(self, file):
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
		print(str(eS) + " events saved")
	
	def GE(self, name):
		for event in self.eventList:
			if event.getName() == name:
				return event
		return False
	
	def getFromFile(self):
		print("Loading Event list from " + self.file + "...")
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
					effects = eval(row[1])
					event = row[2]
					events.append(Event(name, effects, event))
					eventsLoaded += 1
				currentRow += 1
		print(str(eventsLoaded) + " Events succesfully loaded from file! ")
		return events[:]







































				