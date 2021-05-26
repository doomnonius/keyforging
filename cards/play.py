from os import path
import time
import random
import pyautogui, pygame
from functools import reduce
from helpers import absa, makeChoice, chooseSide, stealAmber
# I think it makes more sense to add these to the cardsAsClass file, which means that the only function here is addToBoard

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

def passFunc(game, card):
  """ This catches on play abilities. It is called by all other play functions, and by default for card w/o play effects.
  """
  active = game.activePlayer.board
  inactive = game.inactivePlayer.board
  if card.type == "Creature":
    if "full_moon" in game.activePlayer.states and game.activePlayer.states["full_moon"]:
      game.activePlayer.amber += game.activePlayer.states["full_moon"]
    if "teliga" in [x.title for x in inactive["Creature"]]:
      count = 0
      for x in inactive["Creature"]:
        if x.title == "teliga":
          count += 1
      game.inactivePlayer.amber += count
    if "hunting_witch" in [x.title for x in active["Creature"]]:
      count = sum(x.title == "hunting_witch" for x in active["Creature"])
      if card.title == "hunting_witch":
        count -= 1 # this prevents hunting witch from triggering off itself
      game.activePlayer.amber += count
    if card.house == "Mars" and "tunk" in [x.title for x in active["Creature"]]:
      location = [active["Creature"].index(x) for x in active["Creature"] if x.title == "tunk"]
      for x in location:
        active["Creature"][x].damage = 0
    if "charge" in game.activePlayer.states and game.activePlayer.states["charge!"] and inactive["Creature"]:
      # above line makes sure there will be at least one potential target
      choice = game.chooseCards("Creature", "Choose an enemy minion to deal 2 damage to:", "enemy")[0][1]
      inactive["Creature"][choice].damageCalc(game, 2)
      if inactive["Creature"][choice].updateHealth():
        game.pendingLoc.append(inactive["Creature"].pop(choice))
    # stuff that gives armor
    if "gray_monk" in [x.title for x in active["Creature"]]:
      extra = sum(x.title == "gray_monk" for x in active["Creature"])
      if card.name == "gray_monk":
        extra -= 1 # so it doesn't hit itself
      card.extraArm += extra
    if "banner_of_battle" in [x.title for x in active["Creature"]]:
      extra = sum(x.title == "banner_of_battle" for x in active["Creature"])
      card.extraPow += extra
    # this is deliberately after gray_monk
    if "autocannon" in inactive["Artifact"] + active["Artifact"]:
      count = sum(x.title == "autocannon" for x in inactive["Artifact"] + active["Artifact"])
      card.calcDamage(game, count)
      if card.updateHealth():
        game.pendingReloc.append(active["Creature"].pop(active["Creature"].index(card)))
    if "pingle_who_annoys" in inactive["Artifact"] + active["Artifact"]:
      count = sum(x.title == "pingle_who_annoys" for x in inactive["Artifact"] + active["Artifact"])
      card.calcDamage(game, count)
      if card.updateHealth():
        game.pendingReloc.append(active["Creature"].pop(active["Creature"].index(card)))
    game.pending()
  if card.type == "Artifact" and "carlo_phantom" in [x.title for x in active["Creature"]]:
    stealAmber(game.activePlayer, game.inactivePlayer, sum(x.title == "carlo_phantom" for x in active["Creature"]))
    pyautogui.alert("'Carlo Phantom' stole 1 amber for you. You now have " + str(game.activePlayer.amber) + " amber.")
  if "library_access" in game.activePlayer.states and game.activePlayer.states["library_access"]:
    game.activePlayer += game.activePlayer.states["library_access"]
    pyautogui.alert("You draw a card because you played 'Library Access' earlier this turn.")
  if "soft_landing" in game.activePlayer.states and game.activePlayer.states["soft_landing"]:
    card.ready = True
    pyautogui.alert(card.title + " enters play ready!")
    game.activePlayer.states["soft_landing"] = 0

###########
# Brobnar #
###########

###########
# Actions #
###########

def anger(game, card):
  """Anger. Ready and fight with a friendly creature.
  """
  passFunc(game, card)
  
  if not game.activePlayer.board["Creature"]:
    pyautogui.alert("No valid targets. The card is still played.")
    return
  
  choice = game.chooseCards("Creature", "Choose a friendly creature:", "friend")[0][1]
  if not game.activePlayer.board["Creature"][choice].ready:
    game.activePlayer.board["Creature"][choice].ready = True
    game.fightCard(choice)
  else:
    game.fightCard(choice)


def barehanded(game, card):
  """Barehanded. Put each artifact on top of its owner's \
  deck.
  """
  passFunc(game, card)
  while len(game.activePlayer.board["Artifact"]) > 0:
    game.pendingReloc.append(game.activePlayer.board["Artifact"].pop())
  # run it all again w/ inactive player
  while len(game.inactivePlayer.board["Artifact"]) > 0:
    game.pendingReloc.append(game.inactivePlayer.board["Artifact"].pop())
  # deal with all artifacts
  game.pending("deck")

def blood_money(game, card):
  """Blood Money: Place 2 amber from the common supply on an enemy creature.
  """
  passFunc(game, card)
  if len(game.inactivePlayer.board["Creature"]) == 0:
    pyautogui.alert("Your opponent has no creatures for you to target. The card is still played.")
  else:
    choice = game.chooseCards("Creature", "Choose an enemy creature to gain two amber:", "enemy")[0][1]
    game.inactivePlayer.board["Creature"][choice].captured += 2
    pyautogui.alert(game.inactivePlayer.board["Creature"][choice].title + " now has " + game.inactivePlayer.board["Creature"][choice].amber + " amber.")
    return
        
def brothers_in_battle(game, card):
  """ Brothers in Battle: Value: 1 amber. Choose a house. For the remainder of the turn, each friendly creature of that house may fight.
  """
  passFunc(game, card)
  game.extraFightHouses.append(game.chooseHouse("extraFight")[0]) # this function will add extra houses that only work for fighting

def burn_the_stockpile(game, card):
  """Burn the Stockpile: If your opponent has 7 or more amber, they lose 4.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber > 6:
    game.inactivePlayer.amber -= 4
    pyautogui.alert("Your opponent had " + str(game.inactivePlayer.amber + 4) + " amber, and you destroyed 4, leaving them with " + str(game.inactivePlayer.amber) + " amber." )
  else:
    pyautogui.alert("Your opponent didn't have enough amber, so you didn't destroy anything. The card is still played.")

def champions_challenge(game, card):
  """ Champion's Challenge: Destroy each enemy creature except the most powerful enemy creature. Destroy each friendly creature except the most powerful friendly creature. Ready and fight with your remaining creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]

  # inactive board first
  if len(inactiveBoard) > 1:
    # find highest power
    high = max([x.power for x in inactiveBoard])
    # discard all cards that aren't tied
    n = 0
    while min([x.power for x in inactiveBoard]) < high:
      if inactiveBoard[n].power < high:
        game.pendingReloc.append(inactiveBoard.pop(n))
      else:
        n += 1
        if n == len(inactiveBoard):
          break
    # check length of inactiveBoard, if > 1, let player choose which one to keep
    if len(inactiveBoard) > 1: # at this point only creatures tied for highest power will be in play
      choice = game.chooseCards("Creature", "Choose which enemy creature will survive:", "enemy")[0][1]
      # then destroy all cards except choice
      while len(inactiveBoard > 1):
        # easy part: choice at beginning of list
        if choice == 0: game.pendingReloc.append(inactiveBoard[1])
        else:
          game.pendingReloc.append(inactiveBoard[0])
          choice -= 1

  # i don't need to restate pending discard as empty, because pending() will raise an error if the list isn't emptied

  # then active board
  if len(activeBoard) > 1:
    # find highest power
    high = max([x.power for x in activeBoard])
    # discard all cards that aren't tied
    n = 0
    while min([x.power for x in activeBoard]) < high:
      if activeBoard[n].power < high:
        game.pendingReloc.append(activeBoard.pop(n))
      else:
        n += 1
        if n == len(activeBoard):
          break
    # check length of activeBoard, if > 1, let player choose which one to keep
    if len(activeBoard) > 1:
      choice = game.chooseCards("Creature", "Choose which friendly creature will survive:", "friend")[0][1]
      # then discard all cards except choice
      while len(activeBoard > 1):
        # easy part: choice at beginning of list
        if choice == 0: game.pendingReloc.append(activeBoard[1])
        else:
          game.pendingReloc.append(activeBoard[0])
          choice -= 1
  game.pending()

  # then ready and fight with remaining minion
  if len(game.activePlayer.board["Creature"]) == 0:
    pyautogui.alert("You have no creatures to target.")
    return
  choice = game.chooseCards("Creature", "Choose a creature to fight with:", "friend")[0][1] # because ward will be a thing, and something could happen
  if not game.activePlayer.board["Creature"][choice].ready:
    game.activePlayer.board["Creature"][choice].ready = True
    game.fightCard(choice)
  else:
    game.fightCard(choice)

def cowards_end (game, card):
  """Coward's End: Destroy each undamaged creature. Gain 3 chains.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc
  length = len(activeBoard)
  # active player
  undamageList = [x.damage for x in activeBoard if x.damage == 0]
  # easy case: everything undamaged
  if len(undamageList) == len(activeBoard): pendingDiscard = activeBoard
  else:
    [pendingDiscard.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].damage == 0]
  length = len(inactiveBoard)
  # inactive player
  undamageList = [x.damage for x in inactiveBoard if x.damage == 0]
  # easy case: everything undamaged
  if len(undamageList) == len(inactiveBoard): 
    pendingDiscard.extend(inactiveBoard)
    inactiveBoard = []
  else:
    [pendingDiscard.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].damage == 0]
  
  game.pending()
  
  # finally, add chains
  game.activePlayer.chains += 3

def follow_the_leader(game, card):
  """Follow the Leader: For the remainder of the turn, each friendly creature may fight.
  """
  passFunc(game, card)
  # as easy as setting game.extraFightHouses to all houses
  game.extraFightHouses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]

def lava_ball (game, card):
  """Lava Ball: Deal 4 damage to a creature with 2 splash.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc # this one's fine because only one side is ever affected; pending would be able to handle it anyway though

  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets. The card is still played.")
    return

  choice = game.chooseCards("Creature", "Deal 4 damage with 2 splash to a creature:")[0]
  if choice[0] == "fr":
    card = activeBoard[choice[1]]
    card.damageCalc(game, 4)
    for neigh in card.neighbors():
      activeBoard[neigh].damageCalc(game, 2)
      if activeBoard[neigh].updateHealth():
        pendingDiscard.append(activeBoard.pop(neigh))
    if card.updateHealth():
      pendingDiscard.append(activeBoard.pop(choice))
  else:
    card = inactiveBoard[choice[1]]
    card.damageCalc(game, 4)
    for neigh in card.neighbors():
      inactiveBoard[neigh].damageCalc(game, 2)
      if inactiveBoard[neigh].updateHealth():
        pendingDiscard.append(inactiveBoard.pop(choice - 1))
    if card.updateHealth():
      pendingDiscard.append(inactiveBoard.pop(choice))
  game.pending()

def loot_the_bodies (game, card):
  """ Loot the Bodies: For the remainder of the turn, gain 1 amber each time an enemy creature is destroyed.
  """
  passFunc(game, card)
  game.activePlayer.states["loot_the_bodies"] += 1
  # skipping the rest for now, until event emitters or etc are figured out

def take_that_smartypants (game, card):
  """Take that, Smartypants: Steal 2 amber if your opponent has 3 or more Logos cards in play.
  """
  passFunc(game, card)
  inactiveBoard = game.inactivePlayer.board
  count = 0
  for x in (inactiveBoard["Creature"] + inactiveBoard["Artifact"]):
    if x.house == "Logos":
      count += 1
      if count >= 3:
        stealAmber(game.activePlayer, game.inactivePlayer, 2)
        pyautogui.alert("You stole 2 amber from your opponent!")
        break
  else:
    pyautogui.alert("Your opponent had less than 3 Logos cards in play, so you didn't steal anything. The card is still played.")


def punch (game, card):
  """ Punch: Deal 3 damage to a creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc # fine b/c only one side ever affected

  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets. The card is still played.")
    return

  choice = game.chooseCards("Creature", "Deal 3 damage to a creature:")[0]
  if choice[0] == "fr":
    activeBoard[choice].damageCalc(game, 3)
    if activeBoard[choice].update:
      pendingDiscard.append(activeBoard[choice])
  else:
    inactiveBoard[choice].damageCalc(game, 3)
    if inactiveBoard[choice].update:
      pendingDiscard.append(inactiveBoard[choice])
  game.pending()

def relentless_assault (game, card):
  """ Relentless Assault: Ready and fight with up to 3 friendly creatures, one at a time.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  if activeBoard:
    choices = game.chooseCards("Creature", "Choose up to three creatures, in the order you'd like them to fight:", "friend", 3)
  else:
    pyautogui.alert("No friendly creatures to target.")
    return
  choices = [x[1] for x in choices]
  name_check = [activeBoard[x].title for x in choices]
  
  while len(choices) > 0:
    original = len(activeBoard)
    choice = choices.pop(0)
    name = name_check.pop(0)
    # first choice should always be valid, but not the rest
    if choice < len(activeBoard) and activeBoard[choice].title == name:
      activeBoard[choice].ready = True
      game.fightCard(choice)
    else:
      continue
    # make game equal the result of this function call, so that if anything died we have the new board state
    # this doesn't account for phoenix heart, or anything else that might kill the creature before we get to it
    if original > len(activeBoard):
      for x in choices:
        if x > choice:
          x -= 1

def smith (game, card):
  """Smith: Gain 2 amber if you control more creatures than your opponent.
  """
  passFunc(game, card)
  if len(game.activePlayer.board["Creature"]) > len(game.inactivePlayer.board["Creature"]):
    game.activePlayer.amber += 2
    pyautogui.alert("You have more creatures, so you gain 2 amber.")
  else:
    pyautogui.alert("You do not have more creatures, so you don't gain the 2 extra amber. The card is still played.")

def sound_the_horns (game, card):
  """Sound the Horns: Discard cards from the top of your deck until you either discard a Brobnar creature or run out of cards. If you discarded a Brobnar creature this way, put it into your hand.
  """
  passFunc(game, card)
  discard = game.activePlayer.discard
  deck = game.activePlayer.deck
  hand = game.activePlayer.hand
  while deck and (deck[-1].house != "Brobnar" or deck[-1].type != "Creature"):
    discard.append(deck.pop())
  if not deck:
    pyautogui.alert("Your deck is empty, and you found no Brobnar creatures.")
  else: # House is brobnar and type is creature if we get here
    hand.append(deck.pop())

def tremor (game, card):
  """Tremor: Stun a creature and each of its neighbors.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.activePlayer.board["Creature"]

  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets. Card is still played.")
    return
  
  choice = game.chooseCards("Creature", "Stun a creature and its neighbors:")[0]

  if choice[0] == "fr":
    card = activeBoard[choice[1]]
    card.stun = True
    for neigh in card.neighbors():
      activeBoard[neigh].stun = True
  else:
    card = inactiveBoard[choice[1]]
    card.stun = True
    for neigh in card.neighbors():
      inactiveBoard[neigh].stun = True

def unguarded_camp (game, card):
  """Unguarded Camp: For each creature you have in excess of your opponent, a friendly creature captures 1 amber. Each creature cannot capture more than 1 amber this way.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  diff = len(activeBoard) - len(inactiveBoard)

  if diff < 0:
    pyautogui.alert("You have less creatures than your opponent, so no amber is captured. The card is stil played.")
    return
  elif diff == 0:
    pyautogui.alert("You have as many creatures as your opponent, so no amber is captured. The card is still played.")
    return
  # pyautogui.alert(f"You have {diff} more minions than your opponent, so you will capture {diff} amber.")
  if diff == len(activeBoard) and game.inactivePlayer.amber >= diff:
    [x.capture(game, 1) for x in activeBoard]
    return
  diff = min(diff, game.inactivePlayer.amber)
  choices = [x[1] for x in game.chooseCards("Creature", f"Choose {diff} friendly creatures to capture an amber:", "friend", diff, True)]
  for x in choices:
    activeBoard[x].capture(game, 1)

def warsong (game, card):
  """Warsong: For the remainder of the turn, gain 1 amber each time a friendly creature fights.
  """
  passFunc(game, card)
  game.activePlayer.states["warsong"] += 1

#####################
# Brobnar Creatures #
#####################

def bumpsy (game, card):
  """Bumpsy: Your opponent loses one amber.
  """
  passFunc(game, card)
  victim = game.inactivePlayer.amber
  if victim > 0:
    game.inactivePlayer.amber -= 1
    pyautogui.alert("Your opponent had " + str(victim) + " amber.\n\nThey now have " + str(game.inactivePlayer.amber) + " amber.")
    return
  pyautogui.alert("Your opponent had no amber to lose.")



def earthshaker (game, card):
  """Earthshaker: Destroy each creature with power 3 or lower.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard= game.pendingReloc
  length = len(activeBoard)
  # active board: LC
  [pendingDiscard.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].power <= 3]
  # then inactive
  length = len(inactiveBoard)
  [pendingDiscard.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].power <= 3]
  game.pending()

def ganger_chieftain (game, card):
  """Ganger Chieftain: You may ready and fight with a neighboring creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]

  # this can't handle the edge case where ganger chieftain is destroyed upon entering
  if len(activeBoard) == 1:
    return

  if activeBoard.index(card) == 0:
    maybe = pyautogui.confirm(f"Would you like to ready and fight with {activeBoard[1].title}", buttons=["Yes", "No"])
    if maybe == "Yes":
      activeBoard[1].ready = True
      game.fightCard(1)
    return
  elif activeBoard.index(card) == len(activeBoard)-1:
    maybe = pyautogui.confirm(f"Would you like to ready and fight with {activeBoard[-2].title}", buttons=["Yes", "No"])
    if maybe == "Yes":
      activeBoard[-2].ready = True
      game.fightCard(len(activeBoard)-2)
    return

def hebe_the_huge (game, card):
  """Hebe the Huge: Deal 2 damage to each other undamaged creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc

  # deal damage
  [x.damageCalc(game, 2) for x in activeBoard if x.damage == 0 and activeBoard.index(x) != activeBoard.index(card)]
  # deal damage
  [x.damageCalc(game, 2) for x in inactiveBoard if x.damage == 0]
  # check for deaths
  length = len(activeBoard)
  [pendingDiscard.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].updateHealth()]
  # check for deaths
  length = len(inactiveBoard)
  [pendingDiscard.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].updateHealth()]
  game.pending()

def lomir_flamefist (game, card):
  """Lomir Flamefist: If your opponent has 7 or more amber, they lose 2.
  """
  passFunc(game, card)
  victim = game.inactivePlayer.amber
  if victim >= 7:
    pyautogui.alert(f"Your opponent had {victim} amber. They now have {victim - 2} amber.")
    game.inactivePlayer.amber -= 2
    return
  pyautogui.alert(f"Your opponent only had {victim} amber. They don't lose anything.")

def smaaash (game, card):
  """Smaaash: Stun a creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  
  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets.")
    return

  choice = game.chooseCards("Creature", "Stun a friendly creature:")[0]

  if choice[0] == "fr":
    activeBoard[choice[1]].stun = True
  else:
    inactiveBoard[choice[1]].stun = True

def wardrummer (game, card):
  """Wardrummer: Return each other friendly Brobnar creature to your hand.
  """
  passFunc(game, card)
  index = game.activePlayer.board["Creature"].index(card)
  activeBoard = game.activePlayer.board["Creature"]
  pending = game.pendingReloc
  length = len(activeBoard)
  [pending.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].house == 'Brobnar' and abs(x - length + 1) != index]
  game.pending('hand')

def yo_mama_mastery(game, card):
  """Yo Mama Mastery: Fully heal this creature
  """
  passFunc(game, card)
  # I'm going to only handle the play effect, I'll write something else to handle upgrades later
  # whatever that looks like, this card is going to be attached first, so we'll need to heal the attached card
  card.attached.damage = 0

## End house Brobnar

#######
# Dis #
#######

###########
# Actions #
###########

def a_fair_game (game, card):
  """ A Fair Game: Discard top card of opp's deck, reveal their hand. Gain amber for each card in hand matching house of discarded card. Opponent repeats effect on you.
  """
  passFunc(game, card)
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
  passFunc(game, card)
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
  passFunc(game, card)
  house = ''
  while house == '':
    house = input("Choose a house: ").title()
    if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]: break
    else: house = ''
  game.inactivePlayer.states["House"].update({"Control the Weak":house})

def key056(game, card):
  """ Creeping Oblivion: purge up to 2 cards from a discard pile.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.activePlayer.board["Creature"]
  pendingDestroyed = []
  choice = makeChoice("Choose a number. All creatures with power equal to this number will be destroyed: ")
  # active player
  length = len(active)
  [pendingDestroyed.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].power == choice]
  #inactive player
  length = len(inactive)
  [pendingDestroyed.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].power == choice]
  game.pending(pendingDestroyed)

def key058(game, card):
  """ Fear: Return an enemy creature to its owner's hand.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  if len(inactive) == 0:
    print("Your opponent has no creatures to target. The card is still played.")
    return
  elif len(inactive) == 1:
    choice = 0
  else:
    choice = makeChoice("Choose a minion to return to your opponent's hand: ", inactive)
  pending.append(inactive.pop(choice))
  game.pending(pending, 'hand')

def key059(game, card):
  """ Gateway to Dis: Destroy each creature. Gain three gains.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  # active player
  while len(active) > 0:
    pendingDiscard.append(active.pop())
  # inactive player
  while len(inactive) > 0:
    pendingDiscard.append(inactive.pop())

  game.pending(pendingDiscard)

  # add chains
  game.activePlayer.chains += 3
  
def key060(game, card):
  """ Gongoozle: Deal 3 to a creature. If it is not destroyed, its owner discards a random card from their hand.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = [] # fine b/c only ever one side
  choice, side = chooseSide(game)
  if side == 0: # friendly side
    active[choice].damageCalc(game, 3)
    if active[choice].updateHealth():
      pendingDiscard.append(active.pop(choice))
      game.pending(pendingDiscard)
    else:
      ran = random.choice(list(range(len(active))))
      pendingDiscard.append(game.activePlayer.hand.pop(ran))
      discardA = True
  # enemy side
  inactive[choice].damageCalc(game, 3)
  if inactive[choice].updateHealth(): 
    pendingDiscard.append(inactive.pop(choice))
    game.pending(pendingDiscard)
  else:
    ran = random.choice(list(range(len(inactive))))
    pendingDiscard.append(game.inactivePlayer.hand.pop(ran))
  game.pending(pendingDiscard, destroyed = False)
  
  if discardA and "Rock-Hurling Giant" in [x.title for x in active] and game.activePlayer.discard[-1].house == "Brobnar":
    side = chooseSide(game, choices = False)
    if side == 0:
      target = makeChoice("Choose a creature to target: ", active)
      active[target].damageCalc(game, 4)
      if active[target].updateHealth():
        pendingDiscard.append(active.pop(target))
    else:
      target = makeChoice("Choose a creature to target: ", inactive)
      inactive[target].damageCalc(game, 4)
      if inactive[target].updateHealth():
        pendingDiscard.append(inactive.pop(target))
    game.pending(pendingDiscard)


def key061(game, card):
  """ Guilty Hearts: Destroy each creature with any amber on it.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  # active player
  length = len(active)
  [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].captured > 0]
  # inactive player
  length = len(inactive)
  [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].captured > 0]
  game.pending(pendingDiscard)

def key062(game, card):
  """ Hand of Dis: Destroy a creature that is not on a flank.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = [] # fine b/c only one target
  # running a modified version of chooseSide because of the slightly different restrictions on this card
  side = ''
  if len(active) <= 2 and len(inactive) <= 2:
    print("There are no creatures not on a flank to target. The card is still played.")
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
  elif side == 1:
    pendingDiscard.append(inactive.pop(choice))
  game.pending(pendingDiscard)

def key063(game, card):
  """ Hecatomb: Destroy each Dis creature. Each player gains 1 amber for each creature they control that was destroyed this way.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  # active player
  length = len(active)
  [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length+ 1)].house == "Dis"]
  count = len(pendingDiscard)
  game.activePlayer.amber += count
  # inactive player
  length = len(inactive)
  [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].house == "Dis"]
  count = len(pendingDiscard) - count # lowest possibility is 0
  game.inactivePlayer.amber += count
  game.pending(pendingDiscard)

def key064(game, card):
  """ Tendrils of Pain: Deal 1 to each creature. Deal an additional 3 to each creature if your opponent forged a key on their previous turn.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  # deal 1 damage to everything
  # active
  length = len(active)
  [x.damageCalc(game, 1) for x in active]
  [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in active if active[abs(x - length + 1)].updateHealth()]
  # inactive
  length = len(inactive)
  [x.damageCalc(game, 1) for x in inactive]
  [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in inactive if inactive[abs(x - length + 1)].updateHealth()]

  # potential extra 3 damage to everything
  if not game.forgedLastTurn[0]:
    return
  # active
  length = len(active)
  [x.damageCalc(game, 3) for x in active]
  [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in active if active[abs(x - length + 1)].updateHealth()]
  # inactive
  length = len(inactive)
  [x.damageCalc(game, 3) for x in inactive]
  [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in inactive if inactive[abs(x - length + 1)].updateHealth()]
  game.pending(pendingDiscard)

def key065(game, card):
  """ Hysteria: Return each creature to its owner's hand.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  # active
  length = len(active)
  [pending.append(active.pop(abs(x - length + 1))) for x in range(len(active))]
  # inactive
  length = len(inactive)
  [pending.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive))]
  game.pending(pending, 'hand')

def key066(game, card):
  """ Key Hammer: If your opponent forged a key on their previous turn, unforge it. Your opponent gains 6 amber.
  """
  passFunc(game, card)
  if game.forgedLastTurn[0]:
    game.inactivePlayer.keys -= 1
  game.inactivePlayer.amber += 6

def key067(game, card):
  """ Mind Barb: Your opponent discards a random card from their hand.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.hand
  ran = random.choice(list(range(len(inactive))))
  game.inactivePlayer.discard.append(inactive.pop(ran))
  print("your opponent discarded:\n" + repr(game.inactivePlayer.discard[-1]))

def key068(game, card):
  """ Pandemonium: Each undamaged creature captures 1 from its opponent.
  """
  passFunc(game, card)
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
  passFunc(game, card)
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
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = [] # fine b/c only hits one side
  length = len(inactive)
  armorList = [inactive[abs(x - length + 1)].armor for x in range(len(inactive))]
  # deal damage
  for x in range(len(inactive)):
    if armorList[x] > 0:
      inactive[abs(x - length + 1)].armor -= armorList[x]
      inactive[abs(x - length + 1)].damageCalc(game, armorList[x])
  # check for deaths
  [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].updateHealth()]
  game.pending(pendingDiscard)

def key071(game, card):
  """ Three Fates: Destroy the three most powerful creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard= []
  # check # of creatures
  if len(active) + len(inactive) <= 3:
    # active
    pendingDiscard.extend(active)
    # discard
    pendingDiscard.extend(inactive)
    inactive = []
    game.pending(pendingDiscard)
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
      [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].power == high]
      #inactive
      length = len(inactive)
      [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].power == high]
      game.pending(pendingDiscard)
      return
    elif count < left: # add all to relevant discards and continue
      length = len(active)
      [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].power == high]
      length = len(inactive)
      [pendingDiscard.append(inactive.pop(abs(x - length+ 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].power == high]
      left -= count
    else: #if count > left, choose which card to discard
      print("Your minions at specified power: ")
      [print(highList.index(x) + ": " + str(x)) for x in highList if x.deck == game.activePlayer.name]
      print("Opponent minions at specified power: ")
      [print(highList.index(x) + ": " + str(x)) for x in highList if x.deck == game.inactivePlayer.name]
      choice = makeChoice("Choose which minion to destroy: ", highList)
      # active
      try:
        pendingDiscard.append(active.pop(active.index(highList[choice])))
      # inactive
      except:
        pendingDiscard.append(inactive.pop(active.index(highList[choice])))
      left -= 1
  game.pending(pendingDiscard)

def key081(game, card):
  """ Charette: Capture 3 amber.
  """
  passFunc(game, card)
  card.capture(game, 3)

def key082(game, card):
  """ Drumble: if your opponent has 7 amber or more, capture all of it.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber >= 7:
    card.capture(game, game.inactivePlayer.amber)

def key088(game, card):
  """ Guardian Demon: Heal up to 2 damage from a creature. Deal that amount of damage to another creature
  """
  passFunc(game, card)
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
    active[choice].damageCalc(game, heal)
    if active[choice].updateHealth():
      pendingDisc.append(active.pop(choice))
    game.pending(pendingDisc)
  if side == 1: #enemy
    inactive[choice].damageCalc(game, heal)
    if inactive[choice].updateHealth():
      pendingDisc.append(inactive.pop(choice))
    game.pending(pendingDisc)

def key094(game, card):
  """ Restringuntus: Choose a house. Your opponent cannot choose that house as their active house until Restringuntus leaves play.
  """
  passFunc(game, card)
  # no deck has more than one copy of this card
  game.chooseHouse(card.title)

def key096(game, card):
  """ Shooler: if your opponent has 4 or more amber, steal 1.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber >= 4:
    stealAmber(game.activePlayer, game.inactivePlayer, 1)
  
def key101(game, card):
  """ The Terror: If your opponent has no amber, gain 2.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber == 0:
    game.activePlayer.amber += 2

def truebaru (game, card):
  """ Truebaru: You must lose 3<a> in order to play Truebaru.
  """
  passFunc(game, card)
  game.activePlayer.amber -= 3

## End house Dis

#########
# Logos #
#########

###########
# Actions #
###########

def key107(game, card):
  """ Bouncing Deathquark: Destroy and enemy creature and a friendly creature. Repeat effect as many times as you want, as long as you can repeat entire effect.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  print(game)
  choice = makeChoice("Choose an enemy creature to destroy: ", inactive)
  pendingDiscard.append(inactive.pop(choice))
  if len(active) > 1:
    choice2 = makeChoice("Choose a friendly creature to destroy: ", active)
  elif len(active) == 1:
    choice2 = 0
  else:
    print("You have no creatures. The card's effect ends.")
    return
  pendingDiscard.append(active.pop(choice2))
  game.pending(pendingDiscard)
  while len(active) > 0 and len(inactive) > 0:
    print(game)
    choice = makeChoice("Choose an enemy creature to destroy: ")
    choice2 = makeChoice("Choose a friendly creature to destroy: ")
    pendingDiscard.append(inactive.pop(choice))
    pendingDiscard.append(active.pop(choice))
    game.pending(pendingDiscard)
  if len(active) == 0:
    print("You have no more creatures, so the effect cannot be repeated.")
    return
  print("Your opponent has no more creatures, so the effect cannot be repeated.")

def key108(game, card):
  """ Dimension Door: For the remainder of the turn, any amber you would gain from reaping is stolen from your opponent instead.
  """
  passFunc(game, card)
  # just set a state, effect doesn't stack from multiple copies
  game.activePlayer.states["Reap"].update({card.title:True})

def key109(game, card):
  """ Effervescent Principle: Each player loses half their amber (rounding down the loss). Gain one chain.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  # states should always be in deck that they affect
  game.inactivePlayer.states["Fight"].update({card.title:True})

def key111(game, card):
  """ Help from Future Self: Search your deck and discard pile for a Timetraveller, reveal it, and put it into your hand. Shuffle your discard pile into your deck.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  # update state
  game.inactivePlayer.states["Forge"].update({card.title:True})

def key113(game, card):
  """ Knowledge is Power: Choose one: Archive a card, or, for each archived card you have, gain 1 amber.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  archive = makeChoice("Choose a card from hand to archive: ", game.activePlayer.hand)
  game.activePlayer.archive.append(game.activePlayer.hand.pop(archive))
  print(archive[-1].title + " archived! Type 'Archive' to view your archive.")

def key115(game, card):
  """ Library Access: Purge this card. For the remainder of the turn, each time you play another card, draw a card.
  """
  passFunc(game, card)
  print(card.title + " is played, then immediately purged.")
  game.activePlayer.purge.append(game.activePlayer.board["Action"].pop()) # b/c library access will usually be only card, and if it isn't will definitely be last card
  game.activePlayer.states["Play"].update({card.title:True})

def key116(game, card):
  """ Neuro Syphon: If your opponent has more amber than you, steal 1 amber and draw a card.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  # this is a tough one. effect can stack, so we'll use a list
  game.activePlayer.states["Play"].update({card.title:[True]})

def key118(game, card):
  """ Positron Bolt: Deal 3 damage to a flank creature. Deal 2 damage to its neighbor. Deal 1 damage to the second creature's other neighbor.
  """
  passFunc(game, card)
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
    active[choice].damageCalc(game, 3)
    if choice == 0:
      try: 
        active[choice + 1].damageCalc(game, 2)
        try: active[choice + 2].damageCalc(game, 1)
        except: print("No second neighbor.")
      except: print("No neighbor.")
      [pendingDisc.append(active.pop(x)) for x in [choice + 2, choice + 1, choice] if active[x].updateHealth()]
    else:
      try: 
        active[choice - 1].damageCalc(game, 2)
        try: active[choice - 2].damageCalc(game, 1)
        except: print("No second neighbor.")
      except: print("No neighbor.")
      [pendingDisc.append(active.pop(x)) for x in [choice, choice - 1, choice - 2] if active[x].updateHealth()]
    game.pending(pendingDisc)
    return
  if choice != 0: choice = len(inactive) - 1
  inactive[choice].damageCalc(game, 3)
  if choice == 0:
    try:
      inactive[choice + 1].damageCalc(game, 2)
      try: inactive[choice + 2].damageCalc(game, 1)
      except: print("No second neighbor.")
    except: print("No neighbor.")
    [pendingDisc.append(inactive.pop(x)) for x in [choice + 2, choice + 1, choice] if inactive[x].updateHealth()]
  else:
    try:
      inactive[choice - 1].damageCalc(game, 2)
      try: inactive[choice - 2].damageCalc(game, 1)
      except: print("No second neighbor.")
    except: print("No neighbor.")
    [pendingDisc.append(inactive.pop(x)) for x in [choice, choice - 1, choice - 2] if inactive[x].updateHealth()]
  game.pending(pendingDisc)

def key119(game, card):
  """ Random Access Archives: Archive the top card of your deck.
  """
  passFunc(game, card)
  # if deck is empty, don't shuffle
  if len(game.activePlayer.deck) > 0:
    game.activePlayer.archive.append(game.activePlayer.deck.pop())
    print("The top card or your deck has been archived.")
    return
  print("Your deck is empty. Nothing happenss.")

def key120(game, card):
  """ Remote Access: use an opponent's artifact as if it were yours.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  game.activePlayer.deck, game.activePlayer.discard = game.activePlayer.discard, game.activePlayer.deck
  random.shuffle(game.activePlayer.deck)

def key122(game, card):
  """ Scrambler Storm: Your opponent cannot play action cards on their next turn.
  """
  passFunc(game, card)
  game.inactivePlayer.states["Play"].update({card.title:True})

def key123(game, card):
  """ Sloppy Labwork: Archive a card. Discard a card.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = []
  left = 2
  while left > 0 and len(active) + len(inactive) > 0:
    print("Choose a target to deal 2 damage to:")
    choice, side = chooseSide(game)
    if side == 0: # friendly
      active[choice].damageCalc(game, 2)
      if active[choice].update:
        pendingDisc.append(active.pop(choice))
      left -= 1
    elif side == 1: #enemy
      inactive[choice].damageCalc(game, 2)
      if active[choice].update:
        pendingDisc.append(active.pop(choice))
      left -= 1
    else:
      return
  game.pending(pendingDisc)

def key125(game, card):
  """ Wild Wormhole: Play the top card of your deck.
  """
  passFunc(game, card)
  game.playCard(100, False)

def key138(game, card):
  """ Dextre: Capture 1 amber.
  """
  passFunc(game, card)
  card.capture(game, 1)
  print("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def key140(game, card):
  """ Dr. Escotera: Gain 1 amber for each key your opponent has.
  """
  passFunc(game, card)
  game.activePlayer.amber += game.inactivePlayer.keys
  print("You now have " + str(game.activePlayer.amber) + " amber")

def key141(game, card):
  """ Dysania: Your opponent discards each of their archived cards. You gain 1 amber for each card discarded this way.
  """
  passFunc(game, card)
  # edge case: if your opponent has your cards in their archive, they don't get discarded, but sent to your hand
  if len(game.inactivePlayer.archive) > 0:
    count = 0
    for x in game.inactivePlayer.archive:
      if x.deck == game.inactivePlayer.name:
        count += 1
    game.activePlayer.amber += count
    print("You gained " + str(count) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
    pendingDisc = game.inactivePlayer.archive
    game.pending(pendingDisc, destroyed = False)

def key143(game, card):
  """ Harland Mindlock: Take control of an enemy flank creature until Harland Mindlock leaves play.
  """
  passFunc(game, card)
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
  passFunc(game, card)
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
    game.pending(pendingDiscard)

    game.activePlayer.discard.append(game.activePlayer.deck.pop())
    if game.activePlayer.discard[-1].house == "Logos":
      logos = False
    
def key149(game, card):
  """ Psychic Bug: Look at your opponent's hand.
  """
  passFunc(game, card)
  
  inhand = game.inactivePlayer.hand

  game.activePlayer.printShort(inhand)

def key152(game, card):
  """ Skippy Timehog: Your opponent canot use any cards next turn.
  """
  passFunc(game, card)
  
  game.inactivePlayer.states["Reap"].update({card.title:True})
  game.inactivePlayer.states["Fight"].update({card.title:True})
  game.inactivePlayer.states["Action"].update({card.title:True})

def key153(game, card):
  """ Timetraveller: Draw two cards.
  """
  passFunc(game, card)
  
  game.activePlayer += 2

def key157(game, card):
  """ Experimental Therapy: Stun and exhaust this creature.
  """
  passFunc(game, card)
  card.stun = True
  card.ready = False

## End house Logos

########
# Mars #
########

###########
# Actions #
###########

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
  passFunc(game, card)
  
  active = game.activePlayer.board["Creature"]
  inactive = game.activePlayer.board["Creature"]
  pendingDisc = []
  
  [x.damageCalc(game, 3) for x in active]
  [x.damageCalc(game, 3) for x in inactive]
  length = len(active)
  [pendingDisc.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].updateHealth()]
  length = len(inactive)
  [pendingDisc.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].updateHealth()]
  game.pending(pendingDisc)

def key161(game, card):
  """ Battle Fleet: Reveal any number of Mars cards from your hand. For each card revealed this way, draw 1 card.
  """
  passFunc(game, card)
  revealed = reveal(game, game.activePlayer.hand)
  game.activePlayer.printShort(revealed)
  game.activePlayer += len(revealed)
  print("You drew " + str(len(revealed)) + " cards.")

def key162(game, card):
  """ Deep Probe: Choose a house: Reveal your opponent's hand. Discard each creature of that house revealed this way.
  """
  passFunc(game, card)
  
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
  passFunc(game, card)
  
  activeC = game.activePlayer.board["Creature"]
  activeA = game.activePlayer.board["Artifact"]
  inactiveC = game.inactivePlayer.board["Creature"]
  inactiveA = game.inactivePlayer.board["Artifact"]
  
  for x in [x for x in (activeC + inactiveC) if x.house == "Mars" or "Robot" in x.traitList]:
    x.stun = True
  pendingDiscard = activeA # fine because Artifacts don't have destroyed effects
  pendingDiscard.extend(inactiveA)
  inactiveA = []
  game.pending(pendingDiscard)
  print(game)

def key164(game, card):
  """ Hypnotic Command: For each friendly Mars creature, choose an enemy creature to capture one from their own side.
  """
  passFunc(game, card)
  
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
  passFunc(game, card)
  
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = [] # fine because only one side

  if game.inactivePlayer.amber >= 6:
    length = len(inactive)
    [x.damageCalc(game, 3) for x in inactive]
    [pendingDisc.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].updateHealth()]

def key166(game, card):
  """ Key Abduction: Return each Mars creature to its owner's hand. Then you may forge a key at +9 current cost, reduced by 1 for each card in your hand.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  length = len(active)
  pending = []
  [pending.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].house == "Mars" and active[abs(x - length + 1)].type == "Creature"]
  length = len(inactive)
  [pending.append(inactive.pop(abs(x - length+ 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].house == "Mars" and inactive[abs(x - length + 1)].type == "Creature"]
  game.pending(pending, 'hand')
  game.activePlayer.keyCost = game.calculateCost()
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
    print("You now have " + str(game.activePlayer.keys) + " keys and " + str(game.activePlayer.amber) + " amber.")

def key167(game, card):
  """ Martian Hounds: Choose a creature. For each damaged creature, give the chosen creature two +1 power counters.
  """
  passFunc(game, card)
  
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
  passFunc(game, card)
  
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
  passFunc(game, card)
  
  inactive = game.inactivePlayer.board["Creature"]
  count = len([x for x in inactive if x.damage > 0])
  if count == 0:
    print("There are no damaged enemy creatures. The card is still played.")
  else:
    again = input("Would you like to archive any enemy creatures [Y/n]?\n>>>").title()
    if again[0] == "N":
      return
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
  passFunc(game, card)
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
  passFunc(game, card)
  
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
      active[choice].damageCalc(game, 2)
      if active[choice].updateHealth():
        pendingDisc.append(active.pop(choice))
        game.pending(pendingDisc)
        count -= 1
        continue
    if side == 1: # enemy
      inactive[choice].damageCalc(game, 2)
      if active[choice].updateHealth():
        pendingDisc.append(active.pop(choice))
        game.pending(pendingDisc)
        count -= 1
        continue
    if side == '':
      break # side will tell them that they are no more targets

def key172(game, card):
  """ Orbital Bombardment: Reveal any number of Mars cards from your hand. For each card revealed this way, deal 2 damage to a creature. (you may choose a different creature each time.)
  """
  passFunc(game, card)
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
      active[choice].damageCalc(game, 2)
      if active[choice].updateHealth():
        pendingDisc.append(active.pop(choice))
        game.pending(pendingDisc)
        count -= 1
        continue
    if side == 1: # enemy
      inactive[choice].damageCalc(game, 2)
      if active[choice].updateHealth():
        pendingDisc.append(active.pop(choice))
        game.pending(pendingDisc)
        count -= 1
        continue
    if side == '':
      break # side will tell them that they are no more targets
  
def key173(game, card):
  """ Phosphorous Stars: Stun each non-Mars creature. Gain 2 chains.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  for x in (active + inactive):
    if x.house != "Mars":
      x.stun = True

  game.activePlayer.chains += 2

def key174(game, card):
  """ Psychic Network: Steal 1 amber for each friendly ready Mars creature.
  """
  passFunc(game, card)
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
  passFunc(game, card)
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

def key176(game, card):
  """ Shatter Storm: Lose all your amber. Then, your opponent loses triple the amount of amber you lost this way.
  """
  passFunc(game, card)
  count = game.activePlayer.amber
  if count == 0:
    print("You have no amber to lose, so your opponent loses no amber. The card is still played.")
    return
  game.activePlayer.amber -= count
  game.inactivePlayer.amber -= (count * 3)
  if game.inactivePlayer.amber < 0:
    game.inactivePlayer.amber = 0

def key177(game, card):
  """ Soft Landing: The next creature or artifact you play this turn enters play ready.
  """
  passFunc(game, card)
  game.activePlayer.states["Play"].update({"Soft Landing":True})

def key178(game, card):
  """ Squawker: Ready a Mars creature or stun a non-Mars creature.
  """
  passFunc(game, card)
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
  passFunc(game, card)
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
  game.pending(pendingHand, 'hand')

def key203(game, card):
  """ Yxili Marauder: Capture 1 amber for each friendly ready Mars creature.
  """
  passFunc(game, card)
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

## End house Mars

###########
# Sanctum #
###########

###########
# Actions #
###########

def key212(game, card):
  """ Begone!: Choose one: destroy each Dis creature, or gain 1 amber.
  """
  passFunc(game, card)
  while True:
    choice = input("Would you like to [D]estroy each Dis creature, or [G]ain 1 amber?").title()
    if choice[0] == "D":
      active = game.activePlayer.board["Creature"]
      inactive = game.inactivePlayer.board["Creature"]
      pending = []
      length = len(active)
      [pending.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].house == "Dis"]
      length = len(inactive)
      [pending.append(inactive.pop(absa(x, length))) for x in range(length) if inactive[absa(x, length)].house == "Dis"]
      game.pending(pending)
      return
    if choice[0] == "G":
      game.activePlayer.amber += 1
      print("You now have " + str(game.activePlayer.amber) + " amber.")
      return
    print("Not a valid input. Try again.")

def key213(game, card):
  """ Blinding Light: Choose a house. Stun each creature of that house.
  """
  passFunc(game, card)
  while True:
    print(game)
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
  passFunc(game, card)
  game.activePlayer.states["Play"].update({card.title:True})

def key215(game, card):
  """ Cleansing Wave: Heal 1 damage from each creature. Gain 1 amber for each creature healed this way.
  """
  passFunc(game, card)
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
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  for x in active:
    if x.stun == True:
      print(x.title + " is no longer stunned.")
      x.stun = False

def key217(game, card):
  """ Doorstep to Heaven: Each player with 6 or more amber is reduced to five amber.
  """
  passFunc(game, card)
  if game.activePlayer.amber >= 6:
    game.activePlayer.amber = 5
  if game.inactivePlayer.amber >= 6:
    game.inactivePlayer.amber = 5

def key218(game, card):
  """ Glorious Few: For each creature your opponent controls in excess of you, gain 1 amber.
  """
  passFunc(game, card)
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
  passFunc(game, card)
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
  passFunc(game, card)
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
    if game.checkFightStates(active[choice]):
      game.fightCard(choice)
    return
  if use[0] == "A":
    if game.checkActionStates:
      active[choice].action(game, active[choice])

def key221(game, card):
  """ Mighty Lance: Deal 3 damage to a creature and 3 damage to a neighbor of that creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  choice, side = chooseSide(game)
  pendingD = []
  
  if side == 0: # friendly
    neigh = active[choice].neighbors(game)
    if neigh == 0:
      print("This card has no neighbors. No extra damage is dealt.")
    elif neigh == 1:
      if choice == 0:
        other = choice + 1
    else:
      while True:
        other = makeChoice("Choose which neighbor to damage: ", active[choice-1:choice+2])
        if other == 1:
          print("You must select a neighbor of that minion. Try again.")
          continue
      if other == 0:
        other = choice - 1
      else:
        other = choice + 1
    active[choice].damageCalc(game, 3)
    active[other].damageCalc(game, 3)
    if choice > other:
      [pendingD.append(active.pop(x)) for x in [choice, other] if active[x].updateHealth()]
    else: 
      [pendingD.append(active.pop(x)) for x in [other, choice] if active[x].updateHealth()]
    game.pending(pendingD)
    return
  if side == 1: # enemy
    neigh = inactive[choice].neighbors(game)
    if neigh == 0:
      print("This card has no neighbors. No extra damage is dealt.")
    elif neigh == 1:
      if choice == 0: other = choice + 1
      else: other = choice - 1
    else:
      while True:
        other = makeChoice("Choose which neighbor to damage: ", inactive[choice-1:choice+2])
        if other == 1:
          print("You must select a neighbor of that minion. Try again.")
          continue
      if other == 0:
        other = choice - 1
      else:
        other = choice + 1
    inactive[choice].damageCalc(game, 3)
    inactive[other].damageCalc(game, 3)
    if choice > other:
      [pendingD.append(inactive.pop(x)) for x in [choice, other] if inactive[x].updateHealth()]
      return
    else:
      [pendingD.append(inactive.pop(x)) for x in [other, choice] if inactive[x].updateHealth()]
    game.pending(pendingD)
    return
  if side == '':
    return # chooseSide will tell the player that the board is empty

def key222(game, card):
  """ Oath of Poverty: Destroy each of your artifacts. Gain 2 amber for each artifact destroyed this way.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  count = len(active)
  pending = []
  if count == 0:
    print("You have no artifacts, so no extra amber is gained. The card is still played.")
    return
  pending = active
  game.pending(pending)
  game.activePlayer.amber += (count * 2)
  print("You destroyed " + str(count) + " artifacts, so you gain " + str(count * 2) + " amber.")

def key223(game, card):
  """ One Stood Against Many: Ready and fight with a friendly creature 3 times, each time against a different enemy creature. Resolve these fights one at a time.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  count = 3
  fought = [] # this should be cards, not indexes, so that if something dies and the index changes we're still good
  pendingD = []
  choice = makeChoice("Choose a friendly creature: ", active)
  
  # need to implement the fighting here so I can track targets
  # that's why I'm not using game.fightCard
  while count > 0 and len(inactive) > 0:
    active[choice].ready = True
    target = makeChoice("Which enemy creature would you like to attack?\n>>>", inactive)
    if inactive[target] in fought:
      print("You can't fight against that minion a second time. Try again.")
      continue
    if not game.checkFightStates(active[choice]):
      return # checkFightStates will explain why
    active[choice].fightCard(inactive[target], game)
    fought.append(inactive[target])
    if inactive[target].updateHealth():
      pendingD.append(inactive.pop(target))
      game.pending(pendingD)
    if active[choice].updateHealth():
      pendingD.append(active.pop(choice))
      game.pending(pendingD)
      print("Your creature died, so the card's effect ends.")
      break
    if active[choice].fight:
      active[choice].fight(game, active[choice])
    count -= 1
  if len(inactive) == 0:
    print("Your opponent has no more creatures for you to fight.")

def key224(game, card):
  """ Radiant Truth: Stun each enemy creature not on a flank.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  for x in inactive[1:-1]:
    x.stun = True

def key225(game, card):
  """ Shield of Justice: For the remainder of the turn, each friendly creature cannot be dealt damage.
  """
  passFunc(game, card)
  # create a state that is checked in damageCalc. which means damage calc needs more inputs
  game.activePlayer.states["Fight"].update({"Shield of Justice":True})

def key226(game, card):
  """ Take Hostages: For the remainder of the turn, each time a friendly creature fights, it captures 1 amber.
  """
  passFunc(game, card)
  # creates a state to be checked in checkFightStates
  if not game.activePlayer.states["Fight"][card.title][0]:
    game.activePlayer.states["Fight"].update({card.title:[True]})
  else:
    game.activePlayer.states["Fight"][card.title].append(True)
  # should be able to account for multiple instances of the card

def key227(game, card):
  """ Terms of Redress: Choose a friendly creature to capture 2.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  choice = makeChoice("Choose a friendly creature to capture two amber: ", active)
  active[choice].capture(2)

def key228(game, card):
  """ The Harder They Come: Purge a creature with power 5 or higher.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  purgableA = [x for x in active if x.power + x.extraPow >= 5]
  purgableI = [x for x in inactive if x.power + x.extraPow >= 5]
  pending = []
  if len(purgableA) == 0 and len(purgableI) == 0:
    print("There are no valid targets. The card is still played.")
  elif len(purgableA) == 0: # so inactive has targets
    if len(purgableI) == 1:
      pending.append(inactive.pop(inactive.index(purgableI[0])))
      print("You purged your opponent's " + pending[0].title + ".")
    else:
      choice = makeChoice("Choose an enemy creature with 5 or more power to purge: ", purgableI)
      pending.append(inactive.pop(inactive.index(purgableI[choice])))
      print("You purged your opponent's " + pending[0].title + ".")
  elif len(purgableI) == 0: # so active has targets
    if len(purgableA) == 1:
      pending.append(active.pop(active.index(purgableA[0])))
      print("You purged your " + pending[0].title + ".")
    else:
      choice = makeChoice("Choose a friendly creature with 5 or more power to purge: ", purgableA)
      pending.append(active.pop(active.index(purgableA[choice])))
      print("You purged your " + pending[0].title + ".")
  else: # both have something
    side = ''
    while side[0] != "F" and side[0] != "E":
      side = input("Would you like to target an [E]nemy creature or a [F]riendly creature?").title()
    if side[0] == "F":
      choice = makeChoice("Choose a friendly creature with 5 or more power to purge: ", purgableA)
      pending.append(active.pop(active.index(purgableA[choice])))
      print("You purged your " + pending[0].title + ".")
    elif side[0] == "E":
      choice = makeChoice("Choose an enemy creature with 5 or more power to purge: ", purgableI)
      pending.append(inactive.pop(inactive.index(purgableI[choice])))
      print("You purged your opponent's " + pending[0].title + ".")
  game.pending(pending, 'purge')

def key229(game, card):
  """ The Spirit's Way: Destroy each creature with power 3 or higher.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingD = []
  length = len(active)
  [pendingD.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].power >= 3]
  length = len(inactive)
  [pendingD.append(inactive.pop(absa(x, length))) for x in range(length) if inactive[absa(x, length)].power >= 3]
  game.pending(pendingD)

def key231(game, card):
  """ Epic Quest: Archive each friendly Knight creature in play.
  """
  passFunc(game, card)
  archive = game.activePlayer.archive
  active = game.activePlayer.board["Creature"]
  length = len(active)
  [archive.append(active.pop(absa(x, length))) for x in range(length) if "Knight" in active[absa(x, length)].traitList]

def key246(game, card):
  """ Horseman of Death: Return each Horseman creature from your discard pile to your hand.
  """
  passFunc(game, card)
  discard = game.activePlayer.discard
  hand = game.activePlayer.hand
  length = len(discard)
  [hand.append(discard.pop(absa(x, length))) for x in range(length) if "Horseman" in discard[absa(x, length)].traitList]

def key247(game, card):
  """ Horseman of Famine: Destroy the least powerful creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  powers = [x.power for x in (active + inactive)]
  low = min(powers)
  options = []
  pendingD = []
  for x in (active + inactive):
    if x.power == low:
      try: options.append((x, active.index(x)))
      except: options.append((x, inactive.index(x)))
  # having zero options is impossible, even if played on an empty board it will have to target itself
  if len(options) == 1:
    try: pendingD.append(active.pop(options[0][1]))
    except: pendingD.append(inactive.pop(options[0][1]))
    return
  choice = ("Some creatures are tied for the lowest power. Choose which one to destroy.", [x[0] for x in options])
  try: 
    pendingD.append(active.pop(choice[1]))
  except: 
    pendingD.append(inactive.pop(choice[1]))
  game.pending(pendingD)

def key248(game, card):
  """ Horseman of Pestilence: Deal 1 damage to each non-Horseman creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  for x in (active + inactive):
    if "Horseman" not in x.traitList:
      x.damageCalc(game, 1)
  length = len(active)
  [pending.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].updateHealth()]
  length = len(inactive)
  [pending.append(inactive.pop(absa(x, length))) for x in range(length) if inactive[absa(x, length)].updateHealth()]
  game.pending(pending)

def key249(game, card):
  """ Horseman of War: For the remainder of the turn, each friendly creature can be used as if they were in the active house, but can only fight.
  """
  passFunc(game, card)
  game.extraFightHouses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]

def key251(game, card):
  """ Lady Maxena: Stun a creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  choice, side = chooseSide(game)
  if side == 0:
    game.activePlayer.printShort(activeBoard)
    activeBoard[choice].stun = True
  else:
    game.inactivePlayer.printShort(inactiveBoard)
    inactiveBoard[choice].stun = True

def key253(game, card):
  """ Numquid the Fair: Destroy an enemy creature. Repeat this card's effect if your opponent still controls more creatures than you.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pending = []

  def helper(game, card, inactiveBoard, pending):
    """ Destroy an enemy creature.
    """
    choice = makeChoice("Choose an enemy creature to destroy: ", inactiveBoard)
    pending.append(inactiveBoard.pop(choice))
    game.pending(pending)
  
  helper(game, card, inactiveBoard, pending)
  # possible edge case: Numquid hits enemy w/ Phoenix Heart. Numquid then dies and the effect should not repeat.
  while len(inactiveBoard) > len(activeBoard) and card in activeBoard:
    helper(game, card, inactiveBoard, pending)

def key255(game, card):
  """ Raiding Knight: Capture 1 amber.
  """
  passFunc(game, card)
  card.capture(game, 1)

def key258(game, card):
  """ Sergeant Zakiel: You may ready and fight with a neighboring creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]

  if len(activeBoard) == 1:
    return

  if activeBoard.index(card) == 0:
    maybe = input("Would you like to ready and fight with " + str(activeBoard[1]) + " [Y/n]?").title()
    if maybe[0] != "N":
      activeBoard[1].ready = True
      game.fightCard(1)
    return
  elif activeBoard.index(card) == len(activeBoard)-1:
    maybe = input("Would you like to ready and fight with " + str(activeBoard[(len(activeBoard)-2)]) + " [Y/n]?").title()
    if maybe[0] != "N":
      activeBoard[(len(activeBoard)-2)].ready = True
      game.fightCard(len(activeBoard)-2)
    return

def key260(game, card):
  """ Gatekeeper: If your opponent has 7 or more amber, capture all but 5 of it.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber >= 7:
    diff = game.inactivePlayer.amber - 5
  card.capture(game, diff)
  print(card.title + " captured " + str(card.captured) + " amber.")

def key262(game, card):
  """ Veemos Lightbringer: Destroy each elusive creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  length = len(active)
  [pending.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].elusive]
  length = len(inactive)
  [pending.append(inactive.pop(absa(x, length))) for x in range(length) if inactive[absa(x, length)].elusive]

## End house Sanctum

###########
# Shadows #
###########

###########
# Actions #
###########

def key267(game, card):
  """ Bait and Switch: If your opponent has more amber than you, steal 1. Repeat the preceding effect if your opponent still has more amber than you.
  """
  passFunc(game, card)
  count = 2
  while count > 0:
    if game.inactivePlayer.amber > game.activePlayer.amber:
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You steal 1 amber. You now have " + str(game.activePlayer.amber) + " amber.")
      count -= 1
    else:
      break

def key268(game, card):
  """ Booby Trap: Deal 4 damage to a creature that is not on a flank with 2 splash.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  # first check that there are flank creatures to target
  side = ''
  if len(active) <= 2 and len(inactive) <= 2:
    print("There are no creatures not on a flank to target. The card is still played.")
    return
  elif len(inactive) <= 2:
    game.activePlayer.printShort(active, True)
    side = 0
    choice = makeChoice("There are no enemy creatures to target, so you must choose a friendly creature to target: ", active[1:-1])
  else:
    while side[0] != "F" and side[0] != "E":
      side = input("Would you like to target an [E]nemy creature or a [F]riendly creature?").title()
    if side[0] == "F":
      game.activePlayer.printShort(active[1:-1], True)
      side = 0
      choice = makeChoice("Choose a target: ", active[1:-1]) + 1
    elif side[0] == "E":
      game.activePlayer.printShort(inactive[1:-1], True)
      side = 1
      choice = makeChoice("Choose a target: ", inactive[1:-1]) + 1

  if side == 0: # friendly side
    active[choice].damageCalc(game, 4)
    # guaranteed to have two neighbors if can be targeted
    active[choice + 1].damageCalc(game, 2)
    active[choice - 1].damageCalc(game, 2)
    [pending.append(active.pop(x)) for x in [choice + 1, choice, choice - 1] if active[x].updateHealth()]
  elif side == 1:
    inactive[choice].damageCalc(game, 4)
    # guaranteed to have two neighbors if can be targeted
    inactive[choice + 1].damageCalc(game, 2)
    inactive[choice - 1].damageCalc(game, 2)
    [pending.append(inactive.pop(x)) for x in [choice + 1, choice, choice - 1] if inactive[x].updateHealth()]
  game.pending(pending)

def key269(game, card):
  """ Finishing Blow: Destroy a damaged creature. If you do, steal 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  damagedA = [(x.title, active.index(x)) for x in active if x.damage > 0]
  damagedI = [(x.title, inactive.index(x)) for x in inactive if x.damage > 0]
  if len(damagedA + damagedI) == 0:
    print("There are no damaged creatures to target. The card is still played.")
    return
  # else: another modified version of chooseSide
  if len(damagedI) == 0: # so damagedA does have something
    if len(damagedA) == 1:
      pending.append(active.pop(damagedA[0][1]))
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You destroyed your damaged " + pending[0].title + " and stole 1 amber. You now have " + game.activePlayer.amber + " amber.")
    else:
      choice = makeChoice("Choose a damaged friendly creature to destroy: ", [x[0] for x in damagedA])
      pending.append(active.pop(damagedA[choice][1]))
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You destroyed your damaged " + pending[0].title + " and stole 1 amber. You now have " + game.activePlayer.amber + " amber.")
  elif len(damagedA) == 0: # so damagedI does have something
    if len(damagedI) == 1:
      pending.append(inactive.pop(damagedI[0][1]))
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You destroyed your opponent's damaged " + pending[0].title + " and stole 1 amber. You now have " + game.activePlayer.amber + " amber.")
    else:
      choice = makeChoice("Choose a damaged enemy creature to destroy: ", [x[0] for x in damagedI])
      pending.append(inactive.pop(damagedI[choice][1]))
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You destroyed your opponent's damaged " + pending[0].title + " and stole 1 amber. You now have " + game.activePlayer.amber + " amber.")
  else: # both have something
    side = ''
    while side[0] != "F" and side[0] != "E":
      side = input("Would you like to target an [E]nemy creature or a [F]riendly creature?").title()
    if side[0] == "F":
      choice = makeChoice("Choose a damaged friendly creature to destroy: ", [x[0] for x in damagedA])
      pending.append(active.pop(damagedA[choice][1]))
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You destroyed your damaged " + pending[0].title + " and stole 1 amber. You now have " + game.activePlayer.amber + " amber.")
    elif side[0] == "E":
      choice = makeChoice("Choose a damaged enemy creature to destroy: ", [x[0] for x in damagedI])
      pending.append(inactive.pop(damagedI[choice][1]))
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      print("You destroyed your opponent's damaged " + pending[0].title + " and stole 1 amber. You now have " + game.activePlayer.amber + " amber.")
  game.pending(pending)

def key270(game, card):
  """ Ghostly Hand: If your opponent has exactly 1 amber, steal it.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber == 1:
    stealAmber(game.activePlayer, game.inactivePlayer, 1)
    print("You stole your opponent's only amber, you jerk. You now have " + str(game.activePlayer.amber) + " amber.")
    return
  print("Your opponent has " + str(game.inactivePlayer.amber) + "amber. You steal nothing.")

def key271(game, card):
  """ Hidden Stash: Archive a card.
  """
  passFunc(game, card)
  archive = makeChoice("Choose a card from hand to archive: ", game.activePlayer.hand)
  game.activePlayer.archive.append(game.activePlayer.hand.pop(archive))
  print(archive[-1].title + " archived! Type 'Archive' to view your archive.")

def key272(game, card):
  """ Imperial Traitor: Look at your opponent's hand. You may choose and purge a Sanctum card in it.
  """
  passFunc(game, card)
  # check for Sanctum card in opp hand
  pending = []
  game.activePlayer.printShort(game.inactivePlayer.hand)
  if "Sanctum" in [x.house for x in game.inactivePlayer.hand]:
    choice = makeChoice("Choose a Sanctum card from your opponent's hand and purge it: ", game.inactivePlayer.hand)
    pending.append(game.inactivePlayer.hand.pop(choice))
    game.pending(pending, 'purge', destroyed = False)
    return
  print("Your opponent had no Sanctum cards in hand, so you don't get to purge anything.")

def key273(game, card):
  """ Key of Darkness: Forge a key at +6 current cost. If your opponent has no amber, forge a key at +2 current cost instead.
  """
  passFunc(game, card)
  # whenever we forge a key, we calculate key cost
  # this will be a function in Game
  game.activePlayer.keyCost = game.calculateCost()
  var = 6
  if game.inactivePlayer.amber == 0:
    var = 2
  if game.activePlayer.amber >= (game.activePlayer.keyCost + var):
    print("You forge a key for " + str(game.activePlayer.keyCost + var) + " amber.")
    game.activePlayer.amber -= (game.activePlayer.keyCost + var)
    game.activePlayer.keys += 1
    if game.activePlayer.keys >= 3:
      game.endBool = False # This will make the game end.
      return
    print("You now have " + str(game.activePlayer.keys) + " keys and " + str(game.activePlayer.amber) + " amber.")

def key274(game, card):
  """ Lights Out: Return 2 enemy creature's to their owner's hand.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  count = 2
  while count > 0 and len(inactive) > 0:
    choice = makeChoice("Choose an enemy creature to return to your opponent's hand: ", inactive)
    pending.append(inactive.pop(choice))
    count -= 1
  game.pending(pending, 'hand')

def key275(game, card):
  """ Miamsa: Your opponent skips the "forge a key" step on their next turn.
  """
  passFunc(game, card)
  game.inactivePlayer.states["Forge"].update({card.title:True})

def key276(game, card):
  """ Nerve Blast: Steal 1 amber. If you do, deal 2 damage to a creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  orig = game.activePlayer.amber
  stealAmber(game.activePlayer, game.inactivePlayer, 1)
  if game.activePlayer.amber > orig:
    print("You now have " + game.activePlayer.amber + " amber. Now, deal 2 damage to a creature.")
    choice, side = chooseSide(game)
  else:
    print("You didn't steal any amber, so you don't deal any damage. The card is still played.")
    return
  if side == 0: #friendly
    active[choice].damageCalc(game, 2)
    if active[choice].updateHealth():
      pending.append(active.pop(choice))
  if side == 1: #enemy
    inactive[choice].damageCalc(game, 2)
    if inactive[choice].updateHealth():
      pending.append(inactive.pop(choice))
  game.pending(pending)

def key277(game, card):
  """ One Last Job: Purge each friendly Shadows creature. Steal 1 amber for each creature purged this way.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  pending = []
  length = len(active)
  [pending.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].house == "Shadows"]
  if len(pending) > 0:
    game.activePlayer.amber += len(pending)
    print("You gain " + str(len(pending)) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
    game.pending(pending, 'purge')
    return
  print("You had no friendly Shadows creatures in play. You gain no extra amber. The card is still played.")

def key278(game, card):
  """ Oubliette: Purge a creature with power 3 or lower.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  purgableA = [x for x in active if x.power + x.extraPow <= 3]
  purgableI = [x for x in inactive if x.power + x.extraPow <= 3]
  pending = []
  if len(purgableA) == 0 and len(purgableI) == 0:
    print("There are no valid targets. The card is still played.")
  elif len(purgableA) == 0: # so inactive has targets
    if len(purgableI) == 1:
      pending.append(inactive.pop(inactive.index(purgableI[0])))
      print("You purged your opponent's " + pending[0].title + ".")
    else:
      choice = makeChoice("Choose an enemy creature with 3 or less power to purge: ", purgableI)
      pending.append(inactive.pop(inactive.index(purgableI[choice])))
      print("You purged your opponent's " + pending[0].title + ".")
  elif len(purgableI) == 0: # so active has targets
    if len(purgableA) == 1:
      pending.append(active.pop(active.index(purgableA[0])))
      print("You purged your " + pending[0].title + ".")
    else:
      choice = makeChoice("Choose a friendly creature with 3 or less power to purge: ", purgableA)
      pending.append(active.pop(active.index(purgableA[choice])))
      print("You purged your " + pending[0].title + ".")
  else: # both have something
    side = ''
    while side[0] != "F" and side[0] != "E":
      side = input("Would you like to target an [E]nemy creature or a [F]riendly creature?").title()
    if side[0] == "F":
      choice = makeChoice("Choose a friendly creature with 3 or less power to purge: ", purgableA)
      pending.append(active.pop(active.index(purgableA[choice])))
      print("You purged your " + pending[0].title + ".")
    elif side[0] == "E":
      choice = makeChoice("Choose an enemy creature with 3 or less power to purge: ", purgableI)
      pending.append(inactive.pop(inactive.index(purgableI[choice])))
      print("You purged your opponent's " + pending[0].title + ".")
  game.pending(pending, 'purge')

def key279(game, card):
  """ Pawn Sacrifice: Sacrifice a friendly creature. If you do, deal 3 damage each to 2 creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []

  if len(active) == 0:
    print("You have no creatures to sacrifice. No damage is dealt, but the card is still played.")
    return
  choice = makeChoice("Choose a friendly creature to sacrifice: ", active)
  pending.append(active.pop(choice))
  print("You sacrificed " + pending[0].title + ". Now, choose two targets to deal three damage to.")
  game.pending(pending)

  if len(active) + len(inactive) == 0:
    print("There are no creatures to damage.")
    return
  count = 2
  while count > 0 and (len(active) + len(inactive)) > 0:
    choice, side = chooseSide(game)
    if side == 0: #friendly
      active[choice].damageCalc(game, 3)
      if active[choice].updateHealth():
        pending.append(active.pop(choice))
    if side == 1: #enemy
      inactive[choice].damageCalc(game, 3)
      if inactive[choice].updateHealth():
        pending.append(inactive.pop(choice))
    count -= 1
  game.pending(pending)

def key280(game, card):
  """ Poison Wave: Deal 2 damage to each creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.activePlayer.board["Creature"]
  pendingDisc = []
  
  [x.damageCalc(game, 2) for x in active]
  [x.damageCalc(game, 2) for x in inactive]
  length = len(active)
  [pendingDisc.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].updateHealth()]
  length = len(inactive)
  [pendingDisc.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].updateHealth()]
  game.pending(pendingDisc)

def key281(game, card):
  """ Relentless Whispers: Deal 2 damage to a creature. If this damage destroys that creature, steal 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []

  if len(active) + len(inactive) == 0:
    return

  print("Choose a creature to deal 2 damage to:")
  choice, side = chooseSide(game)

  if side == 0: #friendly
    active[choice].damageCalc(game, 2)
    if active[choice].updateHealth():
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      pending.append(active.pop(choice))
  if side == 1: #enemy
    inactive[choice].damageCalc(game, 2)
    if inactive[choice].updateHealth():
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      pending.append(inactive.pop(choice))
  game.pending(pending)

def key282(game, card):
  """ Routine Job: Steal 1 amber. Then, steal 1 amber for each copy of Routine Job in your discard pile.
  """
  passFunc(game, card)
  stealAmber(game.activePlayer, game.inactivePlayer, 1)
  count = len([x for x in game.activePlayer.discard if x.title == card.title])
  if count > 0:
    stealAmber(game.activePlayer, game.inactivePlayer, count)

def key283(game, card):
  """ Too Much to Protect: Steal all but 6 of your opponent's amber.
  """
  passFunc(game, card)
  diff = 0
  if game.inactivePlayer.amber > 6:
    diff = game.inactivePlayer.amber - 6
    stealAmber(game.activePlayer, game.inactivePlayer, diff)
    return
  print("Your opponent had 6 or less amber, so you stole nothing.")

def key284(game, card):
  """ Treasure Map: If you have not played any other cards this turn, gain 3 amber. For the remainder of the turn, you cannot play cards.
  """
  passFunc(game, card)
  # game.numPlays is incremented before a card's action is called
  if game.numPlays - 1 == 0:
    game.activePlayer.amber += 3
    print("You gained 3 amber. You now have " + str(game.activePlayer.amber) + " amber.")
  game.activePlayer.states["Play"].update({card.title:True})

def key288(game, card):
  """ Masterplan: Put a card from your hand facedown beneath Masterplan.
  """
  passFunc(game, card)
  hand = game.activePlayer.hand
  game.activePlayer.board["Masterplan"] = []
  plan = game.activePlayer.board["Masterplan"]
  choice = makeChoice("Choose a card to put under Masterplan: ", hand)
  plan.append(hand.pop(choice))

def key303(game, card):
  """ Magda the Rat: Steal 2 amber.
  """
  passFunc(game, card)
  stealAmber(game.activePlayer, game.inactivePlayer, 2)

def key307(game, card):
  """ Old Bruno: Capture 3 amber.
  """
  passFunc(game, card)
  card.capture(game, 3)

def key313(game, card):
  """ Sneklifter: Take control of an enemy artifact. While under your control, if it does not belong to one of your three houses, it is considered to be of house Shadows.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]

  if len(inactive) == 0:
    print("Your opponent has no artifacts for you to steal.")
    return
  choice = makeChoice("Choose an enemy artifact to steal: ", inactive)
  if inactive[choice].house not in game.activePlayer.houses:
    inactive[choice].house = "Shadows"
  active.append(inactive.pop(choice))

def key315(game, card):
  """ Urchin: Steal 1 amber.
  """
  passFunc(game, card)
  stealAmber(game.activePlayer, game.inactivePlayer, 1)

## End house Shadows

###########
# Untamed #
###########

###########
# Actions #
###########

def key319(game, card):
  """ Cooperative Hunting: Deal 1 damage for each friendly creature in play. You may divide this damage among any number of creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  count = len(active)
  while count > 0:
    choice, side = chooseSide(game)
    if side == 0: # friendly
      if active[choice].health() > count:
        damage = makeChoice("How much damage would you like to deal to this creature?", list(range(1, count + 2)))
      else:
        damage = makeChoice("How much damage would you like to deal to this creature?", list(range(1, active[choice].health() + 2)))
      active[choice].damageCalc(game, damage)
      if active[choice].updateHealth():
        pending.append(active.pop(choice))
        game.pending(pending)
        count -= 1
        continue
    if side == 1: # enemy
      if inactive[choice].health() > count:
        damage = makeChoice("How much damage would you like to deal to this creature?", list(range(1, count + 2)), show = False)
      else:
        damage = makeChoice("How much damage would you like to deal to this creature?", list(range(1, inactive[choice].health() + 2)), show = False)
      inactive[choice].damageCalc(game, damage)
      if inactive[choice].updateHealth():
        pending.append(inactive.pop(choice))
        game.pending(pending)
        count -= 1
        continue
    if side == '':
      break # side will tell them that they are no more targets

def key320(game, card):
  """ Curiosity: Destroy each Scientist creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  length = len(active)
  [pending.append(active.pop(absa(x, length))) for x in range(length) if "Scientist" in active[absa(x, length)].traitList]
  length = len(inactive)
  [pending.append(inactive.pop(absa(x, length))) for x in range(length) if "Scientist" in inactive[absa(x, length)].traitList]
  game.pending(pending)

def key321(game, card):
  """ Fertility Chant: Your opponent gains 2 amber.
  """
  passFunc(game, card)
  game.inactivePlayer.amber += 2
  print("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def key322(game, card):
  """ Fogbank: Your opponent cannot use creatures to fight on their next turn.
  """
  passFunc(game, card)
  # states should always be in deck that they affect
  game.inactivePlayer.states["Fight"].update({card.title:True})

def key323(game, card):
  """ Full Moon: For the remainder of the turn, gain 1 amber each time you play a creature.
  """
  passFunc(game, card)
  if not game.activePlayer.states["Play"][card.title][0]:
    game.activePlayer.states["Play"].update({card.title:[True]})
  else:
    game.activePlayer.states["Play"][card.title].append(True)
  # should be able to account for multiple instances of full 
  
def key324(game, card):
  """ Grasping Vines: Return up to 3 artifacts to their owners' hands.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]
  pending = []
  count = 3
  again = input("Would you like to return any artifacts to their owners' hands [Y/n]?\n>>>").title()
  if again[0] == "N":
    return
  while count > 0:
    print("Choose an artifact to return to its owner's hand: ")
    choice, side = chooseSide(game, stringy = "Artifact")
    if side == 0: # friendly
      pending.append(active.pop(choice))
      game.pending(pending, 'hand')
      count -= 1
    elif side == 1: # enemy
      pending.append(inactive.pop(choice))
      game.pending(pending, 'hand')
      count -= 1
    else:
      return # choose side will inform you that the board is empty
    if count > 0:
      again = input("Would you like to return another artifact to its owner's hand [Y/n]?\n>>>").title()
      if again[0] == "N":
        return

def key325(game, card):
  """ Key Charge: Lost 1 amber. If you do, you may forge a key at current cost.
  """
  passFunc(game, card)
  game.activePlayer.amber -= 1
  game.activePlayer.keyCost = game.calculateCost()
  if game.activePlayer.amber >= game.activePlayer.keyCost:
    forge = input("Would you like to forge a key for " + str(game.activePlayer.keyCost) + " amber [Y/n]?\n>>>").title()
    if forge == '':
      forge = "Y"
    if forge[0] != 'N':
      print("Key forged!")
      game.activePlayer.keys += 1
      game.activePlayer.amber -= game.activePlayer.keyCost
      if game.activePlayer.keys >= 3:
        game.endBool = False
        return
      print("You now have " + str(game.activePlayer.keys) + " keys and " + str(game.activePlayer.amber) + " amber.")

def key326(game, card):
  """ Lifeweb: If your opponent played 3 or more creatures on their previous turn, steal 2 amber.
  """
  passFunc(game, card)
  # implement tracking how many creatures opponent played last turn
  # if a deck has lifeweb in it, it will set Lifeweb in states to [True, 0]. Whenever the opponent plays a creature, it will be incremented.
  if game.activePlayer.states["Play"][card.title] >= 3:
    stealAmber(game.activePlayer, game.inactivePlayer, 2)
    print("Your opponent played enough creatures last turn, so you stole 2 amber.")
    return
  print("Your opponent did not play enough creatures last turn, so you steal no amber. The card is still played.")

def key327(game, card):
  """ Lost in the Woods: Choose 2 friendly creatures and 2 enemy creatures. Shuffle each chosen creature into its owner's deck.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  if len(active) <= 2:
    print("Shuffling all friendly creatures into owners' decks.")
    pending.extend(active)
    game.pending(pending, 'deck', False)
  else:
    count = 2
    while count > 0:
      choice = makeChoice("Choose a friendly creature to shuffle into its owner's deck: ", active)
      pending.append(active.pop(choice))
      count -= 1
    game.pending(pending, 'deck', False)
  if len(inactive) <= 2:
    print("Shuffling all enemy creatures into owners' decks.")
    pending.extend(inactive)
    game.pending(pending, 'deck', False)
  else:
    count = 2
    while count > 0:
      choice = makeChoice("Choose an enemy creature to shuffle into its owner's deck: ", inactive)
      pending.append(inactive.pop(choice))
      count -= 1
    game.pending(pending, 'deck', False)
  
  random.shuffle(game.activePlayer.deck)
  random.shuffle(game.inactivePlayer.deck)

def key328(game, card):
  """ Mimicry: When you play this card, treat it as a copy of an action card in your opponent's discard pile.
  """
  passFunc(game, card)
  options = [(x, game.inactivePlayer.discard.index(x)) for x in range(len(game.inactivePlayer.discard)) if x.type == "Action"]
  choice = makeChoice("Choose an action card to copy: ", [x[0] for x in options])
  print(game.inactivePlayer.discard[options[choice][1]].text)
  game.inactivePlayer.discard[options[choice][1]].play(game, game.inactivePlayer.discard[options[choice][1]])

def key329(game, card):
  """ Nature's Call: Return up to 3 creatures to their owners' hands.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  count = 3
  again = input("Would you like to return any creatures to their owners' hands [Y/n]?\n>>>").title()
  if again[0] == "N":
    return
  while count > 0:
    print("Choose a creature to return to its owner's hand: ")
    choice, side = chooseSide(game)
    if side == 0: # friendly
      pending.append(active.pop(choice))
      game.pending(pending, 'hand')
      count -= 1
    elif side == 1: # enemy
      pending.append(inactive.pop(choice))
      game.pending(pending, 'hand')
      count -= 1
    else:
      return # choose side will inform you that the board is empty
    if count > 0:
      again = input("Would you like to return another creature to its owner's hand [Y/n]?\n>>>").title()
      if again[0] == "N":
        return

def key330(game, card):
  """ Nocturnal Maneuver: Exhaust up to 3 creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  count = 3
  again = input("Would you like to exhaust any creatures [Y/n]?\n>>>").title()
  if again[0] == "N":
    return
  while count > 0:
    print("Choose a creature to exhaust: ")
    choice, side = chooseSide(game)
    if side == 0: # friendly
      active[choice].ready = False
      count -= 1
    elif side == 1: # enemy
      inactive[choice].ready = False
      count -= 1
    else:
      return # choose side will inform you that the board is empty
    if count > 0:
      again = input("Would you like to exhaust another creature [Y/n]?\n>>>").title()
      if again[0] == "N":
        return

def key331(game, card):
  """ Perilous Wild: Destroy each elusive creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  length = len(active)
  [pending.append(active.pop(absa(x, length))) for x in range(length) if active[absa(x, length)].elusive]
  length = len(inactive)
  [pending.append(inactive.pop(absa(x, length))) for x in range(length) if inactive[absa(x, length)].elusive]

def key332(game, card):
  """ Regrowth: Return a creature from your discard pile to your hand.
  """
  passFunc(game, card)
  active = game.activePlayer.discard
  options = [(x, active.index(x)) for x in range(len(active)) if x.type == "Creature"]
  choice = makeChoice("Choose a creature to return to your hand: ", [x[0] for x in options])
  # I can skip pending b/c this card is guaranteed to belong to the active player
  game.activePlayer.hand.append(active[options[choice][1]])

def key333(game, card):
  """ Save the Pack: Destroy each damaged creature. Gain 1 chain.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  length = len(activeBoard)
  # active player
  damageList = [x.damage for x in activeBoard if x.damage > 0]
  # easy case: everything damaged
  if len(damageList) == len(activeBoard): pendingDiscard = activeBoard
  else:
    [pendingDiscard.append(activeBoard.pop(abs(x - length + 1))) for x in range(len(activeBoard)) if activeBoard[abs(x - length + 1)].damage > 0]
  length = len(inactiveBoard)
  # inactive player
  damageList = [x.damage for x in inactiveBoard if x.damage > 0]
  # easy case: everything damaged
  if len(damageList) == len(inactiveBoard): 
    pendingDiscard.extend(inactiveBoard)
    inactiveBoard = []
  else:
    [pendingDiscard.append(inactiveBoard.pop(abs(x - length + 1))) for x in range(len(inactiveBoard)) if inactiveBoard[abs(x - length + 1)].damage > 0]
  
  game.pending(pendingDiscard)

  game.activePlayer.chains += 1

def key334(game, card):
  """ Scout: For the remainder of the turn, up to 2 friendly creatures gain skirmish. Then, fight with those creatures one at a time.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  count = 2
  choices = []
  again = input("Would you like to give any creatures skirmish [Y/n]?\n>>>").title()
  if again[0] == "N":
    return
  while count > 0:
    choice = makeChoice("Choose a creature to gain skirmish: ", active)
    if choice in choices:
      print("You already chose that minion. Try again.")
      continue
    active[choice].skirmish = True
    choices.append(choice)
    count -= 1
    if count > 0:
      again = input("Would you like to give another creature skirmish [Y/n]?\n>>>").title()
      if again[0] == "N":
        break
  game.activePlayer.states["Fight"][card.title] = [active[x] for x in choices]
  [game.fightCard(x) for x in choices]
  # I need to find a way to make sure these cards lose skirmish at the end of the turn, but not sooner, so I can't make them lose skirmish here
  # perhaps use states? store the cards I gave skirmish to, and at end of turn check

def key335(game, card):
  """ Stampede: If you used 3 or more creatures this turn, steal 2 amber.
  """
  passFunc(game, card)
  if game.activePlayer.states["Action"][card.title] >= 3:
    print("You have used at least 3 creatures this turn, so you steal 2 amber.")
    stealAmber(game.activePlayer, game.inactivePlayer, 2)
    return
  print("You have used less than 3 creatures this turn, so you steal no amber. The card is still played.")

def key336(game, card):
  """ The Common Cold: Deal 1 damage to each creature. You may destroy all Mars creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = []
  # deal 1 damage to everything
  # active
  length = len(active)
  [x.damageCalc(game, 1) for x in active]
  [pendingDiscard.append(active.pop(abs(x - length + 1))) for x in active if active[abs(x - length + 1)].updateHealth()]
  # inactive
  length = len(inactive)
  [x.damageCalc(game, 1) for x in inactive]
  [pendingDiscard.append(inactive.pop(abs(x - length + 1))) for x in inactive if inactive[abs(x - length + 1)].updateHealth()]
  game.pending(pendingDiscard)
  # optional destroy Mars creatures
  marsA = [active.index(x) for x in active if x.house == "Mars"]
  marsA.sort(reverse = True)
  marsI = [inactive.index(x) for x in inactive if x.house == "Mars"]
  marsI.sort(reverse = True)
  if len(marsA) == 0 and len(marsI) == 0:
    print("There are no Mars creatures to destroy")
    return
  elif len(marsA) == 0: # so marsI has something
    print("Enemy creatures:")
    game.activePlayer.printShort(inactive)
    choice = input("You have no Mars creatures. Would you like destroy all Mars creatures [Y/n]?\n>>>").title()
    if choice[0] == "N":
      return
    else:
      [pendingDiscard.append(inactive.pop(x)) for x in marsI]
  elif len(marsI) == 0:
    print("Friendly creatures:")
    game.activePlayer.printShort(active)
    choice = input("Your opponent has no Mars creatures. Would you like destroy all Mars creatures [y/N]?\n>>>").title()
    if choice[0] == "Y":
      [pendingDiscard.append(active.pop(x)) for x in marsA]
    else:
      return
  else:
    print("Enemy creatures:")
    game.activePlayer.printShort(inactive)
    print("Friendly creatures:")
    game.activePlayer.printShort(active)
    choice = input("Would you like destroy all Mars creatures [y/N]?\n>>>").title()
    if choice[0] == "Y":
      [pendingDiscard.append(active.pop(x)) for x in marsA]
      [pendingDiscard.append(inactive.pop(x)) for x in marsI]
    else:
      return
  game.pending(pendingDiscard)

def key337(game, card):
  """ Troop Call: Return each friendly Niffle creature from your discard pile and from play to your hand.
  """
  passFunc(game, card)
  disc = game.activePlayer.discard
  active = game.activePlayer.board["Creature"]
  pending = []
  length = len(disc)
  for x in range(length):
    if "Niffle" in disc[absa(x, length)].traitList:
      pending.append(disc.pop(absa(x, length)))
  length = len(active)
  for x in range(length):
    if "Niffle" in active[absa(x, length)].traitList:
      pending.append(disc.pop(absa(x, length)))
  game.pending(pending, 'hand')
  game.activePlayer.hand.sort(key = lambda x: x.house)

def key338(game, card):
  """ Vigor: Heal up to 3 damage from a creature. If you healed 3 damage, gain 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  damage = reduce(lambda x,y: x + y, [x.damage for x in (active + inactive)])
  if damage > 3:
    count = 3
  else:
    count = damage
  if count == 0:
    print("There are no damaged creatures. The card is still played.")
  again = input("Would you like to heal any damage[Y/n]?\n>>>").title()
  if again[0] == "N":
    return
  print("Choose a creature to heal:")
  choice, side = chooseSide(game)
  if side == 0: # friendly
    while count > 0 and active[choice].damage > 0:
      active[choice].damage -= 1
      count -= 1
      if count > 0:
        again = input("Would you like to heal another damage from this creature [Y/n]?\n>>>").title()
        if again[0] == "N":
          return
  elif side == 1: # enemy
    while count > 0 and inactive[choice].damage > 0:
      inactive[choice].damage -= 1
      count -= 1
      if count > 0:
        again = input("Would you like to heal another damage from this creature [Y/n]?\n>>>").title()
        if again[0] == "N":
          return
  else:
    return # choose side will inform you that the board is empty
  if choice == 0:
    game.activePlayer.amber += 1
    print("You healed 3 damage, so you gain one amber. You now have " + str(game.activePlayer.amber) + " amber.")

def key339(game, card):
  """ Word of Returning: Deal 1 damage to each enemy for each amber on it. Return all amber from those creatures to your pool.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  length = len(inactive)
  for x in range(length):
    if inactive[absa(x, length)].captured > 0:
      inactive[absa(x, length)].damageCalc(game, inactive[absa(x, length)].captured)
      game.activePlayer.amber += inactive[absa(x, length)].captured
      inactive[absa(x, length)].captured = 0
      if inactive[absa(x, length)].updateHealth():
        pending.append(inactive.pop(absa(x, length)))
  game.pending(pending)

def key349(game, card):
  """ Chota Hazri: Lose 1 amber, if you do, you may forge a key at current cost.
  """
  passFunc(game, card)
  game.activePlayer.amber -= 1
  game.activePlayer.keyCost = game.calculateCost()
  if game.activePlayer.amber >= game.activePlayer.keyCost:
    forge = input("Would you like to forge a key for " + str(game.activePlayer.keyCost) + " [Y/n]?\n>>>").title()
    if forge[0] == 'Y':
      print("Key forged!")
      game.activePlayer.keys += 1
      game.activePlayer.amber -= game.activePlayer.keyCost
      if game.activePlayer.keys >= 3:
        game.endBool = False
        return
      print("You now have " + str(game.activePlayer.keys) + " keys and " + str(game.activePlayer.amber) + " amber.")

def key352(game, card):
  """ Flaxia: If you control more creatures than your opponent, gain 2 amber.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  active = game.activePlayer.board["Creature"]

  if len(active) > len(inactive):
    game.activePlayer.amber += 2
    print("You control more creatures than your opponent, so you gain 2 amber. You now have " + str(game.activePlayer.amber) + " amber.")

def key353(game, card):
  """ Fuzzy Gruen: Your opponent gains 1 amber.
  """
  passFunc(game, card)
  game.inactivePlayer.amber += 1
  print("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def key356(game, card):
  """ Inka the Spider: Stun a creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  choice, side = chooseSide(game)
  if side == 0:
    game.activePlayer.printShort(activeBoard)
    activeBoard[choice].stun = True
  elif side == 1:
    game.inactivePlayer.printShort(inactiveBoard)
    inactiveBoard[choice].stun = True
  else:
    return # board is empty

def key359(game, card):
  """ Lupo the Scarred: Deal 2 damage to an enemy creature.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  if len(inactive) == 0:
    print("There are no enemy creatures to damage. The card is still played.")
    return
  choice = makeChoice("Choose an enemy creature to damage: ", inactive)
  inactive[choice].damageCalc(game, 2)
  if inactive[choice].updateHealth():
    pending.append(inactive.pop(choice))
    game.pending(pending)

def key360(game, card):
  """ Mighty Tiger: Deal 4 damage to an enemy creature.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = []
  if len(inactive) == 0:
    print("There are no enemy creatures to damage. The card is still played.")
    return
  choice = makeChoice("Choose an enemy creature to damage: ", inactive)
  inactive[choice].damageCalc(game, 4)
  if inactive[choice].updateHealth():
    pending.append(inactive.pop(choice))
    game.pending(pending)

def key365(game, card):
  """ Piranha Monkeys: Deal 2 damage to each other creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.activePlayer.board["Creature"]
  pendingDisc = []
  [x.damageCalc(game, 2) for x in active if x != card]
  [x.damageCalc(game, 2) for x in inactive]
  length = len(active)
  [pendingDisc.append(active.pop(abs(x - length + 1))) for x in range(len(active)) if active[abs(x - length + 1)].updateHealth()]
  length = len(inactive)
  [pendingDisc.append(inactive.pop(abs(x - length + 1))) for x in range(len(inactive)) if inactive[abs(x - length + 1)].updateHealth()]
  game.pending(pendingDisc)

## End house Untamed

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly') 