import string
import sys
import time
from Commands.CommandClass import *
from Users.User import *
from Socket import *
from Startup.Read import *
from Startup.Initialize import joinRoom
import logging
LOG_FILENAME = 'CrashLog/CrashLog.nabi'
logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG)

with open("GUI/Status.nabi", "w") as f:
	f.write("Running")
	f.truncate()

	
try:
	if __name__ == "__main__":
		s = openSocket()
		readbuffer = ""
		comList = CommandList("CommandList.csv")
		userList = UserList("UserList.csv")
		bList = blockedUsers("Users/BlockList.csv")
		time.clock()
		timeLogged = 0
		s.settimeout(0.9)
		joinRoom(s)
		userList.updateUsers(s)
		userList.sendListToFile()

		while True:
			with open("GUI/Close.nabi", "rb") as f:
				tempRead = f.read()
			if tempRead == "1":
				with open("GUI/Close.nabi", "wb") as f:
					f.write("0")
					log(" ")
					log(" ")
					log("Nabi is now going to sleep (-o-)zzZ")
					log(" ")
					log(" ")
					sys.exit()
			try:
				readbuffer = readbuffer + s.recv(1024)
				temp = string.split(readbuffer, "\n")
				readbuffer = temp.pop()
			except:
				# log(int(time.clock()) - timeLogged)
				if int(time.clock()) - timeLogged >= 60:
					log("Updating Users...")
					timeLogged = int(time.clock())
					userList.updateUsers(s)
					userList.sendListToFile()
				temp = []
			userList.coolCount()
			for line in temp:
				if "PING" == line[0:4]:
					log(line)
					pong = line.replace("PING", "PONG") + " \r\n"
					s.send(pong.encode())
					log(pong)
					break
				user = getUser(line)
				if user.lower() in bList:
					continue
				message = getMessage(line)
				options = message.split(" ")
				UserObj = userList.isInList(user)
				if UserObj == False:
					userList.addUser(User(user.lower()))
					sendMessage(s, "Welcome to the stream " + user + "! a new user profile has been made for you in my database (>w<)/, please enjoy your stay! (^o^)/")
					userList.sendListToFile()
					UserObj = userList.isInList(user)
					UserObj.newComment(message)
				else:
					UserObj.newComment(message)
				commandIssued = options[:][0]
				del options[0]
				if "How's life?" in message:
					sendMessage(s, "I don't know, I'm a bot :/")
				for command in comList.commandsList[:]:
					Check = command[1].check(commandIssued, options)
					if Check == True:
						if UserObj.canUseCommand(s, UserObj, command[1]):
							# log(command[0] + " command found, executing...")
							Success = command[1].execute(s, options, UserObj, userList, comList)
							# log(Success)
							if Success == True:
								UserObj.addCooldown(command[1], command[1].getCooldown())
							break
						else:
							break
					else:
						continue
except:
	logging.exception('Nabi Core Crashed (>w<)')
	with open(LOG_FILENAME, "r") as l:
		d = l.readlines()
		try:
			if d[4].strip().lower() == "systemexit":
				with open("GUI/Status.nabi", "w") as f:
					f.write("Not Running")
					f.truncate()
			elif d[9].strip().lower() == "systemexit":
				with open("GUI/Status.nabi", "w") as f:
					f.write("Not Running")
					f.truncate()
			else:
				sendMessage(s, "/me crashes >o<")
				with open("GUI/Status.nabi", "w") as f:
					f.write("Crashed")
					f.truncate()
				# pass
		except IndexError:
			sendMessage(s, "/me crashes >o<")
			with open("GUI/Status.nabi", "w") as f:
				f.write("Crashed")
				f.truncate()
	raise
	# """offline console testing version"""

	# s = None

	# while True:
		# temp = "Shuruni: " + raw_input("")
		# user = temp.split(": ")[0]
		# message = temp.split(": ")[1]
		# options = message.split(" ")
		# """both"""
		# UserObj = userList.isInList(user)
		# if UserObj == False:
			# userList.addUser(User(user.lower()))
			# sendMessage(s, "Welcome to the stream " + user + "! a new user profile has been made for you in my database (>w<)/, please enjoy your stay! (^o^)/")
			# userList.sendListToFile()
			# UserObj = userList.isInList(user)
		# else:
			# UserObj.newComment()
		# commandIssued = options[:][0]
		# del options[0]
		# print user + " typed: " + message
		# if int(time.clock()) % 60 == 0:
			# print("it is 0")
			# if int(time.clock()) == timeLogged:
				# pass
			# else:
				# timeLogged = int(time.clock())
				# userList.updateUsers(s)
		# """"""
		# if "How's life?" in message:
			# print("I don't know, I'm a bot :/")
			
		# for command in comList.commandsList[:]:
			# Check = command[1].check(commandIssued, options)
			# if Check == True:
				# command[1].execute(s, options, UserObj, userList)
			# else:
				# continue
# def sendMessage(s, message):
		# print message