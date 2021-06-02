import pyautogui, pygame, random
from functools import reduce
from helpers import stealAmber, willEnterReady, destroy
# I think it makes more sense to add these to the cardsAsClass file, which means that the only function here is addToBoard

# This is a list of functions for all the play effects on cards, including creature, upgrades, action cards
# Basically any and all cards with "Play:" on them

def passFunc(game, card):
  """ This catches on play abilities. It is called by all other play functions, and by default for card w/o play effects.
  """
  active = game.activePlayer.board
  inactive = game.inactivePlayer.board
  activeS = game.activePlayer.states
  if card.type == "Creature":
    if "full_moon" in activeS and activeS["full_moon"]:
      game.activePlayer.gainAmber(activeS["full_moon"], game)
    if "teliga" in [x.title for x in inactive["Creature"]]:
      count = 0
      for x in inactive["Creature"]:
        if x.title == "teliga":
          count += 1
      game.inactivePlayer.gainAmber(count, game)
    if "hunting_witch" in [x.title for x in active["Creature"]]:
      count = sum(x.title == "hunting_witch" for x in active["Creature"])
      if card.title == "hunting_witch":
        count -= 1 # this prevents hunting witch from triggering off itself
      game.activePlayer.gainAmber(count, game)
    if card.house == "Mars" and "tunk" in [x.title for x in active["Creature"]]:
      location = [active["Creature"].index(x) for x in active["Creature"] if x.title == "tunk"]
      for x in location:
        active["Creature"][x].damage = 0
    if "charge" in activeS and activeS["charge"] and inactive["Creature"]:
      # above line makes sure there will be at least one potential target
      count = activeS["charge"]
      while inactive["Creature"] and count > 0:
        choice = game.chooseCards("Creature", "Choose an enemy minion to deal 2 damage to:", "enemy")[0][1]
        inactive["Creature"][choice].damageCalc(game, 2)
        inactive["Creature"][choice].updateHealth(game.inactivePlayer)
        if inactive["Creature"][choice].destroyed:
          game.pendingReloc.append(card)
        game.pending()
        count -= 1
    # stuff that gives armor
    if "gray_monk" in [x.title for x in active["Creature"]]:
      extra = sum(x.title == "gray_monk" for x in active["Creature"])
      if card.name == "gray_monk":
        extra -= 1 # so it doesn't hit itself
      card.extraArm += extra
      card.resetArmor(game)
    if "banner_of_battle" in [x.title for x in active["Creature"]]:
      extra = sum(x.title == "banner_of_battle" for x in active["Creature"])
      card.power += extra
    # this is deliberately after gray_monk
    if "autocannon" in inactive["Artifact"] + active["Artifact"]:
      count = sum(x.title == "autocannon" for x in inactive["Artifact"] + active["Artifact"])
      while count > 0:
        card.calcDamage(game, 1)
        count -= 1
        card.updateHealth(game.activePlayer)
        if card.destroyed:
          game.pendingReloc.append(card)
          break
    if "pingle_who_annoys" in inactive["Creature"] + active["Creature"]:
      count = sum(x.title == "pingle_who_annoys" for x in inactive["Artifact"] + active["Artifact"])
      while count > 0:
        card.calcDamage(game, 1)
        count -= 1
        card.updateHealth(game.activePlayer)
        if card.destroyed:
          game.pendingReloc.append(card)
          break
    game.pending()
    if card.house == "Mars":
      if card.title in ["chuff_ape", "yxilx_dominator", "zorg"]:
        card.stun = True
      for c in game.activePlayer.board["Creature"]:
        if "brain_stem_antenna" in [x.title for x in c.upgrade]:
          c.ready = True
          c.house = "Mars"
          game.resetHouse.append(c)
          game.cardChanged()
  if willEnterReady(game, card):
    card.ready = True
    pyautogui.alert(card.title + " enters play ready!")
  if card.type == "Artifact":
    if "carlo_phantom" in [x.title for x in active["Creature"]]:
      stealAmber(game.activePlayer, game.inactivePlayer, sum(x.title == "carlo_phantom" for x in active["Creature"]))
      pyautogui.alert("'Carlo Phantom' stole 1 amber for you. You now have " + str(game.activePlayer.amber) + " amber.")
    if "hayyel_the_merchant" in [x.title for x in active["Creature"]]:
      game.activePlayer.gainAmber(1, game)
  if "library_access" in activeS and activeS["library_access"]:
    game.activePlayer += activeS["library_access"]
    pyautogui.alert("You draw a card because you played 'Library Access' earlier this turn.")


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
    game.fightCard(choice, cheat=True)
  else:
    game.fightCard(choice, cheat=True)


def barehanded(game, card):
  """Barehanded. Put each artifact on top of its owner's \
  deck.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]
  for c in active[::-1]:
    game.pendingReloc.append(c)
    active.remove(c)
  # run it all again w/ inactive player
  for c in inactive[::-1]:
    game.pendingReloc.append(c)
    active.remove(c)
  # deal with all artifacts
  game.pending("deck", reveal = True)

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
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  max_friend = max([x.power + x.extraPow for x in active])
  max_enemy = max([x.power + x.extraPow for x in inactive])

  if active:
    choiceA = active[game.chooseCards("Creature", "Choose which friendly creature of the highest power will survive:", condition = lambda x: x.power + x.extraPow == max_friend, con_message = "That creature doesn't have the highest power among friendlies.")[0][1]]
  if inactive:
    choiceI = inactive[game.chooseCards("Creature", "Choose which enemy creature of the highest power will survive:", condition = lambda x: x.power + x.extraPow == max_enemy, con_message = "That creature doesn't have the highest power among enemies.")[0][1]]

  for c in active:
    if c != choiceA:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        game.pendingReloc.append(c)
  for c in inactive:
    if c != choiceI:
      destroy(c, game.inactivePlayer, game)
      if c.destroyed:
        game.pendingReloc.append(c)

  game.pending()
  game.cardChanged()

  # then ready and fight with remaining minion
  if len(game.activePlayer.board["Creature"]) == 0:
    pyautogui.alert("You have no creatures to target.")
    return
  choice = active[game.chooseCards("Creature", "Choose a creature to fight with:", "friend")[0][1]] # because ward will be a thing, and something could happen
  if not choice.ready:
    choice.ready = True
    game.fightCard(active.index(choice), cheat=True)
  else:
    game.fightCard(active.index(choice), cheat=True)

def cowards_end (game, card):
  """Coward's End: Destroy each undamaged creature. Gain 3 chains.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc

  for card in activeBoard[::-1]:
    if card.damage == 0:
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
  for card in inactiveBoard[::-1]:
    if card.damage == 0:
      destroy(card, game.inactivePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
  game.pending()
  
  # finally, add chains
  game.activePlayer.chains += 3
  game.setKeys()

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
  pendingDisc = game.pendingReloc # this one's fine because only one side is ever affected; pending would be able to handle it anyway though

  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets. The card is still played.")
    return

  side, choice = game.chooseCards("Creature", "Deal 4 damage with 2 splash to a creature:")[0]
  if side == "fr":
    c = activeBoard[choice]
    c.damageCalc(game, 4)
    for neigh in c.neighbors(game):
      neigh.damageCalc(game, 2)
    for neigh in c.neighbors(game):
      neigh.updateHealth(game.activePlayer)
      if neigh.destroyed:
        pendingDisc.append(neigh)
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  else:
    c = inactiveBoard[choice]
    c.damageCalc(game, 4)
    for neigh in c.neighbors(game):
      neigh.damageCalc(game, 2)
    for neigh in c.neighbors(game):
      neigh.updateHealth(game.inactivePlayer)
      if neigh.destroyed:
        pendingDisc.append(neigh)
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  game.pending()

def loot_the_bodies (game, card):
  """ Loot the Bodies: For the remainder of the turn, gain 1 amber each time an enemy creature is destroyed.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))
  # the rest will be in basicDest

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

  side, choice = game.chooseCards("Creature", "Deal 3 damage to a creature:")[0]
  if side == "fr":
    c = activeBoard[choice]
    c.damageCalc(game, 3)
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pendingDiscard.append(c)
  else:
    c = inactiveBoard[choice]
    c.damageCalc(game, 3)
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pendingDiscard.append(c)
  game.pending()

def relentless_assault (game, card):
  """ Relentless Assault: Ready and fight with up to 3 friendly creatures, one at a time.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  
  count = 1
  chosen = []
  while count < 4:
    if sum(x in chosen for x in activeBoard) == len(activeBoard):
      pyautogui.alert("No more valid friendly targets.")
      break
    if activeBoard:
      choice = game.chooseCards("Creature", f"Choose up to three creatures, one at a time. (Choice {count} of 3):", "friend", 1, False, lambda x: x not in chosen, con_message = "You've already chosen that creature, you can't fight with it again.")
    else:
      pyautogui.alert("No friendly creatures to target.")
      return
    if choice:
      choice = choice[0][1]
    else:
      return
    card = activeBoard[choice]
    # first choice should always be valid, but not the rest
    if card not in chosen:
      card.ready = True
      game.fightCard(choice, cheat=True)
    else:
      pyautogui.alert("You've already chosen that creature, you can't fight with it again.")
      continue
    chosen.append(card)
    count += 1

def smith (game, card):
  """Smith: Gain 2 amber if you control more creatures than your opponent.
  """
  passFunc(game, card)
  if len(game.activePlayer.board["Creature"]) > len(game.inactivePlayer.board["Creature"]):
    game.activePlayer.gainAmber(2, game)
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
  inactiveBoard = game.inactivePlayer.board["Creature"]

  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets. Card is still played.")
    return
  
  choice = game.chooseCards("Creature", "Stun a creature and its neighbors:")[0]

  if choice[0] == "fr":
    card = activeBoard[choice[1]]
    card.stun = True
    for neigh in card.neighbors(game):
      neigh.stun = True
  else:
    card = inactiveBoard[choice[1]]
    card.stun = True
    for neigh in card.neighbors(game):
      neigh.stun = True

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
  if diff:
    choices = [x[1] for x in game.chooseCards("Creature", f"Choose {diff} friendly creatures to capture an amber:", "friend", diff)]
    for x in choices:
      activeBoard[x].capture(game, 1)

def warsong (game, card):
  """Warsong: For the remainder of the turn, gain 1 amber each time a friendly creature fights.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))

def banner_of_battle (game, card):
  """ Banner of Battle: Each friendly creature gets +1 power.
  """
  passFunc(game, card)
  for card in game.activePlayer.board["Creature"]:
    card.power += 1

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

  for card in activeBoard[::-1]:
    if card.power + card.extraPow <= 3:
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
  for card in inactiveBoard[::-1]:
    if card.power + card.extraPow <= 3:
      destroy(card, game.inactivePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
  game.pending()

def ganger_chieftain (game, card):
  """Ganger Chieftain: You may ready and fight with a neighboring creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]

  # this can't handle the edge case where ganger chieftain is destroyed upon entering
  if len(activeBoard) <= 1:
    return

  if activeBoard.index(card) == 0:
    maybe = game.chooseHouse("custom", (f"Would you like to ready and fight with {activeBoard[1].title.replace('_', ' ').title()}", ["Yes", "No"]))[0]
    if maybe == "Yes":
      activeBoard[1].ready = True
      game.fightCard(1, cheat=True)
    return
  elif activeBoard.index(card) == len(activeBoard)-1:
    maybe = game.chooseHouse("custom", (f"Would you like to ready and fight with {activeBoard[-2].title.replace('_', ' ').title()}", ["Yes", "No"]))[0]
    if maybe == "Yes":
      activeBoard[-2].ready = True
      game.fightCard(len(activeBoard)-2, cheat=True)
    return

def hebe_the_huge (game, card):
  """Hebe the Huge: Deal 2 damage to each other undamaged creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]

  for c in activeBoard:
    if c != card and c.damage == 0:
      c.damageCalc(game, 2)
  for c in inactiveBoard:
    if c.damage == 0:
      c.damageCalc(game, 2)
  
  for card in activeBoard[::-1]:
    card.updateHealth(game.activePlayer)
    if card.destroyed:
      game.pendingReloc.append(card)
  for card in inactiveBoard[::-1]:
    card.updateHealth(game.inactivePlayer)
    if card.destroyed:
      game.pendingReloc.append(card)
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

  choice = game.chooseCards("Creature", "Stun a creature:")[0]

  if choice[0] == "fr":
    activeBoard[choice[1]].stun = True
  else:
    inactiveBoard[choice[1]].stun = True

def wardrummer (game, card):
  """Wardrummer: Return each other friendly Brobnar creature to your hand.
  """
  # ward?
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  pending = game.pendingReloc
  
  for c in activeBoard[::-1]:
    if c.house == "Brobnar" and c != card:
      c.returned = True
      pending.append(c)
  
  game.pending('hand')

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
    house = game.inactivePlayer.discard[-1].house
    for card in game.inactivePlayer.hand:
      card.revealed = True
      if card.house == house:
        count += 1
    pyautogui.alert(f"Your opponent has {str(count)} cards in their hand of the same house as the discarded card. You gain that much amber.")
  else:
    for card in game.inactivePlayer.hand:
      card.revealed = True
    pyautogui.alert("Your opponent has no cards to discard, so you gain no amber.")
  game.activePlayer.gainAmber(count, game)
  count = 0
  if len(game.activePlayer.deck) > 0:
    game.activePlayer.discard.append(game.activePlayer.deck.pop())
    house = game.activePlayer.discard[-1].house
    for card in game.activePlayer.hand:
      card.revealed = True
      if card.house == house:
        count += 1
    pyautogui.alert("You have " + str(count) + " cards in your hand of the same house as the discarded card. Your opponent gains that much amber.")
  else:
    for card in game.activePlayer.hand:
      card.revealed = True
    pyautogui.alert("You have no cards to discard, so your opponent gains no amber.")
  game.inactivePlayer.gainAmber(count, game)

def arise (game, card):
  """Arise!: Choose a house. Return each creature of that house from your discard pile to your hand. Gain 1 chain.
  """
  passFunc(game, card)
  active = game.activePlayer.discard
  house = game.chooseHouse("other")[0]
  # return cards from discard pile
  for c in active[::-1]:
    if c.house == house and c.type == "Creature":
      game.pendingReloc.append(c)
      active.remove(c)
  game.pending("hand")
  # finally, add chains
  game.activePlayer.chains += 1
  game.setKeys()

def control_the_weak (game, card):
  """ Control the Weak: Choose a house on opp's id card, they must choose that house on next turn.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] = game.chooseHouse("control")
  game.resetStatesNext.append(("i", card.title))

def creeping_oblivion (game, card):
  """ Creeping Oblivion: purge up to 2 cards from a discard pile.
  """
  passFunc(game, card)
  activeDisc = game.activePlayer.discard
  inactiveDisc = game.inactivePlayer.discard
  game.drawFriendDiscard = True
  game.drawEnemyDiscard = True
  toPurge = game.chooseCards("Discard", "Choose up to two cards to purge:", "either", 2, False).sort(key = lambda x: x[1], reverse = True)
  for side, choice in toPurge:
    if side == "fr":
      c = activeDisc[choice]
      activeDisc.remove(c)
    else:
      c = inactiveDisc[choice]
    game.pendingReloc.append(c)
  game.pending(c)
  game.drawFriendDiscard = False
  game.drawEnemyDiscard = False
  

def dance_of_doom (game, card):
  """ Dance of Doom: Choose a number. Destroy each creature with power equal to that number.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDestroyed = game.pendingReloc
  # choice = int(pyautogui.prompt("Choose a number. All creatures with power equal to that number will be destroyed:"))
  choice = int(game.chooseHouse("custom", ("Choose a number. All creatures with power equal to that number will be destroyed:", [0] + list({x.power + x.extraPow for x in active + inactive})))[0])
  for card in active[::-1]:
    if card.power + card.extraPow == choice:
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        pendingDestroyed.append(card)
  for card in inactive[::-1]:
    if card.power + card.extraPow == choice:
      destroy(card, game.inactivePlayer, game)
      if card.destroyed:
        pendingDestroyed.append(card)
  game.pending()

def fear (game, card):
  """ Fear: Return an enemy creature to its owner's hand.
  """
  # ward?
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  if len(inactive) == 0:
    pyautogui.alert("Your opponent has no creatures to target. The card is still played.")
    return
  elif len(inactive) == 1:
    choice = inactive[0]
  else:
    choice = inactive[game.chooseCards("Creature", "Choose an enemy creature to return to its owner's hand:", "enemy")[0][1]]
  pending.append(choice)
  choice.returned = True
  game.pending('hand')

def gateway_to_dis (game, card):
  """ Gateway to Dis: Destroy each creature. Gain three gains.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc
  # active player
  for card in active[::-1]:
    destroy(card, game.activePlayer, game)
    if card.destroyed:
      pendingDiscard.append(card)
  # inactive player
  for card in inactive[::-1]:
    destroy(card, game.inactivePlayer, game)
    if card.destroyed:
      pendingDiscard.append(card)
  game.pending()
  # add chains
  game.activePlayer.chains += 3
  game.setKeys()
  
def gongoozle (game, card):
  """ Gongoozle: Deal 3 to a creature. If it is not destroyed, its owner discards a random card from their hand.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc # fine b/c only ever one side
  
  if not active and not inactive:
    return

  side, choice = game.chooseCards("Creature", "Deal 3 damage to a creature:")[0]
  if side == "fr": # friendly side
    card = active[choice]
    card.damageCalc(game, 3)
    card.updateHealth(game.activePlayer)
    if card.destroyed:
      pendingDiscard.append(card)
      game.pending()
    else:
      ran = random.choice(list(range(len(active))))
      game.discardCard(ran, True)
  # enemy side
  else:
    card = inactive[choice]
    card.damageCalc(game, 3)
    card.updateHealth(game.inactivePlayer)
    if card.destroyed:
      pendingDiscard.append(card)
      game.pending()
    else:
      ran = game.inactivePlayer.hand[random.choice(list(range(len(inactive))))]
      pendingDiscard.append(ran)
      game.inactivePlayer.hand.remove(ran)
      game.pending()


def guilty_hearts (game, card):
  """ Guilty Hearts: Destroy each creature with any amber on it.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc
  # active player
  for card in active[::-1]:
    if card.captured > 0:
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
  for card in inactive[::-1]:
    if card.capture > 0:
      destroy(card, game.inactivePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
  game.pending()

def hand_of_dis (game, card):
  """ Hand of Dis: Destroy a creature that is not on a flank.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc # fine b/c only one target
  # running a modified version of chooseSide because of the slightly different restrictions on this card
  
  if not (sum(card.isFlank(game) for card in active) + sum(card.isFlank(game) for card in inactive)):
    pyautogui.alert("No valid targets. The card is still played.")
    return
  
  side, choice = game.chooseCards("Creature", "Choose a non-flank creature to destroy:", condition = lambda x: x.isFlank(game), con_message = "You didn't choose a flank creature. Please try again.")[0]
  if side == "fr":
    card = active[choice]
    destroy(card, game.activePlayer, game)
    if card.destroyed:
      pendingDiscard.append(card)
  else:
    card = inactive[choice]
    destroy(card, game.inactivePlayer, game)
    if card.destroyed:
      pendingDiscard.append(card)
  
  game.pending()

def hecatomb (game, card):
  """ Hecatomb: Destroy each Dis creature. Each player gains 1 amber for each creature they control that was destroyed this way.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc
  count = 0
  for c in active[::-1]:
    if c.house == "Dis":
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        pendingDiscard.append(c)
        count += 1
  game.activePlayer.gainAmber(count, game)
  count = 0
  for c in inactive[::-1]:
    if c.house == "Dis":
      destroy(c, game.inactivePlayer, game)
      if c.destroyed:
        pendingDiscard.append(c)
        count += 1
  game.inactivePlayer.gainAmber(count, game)
  game.pending()

def tendrils_of_pain (game, card):
  """ Tendrils of Pain: Deal 1 to each creature. Deal an additional 3 to each creature if your opponent forged a key on their previous turn.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc
  # deal 1 damage to everything
  for c in active:
    c.damageCalc(game, 1)
  for c in inactive:
    c.damageCalc(game, 1)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  # potential extra 3 damage to everything
  if not game.forgedLastTurn:
    return
  
  for c in active:
    c.damageCalc(game, 3)
  for c in inactive:
    c.damageCalc(game, 3)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  game.pending()

def hysteria (game, card):
  """ Hysteria: Return each creature to its owner's hand.
  """
  # ward
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  
  for c in active[::-1]:
    pending.append(c)
    c.returned = True
  for c in inactive[::-1]:
    pending.append(c)
    c.returned = True
  
  game.pending('hand')

def key_hammer (game, card):
  """ Key Hammer: If your opponent forged a key on their previous turn, unforge it. Your opponent gains 6 amber.
  """
  passFunc(game, card)
  if game.forgedLastTurn:
    if len(game.forgedLastTurn) > 1:
      unforge = game.forgedLastTurn[0]
    else:
      unforge = game.chooseHouse("color", ("Choose which key your opponent forged last turn to unforge", game.forgedLastTurn, [x.upper() for x in game.forgedLastTurn]))[0]
    game.inactivePlayer.keys -= 1
    if unforge == "Red":
      game.inactivePlayer.red = False
    elif unforge == "Yellow":
      game.inactivePlayer.yellow = False
    elif unforge == "Blue":
      game.inactivePlayer.blue = False
  game.inactivePlayer.gainAmber(6, game)
  # game.setKeys() # don't need to call this because gainAmber will

def mind_barb (game, card):
  """ Mind Barb: Your opponent discards a random card from their hand.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.hand
  ran = inactive[random.choice(list(range(len(inactive))))]
  game.inactivePlayer.discard.append(ran)
  inactive.remove(ran)

def pandemonium (game, card):
  """ Pandemonium: Each undamaged creature captures 1 from its opponent.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  #active
  undamaged = [x for x in active if x.damage == 0]
  if len(undamaged) <= game.inactivePlayer.amber:
    [x.capture(game, 1) for x in active if x.damage == 0]
  else:
    choices = game.chooseCards("Creature", "Choose which friendly undamaged creatures will capture an amber:", "friend", game.inactivePlayer.amber, condition = lambda x: x.damage == 0, con_message = "That creature is not damaged. Choose a different one")
    # for choice in choices:
    #   if active[choice[1]].damage > 0:
    #     pyautogui.alert("You chose a damaged creature, please select again.")
    #     continue
    for choice in choices:
      active[choice[1]].capture(game, 1)
    # break
  #inactive
  undamaged = [x for x in inactive if x.damage == 0]
  if len(undamaged) <= game.activePlayer.amber:
    [x.capture(game, 1) for x in inactive if x.damage == 0]
  else:
    #  while True:
    choices = game.chooseCards("Creature", "Choose which enemy undamaged creatures will capture an amber:", "enemy", game.inactivePlayer.amber, condition = lambda x: x.damage == 0, con_message = "That creature is not damaged. Choose a different one")
      # for choice in choices:
      #   if inactive[choice[1]].damage > 0:
      #     pyautogui.alert("You chose a damaged creature, please select again.")
      #     continue
    for choice in choices:
      inactive[choice[1]].capture(game, 1)
      # break

def poltergeist (game, card):
  """ Poltergeist: Use an artifact controlled by any player as if it were yours. Destroy that artifact.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]
  pending = game.pendingReloc
  
  if not active and not inactive:
    pyautogui.alert("No valid targets. The card is still played.")
    return

  choice = game.chooseCards("Artifact", "Choose an artifact to use as if it were yours, then destroy it:")[0]
  if choice[0] == "fr": # friendly side
    card = active[choice[1]]
    if card.ready and card.action:
      game.actionCard(card, "Artifact", cheat=True)
    destroy(card, game.activePlayer, game)
    pending.append(card)
  else:
    card = inactive[choice[1]]
    if card.ready and card.action:
      card.action(game, card)
    pending.append(card)
  game.pending()

def red_hot_armor (game, card):
  """ Red-Hot Armor: Each enemy creature with armor loses all of its armor until the end of the turn and is dealt 1 for each point of armor it lost this way.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc # fine b/c only hits one side
  # deal damage
  for card in inactive:
    damage = card.armor
    card.armor = 0
    card.damageCalc(game, damage)
  for card in inactive[::-1]:
    card.updateHealth(game.inactivePlayer)
    if card.destroyed:
      pendingDiscard.append(card)
  game.pending()

def three_fates (game, card):
  """ Three Fates: Destroy the three most powerful creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc
  # check # of creatures
  if len(active) + len(inactive) <= 3:
    # active
    for card in active[::-1]:
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
    # discard
    for card in inactive[::-1]:
      destroy(card, game.inactivePlayer, game)
      if card.destroyed:
        pendingDiscard.append(card)
    game.pending()
    return
  # find highest power on board
  left = 3
  while left > 0:
    high = max([x.power + x.extraPow for x in active] + [x.power + x.extraPow for x in inactive])
    highList = [x for x in active if x.power + x.extraPow == high] + [x for x in inactive if x.power + x.extraPow == high]
    count = len(highList)
    if count == left: # add all to relevant discards and done
      # active
      for card in active[::-1]:
        if card.power + card.extraPow == high:
          destroy(card, game.activePlayer, game)
        if card.destroyed:
          pendingDiscard.append(card)
      #inactive
      for card in inactive[::-1]:
        if card.power + card.extraPow == high:
          destroy(card, game.inactivePlayer, game)
        if card.destroyed:
          pendingDiscard.append(card)
      game.pending()
      return
    elif count < left: # add all to relevant discards and continue
      for card in active[::-1]:
        if card.power + card.extraPow == high:
          destroy(card, game.activePlayer, game)
        if card.destroyed:
          pendingDiscard.append(card)
      for card in active[::-1]:
        if card.power + card.extraPow == high:
          destroy(card, game.activePlayer, game)
        if card.destroyed:
          pendingDiscard.append(card)
      left -= count
      game.draw()
      pygame.display.flip()
    else:
      choices = game.chooseCards("Creature", f"Choose which {left} creature(s) with the highest power to destroy:", left, condition = lambda x: x.power == high, con_message = "You chose a minion that didn't have the highest power. Please select again.")
      for choice in choices:
        if choice[0] == "fr":
          card = active[choice[1]]
          destroy(card, game.activePlayer, game)
          if card.destroyed:
            pendingDiscard.append(card)
        else:
          card = inactive[choice[1]]
          destroy(card, game.activePlayer, game)
          if card.destroyed:
            pendingDiscard.append(card)
        # break
  game.pending()

#############
# Creatures #
#############

def charette (game, card):
  """ Charette: Capture 3 amber.
  """
  passFunc(game, card)
  card.capture(game, 3)

def drumble (game, card):
  """ Drumble: if your opponent has 7 amber or more, capture all of it.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber >= 7:
    card.capture(game, game.inactivePlayer.amber)

def guardian_demon (game, card):
  """ Guardian Demon: Heal up to 2 damage from a creature. Deal that amount of damage to another creature
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc
  # easy case: no damage
  if reduce(lambda x, y: x + y, [x.damage for x in game.activePlayer.board["Creature"]] + [x.damage for x in game.inactivePlayer.board["Creature"]]) == 0:
    pyautogui.alert("There are no damaged creatures, so the play effect doesn't happen. The card is still played.")
    return
  choice = game.chooseCards("Creature", "Choose a creature:")[0]
  if choice[0] == "fr":
    card1 = active[choice[1]]
    if card1.damage > 0:
      heal = int(game.chooseHouse("custom", ("How much damage would you like to heal?", ["  0  ", "  1  ", "  2  "]))[0])
    else:
      pyautogui.alert("There was no damage on this creature, so no damage will be dealt.")
      return
  else:
    card1 = inactive[choice[1]]
    if card1.damage > 0:
      heal = game.chooseHouse("guardian")[0]
    else:
      pyautogui.alert("There was no damage on this creature, so no damage will be dealt.")
      return
  if heal:
    side, choice = game.chooseCards("Creature", f"Choose a creature to deal {heal} damage to:", condition = lambda x: x != card1, con_message = "You can't damage the creature you healed. Choose a different target.")[0]
    if side == "fr":
      card2 = active[choice]
      card2.damageCalc(game, heal)
      card2.updateHealth(game.activePlayer)
      if card2.destroyed:
        pendingDisc.append(card2)
    else:
      card2 = inactive[choice]
      card2.damageCalc(game, heal)
      card2.updateHealth(game.inactivePlayer)
      if card.destroyed:
        pendingDisc.append(card2)
    game.pending()

def restringuntus (game, card):
  """ Restringuntus: Choose a house. Your opponent cannot choose that house as their active house until Restringuntus leaves play.
  """
  passFunc(game, card)
  # no deck has more than one copy of this card
  game.chooseHouse("other")

def shooler (game, card):
  """ Shooler: if your opponent has 4 or more amber, steal 1.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber >= 4:
    stealAmber(game.activePlayer, game.inactivePlayer, 1)
  
def the_terror (game, card):
  """ The Terror: If your opponent has no amber, gain 2.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber == 0:
    game.activePlayer.gainAmber(2, game)

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

def bouncing_deathquark (game, card):
  """ Bouncing Deathquark: Destroy an enemy creature and a friendly creature. Repeat effect as many times as you want, as long as you can repeat entire effect.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc
  while active and inactive:
    while True:
      choices = game.chooseCards("Creature", "Choose an enemy creature to destroy and a friendly creature to destroy, or choose no creatures to stop:", count = 2, full = False) # this condition is more complicated, can't integrate it
      if len(choices) == 0:
        return
      if len(choices) == 1 or choices[0][0] == choices[1][0]:
        pyautogui.alert("You need to choose one enemy and one friendly creature. Try again.")
        continue
      else:
        for choice in choices:
          if choice[0] == "fr":
            card = active[choice[1]]
            destroy(card, game.activePlayer, game)
            if card.destroyed:
              pendingDiscard.append(card)
          else:
            card = inactive[choice[1]]
            destroy(card, game.inactivePlayer, game)
            if card.destroyed:
              pendingDiscard.append(card)
        break
    game.pending()

def dimension_door (game, card):
  """ Dimension Door: For the remainder of the turn, any amber you would gain from reaping is stolen from your opponent instead.
  """
  passFunc(game, card)
  # just set a state, effect doesn't stack from multiple copies
  game.activePlayer.states[card.title] += 1
  game.resetStates.append("a", card.title)

def effervescent_principle (game, card):
  """ Effervescent Principle: Each player loses half their amber (rounding down the loss). Gain one chain.
  """
  passFunc(game, card)
  if game.activePlayer.amber % 2 != 0:
    game.activePlayer.amber += 1 # this is actually not a gain amber, this is just a hack
  if game.inactivePlayer.amber % 2 != 0:
    game.inactivePlayer.amber += 1 # this is actually not a gain amber, this is just a hack
  if game.activePlayer.amber > 0:
    game.activePlayer.amber //= 2
    pyautogui.alert("After losing half your amber, you now have " + str(game.activePlayer.amber) + " amber.")
  else:
    pyautogui.alert("You still have no amber.")
  if game.inactivePlayer.amber > 0:
    game.inactivePlayer.amber //= 2
    pyautogui.alert("After losing half their amber, your opponent now has " + str(game.inactivePlayer.amber) + " amber.")
  else:
    pyautogui.alert("Your opponent still has no amber.")
  game.activePlayer.chains += 1
  game.setKeys()

def foggify (game, card):
  """ Foggify: your opponent cannot use creatures to fight on their next turn.
  """
  passFunc(game, card)
  # states should always be in deck that they affect
  game.activePlayer.states[card.title] += 1
  game.resetStatesNext.append(("i", card.title))

def help_from_future_self (game, card):
  """ Help from Future Self: Search your deck and discard pile for a Timetraveller, reveal it, and put it into your hand. Shuffle your discard pile into your deck.
  """
  passFunc(game, card)
  # multiples of these pairings is possible, but only come in pairs
  # let's use an iterative function to search with
  def search(hand, L):
    # look at first item in deck
    x = 0
    while x < len(L):
      if L[x].title == "timetraveller":
        hand.append(L.pop(x))
        return True
      else:
        x += 1
    return False
  
  if not search(game.activePlayer.hand, game.activePlayer.deck):
    if not search(game.activePlayer.hand, game.activePlayer.discard):
      pyautogui.alert("No 'Timetraveller' found.")
  game.activePlayer.shuffleDiscard()

def interdimensional_graft (game, card):
  """ Interdimensional Graft: If an opponent forges a key on their next turn, they must give you their remaining amber.
  """
  passFunc(game, card)
  # update state
  game.activePlayer.states[card.title] += 1
  game.resetStatesNext.append(("i", card.title))

def knowledge_is_power (game, card):
  """ Knowledge is Power: Choose one: Archive a card, or, for each archived card you have, gain 1 amber.
  """
  passFunc(game, card)
  # b/c this is one of only two choose card in whole set, will give card text
  choice = game.chooseHouse("custom", ("Archive a card, or gain 1 amber for each card in your archives?", ["Archive", "Gain amber"]))[0]
  if choice == "Archive":
    if len(game.activePlayer.hand) > 0:
      archive = game.chooseCards("Hand", "Choose a card to archive:")[0][1]
      card = game.activePlayer.hand[archive]
      game.pendingReloc.append(card)
      game.activePlayer.hand["Creature"].remove(card)
      game.pending("archive", target = game.activePlayer)
    else:
      pyautogui.alert("Your hand is empty, so you can't archive a card.")
  else:
    game.activePlayer.gainAmber(len(game.activePlayer.archive), game)


def labwork (game, card):
  """ Labwork: Archive a card.
  """
  passFunc(game, card)
  if game.activePlayer.hand:
    archive = game.chooseCards("Hand", "Choose a card from your hand to archive:")[0][1]
    card = game.activePlayer.hand[archive]
    game.pendingReloc.append(card)
    game.activePlayer.hand.remove(card)
    game.pending("archive", target = game.activePlayer)

def library_access (game, card):
  """ Library Access: Purge this card. For the remainder of the turn, each time you play another card, draw a card.
  """
  passFunc(game, card)
  # purging is handled in the playCard function, my old solution would have led to popping from an empty list
  game.activePlayer.states[card.title] += 1

def neuro_syphon (game, card):
  """ Neuro Syphon: If your opponent has more amber than you, steal 1 amber and draw a card.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber > game.activePlayer.amber:
    stealAmber(game.activePlayer, game.inactivePlayer, 1)
    pyautogui.alert("Your opponent has more amber than you, so the effect triggers. You now have " + str(game.activePlayer.amber) + " amber. Drawing a card.")
    game.activePlayer += 1
    return
  pyautogui.alert("You have at least as much amber as your opponent. Nothing happens.")
    
def phase_shift (game, card):
  """ Phase Shift: You may play one non-Logos card this turn.
  """
  passFunc(game, card)
  # this is a tough one. effect can stack, so we'll use a list
  game.activePlayer.states[card.title] += 1
  game.resetStates.append("a", card.title)

def positron_bolt (game, card):
  """ Positron Bolt: Deal 3 damage to a flank creature. Deal 2 damage to its neighbor. Deal 1 damage to the second creature's other neighbor.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc # fine b/c only one side
  
  if not active and not inactive:
    pyautogui.alert("No valid targets. The cards is still played.")
    return
  
  side, choice = game.chooseCards("Creature", "Choose a flank creature to deal three damage to:", condition = lambda x: x.isFlank(game), con_message = "You didn't choose a flank creature. Please try again.")[0]
  
  if side == "fr":
    if choice == 0:
      i = 0
      card1 = active[i]
      card1.damageCalc(game, 3)
      if len(active) > 1:
        card2 = active[i + 1]
        card2.damageCalc(game, 2)
      else:
        card2 = False
      if len(active) > 2:
        card3 = active[i + 2]
        card3.damageCalc(game, 1)
      else:
        card3 = False
      card1.updateHealth(game.activePlayer)
      if card1.destroyed:
        pending.append(card1)
      if card2:
        card2.updateHealth(game.activePlayer)
        if card2.destroyed:
          pending.append(card2)
      if card3:
        card3.updateHealth(game.activePlayer)
        if card3.destroyed:
          pending.append(card3)
    else:
      i = choice
      card1 = active[i]
      card1.damageCalc(game, 3)
      card2 = active[i - 1]
      card2.damageCalc(game, 2)
      if len(active) > 2:
        card3 = active[i - 2]
        card3.damageCalc(game, 1)
      else:
        card3 = False
      card1.updateHealth(game.activePlayer)
      if card1.destroyed:
        pending.append(card1)
      card2.updateHealth(game.activePlayer)
      if card2.destroyed:
        pending.append(card2)
      if card3:
        card3.updateHealth(game.activePlayer)
        if card3.destroyed:
          pending.append(card3)
  else:
    if choice == 0:
      i = 0
      card1 = inactive[1]
      card1.damageCalc(game, 3)
      if len(inactive) > 1:
        card2 = inactive[i + 1]
        card2.damageCalc(game, 2)
      else:
        card2 = False
      if len(inactive) > 2:
        card3 = inactive[i + 2]
        card3.damageCalc(game, 1)
      else:
        card3 = False
      card1.updateHealth(game.inactivePlayer)
      if card1.destroyed:
        pending.append(card1)
      if card2:
        card2.updateHealth(game.inactivePlayer)
        if card2.destroyed:
          pending.append(card2)
      if card3:
        card3.updateHealth(game.inactivePlayer)
        if card3.destroyed:
          pending.append(card3)
    else:
      i = choice
      card1 = inactive[i]
      card1.damageCalc(game, 3)
      card2 = inactive[i - 1]
      card2.damageCalc(game, 2)
      if len(inactive) > 2:
        card3 = inactive[i - 2]
        card3.damageCalc(game, 1)
      else:
        card3 = False
      card1.updateHealth(game.inactivePlayer)
      if card1.destroyed:
        pending.append(card1)
      card2.updateHealth(game.inactivePlayer)
      if card2.destroyed:
        pending.append(card2)
      if card3:
        card3.updateHealth(game.inactivePlayer)
        if card3.destroyed:
          pending.append(card3)
  game.pending()

def random_access_archives (game, card):
  """ Random Access Archives: Archive the top card of your deck.
  """
  passFunc(game, card)
  # if deck is empty, don't shuffle
  if len(game.activePlayer.deck) > 0:
    card = game.activePlayer.deck[-1]
    game.pendingReloc.append(card)
    game.activePlayer.deck["Creature"].remove(card)
    game.pending("archive", target = game.activePlayer)
    pyautogui.alert("The top card or your deck has been archived.")
    return
  pyautogui.alert("Your deck is empty. Nothing happens.")

def remote_access(game, card):
  """ Remote Access: use an opponent's artifact as if it were yours.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Artifact"]
  if len(inactive) > 0:
    choice = game.chooseCards("Artifact", "Choose an opponent's artifact to use:", "enemy")[0][1]
    if inactive[choice].ready and inactive[choice].action:
      inactive[choice].action(game, game.inactivePlayer.board["Artifact"][choice])
      inactive[choice].ready = False
  else:
    pyautogui.alert("Your opponent has no artifacts. The card is stil played.")

def reverse_time (game, card):
  """ Reverse Time: Swap your deck and your discard pile. Then, shuffle your deck.
  """
  passFunc(game, card)
  game.activePlayer.deck, game.activePlayer.discard = game.activePlayer.discard, game.activePlayer.deck
  random.shuffle(game.activePlayer.deck)

def scrambler_storm (game, card):
  """ Scrambler Storm: Your opponent cannot play action cards on their next turn.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] += 1
  game.resetStatesNext.append(("i", card.title))

def sloppy_labwork (game, card):
  """ Sloppy Labwork: Archive a card. Discard a card.
  """
  passFunc(game, card)
  hand = game.activePlayer.hand
  
  if len(hand) > 0:
    choice = game.chooseCards("Hand", "Choose a card to archive:")[0][1]
    card = hand[choice]
    game.pendingReloc.append(card)
    hand.remove(card)
    game.pending("archive", target = game.activePlayer)
    pyautogui.alert("Card archived!")
  if len(hand) > 0:
    choice = game.chooseCards("Hand", "Choose a card to discard:")[0][1]
    game.discardCard(choice, cheat=True)
    pyautogui.alert("Card discarded!")

def twin_bolt_emission (game, card):
  """ Twin Bolt Emission: Deal 2 damage to a creature and deal 2 damage to a different creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc
  if active or inactive:
    choices = game.chooseCards("Creature", f"Choose {min(2, len(active) + len(inactive))} creature(s) to deal two damage to:", count = min(2, len(active) + len(inactive)))
    for side, choice in choices:
      if side == "fr":
        c = active[choice]
        c.damageCalc(game, 2)
        c.updateHealth(game.activePlayer)
        if c.destroyed:
          pendingDisc.append(c)
      else:
        c = inactive[choice]
        c.damageCalc(game, 2)
        c.updateHealth(game.inactivePlayer)
        if c.destroyed:
          pendingDisc.append(c)
  game.pending()

def wild_wormhole (game, card):
  """ Wild Wormhole: Play the top card of your deck.
  """
  passFunc(game, card)
  game.activePlayer.deck[-1].revealed = True
  game.draw() # so they can see what card is being played (if I update the drawing the board function properly)
  pygame.display.update()
  game.playCard(len(game.activePlayer.deck) - 1, "Deck")

#############
# Creatures #
#############

def dextre(game, card):
  """ Dextre: Capture 1 amber. Destroyed: Put Dextre on top of your deck.
  """
  passFunc(game, card)
  card.capture(game, 1)
  pyautogui.alert("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def dr_escotera(game, card):
  """ Dr. Escotera: Gain 1 amber for each key your opponent has.
  """
  passFunc(game, card)
  game.activePlayer.gainAmber(game.inactivePlayer.keys, game)
  pyautogui.alert("You now have " + str(game.activePlayer.amber) + " amber")

def dysania (game, card):
  """ Dysania: Your opponent discards each of their archived cards. You gain 1 amber for each card discarded this way.
  """
  passFunc(game, card)
  # edge case: if your opponent has your cards in their archive, they don't get discarded, but sent to your hand, so you don't gain amber for them
  if len(game.inactivePlayer.archive) > 0:
    count = 0
    for x in game.inactivePlayer.archive:
      if x.deck == game.inactivePlayer.name:
        count += 1
        game.pendingReloc.append(x)
        game.inactivePlayer.archive.remove(x)
      else:
        game.activePlayer.hand.append(x)
        game.inactivePlayer.archive.remove(x)
    game.activePlayer.gainAmber(count, game)
    print("You gained " + str(count) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
    game.pending()

def harland_mindlock (game, card):
  """ Harland Mindlock: Take control of an enemy flank creature until Harland Mindlock leaves play.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if not inactive:
    pyautogui.alert("No enemy creatures to steal!")
    return

  choice = inactive[game.chooseCards("Creature", "Choose an enemy flank creature to steal:", "enemy", condition = lambda x: x.isFlank(game), con_message = "You didn't choose a flank creature. Please try again.")[0][1]]
  flank = game.chooseHouse("custom", ("Put the minion on your left flank or your right flank?", ["Left", "Right"]))
  card.harland = choice
  if flank == "Left":
    flank = 0
  else:
    flank = len(active)
  active.insert(flank, choice)
  inactive.remove(choice)


def neutron_shark (game, card):
  """ Neutron Shark: Destroy an enemy creature or artifact and a friendly creature or artifact. Discard the top card of your deck. If that card is not a Logos card, trigger this effect again.
  """
  passFunc(game, card)
  active = game.activePlayer.board
  inactive = game.inactivePlayer.board
  pendingDiscard = game.pendingReloc

  while card in active:
    if inactive:
      targetType = game.chooseHouse("custom", ("Would you like to target an enemy artifact or an enemy creature?", ["Artifact", "Creature"]))[0]
      choice1 = game.chooseCards(targetType, f"Choose an enemy {targetType.lower()} to destroy:", "enemy")[0][1]
      card1 = game.inactivePlayer.board[targetType][choice1]
      destroy(card1, game.inactivePlayer, game)
      if (card1.type == "Creature" and card1.destroyed) or card1.type == "Artifact":
        pendingDiscard.append(card1)
    if active:
      targetType2 = game.chooseHouse("custom", ("Would you like to target a friendly artifact or a friendly creature?", ["Artifact", "Creature"]))[0]
      choice2 = game.chooseCards(targetType2, f"Choose a friendly {targetType2.lower()} to destroy:", "friend")[0][1]
      card2 = game.inactivePlayer.board[targetType2][choice2]
      destroy(card2, game.inactivePlayer, game)
      if (card2.type == "Creature" and card2.destroyed) or card2.type == "Artifact":
        pendingDiscard.append(card2)
    game.pending()
    if game.activePlayer.deck:
      game.activePlayer.discard.append(game.activePlayer.deck.pop())
      if game.activePlayer.discard[-1].house == "Logos":
        break
    else:
      break
    
def psychic_bug (game, card):
  """ Psychic Bug: Look at your opponent's hand.
  """
  passFunc(game, card)
  for card in game.inactivePlayer.hand:
    card.revealed = True

def skippy_timehog (game, card):
  """ Skippy Timehog: Your opponent canot use any cards next turn.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] += 1
  game.resetStatesNext.append(("i", card.title))

def timetraveller (game, card):
  """ Timetraveller: Draw two cards.
  """
  passFunc(game, card)
  game.activePlayer += 2

## End house Logos

########
# Mars #
########

###########
# Actions #
###########

# I should be able to use chooseCards instead of reveal here.

def ammonia_clouds (game, card):
  """ Ammonia Clouds: Deal 3 damage to each creature.
  """
  passFunc(game, card)
  
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc
  
  for c in active:
    c.damageCalc(game, 3)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  for c in inactive:
    c.damageCalc(game, 3)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  game.pending()

def battle_fleet (game, card):
  """ Battle Fleet: Reveal any number of Mars cards from your hand. For each card revealed this way, draw 1 card.
  """
  passFunc(game, card)
  revealed = [x[1] for x in game.chooseCards("Hand", "Reveal any number of Mars cards from your hand:", count = max(1, sum(x.house == "Mars" for x in game.activePlayer.hand)), full = False, condition = lambda x: x.house == "Mars", con_message = "That's not a Mars card. Please pick again.")]
  for card in revealed:
    game.activePlayer.hand[card].revealed = True
  game.activePlayer += len(revealed)

def deep_probe (game, card):
  """ Deep Probe: Choose a house: Reveal your opponent's hand. Discard each creature of that house revealed this way.
  """
  passFunc(game, card)
  house = game.chooseHouse("other")[0]

  for c in game.activePlayer.hand[::-1]:
    c.revealed = True
    if c.house == house and c.type == "Creature":
      game.pendingReloc.append(c)
      game.activePlayer.hand.remove(c)
  
  game.pending()

def emp_blast (game, card):
  """ EMP Blast: Each Mars creature and each Robot creature is stunned. Each artifact is destroyed.
  """
  passFunc(game, card)
  
  activeC = game.activePlayer.board["Creature"]
  activeA = game.activePlayer.board["Artifact"]
  inactiveC = game.inactivePlayer.board["Creature"]
  inactiveA = game.inactivePlayer.board["Artifact"]
  
  for x in [x for x in (activeC + inactiveC) if x.house == "Mars" or "Robot" in x.traits]:
    x.stun = True
  for card in activeA[::-1]:
    destroy(card, game.activePlayer, game)
    game.pendingReloc.append(card)
  for card in inactiveA[::-1]:
    destroy(card, game.inactivePlayer, game)
    game.pendingReloc.append(card)
  game.pending()

def hypnotic_command (game, card):
  """ Hypnotic Command: For each friendly Mars creature, choose an enemy creature to capture one amber from their own side.
  """
  passFunc(game, card)
  
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.house == "Mars" for x in active)
  while count > 0:
    choice = game.chooseCards("Creature", "Choose an enemy creature to capture one amber from their own side: ", "enemy")[0][1]
    # looks like they can choose the same minion each time, which is why the loop
    inactive[choice].capture(game, 1, True)
    count -= 1
  pyautogui.alert("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")
  
def irradiated_amber (game, card):
  """ Irradiated Amber: If your opponent has 6 or more amber, deal 3 damage to each enemy creature.
  """
  passFunc(game, card)
  
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc

  if game.inactivePlayer.amber >= 6:
    for card in inactive:
      card.damageCalc(game, 3)
    for card in inactive[::-1]:
      card.updateHealth(game.inactivePlayer)
      if card.destroyed:
        pendingDisc.append(card)
  game.pending()

def key_abduction (game, card):
  """ Key Abduction: Return each Mars creature to its owner's hand. Then you may forge a key at +9 current cost, reduced by 1 for each card in your hand.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  for c in active[::-1]:
    if c.house == "Mars":
      c.returned = True
      pending.append(c)
  for c in inactive[::-1]:
    if c.house == "Mars":
      c.returned = True
      pending.append(c)
  game.pending('hand')

  temp_cost = game.calculateCost() + 9 - len(game.activePlayer.hand)
  if game.canForge() and game.activePlayer.amber >= temp_cost:
    forge = game.chooseHouse("custom", (f"You may now forge a key for {temp_cost} amber. Would you like to do so?", ["Yes", "No"]))[0]
    if forge == "No":
      pyautogui.alert("You have chosen not to forge a key.")
      return
    game.forgeKey("active", temp_cost)
    if game.activePlayer.keys >= 3:
      pyautogui.alert(f"{game.activePlayer.name} wins!")
      pygame.quit()
  elif game.canForge():
    pyautogui.alert("You don't have enough amber to forge a key.")
  else:
    pyautogui.alert("You are unable to forge a key right now for some reason.")

def martian_hounds (game, card):
  """ Martian Hounds: Choose a creature. For each damaged creature, give the chosen creature two +1 power counters.
  """
  passFunc(game, card)
  
  count = sum(x.damage > 0 for x in game.activePlayer.board["Creature"] + game.inactivePlayer.board["Creature"])
  if count == 0:
    pyautogui.alert("There are no damaged creatures, so no power will be gained. The card is still played.")
    return
  side, choice = game.chooseCards("Creature", f"Choose a creature to give {count * 2} power counters to:")[0]
  if side == "fr": # friendly
    choice = game.activePlayer.board["Creature"][choice]
    choice.power += (2 * count)
    pyautogui.alert(f"{choice.title} now has {choice.power + choice.extraPow} power.")
    return
  choice = game.inactivePlayer.board["Creature"][choice]
  choice.power += (2 * count)
  print(choice.title + " now has " + str(choice.power + choice.extraPow) + " power.")

def martians_make_bad_allies (game, card):
  """ Martians Make Bad Allies: Reveal your hand. Purge each revealed non-Mars creature and gain 1 amber for each card purged this way.
  """
  passFunc(game, card)
  active = game.activePlayer.hand
  count = 0 
  for c in active[::-1]:
    c.revealed = True
    if c.type == "Creature" and c.house != "Mars":
      count += 1
      game.activePlayer.purge.append(c)
      active.remove(c)
  if count > 0:
    game.activePlayer.gainAmber(count, game)
    pyautogui.alert("You gained " + str(count) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
    return
  pyautogui.alert("You had no non-Mars creatures in hand. You gain no amber. The card is still played.")

def mass_abduction (game, card):
  """ Mass Abduction: Put up to 3 damaged enemy creatures into your archives. If any of these creatures leave your archives, they are put into their owner's hand instead.
  """
  passFunc(game, card)
  
  inactive = game.inactivePlayer.board["Creature"]
  count = len([x for x in inactive if x.damage > 0])
  
  if count == 0:
    pyautogui.alert("There are no damaged enemy creatures. The card is still played.")
    return

  choices = [x[1] for x in game.chooseCards("Creature", "Choose up to 3 damaged enemy creatures to put into your archives:", "enemy", 3, False, lambda x: x.damage > 0)].sort(reverse=True)

  if choices:
    for choice in choices:
      c = inactive[choice]
      game.pendingReloc.append(c)
      inactive.remove(c)
  
  game.pending("archive", target = game.activePlayer)

def mating_season (game, card):
  """ Mating Season: Shuffle each Mars creature into its owner's deck. Each player gains 1 amber for each creature shuffled into their deck this way.
  """
  passFunc(game, card)
  activeD = game.activePlayer.deck
  inactiveD = game.inactivePlayer.deck
  activeC = game.activePlayer.board["Creature"]
  inactiveC = game.inactivePlayer.board["Creature"]
  
  count = 0
  for c in activeC[::-1]:
    if c.house == "Mars":
      game.pendingReloc.append(c)
      activeC.remove(c)
      count += 1
  game.activePlayer.gainAmber(count, game)
  count = 0
  for c in inactiveC[::-1]:
    if c.house == "Mars":
      game.pendingReloc.append(c)
      inactiveC.remove(c)
      count += 1
  game.inactivePlayer.gainAmber(count, game)

  game.pending("deck")
  random.shuffle(activeD)
  random.shuffle(inactiveD)

def mothership_support (game, card):
  """ Mothership Support: For each friendly ready Mars creature, deal 2 damage to a creature. (You may choose a different creature each time.)
  """
  passFunc(game, card)
  
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc # fine because one target at a time
  friend_damaged = []
  enemy_damaged = []
  count = sum(x.ready and x.house == "Mars" for x in active)
  if count == 0:
    pyautogui.alert("You have no Mars creatures, so no damage is dealt. The card is still played.")
    return
  hits = 1
  while hits <= count:
    side, choice = game.chooseCards("Creature", f"Deal 2 damage to a creature ({hits} of {count}):")[0]
    if side == "fr":
      c = active[choice]
      if c not in friend_damaged:
        friend_damaged.append(c)
      c.damageCalc(game, 2)
    else:
      c = inactive[choice]
      if c not in enemy_damaged:
        enemy_damaged.append(c)
      c.damageCalc(game, 2)
    hits += 1
  for c in friend_damaged:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in enemy_damaged:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  game.pending()

def orbital_bombardment (game, card):
  """ Orbital Bombardment: Reveal any number of Mars cards from your hand. For each card revealed this way, deal 2 damage to a creature. (you may choose a different creature each time.)
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  friend_damaged = []
  enemy_damaged = []

  revealed = [x[1] for x in game.chooseCards("Hand", "Reveal any number of Mars cards from your hand:", count = max(1, sum(x.house == "Mars" for x in game.activePlayer.hand)), full = False, condition = lambda x: x.house == "Mars", con_message = "That's not a Mars card. Please pick again.")]
  count = len(revealed)
  if count == 0:
    pyautogui.alert("You revealed no Mars cards, so no damage is dealt. The card is still played.")
    return
  hits = 1
  while hits <= count:
    side, choice = game.chooseCards("Creature", f"Deal 2 damage to a creature ({hits} of {count}):")[0]
    if side == "fr":
      c = active[choice]
      if c not in friend_damaged:
        friend_damaged.append(c)
      c.damageCalc(game, 2)
    else:
      c = inactive[choice]
      if c not in enemy_damaged:
        enemy_damaged.append(c)
      c.damageCalc(game, 2)
    hits += 1
  for c in friend_damaged:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in enemy_damaged:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  game.pending()
  
def phosphorous_stars (game, card):
  """ Phosphorous Stars: Stun each non-Mars creature. Gain 2 chains.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  for x in (active + inactive):
    if x.house != "Mars":
      x.stun = True

  game.activePlayer.chains += 2
  game.setKeys()

def psychic_network (game, card):
  """ Psychic Network: Steal 1 amber for each friendly ready Mars creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  count = sum(x.ready and x.house == "Mars" for x in active)
  if count == 0:
    pyautogui.alert("You have no friendly ready Mars creatures, so you don't steal any amber. The card is still played.")
    return
  stealAmber(game.activePlayer, game.inactivePlayer, count)

def sample_collection (game, card):
  """ Sample Collection: Put an enemy creature into your archives for each key your opponent has forged. If any of these creatures leave your archives, they are put into their owner's hand instead.
  """
  passFunc(game, card)
  count = game.inactivePlayer.keys
  inactive = game.inactivePlayer.board["Creature"]
  
  if count == 0:
    pyautogui.alert("Your opponent has forged no keys, so you archive no enemy creatures. The card is still played.")
    return
  
  if not inactive:
    pyautogui.alert("Your opponent has no creatures to target.")
  
  targets = min(len(inactive), count)
  choices = [x[1] for x in game.chooseCards("Creature", f"Choose {targets} creature(s) to put into your archives:", "enemy", targets)]
  for choice in choices:
    game.pendingReloc.append(inactive[choice])
    inactive.remove(inactive[choice])
  game.pending("archive", target = game.activePlayer)

def shatter_storm (game, card):
  """ Shatter Storm: Lose all your amber. Then, your opponent loses triple the amount of amber you lost this way.
  """
  passFunc(game, card)
  count = game.activePlayer.amber
  if count == 0:
    pyautogui.alert("You have no amber to lose, so your opponent loses no amber. The card is still played.")
    return
  game.activePlayer.amber -= count
  game.inactivePlayer.amber -= (count * 3)
  if game.inactivePlayer.amber < 0:
    game.inactivePlayer.amber = 0

def soft_landing (game, card):
  """ Soft Landing: The next creature or artifact you play this turn enters play ready.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] = 1
  # this one doesn't go in reset states, is controlled by basicPlay, but still needs to be in reset states in case that isn't triggered
  game.resetStates.append(("a", card.title))

def squawker (game, card):
  """ Squawker: Ready a Mars creature or stun a non-Mars creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if active or inactive:
    side, choice = game.chooseCards("Creature", "Ready a Mars creature or stun a non-Mars creature:")[0]
    if side == "fr":
      card = active[choice]
      if card.house == "Mars":
        card.ready = True
      else:
        card.stun = True
    else:
      card = inactive[choice]
      if card.house == "Mars":
        card.ready = True
      else:
        card.stun = True

def total_recall (game, card):
  """ Total Recall: For each friendly ready creature, gain 1 amber. Return each friendly creature to your hand.
  """
  # ward
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  pendingHand = game.pendingReloc
  count = sum(x.ready for x in active)
  if len(active) == 0:
    pyautogui.alert("You have no friendly creatures, so nothing happens. The card is still played.")
    return
  if count == 0:
    print("You have no ready creatures, so you gain no amber.")
  for c in active[::-1]:
    pendingHand.append(c)
    c.returned = True
  game.pending('hand')

#############
# Creatures #
#############

def yxili_marauder (game, card):
  """ Yxili Marauder: Capture 1 amber for each friendly ready Mars creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  count = sum(x.ready and x.house == "Mars" for x in active)

  if count == 0:
    pyautogui.alert("You have no friendly ready Mars creatures. " + card.title + " captures no amber.")
    return
  while count > 0 and game.inactivePlayer.amber > 0:
    card.capture(game, 1)
    count -= 1
  pyautogui.alert("Yxili Marauder captured " + str(card.captured) + " amber.")

## End house Mars

###########
# Sanctum #
###########

###########
# Actions #
###########

def begone (game, card):
  """ Begone!: Choose one: destroy each Dis creature, or gain 1 amber.
  """
  passFunc(game, card)
  choice = game.chooseHouse("custom", ("Choose one: Destroy each Dis creature, or gain 1 amber", ["Destroy Dis", "Gain amber"]))[0]
  if choice[0] == "D":
    for c in game.activePlayer.board["Creature"][::-1]:
      if c.house == "Dis":
        destroy(c, game.activePlayer, game)
        if c.destroyed:
          game.pendingReloc.append(c)
    for c in game.inactivePlayer.board["Creature"][::-1]:
      if c.house == "Dis":
        destroy(c, game.inactivePlayer, game)
        if c.destroyed:
          game.pendingReloc.append(c)
  else:
    game.activePlayer.gainAmber(1, game)

def blinding_light (game, card):
  """ Blinding Light: Choose a house. Stun each creature of that house.
  """
  passFunc(game, card)
  choice = game.chooseHouse("any")
  if choice not in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
    print("Not a valid input. Try again.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  for x in (active + inactive):
    if x.house == choice:
      x.stun = True

def charge (game, card):
  """ Charge!: For the remainder of the turn, each creature you play gains, "Play: Deal 2 to an enemy creature."
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))

def cleansing_wave (game, card):
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
  game.activePlayer.gainamber(count, game)
  pyautogui.alert("You healed " + str(count) + " damage. You gain that much amber.")

def clear_mind (game, card):
  """ Clear Mind: Unstun each friendly creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  for x in active:
    x.stun = False

def doorstep_to_heaven (game, card):
  """ Doorstep to Heaven: Each player with 6 or more amber is reduced to five amber.
  """
  passFunc(game, card)
  if game.activePlayer.amber >= 6:
    game.activePlayer.amber = 5
  if game.inactivePlayer.amber >= 6:
    game.inactivePlayer.amber = 5

def glorious_few (game, card):
  """ Glorious Few: For each creature your opponent controls in excess of you, gain 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if len(inactive) > len(active):
    game.activePlayer.gainAmber((len(inactive) - len(active)), game)
    pyautogui.alert("You gained " + str(len(inactive) - len(active)) + " amber. You now have " + str(game.activePlayer.amber) + " amber.")
    return
  pyautogui.alert("Your opponent does not have more creatures than you, so you gain no amber. The card is still played.")

def honorable_claim (game, card):
  """ Honorable Claim: Each friendly knight creature captures 1.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  knights = sum("Knight" in x.traits for x in active)
  if knights > game.inactivePlayer.amber and game.inactivePlayer.amber > 0:
    pyautogui.alert("You have more knights than your opponent has amber.")
    choices = [x[1] for x in game.chooseCards("Creature", "You have more knights than your opponent has amber. Choose which knights will capture an amber:", "friend", game.inactivePlayer.amber, condition = lambda x: "Knight" in x.traits, con_message = "That's not a knight.")]
    for choice in choices:
      active[choice].capture(game, 1)
  elif knights <= game.inactivePlayer.amber:
    for c in active[::-1]:
      if "Knight" in c.traits:
        c.capture(game, 1)
  else:
    pyautogui.alert("Your opponent has no amber to capture.")

def inspiration (game, card):
  """ Inspiration: Ready and use a friendly creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  choice = game.chooseCards("Creature", "Ready and use a friendly creature", "friend")[0][1]
  card = active[choice]
  card.ready = True
  uses =  ["Reap", "Fight"]
  if active[choice].action:
    uses.append("Action")
  use = game.chooseHouse("custom", ("How would you like to use this creature?", uses))[0]
  if use[0] == "R":
    if game.canReap(card, cheat = True):
      game.reapCard(choice, cheat = True)
  elif use[0] == "F":
    if game.canFight(card, cheat = True):
      game.fightCard(choice, cheat=True)
  elif use[0] == "A":
    if game.canAction(card, cheat = True):
      game.actionCard(choice, cheat = True)

def mighty_lance (game, card):
  """ Mighty Lance: Deal 3 damage to a creature and 3 damage to a neighbor of that creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingD = game.pendingReloc
  
  if not active and not inactive:
    return

  side, choice1 = game.chooseCards("Creature", "Deal three damage to a creature:")[0]
  if side == "fr":
    card1 = active[choice1]
    if len(active) > 1:
      choice2 = game.chooseCards("Creature", "Deal three damage to a neighbor of that creature:", condition=lambda x: x in card1.neighbors(game), con_message = "That's not a neighbor of your original target.")[0][1]
      card2 = active[choice2]
      card2.damageCalc(game, 3)
      card2.updateHealth(game.activePlayer)
      if card2.destroyed:
        pendingD.append(card2)
    card1.damageCalc(game, 3)
    card1.updateHealth(game.activePlayer)
    if card1.destroyed:
      pendingD.append(card1)
  else:
    card1 = inactive[choice1]
    if len(inactive) > 1:
      choice2 = game.chooseCards("Creature", "Deal three damage to a neighbor of that creature:", condition = lambda x: x in card1.neighbors(game), con_message = "That's not a neighbor of your original target.")[0][1]
      card2 = inactive[choice2]
      card2.damageCalc(game, 3)
      card2.updateHealth(game.inactivePlayer)
      if card2.destroyed:
        pendingD.append(card2)
    card1.damageCalc(game, 3)
    card1.updateHealth(game.inactivePlayer)
    if card1.destroyed:
      pendingD.append(card1)

  game.pending()

def oath_of_poverty (game, card):
  """ Oath of Poverty: Destroy each of your artifacts. Gain 2 amber for each artifact destroyed this way.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  count = len(active)
  pending = game.pendingReloc

  if count == 0:
    pyautogui.alert("You have no artifacts, so no extra amber is gained.")
  else:
    for a in active:
      destroy(a, game.activePlayer, game)
      pending.append(a)
  
  game.pending()

def one_stood_against_many (game, card):
  """ One Stood Against Many: Ready and fight with a friendly creature 3 times, each time against a different enemy creature. Resolve these fights one at a time.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  count = 3
  fought = [] # this should be cards, not indexes, so that if something dies and the index changes we're still good

  if active:
    fighting = game.chooseCards("Creature", "Choose a friendly creature to fight with:", "friend")[0][1]
    fighter = active[fighting]
  else:
    return
  fighter.ready = True
  attacks = 1
  while inactive and fighter in active and attacks <= count:
    choice = game.chooseCards("Creature", f"Choose an enemy creature to attack ({attacks} of {count}):", "enemy", condition = lambda x: x not in fought, con_message = "You've already fought that creature")[0][1]
    fought.append(inactive[choice])
    if game.canFight(fighter, reset = False, cheat=True):
      game.fightCard(fighting, cheat = True, defender = choice)
    attacks += 1
    if attacks < 3:
      fighter.ready = True


def radiant_truth (game, card):
  """ Radiant Truth: Stun each enemy creature not on a flank.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  for x in inactive[1:-1]:
    x.stun = True

def shield_of_justice (game, card):
  """ Shield of Justice: For the remainder of the turn, each friendly creature cannot be dealt damage.
  """
  passFunc(game, card)
  # create a state that is checked in damageCalc
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))

def take_hostages (game, card):
  """ Take Hostages: For the remainder of the turn, each time a friendly creature fights, it captures 1 amber.
  """
  passFunc(game, card)
  # create a state that is check in basicFight
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))

def terms_of_redress (game, card):
  """ Terms of Redress: Choose a friendly creature to capture 2 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  choice = game.chooseCards("Creature", "Choose a friendly creature to capture 2 amber:", "friend")[0][1]
  active[choice].capture(game, 2)

def the_harder_they_come (game, card):
  """ The Harder They Come: Purge a creature with power 5 or higher.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if True not in [x.power + x.extraPow > 4 for x in active + inactive]:
    return
  
  side, choice = game.chooseCards("Creature", "Purge a creature with power 5 or higher:", condition = lambda x: x.power + x.extraPow > 4, con_message = "This creature doesn't have high enough power.")[0]

  if side == "fr":
    card = active[choice]
    active.remove(card)
    game.pendingReloc.append(card)
  else:
    card = inactive[choice]
    inactive.remove(card)
    game.pendingReloc.append(card)
  game.pending("purge")

def the_spirits_way (game, card):
  """ The Spirit's Way: Destroy each creature with power 3 or higher.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingD = game.pendingReloc

  for c in active[::-1]:
    if c.power + c.extraPow > 2:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        pendingD.append(c)
  for c in inactive[::-1]:
    if c.power + c.extraPow > 2:
      destroy(c, game.inactivePlayer, game)
      if c.destroyed:
        pendingD.append(c)

  game.pending()

def epic_quest (game, card):
  """ Epic Quest: Archive each friendly Knight creature in play.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]

  for c in active[::-1]:
    if "Knight" in c.traits:
      game.pendingReloc.append(c)
  
  game.pending("archive", target = game.activePlayer)

############
# Creature #
############

def gray_monk (game, card):
  """ Gray Monk: Each other friendly creature has +1 armor.
  """
  for c in game.activePlayer.board["Creature"]:
    if c != card:
      c.extraArm += 1
      c.armor += 1 # because extra armor isn't applied immediately

def horseman_of_death (game, card):
  """ Horseman of Death: Return each Horseman creature from your discard pile to your hand.
  """
  passFunc(game, card)
  discard = game.activePlayer.discard
  hand = game.activePlayer.hand
  for c in discard[::-1]:
    if "Horseman" in c.traits:
      hand.append(c)

def horseman_of_famine (game, card):
  """ Horseman of Famine: Destroy the least powerful creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  low = min(x.power + x.extraPow for x in (active + inactive))
  pendingD = game.pendingReloc

  if not active and not inactive:
    return

  side, choice = game.chooseCards("Creature", "Destroy a creature with the lowest power:", condition = lambda x: x.power + x.extraPow == low, con_message = "That creature does not have the lowest power.")[0]
  if side == "fr":
    card = active[choice]
    destroy(card, game.activePlayer, game)
    if card.destroyed:
      pendingD.append(card)
  else:
    card = inactive[choice]
    destroy(card, game.inactivePlayer, game)
    if card.destroyed:
      pendingD.append(card)
  game.pending()

def horseman_of_pestilence (game, card):
  """ Horseman of Pestilence: Deal 1 damage to each non-Horseman creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active:
    if "Horseman" not in c.traits:
      c.damageCalc(game, 1)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in inactive:
    if "Horseman" not in c.traits:
      c.damageCalc(game, 1)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)

  game.pending()

def horseman_of_war (game, card):
  """ Horseman of War: For the remainder of the turn, each friendly creature can be used as if they were in the active house, but can only fight.
  """
  passFunc(game, card)
  game.extraFightHouses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]

def lady_maxena (game, card):
  """ Lady Maxena: Stun a creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  side, choice = game.chooseCards("Creature", "Stun a creature:")[0]
  if side == "fr":
    active[choice].stun = True
  else:
    inactive[choice].stun = True

def numquid_the_fair (game, card):
  """ Numquid the Fair: Destroy an enemy creature. Repeat this card's effect if your opponent still controls more creatures than you.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  # possible edge case: Numquid hits enemy w/ Phoenix Heart. Numquid then dies and the effect should not repeat. handle this by running pending after each destruction
  while len(inactive) > len(active) and card in active:
    choice = game.chooseCards("Creature", "Destroy an enemy creature:", "enemy")[0][1]
    card = inactive[choice]
    destroy(card, game.inactivePlayer, game)
    if card.destroyed:
      pending.append(card)
    game.pending()

def raiding_knight (game, card):
  """ Raiding Knight: Capture 1 amber.
  """
  passFunc(game, card)
  card.capture(game, 1)

def sergeant_zakiel (game, card):
  """ Sergeant Zakiel: You may ready and fight with a neighboring creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]

  # this can't handle the edge case where zakiel is destroyed upon entering
  if len(activeBoard) <= 1:
    return

  if activeBoard.index(card) == 0:
    maybe = game.chooseHouse("custom", (f"Would you like to ready and fight with {activeBoard[1].title.replace('_', ' ').title()}", ["Yes", "No"]))[0]
    if maybe == "Yes":
      activeBoard[1].ready = True
      game.fightCard(1, cheat=True)
    return
  elif activeBoard.index(card) == len(activeBoard)-1:
    maybe = game.chooseHouse("custom", (f"Would you like to ready and fight with {activeBoard[-2].title.replace('_', ' ').title()}", ["Yes", "No"]))[0]
    if maybe == "Yes":
      activeBoard[-2].ready = True
      game.fightCard(len(activeBoard)-2, cheat=True)
    return

def gatekeeper (game, card):
  """ Gatekeeper: If your opponent has 7 or more amber, capture all but 5 of it.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber >= 7:
    diff = game.inactivePlayer.amber - 5
  card.capture(game, diff)
  pyautogui.alert(card.title + " captured " + str(card.captured) + " amber.")

def veemos_lightbringer (game, card):
  """ Veemos Lightbringer: Destroy each elusive creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active[::-1]:
    if c.elusive:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        pending.append(c)
  for c in inactive[::-1]:
    if c.elusive:
      destroy(c, game.inactivePlayer, game)
      if c.destroyed:
        pending.append(c)
  
  game.pending()

## End house Sanctum

###########
# Shadows #
###########

###########
# Actions #
###########

def bait_and_switch (game, card):
  """ Bait and Switch: If your opponent has more amber than you, steal 1. Repeat the preceding effect if your opponent still has more amber than you.
  """
  passFunc(game, card)
  count = 2
  while count > 0:
    if game.inactivePlayer.amber > game.activePlayer.amber:
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      pyautogui.alert("You steal 1 amber. You now have " + str(game.activePlayer.amber) + " amber.")
      count -= 1
    else:
      break

def booby_trap (game, card):
  """ Booby Trap: Deal 4 damage to a creature that is not on a flank with 2 splash.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  # first check that there are flank creatures to target
  
  if False not in [x.isFlank(game) for x in active + inactive]:
    pyautogui.alert("No valid targets. The card is still played.")
    return

  choice = game.chooseCards("Creature", "Deal 4 damage with 2 splash to a non-flank creature:", condition = lambda x: not x.isFlank(game), con_message = "")[0]
  if choice[0] == "fr":
    card = active[choice[1]]
    card.damageCalc(game, 4)
    for neigh in card.neighbors(game):
      neigh.damageCalc(game, 2)
    for neigh in card.neighbors(game):
      neigh.updateHealth(game.activePlayer)
      if neigh.destroyed:
        pending.append(neigh)
    card.updateHealth(game.activePlayer)
    if card.destroyed:
      pending.append(card)
  else:
    card = inactive[choice[1]]
    card.damageCalc(game, 4)
    for neigh in card.neighbors(game):
      neigh.damageCalc(game, 2)
    for neigh in card.neighbors(game):
      neigh.updateHealth(game.inactivePlayer)
      if neigh.destroyed:
        pending.append(neigh)
    card.updateHealth(game.inactivePlayer)
    if card.destroyed:
      pending.append(card)
  
  game.pending()

def finishing_blow (game, card):
  """ Finishing Blow: Destroy a damaged creature. If you do, steal 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if True not in [x.damage > 0 for x in active + inactive]:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Choose a damaged creature to destroy:", condition = lambda x: x.damage > 0, con_message = "That creature isn't damaged.")[0]

  if side == "fr":
    card = active[choice]
    destroy(card, game.activePlayer, game)
    if card.destroyed:
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      pending.append(card)
  else:
    card = inactive[choice]
    destroy(card, game.inactivePlayer, game)
    if card.destroyed:
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
      pending.append(card)

  game.pending()

def ghostly_hand (game, card):
  """ Ghostly Hand: If your opponent has exactly 1 amber, steal it.
  """
  passFunc(game, card)
  if game.inactivePlayer.amber == 1:
    stealAmber(game.activePlayer, game.inactivePlayer, 1)
    pyautogui.alert("You stole your opponent's only amber, you jerk. You now have " + str(game.activePlayer.amber) + " amber.")
    return
  pyautogui.alert("Your opponent has " + str(game.inactivePlayer.amber) + "amber. You steal nothing.")

def hidden_stash (game, card):
  """ Hidden Stash: Archive a card.
  """
  passFunc(game, card)
  if game.activePlayer.hand:
    archive = game.chooseCards("Hand", "Choose a card from your hand to archive:", "friend")[0][1]
    card = game.activePlayer.hand[archive]
    game.activePlayer.hand.remove(card)
    game.pendingReloc.append(card)
    game.pending("archive", target = game.activePlayer)

def imperial_traitor (game, card):
  """ Imperial Traitor: Look at your opponent's hand. You may choose and purge a Sanctum card in it.
  """
  passFunc(game, card)
  # check for Sanctum card in opp hand
  hand = game.inactivePlayer.hand
  pending = game.pendingReloc
  for card in hand:
    card.revealed = True
  
  if True in [x.house == "Sanctum" for x in hand]:
    choice = game.chooseCards("Hand", "Purge a Sanctum card from your opponent's hand:", "enemy", condition = lambda x: x.house == "Sanctum")[0][1]
    card = hand[choice]
    hand.remove(card)
    pending.append(card)
    game.pending("purge")

  else:
    pyautogui.alert("Your opponent had no Sanctum cards in hand, so you don't get to purge anything.")

def key_of_darkness (game, card):
  """ Key of Darkness: Forge a key at +6 current cost. If your opponent has no amber, forge a key at +2 current cost instead.
  """
  passFunc(game, card)
  # whenever we forge a key, we calculate key cost
  # this will be a function in Game
  if game.inactivePlayer.amber == 0:
    game.forgeKey("active", game.calculateCost() + 2)
  else:
    game.forgeKey("active", game.calculateCost() + 6)

def lights_out (game, card):
  """ Lights Out: Return 2 enemy creature's to their owner's hand.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  count = min(len(inactive), 2)
  if count:
    choices = [x[1] for x in game.chooseCards("Creature", f"Return {count} enemy creatures to their owner's hand:", "enemy", count)]
    for choice in choices:
      card = inactive[choice]
      pending.append(card)
      choice.returned = True
  game.pending('hand')

def miasma (game, card):
  """ Miamsa: Your opponent skips the "forge a key" step on their next turn.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] = 1
  # this one resets in canForge

def nerve_blast (game, card):
  """ Nerve Blast: Steal 1 amber. If you do, deal 2 damage to a creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  orig = game.activePlayer.amber

  stealAmber(game.activePlayer, game.inactivePlayer, 1)
  if game.activePlayer.amber > orig:
    pyautogui.alert("You now have " + game.activePlayer.amber + " amber. Now, deal 2 damage to a creature.")
    side, choice = game.chooseCards("Creature", "Deal 2 damage to a creature:")[0]
    if side == "fr":
      card = active[choice]
      card.damageCalc(game, 2)
      card.updateHealth(game.activePlayer)
      if card.destroyed:
        pending.append(card)
    else:
      card = inactive[choice]
      card.damageCalc(game, 2)
      card.updateHealth(game.inactivePlayer)
      if card.destroyed:
        pending.append(card)
  else:
    pyautogui.alert("You didn't steal any amber, so you don't deal any damage.")
    return
  
  game.pending()

def one_last_job (game, card):
  """ One Last Job: Purge each friendly Shadows creature. Steal 1 amber for each creature purged this way.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  pending = game.pendingReloc
  
  count = 0
  for c in active[::-1]:
    if c.house == "Shadows":
      active.remove(c)
      pending.append(c)
      count += 1
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
    game.pending("purge")

  pyautogui.alert("You may have stolen some amber.")

def oubliette (game, card):
  """ Oubliette: Purge a creature with power 3 or lower.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if True not in [x.power + x.extraPow > 2 for x in active + inactive]:
    pyautogui.alert("No valid targets.")
    return
  
  side, choice = game.chooseCards("Creature", "Purge a creature with 3 or less power.", condition = lambda x: x.power + x.extraPow > 2, con_message = "That creature has less than 3 power.")[0]
  if side == "fr":
    card = active[choice]
    game.pendingReloc.append(card)
    active.remove(card)
  else:
    card = inactive[choice]
    game.pendingReloc.append(card)
    inactive.remove(card)
  
  game.pending("purge")
  
def pawn_sacrifice (game, card):
  """ Pawn Sacrifice: Sacrifice a friendly creature. If you do, deal 3 damage each to 2 creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not active:
    pyautogui.alert("You have no friendly creatures to sacrifice.")
    return
  
  choice = game.chooseCards("Creature", "Choose a friendly creature to sacrifice:", "friend")[0][1]
  card = active[choice]
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    pending.append(card)
    game.pending()
  else:
    return

  count = min(2, len(inactive) + len(active))
  targets = game.chooseCards("Creature", f"Choose {count} minions to deal 3 damage to:")
  for side, target in targets:
    if side == "fr":
      card = active[target]
      card.damageCalc(game, 3)
      card.updateHealth(game.activePlayer)
      if card.destroyed:
        pending.append(card)
    else:
      card = inactive[target]
      card.damageCalc(game, 3)
      card.updateHealth(game.inactivePlayer)
      if card.destroyed:
        pending.append(card)
  
  game.pending()

def poison_wave (game, card):
  """ Poison Wave: Deal 2 damage to each creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc
  
  for c in active:
    c.damageCalc(game, 2)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pendingDisc.append(c)
  for c in inactive:
    c.damageCalc(game, 2)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pendingDisc.append(c)

  game.pending()

def relentless_whispers (game, card):
  """ Relentless Whispers: Deal 2 damage to a creature. If this damage destroys that creature, steal 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not len(active) + len(inactive):
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 2 damage to a creature. If this damage destroys that creature, steal 1 amber:")[0]
  if side == "fr":
    card = active[choice]
    card.damageCalc(game, 2)
    card.updateHealth(game.activePlayer)
    if card.destroyed:
      pending.append(card)
      stealAmber(game.activePlayer, game.inactivePlayer, 1)
  else:
    card = inactive[choice]
    card.damageCalc(game, 2)
    card.updateHealth(game.inactivePlayer)
    if card.destroyed:
      pending.append(card)
      stealAmber(game.activePlayer, game.inactivePlayer, 1)

  game.pending()

def routine_job (game, card):
  """ Routine Job: Steal 1 amber. Then, steal 1 amber for each copy of Routine Job in your discard pile.
  """
  passFunc(game, card)
  stealAmber(game.activePlayer, game.inactivePlayer, 1)
  
  for c in game.activePlayer.discard:
    if c.title == card.title:
      stealAmber(game.activePlayer, game.inactivePlayer, 1)

def too_much_to_protect (game, card):
  """ Too Much to Protect: Steal all but 6 of your opponent's amber.
  """
  passFunc(game, card)
  diff = 0
  if game.inactivePlayer.amber > 6:
    diff = game.inactivePlayer.amber - 6
    stealAmber(game.activePlayer, game.inactivePlayer, diff)

def treasure_map (game, card):
  """ Treasure Map: If you have not played any other cards this turn, gain 3 amber. For the remainder of the turn, you cannot play cards.
  """
  passFunc(game, card)
  if len(game.playedThisTurn) - 1 == 0:
    game.activePlayer.gainAmber(3, game)
    pyautogui.alert("You gained 3 amber. You now have " + str(game.activePlayer.amber) + " amber.")
  game.activePlayer.states[card.title] = 1

def masterplan (game, card):
  """ Masterplan: Put a card from your hand facedown beneath Masterplan.
  """
  passFunc(game, card)
  hand = game.activePlayer.hand

  if len(hand):
    choice = game.chooseCards("Hand", "Put a card facedown beneath Masterplan.", "friend")[0][1]
    c = hand[choice]
    hand.remove(c)
    card.upgrade.append(c) # not going to use pendingReloc for this one, going to cheat and use upgrade

#############
# Creatures #
#############

def magda_the_rat (game, card):
  """ Magda the Rat: Steal 2 amber.
  """
  passFunc(game, card)
  stealAmber(game.activePlayer, game.inactivePlayer, 2)

def old_bruno (game, card):
  """ Old Bruno: Capture 3 amber.
  """
  passFunc(game, card)
  card.capture(game, 3)

def sneklifter(game, card):
  """ Sneklifter: Take control of an enemy artifact. While under your control, if it does not belong to one of your three houses, it is considered to be of house Shadows.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]

  if len(inactive) == 0:
    pyautogui.alert("Your opponent has no artifacts for you to steal.")
    return
  choice = game.chooseCards("Artifact", "Steal an enemy artifact:", "enemy")[0][1]
  c = inactive[choice]
  inactive.remove(c)
  if c.house not in game.activePlayer.houses:
    c.house = "Shadows"
  active.append(c)

def urchin (game, card):
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

def cooperative_hunting (game, card):
  """ Cooperative Hunting: Deal 1 damage for each friendly creature in play. You may divide this damage among any number of creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  friend_damaged = []
  enemy_damaged = []

  count = len(active)
  if count == 0:
    pyautogui.alert("You have no creatures, so no damage is dealt.")
    return
  hits = 1
  while hits <= count:
    side, choice = game.chooseCards("Creature", f"Deal 1 damage to a creature ({hits} of {count}):")[0]
    if side == "fr":
      c = active[choice]
      if c not in friend_damaged:
        friend_damaged.append(c)
      c.damageCalc(game, 1)
    else:
      c = inactive[choice]
      if c not in enemy_damaged:
        enemy_damaged.append(c)
      c.damageCalc(game, 1)
    hits += 1
  for c in friend_damaged:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in enemy_damaged:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  game.pending()

def curiosity (game, card):
  """ Curiosity: Destroy each Scientist creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active[::-1]:
    if "Scientist" in c.traits:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        pending.append(c)
  for c in inactive[::-1]:
    if "Scientist" in c.traits:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        pending.append(c)
  
  game.pending()

def fertility_chant (game, card):
  """ Fertility Chant: Your opponent gains 2 amber.
  """
  passFunc(game, card)
  game.inactivePlayer.gainAmber(2, game)
  pyautogui.alert("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def fogbank (game, card):
  """ Fogbank: Your opponent cannot use creatures to fight on their next turn.
  """
  passFunc(game, card)
  # states should always be in deck that they affect
  game.activePlayer.states[card.title] = 1
  game.resetStatesNext.append(("i", card.title))

def full_moon (game, card):
  """ Full Moon: For the remainder of the turn, gain 1 amber each time you play a creature.
  """
  passFunc(game, card)
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))
  # should be able to account for multiple instances of full 
  
def grasping_vines (game, card):
  """ Grasping Vines: Return up to 3 artifacts to their owners' hands.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]
  pending = game.pendingReloc

  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return

  choices = game.chooseCards("Artifact", "Return up to 3 artifacts to their owner's hands:", count = 3, full = False)
  for side, target in choices:
    if side == "fr":
      c = active[target]
      active.remove(c)
      pending.append(c)
    else:
      c = inactive[target]
      inactive.remove(c)
      pending.append(c)

  game.pending('hand')

def key_charge (game, card):
  """ Key Charge: Lost 1 amber. If you do, you may forge a key at current cost.
  """
  passFunc(game, card)
  game.activePlayer.amber -= 1
  
  temp_cost = game.calculateCost()
  if game.canForge() and game.activePlayer.amber >= temp_cost:
    forge = game.chooseHouse("custom", (f"You may now forge a key for {temp_cost} amber. Would you like to do so?", ["Yes", "No"]))[0]
    if forge == "No":
      pyautogui.alert("You have chosen not to forge a key.")
      return
    game.forgeKey("active", temp_cost)
    if game.activePlayer.keys >= 3:
      pyautogui.alert(f"{game.activePlayer.name} wins!")
      pygame.quit()
  elif game.canForge():
    pyautogui.alert("You don't have enough amber to forge a key.")
  else:
    pyautogui.alert("You are unable to forge a key right now for some reason.")

def lifeweb (game, card):
  """ Lifeweb: If your opponent played 3 or more creatures on their previous turn, steal 2 amber.
  """
  passFunc(game, card)
  # implement tracking how many creatures opponent played last turn
  # if a deck has lifeweb in it, it will set Lifeweb in states to [True, 0]. Whenever the opponent plays a creature, it will be incremented.
  if sum(x.type == "Creature" for x in game.playedLastTurn) > 2:
    stealAmber(game.activePlayer, game.inactivePlayer, 2)
    pyautogui.alert("Your opponent played enough creatures last turn, so you stole 2 amber.")
    return
  pyautogui.alert("Your opponent did not play enough creatures last turn, so you steal no amber.")

def lost_in_the_woods (game, card):
  """ Lost in the Woods: Choose 2 friendly creatures and 2 enemy creatures. Shuffle each chosen creature into its owner's deck.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  f_choices = [x[1] for x in game.chooseCards("Creature", "Choose two friendly creatures to shuffle into their owner's deck:", condition = lambda x: x in active)].sort()
  e_choices = [x[1] for x in game.chooseCards("Creature", "Choose two enemy creatures to shuffle into their owner's deck:", condition = lambda x: x in inactive)].sort()
  for choice in f_choices[::-1]:
    c = active[choice]
    active.remove(c)
    pending.append(c)
  for choice in e_choices[::-1]:
    c = inactive[choice]
    inactive.remove(c)
    pending.append(c)
  game.pending("deck")
  
  random.shuffle(game.activePlayer.deck)
  random.shuffle(game.inactivePlayer.deck)

def mimicry (game, card):
  """ Mimicry: When you play this card, treat it as a copy of an action card in your opponent's discard pile.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.discard
  options = sum(x.type == "Action" for x in inactive)
  if not options:
    pyautogui.alert("No Actions in your opponent's discard.")
    return
  game.drawEnemyDiscard = True
  choice = game.chooseCards("Discard", "Choose an enemy action", "enemy", condition = lambda x: x.type == "Action", con_message = "That's not an action card.")[0][1]
  game.inactivePlayer.discard[choice].play(game, game.inactivePlayer.discard[choice])
  game.cardChanged()
  

def natures_call (game, card):
  """ Nature's Call: Return up to 3 creatures to their owners' hands.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return

  choices = game.chooseCards("Creature", "Return up to 3 creatures to their owner's hands:", count = 3, full = False).sort(key = lambda x: x[1], reverse = True)
  for side, target in choices:
    if side == "fr":
      c = active[target]
      c.returned = True
      pending.append(c)
    else:
      c = inactive[target]
      c.returned = True
      pending.append(c)
  
  game.pending('hand')

def nocturnal_maneuver (game, card):
  """ Nocturnal Maneuver: Exhaust up to 3 creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return
  
  choices = game.activePlayer("Creature", "Exhaust up to 3 creatures:", count = 3, full = False).sort(key = lambda x: x[1], reverse = True)
  for side, target in choices:
    if side == "fr":
      c = active[target]
    else:
      c = inactive[target]
    c.ready = False

def perilous_wild (game, card):
  """ Perilous Wild: Destroy each elusive creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active[::-1]:
    if c.elusive:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        pending.append(c)
  for c in inactive[::-1]:
    if c.elusive:
      destroy(c, game.inactivePlayer, game)
      if c.destroyed:
        pending.append(c)
  
  game.pending()

def regrowth (game, card):
  """ Regrowth: Return a creature from your discard pile to your hand.
  """
  passFunc(game, card)
  active = game.activePlayer.discard
  options = sum(x.type == "Creature" for x in active)

  if not options:
    pyautogui.alert("No creatures in your discard.")
    return

  choice = game.chooseCard("Discard", "Return a creature from your discard pile to your hand:", "friend", condition = lambda x: x.type == "Creature", con_message = "That's not a creature.")[0][1]
  # I can skip pending b/c this card is guaranteed to belong to the active player
  c = active[choice]
  active.remove(c)
  game.activePlayer.hand.append(c)

def save_the_pack (game, card):
  """ Save the Pack: Destroy each damaged creature. Gain 1 chain.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  
  for c in active[::-1]:
    if c.damage > 0:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        active.remove(c)
        pending.append(c)
  for c in inactive[::-1]:
    if c.damage > 0:
      destroy(c, game.activePlayer, game)
      if c.destroyed:
        active.remove(c)
        pending.append(c)
    
  game.pending()
  game.activePlayer.chains += 1
  game.setKeys()

def scout (game, card):
  """ Scout: For the remainder of the turn, up to 2 friendly creatures gain skirmish. Then, fight with those creatures one at a time.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  
  if not active:
    pyautogui.alert("No friendly creatures.")
    return

  choices = [active[x[1]] for x in game.chooseCards("Creature", "Choose up to 2 friendly creatures to gain skirmish:", "friend", count = 2, full = False)]
  for choice in choices:
    choice.temp_skirmish = True
  ready = sum(x.ready for x in choices)
  if ready > 1:
    first = [active[x[1]] for x in game.chooseCards("Creature", "Choose which one will fight first:", "friend", condition = lambda x: x in choices, con_message = "That's not one the creatures you gave skirmish too.")]
    game.fightCard(active.index(first), cheat = True)
    choices.remove(first)
    game.fightCard(active.index(choices[0]), cheat = True)
  elif ready:
    for choice in choices:
      if choice.ready:
        pyautogui.alert(f"Fighting with {choice.title.replace('_', ' ').title()}")
        game.fightCard(active.index(choice), cheat = True)
  else:
    pyautogui.alert("Neither of your cards were ready, so neither of them fought.")
    

def stampede (game, card):
  """ Stampede: If you used 3 or more creatures this turn, steal 2 amber.
  """
  passFunc(game, card)
  if sum(x.type == "Creature" for x in game.usedThisTurn) > 2:
    pyautogui.alert("You have used at least 3 creatures this turn, so you steal 2 amber.")
    stealAmber(game.activePlayer, game.inactivePlayer, 2)
    return
  pyautogui.alert("You have used less than 3 creatures this turn, so you steal no amber. The card is still played.")

def the_common_cold (game, card):
  """ The Common Cold: Deal 1 damage to each creature. You may destroy all Mars creatures.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  # deal 1 damage to everything
  for c in active:
    c.damageCalc(game, 1)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in inactive:
    c.damageCalc(game, 1)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  game.pending()
  game.cardChanged()

  mars = sum(x.house == "Mars" for x in active + inactive)
  if not mars:
    pyautogui.alert("No Mars creatures to destroy")
    return

  destroy = game.chooseHouse("custom", (f"Would you like to destroy all {mars} Mars creatures?", ["Yes", "No"]), highlight = "Mars")[0]
  if destroy == "Yes":
    for c in active[::-1]:
      if c.house == "Mars":
        destroy(c, game.activePlayer, game)
        if c.destroyed:
          pending.append(c)
    for c in inactive[::-1]:
      if c.house == "Mars":
        destroy(c, game.inactivePlayer, game)
        if c.destroyed:
          pending.append(c)
  game.pending()

def troop_call (game, card):
  """ Troop Call: Return each friendly Niffle creature from your discard pile and from play to your hand.
  """
  passFunc(game, card)
  disc = game.activePlayer.discard
  active = game.activePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in disc:
    if "Niffle" in c.traits:
      disc.remove(c)
      pending.append(c)
  for c in active:
    if "Niffle" in c.traits:
      c.returned = True
      pending.append(c)
  
  game.pending('hand')

def vigor (game, card):
  """ Vigor: Heal up to 3 damage from a creature. If you healed 3 damage, gain 1 amber.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  side, choice = game.chooseCards("Creature", "Heal up to three damage from a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  heal = int(game.chooseHouse("custom", ("How much damage would you like to heal?", list(range(min(c.damage + 1, 4)))))[0])
  c.damage -= heal
  if heal == 3:
    game.activePlayer.gainAmber(1, game)

def word_of_returning (game, card):
  """ Word of Returning: Deal 1 damage to each enemy for each amber on it. Return all amber from those creatures to your pool.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in inactive:
    c.damageCalc(game, c.captured)
    game.activePlayer.gainAmber(c.captured)
    c.captured = 0
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  game.pending()

#############
# Creatures #
#############

def chota_hazri (game, card):
  """ Chota Hazri: Lose 1 amber, if you do, you may forge a key at current cost.
  """
  passFunc(game, card)
  game.activePlayer.amber -= 1
  
  temp_cost = game.calculateCost()
  if game.canForge() and game.activePlayer.amber >= temp_cost:
    forge = game.chooseHouse("custom", (f"You may now forge a key for {temp_cost} amber. Would you like to do so?", ["Yes", "No"]))[0]
    if forge == "No":
      pyautogui.alert("You have chosen not to forge a key.")
      return
    game.forgeKey("active", temp_cost)
    if game.activePlayer.keys >= 3:
      pyautogui.alert(f"{game.activePlayer.name} wins!")
      pygame.quit()
  elif game.canForge():
    pyautogui.alert("You don't have enough amber to forge a key.")
  else:
    pyautogui.alert("You are unable to forge a key right now for some reason.")

def flaxia (game, card):
  """ Flaxia: If you control more creatures than your opponent, gain 2 amber.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  active = game.activePlayer.board["Creature"]

  if len(active) > len(inactive):
    game.activePlayer.gainAmber(2, game)
    pyautogui.alert("You control more creatures than your opponent, so you gain 2 amber. You now have " + str(game.activePlayer.amber) + " amber.")

def fuzzy_gruen (game, card):
  """ Fuzzy Gruen: Your opponent gains 1 amber.
  """
  passFunc(game, card)
  game.inactivePlayer.gainAmber(1, game)
  pyautogui.alert("Your opponent now has " + str(game.inactivePlayer.amber) + " amber.")

def inka_the_spider (game, card):
  """ Inka the Spider: Stun a creature.
  """
  passFunc(game, card)
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  
  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Stun a creature:")[0]

  if side == "fr":
    activeBoard[choice].stun = True
  else:
    inactiveBoard[choice].stun = True

def lupo_the_scarred (game, card):
  """ Lupo the Scarred: Deal 2 damage to an enemy creature.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not inactive:
    pyautogui.alert("There are no enemy creatures to damage. The card is still played.")
    return
  choice = game.chooseCards("Creature", "Deal 2 damage to an enemy creature:", "enemy")[0][1]
  c = inactive[choice]
  c.damageCalc(game, 2)
  c.updateHealth()
  if c.destroyed:
    pending.append(c)
    
  game.pending()

def mighty_tiger (game, card):
  """ Mighty Tiger: Deal 4 damage to an enemy creature.
  """
  passFunc(game, card)
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  if not inactive:
    pyautogui.alert("There are no enemy creatures to damage. The card is still played.")
    return
  choice = game.chooseCards("Creature", "Deal 4 damage to an enemy creature:", "enemy")[0][1]
  c = inactive[choice]
  c.damageCalc(game, 4)
  c.updateHealth()
  if c.destroyed:
    pending.append(c)
  game.pending()

def piranha_monkeys (game, card):
  """ Piranha Monkeys: Deal 2 damage to each other creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  
  for c in active:
    if c != card:
      c.damageCalc(game, 2)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in inactive:
    c.damageCalc(game, 2)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  
  game.pending()


## End house Untamed

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly') 