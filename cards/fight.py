import pyautogui

def basicFight(game, card, attacked):
  """This checks for things that create before fight effects, if there are any. Like, for example, if something attacks Krump or similar and dies.
  """
  if card.temp_skirmish:
    card.temp_skirmish = False
    # this won't happen if a card dies, should be in card.reset() anyway
  if card.updateHealth():
    ... # generic stuff?
  # check if you've died attacking Krump?
    

def basicBeforeFight(game, card):
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

#######
# Dis #
#######

#########
# Logos #
#########

def rocket_boots (game, card):
  """ Rocket Boots: If this is the first time this creature was used this turn, ready it.
  """
  pass

########
# Mars #
########



###########
# Sanctum #
###########



###########
# Shadows #
###########

###########
# Untamed #
###########

if __name__ == '__main__':
  print ('This statement will be executed only if this script is called directly')