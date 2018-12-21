import string
import sys
import time
from Commands.CommandClass import *
from Users.User import *
from Socket import *
from Read import *
from Initialize import joinRoom

if __name__ == "__main__":
	# s = openSocket()
	# joinRoom(s)
	# readbuffer = ""
	"""both"""
	comList = CommandList("CommandList.csv")
	print comList.file
	cList = comList.commandsList[:]
	for c in cList:
		print c[0] + " " + c[1].getFunction() + " ", c[1].getSyntax()
	userList = UserList("UserList.csv")
	uList = userList.userList[:]
	for u in uList:
		print u[0] + ":  wallet: " + str(u[1].getBalance()) + " coins, Level: " + str(u[1].getLevel()) + ", EXP: " + str(u[1].getExp()) + ", Standings Rank: " + u[1].getStanding().currentStanding() + ". "
	time.clock()
	timeLogged = 0
	""""""

	# while True:
		# readbuffer = readbuffer + s.recv(1024)
		# temp = string.split(readbuffer, "\n")
		# readbuffer = temp.pop()
		
		# for line in temp:
			# if "PING" == line[0:4]:
				# print line
				# s.send(line.replace("PING", "PONG"))
				# print line.replace("PING", "PONG")
				# break
			# user = getUser(line)
			# message = getMessage(line)
			# options = message.split(" ")
			# commandIssued = options[:][0]
			# del options[0]
			# print user + " typed: " + message
			# if "How's life?" in message:
				# sendMessage(s, "I don't know, I'm a bot :/")
				
				
	"""offline console testing version"""

	s = None

	while True:
		temp = "Shuruni: " + raw_input("")
		user = temp.split(": ")[0]
		message = temp.split(": ")[1]
		options = message.split(" ")
		"""both"""
		UserObj = userList.isInList(user)
		if UserObj == False:
			userList.addUser(User(user.lower()))
			sendMessage(s, "Welcome to the stream " + user + "! a new user profile has been made for you in my database (>w<)/, please enjoy your stay! (^o^)/")
		else:
			UserObj.newComment()
		commandIssued = options[:][0]
		del options[0]
		print user + " typed: " + message
		if int(time.clock()) % 60 == 0:
			# print("it is 0")
			if int(time.clock()) == timeLogged:
				pass
			else:
				timeLogged = int(time.clock())
				userList.updateUsers(s)
		""""""
		if "How's life?" in message:
			print("I don't know, I'm a bot :/")
			
		for command in comList.commandsList[:]:
			Check = command[1].check(commandIssued, options)
			if Check == True:
				command[1].execute(s, options, UserObj, userList)
			else:
				continue
def sendMessage(s, message):
		print message