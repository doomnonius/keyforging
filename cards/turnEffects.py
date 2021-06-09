import logging

###########
# Brobnar #
###########

def eot_rogue_ogre (game, card):
  """ Rogue Ogre: If you only played one card this turn, Rogue Ogre heals 2 damage and captures 1 amber.
  """
  if len(game.playedThisTurn) == 1:
    logging.info(f"{card.title}'s eot effect has triggered.")
    card.damage -= min(2, card.damage)
    card.capture(game, 1)

#######
# Dis #
#######

def eot_shaffles (game, card):
  """ Shaffles: Your opponent loses 1 amber.
  """
  logging.info(f"{card.title}'s eot effect has triggered.")
  game.inactivePlayer.amber -= min(1, game.inactivePlayer.amber)