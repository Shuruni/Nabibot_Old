


class Wallet(object):
	def __init__(self, balance=0, income=10, expenses=5):
		self.balance = balance
		self.income = income
		self.expenses = expenses
		
	def getBalance(self):
		return self.balance
	
	def getIncome(self):
		return self.income
	
	def getExpenses(self):
		return self.expenses
	
	def canPay(self, amount):
		if amount > self.balance:
			return False
		else:
			return True
	
	def pay(self, amount):
		self.balance -= amount
	
	def recieve(self, amount):
		self.balance += amount
	
	def updateWallet(self):
		self.balance += self.income
		self.balance -= self.expenses
	
	def payRaise(self, increase):
		self.income += increase
	
	def payCut(self, decrease):
		self.income -= decrease
	
	def extraExpenses(self, increase):
		self.expenses += increase
	
	def expenseDrops(self, decrease):
		self.expenses -= decrease
	
	def newJob(self, income, expenses):
		self.income = income
		self.expenses = expenses