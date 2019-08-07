import time
import random
from functools import reduce
# I think it makes more sense to add these to the cardsAsClass file, which means that the only function here is addToBoard

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

def absa(num, length):
	return abs(num - length + 1)

def backwardsList(input_L, actionstring, compstring, result_L = []):
	""" [pendingDiscard.append(active.pop(abs(x - len(active) + 1))) for x in range(len(active)) if active[abs(x - len(active) + 1)].captured > 0]
	"""
	print("This function is deprecated.")

def makeChoice(stringy, L = []):
	""" Takes a string explaining the choice and a list, only accepts results within the length of the list, unless the list is empty, then it just returns the number.
	"""
	if L != 0:
		[print(str(x) + ": " + str(L[x])) for x in range(len(L))]
	while True:
		try:
			choice = int(input(stringy))
			if 0 <= choice < len(L):
				return choice
			elif L == []:
				return choice
			else:
				raise IndexError
		except:
			pass

def passFunc(game, card):
	return

def pending(game, L, destination, fromPlay = True, ask = False):
	""" A function that deals with pending piles of cards.
	Arguments: game should be self-evident, it's needed to be able to modify the game, L is the list being emptied, and destination is the list being appended to.
	"""
	# need to update this, but if destination is discard and source is from play then check for annihilation ritual, etc
	# also needs to confirm that it's putting cards in the right discard pile b/c creatures can be stolen
	# will also reset cards when putting them anywhere (dealing with captured amber, losing extra power, extra armor, upgrades, etc.)
	if L == []:
		return
	length = len(L)
	for x in range(len(L)):
		if destination == game.activePlayer.discard and L[abs(x - length + 1)].deck != game.activePlayer.name:
			game.inactivePlayer.discard.append(L.pop(abs(x - length + 1)))
		elif destination == game.inactivePlayer.discard and L[abs(x - length + 1)].deck != game.inactivePlayer.name:
			game.activePlayer.discard.append(L.pop(abs(x - length + 1)))
	if (destination == game.activePlayer.discard or destination == game.inactivePlayer.discard) and ("Annihilation Ritual" in [x.title for x in game.activePlayer.board["Artifact"]] or "Annihilation Ritual" in [x.title for x in game.inactivePlayer.board["Artifact"]]):
		if destination == game.activePlayer.discard:
			destination = game.activePlayer.purge
		else: # because destination has to be one or the other for this to pass, we don't need to explicitly state the second
			destination = game.inactivePlayer.purge
	final = len(L) + len(destination)
	game.activePlayer.printShort(L, False)
	if not ask:
		destination.extend(L) # list will be reset in higher order function
		return
	while len(L) > 1:
		choice = makeChoice("Choose which card to add to the top of your deck next: ", L)
		destination.append(L.pop(choice))
	destination.append(L.pop())
	if len(L) > 0:
		raise ValueError("card.pending did not properly empty the list.")
	if len(destination) != final:
		raise ValueError("card.pending did not extend the destination the correct length")

def chooseSide(game, stringy = "Creature", choices = True):
	""" A return of 0 is friendly, 1 is enemy. Strings can make it deal with different lists. Choices set to true returns choice, side; set to false returns only side. Returns two empty strings if both sides are empty.
	"""
	activeBoard = game.activePlayer.board[stringy]
	inactiveBoard = game.inactivePlayer.board[stringy]
	
	side = ''
	if len(inactiveBoard) == 0 and len(activeBoard) == 0:
		print("There are no " + stringy.lower() + "s to target. The card is still played.")
		return side, side
	elif len(inactiveBoard) == 0:
		game.activePlayer.printShort(activeBoard, True)
		side = 0
		if choices:
			choice = makeChoice("There are no enemy " + stringy.lower() + "s to target, so you must choose a friendly " + stringy.lower() + " to target: ", activeBoard)
			return choice, side
	else:
		while side != "Friendly" and side != "Enemy":
			side = input("Would you like to target an [enemy] " + stringy.lower() + " or a [friendly] " + stringy.lower() + "?").title()
		if side == "Friendly":
			game.activePlayer.printShort(activeBoard, True)
			side = 0
			if choices:
				choice = makeChoice("Choose a target: ", activeBoard)
				return choice, side
		elif side == "Enemy":
			game.activePlayer.printShort(inactiveBoard, True)
			side = 1
			if choices:
				choice = makeChoice("Choose a target: ", inactiveBoard)
				return choice, side
	return side

def stealAmber(thief, victim, num):
	if victim.amber >= num:
		victim.amber -= num
		thief.amber += num
		print(thief.name + " stole " + str(num) + " amber from " + victim.name + ".")
	else:
		thief.amber += victim.amber
		if victim.amber == 0:
			print("Your opponent had no amber to steal. The card is stil played.")
			return
		print("Your opponent only had " + victim.amber + " amber for you to steal.")
		victim.amber = 0

## Start House Brobnar

def key001(game, card):
	"""Anger. Ready and fight with a friendly creature.
	"""
	print("\nYour creatures:")
	game.activePlayer.printShort(game.activePlayer.board["Creature"], False)
	print("")
	if len(game.activePlayer.board["Creature"]) == 0:
		print("You have no creatures to target. The card is still played.")
		return
	choice = makeChoice("Choose a friendly creature to ready: ", game.activePlayer.board["Creature"])
	if not game.activePlayer.board["Creature"][choice].ready:
		game.activePlayer.board["Creature"][choice].ready = True
		game.fightCard(choice)
	else:
		game.fightCard(choice)


def key002(game, card):
	"""Barehanded. Put Each artifact on top of its owner's \
	deck.
	"""
	# can't use a while loop b/c active player chooses order
	if len(game.activePlayer.board["Artifact"]) > 1:
		pendingDeck = []
		while len(game.activePlayer.board["Artifact"]) > 0:
			pendingDeck.append(game.activePlayer.board["Artifact"].pop())
	elif len(game.activePlayer.board["Artifact"]) == 1:
		game.activePlayer.deck.append(game.activePlayer.board["Artifact"].pop())
	pending(game, pendingDeck, game.activePlayer.deck)
	# run it all again w/ inactive player
	if len(game.inactivePlayer.board["Artifact"]) > 1:
		pendingDeck = []
		while len(game.inactivePlayer.board["Artifact"]) > 0:
			pendingDeck.append(game.inactivePlayer.board["Artifact"].pop())
	elif len(game.inactivePlayer.board["Artifact"]) == 1:
		game.inactivePlayer.deck.append(game.inactivePlayer.board["Artifact"].pop())
	pending(game, pendingDeck, game.inactivePlayer.deck)

def key003(game, card):
	"""Blood Money: Place 2 amber from the common supply on an enemy creature.
	"""
	if len(game.inactivePlayer.board["Creature"]) == 0:
		print("Your opponent has no creatures for you to target. The card is still played.")
		return
	else:
		game.inactivePlayer.printShort(game.inactivePlayer.board["Creature"])
		choice = makeChoice("Choose an enemy creature to gain two amber: ", game.inactivePlayer.board["Creature"])
		game.inactivePlayer.board["Creature"][choice].captured += 2
		print(game.inactivePlayer.board["Creature"][choice].title + " now has " + game.inactivePlayer.board["Creature"][choice].amber + " amber.")
		return
				
def key004(game, card):
	""" Brothers in Battle: Value: 1 amber. Choose a house. For the remainder of the turn, each friendly creature of that house may fight.
	"""
	game.chooseHouse("extraFight") # this function will add extra houses that only work for fighting

def key005(game, card):
	"""Burn the Stockpile: If your opponent has 7 or more amber, they lose 4.
	"""
	if game.inactivePlayer.amber > 6:
		game.inactivePlayer.amber -= 4
		print("Your opponent had " + str(game.inactivePlayer.amber + 4) + " amber, and you destroyed 4, leaving them with " + str(game.inactivePlayer.amber) + " amber." )
	else:
		print("Your opponent didn't have enough amber, so you didn't destroy anything. The card is still played.")

def key006 (game, card):
	""" Champion's Challenge: Destroy each enemy creature except the most powerful enemy creature. Destroy each friendly creature except the most powerful friendly creature. Ready and fight with your remaining creature.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]

	pendingDiscard = []	# this one's fine b/c it does actually happen one at a time
	# inactive board first
	if len(inactiveBoard) > 1:
		# find highest power
		high = max([x.power for x in inactiveBoard])
		# discard all cards that aren't tied
		n = 0
		while min([x.power for x in inactiveBoard]) < high:
			if inactiveBoard[n].power < high:
				pendingDiscard.append(inactiveBoard.pop(n))
			else:
				n += 1
				if n == len(inactiveBoard):
					break
		# check length of inactiveBoard, if > 1, let player choose which one to keep
		if len(inactiveBoard) > 1:
			game.inactivePlayer.printShort(inactiveBoard)
			choice = makeChoice("Choose which enemy creature will survive: ", inactiveBoard)
			# then discard all cards except choice
			while len(inactiveBoard > 1):
				# easy part: choice at beginning of list
				if choice == 0: pendingDiscard.append(inactiveBoard[1])
				else:
					pendingDiscard.append(inactiveBoard[0])
					choice -= 1
		pending(game, pendingDiscard, game.inactivePlayer.discard)

	# i don't need to restate pending discard as empty, because pending() will raise an error if the list isn't emptied

	# then active board
	if len(activeBoard) > 1:
		# find highest power
		high = max([x.power for x in activeBoard])
		# discard all cards that aren't tied
		n = 0
		while min([x.power for x in activeBoard]) < high:
			if activeBoard[n].power < high:
				pendingDiscard.append(activeBoard.pop(n))
			else:
				n += 1
				if n == len(activeBoard):
					break
		# check length of activeBoard, if > 1, let player choose which one to keep
		if len(activeBoard) > 1:
			game.activePlayer.printShort(activeBoard)
			choice = makeChoice("Choose which friendly creature will survive: ", activeBoard)
			# then discard all cards except choice
			while len(activeBoard > 1):
				# easy part: choice at beginning of list
				if choice == 0: pendingDiscard.append(activeBoard[1])
				else:
					pendingDiscard.append(activeBoard[0])
					choice -= 1
		pending(game, pendingDiscard, game.activePlayer.discard)

	# then ready and fight with remaining minion
	print("\nYour creature:")
	game.activePlayer.printShort(game.activePlayer.board["Creature"], False)
	print("")
	if len(game.activePlayer.board["Creature"]) == 0:
		print("You have no creatures to target. The card is still played.")
		return
	choice = 0 # because only 1 creature
	if not game.activePlayer.board["Creature"][choice].ready:
		game.activePlayer.board["Creature"][choice].ready = True
		game.fightCard(choice)
	else:
		game.fightCard(choice)

def key007 (game, card):
	"""Coward's End: Destroy each undamaged creature. Gain 3 chains.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	length = len(activeBoard)
	# active player
	undamageList = [x.damage for x in activeBoard if x.damage == 0]
	# easy case: everything undamaged
	if len(undamageList) == len(activeBoard): pendingDiscardA = activeBoard
	else:
		[pendingDiscardA.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].damage == 0]
		# for x in range(len(activeBoard)):
			# so that i can work from right to left
			# x = abs(x - len(activeBoard) + 1)
			# if activeBoard[x].damage > 0:
			# 	pendingDiscard.append(activeBoard.pop(x))
	length = len(inactiveBoard)
	# inactive player
	undamageList = [x.damage for x in inactiveBoard if x.damage == 0]
	# easy case: everything undamaged
	if len(undamageList) == len(inactiveBoard): pendingDiscardI = inactiveBoard
	else:
		[pendingDiscardI.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].damage == 0]
		# for x in range(len(inactiveBoard)):
		# 	# so that i can work from right to left
		# 	x = abs(x - len(inactiveBoard) + 1)
		# 	if inactiveBoard[x].damage > 0:
		# 		pendingDiscard.append(inactiveBoard.pop(x))
	
	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)
	
	# finally, add chains
	game.activePlayer.chains += 3

def key008(game, card):
	"""Follow the Leader: For the remainder of the turn, each friendly creature may fight.
	"""
	# as easy as setting game.extraFightHouses to all houses
	game.extraFightHouses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]

def key009 (game, card):
	"""Lava Ball: Deal 4 damage to a creature with 2 splash.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	pendingDiscard = [] # this one's fine because only one side is ever affected

	choice, side = chooseSide(game)

	# now that target is chosen, apply damages
	if side == 0:
		activeBoard[choice].damageCalc(4)
		try: 
			activeBoard[choice + 1].damageCalc(2)
			right = True
		except: print("This creature has no neighbor on the right.")
		try: 
			activeBoard[choice - 1].damageCalc(2)
			left = True
		except: print("This creature has no neighbor on the left.")
		if activeBoard[choice].update():
			pendingDiscard.append(activeBoard.pop(choice))
		if right == True:
			if activeBoard[choice + 1].update():
				pendingDiscard.append(activeBoard.pop(choice + 1))
		if left == True:
			if activeBoard[choice - 1].update():
				pendingDiscard.append(activeBoard.pop(choice - 1))
		pending(game, pendingDiscard, game.activePlayer.discard)
	elif side == 1:
		inactiveBoard[choice].damageCalc(4)
		try: 
			inactiveBoard[choice + 1].damageCalc(2)
			right = True
		except: print("This creature has no neighbor on the right.")
		try: 
			inactiveBoard[choice - 1].damageCalc(2)
			left = True
		except: print("This creature has no neighbor on the left.")
		if inactiveBoard[choice].update():
			pendingDiscard.append(inactiveBoard.pop(choice))
		if right == True:
			if inactiveBoard[choice + 1].update():
				pendingDiscard.append(inactiveBoard.pop(choice + 1))
		if left == True:
			if inactiveBoard[choice - 1].update():
				pendingDiscard.append(inactiveBoard.pop(choice - 1))
		pending(game, pendingDiscard, game.inactivePlayer.discard)

def key010(game, card):
	""" Loot the Bodies: For the remainder of the turn, gain 1 amber each time an enemy creature is destroyed.
	"""
	if not game.activePlayer.states["Destroyed"]["Loot the Bodies"][0]:
		game.activePlayer.states["Destroyed"].update({"Loot the Bodies": [True]})
	else: # for handling multiples of a card
		game.activePlayer.states["Destroyed"]["Loot the Bodies"].append(True)
	# skipping the rest for now, until event emitters or etc are figured out

def key011 (game, card):
	"""Take that, Smartypants: Steal 2 amber if your opponent has 3 or more Logos cards in play.
	"""
	inactiveBoard = game.inactivePlayer.board
	count = 0
	for x in (inactiveBoard["Creature"] + inactiveBoard["Artifact"]):
		if x.house == "Logos":
			count += 1
	if count >= 3:
		stealAmber(game.activePlayer, game.inactivePlayer, 2)
	else:
		print("Your opponent had less than 3 Logos cards in play, so you didn't steal anything. The card is still played.")


def key012 (game, card):
	""" Punch: Deal 3 damage to a creature.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	pendingDiscard = [] # fine b/c only one side ever affected

	choice, side = chooseSide(game)
	# side == 0, active board
	if side == 0:
		activeBoard[choice].damageCalc(3)
		if activeBoard[choice].update:
			pendingDiscard.append(activeBoard[choice])
	else:
		inactiveBoard[choice].damageCalc(3)
		if inactiveBoard[choice].update:
			pendingDiscard.append(inactiveBoard[choice])

def key013(game, card):
	""" Relentless Assault: Ready and fight with up to 3 friendly creatures, one at a time.
	"""
	if len(game.activePlayer.board["Creature"]) >= 3:
		count = 3
	else:
		count = len(game.activePlayer.board["Creature"])
	disallow = []
	died = True
	while count > 0:
		activeBoard = game.activePlayer.board["Creature"]
		original = len(activeBoard)
		game.activePlayer.printShort(activeBoard)
		if False not in [(x in disallow) for x in activeBoard]:
			print("There are no more valid targets.")
			return
		choice = makeChoice("Choose a creature to fight with: ", activeBoard)
		# first choice should always be valid
		if activeBoard[choice] not in disallow:
			activeBoard[choice].ready = True
			game, died = game.fightCard(choice)
		else:
			print("You've already chosen that minion. Try again.")
			count += 1
			died = True
		# make game equal the result of this function call, so that if anything died we have the new board state
		if died:
			# this doesn't account for phoenix heart
			pass
		elif not died and original == len(game.activePlayer.board["Creature"]):
			disallow.append(activeBoard[choice])
		count -= 1

def key014 (game, card):
	"""Smith: Gain 2 amber if you control more creatures than your opponent.
	"""
	if len(game.activePlayer.board["Creature"]) > len(game.inactivePlayer.board["Creature"]):
		game.activePlayer.amber += 2
		print("You have more creatures, so you gain 2 amber.")
	else:
		print("You do not have more creatures, so you don't gain any amber. The card is still played.")

def key015 (game, card):
	"""Sound the Horns: Discard cards from the top of your deck until you either discard a Brobnar creature or run out of cards. If you discarded a Brobnar creature this way, put it into your hand.
	"""
	discard = game.activePlayer.discard
	deck = game.activePlayer.deck
	hand = game.activePlayer.hand
	if len(deck) > 0 and (deck[-1].house != "Brobnar" or deck[-1].type != "Creature"): # avoids indexerror because if len(deck) evaluates to False, it skips looking at the rest of the statement
		discard.append(deck.pop())
		print(repr(discard[-1]))
		time.sleep(3)
	elif len(deck) == 0:
		print("Your deck is empty, and you found no Brobnar creatures.")
	else: # House is brobnar and type is creature if we get here
		hand.append(deck.pop())
		print(repr(hand[-1]))

def key016(game, card):
	"""Tremor: Stun a creature and each of its neighbors.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.activePlayer.board["Creature"]
	choice, side = chooseSide(game)
	if side == 0:
		game.activePlayer.printShort(activeBoard)
		activeBoard[choice].stun = True
		try: activeBoard[choice + 1].stun = True
		except: print("This creature has no right neighbor.")
		try: activeBoard[choice - 1].stun = True
		except: print("This creature has no left neighbor.")
	else:
		game.activePlayer.printShort(inactiveBoard)
		inactiveBoard[choice].stun = True
		try: inactiveBoard[choice + 1].stun = True
		except: print("This creature has no right neighbor.")
		try: inactiveBoard[choice - 1].stun = True
		except: print("This creature has no left neighbor.")

def key017(game, card):
	"""Unguarded Camp: For each creature you have in excess of your opponent, a friendly creature captures 1 amber. Each creature cannot capture more than 1 amber this way.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	diff = len(activeBoard) - len(inactiveBoard)

	if diff < 0:
		print("You have less creatures than your opponent, so no amber is captured. The card is stil played.")
		return
	elif diff == 0:
		print("You have as many creatures as your opponent, so no amber is captured. The card is still played.")
		return
	print("You have " + diff + " more minions than your opponent, so you will capture " + diff + "amber.")
	if diff == len(activeBoard):
		[x.capture(game, 1) for x in activeBoard]
		return
	disallow = []
	while diff > 0:
		[print(x + ": " + str(activeBoard[x])) for x in range(len(activeBoard)) if activeBoard[x] not in disallow]
		choice = makeChoice("Choose a minion to capture an amber. Only valid options are shown: ", activeBoard)
		activeBoard[choice].capture(game, 1)
		disallow.append(activeBoard[choice])
		diff -= 1

def key018(game, card):
	"""Warsong: For the remainder of the turn, gain 1 amber each time a friendly creature fights.
	"""
	if not game.activePlayer.states["Fight"]["Warsong"][0]:
		game.activePlayer.states["Fight"].update({"Warsong":[True]})
	else:
		game.activePlayer.states["Fight"]["Warsong"].append(True)
	# should be able to account for multiple instances of warsong

def key030(game, card):
	"""Bumpsy: Your opponent loses one amber.
	"""
	victim = game.inactivePlayer.amber
	if victim > 0: 
		print("Your opponent had " + str(victim) + " amber.")
		game.inactivePlayer.amber -= 1
		print("They now have " + str(game.inactivePlayer.amber) + " amber.")
		return
	print("Your opponent had no amber to lose.")



def key031(game, card):
	"""Earthshaker: Destroy each creature with power 3 or lower.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	length = len(activeBoard)
	# active board: LC
	[pendingDiscardA.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].power <= 3]
	pending(game, pendingDiscardA, game.activePlayer.discard)
	# then inactive
	length = len(inactiveBoard)
	[pendingDiscardI.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].power <= 3]
	pending(game, pendingDiscardI, game.inactivePlayer.discard)

def key033(game, card):
	"""Ganger Chieftain: You may ready and fight with a neighboring creature.
	"""
	activeBoard = game.activePlayer.board["Creature"]

	if len(activeBoard) == 0:
		return

	if activeBoard.index(card) == 0:
		maybe = input("Would you like to ready and fight with " + str(activeBoard[1]) + " [Y/n]?").title()
		if maybe == '' or maybe == "Y" or maybe == "Yes":
			activeBoard[1].ready = True
			game.fightCard(1)
		return
	elif activeBoard.index(card) == len(activeBoard)-1:
		maybe = input("Would you like to ready and fight with " + str(activeBoard[(len(activeBoard)-2)]) + " [Y/n]?").title()
		if maybe == '' or maybe == "Y" or maybe == "Yes":
			activeBoard[(len(activeBoard)-2)].ready = True
			game.fightCard(len(activeBoard)-2)
		return

def key036(game, card):
	"""Hebe the Huge: Deal 2 damage to each other undamaged creature.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []

	# deal damage
	[x.damageCalc(2) for x in activeBoard if x.damage == 0 and activeBoard.index(x) != activeBoard.index(card)]
	# deal damage
	[x.damageCalc(2) for x in inactiveBoard if x.damage == 0]
	# check for deaths
	length = len(activeBoard)
	[pendingDiscardA.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].update()]
	pending(game, pendingDiscardA, game.activePlayer.discard)
	# check for deaths
	length = len(inactiveBoard)
	[pendingDiscardI.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].update()]
	pending(game, pendingDiscardI, game.activePlayer.discard)

def key040(game, card):
	"""Lomir Flamefist: If your opponent has 7 or more amber, they lose 2.
	"""
	victim = game.inactivePlayer.amber
	if victim >= 7:
		print("Your opponent had " + str(victim) + " amber. They now have " + str(victim - 2) + " amber.")
		game.inactivePlayer.amber -= 2
		return
	print("Your opponent only had " + str(victim) + " amber. They don't lose anything.")

def key046(game, card):
	"""Smaaash: Stun a creature.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	choice, side = chooseSide(game)
	if side == 0:
		game.activePlayer.printShort(activeBoard)
		activeBoard[choice].stun = True
	else:
		game.inactivePlayer.printShort(inactiveBoard)
		inactiveBoard[choice].stun = True

def key049(game, card):
	"""Wardrummer: Return each other friendly Brobnar creature to your hand.
	"""
	index = game.activePlayer.board["Creature"].index(card)
	activeBoard = game.activePlayer.board["Creature"]
	length = len(activeBoard)
	[game.activePlayer.hand.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].house == 'Brobnar' and abs(x - length + 1) != index]

def key052(game, card):
	"""Yo Mama Mastery: Fully heal this creature
	"""
	# I'm going to only handle the play effect, I'll write something else to handle upgrades later
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	choice, side = chooseSide(game)
	if side == 0:
		game.activePlayer.printShort(activeBoard)
		activeBoard[choice].damage = 0
		return
	game.inactivePlayer.printShort(inactiveBoard)
	inactiveBoard[choice].damage = 0

## End House Brobnar

#######
# Dis #
#######

def key053(game, card):
	""" A Fair Game: Discard top card of opp's deck, reveal their hand. Gain amber for each card in hand matching house of discarded card. Opponent repeats effect on you.
	"""
	count = 0
	if len(game.inactivePlayer.deck) > 0:
		game.inactivePlayer.discard.append(game.inactivePlayer.deck.pop())
		print("Your opponent discarded: \n")
		print(repr(game.inactivePlayer.deck[-1]) + "\n")
		house = game.inactivePlayer.deck[-1].house
		[print(x + ": " + str(x)) for x in game.inactivePlayer.hand]
		for x in game.inactivePlayer.hand:
			if x.house == house:
				count += 1
		print("Your opponent has " + str(count) + " cards in their hand of the same house as the discarded card. You gain that much amber.")
	else:
		print("Your opponent has no cards to discard, so you gain no amber. The card is still played.")
	game.activePlayer.amber += count
	count = 0
	if len(game.activePlayer.deck) > 0:
		game.activePlayer.discard.append(game.activePlayer.deck.pop())
		print("Your opponent discarded: \n")
		print(repr(game.activePlayer.deck[-1]) + "\n")
		house = game.activePlayer.deck[-1].house
		[print(x + ": " + str(x)) for x in game.activePlayer.hand]
		for x in game.activePlayer.hand:
			if x.house == house:
				count += 1
		print("You have " + str(count) + " cards in your hand of the same house as the discarded card. Your opponent gains that much amber.")
	else:
		print("You have no cards to discard, so your opponent gains no amber. The card is still played.")
	game.inactivePlayer.amber += count

def key054(game, card):
	"""Arise!: Choose a house. Return each creature of that house from your discard pile to your hand.
	"""
	active = game.activePlayer.discard
	house = ''
	while house == '':
		house = input("Choose a house: ").title()
		if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]: break
		else: house = ''
	# return cards from discard pile
	length = len(active)
	[game.activePlayer.hand.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].house == house and active[abs(x - length + 1)].type == "Creature"]
	# finally, add chains
	game.activePlayer.chains += 1

def key055(game, card):
	""" Control the Weak: Choose a house on opp's id card, they must choose that house on next turn.
	"""
	house = ''
	while house == '':
		house = input("Choose a house: ").title()
		if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]: break
		else: house = ''
	game.inactivePlayer.states["House"].update({"Control the Weak":house})

def key056(game, card):
	""" Creeping Oblivion: purge up to 2 cards from a discard pile.
	"""
	activeDisc = game.activePlayer.discard
	inactiveDisc = game.inactivePlayer.discard
	# chooseSide only works for things that target minions
	side = input("Would you like to purge from the [enemy] discard, [friendly] discard, or purge [nothing]?\n>>>").title()
	while True:
		if side == "Enemy":
			n = 2
			while n > 0:
				if len(inactiveDisc) == 0:
					print("Your opponent's discard is empty.")
					break
				game.activePlayer.printShort(inactiveDisc)
				choice = makeChoice("Choose a card to purge: ", inactiveDisc)
				game.inactivePlayer.purge.append(inactiveDisc.pop
				(choice))
				n -= 1
				if n > 0:
					again = input("Would you like to purge another card [Y/n]?").title()
					if "Y" not in again:
						n = 0
			break
		elif side == "Friendly":
			n = 2
			while n > 0:
				if len(activeDisc) == 0:
					print("Your discard is empty.")
					break
				game.activePlayer.printShort(activeDisc)
				choice = makeChoice("Choose a card to purge: ", activeDisc)
				game.inactivePlayer.purge.append(activeDisc.pop
				(choice))
				n -= 1
				if n > 0:
					again = input("Would you like to purge another card [Y/n]?").title()
					if "Y" not in again:
						n = 0
		elif side == 'Nothing':
			pass
		else:
			side = input("Invalid input. Would you like to purge from the [enemy] discard, [friendly] discard, or purge [nothing]?\n>>>").title()

def key057(game, card):
	""" Dance of Doom: Choose a number. Destroy each creature with power equal to that number.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.activePlayer.board["Creature"]
	pendingDestroyed = []
	choice = makeChoice("Choose a number. All creatures with power equal to this number will be destroyed: ")
	# active player
	length = len(active)
	[pendingDestroyed.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].power == choice]
	pending(game, pendingDestroyed, game.activePlayer.discard)
	#inactive player
	length = len(inactive)
	[pendingDestroyed.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].power == choice]
	pending(game, pendingDestroyed, game.inactivePlayer.discard)

def key058(game, card):
	""" Fear: Return an enemy creature to its owner's hand.
	"""
	inactive = game.inactivePlayer.board["Creature"]
	if len(inactive) == 0:
		print("Your opponent has no creatures to target. The card is still played.")
		return
	elif len(inactive) == 1:
		choice = 0
	else:
		choice = makeChoice("Choose a minion to return to your opponent's hand: ", inactive)
	game.inactivePlayer.hand.append(inactive.pop(choice))

def key059(game, card):
	""" Gateway to Dis: Destroy each creature. Gain three gains.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	# active player
	while len(active) > 0:
		pendingDiscardA.append(active.pop())
	# inactive player
	while len(inactive) > 0:
		pendingDiscardI.append(inactive.pop())

	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)
	
	# add chains
	game.activePlayer.chains += 3
	
def key060(game, card):
	""" Gongoozle: Deal 3 to a creature. If it is not destroyed, its owner discards a random card from their hand.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = [] # fine b/c only ever one side
	choice, side = chooseSide(game)
	if side == 0: # friendly side
		active[choice].damageCalc(3)
		if active[choice].update():
			pendingDiscard.append(active.pop(choice))
		else:
			ran = random.choice([range(len(active))])
			pendingDiscard.append(game.activePlayer.hand.pop(ran))
		pending(game, pendingDiscard, game.activePlayer.discard)
		return
	inactive[choice].damageCalc(3)
	if inactive[choice].update():
		pendingDiscard.append(inactive.pop(choice))
	else:
		ran = random.choice([range(len(inactive))])
		pendingDiscard.append(game.inactivePlayer.hand.pop(ran))
	pending(game, pendingDiscard, game.inactivePlayer.discard)

def key061(game, card):
	""" Guilty Hearts: Destroy each creature with any amber on it.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	# active player
	length = len(active)
	[pendingDiscardA.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].captured > 0]
	# inactive player
	length = len(inactive)
	[pendingDiscardI.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].captured > 0]
	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)

def key062(game, card):
	""" Hand of Dis: Destroy a creature that is not on a flank.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = [] # fine b/c only one target
	# running a modified version of chooseSide because of the slightly different restrictions on this card
	side = ''
	if len(active) <= 2 and len(inactive) <= 2:
		print("There are no flank minions to target. The card is still played.")
		return
	elif len(inactive) <= 2:
		game.activePlayer.printShort(active, True)
		side = 0
		choice = makeChoice("There are no enemy creatures to target, so you must choose a friendly creature to target: ", active[1:-1])
	else:
		while side != "Friendly" and side != "Enemy":
			side = input("Would you like to target an [enemy] creature or a [friendly] creature?").title()
		if side == "Friendly":
			game.activePlayer.printShort(active[1:-1], True)
			side = 0
			choice = makeChoice("Choose a target: ", active[1:-1]) + 1
		elif side == "Enemy":
			game.activePlayer.printShort(inactive[1:-1], True)
			side = 1
			choice = makeChoice("Choose a target: ", inactive[1:-1]) + 1

	if side == 0: # friendly side
		pendingDiscard.append(active.pop(choice))
		pending(game, pendingDiscard, game.activePlayer.discard)
		return
	pendingDiscard.append(inactive.pop(choice))
	pending(game, pendingDiscard, game.inactivePlayer.discard)

def key063(game, card):
	""" Hecatomb: Destroy each Dis creature. Each player gains 1 amber for each creature they control that was destroyed this way.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	# active player
	length = len(active)
	[pendingDiscardA.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length+ 1)].house == "Dis"]
	count = len(pendingDiscardA)
	game.activePlayer.amber += count
	# inactive player
	length = len(inactive)
	[pendingDiscardI.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].house == "Dis"]
	count = len(pendingDiscardI)
	game.inactivePlayer.amber += count
	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)

def key064(game, card):
	""" Tendrils of Pain: Deal 1 to each creature. Deal an additional 3 to each creature if your opponent forged a key on their previous turn.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	# deal 1 damage to everything
	# active
	length = len(active)
	[x.damageCalc(1) for x in active]
	[pendingDiscardA.append(active.pop(abs(x - length + 1))) for x in active if active[abs(x - length + 1)].update()]
	# inactive
	length = len(inactive)
	[x.damageCalc(1) for x in inactive]
	[pendingDiscardI.append(inactive.pop(abs(x - length + 1))) for x in inactive if inactive[abs(x - length + 1)].update()]
	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)

	# potential extra 3 damage to everything
	if not game.forgedLastTurn[0]:
		return
	# active
	length = len(active)
	[x.damageCalc(3) for x in active]
	[pendingDiscardA.append(active.pop(abs(x - length + 1))) for x in active if active[abs(x - length + 1)].update()]
	# inactive
	length = len(inactive)
	[x.damageCalc(3) for x in inactive]
	[pendingDiscardI.append(inactive.pop(abs(x - length + 1))) for x in inactive if inactive[abs(x - length + 1)].update()]
	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)

def key065(game, card):
	""" Hysteria: Return each creature to its owner's hand.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	# active
	length = len(active)
	[game.activePlayer.hand.append(active.pop(abs(x - length + 1))) for x in range(len(active))]
	# inactive
	length = len(inactive)
	[game.inactivePlayer.hand.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive))]

def key066(game, card):
	""" Key Hammer: If your opponent forged a key on their previous turn, unforge it. Your opponent gains 6 amber.
	"""
	if game.forgedLastTurn[0]:
		game.inactivePlayer.keys -= 1
	game.inactivePlayer.amber += 6

def key067(game, card):
	""" Mind Barb: Your opponent discards a random card from their hand.
	"""
	inactive = game.inactivePlayer.hand
	ran = random.choice([range(len(inactive))])
	game.inactivePlayer.discard.append(inactive.pop(ran))
	print("your opponent discarded:\n" + repr(game.inactivePlayer.discard[-1]))

def key068(game, card):
	""" Pandemonium: Each undamaged creature captures 1 from its opponent.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]

	#active
	[x.capture(game, 1) for x in active if x.damage == 0]
	#inactive
	[x.capture(game, 1) for x in inactive if x.damage == 0]
	print(game)

def key069(game, card):
	""" Poltergeist: Use an artifact controlled by any player as if it were yours. Destroy that artifact.
	"""
	active = game.activePlayer.board["Artifact"]
	inactive = game.inactivePlayer.board["Artifact"]
	# don't need pendingDestroyed for artifacts
	choice, side = chooseSide(game, "Artifact")
	if side == 0: # friendly side
		# active[choice].action(game, card)
		game.activePlayer.discard.append(active.pop(choice))
		return
	# inactive[choice].action(game, card)
	game.inactivePlayer.discard.append(inactive.pop(choice))

def key070(game, card):
	""" Red-Hot Armor: Each enemy creature with armor loses all of its armor until the end of the turn and is dealt 1 for each point of armor it lost this way.
	"""
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = [] # fine b/c only hits one side
	length = len(inactive)
	armorList = [inactive[abs(x - length + 1)].armor for x in range(len(inactive))]
	# deal damage
	for x in range(len(inactive)):
		if armorList[x] > 0:
			inactive[abs(x - length + 1)].armor -= armorList[x]
			inactive[abs(x - length + 1)].damageCalc(armorList[x])
	# check for deaths
	[pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].update()]
	pending(game, pendingDiscard, game.inactivePlayer.discard)

def key071(game, card):
	""" Three Fates: Destroy the three most powerful creatures.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	# check # of creatures
	if len(active) + len(inactive) <= 3:
		# active
		pendingDiscardA.extend(active)
		game.activePlayer.board["Creature"] = []
		pending(game, pendingDiscardA, game.activePlayer.discard)
		# discard
		pendingDiscardI.extend(inactive)
		game.inactivePlayer.board["Creature"] = []
		pending(game, pendingDiscardI, game.inactivePlayer.discard)
		return
	# find highest power on board
	left = 3
	while left > 0:
		high = max([x.power for x in active] + [x.power for x in inactive])
		highList = []
		[highList.append(x) for x in active if x.power == high]
		[highList.append(x) for x in inactive if x.power == high]
		count = len(highList)
		if count == left: # add all to relevant discards and done
			# active
			length = len(active)
			[pendingDiscardA.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].power == high]
			pending(game, pendingDiscardA, game.activePlayer.discard)
			#inactive
			length = len(inactive)
			[pendingDiscardI.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].power == high]
			pending(game, pendingDiscardI, game.inactivePlayer.discard)
			return
		elif count < left: # add all to relevant discards and continue
			length = len(active)
			[pendingDiscardA.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].power == high]
			length = len(inactive)
			[pendingDiscardI.append(inactive.pop(abs(x - length+ 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].power == high]
			left -= count
		else: #if count > left, choose which card to discard
			print("Your minions at specified power: ")
			[print(highList.index(x) + ": " + str(x)) for x in highList if x.deck == game.activePlayer.name]
			print("Opponent minions at specified power: ")
			[print(highList.index(x) + ": " + str(x)) for x in highList if x.deck == game.inactivePlayer.name]
			choice = makeChoice("Choose which minion to destroy: ", highList)
			# active
			if highList[choice].deck == game.activePlayer.name:
				pendingDiscardA.append(active.pop(active.index(highList[choice])))
			# inactive
			else:
				pendingDiscardI.append(inactive.pop(active.index(highList[choice])))
			left -= 1
	pending(game, pendingDiscardA, game.activePlayer.discard)
	pending(game, pendingDiscardI, game.inactivePlayer.discard)

def key081(game, card):
	""" Charette: Capture 3 amber.
	"""
	card.capture(game, 3)

def key082(game, card):
	""" Drumble: if your opponent has 7 amber or more, capture all of it.
	"""
	if game.inactivePlayer.amber >= 7:
		card.capture(game, game.inactivePlayer.amber)

def key088(game, card):
	""" Guardian Demon: Heal up to 2 damage from a creature. Deal that amount of damage to another creature
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDisc = []
	# easy case: no damage
	if reduce(lambda x, y: x + y, [x.damage for x in game.activePlayer.board["Creature"]] + [x.damage for x in game.inactivePlayer.board["Creature"]]) == 0:
		print("There are no damaged creatures, so the play effect doesn't happen. The card is still played.")
		return
	print("Choose a target to heal: \n")
	choice, side = chooseSide(game)
	heal = makeChoice("How much damage would you like to heal?", [0, 1, 2])
	if heal == 0:
		return
	if side == 0: # friendly
		if 0 < active[choice].damage < heal: # aka heal == 2
			print(active[choice].title + " only has 1 damage, so you only heal one damage.")
			heal = 1
			active[choice].damage -= heal
		elif active[choice].damage >= heal: # aka heal == 2
			print(active[choice].title + " now has only " + str(active[choice].damage - heal) + " damage.\n")
			active[choice].damage -= heal
	if side == 1: #enemy
		if 0 < inactive[choice].damage < heal: # aka heal == 2
			print(inactive[choice].title + " only has 1 damage, so you only heal 1 damage.")
			heal = 1
			inactive[choice].damage -= heal
		elif inactive[choice].damage >= heal: # aka heal == 2
			print(inactive[choice].title + " now has only " + str(inactive[choice].damage - heal) + " damage.\n")
			inactive[choice].damage -= heal
	print("Now, choose which creature to transfer the damage to: ")
	choice, side = chooseSide(game)
	if side == 0: # friendly
		active[choice].damageCalc(heal)
		if active[choice].update():
			pendingDisc.append(active.pop(choice))
		pending(game, pendingDisc, game.activePlayer.discard)
	if side == 1: #enemy
		inactive[choice].damageCalc(heal)
		if inactive[choice].update():
			pendingDisc.append(inactive.pop(choice))
		pending(game, pendingDisc, game.inactivePlayer.discard)

def key094(game, card):
	""" Restringuntus: Choose a house. Your opponent cannot choose that house as their active house until Restringuntus leaves play.
	"""
	# no deck has more than one copy of this card
	game.chooseHouse(card.title)

def key096(game, card):
	""" Shooler: if your opponent has 4 or more amber, steal 1.
	"""
	if game.inactivePlayer.amber >= 4:
		stealAmber(game.activePlayer, game.inactivePlayer, 1)
	
def key101(game, card):
	""" The Terror: If your opponent has no amber, gain 2.
	"""
	if game.inactivePlayer.amber == 0:
		game.activePlayer.amber += 2

#########
# Logos #
#########

def key107(game, card):
	""" Bouncing Deathquark: Destroy and enemy creature and a friendly creature. Repeat effect as many times as you want, as long as you can repeat entire effect.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscardA = []
	pendingDiscardI = []
	print(game)
	choice = makeChoice("Choose an enemy creature to destroy: ", inactive)
	pendingDiscardI.append(inactive.pop(choice))
	if len(active) > 1:
		choice2 = makeChoice("Choose a friendly creature to destroy: ", active)
	elif len(active) == 1:
		choice2 = 0
	else:
		print("You have no creatures. The card's effect ends.")
		return
	pendingDiscardA.append(active.pop(choice2))
	pending(game, pendingDiscardI, game.inactivePlayer.discard)
	pending(game, pendingDiscardA, game.activePlayer.discard)
	while len(active) > 0 and len(inactive) > 0:
		print(game)
		choice = makeChoice("Choose an enemy creature to destroy: ")
		choice2 = makeChoice("Choose a friendly creature to destroy: ")
		pendingDiscardI.append(inactive.pop(choice))
		pendingDiscardA.append(active.pop(choice))
		pending(game, pendingDiscardI, game.inactivePlayer.discard)
		pending(game, pendingDiscardA, game.activePlayer.discard)
	if len(active) == 0:
		print("You have no more creatures, so the effect cannot be repeated.")
		return
	print("Your opponent has no more creatures, so the effect cannot be repeated.")

def key108(game, card):
	""" Dimension Door: For the remainder of the turn, any amber you would gain from reaping is stolen from your opponent instead.
	"""
	# just set a state, effect doesn't stack from multiple copies
	game.activePlayer.states["Reap"].update({card.title:True})

def key109(game, card):
	""" Effervescent Principle: Each player loses half their amber (rounding down the loss). Gain one chain.
	"""
	if game.activePlayer.amber % 2 == 0:
		game.activePlayer.amber += 1
	if game.inactivePlayer.amber % 2 == 0:
		game.inactivePlayer.amber += 1
	if game.activePlayer.amber > 0:
		game.activePlayer.amber /= 2
		print("After losing half your amber, you now have " + str(game.activePlayer.amber) + " amber.")
	else:
		print("You still have no amber.")
	if game.inactivePlayer.amber > 0:
		game.inactivePlayer.amber /= 2
		print("After losing half their amber, your opponent now has " + str(game.inactivePlayer.amber) + " amber.")
	else:
		print("Your opponent still has no amber.")
	game.activePlayer.chains += 1

def key110(game, card):
	""" Foggify: your opponent cannot use creatures to fight on their next turn.
	"""
	# states should always be in deck that they affect
	game.inactivePlayer.states["Fight"].update({card.title:True})

def key111(game, card):
	""" Help from Future Self: Search your deck and discard pile for a Timetraveller, reveal it, and put it into your hand. Shuffle your discard pile into your deck.
	"""
	# multiples of these pairings is possible, but only come in pairs
	# let's use an iterative function to search with
	def search(hand, L):
		# look at first item in deck
		x = 0
		while x < len(L):
			if L[x].title == "Timetraveller":
				hand.append(L.pop(x))
				return True
			else:
				x += 1
		return False
	
	if not search(game.activePlayer.hand, game.activePlayer.deck):
		search(game.activePlayer.hand, game.activePlayer.discard)
	game.activePlayer.shuffleDiscard()

def key112(game, card):
	""" Interdimensional Graft: If an opponent forges a key on their next turn, they must give you their remaining amber.
	"""
	# update state
	game.inactivePlayer.states["Forge"].update({card.title:True})

def key113(game, card):
	""" Knowledge is Power: Choose one: Archive a card, or, for each archived card you have, gain 1 amber.
	"""
	# b/c this is only choose card in whole set, will give card text
	while True:
		choice = input(card.text + "\n[A]rchive/[G]ain\n>>>").title()
		if len(game.activePlayer.hand) == 0 and choice[0] == "A":
			print("You have no cards in hand to archive.")
			choice = input("Would you like to gain amber instead [Y/n]? ").title()
			if choice[0] == "Y":
				choice = "G"
			else:
				return
		if "A" in choice[0]:
			archive = makeChoice("Choose a card from hand to archive: ", game.activePlayer.hand)
			game.activePlayer.archive.append(game.activePlayer.hand.pop(archive))
			print("Card archived! Type 'Archive' to view your archive.")
			return
		elif "G" in choice[0]:
			print("You gain " + str(len(game.activePlayer.archive)) + " amber.")
			game.activePlayer.amber += len(game.activePlayer.archive)
			return

def key114(game, card):
	""" Labwork: Archive a card.
	"""
	archive = makeChoice("Choose a card from hand to archive: ", game.activePlayer.hand)
	game.activePlayer.archive.append(game.activePlayer.hand.pop(archive))
	print("Card archived! Type 'Archive' to view your archive.")

def key115(game, card):
	""" Library Access: Purge this card. For the remainder of the turn, each time you play another card, draw a card.
	"""
	print(card.title + " is played, then immediately purged.")
	game.activePlayer.purge.append(game.activePlayer.board["Action"].pop()) # b/c library access will usually be only card, and if it isn't will definitely be last card
	game.activePlayer.states["Play"].update({card.title:True})

def key116(game, card):
	""" Neuro Syphon: If your opponent has more amber than you, steal 1 amber and draw a card.
	"""
	if game.inactivePlayer.amber > game.activePlayer.amber:
		print("Your opponent has more amber than you, so the effect triggers.")
		stealAmber(game.activePlayer, game.inactivePlayer, 1)
		print("You now have " + str(game.activePlayer.amber) + " amber.")
		game.activePlayer += 1
		print("Drawing a card.")
		return
	print("You have at least as much amber as your opponent. Nothing happens.")
		
def key117(game, card):
	""" Phase Shift: You may play one non-Logos card this turn.
	"""
	# this is a tough one. effect can stack, so we'll use a list
	game.activePlayer.states["Play"].update({card.title:[True]})

def key118(game, card):
	""" Positron Bolt: Deal 3 damage to a flank creature. Deal 2 damage to its neighbor. Deal 1 damage to the second creature's other neighbor.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDisc = [] # fine b/c only one side

	
	side = chooseSide(game, choices = False) # only sides w/ at least one creature can be returned from this function
	while True:
		choice = input("Choose [L]eft flank or [R]ight flank: ")
		if choice[0] == "L":
			choice = 0
			break
		elif choice[0] == "R":
			choice = 1
			break
	
	if side == 0: # friendly
		if choice != 0: choice = len(active) - 1
		active[choice].damageCalc(3)
		if choice == 0:
			try: 
				active[choice + 1].damageCalc(2)
				try: active[choice + 2].damageCalc(1)
				except: print("No second neighbor.")
			except: print("No neighbor.")
			[pendingDisc.append(active.pop(x)) for x in [choice + 2, choice + 1, choice] if active[x].update()]
		else:
			try: 
				active[choice - 1].damageCalc(2)
				try: active[choice - 2].damageCalc(1)
				except: print("No second neighbor.")
			except: print("No neighbor.")
			[pendingDisc.append(active.pop(x)) for x in [choice, choice - 1, choice - 2] if active[x].update()]
		pending(game, pendingDisc, game.activePlayer.discard)
		return
	if choice != 0: choice = len(inactive) - 1
	inactive[choice].damageCalc(3)
	if choice == 0:
		try:
			inactive[choice + 1].damageCalc(2)
			try: inactive[choice + 2].damageCalc(1)
			except: print("No second neighbor.")
		except: print("No neighbor.")
		[pendingDisc.append(inactive.pop(x)) for x in [choice + 2, choice + 1, choice] if inactive[x].update()]
	else:
		try:
			inactive[choice - 1].damageCalc(2)
			try: inactive[choice - 2].damageCalc(1)
			except: print("No second neighbor.")
		except: print("No neighbor.")
		[pendingDisc.append(inactive.pop(x)) for x in [choice, choice - 1, choice - 2] if inactive[x].update()]
	pending(game, pendingDisc, game.inactivePlayer.discard)

def key119(game, self):
	""" Random Access Archives: Archive the top card of your deck.
	"""
	# if deck is empty, don't shuffle
	if len(game.activePlayer.deck) > 0:
		game.activePlayer.archive.append(game.activePlayer.deck.pop())
		print("The top card or your deck has been archived.")
		return
	print("Your deck is empty. Nothing happenss.")

def key120(game, self):
	""" Remote Access: use an opponent's artifact as if it were yours.
	"""
	if len(game.inactivePlayer.board["Artifact"]) > 1:
		game.activePlayer.printShort(game.inactivePlayer.board["Artifact"])
		choice = makeChoice("Choose one of your opponent's artifacts to use: ", game.inactivePlayer.board["Artifact"])
		# game.inactivePlayer.board["Artifact"][choice].action(game, card) # waiting on implementation
	elif len(game.inactivePlayer.board["Artifact"]) == 1:
		pass
		# game.inactivePlayer.board["Artifact"][0].action(game, card) # waiting on implementation
	else:
		print("Your opponent has no artifacts. The card is stil played.")

def key121(game, card):
	""" Reverse Time: Swap your deck and your discard pile. Then, shuffle your deck.
	"""
	game.activePlayer.deck, game.activePlayer.discard = game.activePlayer.discard, game.activePlayer.deck
	random.shuffle(game.activePlayer.deck)

def key122(game, card):
	""" Scrambler Storm: Your opponent cannot play action cards on their next turn.
	"""
	game.inactivePlayer.states["Play"].update({card.title:True})

def key123(game, card):
	""" Sloppy Labwork: Archive a card. Discard a card.
	"""
	hand = game.activePlayer.hand
	archive = game.activePlayer.archive
	if len(hand) > 0:
		game.activePlayer.printShort(hand)
		choice = makeChoice("Choose a card to archive: ", hand)
		archive.append(hand.pop(choice))
		print("Card archived! Type 'Archive' to see your archived cards.")
	if len(hand) > 0:
		game.activePlayer.printShort(hand)
		choice = makeChoice("Choose a card to discard: ", hand)
		game.activePlayer.discard.append(hand.pop(choice))
		print("Card discarded!")

def key124(game, card):
	""" Twin Bolt Emission: Deal 2 damage to a creature and deal 2 damage to a different creature.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscA = []
	pendingDiscI = []

	left = 2
	while left > 0:
		print("Choose a target to deal 2 damage to:")
		choice, side = chooseSide(game)
		if side == 0: # friendly
			active[choice].damageCalc(2)
			if active[choice].update:
				pendingDiscA.append(active.pop(choice))
			left -= 1
		elif side == 1: #enemy
			inactive[choice].damageCalc(2)
			if active[choice].update:
				pendingDiscI.append(active.pop(choice))
			left -= 1
		else:
			return
	pending(game, pendingDiscA, game.activePlayer.discard)
	pending(game, pendingDiscI, game.inactivePlayer.discard)

def key125(game, card):
	""" Wild Wormhole: Play the top card of your deck.
	"""
	game.playCard(100, False)

def key138(game, card):
	""" Dextre: Capture 1 amber.
	"""
	card.capture(game, 1)
	print("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def key140(game, card):
	""" Dr. Escotera: Gain 1 amber for each key your opponent has.
	"""
	
	game.activePlayer.amber += game.inactivePlayer.keys
	print("You now have " + str(game.activePlayer.amber) + " amber")

def key141(game, card):
	""" Dysania: Your opponent discards each of their archived cards. You gain 1 amber for each card discarded this way.
	"""
	
	if len(game.inactivePlayer.archive) > 0:
		game.activePlayer.amber += len(game.inactivePlayer.archive)
		print("You gained " + str(len(game.inactivePlayer.archive)) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
		pendingDisc = game.inactivePlayer.archive
		game.inactivePlayer.archive = []
		pending(game, pendingDisc, game.inactivePlayer.discard)

def key143(game, card):
	""" Harland Mindlock: Take control of an enemy flank creature until Harland Mindlock leaves play.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]

	
	while True:
		choice = input("Choose [L]eft flank or [R]ight flank enemy creature to target: ")
		if choice[0] == "L":
			choice = 0
			break
		elif choice[0] == "R":
			choice = len(inactive) - 1
			break

	while True:
		flank = input("Choose [L]eft flank or [R]ight flank to put stolen creature: ")
		if choice[0] == "L":
			flank = 0
			break
		elif choice[0] == "R":
			flank = len(active)
			break

	active.insert(flank, inactive.pop(choice))

def key146(game, card):
	""" Neutron Shark: Destroy an enemy creature or artifact and a friendly creature or artifact. Discard the top card of your deck. If that card is not a Logos card, trigger this effect again.
	"""
	active = game.activePlayer.board
	inactive = game.inactivePlayer.board
	pendingDiscard = []

	print(game)
	logos = True
	while logos:
		while True:
			if len(inactive["Creature"]) + len(inactive["Artifact"]) == 0:
				print("Your opponent has nothing for you to target. The effect still continues.")
				choice = "extra"
			elif len(inactive["Creature"]) == 0:
				print("Your opponent has no creatures to destroy, so you must target an artifact.")
				choice = "Artifact"
			elif len(inactive["Artifact"]) == 0:
				print("Your opponent has no artifacts to destroy, so you must target a creature.")
				choice = "Creature"
			else:
				choice = input("Target enemy [C]reature or enemy [A]rtifact?\n>>>")
				if choice[0] == "C":
					choice = "Creature"
					break
				elif choice[0] == "A":
					choice = "Artifact"
					break
		if choice != "extra":
			game.activePlayer.printShort(inactive[choice])
			choice2 = makeChoice("Choose a target: ", inactive[choice])
			pendingDiscard.append(inactive[choice].pop(choice2))
			pending(game, pendingDiscard, game.inactivePlayer.discard)
		while True:
			if len(active["Creature"]) + len(active["Artifact"]) == 0:
				print("You have nothing to target. The effect still continues.")
				choice = "extra"
			elif len(active["Creature"]) == 0:
				print("You have no creatures to destroy, so you must target an artifact.")
				choice = "Artifact"
			elif len(active["Artifact"]) == 0:
				print("You have no artifacts to destroy, so you must target a creature.")
				choice = "Creature"
			else:
				choice = input("Target friendly [C]reature or friendly [A]rtifact?\n>>>")
				if choice[0] == "C":
					choice = "Creature"
					break
				elif choice[0] == "A":
					choice = "Artifact"
					break
		if choice != "extra":
			game.activePlayer.printShort(active[choice])
			choice2 = makeChoice("Choose a target: ", active[choice])
			pendingDiscard.append(active[choice].pop(choice2))
			pending(game, pendingDiscard, game.activePlayer.discard)

		game.activePlayer.discard.append(game.activePlayer.deck.pop())
		if game.activePlayer.discard[-1].house == "Logos":
			logos = False
		
def key149(game, card):
	""" Psychic Bug: Look at your opponent's hand.
	"""
	
	inhand = game.inactivePlayer.hand

	game.activePlayer.printShort(inhand)

def key152(game, card):
	""" Skippy Timehog: Your opponent canot use any cards next turn.
	"""
	
	game.inactivePlayer.states["Reap"].update({card.title:True})
	game.inactivePlayer.states["Fight"].update({card.title:True})
	game.inactivePlayer.states["Action"].update({card.title:True})

def key153(game, card):
	""" Timetraveller: Draw two cards.
	"""
	
	game.activePlayer += 2

def key157(game, card):
	""" Experimental Therapy: Stun and exhaust this creature.
	"""
	card.stun = True
	card.ready = False

########
# Mars #
########

def reveal(game, L):
	""" A function to handle the Mars card revealing feature. Returns a list of revealed cards.
	"""
	hand = [x for x in L if x.house == "Mars"]
	if len(hand) > 0:
		original = len(hand)
	else:
		print("You have no Mars cards in your hand.")
		return
	reveal = []
	print("The Mars cards in your hand are: ")
	game.activePlayer.printShort(hand)
	while len(reveal) < original:
		choice = makeChoice("Choose a card to reveal: ", hand)
		reveal.append(hand.pop(choice))
		again = input("Would you like to reveal another card [Y/n]?").title()
		if again[0] == "N":
			break
	return reveal

def key160(game, card):
	""" Ammonia Clouds: Deal 3 damage to each creature.
	"""
	
	active = game.activePlayer.board["Creature"]
	inactive = game.activePlayer.board["Creature"]
	pendingDiscA = []
	pendingDiscI = []
	
	[x.damageCalc(3) for x in active]
	[x.damageCalc(3) for x in inactive]
	length = len(active)
	[pendingDiscA.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].update()]
	length = len(inactive)
	[pendingDiscI.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].update()]
	pending(game, pendingDiscA, game.activePlayer.discard)
	pending(game, pendingDiscI, game.inactivePlayer.discard)

def key161(game, card):
	""" Battle Fleet: Reveal any number of Mars cards from your hand. For each card revealed this way, draw 1 card.
	"""
	
	revealed = reveal(game, game.activePlayer.hand)
	game.activePlayer.printShort(revealed)
	game.activePlayer += len(revealed)
	print("You drew " + str(len(revealed)) + " cards.")

def key162(game, card):
	""" Deep Probe: Choose a house: Reveal your opponent's hand. Discard each creature of that house revealed this way.
	"""
	
	discard = []
	house = ''
	while house == '':
		house = input("Choose a house: ").title()
		if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]: break
		else: house = ''
	length = len(game.inactivePlayer.hand)
	[discard.append(game.inactivePlayer.hand.pop(abs(x - length + 1))) for x in len(game.inactivePlayer.hand) if game.inactivePlayer.hand[abs(x - length + 1)].house == house and game.inactivePlayer.hand[abs(x - length + 1)].type == "Creature"]
	print("Your opponent discarded:")
	game.activePlayer.printShort(discard)

def key163(game, card):
	""" EMP Blast: Each Mars creature and each Robot creature is stunned. Each artifact is destroyed.
	"""
	
	activeC = game.activePlayer.board["Creature"]
	activeA = game.activePlayer.board["Artifact"]
	inactiveC = game.inactivePlayer.board["Creature"]
	inactiveA = game.inactivePlayer.board["Artifact"]
	
	for x in [x for x in (activeC + inactiveC) if x.house == "Mars" or "Robot" in x.traitList]:
		x.stun = True
	pendingDiscard = activeA # fine because Artifacts don't have destroyed effects
	pending(game, pendingDiscard, game.activePlayer.discard)
	pendingDiscard = inactiveA
	pending(game, pendingDiscard, game.inactivePlayer.discard)
	print(game)

def key164(game, card):
	""" Hypnotic Command: For each friendly Mars creature, choose an enemy creature to capture one from their own side.
	"""
	
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]

	count = 0
	for x in active:
		if x.house == "Mars" and x.type == "Creature": # second part of if is for redundancy
			count += 1
	print("You have " + str(count) + " Mars creatures.")
	while count > 0:
		choice = makeChoice("Choose an enemy creature to capture one amber from their own side: ", inactive)
		# looks like they can choose the same minion each time
		inactive[choice].capture(game, 1, True)
		count -= 1
	print("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")
	
def key165(game, card):
	""" Irradiated Amber: If your opponent has 6 or more amber, deal 3 damage to each enemy creature.
	"""
	
	inactive = game.inactivePlayer.board["Creature"]
	pendingDisc = [] # fine because only one side

	if game.inactivePlayer.amber >= 6:
		length = len(inactive)
		[x.damageCalc(3) for x in inactive]
		[pendingDisc.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].update()]

def key166(game, card):
	""" Key Abduction: Return each Mars creature to its owner's hand. Then you may forge a key at +9 current cost, reduced by 1 for each card in your hand.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	length = len(active)
	[game.activePlayer.hand.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].house == "Mars" and active[abs(x - length + 1)].type == "Creature"]
	length = len(inactive)
	[game.inactivePlayer.hand.append(inactive.pop(abs(x - length+ 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].house == "Mars" and inactive[abs(x - length + 1)].type == "Creature"]
	if game.activePlayer.amber >= (game.activePlayer.keyCost + 9 - len(game.activePlayer.hand)):
		print("You may now forge a key for " + str(game.activePlayer.keyCost + 9 - len(game.activePlayer.hand)) + " amber.")
		forge = input("Would you like so to do [Y/n]? ").title()
		if forge[0] == "N":
			print("You have chosen not to forge a key.")
			return
		print("Forging key!")
		game.activePlayer.amber -= (game.activePlayer.keyCost + 9 - len(game.activePlayer.hand))
		game.activePlayer.keys += 1
		if game.activePlayer.keys == 3:
			game.endBool = False # This will make the game end.
			return
		print("You now have " + game.activePlayer.amber + " amber.")

def key167(game, card):
	""" Martian Hounds: Choose a creature. For each damaged creature, give the chosen creature two +1 power counters.
	"""
	
	count = 0
	for x in (game.activePlayer.board["Creature"] + game.activePlayer.board["Creature"]):
		if x.damage > 0:
			count += 1
	choice, side = chooseSide(game)
	if count == 0:
		print("There are no damaged creatures, so no power will be gained. The card is still played.")
		return
	if side == 0: # friendly
		choice = game.activePlayer.board["Creature"][choice]
		choice.extraPow += (2 * count)
		print(choice.title + " now has " + str(choice.power + choice.extraPow) + " power.")
		return
	choice = game.inactivePlayer.board["Creature"][choice]
	choice.extraPow += (2 * count)
	print(choice.title + " now has " + str(choice.power + choice.extraPow) + " power.")

def key168(game, card):
	""" Martians Make Bad Allies: Reveal your hand. Purge each revealed non-Mars creature and gain 1 amber for each card purged this way.
	"""
	
	active = game.activePlayer.hand
	game.activePlayer.printShort(active)
	length = len(active)
	count = 0 
	for x in range(len(active)):
		if active[abs(x - length + 1)].house != "Mars" and active[abs(x - length + 1)].type == "Creature":
			count += 1
			print("Purging " + active[abs(x - length + 1)].title + ".")
			game.activePlayer.purge.append(active.pop(abs(x - length + 1)))
	if count > 0:
		game.activePlayer.amber += count
		print("You gained " + str(count) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
		return
	print("You had no creatures in hand. You gain no amber. The card is still played.")

def key169(game, card):
	""" Mass Abduction: Put up to 3 damaged enemy creatures into your archives. If any of these creatures leave your archives, they are put into their owner's hand instead.
	"""
	
	inactive = game.inactivePlayer.board["Creature"]
	count = len([x for x in inactive if x.damage > 0])
	if count == 0:
		print("There are no damaged enemy creatures. The card is still played.")
	else:
		while count > 0:
			[print(x + ": " + str(x)) for x in range(len(inactive))]
			choice = makeChoice("Choose a damaged enemy creature to target: ")
			if inactive[choice].damage > 0:
				game.activePlayer.archive.append(inactive.pop(choice))
				count -= 1
			else:
				print("You can only target damaged creatures.")
			if count > 0:
				again = input("Would you like to archive another enemy creature [Y/n]?\n>>>").title()
				if again[0] == "N":
					return

def key170(game, card):
	""" Mating Season: Shuffle each Mars creature into its owner's deck. Each player gains 1 amber for each creature shuffled into their deck this way.
	"""
	actDeck = game.activePlayer.deck
	inactDeck = game.inactivePlayer.deck
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	
	if "Mars" in [x.house for x in active]:
		length = len(active)
		[actDeck.append(active.pop(absa(x, length))) for x in range(len(active)) if active[absa(x, length)].house == "Mars"]
		random.shuffle(actDeck)
		game.activePlayer.amber += (length - len(active))
		return
	print("You have no Mars creatures, so you gain no amber.")
	if "Mars" in [x.house for x in inactive]:
		length = len(inactive)
		[inactDeck.append(inactive.pop(absa(x, length))) for x in range(len(inactive)) if inactive[absa(x, length)].house == "Mars"]
		random.shuffle(inactDeck)
		game.inactivePlayer.amber += (length - len(inactive))
		return
	print("Your opponent has no Mars creatures, so they gain no amber.")

def key171(game, card):
	""" Mothership Support: For each friendly ready Mars creature, deal 2 damage to a creature. (You may choose a different creature each time.)
	"""
	
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDisc = [] # fine because one target at a time
	count = 0
	for x in range(len(active)):
		if x.house == "Mars" and x.ready == True:
			count += 1
	if count == 0:
		print("You have no Mars creatures, so no damage is dealt. The card is still played.")
		return
	while count > 0:
		choice, side = chooseSide(game)
		if side == 0: # friendly
			active[choice].damageCalc(2)
			if active[choice].update():
				pendingDisc.append(active.pop(choice))
				pending(game, pendingDisc, game.activePlayer.discard)
				count -= 1
				continue
		if side == 1: # enemy
			inactive[choice].damageCalc(2)
			if active[choice].update():
				pendingDisc.append(active.pop(choice))
				pending(game, pendingDisc, game.activePlayer.discard)
				count -= 1
				continue
		if side == '':
			break # side will tell them that they are no more targets

def key172(game, card):
	""" Orbital Bombardment: Reveal any number of Mars cards from your hand. For each card revealed this way, deal 2 damage to a creature. (you may choose a different creature each time.)
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDisc = [] # fine because only one side
	revealed = reveal(game, game.activePlayer.hand)
	count = len(revealed)
	if count == 0:
		print("You have no Mars creatures, so no damage is dealt. The card is still played.")
		return
	while count > 0:
		choice, side = chooseSide(game)
		if side == 0: # friendly
			active[choice].damageCalc(2)
			if active[choice].update():
				pendingDisc.append(active.pop(choice))
				pending(game, pendingDisc, game.activePlayer.discard)
				count -= 1
				continue
		if side == 1: # enemy
			inactive[choice].damageCalc(2)
			if active[choice].update():
				pendingDisc.append(active.pop(choice))
				pending(game, pendingDisc, game.activePlayer.discard)
				count -= 1
				continue
		if side == '':
			break # side will tell them that they are no more targets
	
def key173(game, card):
	""" Phosphorous Stars: Stun each non-Mars creature. Gain 2 chains.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]

	for x in (active + inactive):
		if x.house != "Mars":
			x.stun = True

	game.activePlayer.chains += 2

def key174(game, card):
	""" Psychic Network: Steal 1 amber for each friendly ready Mars creature.
	"""
	active = game.activePlayer.board["Creature"]
	count = 0
	for x in active:
		if x.house == "Mars" and x.ready == True:
			count += 1
	if count == 0:
		print("You have no friendly ready Mars creatures, so you don't steal any amber. The card is still played.")
		return
	stealAmber(game.activePlayer, game.inactivePlayer, count)

def key175(game, card):
	""" Sample Collection: Put an enemy creature into your archives for each key your opponent has forged. If any of these creatures leave your archives, they are put into their owner's hand instead.
	"""
	count = game.inactivePlayer.keys
	inactive = game.inactivePlayer.board["Creature"]
	archive = game.activePlayer.archive
	if count == 0:
		print("Your opponent has forged no keys, so you archive no enemy creatures. The card is still played.")
		return
	while count > 0 and len(inactive) > 0:
		[print(str(x) + ": " + str(inactive[x])) for x in range(len(inactive))]
		choice = makeChoice("Choose an enemy creature to archive: ", inactive)
		archive.append(inactive.pop(choice))

def key176(game, choice):
	""" Shatter Storm: Lose all your amber. Then, your opponent loses triple the amount of amber you lost this way.
	"""
	count = game.activePlayer.amber
	if count == 0:
		print("You have no amber to lose, so your opponent loses no amber. The card is still played.")
		return
	game.activePlayer.amber -= count
	game.inactivePlayer.amber -= (count * 3)
	if game.inactivePlayer.amber < 0:
		game.inactivePlayer.amber = 0

def key177(game, choice):
	""" Soft Landing: The next creature or artifact you play this turn enters play ready.
	"""
	game.activePlayer.states["Play"].update({"Soft Landing":True})

def key178(game, choice):
	""" Squawker: Ready a Mars creature or stun a non-Mars creature.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	choice, side = chooseSide(game)
	if side == 0: # friendly
		if active[choice].house == "Mars":
			active[choice].ready = True
			print(active[choice].title + " is now ready!")
		else:
			active[choice].stun = True
			print(active[choice].title + " is now stunned!")
		return
	if side == 1: # friendly
		if inactive[choice].house == "Mars":
			inactive[choice].ready = True
			print(active[choice].title + " is now ready!")
		else:
			inactive[choice].stun = True
			print(inactive[choice].title + " is now stunned!")
		return
	return # because chooseSide will tell them about the empty board

def key179(game, card):
	""" Total Recall: For each friendly ready creature, gain 1 amber. Return each friendly creature to your hand.
	"""
	active = game.activePlayer.board["Creature"]
	pendingHand = []
	count = 0
	if len(active) == 0:
		print("You have no friendly creatures, so nothing happens. The card is still played.")
		return
	for x in active:
		if x.ready == True:
			count += 1
	if count == 0:
		print("You have no ready creatures, so you gain no amber.")
	pendingHand.extend(active)
	active = []
	pending(game, pendingHand, game.activePlayer.hand, ask = False)

def key203(game, card):
	""" Yxili Marauder: Capture 1 amber for each friendly ready Mars creature.
	"""
	active = game.activePlayer.board["Creature"]
	count = 0
	for x in active:
		if x.ready == True and x.house == "Mars":
			count += 1
	if count == 0:
		print("You have no friendly ready Mars creatures. " + card.title + " captures no amber.")
		return
	while count > 0 and game.inactivePlayer.amber > 0:
		card.capture(1)
		count -= 1
	print("Yxili Marauder captured " + str(card.captured) + " amber.")
	card.extraPow = card.captured


###########
# Sanctum #
###########


def key212(game, card):
	""" Begone!: Choose one: destroy each Dis creature, or gain 1 amber.
	"""
	while True:
		choice = input("Would you like to [D]estroy each Dis creature, or [G]ain 1 amber?").title()
		if choice[0] == "D":
			active = game.activePlayer.board["Creature"]
			inactive = game.inactivePlayer.board["Creature"]
			pendingA = []
			pendingI = []
			length = len(active)
			[pendingA.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].house == "Dis"]
			length = len(inactive)
			[pendingA.append(inactive.pop(absa(x, length))) for x in range(length) if inactive[absa(x, length)].house == "Dis"]
			pending(game, pendingA, game.activePlayer.discard)
			pending(game, pendingI, game.inactivePlayer.discard)
			return
		if choice[0] == "G":
			game.activePlayer.amber += 1
			print("You now have " + str(game.activePlayer.amber) + " amber.")
			return
		print("Not a valid input. Try again.")

def key213(game, card):
	""" Blinding Light: Choose a house. Stun each creature of that house.
	"""
	while True:
		house = input("Choose a house. For handy reference, your opponent's houses are " + game.inactivePlayer.houses[0] + ", " + game.inactivePlayer.houses[1] + ", and " + game.inactivePlayer.houses[2] + ".\n>>>").title()
		if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]: break
		print("Not a valid input. Try again.")
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	count = 0
	for x in (active + inactive):
		if x.house == house:
			x.stun = True
			count += 1
	print("You stunned " + str(count) + " minions.")

def key214(game, card):
	""" Charge!: For the remainder of the turn, each creature you play gains, "Play: Deal 2 to an enemy creature."
	"""
	game.activePlayer.states["Play"].update({card.title:True})

def key215(game, card):
	""" Cleansing Wave: Heal 1 damage from each creature. Gain 1 amber for each creature healed this way.
	"""
	inactive = game.inactivePlayer.board["Creature"]
	active = game.activePlayer.board["Creature"]
	count = 0
	for x in (active + inactive):
		if x.damage > 0:
			x.damage -= 1
			count += 1
	print("You healed " + str(count) + " damage. You gain that much amber.")

def key216(game, card):
	""" Clear Mind: Unstun each friendly creature.
	"""
	active = game.activePlayer.board["Creature"]
	for x in active:
		if x.stun == True:
			print(x.title + " is no longer stunned.")
			x.stun = False

def key217(game, card):
	""" Doorstep to Heaven: Each player with 6 or more amber is reduced to five amber.
	"""
	if game.activePlayer.amber >= 6:
		game.activePlayer.amber = 5
	if game.inactivePlayer.amber >= 6:
		game.inactivePlayer.amber = 5

def key218(game, card):
	""" Glorious Few: For each creature your opponent controls in excess of you, gain 1 amber.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	if len(inactive) > len(active):
		game.activePlayer.amber += (len(inactive) - len(active))
		print("You gained " + str(len(inactive) - len(active)) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
		return
	print("Your opponent does not have more creatures than you, so you gain no amber. The card is still played.")

def key219(game, card):
	""" Honorable Claim: Each friendly knight creature captures 1.
	"""
	active = game.activePlayer.board["Creature"]
	count = 0
	knights = []
	for x in active:
		if "Knight" in x.traitList:
			count += 1
			knights.append(x)
	if count > game.inactivePlayer.amber and game.inactivePlayer.amber > 0:
		print("You have more knights than your opponent has amber.")
		while game.inactivePlayer.amber > 0:
			choice = makeChoice("Choose a knight to capture 1 amber: ", knights)
			knights[choice].capture(1)
			knights.pop(choice)
		print("You captured all of your opponent's amber.")
		return
	if count < game.inactivePlayer.amber:
		[x.capture(1) for x in knights]
		return
	print("Your opponent has no amber to capture.")

def key220(game, card):
	""" Inspiration: Ready and use a friendly creature.
	"""
	active = game.activePlayer.board["Creature"]
	choice = makeChoice("Choose a friendly creature to ready and use: ", active)
	active[choice].ready = True
	uses =  ["Reap", "Fight"]
	if active[choice].action: uses.append("Action")
	while True:
		use = input("How would you like to use this creature? Your options are " + str(uses) + "\n>>>").title()
		if use in uses:
			break
	if use[0] == "R":
		if game.checkReapStates:
			active[choice].reap(game, active[choice])
		return
	if use[0] == "F":
		if game.checkFightStates:
			game.fightCard(choice)
		return
	if use[0] == "A":
		if game.checkActionStates:
			active[choice].action(game, active[choice])


if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')