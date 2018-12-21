import socket
from Startup.Settings import *
import time
"""online standard version"""
def openSocket():
	s = socket.socket()
	s.connect((HOST,PORT))
	s.send("PASS " + PASS + "\r\n")
	s.send("NICK " + NICK + "\r\n")
	s.send("JOIN #" + CHANNEL + "\r\n")
	return s
	
def sendMessage(s, message):
	messageTemp = "PRIVMSG #" + CHANNEL + " :" + message + "\r\n"
	s.send(messageTemp.decode("utf-8", "replace").encode("utf-8", "replace"))
	cTime = time.strftime("[%I:%M:%S%p] ", time.localtime())
	log("CILM: >W< " + cTime + " NabiBot_: " + message)

def parseSend(user, s, text):
	cCharLen = 350
	log(len(text))
	if len(text) > cCharLen :
		temp = text
		temp2 = temp.split(", ")
		# log(temp)
		# log(temp2)
		cLen = 0
		combine = ""
		printList = []
		for sentence in temp2:
			sentence += ", "
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
			sendMessage(s, message)
			time.sleep(2)
			
	else:
		sendMessage(s, text)

def log(message):
	with open("GUI/Log.nabi", "a") as f:
		f.write(str(message)+"\n")
	
# """offline console testing version"""
# def sendMessage(s, message):
	# print message