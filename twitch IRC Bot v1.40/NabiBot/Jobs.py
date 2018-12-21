import random, time
from Quests import *
from Socket import *
FirstTier = ["Scavenger", "Farmer", "Writer", "Student", "Bartender", "Street_Performer", "Apprentice", "Thief", "Outsider", "Lesser_Demon", "Adventurer", "Mechanic", "Linguist", "Peddler"]
SecondTier = ["Lumberjack", "Soldier", "Librarian", "Scholor", "Server", "Actor", "Miko", "Gangster", "Horseman", "Greater_Demon", "Mercenary", "Mason", "Translator", "Trader"]
ThirdTier = ["Fisherman", "Captain", "Accountant", "Disciple", "Culinary_Attendant", "Dancer", "Priest", "Assassin", "Beast_Tamer", "Elite_Demon", "Freelancer", "Blacksmith", "Judge", "Innkeeper"]
FourthTier = ["Hunter", "General", "Advisor", "Teacher", "Chef", "Idol", "Oracle", "Executioner", "Summoner", "Demon_Lord", "Hero", "Craftsman", "Supreme_Justice", "Banker"]
SpecialTierAvailable = ["King", "Queen", "Creator", "Lesser_God"]
AvailableOccList = ["Scavenger", "Lumberjack", "Fisherman", "Hunter", "Farmer", "Soldier", "Captain", "General", "Writer", "Librarian", "Accountant", "Advisor", "Student", "Scholar", "Disciple", "Teacher", "Bartender", "Server", "Culinary_Attendant", "Chef", "Street_Performer", "Actor", "Dancer", "Idol", "Apprentice", "Miko", "Priest", "Oracle", "King", "Queen", "Thief", "Gangster", "Assassin", "Executioner", "Outsider", "Horseman", "Beast_Tamer", "Summoner", "Lesser_Demon", "Greater_Demon", "Elite_Demon", "Demon_Lord", "Adventurer", "Mercenary", "Freelancer", "Hero", "Mechanic", "Mason", "Blacksmith", "Craftsman", "Linguist", "Translator", "Judge", "Supreme_Justice", "Peddler", "Trader", "Innkeeper", "Banker"]
OccupationsList = ("Scavenger", "Lumberjack", "Fisherman", "Hunter", "Farmer", "Soldier", "Captain", "General", "Writer", "Librarian", "Accountant", "Advisor", "Student", "Scholar", "Disciple", "Teacher", "Bartender", "Server", "Culinary_Attendant", "Chef", "Street_Performer", "Actor", "Dancer", "Idol", "Apprentice", "Miko", "Priest", "Oracle", "King", "Queen", "Thief", "Gangster", "Assassin", "Executioner", "Outsider", "Horseman", "Beast_Tamer", "Summoner", "Lesser_Demon", "Greater_Demon", "Elite_Demon", "Demon_Lord", "Adventurer", "Mercenary", "Freelancer", "Hero", "Mechanic", "Mason", "Blacksmith", "Craftsman", "Linguist", "Translator", "Judge", "Supreme_Justice", "Peddler", "Trader", "Innkeeper", "Banker")
SpecialTierList = ("King", "Queen", "Creator", "Lesser_God") #LesserGod = Moderator, Creator = Shuruni, King & Queen = only one of each; income equivalent to average income of all active users

QLO = QuestList("Jobs/Quests.csv")
Events = EventList("Jobs/Events.csv")


class Occupation(object):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 0, IUP = 0, ELOW = 0, EUP = 0):
		"""
		REDEFINE:
			self.name
			self.LVFN
			self.rankUpReq
			self.Squests
			self.Cquests
			self.Events
			self.NextJob
			
		__init__ variables:
			exp: defines self.exp
			level: defines self.level
			CSQ: defines self.CSQ
			Icur: current Income
			Ecur: current Expenses
			ILOW: lower bound for range of added income
			IUP: upper bound for range of added income
			ELOW: lower bound for range of added expenses
			EUP: upper bound for range of added expenses
		Internal variables:
			self.name: str, Name of Occupation, MUST BE THE EXACT NAME OF THE CLASS, space parsing takes places in get fuctions
			self.income: int, should be a random.randrange(lowerBound, upperBound)
			self.expenses: int, should be a random.randrange(lowerBound, upperBound)
			self.exp: int, exp collected while user has had this occupation
			self.level: int, current Level of job class
			self.LVFN: str, contains function defining required exp for i=level
			self.rankUpReq: int if level requirement, str if quest requirement, list if multiple
			self.Squests: list of Quest(object), list of story quests
			self.Cquests: list of Quest(object), list of common quests
			self.Events: list of Event(object), list of events
			self.CSQ: list of Quest(object), list of completed story quests
			self.NextJob: str, name of next Class after this Class when self.rankUpReq is met; MUST BE THE EXACT NAME OF THE CLASS, or NoneType
		"""
		self.name = "Occupation"  #str, Name of Occupation, MUST BE THE EXACT NAME OF THE CLASS, space parsing takes places in get fuctions
		self.income = random.randrange(ILOW, IUP) + Icur #int, should be a random.randrange(lowerBound, upperBound)
		self.expenses = random.randrange(ELOW, EUP) + Ecur  #int, should be a random.randrange(lowerBound, upperBound)
		self.exp = exp  #int, exp collected while user has had this occupation
		self.level = level  #int, current Level of job class
		self.LVFN = "(18*(self.level-1)^2)+80" #str, contains function defining required exp for i=level
		self.rankUpReq = None  #int if level requirement, str if quest requirement, list if multiple
		self.Squests = []  #list of Quest(object), list of story quests
		self.Cquests = []  #list of Quest(object), list of common quests
		self.Events = []  #list of Event(object), list of events
		self.CSQ = []  #list of Quest(object), list of completed story quests
		self.NextJob = None  #str, name of next Class after this Class when self.rankUpReq is met; MUST BE THE EXACT NAME OF THE CLASS, or NoneType
	def getParsedName(self):
		temp = self.name[:]
		temp.replace("_", " ")
		return temp
	def getName(self):
		return self.name
	def getIncome(self):
		return self.income
	def getExpenses(self):
		return self.expenses
	def getExp(self):
		return self.exp
	def getLevel(self):
		return self.level
	def getLVFN(self):
		return self.LVFN
	def getRankUpReq(self):
		try:
			return self.rankUpReq[:]
		except:
			return self.rankUpReq
	def getStoryQuests(self):
		return self.Squests[:]
	def getStoryQuestsNames(self):
		temp = []
		for quest in self.Squests:
			temp.append(quest.getName())
		return temp[:]
	def getCommonQuests(self):
		return self.Cquests[:]
	def getCommonQuestsNames(self):
		temp = []
		for quest in self.Cquests:
			temp.append(quest.getName())
		return temp[:]
	def getCSQ(self):
		return self.CSQ[:]
	def getCSQNames(self):
		temp = []
		for quest in self.CSQ:
			temp.append(quest.getName())
		return temp[:]
	def getNextJob(self):
		return self.NextJob
	def getParsedNextJob(self):
		temp = self.NextJob[:]
		temp.replace("_", " ")
		return temp
	
	def randomEvent(self, user, s):
		try:
			choice = random.choice(self.Events)
		except IndexError:
			return False
		Events.GE(choice).execute(user, s)
		return Events.GE(choice)
	
	def randomCQuest(self, user, s):
		for i in range(1000):
			try:	
				choice = random.choice(self.Cquests)
			except IndexError:
				return False
			choiceObj = QLO.GQ(choice)
			canUse = choiceObj.canTakeQuest(self)
			if canUse:
				choiceObj.execute(user, s)
				return choiceObj
			else:
				continue
		return False
	
	def nextSQuest(self, user, s):
		for i in range(1000):
			try:
				choice = random.choice(self.Squests)
			except IndexError:
				return False
			choiceObj = QLO.GQ(choice)
			canUse = choiceObj.canTakeQuest(self)
			if canUse:
				choiceObj.execute(user, s)
				return choiceObj
			else:
				continue
		return False
	
	def expToNextLevel(self):
		#returns a list so that list[0] == [needed, outOfTotal] & list[1] == [current, required]
		nextLevelExp = 0
		reqOutOfExp = 0
		for i in range(self.level+1):
			reqOutOfExp = eval(self.LVFN)
			nextLevelExp += reqOutOfExp
		return [[nextLevelExp - self.exp, reqOutOfExp], [self.exp,nextLevelExp]]
	
	def addExp(self, gainedexp):
		self.exp+=gainedexp
	def checkLevelUp(self, socket, user):
		level = self.getLevel() + 1
		reqExp = self.expToNextLevel()
		if reqExp[1][0] >= reqExp[1][1]:
			self.level+=1
			sendMessage(socket, "Congratulations " + user.getName() + "! You've just advanced to " + self.getParsedName() + " level " + str(self.level) + "! \\(^w^)/")
			time.sleep(0.1)
	def checkJobUp(self, requirement):
		if requirement == None:
			return False
		elif type(requirement) == list:
			for req in requirement:
				prelimOutcome = self.checkJobUp(req)
				if prelimOutcome == False:
					return False
			return True
		elif type(requirement) == int:
			if self.getLevel() >= requirement:
				return True
			else:
				return False
		elif type(requirement) == str:
			if requirement in self.getCSQ():
				return True
			else:
				return False
		else:
			print("type error in rank up requirements")
			return False
	def JobUp(self, user, s):
		sendMessage(s, "Congratulations " + user.getName() + "! you have just advanced in your career!")
		time.sleep(1)
		sendMessage(s, "You are now a " + self.getParsedNextJob() + "! (^w^)b")
		newJob = eval(self.getNextJob() + "(Icur = " + str(self.getIncome()) + ", Ecur = " + str(self.getExpenses()) + ")")
		user.occupation = newJob
		
	def update(self, s, user, gainedexp):
		self.addExp(gainedexp)
		self.checkLevelUp(s, user)
		user.getWallet().newJob(self.getIncome(), self.getExpenses())
		if self.checkJobUp(self.rankUpReq):
			self.JobUp(user, s)
			return None

#Unemployed
class Unemployed(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 6, ELOW = 4, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Unemployed"
		self.Squests = []
		self.Cquests = []
		self.Events = []






#Scavenger->Lumberjack->Fisherman->Hunter
class Scavenger(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Scavenger"
		self.rankUpReq = [8]
		self.Squests = []
		self.Cquests = ["FarmerC1", "FarmerC2", "FarmerC3"]
		self.Events = ["FarmerE1", "FarmerE2", "FarmerE3"]
		self.NextJob = "Lumberjack"
		
class Lumberjack(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Lumberjack"
		self.rankUpReq = [8, "LumberjackFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Fisherman"

class Fisherman(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Fisherman"
		self.rankUpReq = [8, "FishermanFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Hunter"

class Hunter(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Hunter"
		self.Squests = []
		self.Cquests = []
		self.Events = []

		
#Farmer->Soldier->Captain->General
class Farmer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Farmer"
		self.rankUpReq = [8, "FarmerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Soldier"
		
class Soldier(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Soldier"
		self.rankUpReq = [11, "SoldierFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Captain"

class Captain(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Captain"
		self.rankUpReq = [11, "CaptainFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "General"

class General(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "General"
		self.Squests = []
		self.Cquests = []
		self.Events = []


#Writer->Librarian->Accountant->Advisor
class Writer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Writer"
		self.rankUpReq = [11, "WriterFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Librarian"
		
class Librarian(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Librarian"
		self.rankUpReq = [14, "LibrarianFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Accountant"

class Accountant(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Accountant"
		self.rankUpReq = [14, "AccountantFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Advisor"

class Advisor(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Advisor"
		self.Squests = []
		self.Cquests = []
		self.Events = []


#Student->Scholar->Disciple->Teacher
class Student(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Student"
		self.rankUpReq = [11, "StudentFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Scholar"
		
class Scholar(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Scholar"
		self.rankUpReq = [14, "ScholarFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Disciple"

class Disciple(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Disciple"
		self.rankUpReq = [14, "DiscipleFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Teacher"

class Teacher(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Teacher"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Bartender->Server->Culinary Attendant->Chef
class Bartender(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Bartender"
		self.rankUpReq = [11, "BartenderFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Server"
		
class Server(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Server"
		self.rankUpReq = [14, "ServerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Culinary_Attendant"

class Culinary_Attendant(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Culinary_Attendant"
		self.rankUpReq = [14, "Culinary_AttendantFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Chef"

class Chef(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 5, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Chef"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Street_Performer->Actor->Dancer-> Idol
class Street_Performer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Street_Performer"
		self.rankUpReq = [17, "Street_PerformerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Actor"
		
class Actor(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Actor"
		self.rankUpReq = [14, "ActorFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Dancer"
		
class Dancer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Dancer"
		self.rankUpReq = [17, "DancerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Idol"

class Idol(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Idol"
		self.Squests = []
		self.Cquests = []
		self.Events = []

		
#Apprentice->Miko->Priest->Oracle
class Apprentice(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Apprentice"
		self.rankUpReq = [11, "ApprenticeFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Miko"
		
class Miko(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Miko"
		self.rankUpReq = [17, "MikoFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Priest"

class Priest(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Priest"
		self.rankUpReq = [14, "PriestFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Oracle"

class Oracle(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 15, EUP = 26):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Oracle"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Thief->Gangster->Assassin ->Executioner
class Thief(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Thief"
		self.rankUpReq = [11, "ThiefFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Gangster"
		
class Gangster(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Gangster"
		self.rankUpReq = [14, "GangsterFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Assassin"

class Assassin(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 20, IUP = 31, ELOW = 11, EUP = 21):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Assassin"
		self.rankUpReq = [11, "AssassinFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Executioner"

class Executioner(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Executioner"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Outsider->Horseman->Beast_Tamer-> Summoner
class Outsider(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Outsider"
		self.rankUpReq = [14, "OutsiderFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Horseman"
		
class Horseman(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Horseman"
		self.rankUpReq = [17, "HorsemanFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Beast_Tamer"

class Beast_Tamer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Beast_Tamer"
		self.rankUpReq = [17, "Beast_TamerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Summoner"

class Summoner(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 20, IUP = 31, ELOW = 11, EUP = 21):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Summoner"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Lesser_Demon->Greater_Demon-> Elite_Demon->Demon_Lord
class Lesser_Demon(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Lesser_Demon"
		self.rankUpReq = [17, "Lesser_DemonFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Greater_Demon"
		
class Greater_Demon(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 20, IUP = 31, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Greater_Demon"
		self.rankUpReq = [14, "Greater_DemonFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Elite_Demon"

class Elite_Demon(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Elite_Demon"
		self.rankUpReq = [14, "Elite_DemonFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Demon_Lord"

class Demon_Lord(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Demon_Lord"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Adventurer->Mercenary->Freelancer->Hero
class Adventurer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Adventurer"
		self.rankUpReq = [14, "AdventurerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Mercenary"
		
class Mercenary(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Mercenary"
		self.rankUpReq = [14, "MercenaryFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Freelancer"

class Freelancer(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Freelancer"
		self.rankUpReq = [14, "FreelancerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Hero"

class Hero(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 20, IUP = 31, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Hero"
		self.Squests = []
		self.Cquests = []
		self.Events = []

		
#Mechanic->Mason->Blacksmith->Craftsman
class Mechanic(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Mechanic"
		self.rankUpReq = [14, "MechanicFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Mason"
		
class Mason(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Mason"
		self.rankUpReq = [14, "MasonFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Blacksmith"

class Blacksmith(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 1, EUP = 6):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Blacksmith"
		self.rankUpReq = [14, "BlacksmithFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Craftsman"

class Craftsman(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Craftsman"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Linguist->Translator->Judge->Supreme_Justice
class Linguist(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Linguist"
		self.rankUpReq = [14, "LinguistFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Translator"
		
class Translator(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 7, IUP = 16, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Translator"
		self.rankUpReq = [17, "TranslatorFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Judge"

class Judge(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 20, IUP = 31, ELOW = 7, EUP = 16):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Judge"
		self.rankUpReq = [14, "JudgeFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Supreme_Justice"

class Supreme_Justice(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Supreme_Justice"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		
#Peddler->Trader->Innkeeper->Banker
class Peddler(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 5, IUP = 11, ELOW = 11, EUP = 21):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Peddler"
		self.rankUpReq = [17, "PeddlerFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Trader"
		
class Trader(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Trader"
		self.rankUpReq = [14, "TraderFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Innkeeper"

class Innkeeper(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 10, IUP = 21, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Innkeeper"
		self.rankUpReq = [17, "InnkeeperFinal"]
		self.Squests = []
		self.Cquests = []
		self.Events = []
		self.NextJob = "Banker"

class Banker(Occupation):
	def __init__(self, exp = 0, level = 0, CSQ = [], Icur = 0, Ecur = 0, ILOW = 15, IUP = 26, ELOW = 3, EUP = 11):
		Occupation.__init__(self, exp, level, CSQ, Icur, Ecur, ILOW, IUP, ELOW, EUP)
		self.name = "Banker"
		self.Squests = []
		self.Cquests = []
		self.Events = []	

		

#







































