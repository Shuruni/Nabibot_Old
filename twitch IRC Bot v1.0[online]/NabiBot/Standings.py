


class Standing(object):
	def __init__(self):
		self.position = "Standing"
		self.permissions = []  #command types useable ex. [fun.roll, Socket.sendMessage, math.calc]
	def getPermissions(self):
		return self.permissions[:]
	def hasPermission(self, permission):
		if permission in self.permissions:
			return True
		else:
			return False
	def currentStanding(self):
		return self.position

class Newbie(Standing):
	def __init__(self):
		self.position = "Newbie"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class Fledgling(Standing):
	def __init__(self):
		self.position = "Fledgling"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class CommonFace(Standing):
	def __init__(self):
		self.position = "CommonFace"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class LoyalFollower(Standing):
	def __init__(self):
		self.position = "LoyalFollower"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class Veteran(Standing):
	def __init__(self):
		self.position = "Veteran"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class NoLifer(Standing):
	def __init__(self):
		self.position = "NoLifer"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class SpecialPerson(Standing):
	def __init__(self):
		self.position = "SpecialPerson"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class Pots_(Standing):
	def __init__(self):
		self.position = "Pots_"
		self.permissions = ["fun.roll", "Socket.sendMessage"]

class Donator(Standing):
	def __init__(self):
		self.position = "Donator"
		self.permissions = ["fun.roll", "Socket.sendMessage"]
	
class Shuruni(Standing):
	def __init__(self):
		self.position = "Shuruni"
		self.permissions = ["everything"]