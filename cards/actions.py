import random, pyautogui, pygame, logging
from helpers import stealAmber, destroy, return_card
from cards.reap import spectral_tunneler as st

###########
# Brobnar #
###########

def cannon (game, card):
  """Cannon: Deal 2 damage to a creature.
  """
  logging.info(f"Using {card.title}'s action.")
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc # fine b/c only one side ever affected

  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets. The card is still played.")
    return

  side, choice = game.chooseCards("Creature", "Deal 2 damage to a creature:")[0]
  if side == "fr":
    c = activeBoard[choice]
  else:
    c = inactiveBoard[choice]
  c.damageCalc(game, 2)
  c.updateHealth(game.inactivePlayer)
  if c.destroyed:
    pendingDiscard.append(c)
  game.pending()

def gauntlet_of_command (game, card):
  """Gauntlet of Command: Ready and fight with a friendly creature.
  """
  logging.info(f"Using {card.title}'s action.")
  if not game.activePlayer.board["Creature"]:
    pyautogui.alert("No valid targets. The card is still played.")
    return
  
  choice = game.chooseCards("Creature", "Choose a friendly creature:", "friend")[0][1]
  if not game.activePlayer.board["Creature"][choice].ready:
    game.activePlayer.board["Creature"][choice].ready = True
    game.fightCard(choice, cheat=True)
  else:
    game.fightCard(choice, cheat=True)

def omni_mighty_javelin (game, card):
  """Might Javelin: Sacrific Mighty Javelin. Deal 4 damage to a creature.
  """
  logging.info(f"Using {card.title}'s action.")
  activeBoard = game.activePlayer.board["Creature"]
  inactiveBoard = game.inactivePlayer.board["Creature"]
  
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  
  if not activeBoard and not inactiveBoard:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 4 damage to a creature:")[0]
  if side == "fr":
    c = activeBoard[choice]
  else:
    c = inactiveBoard[choice]
  c.damageCalc(game, 4)
  c.updateHealth(game.inactivePlayer)
  if c.destroyed:
    game.pendingReloc.append(c)
  game.pending()

def omni_screechbomb (game, card):
  """Screechbomb: Sacrifice Screechbomb. Your opponent loses 2 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.inactivePlayer.amber -= min(2, game.inactivePlayer.amber)
  game.pending()

def the_warchest (game, card):
  """The Warchest: Gain 1 amber for each enemy creature that was destroyed in a fight this turn.
  """
  logging.info(f"Using {card.title}'s action.")
  game.activePlayer.gainAmber(len(game.destInFight), game)

#######
# Dis #
#######

def dominator_bauble (game, card):
  """ Dominator Bauble: Use a friendly creature.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]

  if not active:
    pyautogui.alert("No valid targets.")
    return

  choice = active[game.chooseCards("Creature", "Use a friendly creature:", "friend")[0][1]]
  
  if not choice.ready:
    pyautogui.alert("Card isn't ready, so can't be used.")
    return

  uses =  []
  if game.canReap(card, r_click = True, cheat = True):
    uses.append("Reap")
  if game.canFight(card, r_click = True, cheat = True):
    uses.append("Fight")
  if game.canAction(card, r_click = True, cheat = True):
    uses.append("Action/Omni")
  
  if not uses:
    return ("No valid uses for this card.")
  
  use = game.chooseHouse("custom", ("How would you like to use this creature?", uses))[0]
  if use[0] == "R":
    game.reapCard(choice, cheat = True)
  elif use[0] == "F":
    game.fightCard(choice, cheat=True)
  elif use[0] == "A":
    game.actionCard(choice, cheat = True)

def omni_key_to_dis (game, card):
  """ Key to Dis: Destroy each creature.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)

  for c in active + inactive:
    destroy(c, game.activePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()

def lash_of_broken_dreams (game, card):
  """ Lash of Broken Dreams: Keys cost +3 amber during your opponent's next turn.
  """
  logging.info(f"Using {card.title}'s action.")
  game.activePlayer.states[card.title] += 1
  game.resetStatesNext.append(("i", card.title))

def library_of_the_damned (game, card):
  """ Library of the Damned: Archive a card.
  """
  logging.info(f"Using {card.title}'s action.")
  if game.activePlayer.hand:
    archive = game.chooseCards("Hand", "Choose a card from your hand to archive:")[0][1]
    card = game.activePlayer.hand[archive]
    game.pendingReloc.append(card)
    game.activePlayer.hand.remove(card)
    game.pending("archive", target = game.activePlayer)

def omni_lifeward (game, card):
  """ Lifeward: Sacrific Lifeward. Your opponent canno play creatures on their next turn.
  """
  logging.info(f"Using {card.title}'s action.")
  game.activePlayer.states[card.title] = 1
  game.resetStatesNext.append(("i", card.title))

def sacrificial_altar (game, card):
  """ Sacrificial Altar: Purge a friendly human creature from play. If you do, play a creature from your discard pile.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  discard = game.activePlayer.discard
  count = sum("Human" in x.traits for x in active)

  if not count:
    pyautogui.alert("No valid targets.")
    return
  if not sum(x.type == "Creature" and game.canPlay(x, reset = False, cheat = True) for x in discard):
    pyautogui.alert("No playable creatures in your discard.")
    return
  
  c = active[game.chooseCards("Creature", "Purge a friendly human creature:", "friend", condition = lambda x: "Human" in x.traits, con_message = "That's not a human.")[0][1]]
  game.drawFriendDiscard = True
  cheat = discard[game.chooseCards("Discard", "Play a creature from your discard:", "friend", lambda x: game.canPlay(x, reset = False, cheat = True) and x.type == "Creature", con_message = "That's not a creature, or it is a creature you can't play right now.")[0][1]]

  return_card(c, game.activePlayer, game)
  if c.returned:
    game.pendingReloc.append(c)
    play = True
  game.pending("purge")

  if play:
    discard.remove(cheat)
    game.activePlayer.hand.append(cheat)
    game.playCard(-1, cheat = True)

def screaming_cave (game, card):
  """ Screaming Cave: Shuffle your hand and discard pile into your deck.
  """
  logging.info(f"Using {card.title}'s action.")
  hand = game.activePlayer.hand
  discard = game.activePlayer.discard

  for c in hand[::-1]:
    discard.append(c)
    hand.remove(c)
  
  game.activePlayer.shuffleDiscard()

def pit_demon (game, card):
  """ Pit Demon: Steal 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  stealAmber(game.activePlayer, game.inactivePlayer, 1, game)
  
#########
# Logos #
#########

def anomaly_exploiter (game, card):
  """ Anomaly Exploiter: Destroy a damaged creature.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if not sum(x.damage > 0 for x in active + inactive):
    pyautogui.alert("No damaged creatures.")
    return

  side, choice = game.chooseCards("Creature", "Destroy a damaged creature:", condition = lambda x: x.damage > 0, con_message = "That creature is not damaged.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]

  destroy(c, game.activePlayer, game)
  if c.destroyed:
    game.pendingReloc.append(c)
  game.pending()

def chaos_portal (game, card):
  """ Chaos Portal: Choose a house. Reveal the top card of your deck. If it is of that house, play it.
  """
  logging.info(f"Using {card.title}'s action.")
  deck = game.activePlayer.deck
  house = game.chooseHouse("other")
  deck[-1].revealed = True

  if deck[-1].house == house:
    game.activePlayer.hand.append(deck.pop())
    game.playCard(-1, cheat = True)
  else:
    pyautogui.alert(f"{deck[-1].title.replace('_', ' ').title()} is not of house {house}, and is not played.")

def crazy_killing_machine (game, card):
  """ Crazy Killing Machine: Discard the top card of each player’s deck. For each of those cards, destroy a creature or artifact of that card’s house, if able. If 2 cards are not destroyed as a result of this, destroy Crazy Killing Machine.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board
  inactive = game.inactivePlayer.board
  activeD = game.activePlayer.deck
  inactiveD = game.inactivePlayer.deck
  count = 0

  if activeD:
    game.activePlayer.discard.append(activeD.pop())
    pyautogui.alert(f"Discarded {game.activePlayer.discard[-1].title.replace('_', ' ').title()}")
    aDiscard = game.activePlayer.discard[-1].title
  else:
    pyautogui.alert(f"Your deck is empty, no card is discarded.")
    aDiscard = False
  if inactiveD:
    game.inactivePlayer.discard.append(inactiveD.pop())
    pyautogui.alert(f"Discarded {game.inactivePlayer.discard[-1].title.replace('_', ' ').title()}")
    iDiscard = game.inactivePlayer.discard[-1].title
  else:
    pyautogui.alert(f"Your opponent's deck is empty, no card is discarded.")
    iDiscard = False

  if inactive and iDiscard:
    targetType = game.chooseHouse("custom", (f"Would you like to target an artifact or a creature of house {iDiscard.house}?", ["Artifact", "Creature"]))[0]
    side, choice = game.chooseCards(targetType, f"Choose a(n) {iDiscard.house} {targetType.lower()} to destroy:", condition = lambda x: x.house == iDiscard.house, con_message = "That's not of the right house.")[0]
    if side == "fr":
      card1 = active[choice]
    else:
      card1 = inactive[choice]
    destroy(card1, game.inactivePlayer, game)
    if card1.destroyed:
      game.pendingReloc.append(card1)
      count += 1
  if active and aDiscard:
    targetType2 = game.chooseHouse("custom", (f"Would you like to target an artifact or a creature of house {aDiscard.house}?", ["Artifact", "Creature"]))[0]
    side, choice = game.chooseCards(targetType2, f"Choose a(n) {aDiscard.house} {targetType2.lower()} to destroy:", condition = lambda x: x.house == aDiscard.house, con_message = "That's not of the right house.")[0][1]
    if side == "fr":
      card2 = active[choice]
    else:
      card2 = inactive[choice]
    destroy(card2, game.inactivePlayer, game)
    if card2.destroyed:
      game.pendingReloc.append(card2)
      count += 1
  game.pending()

  if count < 2:
    if card in active["Artifact"]:
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        game.pendingReloc.append(card)
      game.pending()

def library_of_babble (game, card):
  """ Library of Babble: Draw a card.
  """
  logging.info(f"Using {card.title}'s action.")
  game.activePlayer += 1

def mobius_scroll (game, card):
  """ Mobius Scroll: Archive Mobius Scroll and up to 2 cards from your hand.
  """
  logging.info(f"Using {card.title}'s action.")
  hand = game.activePlayer.hand
  return_card(card)
  if card.returned:
    game.pendingReloc.append(card)

  if hand:
    archive = [x[1] for x in game.chooseCards("Hand", "Choose up to 2 cards from your hand to archive:", count = 2, full = False)[0]]
    for a in archive:
      c = game.activePlayer.hand[a]
      game.pendingReloc.append(c)
      game.activePlayer.hand.remove(c)

  game.pending("archive", target = game.activePlayer)

def pocket_universe (game, card):
  """ Pocket Universe: Move 1 amber from your pool to Pocket Universe.
  """
  logging.info(f"Using {card.title}'s action.")
  if game.activePlayer.amber:
    logging.info(f"{card.title} gains 1 amber from the active Player's pool.")
    card.captured += 1
    game.activePlayer.amber -= 1

def spangler_box (game, card):
  """ Spangler Box: Purge a creature in play. If you do, your opponent gains control of Spangler Box. If Spangler Box leaves play, return to play all cards purged by Spangler Box.
  """
  logging.info(f"Using {card.title}'s action.")
  # card.spangler will exist
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if not active + inactive:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Purge a creature in play:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  return_card(c, game)
  if c.returned:
    game.pendingReloc.append(c)
    card.spangler.append(c)
  game.pending("purge")
  
def spectral_tunneler (game, card):
  """ Spectral Tunneler: Choose a creature. For the remainder of the turn, that creature is considered a flank creature and gains, “Reap: Draw a card.”
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  side, choice = game.chooseCards("Creature", "Purge a creature in play:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if not game.activePlayer.states[card.title]:
    game.activePlayer.states[card.title] = [c]
  else:
    game.activePlayer.states[card.title].append(c)
  c.reap.append(st)
  game.resetCard.append((c, "st"))

def novu_archaeologist (game, card):
  """ Novu Archaeologist: Archive a card from your discard pile.
  """
  logging.info(f"Using {card.title}'s action.")
  discard = game.activePlayer.discard

  if discard:
    archive = game.chooseCards("Discard", "Choose a card from your hand to archive:", "friend")[0][1]
    card = discard[archive]
    game.activePlayer.archive.append(card)
    discard.remove(card) # not using pending because no need to reset card in any way

def timetraveller (game, card):
  """ Timetraveller: Shuffle Timetraveller into your deck.
  """
  logging.info(f"Using {card.title}'s action.")
  return_card(card, game)
  if card.returned:
    game.pendingReloc.append(card)
  game.pending("deck")

  if card in game.activePlayer.deck:
    random.shuffle(game.activePlayer.deck) 
  else:
    random.shuffle(game.inactivePlayer.deck) # I think this is how you would handle it?

def transposition_sandals (game, card):
  """ Transposition Sandals: Swap this creature with another friendly creature in the battleline. You may use that creature this turn.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]

  if len(active) < 2:
    pyautogui.alert("No creatures to swap with.")
    return
  
  choice = active[game.chooseCards("Creature", "Swap positions with another friendly creature in your battleline. You can use that card this turn.", "friend", condition = lambda x: x != card)[0][1]]
  sg_i = active.index(card)
  other_i = active.index(choice)
  active[sg_i], active[other_i] = active[other_i], active[sg_i]

  if not game.activePlayer.states[card.title]:
    game.activePlayer.states[card.title] = [choice]
  else:
    game.activePlayer.states[card.title].append(choice)
  game.resetStates(("a", card.title))

########
# Mars #
########

def omni_combat_pheromones (game, card):
  """ Sacrifice Combat Pheromones. You may use up to 2 other Mars cards this turn.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()
  game.activePlayer.states[card.title] += 2
  game.resetStates(("a", card.title))

def commpod (game, card):
  """ Reveal any number of Mars cards from your hand. For each card revealed this way, you may ready one Mars creature.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  revealed = [x[1] for x in game.chooseCards("Hand", "Reveal any number of Mars cards from your hand:", count = max(1, sum(x.house == "Mars" for x in game.activePlayer.hand)), full = False, condition = lambda x: x.house == "Mars", con_message = "That's not a Mars card. Please pick again.")]
  count = len(revealed)
  if count == 0:
    pyautogui.alert("You revealed no Mars cards, so no damage is dealt. The card is still played.")
    return
  readied = game.chooseCards("Creature", f"Ready up to {count} Mars creatures:", count = count, full = False, condition = lambda x: x.house == "Mars", con_message = "That's not a Mars card. Please pick again.")
  for side, choice in readied:
    if side == "fr":
      c = active[choice]
    else:
      c = inactive[choice]
    c.ready = True

def crystal_hive (game, card):
  """ Crystal Hive: For the remainder of the turn, gain 1 amber each time a creature reaps.
  """
  logging.info(f"Using {card.title}'s action.")
  game.activePlayer.states[card.title] += 1
  game.resetStates(("a", card.title))

def omni_custom_virus (game, card):
  """ Custom Virus: Sacrifice Custom Virus. Purge a creature from your hand. Destroy each creature that shares a trait with the purged creature.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()
  
  hand = game.activePlayer.hand
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if not sum(x.type == "Creature" for x in hand):
    pyautogui.alert("No creatures in your hand")
    return

  choice = hand[game.chooseCards("Hand", "Purge a creature from your hand:", condition = lambda x: x.type == "Creature", con_message = "That's not a creature.")[0][1]]
  game.activePlayer.purged.append(choice)
  hand.remove(choice) # no need for pending b/c don't need it reset
  traits = [x for x in choice.traits.split() if len(x) > 2]
  
  for c in active + inactive:
    for tr in traits:
      if tr in c.traits:
        destroy(c, game.activePlayer, game)
        if c.destroyed:
          game.pendingReloc.append(c)
        break # if it matches two traits, we don't destroy it twice (ie ward)
  game.pending()

def feeding_pit (game, card):
  """ Feeding Pit: Discard a creature card from your hand. If you do, gain 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  hand = game.activePlayer.hand
  if not sum(x.type == "Creature" for x in hand):
    pyautogui.alert("No creatures in your hand")
    return

  choice = hand[game.chooseCards("Hand", "Discard a creature from your hand:", condition = lambda x: x.type == "Creature", con_message = "That's not a creature.")[0][1]]
  game.activePlayer.discard.append(choice)
  hand.remove(choice)
  game.activePlayer.gainAmber(1, game)

def omni_incubation_chamber (game, card):
  """ Incubation Chamber: Reveal a Mars creature from your hand. If you do, archive it.
  """
  logging.info(f"Using {card.title}'s action.")
  hand = game.activePlayer.hand
  
  if not sum(x.type == "Creature" and x.house == "Mars" for x in hand):
    pyautogui.alert("No Mars creatures in your hand")
    return

  choice = hand[game.chooseCards("Hand", "Reveal a Mars creature from your hand:", condition = lambda x: x.type == "Creature" and x.house == "Mars", con_message = "That's not a Mars creature.")[0][1]]
  game.activePlayer.archive.append(choice)
  hand.remove(choice) # no need to use pending because no need to reset

def invasion_portal (game, card):
  """ Invastion Portal: Discard cards from the top of your deck until you discard a Mars creature or run out of cards. If you discard a Mars creature this way, put it into your hand.
  """
  logging.info(f"Using {card.title}'s action.")
  discard = game.activePlayer.discard
  deck = game.activePlayer.deck
  hand = game.activePlayer.hand
  while deck and (deck[-1].house != "Mars" or deck[-1].type != "Creature"):
    discard.append(deck.pop())
  if not deck:
    pyautogui.alert("Your deck is empty, and you found no Mars creatures.")
  else: # House is mars and type is creature if we get here
    hand.append(deck.pop())

def mothergun (game, card):
  """ Mothergun: Reveal any number of Mars cards from your hand. Deal damage to a creature equal to the number of Mars cards revealed this way.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  revealed = [x[1] for x in game.chooseCards("Hand", "Reveal any number of Mars cards from your hand:", count = max(1, sum(x.house == "Mars" for x in game.activePlayer.hand)), full = False, condition = lambda x: x.house == "Mars", con_message = "That's not a Mars card. Please pick again.")]
  damage = len(revealed)
  if damage == 0:
    pyautogui.alert("You revealed no Mars cards, so no damage is dealt.")
    return

  if not active + inactive:
    pyautogui.alert("No valid targets.")
    return
  side, choice = game.chooseCards("Creature", f"Deal {damage} damage to a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, damage)
  c.updateHealth()
  if c.destroyed:
    game.pendingReloc.append(c)
  game.pending()

def sniffer (game, card):
  """ Sniffer: For the remainder of the turn, each creature loses elusive.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  for c in active + inactive:
    c.elusive = False # already have reseting elusive next to reseting armor

def swap_widget (game, card):
  """ Swap Widget: Return a ready friendly Mars creature to your hand. If you do, put a Mars creature with a different name from your hand into play, then ready it.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  hand = game.activePlayer.hand
  initial = len(hand)
  choice = active[game.chooseCards("Creature", "Return a ready friendly Mars creature to your hand", "friend", condition = lambda x: x.ready and (x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade]), con_message = "That's not ready and/or not Mars.")[0][1]]
  return_card(choice, game)
  if choice.returned:
    game.pendingReloc.append(choice)
  game.pending("hand")
  if len(hand) > initial:
    replace = hand[game.chooseCards("Hand", f"Put a Mars creature not named {choice.title.replace('_', ' ').title()} into play:")[0][1]]
    game.activePlayer.states[card.title] = 1
    flank = game.chooseFlank(replace)
    if flank == "Left":
      flank = 0
    else:
      flank = len(active)
    active.insert(flank, replace)
    game.activePlayer.states[card.title] = 0

def mindwarper (game, card):
  """ Mindwarper: Choose an enemy creature. It captures 1 amber from its own side.
  """
  logging.info(f"Using {card.title}'s action.")
  inactive = game.inactivePlayer.board["Creature"]
  choice = inactive[game.chooseCards("Creature", "Choose an enemy creature to capture 1 amber from it's own side:", "enemy")[0][1]]
  choice.capture(game, 1, True)

def phylyx_the_disintegrator (game, card):
  """ Phylyx the Disintegrator: Your opponent loses 1 amber for each other friendly Mars creature.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]

  count = sum((x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade]) and x != card for x in active)
  game.inactivePlayer.amber -= min(game.inactivePlayer.amber, count)

###########
# Sanctum #
###########

def omni_epic_quest (game, card):
  """ Epic Quest: If you have played 7 or more Sanctum cards this turn, destroy Epic Quest and forge a key at no cost.
  """
  logging.info(f"Using {card.title}'s action.")
  if sum(x.house == "Sanctum" for x in game.playedThisTurn) >= 7:
    if game.canForge():
      destroy(card, game.activePlayer, game)
      if card.destroyed:
        game.pendingReloc.append(card)
      game.pending()
      game.forgeKey("active", 0)
    
def omni_gorm_of_omm (game, card):
  """ Gorm of Omm: Destroy Gorm of Omm. Destroy an artifact.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending() # pending calls cardChanged
  game.draw()
  pygame.display.update()
  side, choice = game.chooseCards("Artifact", "Destroy an artifact:")[0]
  if side == "fr":
    d = active[choice]
  else:
    d = inactive[choice]
  destroy(d, game.activePlayer, game)
  if d.destroyed:
    game.pendingReloc.append(d)
  game.pending()
  

def hallowed_blaster (game, card):
  """ Hallowed Blaster: Heal 3 damage from a creature.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if not active + inactive:
    logging.info("No valid targets.")
    return
  
  side, choice = game.chooseCards("Creature", "Heal 3 damage from a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  logging.info(f"Healing {min(c.damage, 3)} from {c.title}")
  c.damage -= min(c.damage, 3)

def omni_potion_of_invulnerability (game, card):
  """ Potion of Invulnerability: Destroy Potion of Invulnerability. For the remainder of the turn, each friendly creature cannot be dealt damage.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()
  game.activePlayer.states[card.title] = 1
  logging.info(f"Turning on {card.title}'s state.")
  game.resetStates.append(("a", card.title))

def omni_sigil_of_brotherhood (game, card):
  """ Sigil of Brotherhood: Sacrifice Sigil of Brotherhood. For the remainder of the turn, you may use friendly Sanctum creatures.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()
  game.extraUseHouses.append("Sanctum")
  logging.info("Added Sanctum to extraUseHouses.")

def whispering_reliquary (game, card):
  """ Whispering Reliquary: Return an artifact to its owner's hand.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Artifact"]
  inactive = game.inactivePlayer.board["Artifact"]
  side, choice = game.chooseCards("Artifact", "Return an artifact to it's owner's hand:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  return_card(c, game)
  if c.returned:
    game.pendingReloc.append(c)
    logging.info(f"{c.title} will be returned to it's owner's hand.")
  game.pending('hand')

def lady_maxena (game, card):
  """ Lady Maxena: Return Lady Maxena to its owner's hand.
  """
  logging.info(f"Using {card.title}'s action.")
  return_card(card, game)
  if card.returned:
    game.pendingReloc.append(card)
    logging.info(f"{card.title} will be returned to it's owner's hand.")
  game.pending('hand')

###########
# Shadows #
###########

def omni_longfused_mines (game, card):
  """ Longfused Mines: Sacrifice Longfused Mines. Deal 3 damage to each enemy creature not on a flank.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()
  inactive = game.inactivePlayer.board["Creature"]
  for c in inactive:
    if not c.isFlank(game):
      c.damageCalc(game, 3)
      c.updateHealth()
    if c.destroyed():
      game.pendingReloc.append(c)
  game.pending()

def omni_masterplan (game, card):
  """ Masterplan: Play the card under Masterplan. Destroy Masterplan.
  """
  logging.info(f"Using {card.title}'s action.")
  # I think it's technically possible to have more than one card under master plan
  # TODO: confirm this possibility, and add functionality for ordering cards
  for c in card.upgrade:
    logging.info(f"Playing {c.title} from under {card.title}.")
    card.upgrade.remove(c)
    game.activePlayer.hand.append(c)
    game.playCard(-1)
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()

def safe_place (game, card):
  """ Safe Place: Move 1 amber from your pool to Safe Place.
  """
  logging.info(f"Using {card.title}'s action.")
  if game.activePlayer.amber:
    logging.info(f"{card.title} gains 1 amber from the active Player's pool.")
    card.captured += 1
    game.activePlayer.amber -= 1

def seeker_needle (game, card):
  """ Seeker Needle: Deal 1 damage to a creature. If this damage destroys that creature, gain 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if not active + inactive:
    logging.info("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 1 damage to a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, 1)
  c.updateHealth()
  if c.destroyed:
    logging.info(f"{card.title} destroyed {c.title}, gaining 1 amber.")
    game.activePlayer.gainAmber(1, game)
    game.pendingReloc.append(c)
  game.pending()


def skeleton_key (game, card):
  """ Skeleton Key: A friendly creature captures 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  c = active[game.chooseCards("Creature", "Choose a friendly creature to capture 1 amber:", "friend")[0][1]]
  logging.info(f"{c.title} targeted with {card.title}")
  c.capture(game, 1)

def omni_special_delivery (game, card):
  """ Special Delivery: Sacrifice Special Delivery. Deal 3 damage to a flank creature. If this damage destroys that creature, purge it.
  """
  logging.info(f"Using {card.title}'s action.")
  pending = game.pendingReloc
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    pending.append(card)
  game.pending()

  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 3 damage to a flank creature. If this damage destroys the creature, purge it:", condition = lambda x: x.isFlank(game), con_message = "That's not a flank creature.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(3, game)
  c.updateHealth()
  if c.destroyed:
    pending.append(c)
    game.pending('purge')

def subtle_maul (game, card):
  """ Subtle Maul: Your opponent discards a random card from their hand.
  """
  logging.info(f"Using {card.title}'s action.")
  inactive = game.inactivePlayer.hand
  ran = inactive[random.choice(list(range(len(inactive))))]
  game.inactivePlayer.discard.append(ran)
  inactive.remove(ran)
  logging.info(f"{card.title} discarded {ran.title} from your opponent's hand.")

def the_sting (game, card):
  """ The Sting: Destroy The Sting.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending()

def omni_deipno_spymaster (game, card):
  """ Deipno Spymaster: Choose a friendly creature. You may use that creature this turn.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  c = active[game.chooseCards("Creature", "Choose a friendly creature to be able to use this turn:", "friend")[0][1]]
  logging.info(f"{c.title} was added to Deipno Spymaster's state.")
  if not game.activePlayer.states[card.title]:
    game.activePlayer.states[card.title] = [c]
  else:
    game.activePlayer.states[card.title].append(c)

def mack_the_knife (game, card):
  """ Mack the Knife: Deal 1 damage to a creature. If this damage destroys that creature, gain 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if not active + inactive:
    logging.info("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 1 damage to a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, 1)
  c.updateHealth()
  if c.destroyed:
    logging.info(f"{card.title} destroyed {c.title}, gaining 1 amber.")
    game.activePlayer.gainAmber(1, game)
    game.pendingReloc.append(c)
  game.pending()



def noddy_the_thief (game, card):
  """ Noddy the Thief: Steal 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  stealAmber(game.activePlayer, game.inactivePlayer, 1, game)


###########
# Untamed #
###########

def bear_flute (game, card):
  """ Bear Flute: Fully heal an Ancient Bear. If there are no Ancient Bears in play, search your deck and discard pile and put each Ancient Bear from them into your hand. If you do, shuffle your discard pile into your deck.
  """
  logging.info(f"Using {card.title}'s action.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  
  if sum(x.title == "ancient_bear" for x in active + inactive):
    side, choice = game.chooseCards("Creature", "Fully heal an Ancient Bear:", condition = lambda x: x.title == "ancient_bear", con_message = "That's not an Ancient Bear.")[0]
    if side == "fr":
      c = active[choice]
    else:
      c = inactive[choice]
    c.damage = 0
    return
  # otherwise:
  for c in game.activePlayer.deck:
    if c.title == "ancient_bear":
      logging.info("Adding an Ancient Bear to hand from deck.")
      game.activePlayer.hand.append(c)
      game.activePlayer.deck.remove(c)
  for c in game.activePlayer.discard:
    if c.title == "ancient_bear":
      logging.info("Adding an Ancient Bear to hand from discard.")
      game.activePlayer.hand.append(c)
      game.activePlayer.discard.remove(c)
  game.activePlayer.shuffleDiscard()

def omni_nepenthe_seed (game, card):
  """ Sacrifice Nepenthe Seed. Return a card from your discard pile to your hand.
  """
  logging.info(f"Using {card.title}'s action.")
  destroy(card, game.activePlayer, game)
  if card.destroyed:
    game.pendingReloc.append(card)
  game.pending() # I'm ruling the player can return Nepenthe Seed to their hand

  discard = game.activePlayer.discard

  if not discard:
    logging.info("No cardss in your discard.")
    return

  game.drawFriendDiscard = True
  choice = game.chooseCard("Discard", "Return a card from your discard pile to your hand:", "friend")[0][1]
  # I can skip pending b/c this card is guaranteed to belong to the active player
  c = discard[choice]
  discard.remove(c)
  game.activePlayer.hand.append(c)

def ritual_of_balance (game, card):
  """ Ritual of Balance: If your opponent has 6 or more amber, steal 1 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  if game.inactivePlayer.amber > 5:
    stealAmber(game.activePlayer, game.inactivePlayer, 1, game)
    logging.info(f"{card.title} stole 1 amber.")

def omni_ritual_of_the_hunt (game, card):
  """ Ritual of the Hunt: Sacrifice Ritual of the Hunt. For the remainder of the turn, you may use friendly Untamed creatures.
  """
  logging.info(f"Using {card.title}'s action, adding Untamed to extraUseHouses.")
  game.extraUseHouses.append("Untamed")

def world_tree (game, card):
  """ World Tree: Return a creature from your discard pile to the top of your deck.
  """
  logging.info(f"Using {card.title}'s action.")
  discard = game.activePlayer.discard

  if not discard:
    logging.info("No cards in your discard.")
    return

  game.drawFriendDiscard = True
  choice = game.chooseCard("Discard", "Return a creature from your discard pile to the top of your deck:", "friend", condition = lambda x: x.type == "Creature", con_message = "That's not a creature.")[0][1]
  # I can skip pending b/c this card is guaranteed to belong to the active player
  c = discard[choice]
  discard.remove(c)
  game.activePlayer.deck.append(c)

def giant_sloth (game, card):
  """ Giant Sloth: Gain 3 amber.
  """
  logging.info(f"Using {card.title}'s action.")
  game.activePlayer.gainAmber(3, game)