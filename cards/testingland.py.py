class Test():
	def __init__(self, booly):
		self.one = 1
		self.two = 2
		self.three = 3
		if booly:
			self.four = lambda x: x + 5
		else:
			self.four = False

L1 = "Hazardous 2"
print(L1[L1.index("Hazardous") + 10])
tuply = "game", "set"
print(tuply[0])