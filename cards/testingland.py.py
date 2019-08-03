discard = []
deck = []
hand = []

if len(deck) > 0 and (deck[-1].house != "Brobnar" or deck[-1].type != "Creature"):
	discard.append(deck.pop())
	print(repr(deck[-1]))
elif len(deck) == 0:
	print("Your deck is empty, and you found no Brobnar creatures.")
else: # House is brobnar and type is creature if we get here
	hand.append(deck.pop())