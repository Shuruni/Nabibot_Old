
import time
import random
import sys
sys.path.append('..')
from Socket import *
sys.path.remove('..')



class debug(object):
	def exit(self, s, options, user, ul, comList):
		sendMessage(s, "It was nice chatting with you (^w^). Take care Shuruni (>.<) ~Nabi")
		sys.exit()
class dummy(object):
	def dummy(self, message, s, options, user, ul, comList):
		sendMessage(s, message)

class command(object):
	def list(self, s, options, user, ul, comList):
		if options == []:
			sendMessage(s, "coming soon... (will eventually link to Shuruni's webpage with a list of commands)")
		
class fun(object):
	def roll(self, s, options, user, ul, comList):
		if options == []:
			Maxamount = 50
			if user.getBalance() < Maxamount:
				sendMessage(s, "Sorry, " + user.getName() + ", you don't have enough money to cover the cost of losing this dice game ^_^;")
				return None
			rollNabi = random.randrange(1,7)
			rollUser = random.randrange(1,7)
			WinTotal = abs(rollUser - rollNabi)*10
			sendMessage(s, user.getName() + " rolled a " + str(rollUser) + " ^w^")
			time.sleep(1)
			sendMessage(s, "Nabi rolled a " + str(rollNabi) + "! ^w^" )
			time.sleep(1)
			if rollUser < rollNabi:
				sendMessage(s, "(^o^)/ yay! Nabi won! Sorry " + user.getName() + " you lost " + str(WinTotal) + " coins to Nabi :3")
				user.pay(WinTotal)
			elif rollUser == rollNabi:
				sendMessage(s, "It's a tie! well, at least you didn't lose to Nabi ;3")
			else:
				sendMessage(s, "Nabi lost (/.\\ ). oh well... Congratualtions " + user.getName() + "! you win " + str(WinTotal) + " coins! -3-")
				user.recieve(WinTotal)
		elif int(options[0]) <= 1:
			sendMessage(s, user.getName() + ", stop trying to roll dice that don't exist (>O<)")
		
		else:
			Maxamount = 10*(int(options[0])-1)
			if user.getBalance() < Maxamount:
				sendMessage(s, "Sorry, " + user.getName() + ", you don't have enough money to cover the cost of losing this dice game ^_^;")
				return None
			rollNabi = random.randrange(1, int(options[0])+1)
			rollUser = random.randrange(1, int(options[0])+1)
			WinTotal = abs(rollUser - rollNabi)*10
			sendMessage(s, user.getName() + " rolled a " + str(rollUser) + " ^w^")
			time.sleep(1)
			sendMessage(s, "Nabi rolled a " + str(rollNabi) + "! ^w^" )
			time.sleep(1)
			if rollUser < rollNabi:
				sendMessage(s, "(^o^)/ yay! Nabi won! Sorry " + user.getName() + " you lost " + str(WinTotal) + " coins to Nabi :3")
				user.pay(WinTotal)
			elif rollUser == rollNabi:
				sendMessage(s, "It's a tie! well, at least you didn't lose to Nabi ;3")
			else:
				sendMessage(s, "Nabi lost (/.\\ ). oh well... Congratualtions " + user.getName() + "! you win " + str(WinTotal) + " coins! -3-")
				user.recieve(WinTotal)

	def challenge(self, s, options, user, ul, comList):
		if options[0] == "fight":
			# sample output: "3" pause 1 sec "2" pause 1 sec "1" pause 2 sec "Fight!" pause for 5 seconds [list of interesting win stements. ex. "UserA wipes the floor with UserB!" or "even though it looked like UserB was winning, User A pulled a surprise attack in the end and won the fight!"] pause 3 seconds "Congratulations UserA/B, you won [amount] coins!"  "!coins take UserA/B [amount]"  "!coins add UserA/B [amount]"
			sendMessage(s, "3")
			time.sleep(1)
			sendMessage(s, "2")
			time.sleep(1)
			sendMessage(s, "1")
			time.sleep(1)
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
		
		elif options[0] == "accept":
			if user.challenged == []:
				sendMessage(s, "silly " + user.getName() + ", No-one has challenged you to anything! :P")
			else:
				sendMessage(s, "Alright, Here we go!")
				UserA = user.challenged[0]
				UserB = user.getName()
				self.challenge(s, ["fight", UserA, UserB], user, ul, comList)
		
		elif options[0] == "decline":	
			challenged = ul.isInList(options[0])
			if user.challenged == []:
				sendMessage(s, "silly " + user.getName() + ", No-one has challenged you to anything! :P")
			else:
				sendMessage(s, "oh well " + user.challenged[0] + ", looks like " + user.getName() + " didn't feel like losing to you today! :P")
				user.challenged == []
		
		elif ul.isInList(options[0]) != False and int(options[1]) > 0:
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
			#prints(commandUser + " challenges " + User + " to a duel with " + str(amount) + " coins at stake! " + User + ", Please type \"!challenge accept\" to accept the challenge, or \"!challenge decline\" to refuse it.") 
			#Note: if the User hs not been created yet (i.e. has not messaged in chat before), do nothing; also, remove the challenge after 10 minutes if no reponse has been made.
		
class coin(object):
	def coins(self, s, options, user, ul, comList):
		if options == []:
			sendMessage(s, user.getName() + " has " + str(user.getBalance()) + " coins ^w^")
		
		elif options[0] == "give" or options[0] == "pay":
			if user.canPay(int(options[2])):
				recipient = ul.isInList(options[1])
				if recipient != False:
					user.pay(int(options[2]))
					recipient.recieve(int(options[2]))
			else:
				sendMessage(s, user.getName() + ", you don't have that much money! -0-")
		
		elif options[0] == "add": #permissions Nabi and Shuruni
			recipient = ul.isInList(options[1])
			if recipient != False:
				recipient.recieve(int(options[2]))
		
		elif options[0] == "take" or options[0] == "remove": #permissions Nabi and Shuruni
			payer = ul.isInList(options[1])
			if recipient != False:
				payer.pay(int(options[2]))
		
		elif options[0] == "set": #permissions Nabi and Shuruni
			person = ul.isInList(options[1])
			if recipient != False:
				person.wallet.balance = int(options[2])
		
		elif options[0] == "income":
			sendMessage(s, user.getName() + "'s income is currently " + str(user.getIncome()) + " coins per minute ^w^")
		
		elif options[0] == "expenses":
			sendMessage(s, user.getName() + "'s expenses are currently " + str(user.getExpenses()) + " coins per minute -w-")
		
		elif ul.isInList(options[0]):
			oUser = ul.isInList(options[0])
			if oUser != False:
				sendMessage(s, oUser.getName() + " has " + str(oUser.getBalance()) + " coins ^w^")
		
class level(object):
	def level(self, s, options, user, ul, comList):
		if options == []:
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
		
		elif options[0] == "leaderboards":
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
		
		elif ul.isInList(options[0]) != False:
			self.level(s, [], ul.isInList(options[0]), ul)
class Nabi():
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
		
	def awake(self, s, options, user, ul, comList):
		if options == []:
			cTime = time.clock()
			sendMessage(s, "NabiBot has been awake for exactly " + str(cTime) + " seconds ^w^")
	def rating(self, s, options, user, ul, comList):
		if options == []:
			if user.getName().lower() == "shuruni":
				sendMessage(s, "Nabi rates Shruni-Oniichan at 11/10. Onii-chan will always be my favorite (^3^) *chu")
				return None
			rating = user.getRating()
			sendMessage(s, "Nabi rates " + user.getName() + " at " + str(rating) + "/10. " + self.messages[rating])
		elif options[0].lower() == "nabibot_" or options[0].lower() == "nabi" or options[0].lower() == "nabibot":
			rating = 7
			sendMessage(s, "Nabi rates Herself at " + str(rating) + "/10. " + self.messages[rating])
		elif options[0].lower() == "shuruni" or options[0].lower() == "shuru" or options[0].lower() == "runi":
			sendMessage(s, "Nabi rates Shruni-Oniichan at 11/10. Onii-chan will always be my favorite (^3^) *chu")
		elif ul.isInList(options[0]) != False:
			qUser = ul.isInList(options[0])
			rating = qUser.getRating()
			sendMessage(s, "Nabi rates " + qUser.getName() + " at " + str(rating) + "/10. " + self.messages[rating])
#










































