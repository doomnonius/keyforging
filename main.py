import os, sys, logging, pyautogui

# Feature add: when the game is installed (like, properly, which is something I'm totally going to get to) a variable will be set that says where the game is installed, then this will be called.
## os.chdir('/mnt/c/Users/devon/workspace/codeclass/keyforge')

# import cards.cardsAsClass as card
import decks.decks as deck
import json, argparse
from game import Board

parser = argparse.ArgumentParser()
parser.add_argument("-a", "--action", help="launch the app, specifiying whether to start a [newgame], [import] a deck", type=str, default="newgame")
args = parser.parse_args()

"""This file should be where instructions are entered by the user, and they can ask for help.
"""

logging.basicConfig(filename='game.log',level=logging.DEBUG, format="%(asctime)s %(levelname)s %(message)s")

def startup(choice = ''): #Called at startup
  """The initial starting of the game. Includes importing the decks (and possibly loading a saved game).
  """
  logging.info("Game started with parameter: {}".format(choice))
  logging.info("Game is starting up!")
  choice = pyautogui.confirm("What would you like to do?", buttons=["New Game", "Import", "Decks", "Load", "Quit"])
  if choice == "Import":
    deck.importDeck()
    another = pyautogui.confirm("Would you like to import another deck?", buttons=["Yes", "No"]) # input("Would you like to import another deck (Y/n)? ")
    while another != 'No':
      deck.importDeck()
      another = pyautogui.confirm("Would you like to import another deck?", buttons=["Yes", "No"])
  elif choice == "New Game":
    Board()
  elif choice == "Load":
    # Display saved games, then let them choose one.
    # display saves here !!!!
    loaded = pyautogui.confirm("Which save would you like to load?", buttons=[x for x in ["A"]]) #input("Which save would you like to load?")
    load(loaded)
  elif choice == "Decks":
    while True:
      show = "Enter a deck's number to see the cards it contains.\n\nAvailable decks:\n"
      with open('decks/deckList.json', encoding='utf-8') as f:
        data = json.load(f)
        for x in range(0, len(data)):
          show += f"{x}: " + data[x]['name'] + "\n"
        chosen = int(pyautogui.prompt(show))
        cardList = ''
        for card in data[chosen]['deck']:
          cardList += f"{card['card_title']} [{card['house']}]\n"
        pyautogui.confirm(cardList)
      startup('')
      break
  else:
    return

def load(saveFile):
  """Loads a saved game.
  """


startup(args.action.title())