import time
import random
from functools import reduce
# I think it makes more sense to add these to the cardsAsClass file, which means that the only function here is addToBoard

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

def backwardsList(input_L, actionstring, compstring, result_L = []):
	""" A list comprehension that goes through a list backwards. Action is a string which goes before the "for", compstring after the "if".
	"""
	[eval(actionstring) for x in range(len(input_L)) if eval(compstring)]
	# not sure if this needs a return

def makeChoice(stringy, L = []):
	""" Takes a string explaining the choice and a list, only accepts results within the length of the list, unless the list is empty, then it just returns the number.
	"""
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

def pending(game, L, destination):
	""" A function that deals with pending piles of cards.
	Arguments: game should be self-evident, it's needed to be able to modify the game, L is the list being emptied, and destination is the list being appended to.
	"""
	if L == []:
		return
	if (destination == game.activePlayer.discard or destination == game.inactivePlayer.discard) and ("Annihilation Ritual" in [x.title for x in game.activePlayer.board["Artifact"]] or "Annihilation Ritual" in [x.title for x in game.inactivePlayer.board["Artifact"]]):
		if destination == game.activePlayer.discard:
			destination = game.activePlayer.purge
		else: # because destination has to be one or the other for this to pass, we don't need to explicitly state the second
			destination = game.inactivePlayer.purge
	final = len(L) + len(destination)
	game.activePlayer.printShort(L, False)
	while len(L) > 1:
		choice = makeChoice("Choose which card to add to the top of your deck next: ", L)
		destination.append(L.pop(choice))
	destination.append(L.pop())
	if len(L) > 0:
		raise ValueError("card.pending did not properly empty the list.")
	if len(destination) != final:
		raise ValueError("card.pending did not extend the destination the correct length")

def chooseSide(game, stringy = "Creature"):
	""" A return of 0 is friendly, 1 is enemy. Strings can make it deal with different lists.
	"""
	activeBoard = game.activePlayer.board[stringy]
	inactiveBoard = game.inactivePlayer.board[stringy]
	
	side = ''
	if len(inactiveBoard) == 0 and len(activeBoard) == 0:
		print("There are no " + stringy.lower() + "s to target. The card is still played.")
	elif len(inactiveBoard) == 0:
		game.activePlayer.printShort(activeBoard, True)
		side = 0
		choice = makeChoice("There are no enemy " + stringy.lower() + "s to target, so you must choose a friendly " + stringy.lower() + " to target: ", activeBoard)
	else:
		while side != "Friendly" and side != "Enemy":
			side = input("Would you like to target an [enemy] " + stringy.lower() + " or a [friendly] " + stringy.lower() + "?").title()
		if side == "Friendly":
			game.activePlayer.printShort(activeBoard, True)
			side = 0
			choice = makeChoice("Choose a target: ", activeBoard)
		elif side == "Enemy":
			game.activePlayer.printShort(inactiveBoard, True)
			side = 1
			choice = makeChoice("Choose a target: ", inactiveBoard)
	return choice, side

def stealAmber(thief, victim, num):
	if victim.amber >= num:
		victim.amber -= num
		thief.amber += num
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

	pendingDiscard = []	
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
	pendingDiscard = []

	# active player
	damageList = [x.damage for x in activeBoard if x.damage > 0]
	# easy case: everything damaged
	if len(damageList) == len(activeBoard): pendingDiscard = activeBoard
	else:
		backwardsList(activeBoard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[(x - len(input_L) + 1)].damage > 0", pendingDiscard)
		# [pendingDiscard.append(activeBoard.pop(abs(x - len(activeBoard) + 1))) for x in range(len(activeBoard)) if activeBoard[(x - len(activeBoard) + 1)].damage > 0]
		# for x in range(len(activeBoard)):
			# so that i can work from right to left
			# x = abs(x - len(activeBoard) + 1)
			# if activeBoard[x].damage > 0:
			# 	pendingDiscard.append(activeBoard.pop(x))

	pending(game, pendingDiscard, game.activePlayer.discard)

	# inactive player
	damageList = [x.damage for x in inactiveBoard if x.damage > 0]
	# easy case: everything damaged
	if len(damageList) == len(inactiveBoard): pendingDiscard = inactiveBoard
	else:
		backwardsList(inactiveBoard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[(x - len(input_L) + 1)].damage > 0", pendingDiscard)
		# [pendingDiscard.append(inactiveBoard.pop(abs(x - len(inactiveBoard) + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[(x - len(inactiveBoard) + 1)].damage > 0]
		# for x in range(len(inactiveBoard)):
		# 	# so that i can work from right to left
		# 	x = abs(x - len(inactiveBoard) + 1)
		# 	if inactiveBoard[x].damage > 0:
		# 		pendingDiscard.append(inactiveBoard.pop(x))

	pending(game, pendingDiscard, game.inactivePlayer.discard)
	
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
	pendingDiscard = []

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
	game.activePlayer.states["Destroyed"].update({"Loot the Bodies": True})
	# skipping the rest for now, until event emitters or etc are figured out

def key011 (game, card):
	"""Take that, Smartypants: Steal 2 amber if your opponent has 3 or more Logos cards in play.
	"""
	inactiveBoard = game.inactivePlayer.board
	count = 0
	[count.__add__(1) for x in [inactiveBoard["Creature"] + inactiveBoard["Artifact"]] if x.house == "Logos"]
	if count >= 3:
		stealAmber(game.activePlayer, game.inactivePlayer, 2)
	else:
		print("Your opponent had less than 3 Logos cards in play, so you didn't steal anything. The card is still played.")


def key012 (game, card):
	""" Punch: Deal 3 damage to a creature.
	"""
	activeBoard = game.activePlayer.board["Creature"]
	inactiveBoard = game.inactivePlayer.board["Creature"]
	pendingDiscard = []

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
	game.activePlayer.states["Fight"].update({"Warsong":True})
	# needs to be able to account for multiple instances of warsong

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
	pendingDiscard = []

	# active board: LC
	backwardsList(activeBoard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1].power <= 3", pendingDiscard)
	pending(game, pendingDiscard, game.activePlayer.discard)
	# then inactive
	backwardsList(inactiveBoard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1].power <= 3", pendingDiscard)
	pending(game, pendingDiscard, game.inactivePlayer.discard)

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
	pendingDiscard = []

	[x.damageCalc(2) for x in activeBoard if x.damage == 0 and activeBoard.index(x) != activeBoard.index(card)]
	backwardsList(activeBoard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].update()", pendingDiscard)
	[x.damageCalc(2) for x in inactiveBoard if x.damage == 0]
	backwardsList(inactiveBoard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].update()", pendingDiscard)

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
	backwardsList(game.activePlayer.board["Creature"], "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].house == 'Brobnar' and abs(x - len(input_L) + 1) != " + str(index), game.activePlayer.hand)

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
		[(count.__add__(1)) for x in game.inactivePlayer.hand if x.house == house]
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
		[(count.__add__(1)) for x in game.activePlayer.hand if x.house == house]
		print("You have " + str(count) + " cards in your hand of the same house as the discarded card. Your opponent gains that much amber.")
	else:
		print("You have no cards to discard, so your opponent gains no amber. The card is still played.")
	game.inactivePlayer.amber += count

def key054(game, card):
	"""Arise!: Choose a house. Return each creature of that house from your discard pile to your hand.
	"""
	house = ''
	while house == '':
		house = input("Choose a house: ").title()
		if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]: break
		else: house = ''
	backwardsList(game.activePlayer.discard, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].house == " + house, game.activePlayer.hand)
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
	backwardsList(active, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].power == " + str(choice), pendingDestroyed)
	pending(game, pendingDestroyed, game.activePlayer.discard)
	#inactive player
	backwardsList(inactive, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].power == " + str(choice), pendingDestroyed)
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
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = []
	# active player
	while len(active) > 0:
		pendingDiscard.append(active.pop())
	pending(game, pendingDiscard, game.activePlayer.discard)
	# inactive player
	while len(inactive) > 0:
		pendingDiscard.append(inactive.pop())
	pending(game, pendingDiscard, game.inactivePlayer.discard)
	# add chains
	game.activePlayer.chains += 3
	
def key060(game, card):
	""" Gongoozle: Deal 3 to a creature. If it is not destroyed, its owner discards a random card from their hand.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = []
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
	pendingDiscard = []
	# active player
	backwardsList(active, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].captured > 0", pendingDiscard)
	pending(game, pendingDiscard, game.activePlayer.discard)
	# inactive player
	backwardsList(inactive, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].captured > 0", pendingDiscard)
	pending(game, pendingDiscard, game.inactivePlayer.discard)

def key062(game, card):
	""" Hand of Dis: Destroy a creature that is not on a flank.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = []
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
	pendingDiscard = []
	# active player
	backwardsList(active, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].house == 'Dis'", pendingDiscard)
	count = len(pendingDiscard)
	game.activePlayer.amber += count
	pending(game, pendingDiscard, game.activePlayer.discard)
	# inactive player
	backwardsList(inactive, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L) + 1)].house == 'Dis'", pendingDiscard)
	count = len(pendingDiscard)
	game.inactivePlayer.amber += count
	pending(game, pendingDiscard, game.inactivePlayer.discard)

def key064(game, card):
	""" Tendrils of Pain: Deal 1 to each creature. Deal an additional 3 to each creature if your opponent forged a key on their previous turn.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingDiscard = []
	# deal 1 damage to everything
	# active
	[x.damageCalc(1) for x in active]
	[pendingDiscard.append(active.pop(abs(x - len(active) + 1))) for x in active if x.update()]
	pending(game, pendingDiscard, game.activePlayer.discard)
	# inactive
	[x.damageCalc(1) for x in inactive]
	[pendingDiscard.append(inactive.pop(abs(x - len(inactive) + 1))) for x in inactive if x.update()]
	pending(game, pendingDiscard, game.inactivePlayer.discard)

	# potential extra 3 damage to everything
	if not game.forgedLastTurn[0]:
		return
	# active
	[x.damageCalc(3) for x in active]
	[pendingDiscard.append(active.pop(abs(x - len(active) + 1))) for x in active if x.update()]
	pending(game, pendingDiscard, game.activePlayer.discard)
	# inactive
	[x.damageCalc(3) for x in inactive]
	[pendingDiscard.append(inactive.pop(abs(x - len(inactive) + 1))) for x in inactive if x.update()]
	pending(game, pendingDiscard, game.inactivePlayer.discard)

def key065(game, card):
	""" Hysteria: Return each creature to its owner's hand.
	"""
	active = game.activePlayer.board["Creature"]
	inactive = game.inactivePlayer.board["Creature"]
	pendingHand = []
	# active
	backwardsList(active, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "1 > 0", pendingHand)
	pending(game, pendingHand, game.activePlayer.hand)
	# inactive
	backwardsList(inactive, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "1 > 0", pendingHand)
	pending(game, pendingHand, game.inactivePlayer.hand)

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
	pendingDiscard = []
	armorList = [inactive[abs(x - len(inactive) + 1)].armor for x in range(len(inactive))]
	[(inactive[abs(x - len(inactive) + 1)].armor.__sub__(armorList[x]), inactive[abs(x - len(inactive) + 1)].damageCalc(armorList[x])) for x in range(len(inactive)) if armorList[x] > 0]
	backwardsList(inactive, "result_L", "input_L[abs(x- len(input_L) + 1)].update()", pendingDiscard)
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
			backwardsList(active, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L))].power == " + str(high), pendingDiscardA)
			pending(game, pendingDiscardA, game.activePlayer.discard)
			backwardsList(inactive, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L))].power == " + str(high), pendingDiscardI)
			pending(game, pendingDiscardI, game.inactivePlayer.discard)
			return
		elif count < left: # add all to relevant discards and continue
			backwardsList(active, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L))].power == " + str(high), pendingDiscardA)
			backwardsList(inactive, "result_L.append(input_L.pop(abs(x - len(input_L) + 1)))", "input_L[abs(x - len(input_L))].power == " + str(high), pendingDiscardI)
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
			pendingDisc.append(active[choice])
		pending(game, pendingDisc, game.activePlayer.discard)
	if side == 1: #enemy
		inactive[choice].damageCalc(heal)
		if inactive[choice].update():
			pendingDisc.append(inactive[choice])
		pending(game, pendingDisc, game.inactivePlayer.discard)

def key094(game, card):
	

		

	


if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')