import socket
from Settings import *
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
	print("Sent: " + messageTemp)

# """offline console testing version"""
# def sendMessage(s, message):
	# print message