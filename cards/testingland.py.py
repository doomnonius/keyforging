def absa(num, L):
	return abs(num - len(L) + 1)
active = [5, 6, 7, 8, 9, 10]
length = len(active)
purge = []
count = 0
[(count.__add__(1), purge.append(active.pop(abs(x - length + 1)))) for x in range(len(active)) if active[abs(x - length + 1)] % 2 == 0]
count.__add__(1)
print(count)
print(purge)
print(active)
# assert purge == [6, 8, 10]
# assert active == [5, 7, 9]