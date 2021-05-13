import os, sys, logging

from pygame.font import SysFont
logging.basicConfig(filename='game.log',level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

# Feature add: when the game is installed (like, properly, which is something I'm totally going to get to) a variable will be set that says where the game is installed, then this will be called.
## os.chdir('/mnt/c/Users/devon/workspace/codeclass/keyforge')

# import cards.cardsAsClass as card
import decks.decks as deck
import json, argparse
from game import Board
from helpers import distance

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="launch the app, specifiying whether to start a [newgame], [import] a deck", type=str, default="newgame")
args = parser.parse_args()

"""This file should be where instructions are entered by the user, and they can ask for help.
"""

def startup(choice = ''): #Called at startup
  """The initial starting of the game. Includes importing the decks (and possibly loading a saved game).
  """
  logging.info("Game started with parameter: {}".format(choice))
  logging.info("Game is starting up!")
  if choice != "Newgame" and choice != "Import" and choice != "Decks" and choice != "Load":
    choice = input("What would you like to do: [Import] a new deck, start a [NewGame], list imported [Decks], or [Load] a game? \n>>> ")
  if distance(choice, "Import") <= 1:
    deck.importDeck()
    another = input("Would you like to import another deck (Y/n)? ")
    while another != 'n' and another != 'N':
      deck.importDeck()
      another = input("Would you like to import another deck (Y/n)? ")
  elif distance(choice, "NewGame") <= 2:
    Board()
  elif distance(choice, "Load") <= 1:
    # Display saved games, then let them choose one.
    # display saves here !!!!
    loaded = input("Which save would you like to load?")
    load(loaded)
  elif distance(choice, "Decks") <= 1:
    while True:
      print("Available decks:")
      with open('decks/deckList.json') as f:
        data = json.load(f)
        for x in range(0, len(data)):
          print(str(x) + ': ' + data[x]['name'])
      startup('')
      break

def load(saveFile):
  """Loads a saved game.
  """


startup(args.action.title())