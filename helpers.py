from typing import Dict


##################
# Contains modules:
# absa
# makeChoice
# chooseSide
# stealAmber
# willEnterReady
##################

def return_card(card, game):
  # here is where we could check for ward
  card.returned = True

def destroy(card, player, game):
  """ Destroys a card owned by player. Make sure you call pending afterwards
  """
  if card.type == "Creature":
    card.destroyed = True
    # if "armageddon_cloak" not in [x.title for x in card.upgrade]:
    #   player.board["Creature"].remove(card)
  elif card.type == "Artifact":
    card.destroyed = True
    # player.board["Artifact"].remove(card)

def stealAmber(thief, victim, num, game):
  """ Function for stealing amber.
  """
  # this will account for edge cases that allow the inactive player to steal amber (namely, Magda leaving play)
  if "The Vaultkeeper" in [x.title for x in victim.board["Creature"]]:
    print("The steal effect fails because of Vaultkeeper.")
    return
  if victim.amber >= num:
    victim.amber -= num
    thief.gainAmber(num, game)
    print(f"{thief.name} stole {num} amber from {victim.name}.")
  else:
    thief.gainAmber(victim.amber, game)
    if victim.amber == 0:
      print("Your opponent had no amber to steal.")
      return
    print(f"Your opponent only had {victim.amber} amber for you to steal.")
    victim.amber = 0


def willEnterReady(game, card, reset: bool = True):
  """ Returns whether or not a card will enter ready.
  """
  activeS = game.activePlayer.states

  if card.type == "Action" or card.type == "Upgrade":
    return False
  
  if card.type == "Creature":
    if card.title == "silvertooth":
      return True
    if card.house == "Mars":
      if "blypyp" in activeS and activeS["blypyp"] and card.house == "Mars":
        if reset:
          activeS["blypyp"] = 0
        return True
    if "speed_sigil" in [x.title for x in game.activePlayer.board["Artifact"] + game.inactivePlayer.board["Artifact"]]:
      c_played = sum(x.type == "Creature" for x in game.playedThisTurn)
      if (not c_played and not reset) or (c_played == 1 and reset):
        return True
  if "soft_landing" in activeS and activeS["soft_landing"] and (card.type == "Creature" or card.type == "Artifact"):
    if reset:
      activeS["soft_landing"] = 0
    return True