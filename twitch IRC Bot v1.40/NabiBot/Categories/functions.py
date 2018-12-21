import time
import random
import sys
import math as pMath
sys.path.append('..')
import Jobs
import Standings as stnd
from Socket import *
from Standings import Standings as stndLst
sys.path.remove('..')



class debug(object):
	def exit(self, s, options, user, ul, comList):
		sendMessage(s, "It was nice chatting with you (^w^). Take care Shuruni (>.<) ~Nabi")
		sys.exit()
			
			
class dummy(object):
	def dummy(self, message, s, options, user, ul, comList):
		sendMessage(s, message)
		
	def add(self, s, options, user, ul, comList):
		result = comList.addCom(options[0], " ".join(options[1:]))
		if result == True:
			sendMessage(s, options[0] + " command successfully added (^o^)/")
		else:
			sendMessage(s, "Sorry " + user.getName() + ", but the " + options[0] + " command already exists ^-^;")
			
	def remove(self, s, options, user, ul, comList):
		result = comList.remCom(options[0])
		if result == "ND":
			sendMessage(s, "Sorry " + user.getName() + ", but you aren't allowed to remove non-dummy commands ^-^;")
		elif result == True:
			sendMessage(s, options[0] + " command successfully removed Owo")
		else:
			sendMessage(s, "that command doesn't exist " + user.getName() + " >w<")


class math(object):
	def add(self, s, options, user, ul, comList):
		result = float(options[1]) + float(options[2])
		if str(result)[-2:] == ".0":
			result = int(result)
		sendMessage(s, options[1] + " + " + options[2] + " = " + str(result) + " ^w^")
		
	def subtract(self, s, options, user, ul, comList):
		result = float(options[1]) - float(options[2])
		if str(result)[-2:] == ".0":
			result = int(result)
		sendMessage(s, options[1] + " - " + options[2] + " = " + str(result) + " owO")
		
	def multiply(self, s, options, user, ul, comList):
		result = float(options[1]) * float(options[2])
		if str(result)[-2:] == ".0":
			result = int(result)
		sendMessage(s, options[1] + " * " + options[2] + " = " + str(result) + " .-.")
	
	def divide(self, s, options, user, ul, comList):
		try:
			result = float(options[1]) / float(options[2])
			if str(result)[-2:] == ".0":
				result = int(result)
			sendMessage(s, options[1] + " / " + options[2] + " = " + str(result) + " ~w~")
		except ZeroDivisionError:
			sendMessage(s, options[1] + " / " + options[2] + " = Undefined -O-")
	
	def random(self, s, options, user, ul, comList):
		if len(options) == 1:
			sendMessage(s, "Nabi thought of " + str(random.randrange(0, 101)) + " (^w^)b")
		else:
			if int(options[1]) < int(options[2]):
				num1 = int(options[1])
				num2 = int(options[2])
			else:
				num1 = int(options[2])
				num2 = int(options[1])
			sendMessage(s, "Nabi thought of " + str(random.randrange(num1, num2+1)) + " (^w^)b")
	
	def modulo(self, s, options, user, ul, comList):
		try:
			result = int(options[1]) % int(options[2])
			sendMessage(s, options[1] + " % " + options[2] + " = " + str(result) + " (>^<)")
		except ZeroDivisionError:
			sendMessage(s, options[1] + " % " + options[2] + " = Undefined -O-")
	def root(self, s, options, user, ul, comList):
		try:
			result = pMath.sqrt(float(options[1]))
			sendMessage(s, "the square root of " + options[1] + " is " + str(result) + " (-.-)")
		except:
			sendMessage(s, "the square root of " + options[1] + " is not a thing (-.-)")


class command(object):
	def web(self, s, options, user, ul, comList):
		sendMessage(s, "https://sites.google.com/site/shurunihikaru/nabi-w/commands")
	
	def list(self, s, options, user, ul, comList):
		commands = set()
		for command in comList.getList():
			commands.add(command[0])
		cLst = []
		while len(commands) > 0:
			cLst.append(commands.pop())
		cLst.sort()
		message = "Nabi can do any of the following commands: " + ", ".join(cLst)
		sendMessage(s, message)
	def reload(self, s, options, user, ul, comList):
		sendMessage(s, "Okay ^w^, Nabi will recheck her commands")
		comList.updateList()
	def save(self, s, options, user, ul, comList):
		sendMessage(s, "Okay ^w^, Nabi will write down her commands")
		comList.sendToFile()
	

class fun(object):
	def roll(self, s, options, user, ul, comList):
		if options == []:
			Maxamount = 50
			if user.getBalance() < Maxamount:
				sendMessage(s, "Sorry, " + user.getName() + ", you don't have enough money to cover the cost of losing this dice game ^_^;")
				return None
			roll1 = random.randrange(1,7)
			roll2 = random.randrange(1,7)
			WinTotal = abs(roll1 - roll2)*10
			if not WinTotal:
				winner = None
			else:
				winNum = random.random()
				if winNum >= 0.5:
					winner = "Nabi"
				else:
					winner = user.getName()
				if roll1 > roll2:
					win = roll1
					lose = roll2
				else:
					win = roll2
					lose = roll1
			if winner == None:
				sendMessage(s, user.getName() + " rolled a " + str(roll1) + " ^w^")
				time.sleep(1)
				sendMessage(s, "Nabi rolled a " + str(roll2) + "! ^w^" )
				time.sleep(1)
				sendMessage(s, "It's a tie! well, at least you didn't lose to Nabi ;3")
			elif winner == "Nabi":
				sendMessage(s, user.getName() + " rolled a " + str(lose) + " ^w^")
				time.sleep(1)
				sendMessage(s, "Nabi rolled a " + str(win) + "! ^w^" )
				time.sleep(1)
				sendMessage(s, "(^o^)/ yay! Nabi won! Sorry " + user.getName() + " you lost " + str(WinTotal) + " coins to Nabi :3")
				user.pay(WinTotal)
			else:
				sendMessage(s, user.getName() + " rolled a " + str(win) + " ^w^")
				time.sleep(1)
				sendMessage(s, "Nabi rolled a " + str(lose) + "! ^w^" )
				time.sleep(1)
				sendMessage(s, "Nabi lost (/.\\ ). oh well... Congratualtions " + user.getName() + "! you win " + str(WinTotal) + " coins! -3-")
				user.recieve(WinTotal)
			
			
		elif int(options[0]) <= 1:
			sendMessage(s, user.getName() + ", stop trying to roll dice that don't exist (>O<)")
		
		else:
			Maxamount = 10*(int(options[0])-1)
			if user.getBalance() < Maxamount:
				sendMessage(s, "Sorry, " + user.getName() + ", you don't have enough money to cover the cost of losing this dice game ^_^;")
				return None
			roll1 = random.randrange(1, int(options[0])+1)
			roll2 = random.randrange(1, int(options[0])+1)
			WinTotal = abs(roll1 - roll2)*10
			if not WinTotal:
				winner = None
			else:
				winNum = random.random()
				if winNum >= 0.5:
					winner = "Nabi"
				else:
					winner = user.getName()
				if roll1 > roll2:
					win = roll1
					lose = roll2
				else:
					win = roll2
					lose = roll1
			if winner == None:
				sendMessage(s, user.getName() + " rolled a " + str(roll1) + " ^w^")
				time.sleep(1)
				sendMessage(s, "Nabi rolled a " + str(roll2) + "! ^w^" )
				time.sleep(1)
				sendMessage(s, "It's a tie! well, at least you didn't lose to Nabi ;3")
			elif winner == "Nabi":
				sendMessage(s, user.getName() + " rolled a " + str(lose) + " ^w^")
				time.sleep(1)
				sendMessage(s, "Nabi rolled a " + str(win) + "! ^w^" )
				time.sleep(1)
				sendMessage(s, "(^o^)/ yay! Nabi won! Sorry " + user.getName() + " you lost " + str(WinTotal) + " coins to Nabi :3")
				user.pay(WinTotal)
			else:
				sendMessage(s, user.getName() + " rolled a " + str(win) + " ^w^")
				time.sleep(1)
				sendMessage(s, "Nabi rolled a " + str(lose) + "! ^w^" )
				time.sleep(1)
				sendMessage(s, "Nabi lost (/.\\ ). oh well... Congratualtions " + user.getName() + "! you win " + str(WinTotal) + " coins! -3-")
				user.recieve(WinTotal)

	def Cfight(self, s, options, user, ul, comList):
		# sample output: "3" pause 1 sec "2" pause 1 sec "1" pause 2 sec "Fight!" pause for 5 seconds [list of interesting win stements. ex. "UserA wipes the floor with UserB!" or "even though it looked like UserB was winning, User A pulled a surprise attack in the end and won the fight!"] pause 3 seconds "Congratulations UserA/B, you won [amount] coins!"  "!coins take UserA/B [amount]"  "!coins add UserA/B [amount]"
		time.sleep(2)
		sendMessage(s, "Fight")
		time.sleep(3)
		Winner = random.random()
		winState = random.randrange(1, 7)
		challenged = ul.isInList(options[2])
		amount = challenged.challenged[1]
		winner = None
		loser = None
		if Winner < 0.5:
			winner = ul.isInList(options[1])
			loser = ul.isInList(options[2])
		else:
			winner = ul.isInList(options[2])
			loser = ul.isInList(options[1])
		if winState == 1:
			sendMessage(s, winner.getName() + " wipes the floor with " + loser.getName() + "!")
		elif winState == 2:
			sendMessage(s, "As " + loser.getName() + " was going to deliver the final blow, " + winner.getName() + " rolls to the side dodging the blow. " + loser.getName() + ", wide open from missing the attack, is knocked out by " + winner.getName() + " from a sucker punch in the face! ")
		elif winState == 3:
			sendMessage(s, loser.getName() + " throws out a cripling punch, but ends up falling into a trap hole dug by " + winner.getName() + "!")
		elif winState == 4:
			sendMessage(s, winner.getName() + " destroys " + loser.getName() + " without any hesitation!")
		elif winState == 5:
			sendMessage(s, winner.getName() + " fought off " + loser.getName() + " with ease, winning the fight like it was nothing!")
		else:
			sendMessage(s, "even though it looked like " + loser.getName() +" was winning, " + winner.getName() + " pulled a surprise attack in the end and won the fight!")
		challenged.challenged = []
		time.sleep(2)
		sendMessage(s, "Congratulations " + winner.getName() + ", you won " + str(amount) + " coins!")
		winner.recieve(int(amount))
		loser.pay(int(amount))
		
	def Caccept(self, s, options, user, ul, comList):
		if user.challenged == []:
			sendMessage(s, "silly " + user.getName() + ", No-one has challenged you to anything! :P")
		else:
			sendMessage(s, "Alright, Here we go!")
			UserA = user.challenged[0]
			UserB = user.getName()
			self.Cfight(s, ["fight", UserA, UserB], user, ul, comList)
		
	def Cdecline(self, s, options, user, ul, comList):	
		challenged = ul.isInList(options[0])
		if user.challenged == []:
			sendMessage(s, "silly " + user.getName() + ", No-one has challenged you to anything! :P")
		else:
			sendMessage(s, "oh well " + user.challenged[0] + ", looks like " + user.getName() + " didn't feel like losing to you today! :P")
			user.challenged == []
		
	def Challenge(self, s, options, user, ul, comList):
		if ul.isInList(options[0]) != False:
			if int(options[1]) > 0:
				challenged = ul.isInList(options[0])
				if challenged == False:
					sendMessage(s, "I don't think that person exists " + user.getName() + " (owO)?")
					return None
				elif user.getBalance() > int(options[1]):
					if challenged.getBalance() > int(options[1]):
						challenged.challengerAproaches(user.getName(), options[1])
						sendMessage(s, user.getName() + " challenges " + options[0] + " to a duel with " + str(options[1]) + " coins at stake! " + options[0] + ", Please type \"!challenge accept\" to accept the challenge, or \"!challenge decline\" to refuse it.")
					else:
						sendMessage(s, "Sorry " + user.getName() + ", " + options[0] + " doesn't have enough money to accept your challenge. ^_^;")
				else:
					sendMessage(s, user.getName() + ", you don't have that much money! -0-")
			else:
				sendMessage(s, "how do you expect to bet with negative coins! >w<")
		elif options[0].lower() == "nabibot_":
			sendMessage(s, "Wah! I don't want to fight (/.\\) Shuruni-Oniichan~ " + user.getName() + " wants to hurt me ;-; get them away from me please T-T")
		else:
			sendMessage(s, "Nabi doesn't know the person you are trying to challenge ^-^;")
	def randomLoli(self, s, options, user, ul, comList):
		LoliList = []
		with open("RandomLoli.nabi", "rb") as f:
			for line in f:
				LoliList.append(line)
		NumLolis = len(LoliList)
		RandChoice = random.randrange(0,NumLolis)
		RandLoli = LoliList[RandChoice]
		sendMessage(s, RandLoli)
	
class coin(object):
	def self(self, s, options, user, ul, comList):
		if options == []:
			sendMessage(s, user.getName() + " has " + str(user.getBalance()) + " coins ^w^")
		
	def pay(self, s, options, user, ul, comList):
		if user.canPay(int(options[2])):
			recipient = ul.isInList(options[1])
			if recipient != False:
				user.pay(int(options[2]))
				recipient.recieve(int(options[2]))
				sendMessage(s, "Nabi has successfully transfered " + options[2] + " coins from " + user.getName() + "'s wallet to " + options[1].lower() + "'s wallet. (^o^)/")
			elif options[1].lower() == "nabibot_":
				user.pay(int(options[2]))
				sendMessage(s, "ooh :o thank's for the coins " + user.getName() + " ^w^")
			else:
				sendMessage(s, "Nabi doesn't know the person you want me to give your money to... I could take it off your hands if you'd like $w$, JK ^W^")
		else:
			sendMessage(s, user.getName() + ", you don't have that much money! -0-")
	
	def add(self, s, options, user, ul, comList):
		recipient = ul.isInList(options[1])
		if recipient != False:
			recipient.recieve(int(options[2]))
			sendMessage(s, "Nabi just sent " + options[2] + " coins to " + options[1].lower() + "'s wallet ^w^")
		else:
			sendMessage(s, "Who are you talking about Shuruni-Oniichan? I don't know who that is >.<")
		
	def remove(self, s, options, user, ul, comList):
		payer = ul.isInList(options[1])
		if payer != False:
			payer.pay(int(options[2]))
			sendMessage(s, "Nabi just took " + options[2] + " coins from " + options[1].lower() + "'s wallet ($o$)/")
		else:
			sendMessage(s, "Who are you talking about Shuruni-Oniichan? I don't know who that is >.<")
		
	def set(self, s, options, user, ul, comList):
		person = ul.isInList(options[1])
		if person != False:
			person.wallet.balance = int(options[2])
			sendMessage(s, "Nabi just took all of " + options[1].lower() + "'s coins and gave them " + options[2] + " coins in place ^w^")
		else:
			sendMessage(s, "Who are you talking about Shuruni-Oniichan? I don't know who that is >.<")
	
	def incomeS(self, s, options, user, ul, comList):
		sendMessage(s, user.getName() + "'s income is currently " + str(user.getIncome()) + " coins per minute ^w^")
	
	def incomeO(self, s, options, user, ul, comList):
		oUser = ul.isInList(options[1])
		if oUser != False:
			sendMessage(s, oUser.getName() + "'s income is currently " + str(oUser.getIncome()) + " coins per minute ^w^")
		elif options[1].lower() == "nabibot_":
				sendMessage(s, "Nabi makes 9001 coins per second \\(^W^)/")
		else:
			sendMessage(s, "Nabi doesn't know the person you want to peek into the wallet of -o-")
	
	def expensesS(self, s, options, user, ul, comList):
		sendMessage(s, user.getName() + "'s expenses are currently " + str(user.getExpenses()) + " coins per minute -w-")
	
	def expensesO(self, s, options, user, ul, comList):
		oUser = ul.isInList(options[1])
		if oUser != False:
			sendMessage(s, oUser.getName() + "'s expenses are currently " + str(oUser.getExpenses()) + " coins per minute -w-")
		elif options[1].lower() == "nabibot_":
				sendMessage(s, "Nabi has no expenses, Shuruni-Oniichan takes care of them for me (^-^)")
		else:
			sendMessage(s, "Nabi doesn't know the person you want to peek into the wallet of -o-")
		
	def other(self, s, options, user, ul, comList):
		oUser = ul.isInList(options[0])
		if oUser != False:
			sendMessage(s, oUser.getName() + " has " + str(oUser.getBalance()) + " coins ^w^")
		elif options[0].lower() == "nabibot_":
				sendMessage(s, "Nabi has more coins than you will ever see in your lifetime ^-^, just give up already \\(-o-)")
		else:
			sendMessage(s, "Nabi doesn't know the person you want to peek into the wallet of -o-")
		
		
class level(object):
	def self(self, s, options, user, ul, comList):
		expData = user.expToNextLevel()
		level = user.getLevel()
		message = user.getName() + " is level " + str(level) + " [" + str(expData[1][0]) + "/" + str(expData[1][1]) + "]. you need " + str(expData[0][0]) + " more exp before you reach level " + str(level+1) + ". "
		if float(expData[0][0])/float(expData[0][1]) <= 0.2:
			sendMessage(s, message + "you're almost there! \\(>w<)/")
		elif float(expData[0][0])/float(expData[0][1]) <= 0.5:
			sendMessage(s, message + "You're over halfway there! (^w^)/")
		elif float(expData[0][0])/float(expData[0][1]) <= 0.7:
			sendMessage(s, message + "you're getting closer. (^o^)/")
		else:
			sendMessage(s, message + "you've got a ways to go... (-w-)")
		
	def leaderboards(self, s, options, user, ul, comList):
		message = "Top 5: "
		place = 1
		# print ul.top5()
		for user in ul.top5():
			message += "#" + str(place) + "  " + user.getName() + ": Lv. " + str(user.getLevel()) + ""
			if place == 5:
				pass
			else:
				message += "   "
			place += 1
		sendMessage(s, message)
		
	def other(self, s, options, user, ul, comList):
		if ul.isInList(options[0]) != False:
			self.self(s, [], ul.isInList(options[0]), ul, comList)
		else:
			sendMessage(s, "Nabi doesn't know the person you are asking her about ^-^;")


class Occupations(object):
	def self(self, s, options, user, ul, comList):
		sendMessage(s, user.getName() + "'s occupation is " + user.getOccupation().getParsedName() + " .-.")
	
	def other(self, s, options, user, ul, comList):
		if ul.isInList(options[0]) != False:
			self.self(s, [], ul.isInList(options[0]), ul, comList)
		else:
			sendMessage(s, "Nabi doesn't know the person you are asking her about ^-^;")
	
	def sLevel(self, s, options, user, ul, comList):
		expData = user.getOccupation().expToNextLevel()
		level = user.getOccupation().getLevel()
		message = user.getName() + " is " + user.getOccupation().getParsedName() + " level " + str(level) + " [" + str(expData[1][0]) + "/" + str(expData[1][1]) + "]. you need " + str(expData[0][0]) + " more exp before you reach level " + str(level+1) + ". "
		if float(expData[0][0])/float(expData[0][1]) <= 0.2:
			sendMessage(s, message + "you're almost there! \\(>w<)/")
		elif float(expData[0][0])/float(expData[0][1]) <= 0.5:
			sendMessage(s, message + "You're over halfway there! (^w^)/")
		elif float(expData[0][0])/float(expData[0][1]) <= 0.7:
			sendMessage(s, message + "you're getting closer. (^o^)/")
		else:
			sendMessage(s, message + "you've got a ways to go... (-w-)")
	
	def oLevel(self, s, options, user, ul, comList):
		if ul.isInList(options[1]) != False:
			self.sLevel(s, ["level"], ul.isInList(options[1]), ul, comList)
		else:
			sendMessage(s, "Nabi doesn't know the person you are asking her about ^-^;")
	
	def list(self, s, options, user, ul, comList):
		if len(options) == 1:
			sendMessage(s, "The 1st Tier occupations are: " + ", ".join(Jobs.FirstTier[:]))
		elif options[1].lower() == "special":
			sendMessage(s, "The Special occupations are: " + ", ".join(Jobs.SpecialTier[:]))
		# elif options[2] == "1":
			# sendMessage(s, "The 1st Tier occupations are: " + ", ".join(Jobs.FirstTier[:]))
		# elif options[2] == "2":
			# sendMessage(s, "The 2nd Tier occupations are: " + ", ".join(Jobs.SecondTier[:]))
		# elif options[2] == "3":
			# sendMessage(s, "The 3rd Tier occupations are: " + ", ".join(Jobs.ThirdTier[:]))
		# elif options[2] == "4":
			# sendMessage(s, "The 4th Tier occupations are: " + ", ".join(Jobs.FourthTier[:]))
		else:
			print("no tier found but command ran")
	
	def sChange(self, s, options, user, ul, comList):
		if options[1] in Jobs.AvailableOccList[:]:
			user.occupation = eval("Jobs." + options[1] + "()")
			sendMessage(s, user.getName() + "'s occupation is now " + user.getOccupation().getParsedName() + " (^o^)/")
		else:
			sendMessage(s, "Nabi didn't know that was an occupation, oh wait... it isn't ;P")
	
	def oChange(self, s, options, user, ul, comList):
		if ul.isInList(options[1]) != False:
			self.sChange(s, [options[0], options[2]], ul.isInList(options[1]), ul, comList)
		else:
			sendMessage(s, "Nabi doesn't know the person you are asking her about ^-^;")
	
	def AcceptQuest(self, s, options, user, ul, comList):
		if user.cQuest == None:
			story = user.getOccupation().nextSQuest(user, s)
			if story == False:
				common = user.getOccupation().randomCQuest(user, s)
				if common == False:
					sendMessage(s, "Nabi doesn't know why, but there aren't any quests that you can do right now ^_^;")
		else:
			sendMessage(s, "you currently are already on a quest. if you would like to drop it, you can type \"!quest drop\", if you drop it, you will still have to wait for the cooldown to get another one")
	
	def QuestOption(self, s, options, user, ul, comList):
		choice = ""
		for i in range(1, len(options)):
			choice += options[i] + " "
		choice2 = choice.strip()
		user.cQuest.execute(user, s, choice2)
		try:
			self.listChoices(self, s, options, user, ul, comList)
		except TypeError:
			pass
	
	def listChoices(self, s, options, user, ul, comList):
		if user.cQuest != None:
			choices = user.cQuest.possibleChoices()
			sendMessage(s, "/w " + user.getName() + " Possible Choices: " + ", ".join(choices))
		else:
			sendMessage(s, "you don't have a quest >w<")
	
	def DropQuest(self, s, options, user, ul, comList):
		if user.cQuest == None:
			sendMessage(s, "you don't have a quest to drop >.<")
		else:
			user.cQuest = None
			sendMessage(s, "quest has been abandoned T-T")
		
	def Event(self, s, options, user, ul, comList):
		user.getOccupation().randomEvent(user, s)


class Nabi(object):
	def __init__(self):
		self.messages = {
			1:"I don't want to be mean but... >_< you're the worst! you made me say it... you're so mean to me! BibleThump"
			,2:"You're so mean to me. Please leave so Nabi can be happy. -o-"
			,3:"I'm not one to be negative, but you're not a nice person. -3-"
			,4:"Eto... I hope you aren't mad at me. It's just my opinion of you ^-^;"
			,5:"You're not a bad person, but you're not a good person either. I guess that makes you an okay person. (^o^)"
			,6:"You're average. (^w^) Please continue to be nice to me."
			,7:"You are a nice person to have around ^-^. After all, you're helping Onii-chan become the best streamer. <3"
			,8:"I think fondly of you, but if you were a bit nicer, I'd rate you a 9/10. ;3"
			,9:"Maybe you could be the one for me. ;3 Just kidding. ;P Shuruni is the one for me. <3"
			,10:"You're one of my favorite people ^w^, but you'll never be as good as Onii-chan. ;)"
			}
		self.AE = []
		with open('Expressions/NabiV2/AvailableExpressions.nabi', 'rb') as f:
			for line in f:
				self.AE.append(line.strip().lower())
		print self.AE
		
	def awake(self, s, options, user, ul, comList):
		if options == []:
			cTime = time.clock()
			sendMessage(s, "NabiBot has been awake for exactly " + str(cTime) + " seconds ^w^")
	def rating(self, s, options, user, ul, comList):
		if options == []:
			if user.getName().lower() == "shuruni":
				sendMessage(s, "Nabi rates Shuruni-Oniichan at 11/10. Onii-chan will always be my favorite (^3^) *chu")
				return None
			if user.getName().lower() == "nolicanoli10":
				sendMessage(s, "Shuruni Onii-chan~ >.< get this lolicon away from me please (/.\\ )")
				return None
			rating = user.getRating()
			sendMessage(s, "Nabi rates " + user.getName() + " at " + str(rating) + "/10. " + self.messages[rating])
		elif options[0].lower() == "nabibot_" or options[0].lower() == "nabi" or options[0].lower() == "nabibot":
			rating = 7
			sendMessage(s, "Nabi rates Herself at " + str(rating) + "/10. " + self.messages[rating])
		elif options[0].lower() == "shuruni" or options[0].lower() == "shuru" or options[0].lower() == "runi":
			sendMessage(s, "Nabi rates Shuruni-Oniichan at 11/10. Onii-chan will always be my favorite (^3^) *chu")
		elif options[0].lower() == "nolicanoli10":
			sendMessage(s, "Shuruni Onii-chan~ >.< get this lolicon away from me please (/.\\ )")
		elif ul.isInList(options[0]) != False:
			qUser = ul.isInList(options[0])
			rating = qUser.getRating()
			sendMessage(s, "Nabi rates " + qUser.getName() + " at " + str(rating) + "/10. " + self.messages[rating])
		else:
			sendMessage(s, "Nabi doesn't know the person you are asking her about ^-^;")
	def ExpressionList(self, s, options, user, ul, comList):
		sendMessage(s, "Nabi can change her expression to any of these: " + str(self.AE))
	def ExpressionChange(self, s, options, user, ul, comList):
		if options[0].lower() in self.AE:
			with open('Expressions/NabiV2/CurrentExpression.nabi', 'wb') as f:
				f.write(options[0].lower())
			sendMessage(s, "alright I'll do that for you that in a bit ^w^")
		else:
			sendMessage(s, "uhmm... I don't know how to make that kind of face ^-^; try just !expressions for a list of the faces I know how to make ^w^")

				
class Osu(object):
	def NP(self, s, options, user, ul, comList):
		with open('Osu/osu!SC/Files/np_playing.txt', 'rb') as p:
			playing = p.readline().strip()
			if playing == "":
				with open('Osu/osu!SC/Files/np_listening.txt', "rb") as l:
					listening = l.readline().strip()
					if listening == "":
						sendMessage(s, "Nothing at the moment ^w^;")
					else:
						sendMessage(s, "Shuruni-Oniichan is listening to: " + listening + " ^w^")
			else:
				sendMessage(s, "Shuruni-Oniichan is playing: " + playing + " (^o^)/")
	def DL(self, s, options, user, ul, comList):
		with open('Osu/osu!SC/Files/np_playing_DL.txt', 'rb') as p:
			playing = p.readline().strip()
			if playing == "":
				sendMessage(s, "Shuruni isn't playing a map right now so you cant download it >.<")
			else:
				sendMessage(s, "Here you are " + user.getName() + " ^w^ : " + playing)

class Standings(object):
	def change(self, s, options, user, ul, comList):
		if options[2] in stndLst:
			oUser = ul.isInList(options[1])
			if oUser != False:
				oUser.standing = eval("stnd." + options[2] + "()")
				sendMessage(s, oUser.getName() + " is now a " + oUser.getStanding().currentStanding() + " \\($w$)/")
			else:
				sendMessage(s, "Nabi doesn't know the person who you want to change the standing of ^w^;")
		else:
			sendMessage(s, "That standing doesn't exist, I may be able to figure out how to add it in the future if you want >.<")
			
	def self(self, s, options, user, ul, comList):
		sendMessage(s, user.getName() + " is a " + user.getStanding().currentStanding() + " .-.")
	def other(self, s, options, user, ul, comList):
		oUser = ul.isInList(options[0])
		if oUser != False:
			sendMessage(s, oUser.getName() + " is a " + oUser.getStanding().currentStanding() + " .-.")
#










































