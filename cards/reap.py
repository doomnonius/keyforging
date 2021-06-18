from functools import reduce
import random, logging
from helpers import stealAmber, destroy, return_card

def basicReap(game, card, replicated: bool = False):
  if "dimension_door" in game.activePlayer.states and game.activePlayer.states["dimension_door"]:
    logging.info("Dimension Door causes amber gained from reaping to be stolen instead.")
    stealAmber(game.activePlayer, game.inactivePlayer, 1, game)
  else:
    game.activePlayer.gainAmber(1, game)
  if "crystal_hive" in game.activePlayer.states:
    game.activePlayer.gainAmber(game.activePlayer.states["crystal_hive"], game)
    logging.info(f"Crystal hive grants {game.activePlayer.states['crystal_hive']} extra amber for reaping.")


###########
# Brobnar #
###########

def kelifi_dragon (game, card, replicated: bool = False):
  """ Kelifi Dragon: Gain 1 amber. Deal 5 damage to a creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  pending = game.pendingReloc

  game.activePlayer.gainAmber(1, game)

  for c in game.chooseCards("Creature", "Deal 5 damage to a creature:"):
    c.damageCalc(5, game)
    c.updateHealth()
    if c.destroyed:
      pending.append(c)
    game.pending()

def looter_goblin (game, card, replicated: bool = False):
  """ Looter Goblin: for the remainder of the turn, gain 1 amber each time an enemy creature is destroyed.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  try:
    game.activePlayer.states[card.title] += 1
  except:
    game.activePlayer.states[card.title] = 1
  game.resetStates.append(("a", card.title))

def troll (game, card, replicated: bool = False):
  """ Troll: Troll heals 3 damage.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  card.heal(3)


#######
# Dis #
#######

def eater_of_the_dead (game, card, replicated: bool = False):
  """ Purge a creature from a discard pile. If you do, put a +1 power counter on Eater of the Dead.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  pendingDisc = game.pendingReloc
  for c in game.chooseCards("Creature", "Choose a creature:"):
    if c.damage > 0:
      heal = int(game.chooseHouse("custom", ("How much damage would you like to heal?", list(range(min(3, c.damage + 1)))))[0])
    else:
      logging.info("There was no damage on this creature, so no damage will be dealt.")
      heal = 0
  if heal:
    for c2 in game.chooseCards("Creature", f"Choose a creature to deal {heal} damage to:", condition = lambda x: x != c, con_message = "You can't damage the creature you healed. Choose a different target."):
      c2.damageCalc(heal, game)
      c2.updateHealth()
      if c2.destroyed:
        pendingDisc.append(c2)
    game.pending()

def master_of_1 (game, card, replicated: bool = False):
  """ Master of 1: You may destroy a creature with 1 power.
  """
  logging.info(f"{card.title}'s reap ability triggered.")

  for c in game.chooseCards("Creature", "Destroy a creature with 1 power:", condition = lambda x: x.power == 1, con_message = "That creature does not have 1 power."):
    destroy(c, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()


def master_of_2 (game, card, replicated: bool = False):
  """ Master of 2: You may destroy a creature with 2 power.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "Destroy a creature with 1 power:", condition = lambda x: x.power == 2, con_message = "That creature does not have 2 power."):
    destroy(c, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()

def master_of_3 (game, card, replicated: bool = False):
  """ Master of 3: You may destroy a creature with 3 power.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "Destroy a creature with 1 power:", condition = lambda x: x.power == 3, con_message = "That creature does not have 3 power."):
    destroy(c, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()

def snudge (game, card, replicated: bool = False):
  """ Snudge: Return an artifact or flank creature to its owner's hand.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  pendingDisc = game.pendingReloc

  for c in game.chooseCards("Board", f"Return a card to its owner's hand:", condition = lambda x: x.type == "Artifact" or x.isFlank(game)):
    return_card(c, game)
    if c.returned:
      pendingDisc.append(c)
    game.pending("hand")

def tocsin (game, card, replicated: bool = False):
  """ Tocsin: your opponent discards a random card from their hand.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  inactive = game.inactivePlayer.hand
  ran = inactive[random.choice(list(range(len(inactive))))]
  game.inactivePlayer.discard.append(ran)
  inactive.remove(ran)

#########
# Logos #
#########

def spectral_tunneler (game, card, replicated: bool = False):
  """ Spectral Tunneler: Draw a card
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  game.activePlayer += 1

def doc_bookton (game, card, replicated: bool = False):
  """ Doc Bookton: Draw a card
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  game.activePlayer += 1

def ganymede_archivist (game, card, replicated: bool = False):
  """ Ganymede Archivist: archive a card
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  for c in game.chooseCards("Hand", "Choose a card from your hand to archive:"):
    game.pendingReloc.append(c)
    game.activePlayer.hand.remove(c)
    game.pending("archive", target = game.activePlayer)

def neutron_shark (game, card, replicated: bool = False):
  """ Neutron Shark: Destroy an enemy creature or artifact and a friendly creature or artifact. Discard the top card of your deck. If that card is not a Logos card, trigger this effect again.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  pendingDiscard = game.pendingReloc

  while card in active:
    for c1 in game.chooseCards("Board", f"Choose an enemy card to destroy:", "enemy"):
      destroy(c1, game.inactivePlayer, game)
      if c1.destroyed:
        pendingDiscard.append(c1)
    if active:
      for c2 in game.chooseCards("Board", f"Choose a friendly card to destroy:", "friend"):
        destroy(c2, game.inactivePlayer, game)
        if c2.destroyed:
          pendingDiscard.append(c2)
    game.pending()
    if game.activePlayer.deck:
      game.activePlayer.discard.append(game.activePlayer.deck.pop())
      if game.activePlayer.discard[-1].house == "Logos":
        break
    else:
      break

def ozmo_martianologist (game, card, replicated: bool = False):
  """ Ozmo, Martianologist: Heal 3 damage from a Mars creature or stun a Mars creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "Choose a Mars creature to heal or stun:", condition = lambda x: x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade], con_message = "That creature is not from house Mars."):
    action = game.chooseHouse("custom", (f"Would you like to stun {c.title.replace('_', ' ').title()} or heal three damage?", ["Stun", "Heal"]), colors = ["YELLOW", "RED"])[0]
    if action == "Heal":
      c.heal(3)
    else:
      c.stun = True

def psychic_bug (game, card, replicated: bool = False):
  """ Psychic Bug: Look at your opponent's hand.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  for card in game.inactivePlayer.hand:
    card.revealed = True

def replicator (game, card, replicated: bool = False):
  """ Replicator: Trigger the reap effect of another creature in play as if you controlled that creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")

  for c in  game.chooseCards("Creature", "Choose a reap effect to copy:", condition = lambda x: x.title != 'replicator' and x.reap, con_message = "That creature doesn't have a reap effect you can copy:"):
    if len(c.reap) > 1:
      pass # TODO: make them choose one, need a function for this kind of thing
    else:
      c.reap[0](game, c, True)

def vespilon_theorist (game, card, replicated: bool = False):
  """ Vespilon Theorist: Choose a house. Reveal the top card of your deck. If it is of that house, archive it and gain 1. Otherwise, discard it.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  deck = game.activePlayer.deck
  hold = []
  house = game.chooseHouse("other")
  if deck:
    hold.append(deck.pop())
  else:
    logging.info("Deck is empty, no card was discarded.")
    return
  if hold[0].house == house:
    game.activePlayer.archive.append(hold.pop())
    game.ativePlayer.gainAmber(1, game)
  else:
    game.activePlayer.discard.append(hold.pop())

########
# Mars #
########

def blypyp (game, card, replicated: bool = False):
  """ Blypyp: The next mars creature you play this turn enters play ready.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  game.activePlayer.states[card.title] = 1
  # this one still needs to be in reset states in case it isn't triggered
  game.resetStates.append(("a", card.title))
    
def chuff_ape (game, card, replicated: bool = False):
  """ Chuff Ape: You may sacrifice another friendly creature. If you do, fully heal Chuff Ape.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "You may sacrifice another creature to fully heal Chuff Ape:", full = False):
    destroy(c, game)
    if c.destroyed:
      sac = True
      game.pendingReloc.append(c)
      card.damage = 0
    game.pending()
  
  if not sac:
    logging.info("No creature was sacrificed.")
    return

def grabber_jammer (game, card, replicated: bool = False):
  """ Grabber Jammer: Capture 1 amber.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  card.capture(1, game, replicated)

def john_smyth (game, card, replicated: bool = False):
  """ John Smyth: Ready a non-agent Mars creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "Ready a non-agent Mars creature:", condition = lambda x: (x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade]) and "Agent" not in x.traits, con_message = "That creature is either an agent or isn't from house Mars."):
    c.ready = True

def qyxxlyx_plague_master (game, card, replicated: bool = False):
  """ Qyxxlyx Plague Master: Deal 3 damage to each human creature. This damage cannot be prevented by armor.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active:
    if "Human" in c.traits:
      c.damageCalc(3, game, armor = False)
      c.updateHealth()
  for c in inactive:
    if "Human" in c.traits:
      c.damageCalc(3, game, armor = False)
      c.updateHealth()
  for c in active:
    if c.destroyed:
      pending.append(c)
  for c in inactive:
    if c.destroyed:
      pending.append(c)
  
  game.pending()

def ulyq_megamouth (game, card, replicated: bool = False):
  """ Ulyq Megamouth: Use a friendly non-Mars creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]

  for c in game.chooseCards("Creature", "Use a friendly non-Mars creature:", "friend", condition = lambda x: x.house != "Mars" and "experimental_therapy" not in [y.title for y in x.upgrade], con_message = "You must pick a creature that doesn't belong to house Mars."):
  
    if not c.ready:
      logging.info("Card isn't ready, so can't be used.")
      return

    uses =  []
    if game.canReap(c, r_click = True, cheat = True):
      uses.append("Reap")
    if game.canFight(c, r_click = True, cheat = True):
      uses.append("Fight")
    if game.canAction(c, r_click = True, cheat = True):
      uses.append("Action")
    if game.canOmni(c, r_click = True, cheat = True):
      uses.append("Omni")
    
    if not uses:
      logging.info("No valid uses for this card.")
      return
    
    use = game.chooseHouse("custom", ("How would you like to use this creature?", uses))[0]
    if use[0] == "R":
      game.reapCard(active.index(c), cheat = True)
    elif use[0] == "F":
      game.fightCard(active.index(c), cheat=True)
    elif use[0] == "A":
      game.actionCard(active.index(c), cheat = True)
    elif use[0] == "O":
      game.omniCard(active.index(c))

def uxlyx_the_zookeeper (game, card, replicated: bool = False):
  """ Uxlyx the Zookeeper: Put an enemy creature into your archives.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", f"Choose an enemy creature to put into your archives:", "enemy"):
    return_card(c, game)
    if c.returned:
      game.pendingReloc.append(c)
    game.pending("archive", target = game.activePlayer)

def vezyma_thinkdrone (game, card, replicated: bool = False):
  """ Vezyma Thinkdrone: You may archive a friendly creature or artifact from play.
  """
  logging.info(f"{card.title}'s reap ability triggered.")

  for c in game.chooseCards("Board", f"You may archive a friendly card from play:", "friend", full = False):
    return_card(c, game)
    if c.returned:
      game.pendingReloc.append(c)
    game.pending("archive", target = game.activePlayer)

def yxilo_bolter (game, card, replicated: bool = False):
  """ Yxilo Bolter: Deal 2 damage to a creaure. If this damage destroys that creature, purge it.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  pending = game.pendingReloc

  for c in game.chooseCards("Creature", "Deal 2 damage to a creature. If this damage destroys the creature, purge it:"):
    c.damageCalc(2, game)
    c.updateHealth()
    if c.destroyed:
      pending.append(c)
      game.pending('purge')

def zyzzix_the_many (game, card, replicated: bool = False):
  """ Zyzzix the Many: You may reveal a creature from your hand. If you do, archive it and Zyzzix the many gets three +1 power counters.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  hand = game.activePlayer.hand

  for c in game.chooseCards("Hand", "You may reveal a creature from your hand:", full = False, condition = lambda x: x.type == "Creature", con_message = "You must choose a creature."):
    c.reveal = True
    game.activePlayer.archive.append(c)
    hand.remove(c)
    card.extraPow += 3
    card.power += 3

def red_planet_ray_gun (game, card, replicated: bool = False):
  """ Red Planet Ray Gun: Choose a creature. Deal 1 damage to that creature for each Mars creature in play.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade] for x in active + inactive)
  for c in game.chooseCards("Creature", f"Deal {count} damage to a creature:"):
    c.damageCalc(count, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  game.pending()

###########
# Sanctum #
###########

def commander_remiel (game, card, replicated: bool = False):
  """ Commander Remiel: Use a friendly non-Sanctum creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]

  for c in game.chooseCards("Creature", "Use a friendly non-Sanctum creature:", "friend", condition = lambda x: x.house != "Sanctum" and "experimental_therapy" not in [y.title for y in x.upgrade], con_message = "You must pick a creature that doesn't belong to house Sanctum."):
  
    if not c.ready:
      logging.info("Card isn't ready, so can't be used.")
      return

    uses =  []
    if game.canReap(c, r_click = True, cheat = True):
      uses.append("Reap")
    if game.canFight(c, r_click = True, cheat = True):
      uses.append("Fight")
    if game.canAction(c, r_click = True, cheat = True):
      uses.append("Action")
    if game.canOmni(c, r_click = True, cheat = True):
      uses.append("Omni")
    
    if not uses:
      logging.info("No valid uses for this card.")
      return
    
    use = game.chooseHouse("custom", ("How would you like to use this creature?", uses))[0]
    if use[0] == "R":
      game.reapCard(active.index(c), cheat = True)
    elif use[0] == "F":
      game.fightCard(active.index(c), cheat=True)
    elif use[0] == "A":
      game.actionCard(active.index(c), cheat = True)
    elif use[0] == "O":
      game.omniCard(active.index(c))

def grey_monk (game, card, replicated: bool = False):
  """ Grey Monk: Heal 2 damage from a creature
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "Heal 2 damage:"):
    c.heal(2)

def horseman_of_famine (game, card, replicated: bool = False):
  """ Horseman of Famine: Destroy the least powerful creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  low = min(x.power for x in (active + inactive))
  pendingD = game.pendingReloc

  for c in game.chooseCards("Creature", "Destroy a creature with the lowest power:", condition = lambda x: x.power == low, con_message = "That creature does not have the lowest power."):
    destroy(c, game)
    if c.destroyed:
      pendingD.append(c)
    game.pending()

def horseman_of_pestilence (game, card, replicated: bool = False):
  """ Horseman of Pestilence: Deal 1 damage to each non-Horseman creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active:
    if "Horseman" not in c.traits:
      c.damageCalc(1, game)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in inactive:
    if "Horseman" not in c.traits:
      c.damageCalc(1, game)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)

  game.pending()

def protectrix (game, card, replicated: bool = False):
  """ Protectrix: You may fully heal a creature. If you do, that creature cannot be dealt damage for the remainder of the turn.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "You may fully heal a creature:", full = False):
    if c.damage > 0:
      healed = True
    c.damage = 0
    if healed:
      try:
        if game.activePlayer.states[card.title]:
          game.activePlayer.states[card.title].append(c)
        else:
          game.activePlayer.states[card.title] = [c]
      except:
        game.activePlayer.states[card.title] = [c]
      game.resetStates.append(("a", card.title))

def sanctum_guardian (game, card, replicated: bool = False):
  """ Sanctum Guardian: Swap SG with another friendly creature in your battleline.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  
  if replicated:
    logging.info("Sanctum Guardian's position cannot be switched into your side, so nothing happens.")
    return
  
  for c in game.chooseCards("Creature", "Swap positions with another friendly creature in your battleline.", "friend", condition = lambda x: x != card):
    sg_i = active.index(card)
    other_i = active.index(c)
    active[sg_i], active[other_i] = active[other_i], active[sg_i]

def sequis (game, card, replicated: bool = False):
  """ Sequis: Capture 1 amber.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  card.capture(1, game, replicated)

###########
# Shadows #
###########

def bulleteye (game, card, replicated: bool = False):
  """ Bulleteye: Destroy a flank creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Creature", "Destroy a flank creature:", condition = lambda x: x.isFlank(game), con_message = "That is not a flank creature."):
    destroy(c, game) # destroy doesn't use the player so it's fine
    if c.destroyed:
      game.pendingReloc.append(c)
    game.pending()

def faygin (game, card, replicated: bool = False):
  """ Faygin: Return an Urchin from play or from your discard pile to your hand.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  discard = game.activePlayer.discard

  for c in game.chooseCards("Faygin", "Choose an Urchin to return to your hand:", condition = lambda x: x.title == "urchin", con_message = "That's not an Urchin."):
    if c in discard:
      discard.remove(c)
      game.activePlayer.hand.append(c)
    else:
      return_card(c)
      if c.returned:
        game.pendingReloc.append(c)
      game.pending("hand")
  
  game.drawFriendDiscard = False

def nexus (game, card, replicated: bool = False):
  """ Nexus: Use an enemy artifact as if it were yours.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  inactive = game.inactivePlayer.board["Artifact"]
  for c in game.chooseCards("Artifact", "Choose an opponent's artifact to use:", "enemy"):

    if not c.ready:
      logging.info("Card isn't ready, so can't be used.")
      return

    uses =  []
    if game.canAction(c, r_click = True, cheat = True):
      uses.append("Action")
    if game.canOmni(c, r_click = True, cheat = True):
      uses.append("Omni")
    
    if not uses:
      logging.info("No valid uses for this card.")
      return
    
    use = game.chooseHouse("custom", ("How would you like to use this creature?", uses))[0]
    if use[0] == "A":
      game.actionCard(inactive.index(c), enemy = True, cheat = True)
    elif use[0] == "O":
      game.omniCard(inactive.index(c), enemy = True)

def selwyn_the_fence (game, card, attacked):
  """ Selwyn the Fence: move 1 amber from one of your cards to your pool.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  
  for c in game.chooseCards("Board", f"Move an amber from a friendly card to your pool:", "friend", condition = lambda x: x.captured > 0, con_message = "That card has no amber on it."):
    c.captured -= 1
    game.activePlayer.gainAmber(1, game)

def smiling_ruth (game, card, replicated: bool = False):
  """ Smiling Ruth: If you forged a key this turn, take control of an enemy flank creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if game.forgedThisTurn:

    for c in game.chooseCards("Creature", "Choose an enemy flank creature to steal:", "enemy", condition = lambda x: x.isFlank(game), con_message = "You didn't choose a flank creature. Please try again."):
      flank = game.chooseFlank(c)
      if flank == "Left":
        flank = 0
      else:
        flank = len(active)
      active.insert(flank, c)
      inactive.remove(c)

def duskrunner (game, card, replicated: bool = False):
  """ Duskrunner: Steal 1 amber.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  stealAmber(game.activePlayer, game.inactivePlayer, 1, game)

def silent_dagger (game, card, replicated: bool = False):
  """ Silent Dagger: Deal 4 damage to a flank creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  pending = game.pendingReloc

  for c in game.chooseCards("Creature", "Deal 4 damage to a flank creature:", condition = lambda x: x.isFlank(game), con_message = "Not a flank creature."):
    c.damageCalc(4, game)
    c.updateHealth()
    if c.destroyed:
      pending.append(c)
    game.pending()

###########
# Untamed #
###########

def bigtwig (game, card, replicated: bool = False):
  """ Bigtwig: Stun and exhaust a creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")

  for c in game.chooseCards("Creature", "Stun and exhaust a creature:"):
    c.ready = False
    c.stun = True

def dew_faerie (game, card, replicated: bool = False):
  """ Dew Faerie: Gain 1 amber.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  game.activePlayer.gainAmber(1, game)

def inka_the_spider (game, card, replicated: bool = False):
  """ Inka the Spider: Stun a creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")

  for c in game.chooseCards("Creature", "Stun a creature:"):
    c.stun = True
  
def kindrith_longshot (game, card, replicated: bool = False):
  """ Kindrith Longshot: Deal 2 damage to a creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  pending = game.pendingReloc

  for c in game.chooseCards("Creature", "Deal 2 damage to a creature:"):
    c.damageCalc(2, game)
    c.updateHealth()
    if c.destroyed:
      pending.append(c)
    game.pending()

def piranha_monkeys (game, card, replicated: bool = False):
  """ Piranha Monkeys: Deal 2 damage to each other creature.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc
  
  for c in active:
    if c != card:
      c.damageCalc(2, game)
  for c in active[::-1]:
    c.updateHealth(game.activePlayer)
    if c.destroyed:
      pending.append(c)
  for c in inactive:
    c.damageCalc(2, game)
  for c in inactive[::-1]:
    c.updateHealth(game.inactivePlayer)
    if c.destroyed:
      pending.append(c)
  
  game.pending()

def witch_of_the_eye (game, card, replicated: bool = False):
  """ Witch of the Eye: Return a card from your discard pile to your hand.
  """
  logging.info(f"{card.title}'s reap ability triggered.")
  active = game.activePlayer.discard

  game.drawFriendDiscard = True
  for c in game.chooseCards("Discard", "Return a card from your discard pile to your hand:", "friend"):
    # I can skip pending b/c this card is guaranteed to belong to the active player
    active.remove(c)
    game.activePlayer.hand.append(c)