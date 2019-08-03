import cards.cardsAsClass as card
import decks.decks as deck 
from helpers import startup
import argparse # so we can call a new game from the command line

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="launch the app, specifiying whether to start a [newgame], [import] a deck", type=str, default="newgame")
args = parser.parse_args()

"""This file should be where instructions are entered by the user, and they can ask for help.
"""

startup(args.action.title())

# [card.printdetails(x) for x in deck.MyDeck]