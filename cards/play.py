import cards.board as board
import cards.cardsAsClass as x
# I think it makes more sense to add these to the cardsAsClass file, which means that the only function here is addToBoard

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

def pending(game, L, destination):
	""" A function that deals with pending piles of cards.
	Arguments: game should be self-evident, it's needed to be able to modify the game, L is the list being emptied, and destination is the list being appended to.
	"""
	final = len(L) + len(destination)
	game.activePlayer.printShort(L, False)
	while len(L) > 1:
		while True:
			try:
				choice = int(input("Choose which card to add to your deck: "))
				break
			except:
				pass
		destination.append(L.pop(choice))
	destination.append(L.pop())
	if len(L) > 0:
		raise ValueError("card.pending did not properly empty the list.")
	if len(destination) != final:
		raise ValueError("card.pending did not extend the destination the correct length")

## Start House Brobnar

def key001(game):
	"""Anger. Ready and fight with a friendly creature.
	"""
	print("\nYour creatures:")
	game.activePlayer.printShort(game.activePlayer.board["Creature"], False)
	print("")
	if len(game.activePlayer.board["Creature"]) == 0:
		print("You have no creatures to target. The card is still played.")
		return
	while True:
		try:
			choice = int(input('Choose a friendly creature: '))
			break
		except:
			pass
	if not game.activePlayer.board["Creature"][choice].ready and 0 <= choice < len(game.activePlayer.board["Creature"]):
		game.activePlayer.board["Creature"][choice].ready = True
		game.fightCard(choice)
	else:
		game.fightCard(choice)


def key002(game):
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

def key003(game):
	"""Blood Money: Place 2 amber from the common supply on an enemy creature.
	"""
	if len(game.inactivePlayer.board["Creature"]) == 0:
		print("Your opponent has no creatures for you to target. The card is still played.")
		return
	else:
		game.inactivePlayer.printShort(game.inactivePlayer.board["Creature"])
		while True:
			try:
				choice = int(input("Choose an enemy creature to target: "))
				break
			except:
				pass
		game.inactivePlayer.board["Creature"][choice].captured += 2
		print(game.inactivePlayer.board["Creature"][choice].title + " now has " + game.inactivePlayer.board["Creature"][choice].amber + " amber.")
		return
				
def key004(game):
	""" Brothers in Battle: Value: 1 amber. Choose a house. For the remainder of the turn, each friendly creature of that house may fight.
	"""
	game.chooseHouse("extraFight") # this function will add extra houses that only work for fighting

def key005(game):
	"""Burn the Stockpile: If your opponent has 7 or more amber, they lose 4.
	"""
	if game.inactivePlayer.amber > 6:
		game.inactivePlayer.amber -= 4
		print("Your opponent had " + str(game.inactivePlayer.amber + 4) + " amber, and you destroyed 4, leaving them with " + str(game.inactivePlayer.amber) + " amber." )
	else:
		print("Your opponent didn't have enough amber, so you didn't destroy anything. The card is still played.")

def key006 (game):
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
			while True:
				try:
					choice = int(input("Choose which minion will stay alive."))
					# test for OOB
					str(inactiveBoard[choice].text)
					break
				except: pass
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
			while True:
				try:
					choice = int(input("Choose which minion will stay alive."))
					# test for OOB
					str(activeBoard[choice].text)
					break
				except: pass
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

def key007 (game):
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
		for x in range(len(activeBoard)):
			# so that i can work from right to left
			x = abs(x - len(activeBoard) + 1)
			if activeBoard[x].damage > 0:
				pendingDiscard.append(activeBoard.pop(x))

	pending(game, pendingDiscard, game.activePlayer.discard)

	# inactive player
	damageList = [x.damage for x in inactiveBoard if x.damage > 0]
	# easy case: everything damaged
	if len(damageList) == len(inactiveBoard): pendingDiscard = inactiveBoard
	else:
		for x in range(len(inactiveBoard)):
			# so that i can work from right to left
			x = abs(x - len(inactiveBoard) + 1)
			if inactiveBoard[x].damage > 0:
				pendingDiscard.append(inactiveBoard.pop(x))

	pending(game, pendingDiscard, game.inactivePlayer.discard)
	
	# finally, add chains
	game.activePlayer.chains += 3

def key008(game):
	"""Follow the Leader: For the remainder of the turn, each friendly creature may fight.
	"""
	# as easy as setting game.extraFightHouses to all houses
	game.extraFightHouses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]

def bloodOfTitans (creature):
	"""This creature gets +5 power"""

def bumpsy (oppAmber):
	"""Your opponent loses one amber."""

def earthshaker (OppBoard, Myboard):
	"""Destroy each creature with power 3 or lower."""


def gangerChieftain (creature):
	"""You may ready and fight with a neighboring creature"""

def hebeTheHuge (OppBoard, MyBoard):
	"""Deal 2 damage to each other undamaged creature."""

def kelifiDragon (MyAmber):
	"""Kelifi Dragon cannot be played unless you have 7 or more amber."""

def lavaBall (creature):
	"""Deal 4 damage to a creature with 2 splash."""

def lootTheBodies (OppBoard):
	"""For the remainder of the turn, gain 1 amber each time \
	an enemy creature is destroyed."""

def lomirFlamefist(OppAmber):
	"""If your opponent has 7 or more amber, they lose 2."""

def takeThatSmartypants (OppBoard):
	"""Value: 1 amber. Steal 2 amber if your opponent has \
	3 or more Logos cards in play."""

def phoenixHeart (creature):
	"""Give a creature the destroyed.phoenixHeart() effect"""

def punch (creature):
	"""Value: 1 amber. Deal 3 damage to a creature."""

def relentlessAssault (creature1, creature2, creature3):
	"""Ready and fight with up to 3 friendl creatures,\
	one at a time."""

def smaaash(creature):
	"""Stun a creature."""

def smith (MyBoard, OppBoard):
	"""Value: 1 amber. Gain 2 amber if you control more creatures than your opponent."""

def soundTheHorns (Deck):
	"""Value: 1 amber. Discard cards from the top of your deck \
	until you either discard a Brobnar creature or run out of \
	cards. If you discarded a Brobnar creature this way, put it \
	into your hand."""

def tremor (creature):
	"""Stun a creature and each of its neighbors."""

def unguardedCamp (MyBoard, OppBoard):
	"""Value: 1 amber. For each creature you have in excess of\
	your opponent, a friendly creature captures 1 amber. Each \
	creature cannot capture more than 1 amber this way."""

def wardrummer(MyBoard):
	"""Return each other friendly Brobnar creature to your hand."""

def warsong (MyBoardstate):
	"""For the remainder of the turn, gain 1 amber each time\
	a friendly creature fights."""

def yoMamaMastery (creature):
	"""Fully heal this creature"""

## End House Brobnar



## Start Dis actions


if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')