import logging

###########
# Brobnar #
###########

def eot_rogue_ogre (game, card):
  """ Rogue Ogre: If you only played one card this turn, Rogue Ogre heals 2 damage and captures 1 amber.
  """
  if sum(v for k,v in game.playedThisTurn.items()) == 1:
    logging.info(f"{card.title}'s eot effect has triggered.")
    card.heal(2)
    card.capture(1, game)

#######
# Dis #
#######

def eot_shaffles (game, card):
  """ Shaffles: Your opponent loses 1 amber.
  """
  logging.info(f"{card.title}'s eot effect has triggered.")
  game.inactivePlayer.amber -= min(1, game.inactivePlayer.amber)