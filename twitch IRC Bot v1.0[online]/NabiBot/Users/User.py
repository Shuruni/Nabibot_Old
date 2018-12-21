import csv
import time
import sys
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
		self.downtime = 10
		self.active = active  # has user posted something to chat in the past 10 minutes?
		self.standing = standing
		self.challenged = []
	
	def getName(self):
		return self.name
	
	def getBalance(self):
		return self.wallet.getBalance()
	
	def getIncome(self):
		return self.wallet.getIncome()
	
	def getExpenses(self):
		return self.wallet.getExpenses()
	
	def pay(self, amount):
		self.wallet.pay(amount)
	
	def canPay(self, amount):
		return self.wallet.canPay(amount)
	
	def getLevel(self):
		return self.level
		
	def getExp(self):
		return self.exp
	
	def getStanding(self):
		return self.standing
	
	def expToNextLevel(self):
		#returns a list so that list[0] == [needed, outOfTotal] & list[1] == [current, required]
		nextLevelExp = 0
		reqOutOfExp = 0
		for i in range(self.level+1):
			reqOutOfExp = i*i+(10*(i+1))
			nextLevelExp += reqOutOfExp
		return [[nextLevelExp - self.exp, reqOutOfExp], [self.exp,nextLevelExp]]
	
	def newComment(self):
		#run when User makes a new comment. timestamp: <int> seconds since program start
		self.active = True
		timestamp = int(time.clock())
		self.CILM.append(timestamp)
		copyCILM = self.CILM[:]
		# print "CILM: ", self.CILM
		for i in range(len(copyCILM)):
			if timestamp - copyCILM[i] > 60:
				del self.CILM[0]
		# print "CILM: ", self.CILM
		if len(self.CILM) > 10:  #changes when diminishing returns kicks in
			self.ReturnsMult = 1 - (0.05*len(self.CILM))
		else:
			self.ReturnsMult = 1
		# print str(self.ReturnsMult)
	
	def challengerAproaches(self, challenger, amount):
		#remember to call this only if User.pay(amount) == True
		self.challenged = [challenger, amount]
	
	def noMoreChallenge(self):
		self.challenged = []
		
	def update(self, s):
		#run once per minute
		if len(self.CILM) > 0:
			self.downtime = 0
			self.active = True
		else:
			self.downtime += 1
		if self.downtime >= 10:
			self.active = False
		if self.active:
			self.exp += len(self.CILM)*self.ReturnsMult
		else:
			self.exp += 1
		if self.expToNextLevel()[0][0] <=0:
			self.level += 1
			sendMessage(s, "Congratulations " + self.name + "! You've just Leveled up! you are now level " + str(self.level) + "! \\(^o^)/")
		self.wallet.updateWallet()
		


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
		
		
		
		
		
		
		
		
		
		
		