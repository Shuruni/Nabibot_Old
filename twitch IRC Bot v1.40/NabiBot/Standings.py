
Standings = ("Newbie", "Fledgling", "CommonFace", "LoyalFollower", "Veteran", "NoLifer", "SpecialPerson", "Moderator", "Shuruni")
NonLVStandings = ("SpecialPerson", "Moderator", "Shuruni")

class Standing(object):
	def __init__(self):
		self.reqLevel = None
		self.position = "Standing"
		self.restrictions = []  #command types useable ex. [fun.roll, math.add()]
	def getRestrictions(self):
		return self.restrictions[:]
	def hasRestrictions(self, restriction):
		if restriction in self.restrictions:
			return True
		else:
			return False
	def currentStanding(self):
		return self.position

class Newbie(Standing):
	def __init__(self):
		#level 0
		self.reqLevel = 0
		self.position = "Newbie"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()","Nabi.ExpressionList()","dummy.add()","dummy.remove()","Nabi.rating()","Osu.skin()","coin.shop()"]

class Fledgling(Standing):
	def __init__(self):
		#level 5
		self.reqLevel = 5
		self.position = "Fledgling"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()","Nabi.ExpressionList()","dummy.add()","dummy.remove()","Nabi.rating()"]

class CommonFace(Standing):
	def __init__(self):
		#level 10
		self.reqLevel = 10
		self.position = "CommonFace"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()","dummy.add()","dummy.remove()"]

class LoyalFollower(Standing):
	def __init__(self):
		#level 15 extra permissions to enact events
		self.reqLevel = 15
		self.position = "LoyalFollower"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()","dummy.add()","dummy.remove()"]

class Veteran(Standing):
	def __init__(self):
		#level 20 extra permissions to enact events
		self.reqLevel = 20
		self.position = "Veteran"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()","dummy.add()","dummy.remove()"]

class NoLifer(Standing):
	def __init__(self):
		#level 25 !add and !remove
		self.reqLevel = 25
		self.position = "NoLifer"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()"]

class SpecialPerson(Standing):
	def __init__(self):
		#anyone helping me in nabi dev or been here for a while... basically special persona s the name suggests
		self.position = "SpecialPerson"
		self.restrictions = ["Occupation.oChange()", "Standings.change()", "debug.exit()","coin.add()","coin.remove()","coin.set()"]

class Moderator(Standing):
	def __init__(self):
		#moderators, duh
		self.position = "Moderator"
		self.restrictions = ["Occupation.oChange()", "coin.add()","coin.remove()","coin.set()"]
		
class Shuruni(Standing):
	def __init__(self):
		self.position = "Shuruni"
		self.restrictions = []