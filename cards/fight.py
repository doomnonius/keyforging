import pyautogui
from helpers import stealAmber, destroy

def basicFight(game, card, attacked):
  """This checks for things that create before fight effects, if there are any. Like, for example, if something attacks Krump or similar and dies.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if card.temp_skirmish:
    card.temp_skirmish = False
    # this won't happen if a card dies, should be in card.reset() anyway
  if attacked.destroyed:
    game.destInFight.append(attacked) # warchest
    if not card.destroyed:
      if card.title == "krump": # one offs for Krump and etc
        game.inactivePlayer.amber -= min(1, game.inactivePlayer.amber)
      elif card.title == "mugwump":
        card.damage = 0
        card.extraPow += 1
        card.power += 1
      elif card.title == "overlord_greking":
        attacked.greking = card
      elif card.title == "stealer_of_souls":
        attacked.stealer = True
        game.activePlayer.gainAmber(1, game)
      elif card.title == "brain_eater":
        game.activePlayer += 1
      elif card.title == "grommid":
        game.inactivePlayer.amber -= min(1, game.inactivePlayer.amber)
      elif card.title == "francus":
        card.capture(game, 1)
  if card.destroyed and not attacked.destroyed:
    if attacked.title == "krump": # one offs for Krump and etc
      game.activePlayer.amber -= min(1, game.activePlayer.amber)
    elif attacked.title == "mugwump":
      attacked.damage = 0
      attacked.extraPow += 1
      attacked.power += 1
    elif attacked.title == "overlord_greking":
      card.greking = attacked
    elif attacked.title == "stealer_of_souls":
      card.stealer = True
      game.activePlayer.gainAmber(1, game)
    elif attacked.title == "brain_eater":
      game.inactivePlayer += 1
    elif attacked.title == "grommid":
      game.activePlayer.amber -= min(1, game.activePlayer.amber)
    elif attacked.title == "francus":
      attacked.capture(game, 1)
    
    

def basicBeforeFight(game, card, attacked):
  """ This checks for things that create before fight effects, like take hostages
      It will be called by all before fight effects, or by cards that have no before fight effects.
  """
  print("Start of basic before fight.")
  if "warsong" in game.activePlayer.states:
    game.activePlayer.gainAmber(game.activePlayer.states["warsong"], game)
  print("After warsong.")
  if "take_hostages" in game.activePlayer.states:
    card.capture(game, game.activePlayer.states["take_hostages"])
  print("After take hostages.")
  if "halacor" in [x.title for x in game.activePlayer.board["Creature"]] and card.isFlank():
    card.temp_skirmish = True
  print("End of basic before fight.")
  if "stampede" in game.activePlayer.states:
    game.activePlayer.states["stampede"] += 1


###########
# Brobnar #
###########

def before_firespitter (game, card, attacked):
  """ Firespitter: Deal 1 damage to each enemy creature:
  """
  basicBeforeFight(game, card)
  
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pending = game.pendingReloc

  for c in active:
    c.damageCalc(game, 1)
    c.updateHealth(game.activePlayer)
  for c in inactive:
    c.damageCalce(game, 1)
    c.updateHealth(game.inactivePlayer)
  for c in active[::-1]:
    if c.destroyed:
      pending.append(c)
  for c in inactive[::-1]:
    if c.destroyed:
      pending.append(c)

  game.pending()

def headhunter (game, card, attacked):
  """ Headhunter: gain 1 amber
  """
  game.activePlayer.gainAmber(1, game)

def kelifi_dragon (game, card, attacked):
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


#######
# Dis #
#######

def eater_of_the_dead (game, card, attacked):
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

def before_gabos_longarms (game, card, attacked):
  """ Gabos Longarms: choose a creature. Gabos deals damage to that creature rather than the one it is fighting.
  """
  basicBeforeFight(game, card, attacked)
  active = game.activePlayer.discard
  inactive = game.inactivePlayer.discard
  side, choice = game.chooseCards("Creature", f"Deal Gabos' {card.power} damage to:", condition = lambda x: x != attacked, con_message = "Gabos can't deal his damage to the creature he is attacking.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.damageCalc(game, card.power)
  c.updateHealth()
  if c.destroyed:
    game.pendingReloc.append(c)
  game.pending()

def guardian_demon (game, card, attacked):
  """ Guardian Demon: Heal up to 2 damage from a creature. Deal that amount of damage to another creature
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  pendingDisc = game.pendingReloc
  # easy case: no damage
  if sum([x.damage for x in game.activePlayer.board["Creature"]] + [x.damage for x in game.inactivePlayer.board["Creature"]]) == 0:
    pyautogui.alert("There are no damaged creatures, so the play effect doesn't happen. The card is still played.")
    return
  choice = game.chooseCards("Creature", "Choose a creature:")[0]
  if choice[0] == "fr":
    card1 = active[choice[1]]
    if card1.damage > 0:
      heal = int(game.chooseHouse("custom", ("How much damage would you like to heal?", list(range(min(3, card1.damage + 1)))))[0])
    else:
      pyautogui.alert("There was no damage on this creature, so no damage will be dealt.")
      return
  else:
    card1 = inactive[choice[1]]
    if card1.damage > 0:
      heal = int(game.chooseHouse("custom", ("How much damage would you like to heal?", list(range(min(3, card1.damage + 1)))))[0])
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

def snudge (game, card, attacked):
  """ Snudge: Return an artifact or flank creature to its owner's hand.
  """
  active = game.activePlayer.board
  inactive = game.inactivePlayer.board
  pendingDisc = game.pendingReloc

  targetType = game.chooseHouse("custom", ("Would you like to target an artifact or a flank creature?", ["Artifact", "Creature"]))[0]
  side, choice = game.chooseCards(targetType, f"Return a {targetType.lower} to its owner's hand:", condition = lambda x: x.type == "Artifact" or x.isFlank(game))[0]
  if side == "fr":
    c = active[targetType][choice]
  else:
    c = inactive[targetType][choice]
  c.returned = True
  pendingDisc.append(c)
  game.pending()

#########
# Logos #
#########

def batdrone (game, card, attacked):
  """ Batdrone: Steal 1 amber
  """
  stealAmber(game.activePlayer, game.inactivePlayer, 1)

def quixo_the_adventurer (game, card, attacked):
  """ Quixo the Adventurer: Draw a card
  """
  game.activePlayer += 1

def neutron_shark (game, card):
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

def ozmo_martianologist (game, card, attacker):
  """ Ozmo, Martianologist: Heal 3 damage from a Mars creature or stun a Mars creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  side, choice = game.chooseCards("Creature", "Choose a Mars creature to heal or stun:", condition = lambda x: x.house == "Mars", con_message = "That creature is not from house Mars.")[0]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  action = game.chooseHouse("custom", (f"Would you like to stun {c.title.replace('_', ' ').title()} or heal three damage?", ["Stun", "Heal"]), colors = ["YELLOW", "RED"])[0]
  if action == "Heal":
    c.damage -= min(3, c.damage)
  else:
    c.stun = True


def rocket_boots (game, card, attacked):
  """ Rocket Boots: If this is the first time this creature was used this turn, ready it.
  """
  if card not in game.usedThisTurn:
    card.ready = True

########
# Mars #
########

def chuff_ape (game, card, attacked):
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
    
def grabber_jammer (game, card, attacked):
  """ Grabber Jammer: Capture 1 amber.
  """
  card.capture(game, 1)

def john_smyth (game, card, attacked):
  """ John Smyth: Ready a non-agent Mars creature.
  """
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]

  if sum(x.house == "Mars" and "Agent" not in x.traits for x in active + inactive):
    side, choice = game.chooseCards("Creature", "Ready a non-agent Mars creature:", condition = lambda x: x.house == "Mars" and "Agent" not in x.traits, con_message = "That creature is either an agent or isn't from house Mars.")[0]
    if side == "fr":
      c = active[choice]
    else:
      c = inactive[choice]
    c.ready = True

def qyxxlyx_plague_master (game, card, attacked):
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

def ulyq_megamouth (game, card, attacked):
  """ Ulyq Megamouth: Use a friendly non-Mars creature.
  """
  active = game.activePlayer.board["Creature"]

  if not sum(x.house != "Mars" for x in active):
    pyautogui.alert("No valid targets.")
    return

  choice = active[game.chooseCards("Creature", "Use a friendly non-Mars creature:", "friend", condition = lambda x: x.house != "Mars", con_message = "You must pick a creature that doesn't belong to house Mars.")[0][1]]
  
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
  
  use = game.chooseHouse("custom", ("How would you like to use this creature?", uses))[0]
  if use[0] == "R":
    if game.canReap(card, r_click = True, cheat = True):
      game.reapCard(active.index(choice), cheat = True)
  elif use[0] == "F":
    if game.canFight(card, r_click = True, cheat = True):
      game.fightCard(active.index(choice), cheat=True)
  elif use[0] == "A":
    if game.canAction(card, r_click = True, cheat = True):
      game.actionCard(active.index(choice), cheat = True)

def yxilo_bolter (game, card, attacked):
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

def before_zorg (game, card, attacked):
  """ Zorg: Stun the creature Zorg fights and each of that creature's neighbors.
  """
  basicBeforeFight(game, card, attacked)
  attacked.stun = True
  for neigh in attacked.neighbors(game):
    neigh.stun = True

def zyzzix_the_many (game, card, attacked):
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

###########
# Sanctum #
###########

def champion_tabris (game, card, attacked):
  """ Champion Tabris: Capture 1 amber.
  """
  card.capture(game, 1)

def horseman_of_famine (game, card):
  """ Horseman of Famine: Destroy the least powerful creature.
  """
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

def before_lord_golgotha (game, card, attacked):
  """ Lord Golgotha: Deal 3 damage to each neighbor of the creature Lord Golgotha fights.
  """
  basicBeforeFight (game, card, attacked)
  for n in attacked.neighbors(game):
    n.damageCalc(game, 3)
    n.updateHealth()
  for n in attacked.neighbors(game):
    if n.destroyed:
      game.pendingReloc.append(n)

  game.pending()

def sanctum_guardian (game, card, attacked):
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


###########
# Shadows #
###########

def mooncurser (game, card, attacked):
  """ Mooncurser: Steal 1 amber
  """
  stealAmber(game.activePlayer, game.inactivePlayer, 1)

def dodger (game, card, attacked):
  """ Dodger: Steal 1 amber.
  """
  stealAmber(game.activePlayer, game.inactivePlayer, 1)

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

def umbra (game, self, card):
  """ Umbra: steal 1 amber
  """
  stealAmber(game.activePlayer, game.inactivePlayer, 1)

###########
# Untamed #
###########

if __name__ == '__main__':
  print ('This statement will be executed only if this script is called directly')