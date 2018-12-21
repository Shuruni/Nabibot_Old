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
	Seen = ''
	ratchk = True
	ratchk2 = True
	RuniRating = ''
	while True:
		g = raw_input("Type 'ADD' to add a genre or type 'DONE' to move on: ")
		if g.lower() == 'add':
			g = raw_input("Please Type in the name of the genre that the anime falls under: ")
			if g.lower() == "":
				print("no genres added")
			else:
				Agenres.append(g)
		elif g.lower() == 'done':
			break
		else:
			print("Invalid Input")
	while ratchk:
		g = raw_input("Have you seen it before? ")
		if g.lower() == 'yes':
			Seen = "Yes"
		elif g.lower() == 'no':
			Seen = "No"
		else:
			print("Invalid Input")
			continue
		while ratchk2:
			g = raw_input("What is your RuniRating of it? (1-10 or 'TL' for favorite)")
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
	return[Aname, Agenres, Seen, RuniRating]