import pyautogui

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