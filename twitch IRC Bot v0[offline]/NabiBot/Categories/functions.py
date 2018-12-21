
import time
import random
import sys
sys.path.append('..')
from Socket import *
sys.path.remove('..')



class debug(object):
	def exit(self, s, options, user, ul):
		sendMessage(s, "It was nice chatting with you (^w^). Take care Shuruni (>.<) ~Nabi")
		sys.exit()
class dummy(object):
	def dummy(self, message, s, options, user, ul):
		sendMessage(s, message)

		
class fun(object):
	def roll(self, s, options, user, ul):
		if options == []:
			sendMessage(s, user.getName() + " rolled a " + str(random.randrange(1,7)) + " ^w^")
		elif int(options[0]) <= 1:
			sendMessage(s, user.getName() + ", stop trying to roll dice that don't exist (>O<)")
		else:
			sendMessage(s, user.getName() + " rolled a " + str(random.randrange(1,int(options[0])+1)) + " ^w^")

	def challenge(self, s, options, user, ul):
		pass
			
class coin(object):
	def coins(self, s, options, user, ul):
		if options == []:
			pass
		
		
class level(object):
	def level(self, s, options, user, ul):
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
			print ul.top5()
			for user in ul.top5():
				message += "\n#" + str(place) + "  " + user.getName() + ": Lv. " + str(user.getLevel()) + ""
				place += 1
			sendMessage(s, message)
class Nabi():
	def awake(self, s, options, user, ul):
		if options == []:
			sendMessage(s, "NabiBot has been awake for exactly " + str(time.clock()) + " seconds ^w^")