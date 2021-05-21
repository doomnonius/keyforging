from typing import Dict


##################
# Contains modules:
# absa
# makeChoice
# chooseSide
# stealAmber
##################

def absa(num, length):
  """ Returns an absolute value for modifying lists in place.
  """
  return abs(num - length + 1)

def makeChoice(stringy, L = [], show = True):
  """ Takes a string explaining the choice and a list, only accepts results within the length of the list.
  """
  if L != [] and show:
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
    game.activePlayer.printShort(activeBoard, False)
    side = 0
    if choices:
      choice = makeChoice("There are no enemy " + stringy.lower() + "s to target, so you must choose a friendly " + stringy.lower() + " to target: ", activeBoard)
      return choice, side
  else:
    while side[0] != "F" and side[0] != "E":
      side = input("Would you like to target an [E]nemy " + stringy.lower() + " or a [F]riendly " + stringy.lower() + "?\n>>>").title()
    if side[0] == "F":
      game.activePlayer.printShort(activeBoard, False)
      side = 0
      if choices:
        choice = makeChoice("Choose a target: ", activeBoard)
        return choice, side
    elif side[0] == "E":
      game.activePlayer.printShort(inactiveBoard, False)
      side = 1
      if choices:
        choice = makeChoice("Choose a target: ", inactiveBoard)
        return choice, side
  return side

def stealAmber(thief, victim, num):
  """ Function for stealing amber.
  """
  # this will account for edge cases that allow the inactive player to steal amber (namely, Magda leaving play)
  if "The Vaultkeeper" in [x.title for x in victim.board["Creature"]]:
    print("The steal effect fails because of Vaultkeeper.")
    return
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


def buildStateDict(deck1, deck2) -> Dict:
  return {}