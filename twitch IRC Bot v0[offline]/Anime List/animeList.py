import csv
import animeLister

class anime(object):
	def __init__(self, name, genres=[], status='', rating=None):
		self.name = name
		self.genres = genres
		self.rating = rating
		self.status = status
	def getName(self):
		return self.name
	def getGenres(self):
		return self.genres[:]
	def getRating(self):
		return self.rating
	def getStatus(self):
		return self.status
	def setName(self, name):
		self.name = name
	def addGenres(self, genre):
		if type(genre) == str:
			self.genres.append(genre)
		elif type(genre) == list or type(genre) == tuple:
			for i in genre:
				self.genres.append(genre)
		else:
			raise(ValueError, "you can't add a genre of type " + type(genre) + " to the genre list!")
	def setGenres(self, genres):
		self.genres = genres[:]
	def setRating(self, rating):
		self.rating = rating
	def setStatus(self, status):
		self.status = status 
	def printData(self):
		print("  Name: " + self.getName() + "\n  Genres: " + ", ".join(self.getGenres()) + "\n  Status: " + self.getStatus() + "\n  Rating: " + str(self.getRating()))
	def __lt__(self, other):
		return self.name < other.name
	def __str__(self):
		return self.name

class animeList(object):
	def __init__(self, fileName = "tempList"):
		self.animeList = []
		self.fileName = str(fileName)
	def getAnimeList(self):
		return self.animeList[:]
	def setAnimeList(self, animeList):
		self.animeList = animeList
	def addAnime(self, anime):
		self.animeList.append(anime)
	def sortByName(self, reverse = False):
		r = self.animeList.sort()
		if reverse:
			r = r.reverse()
	def getAllWithGenres(self, genres):
		animeOfGenre = animeList()
		for a in self.animeList:
			for i in genres:	
				if i.lower() in a.getGenres():
					animeOfGenre.addAnime(a)
					break
		return animeOfGenre		
	def sortByRating(self, reverse = False):
		for i in range(len(self.animeList)):
			for n in range(i,len(self.animeList)):
				if i == n:
					continue
				elif self.animeList[n].getRating() < self.animeList[i].getRating():
					temp = self.animeList[n]
					self.animeList[n] = self.animeList[i]
					self.animeList[i] = temp
		if reverse:
			self.animeList.reverse()
	def sortByStatus(self, reverse = False):
		for i in range(len(self.animeList)):
			for n in range(i,len(self.animeList)):
				if i == n:
					continue
				elif self.animeList[n].getStatus() < self.animeList[i].getStatus():
					temp = self.animeList[n]
					self.animeList[n] = self.animeList[i]
					self.animeList[i] = temp
		if reverse:
			self.animeList.reverse()
	def isInList(self, animeName):
		for a in self.animeList:
			if a.getName().lower() == animeName.lower():
				return True
		return False
	def findAnime(self, animeName):
		for a in self.animeList:
			if a.getName().lower() == animeName.lower():
				return a
	def __str__(self):
		temp = ""
		for i in self.animeList:
			temp += i.getName()
			if i != self.animeList[-1]:
				temp += ", "
		return temp
	def sendToFile(self):
		with open(self.fileName, 'wb') as csvfile:
			animewriter = csv.writer(csvfile)
			animewriter.writerow(['Anime', 'Genres', 'Status', 'Rating'])
			for i in self.animeList:    
				animewriter.writerow([i.getName(), ", ".join(i.getGenres()), i.getStatus(), i.getRating()])


def NewAnime():
	while True:
		Aname = raw_input("Please enter the name of the anime to add to the list: ")
		g = raw_input("confirming that the name of the anime is \"" + Aname + "\" (Y or N)")
		if g.lower() == "y":
			break
		elif g.lower() == "n":
			continue
		else:
			print("Invalid Input, please re-input name of anime")
	Agenres = []
	Status = ''
	ratchk = True
	ratchk2 = True
	RuniRating = ''
	while True:
		g = raw_input("Type 'ADD' to add a genre, ALIST to add multiple separated by commas, or type 'DONE' to move on: ")
		if g.lower() == 'add':
			g = raw_input("Please Type in the name of the genre that the anime falls under: ")
			if g.lower() == "":
				print("no genres added")
			else:
				Agenres.append(g.lower())
		elif g.lower() == 'alist':
			g = raw_input("Please type the genres this anime belongs to separated by commas and a space: ")
			if g.lower() == "":
				print("no genres added")
			else:
				for i in g.split(", "):
					Agenres.append(i.lower())
		elif g.lower() == 'done':
			break
		else:
			print("Invalid Input")
	while ratchk:
		g = raw_input("What is the status of it? (N=Not-seen, W=Watching, C=Completed, H=Hold, D=Dropped) ")
		if g.lower() == 'n':
			Status = "-Not Seen-"
		elif g.lower() == 'w':
			Status = "*Watching*"
		elif g.lower() == 'c':
			Status = "=Completed="
		elif g.lower() == 'h':
			Status = "+On Hold+"
		elif g.lower() == 'd':
			Status = "dropped"
		else:
			print("Invalid Input")
			continue
		while ratchk2:
			g = raw_input("What is your RuniRating of it? (1-10 or 'TL' for favorite)[note: Not-seen anime require an expected rating]")
			if g.lower() == 'tl':
				RuniRating = 'Fav'
				ratchk = False
				break
			for i in range(1,11):
				if g.lower() == str(i):
					RuniRating = str(i)
					ratchk = False
					ratchk2 = False
					break
				elif i == 10:
					print("Invalid Input")
	return anime(Aname, Agenres, Status, RuniRating)

def LoadList(listName,):
	fileName = str(listName) + ".csv"
	List = animeList(fileName)
	animeLoaded = 0
	with open(fileName, 'rb') as csvfile:
		animereader = csv.reader(csvfile)
		for row in animereader:
			if row == ['Anime', 'Genres', 'Status', 'Rating']:
				print("skipped heading...")
				continue
			else:
				List.addAnime(anime(row[0], row[1].split(", "), row[2], row[3]))
				animeLoaded += 1
	print(str(animeLoaded) + " anime loaded from list.")
	return List

ListName = raw_input("Please input the name of the list you wish to access/create: ")
aList = LoadList(ListName)
while True:
	Oalert = raw_input("What would you like to do? \n  (A): Add an anime \n  (C): Check the status of an anime? \n  (Q): Query an animeList by directives? \n  (X):Exit \n ")
	if Oalert.upper() == "X":
		break
	else:
		if Oalert.upper() == "A":
			aList.addAnime(NewAnime())
			aList.sendToFile()
		elif Oalert.upper() == "C":
			ANI = raw_input("Which anime are you searching for? ")
			if aList.isInList(ANI) == True:
				cAnime = aList.findAnime(ANI)
				print("Anime Found!")
				cAnime.printData()
				raw_input()
			else:
				raw_input("oops, looks like that anime is not in this list. ^_^;")
		elif Oalert.upper() == "Q":
			while True:
				query = raw_input("what would you like to find anime by? \n  (L): Letters contained in the name \n  (G): Anime of a specific Genre \n  (S): Current Watching Status \n  (R): Anime of a certain RuniRating \n")
				if query.upper() == "L":
					lquery = raw_input("^w^")
					
				elif query.upper() == "G":
					gquery = raw_input(":o")
					
				elif query.upper() == "S":
					squery = raw_input("^_^;")
					
				elif query.upper() == "R":
					rquery = raw_input(">.<")
					
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	