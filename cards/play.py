from . import board
from . import fight

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

## Start House Brobnar

def anger():
	"""Value: 1 amber. Ready and fight with a friendly creature"""
	print('Your creatures are: ' + str(board.MyBoard))
	choice = input('Choose which one you would like to ready: ')
	if choice.ready:
		choice.ready = True
		fight.fight(choice)
	else:
		fight.fight(choice)


def barehanded (OppArt, MyArt):
	"""Value: 1 amber. Put Each artifact on top of its owner's \
	deck."""

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


