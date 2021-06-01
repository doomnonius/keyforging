from helpers import stealAmber

def basicReap(game, card):
  if "dimension_door" in game.activePlayer.states and game.activePlayer.states["dimension_door"]:
    stealAmber(game.activePlayer, game.inactivePlayer, 1)
  else:
    game.activePlayer.gainAmber(1, game)
  # game.log("You now have " + str(game.activePlayer.amber) + " amber.")


###########
# Brobnar #
###########

#######
# Dis #
#######

#
# Logos #
#

#
# Mars #
#

def red_planet_ray_gun (game, card):
  """ Red Planet Ray Gun: Choose a creature. Deal 1 damage to that creature for each Mars creature in play.
  """
  pass

#
# Sanctum #
#

#
# Shadows #
#

def duskrunner (game, card):
  """ Duskrunner: Steal 1 amber.
  """
  pass

def silent_dagger (game, card):
  """ Silent Dagger: Deal 4 damage to a flank creature.
  """
  pass

#
# Untamed #
#