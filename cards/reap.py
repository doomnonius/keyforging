from functools import reduce
import random
import pyautogui
from helpers import stealAmber, destroy, return_card

def basicReap(game, card, replicated: bool = False):
  if "dimension_door" in game.activePlayer.states and game.activePlayer.states["dimension_door"]:
    stealAmber(game.activePlayer, game.inactivePlayer, 1, game)
  else:
    game.activePlayer.gainAmber(1, game)
  # game.log("You now have " + str(game.activePlayer.amber) + " amber.")


###########
# Brobnar #
###########

def kelifi_dragon (game, card, replicated: bool = False):
  """ Kelifi Dragon: Gain 1 amber. Deal 5 damage to a creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  game.activePlayer.gainAmber(1, game)
  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 5 damage to a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, 5)
  c.updateHealth()
  if c.destroyed:
    pending.append(c)
  game.pending()

def looter_goblin (game, card, replicated: bool = False):
  """ Looter Goblin: for the remainder of the turn, gain 1 amber each time an enemy creature is destroyed.
  """
  game.activePlayer.states[card.title] += 1
  game.resetStates.append(("a", card.title))

def troll (game, card, replicated: bool = False):
  """ Troll: Troll heals 3 damage.
  """
  card.damage -= min(3, card.damage)


#######
# Dis #
#######

def eater_of_the_dead (game, card, replicated: bool = False):
  """ Purge a creature from a discard pile. If you do, put a +1 power counter on Eater of the Dead.
  """
  active = game.activePlayer.discard
  inactive = game.inactivePlayer.discard
  if sum(x.type == "Creature" for x in active):
    game.drawFriendDiscard = True
  if sum(x.type == "Creature" for x in inactive):
    game.drawEnemyDiscard = True
  
  count = sum(x.type == "Creature" for x in active + inactive)
  if not count:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Discard", "Purge a creature from a discard pile:")[0]
  if side == "fr":
    c = active[choice]
    game.activePlayer.purge.append(c)
    active.remove(c)
  else:
    c = inactive[choice]
    game.inactivePlayer.purge.append(c)
    inactive.remove(c)
  
  card.extraPow += 1
  card.power += 1

def guardian_demon (game, card, replicated: bool = False):
  """ Guardian Demon: Heal up to 2 damage from a creature. Deal that amount of damage to another creature
  """
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

def master_of_1 (game, card, replicated: bool = False):
  """ Master of 1: You may destroy a creature with 1 power.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.power == 1 for x in active + inactive)

  if not count:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Destroy a creature with 1 power:", condition = lambda x: x.power == 1, con_message = "That creature does not have 1 power.")[0]
  if side == "fr":
    c = active[choice]
    destroy(c, game.activePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  else:
    c = inactive[choice]
    destroy(c, game.inactivePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()


def master_of_2 (game, card, replicated: bool = False):
  """ Master of 2: You may destroy a creature with 2 power.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.power == 2 for x in active + inactive)

  if not count:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Destroy a creature with 2 power:", condition = lambda x: x.power == 2, con_message = "That creature does not have 2 power.")[0]
  if side == "fr":
    c = active[choice]
    destroy(c, game.activePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  else:
    c = inactive[choice]
    destroy(c, game.inactivePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()

def master_of_3 (game, card, replicated: bool = False):
  """ Master of 3: You may destroy a creature with 3 power.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.power == 3 for x in active + inactive)

  if not count:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Destroy a creature with 3 power:", condition = lambda x: x.power == 3, con_message = "That creature does not have 3 power.")[0]
  if side == "fr":
    c = active[choice]
    destroy(c, game.activePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  else:
    c = inactive[choice]
    destroy(c, game.inactivePlayer, game)
    if c.destroyed:
      game.pendingReloc.append(c)
  
  game.pending()

def snudge (game, card, replicated: bool = False):
  """ Snudge: Return an artifact or flank creature to its owner's hand.
  """
  active = game.activePlayer.board
  inactive = game.inactivePlayer.board
  pendingDisc = game.pendingReloc

  targetType = game.chooseHouse("custom", ("Would you like to target an artifact or a flank creature?", ["Artifact", "Creature"]))[0]
  side, choice = game.chooseCards(targetType, f"Return a {targetType.lower()} to its owner's hand:", condition = lambda x: x.type == "Artifact" or x.isFlank(game))[0]
  if side == "fr":
    c = active[targetType][choice]
  else:
    c = inactive[targetType][choice]
  c.returned = True
  pendingDisc.append(c)
  game.pending("hand")

def tocsin (game, card, replicated: bool = False):
  """ Tocsin: your opponent discards a random card from their hand.
  """
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
  game.activePlayer += 1

def doc_bookton (game, card, replicated: bool = False):
  """ Doc Bookton: Draw a card
  """
  game.activePlayer += 1

def ganymede_archivist (game, card, replicated: bool = False):
  """ Ganymede Archivist: archive a card
  """
  if game.activePlayer.hand:
    archive = game.chooseCards("Hand", "Choose a card from your hand to archive:")[0][1]
    card = game.activePlayer.hand[archive]
    game.pendingReloc.append(card)
    game.activePlayer.hand.remove(card)
    game.pending("archive", target = game.activePlayer)

def neutron_shark (game, card, replicated: bool = False):
  """ Neutron Shark: Destroy an enemy creature or artifact and a friendly creature or artifact. Discard the top card of your deck. If that card is not a Logos card, trigger this effect again.
  """
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

def ozmo_martianologist (game, card, replicated: bool = False):
  """ Ozmo, Martianologist: Heal 3 damage from a Mars creature or stun a Mars creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  side, choice = game.chooseCards("Creature", "Choose a Mars creature to heal or stun:", condition = lambda x: x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade], con_message = "That creature is not from house Mars.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  action = game.chooseHouse("custom", (f"Would you like to stun {c.title.replace('_', ' ').title()} or heal three damage?", ["Stun", "Heal"]), colors = ["YELLOW", "RED"])[0]
  if action == "Heal":
    c.damage -= min(3, c.damage)
  else:
    c.stun = True

def psychic_bug (game, card, replicated: bool = False):
  """ Psychic Bug: Look at your opponent's hand.
  """
  for card in game.inactivePlayer.hand:
    card.revealed = True

def replicator (game, card, replicated: bool = False):
  """ Replicator: Trigger the reap effect of another creature in play as if you controlled that creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.reap for x in active + inactive if x.title != "replicator")
  if not count:
    pyautogui.alert("No reap effects to copy.")
    return

  side, choice = game.chooseCards("Creature", "Choose a reap effect to copy:", condition = lambda x: x.title != 'replicator' and x.reap and x.title != "sanctum_guardian", con_message = "That creature doesn't have a reap effect you can copy:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if len(c.reap) > 1:
    pass # make them choose one, need a function for this kind of thing
  else:
    c.reap[0](game, c, True)

def vespilon_theorist (game, card, replicated: bool = False):
  """ Vespilon Theorist: Choose a house. Reveal the top card of your deck. If it is of that house, archive it and gain 1. Otherwise, discard it.
  """
  deck = game.activePlayer.deck
  hold = []
  house = game.chooseHouse("other")
  if deck:
    hold.append(deck.pop())
  else:
    pyautogui.alert("Deck is empty, no card was discarded.")
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
  game.activePlayer.states[card.title] = 1
  # this one still needs to be in reset states in case it isn't triggered
  game.resetStates.append(("a", card.title))
    
def chuff_ape (game, card, replicated: bool = False):
  """ Chuff Ape: You may sacrifice another friendly creature. If you do, fully heal Chuff Ape.
  """
  active = game.activePlayer.board["Creature"]

  choice = game.chooseCards("Creature", "You may sacrifice another creature to fully heal Chuff Ape:", full = False)
  if not choice:
    pyautogui.alert("No creature is sacrificed.")
    return
  
  choice = active[choice[0][1]]
  destroy(choice, game.activePlayer, game)
  if choice.destroyed:
    game.pendingReloc.append(choice)
    card.damage = 0
  game.pending()

def grabber_jammer (game, card, replicated: bool = False):
  """ Grabber Jammer: Capture 1 amber.
  """
  card.capture(game, 1, replicated)

def john_smyth (game, card, replicated: bool = False):
  """ John Smyth: Ready a non-agent Mars creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if sum((x.house == "Mars"or "experimental_therapy" in [y.title for y in x.upgrade]) and "Agent" not in x.traits for x in active + inactive):
    side, choice = game.chooseCards("Creature", "Ready a non-agent Mars creature:", condition = lambda x: (x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade]) and "Agent" not in x.traits, con_message = "That creature is either an agent or isn't from house Mars.")[0]
    if side == "fr":
      c = active[choice]
    else:
      c = inactive[choice]
    c.ready = True

def qyxxlyx_plague_master (game, card, replicated: bool = False):
  """ Qyxxlyx Plague Master: Deal 3 damage to each human creature. This damage cannot be prevented by armor.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active:
    c.damageCalc(game, 3, armor = False)
    c.updateHealth()
  for c in inactive:
    c.damageCalc(game, 3, armor = False)
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
  active = game.activePlayer.board["Creature"]

  if not sum(x.house != "Mars" and "experimental_therapy" not in [y.title for y in x.upgrade] for x in active):
    pyautogui.alert("No valid targets.")
    return

  choice = active[game.chooseCards("Creature", "Use a friendly non-Mars creature:", "friend", condition = lambda x: x.house != "Mars" and "experimental_therapy" not in [y.title for y in x.upgrade], con_message = "You must pick a creature that doesn't belong to house Mars.")[0][1]]
  
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

def uxlyx_the_zookeeper (game, card, replicated: bool = False):
  """ Reap: Put an enemy creature into your archives.
  """
  inactive = game.inactivePlayer.board["Creature"]
  
  if not inactive:
    pyautogui.alert("Your opponent has no creatures to target.")
  
  choice = game.chooseCards("Creature", f"Choose an enemy creature to put into your archives:", "enemy")[0][1]
  c = inactive[choice]
  return_card(c, game)
  if c.returned:
    game.pendingReloc.append(c)
  game.pending("archive", target = game.activePlayer)

def vezyma_thinkdrone (game, card, replicated: bool = False):
  """ Reap: You may archive a friendly creature or artifact from play.
  """
  active = game.activePlayer.board["Creature"]
  activeA = game.activePlayer.board["Artifact"]

  targetType = game.chooseHouse("custom", ("Would you like to archive a Creature or an Artifact?", ["Creature", "Artifact"]))
  choice = game.chooseCards(targetType, f"You may archive a friendly {targetType.lower()} from play:", "friend", full = False)
  if not choice:
    pyautogui.alert("Nothing will be archived.")
    return

  if targetType == "Creature":
    c = active[choice]
  else:
    c = activeA[choice]
  return_card(c, game)
  if c.returned:
    game.pendingReloc.append(c)
  game.pending("archive", target = game.activePlayer)

def yxilo_bolter (game, card, replicated: bool = False):
  """ Yxilo Bolter: Deal 2 damage to a creaure. If this damage destroys that creature, purge it.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not active and not inactive:
    pyautogui.alert("No valid targets.") # this is impossible
    return

  side, choice = game.chooseCards("Creature", "Deal 2 damage to a creature. If this damage destroys the creature, purge it:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(2, game)
  c.updateHealth()
  if c.destroyed:
    pending.append(c)
    game.pending('purge')

def zyzzix_the_many (game, card, replicated: bool = False):
  """ Zyzzix the Many: You may reveal a creature from your hand. If you do, archive it and Zyzzix the many gets three +1 power counters.
  """
  hand = game.activePlayer.hand
  choice = game.chooseCards("Hand", "You may reveal a creature from your hand:", full = False, condition = lambda x: x.type == "Creature", con_message = "You must choose a creature.")
  if not choice:
    pyautogui.alert("Nothing revealed.")
    return
  choice = hand[choice[0][1]]
  choice.reveal = True
  game.activePlayer.archive.append(choice)
  hand.remove(choice)
  card.extraPow += 3
  card.power += 3

def red_planet_ray_gun (game, card, replicated: bool = False):
  """ Red Planet Ray Gun: Choose a creature. Deal 1 damage to that creature for each Mars creature in play.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  count = sum(x.house == "Mars" or "experimental_therapy" in [y.title for y in x.upgrade] for x in active + inactive)
  side, choice = game.chooseCards("Creature", f"Deal {count} damage to a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, 0)
  if c.destroyed:
    game.pendingReloc.append(c)
  game.pending()

###########
# Sanctum #
###########

def commander_remiel (game, card, replicated: bool = False):
  """ Commander Remiel: Use a friendly non-Sanctum creature.
  """
  active = game.activePlayer.board["Creature"]

  if not sum(x.house != "Sanctum" and "experimental_therapy" not in [y.title for y in x.upgrade] for x in active):
    pyautogui.alert("No valid targets.")
    return

  choice = active[game.chooseCards("Creature", "Use a friendly non-Sanctum creature:", "friend", condition = lambda x: x.house != "Sanctum" and "experimental_therapy" not in [y.title for y in x.upgrade], con_message = "You must pick a creature that doesn't belong to house Sanctum.")[0][1]]
  
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

def grey_monk (game, card, replicated: bool = False):
  """ Grey Monk: Heal 2 damage from a creature
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if not active + inactive:
    pyautogui.alert("No damaged creatures.")
    return
  
  side, choice = game.chooseCards("Creature", "Heal 2 damage:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damage -= min(c.damage, 2)

def horseman_of_famine (game, card, replicated: bool = False):
  """ Horseman of Famine: Destroy the least powerful creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  low = min(x.power for x in (active + inactive))
  pendingD = game.pendingReloc

  if not active and not inactive:
    return

  side, choice = game.chooseCards("Creature", "Destroy a creature with the lowest power:", condition = lambda x: x.power == low, con_message = "That creature does not have the lowest power.")[0]
  if side == "fr":
    c = active[choice]
    destroy(c, game.activePlayer, game)
    if c.destroyed:
      pendingD.append(c)
  else:
    c = inactive[choice]
    destroy(c, game.inactivePlayer, game)
    if c.destroyed:
      pendingD.append(c)
  game.pending()

def horseman_of_pestilence (game, card, replicated: bool = False):
  """ Horseman of Pestilence: Deal 1 damage to each non-Horseman creature.
  """
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

def protectrix (game, card, replicated: bool = False):
  """ Protectrix: You may fully heal a creature. If you do, that creature cannot be dealt damage for the remainder of the turn.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if not active + inactive:
    pyautogui.alert("No damaged creatures.")
    return
  
  side, choice = game.chooseCards("Creature", "Fully heal a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damage = 0
  c.damagable = False
  game.resetCard.append((c, "damagable"))

def sanctum_guardian (game, card, replicated: bool = False):
  """ Sanctum Guardian: Swap SG with another friendly creature in your battleline.
  """
  active = game.activePlayer.board["Creature"]

  if len(active) < 2:
    pyautogui.alert("No creatures to swap with.")
    return
  
  choice = active[game.chooseCards("Creature", "Swap positions with another friendly creature in your battleline.", "friend", condition = lambda x: x != card)[0][1]]
  sg_i = active.index(card)
  other_i = active.index(choice)
  active[sg_i], active[other_i] = active[other_i], active[sg_i]

def sequis (game, card, replicated: bool = False):
  """ Sequis: Capture 1 amber.
  """
  card.capture(game, 1, replicated)

###########
# Shadows #
###########

def bulleteye (game, card, replicated: bool = False):
  """ Bulleteye: Destroy a flank creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if not active + inactive:
    pyautogui.alert("No valid targets.") # no idea how this could happen
    return
  
  side, choice = game.chooseCards("Creature", "Destroy a flank creature:", condition = lambda x: x.isFlank(game), con_message = "That is not a flank creature.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  destroy(c, game.activePlayer, game) # destroy doesn't use the player so it's fine
  if c.destroyed:
    game.pendingReloc.append(c)
  game.pending()

def faygin (game, card, replicated: bool = False):
  """ Faygin: Return an Urchin from play or from your discard pile to your hand.
  """
  discard = game.activePlayer.discard
  active = game.activePlayer.board["Creature"]

  areas = []
  if sum(x.title == "urchin" for x in discard):
    areas.append("Discard")
  if sum(x.title == "urchin" for x in active):
    areas.append("Board")

  if not areas:
    pyautogui.alert("No valid targets.")
    return

  if len(areas) == 1:
    targetType = areas[0]
  else:
    targetType = game.chooseHouse("custom", ("Where would you like to return an Urchin from?", areas))
  if targetType == "Board":
    targetType == "Creature"

  if targetType == "Discard":
    game.drawFriendDiscard = True
  choice = game.chooseCards(targetType, "Choose an Urchin to return to your hand:", "friend", condition = lambda x: x.title == "urchin", con_message = "That's not an Urchin")[0][1]
  if targetType == "Discard":
    c = discard[choice]
    discard.remove(c)
    game.activePlayer.hand.append(c)
    return
  
  c = active[choice]
  return_card(c)
  if c.returned:
    game.pendingReloc.append(c)
  game.pending("hand")

def nexus (game, card, replicated: bool = False):
  """ Nexus: Use an enemy artifact as if it were yours.
  """
  inactive = game.inactivePlayer.board["Artifact"]
  if len(inactive) > 0:
    choice = game.chooseCards("Artifact", "Choose an opponent's artifact to use:", "enemy")[0][1]
    if inactive[choice].ready and inactive[choice].action:
      inactive[choice].action(game, game.inactivePlayer.board["Artifact"][choice])
      inactive[choice].ready = False
  else:
    pyautogui.alert("Your opponent has no artifacts. The card is stil played.")

def selwyn_the_fence (game, card, attacked):
  """ Selwyn the Fence: move 1 amber from one of your cards to your pool.
  """
  active = game.activePlayer.board["Creature"]
  activeA = game.activePlayer.board["Artifact"]

  if sum(x.captured for x in active) and sum(x.captured for x in activeA):
    targetType = game.chooseHouse("custom", ("Would you like to target a friendly artifact or a friendly creature?", ["Artifact", "Creature"]))[0]
  elif sum(x.captured for x in active):
    targetType = "Creature"
  elif sum(x.captured for x in activeA):
    targetType = "Artifact"
  else:
    pyautogui.alert("There is no amber on your cards.")
    return

  choice = game.chooseCards(targetType, f"Move an amber from a friendly {targetType.lower()} to your pool:", "friend", condition = lambda x: x.captured > 0, con_message = "That card has no amber on it.")[0][1]
  if targetType == "Creature":
    c = active[choice]
  else:
    c = activeA[choice]
  c.captured -= 1
  game.activePlayer.gainAmber(1, game)

def smiling_ruth (game, card, replicated: bool = False):
  """ Smiling Ruth: If you forged a key this turn, take control of an enemy flank creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if game.forgedThisTurn:

    if not inactive:
      pyautogui.alert("No enemy creatures to steal!")
      return

    choice = inactive[game.chooseCards("Creature", "Choose an enemy flank creature to steal:", "enemy", condition = lambda x: x.isFlank(game), con_message = "You didn't choose a flank creature. Please try again.")[0][1]]
    flank = game.chooseFlank(choice)
    # game.chooseHouse("custom", ("Put the minion on your left flank or your right flank?", ["Left", "Right"]))
    if flank == "Left":
      flank = 0
    else:
      flank = len(active)
    active.insert(flank, choice)
    inactive.remove(choice)

def duskrunner (game, card, replicated: bool = False):
  """ Duskrunner: Steal 1 amber.
  """
  stealAmber(game.activePlayer, game.inactivePlayer, 1, game)

def silent_dagger (game, card, replicated: bool = False):
  """ Silent Dagger: Deal 4 damage to a flank creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 4 damage to a flank creature:", condition = lambda x: x.isFlank(game), con_message = "Not a flank creature.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, 4)
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
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  side, choice = game.chooseCards("Creature", "Stun and exhaust a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.ready = False
  c.stun = True

def dew_faerie (game, card, replicated: bool = False):
  """ Dew Faerie: Gain 1 amber.
  """
  game.activePlayer.gainAmber(1, game)

def inka_the_spider (game, card, replicated: bool = False):
  """ Inka the Spider: Stun a creature.
  """
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
  
def kindrith_longshot (game, card, replicated: bool = False):
  """ Kindrith Longshot: Deal 2 damage to a creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  if not active and not inactive:
    pyautogui.alert("No valid targets.")
    return

  side, choice = game.chooseCards("Creature", "Deal 2 damage to a creature:")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, 2)
  c.updateHealth()
  if c.destroyed:
    pending.append(c)
  game.pending()

def piranha_monkeys (game, card, replicated: bool = False):
  """ Piranha Monkeys: Deal 2 damage to each other creature.
  """
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

def witch_of_the_eye (game, card, replicated: bool = False):
  """ Witch of the Eye: Return a card from your discard pile to your hand.
  """
  active = game.activePlayer.discard

  if not active:
    pyautogui.alert("No cards in your discard.")
    return

  game.drawFriendDiscard = True
  choice = game.chooseCard("Discard", "Return a card from your discard pile to your hand:")[0][1]
  # I can skip pending b/c this card is guaranteed to belong to the active player
  c = active[choice]
  active.remove(c)
  game.activePlayer.hand.append(c)