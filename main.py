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


# def chooseDecks(): #called by startup()
#   """The players choose their decks from deckDict, and if their choice isn't there they are offered the option to import a deck.
#   """
#   run = True
#   clock = pygame.time.Clock()
#   first_run = True
#   loaded_decks = 0
#   deck_options = []
#   with open('decks/deckList.json', encoding='UTF-8') as f:
#     stuff = json.load(f)
#     for x in stuff:
#       deck_options.append(x['name'])
  
#   while run:
#     clock.tick(FPS)

#     # this needs to be in game in some very different way than currently

#     if first_run:
#       print("Available decks:")
#       with open('decks/deckList.json', encoding='UTF-8') as f:
#         stuff = json.load(f)
#         for x in range(len(stuff)):
#           print(str(x) + ': ' + stuff[x]['name'])
#       deckChoice = makeChoice("Choose player 1's deck by index: ", stuff, show = False)
#       # some code here to list player 2's options, which is all the decks except the one player 1 just chose
#       print("Available decks:")
#       with open('decks/deckList.json', encoding='UTF-8') as f:
#         stuff2 = json.load(f)
#         for x in range(len(stuff2)):
#           if x != deckChoice:
#             print(str(x) + ': ' + stuff2[x]['name'])
#       deckChoice2 = deckChoice
#       while deckChoice2 == deckChoice:
#           deckChoice2 = makeChoice("Choose player 2's deck by index: ", stuff2, show = False)
#       first = random.choice([deckChoice, deckChoice2])
#       # print(first)
#       if first == deckChoice:
#           second = deckChoice2
#       else:
#           second = deckChoice
#       global game
#       # game = Board(first, second)
#       # game.startGame()
#       board = Board()
#       first_run = False

#     ## all this crap is going to need to go into game.py in some way

#     for event in pygame.event.get():
#       print(event)
#       if loaded_decks < 2:
#         board.make_popup(deck_options, WIN)
#       else:
#         board.startGame()
      
#       if event.type == pygame.MOUSEMOTION:
#         #update mouse position
#         self.mousex, self.mousey = event.pos

#       if event.type == pygame.QUIT:
#         run = False

#       if event.type == pygame.MOUSEBUTTONDOWN:
#         pass

#       if event.type == pygame.KEYDOWN:
#         if event.key == 113 and event.mod == 64:
#           run = False
#         pygame.display.toggle_fullscreen()

#     board.draw(WIN)
#     pygame.display.update()

#   pygame.quit()



startup(args.action.title())