level = 9001
exptemp = 0
for i in range(level):
	exp += i*i
	print exp

def calcLevelFromExp(self, exp):
		exptemp = 0
		currentLevel = 0
		While True:
			exptemp += currentLevel*currentLevel + (10*(currentLevel+1))
			if exp < exptemp:
				return currentLevel
			else:
				currentLevel += 1
				continue

def expToNextLevel(self, exp, level):
	#returns a list so that list[0] == needed & list[1] == [current, required]
	nextLevelExp = 0
	for i in range(level+1):
		nextLevelExp += i*i+(10(i+1))
	return [nextLevelExp - exp, [exp,nextLevelExp]]
	
