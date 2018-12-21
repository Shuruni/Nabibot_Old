import csv
import time
import sys
import random
sys.path.append('..')
import Standings
import Coins
from Socket import *
sys.path.remove('..')

class User(object):
	def __init__(self, name, wallet=Coins.Wallet(), level=0, exp=0, active=True, standing=Standings.Newbie()):
		self.name = name
		self.wallet = wallet
		self.level = level  
		self.exp = exp  #how much experience the user has #level up exp scales by x^1.5 when x=5*level
		self.CILM = []  #comments in last minute, list of timestamps, when first and last timestamps differ by 60 sec, remove the earliest timestamp
		self.ReturnsMult = 1  #decreases by 0.1 per comment posted in the same minute for comments exceeding 5 # reverts to 1 every minute
		self.downtime = 9
		self.active = active  # has user posted something to chat in the past 10 minutes?
		self.rating = random.randrange(1, 11)
		self.standing = standing
		self.challenged = []
		self.cooldown = []
	
	def getName(self):
		return self.name
	
	def getBalance(self):
		return self.wallet.getBalance()
	
	def getIncome(self):
		return self.wallet.getIncome()
	
	def getExpenses(self):
		return self.wallet.getExpenses()
	
	def recieve(self, amount):
		self.wallet.recieve(amount)
	
	def pay(self, amount):
		self.wallet.pay(amount)
	
	def canPay(self, amount):
		return self.wallet.canPay(amount)
	
	def getLevel(self):
		return self.level
		
	def getExp(self):
		return self.exp
	
	def getRating(self):
		return self.rating
	
	def getStanding(self):
		return self.standing
	
	def getCooldown(self):
		return self.cooldown[:]
	
	def expToNextLevel(self):
		#returns a list so that list[0] == [needed, outOfTotal] & list[1] == [current, required]
		nextLevelExp = 0
		reqOutOfExp = 0
		for i in range(self.level+1):
			reqOutOfExp = (18*i^2)+80
			nextLevelExp += reqOutOfExp
		return [[nextLevelExp - self.exp, reqOutOfExp], [self.exp,nextLevelExp]]
	
	def newComment(self):
		#run when User makes a new comment. timestamp: <int> seconds since program start
		self.active = True
		timestamp = int(time.clock())
		self.CILM.append(timestamp)
		print(self.getName() + str(self.CILM))
	
	def checkCILM(self):
		timestamp = int(time.clock())
		copyCILM = self.CILM[:]
		# print "CILM: ", self.CILM
		for i in range(len(copyCILM)):
			if timestamp - copyCILM[i] > 60:
				del self.CILM[0]
		# print "CILM: ", self.CILM
		if len(self.CILM) > 5:  #changes when diminishing returns kicks in
			self.ReturnsMult = 0
		else:
			self.ReturnsMult = 1
		# print str(self.ReturnsMult)
	
	def challengerAproaches(self, challenger, amount):
		#remember to call this only if User.pay(amount) == True
		self.challenged = [challenger, amount]
	
	def noMoreChallenge(self):
		self.challenged = []
	
	def addCooldown(self, command, cooldown):
		if self.name.lower() == "shuruni":
			return True
		self.cooldown.append([command, cooldown])
	
	def canUseCommand(self, command):
		if self.name.lower() == "shuruni":
			return True
		for i in self.cooldown:
			if i[0] == command:
				return False
		return True
	
	def CDUpdate(self):
		copy = self.cooldown[:]
		for i in copy:
			i[1] -= 1
			if i[1] == 0:
				del self.cooldown[0]
			else:
				break
	
	def update(self, s):
		#run once per minute
		self.checkCILM()
		if len(self.CILM) > 0:
			self.downtime = 0
			self.active = True
			print(self.getName() + " has made " + str(len(self.CILM)) + " comments in the last minute.")
		else:
			self.downtime += 1
			#print(self.getName() + " has been inactive for " + str(self.downtime) + " minutes")
		if self.downtime == 10:
			self.active = False
			print(self.getName() + " is now afk and is not recieving exp or income (don't worry, you don't have to pay expenses either ^w^)")
		elif self.downtime > 10:
			pass
		else:
			addEXP = random.randrange(2,4)+ len(self.CILM)*self.ReturnsMult
			self.exp += int(addEXP)
			self.wallet.updateWallet()
			print(self.getName() + " gained " + str(addEXP) + " exp, was paid " + str(self.getIncome()) + "coins and spent " + str(self.getExpenses()) + "coins on expenses")
		if self.expToNextLevel()[0][0] <=0:
			self.level += 1
			if self.level:
				sendMessage(s, "Congratulations " + self.name + "! You've just Leveled up! you are now level " + str(self.level) + "! \\(^o^)/")
				time.sleep(1)


class UserList(object):
	def __init__(self, file):
		self.file = "Users/" + file
		self.userList = self.getListFromFile(self.file)
		
	def isInList(self, username):
		for user in self.userList[:]:
			if user[0].lower() == username.lower():
				return user[1]
		return False
		
	def addUser(self, userObj):
		#always run self.isInList() before this to ensure no duplicates
		self.userList.append([userObj.getName(), userObj])
	
	def coolCount(self):
		for user in self.userList:
			user[1].CDUpdate()
	
	def updateUsers(self, s):
		for user in self.userList:
			user[1].update(s)
	
	def top5(self):
		UD = {}
		for user in self.userList:
			UD[user[1].getExp()] =  user[1]
		# print UD
		UK = UD.keys()
		UK.sort()
		UK.reverse()
		# print(UK)
		Top5 = []
		for i in UK[0:5]:
			Top5.append(UD[i])
		return Top5
	
	def  sendListToFile(self):
		toFileList = []
		for user in self.userList:
			toFileList.append([user[1].getName(), [user[1].getBalance(), user[1].getIncome(), user[1].getExpenses()], user[1].getLevel(), user[1].getExp(), "Standings." + user[1].getStanding().currentStanding() + "()"])
		uS = 0
		with open(self.file, 'wb') as csvfile:
			writer = csv.writer(csvfile)
			for userData in toFileList:
				writer.writerow(userData)
				uS +=1
		print(str(uS) + " Users saved")
	
	def getListFromFile(self, file):
		print("Loading User list from " + file + "...")
		users = []
		usersLoaded = 0
		currentRow = 1
		with open(file, 'rb') as csvfile:
			reader = csv.reader(csvfile)
			for row in reader:
				if row[0] == '' or row[1] == '' or row[2] == '' or row[3] == '' or row[4] == '':
					print("failed to load user on row " + str(currentRow) + "! please check that the syntax in the csv file is correct.")
				else:
					name = row[0]
					walletRaw = eval(row[1])
					wallet = Coins.Wallet(walletRaw[0], walletRaw[1], walletRaw[2])
					level = int(row[2])
					exp = int(row[3])
					active = False
					standing = eval(row[4])
					users.append([name, User(name, wallet, level, exp, active, standing)])
					usersLoaded += 1
				currentRow += 1
		print(str(usersLoaded) + " Users succesfully loaded from file! ")
		return users[:]
		
		
def blockedUsers(file):
	print("Loading Blocked User list from " + file + "...")
	users = []
	usersLoaded = 0
	currentRow = 1
	with open(file, 'rb') as csvfile:
		reader = csv.reader(csvfile)
		for row in reader:
			users.append(row[0])
			usersLoaded += 1
			currentRow += 1
	print(str(usersLoaded) + " Blocked Users succesfully loaded from file! ")
	return users[:]
	
		
		
		
		
		
		
		
		