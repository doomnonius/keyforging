activeBoard = [20, 53, "Cheese", 234, "Money"]
pendingDiscard = []

for x in range(len(activeBoard)):
	# so that i can work from right to left
	x = abs(x - len(activeBoard) + 1)
	pendingDiscard.append(activeBoard[x])

print(pendingDiscard)