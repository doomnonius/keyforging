import logging
from helpers import return_card, stealAmber#, return_card

# This is all the destroyed and leaves play effects
# Also include things like Krump?

###########
## Basic ##
###########

def basicLeaves(game, card):
    """ Called for when a card (almost only creatures, with a few unusual artifacts) leaves the board from play (not just destroyed, so to archive, hand, purge as well). It will reset the card, deal with upgrades staying behind or going away, deal with amber remaining on the card. All dest functions will call this function as their last step.
    """
    logging.info(f"Entering basic leaves for {card.title}")
    active = game.activePlayer.board
    inactive = game.inactivePlayer.board
    t = card.type
    # return captured amber if a creature, don't if an artifact
    if card.captured and card.type == "Creature":
      logging.info(f"{card.title} will return {card.captured} amber.")
      if card in inactive[t]:
        game.activePlayer.gainAmber(card.captured, game)
      elif card in active[t]:
        game.inactivePlayer.gainAmber(card.captured, game)
    # if Magda the Rat
    if card.title == "magda_the_rat":
      if card in inactive[t]:
        stealAmber(game.activePlayer, game.inactivePlayer, 2, game)
      elif card in active[t]:
        stealAmber(game.inactivePlayer, game.activePlayer, 2, game)
    # if grey_monk
    if card.title == "grey_monk":
      if card in active[t]:
        for c in active[t]:
          c.extraArm -= 1
          c.armor -= min(1, c.armor)
      elif card in inactive[t]:
        for c in inactive[t]:
          c.extraArm -= 1
          c.armor -= min(1, c.armor)
    # if banner_of_battle
    if card.title == "banner_of_battle":
      if card in active[t]:
        for c in active["Creature"]:
          c.calcPower(game)
          c.updateHealth()
          if c.destroyed:
            game.pendingReloc.append(c)
      if card in inactive[t]:
        for c in inactive["Creature"]:
          c.calcPower(game)
          c.updateHealth()
          if c.destroyed:
            game.pendingReloc.append(c)
      game.pending()
    # handle upgrades
    for up in card.upgrade:
      if up.deck == game.activePlayer.name:
        game.activePlayer.discard.append(up)
        game.activePlayer.board["Upgrade"].remove(up)
      else:
        game.inactivePlayer.discard.append(up)
        game.inactivePlayer.board["Upgrade"].remove(up)
    # remove from board
    logging.info(f"Removing {card.title} from the board.")
    if card in inactive[t]:
      inactive[t].remove(card)
    elif card in active[t]:
      active[t].remove(card)
    # handle restringuntus
    if card.title == "restringuntus":
      game.activePlayer.states[card.title] = 0
    # handle harland_mindlock
    if card.title == "harland_mindlock":
      logging.info("Harland has died, attempting to return the stolen minion.")
      if card in active:
        flank = game.chooseHouse("custom", ("Put the minion on the left flank or right flank?", ["Left", "Right"]))
        # TODO: add putting a card on enemy side
        if flank == "Left":
          flank = 0
        else:
          flank = len(inactive)
        inactive.insert(flank, card)
      elif card in inactive:
        flank = game.chooseFlank(card)
        if flank == "Left":
          flank = 0
        else:
          flank = len(active)
        active.insert(flank, card)
    # handle spangler_box
    if card.title == "spangler_box":
      logging.info("Returning Spangler Box's minions.")
      for c in card.spangler:
        # TODO: choose which order to put them into play
        if c.deck == game.activePlayer.name:
          flank = game.chooseFlank(c)
          if flank == "Left":
            flank = 0
          else:
            flank = len(active)
          active[t].insert(flank, c)
        else:
          # TODO: update choose flank to allow putting a minion on the opponent's flank
          ...
    # handle greking's ability
    if card.type == "Creature" and card.greking and card.greking in active[t] and not card.safe:
      flank = game.chooseHouse("custom", ("Put the minion on the your left flank or your right flank?", ["Left", "Right"]))
      if flank == "Left":
        flank = 0
      else:
        flank = len(active)
      active[t].insert(flank, card)
    elif card.type == "Creature" and card.greking and card.greking in inactive[t] and not card.safe:
      flank = game.chooseHouse("custom", ("Put the minion on your opponent's left flank or right flank?", ["Left", "Right"]))
      if flank == "Left":
        flank = 0
      else:
        flank = len(inactive)
      inactive[t].insert(flank, card)
        

# I don't want to use a basic dest because things can have more than one destroyed effect. Going to incoporate the aspects of basic dest in pending somehow

def basicDest(game, card):
    """ Called for when a card is destroyed, triggers "after a card is destroyed" effects.
    """
    logging.info(f"Entering basic dest for {card.title}")
    active = game.activePlayer.board["Creature"]
    inactive = game.inactivePlayer.board["Creature"]
    activeS = game.activePlayer.states
    inactiveS = game.inactivePlayer.states
    activeA = game.activePlayer.board["Artifact"]
    inactiveA = game.inactivePlayer.board["Artifact"]
    if card.type == "Creature":
      # loot the bodies
      if "loot_the_bodies" in activeS and activeS["loot_the_bodies"] and card in inactive:
        game.activePlayer.gainAmber(activeS["loot_the_bodies"], game)
      # looter goblin
      if "looter_goblin" in activeS and activeS["looter_goblin"] and card in inactive:
        game.activePlayer.gainAmber(activeS["looter_goblin"], game)
      # pile of skulls
      if "pile_of_skulls" in activeA and card in inactive:
        choice = active[game.chooseCards("Creature", "Pile of Skulls: Choose a friendly creature to capture 1 amber:", "friend")[0][1]]
        choice.capture(1, game)
      # soul snatcher
      if "soul_snatcher" in [x.title for x in activeA + inactiveA]:
        logging.info("Soul Snatcher triggered")
        count = sum(x.title == "soul_snatcher" for x in activeA + inactiveA)
        if card in active:
          game.activePlayer.gainAmber(count, game)
        elif card in inactive:
          game.inactivePlayer.gainAmber(count, game)
      # tolas
      count = sum("tolas" == x.title and not x.destroyed for x in active + inactive)
      if count:
        logging.info("Tolas triggered.")
        if card in active:
          game.inactivePlayer.gainAmber(count, game)
        elif card in inactive:
          game.activePlayer.gainAmber(count, game)

    # I think this should be last, because it removes from board and we still need to know what side a card is on above
    basicLeaves(game, card)

###########
# Brobnar #
###########

def grenade_snib (game, card):
  """ Grenade Snib: Your opponent loses 2 amber.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if card in active:
    logging.info(f"{game.inactivePlayer.name} loses 2 amber.")
    game.inactivePlayer.amber -= min(2, game.inactivePlayer.amber)
  elif card in inactive:
    logging.info(f"{game.activePlayer.name} loses 2 amber.")
    game.activePlayer.amber -= min(2, game.activePlayer.amber)

def phoenix_heart (game, card):
  """ Phoenix Heart: Return this creature to its owner's hand and deal 3 damage to each creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  friend_dest = []
  enemy_dest = []
  if game.pendingReloc:
    pending = []
    secondary = True
    logging.info("Nested destruction.")
  else:
    logging.info("First destruction.")
    pending = game.pendingReloc
  
  card.safe = True
  logging.info(f"{card.title} marked safe.")
  
  return_card(card)
  if card.returned:
    basicLeaves(card)
    if card.deck == game.activePlayer.name:
      game.activePlayer.hand.append(card)
    else:
      game.inactivePlayer.hand.append(card)
    logging.info(f"{card.title} returned to hand.")
  
  for c in active:
    if not c.destroyed:
      c.damageCalc(game, 3)
      c.updateHealth()
      if c.destroyed:
        pending.append(c)
  for c in inactive:
    if not c.destroyed:
      c.damageCalc(game, 3)
      c.updateHealth()
      if c.destroyed:
        pending.append(c)
  
  if secondary:
    game.pending(secondary = pending)
  else:
    game.pending()
  
#######
# Dis #
#######

def dust_imp (game, card):
  """ Dust Imp: Gain 2 amber
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  logging.info("Dust Imp's destroyed effect is triggered.")
  if card in active:
    game.activePlayer.gainAmber(2, game)
  elif card in inactive:
    game.inactivePlayer.gainAmber(2, game)

def truebaru (game, card):
  """ Truebaru: Gain 5 amber.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  logging.info("Truebaru's destroyed effect is triggered.")
  if card in active:
    game.activePlayer.gainAmber(5, game)
  elif card in inactive:
    game.inactivePlayer.gainAmber(5, game)

#########
# Logos #
#########

def dextre (game, card):
  """ Dextre: put Dextre on top of your deck.
  """
  logging.info("Dextre's destroyed effect is triggered.")
  card.safe = True
  basicDest(game, card)
  if card.deck == game.activePlayer.name:
    game.activePlayer.deck.append(card)
    logging.info(f"Dextre should now be on top of it's owner's deck. Is it? {card in game.activePlayer.deck}")
  else:
    game.inactivePlayer.deck.append(card)
    logging.info(f"Dextre should now be on top of it's owner's deck. Is it? {card in game.inactivePlayer.deck}")

def research_smoko (game, card):
  """ Research Smoko: Archive the top card of your deck
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  logging.info("Research Smoko's destroyed effect is triggered.")
  if card in active:
    game.activePlayer.archive.append(game.activePlayer.deck.pop())
    logging.info(f"Archived the top card of {game.activePlayer.name}'s deck")
  elif card in inactive:
    game.inactivePlayer.archive.append(game.inactivePlayer.deck.pop())
    logging.info(f"Archived the top card of {game.inactivePlayer.name}'s deck")

########
# Mars #
########

def biomatrix_backup (game, card):
  """ Biomatrix Backup: Put this creature into its owner's archive.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  logging.info("The destroyed ability from Biomatrix Backup is triggered.")
  card.safe = True
  basicDest(game, card)
  if card in active + inactive:
    if card.deck == game.activePlayer.name:
      game.activePlayer.archive.append(card)
      logging.info(f"{card.title} should now be in it's owner's archives. Is it? {card in game.activePlayer.archive}")
    else:
      game.inactivePlayer.archive.append(card)
      logging.info(f"{card.title} should now be in it's owner's archives. Is it? {card in game.inactivePlayer.archive}")

  game.pending()
  

###########
# Sanctum #
###########

def armageddon_cloak (game, card):
  """ Armageddon Cloak: If this creature would be destroyed, fully heal it and destroy Arma Cloak instead.
  """
  logging.info("The destroyed ability from Armageddon Cloak is triggered.")
  card.destroyed = False
  card.hazard -= 2
  card.damage = 0
  pending = [] # we're assuming this has to be part of a nested destroyed
  for c in card.upgrade[::-1]:
    if c.title == "armageddon_cloak":
      pending.append(c)
      card.upgrade.remove(c)
  logging.info(f"{card.title} should still be alive. Is it? {card in game.inactivePlayer.board['Creature'] + game.activePlayer.board['Creature']}")
  game.pending(secondary = pending)

def duma_the_martyr (game, card):
  """ Duma the Martyr: Fully heal each other friendly creature and draw 2 cards.
  """
  logging.info("Duma's destroyed effect is triggered.")
  active = game.activePlayer.board["Creature"]
  for c in active:
    c.damage = 0 # this won't remove destroyed tags
  game.activePlayer += 2

###########
# Shadows #
###########

def bad_penny (game, card):
  """ Bad Penny: Return Bad Penny to your hand.
  """
  logging.info("Bad Penny's destroyed effect is triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  card.safe = True
  basicDest(game, card)
  if card in active + inactive:
    if card.deck == game.activePlayer.name:
      game.activePlayer.hand.append(card)
      logging.info(f"{card.title} should now be in it's owner's hand. Is it? {card in game.activePlayer.hand}")
    else:
      game.inactivePlayer.hand.append(card)
      logging.info(f"{card.title} should now be in it's owner's hand. Is it? {card in game.inactivePlayer.hand}")

###########
# Untamed #
###########


if __name__ == '__main__':
  print ('This statement will be executed only if this script is called directly')