import cards.board as board
import cards.cardsAsClass as x
# I think it makes more sense to add these to the cardsAsClass file, which means that the only function here is addToBoard

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

## Start House Brobnar

def key001(game):
	"""Value: 1 amber. Ready and fight with a friendly creature"""
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
	"""Value: 1 amber. Put Each artifact on top of its owner's \
	deck."""
	# can't use a while loop b/c active player chooses order
	if len(game.activePlayer.board["Artifact"]) > 1:
		pendingDiscard = []
		while len(game.activePlayer.board["Artifact"]) > 0:
			pendingDiscard.append(game.activePlayer.board["Artifact"].pop())
	elif len(game.activePlayer.board["Artifact"]) == 1:
		game.activePlayer.deck.append(game.activePlayer.board["Artifact"].pop())
	else:
		pass
	try:
		game.activePlayer.printShort(pendingDiscard, False)
		while len(pendingDiscard) > 1:
			while True:
				try:
					choice = int(input("Choose which card to add to your deck: "))
					break
				except:
					pass
			game.activePlayer.deck.append(pendingDiscard.pop(choice))
	except:
		pass
	try:
		game.activePlayer.deck.append(pendingDiscard.pop())
	except:
		pass
	# run it all again w/ inactive player
	if len(game.inactivePlayer.board["Artifact"]) > 1:
		pendingDiscard = []
		while len(game.inactivePlayer.board["Artifact"]) > 0:
			pendingDiscard.append(game.inactivePlayer.board["Artifact"].pop())
	elif len(game.inactivePlayer.board["Artifact"]) == 1:
		game.inactivePlayer.deck.append(game.inactivePlayer.board["Artifact"].pop())
	else:
		pass
	try:
		game.inactivePlayer.printShort(pendingDiscard, False)
		while len(pendingDiscard) > 1:
			while True:
				try:
					choice = int(input("Choose which card to add to your opponent's deck: "))
					break
				except:
					pass
			game.inactivePlayer.deck.append(pendingDiscard.pop(choice))
	except:
		pass
	try:
		game.inactivePlayer.deck.append(pendingDiscard.pop())
	except:
		pass

def bloodMoney (creature):
	"""Place 2 amber from the common supply on an enemy creature."""

def bloodOfTitans (creature):
	"""This creature gets +5 power"""

def brothersInBattle (house):
	"""Value: 1 amber. Choose a house. For the remainder of the \
	turn, each friendly creature of that house may fight."""

def bumpsy (oppAmber):
	"""Your opponent loses one amber."""

def burnTheStockpile (oppamber):
	"""If your opponent has 7 or more amber, they lose 4."""

def championsChallenge (OppBoard, MyBoard):
	"""Destroy each enemy creature except the most powerful \
	enemy creature. Destroy each friendly creature except the \
	most powerful friendly creature. Ready and fight with your \
	remaining creature."""

def cowardsEnd (OppBoard, MyBoard):
	"""Destroy each undamaged creature. Gain 3 chains."""

def earthshaker (OppBoard, Myboard):
	"""Destroy each creature with power 3 or lower."""

def followTheLeader (MyBoard):
	"""For the remainder of the turn, each friendly creature may\
	fight."""

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