import logging
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
  logging.info(f"{card.title} leaving play.")
  card.returned = True

def destroy(card, game):
  """ Destroys a card owned by player. Make sure you call pending afterwards
  """
  if card.type == "Creature":
    card.destroyed = True
    logging.info(f"{card.title} destroyed")
  elif card.type == "Artifact":
    card.destroyed = True
    logging.info(f"{card.title} destroyed")

def stealAmber(thief, victim, num, game):
  """ Function for stealing amber.
  """
  # this will account for edge cases that allow the inactive player to steal amber (namely, Magda leaving play)
  if "the_vaultkeeper" in [x.title for x in victim.board["Creature"]]:
    logging.info("The steal effect fails because of Vaultkeeper.")
    return
  if victim.amber >= num:
    victim.amber -= num
    thief.gainAmber(num, game)
    logging.info(f"{thief.name} stole {num} amber from {victim.name}.")
  else:
    thief.gainAmber(victim.amber, game)
    if victim.amber == 0:
      logging.info("Your opponent had no amber to steal.")
      return
    logging.info(f"Your opponent only had {victim.amber} amber for you to steal.")
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
      if "blypyp" in activeS and activeS["blypyp"]:
        if reset:
          activeS["blypyp"] = 0
        return True
      if "swap_widget" in activeS and activeS["swap_widget"]:
        return True
    if "speed_sigil" in [x.title for x in game.activePlayer.board["Artifact"] + game.inactivePlayer.board["Artifact"]]:
      c_played = sum(x.type == "Creature" for x in game.playedThisTurn)
      if (not c_played and not reset) or (c_played == 1 and reset):
        return True
  if "soft_landing" in activeS and activeS["soft_landing"] and (card.type == "Creature" or card.type == "Artifact"):
    if reset:
      activeS["soft_landing"] = 0
    return True