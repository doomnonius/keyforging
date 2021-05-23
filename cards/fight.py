import pyautogui

def basicFight(game, card):
  """This checks for things that create before fight effects, if there are any.
  """
  if card.temp_skirmish:
    card.temp_skirmish = False
    # this won't happen if a card dies, should be in card.reset() anyway
  if card.updateHealth():
    ... # generic stuff?
  # check if you've died attacking Krump?
    

def basicBeforeFight(game, card):
  """ This checks for things that create before fight effects, like take hostages
      It will be called by all before fight effects, or 
  """
  if "warsong" in game.activePlayer.states:
      game.activePlayer.amber += game.activePlayer.states["warsong"]
  if "take_hostages" in game.activePlayer.states:
      card.capture(game, game.activePlayer.states["take_hostages"])
  if "halacor" in [x.title for x in game.activePlayer.board["Creatures"]] and card.isFlank():
      card.temp_skirmish = True

if __name__ == '__main__':
  print ('This statement will be executed only if this script is called directly')