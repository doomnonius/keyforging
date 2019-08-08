class Test():
	def __init__(self, booly):
		self.one = 1
		self.two = 2
		self.three = 3
		if booly:
			self.four = lambda x: x + 5
		else:
			self.four = False

test = Test(True)
other = Test(False)
both = [test, other]
for x in both:
	if x.four:
		print(x.four)