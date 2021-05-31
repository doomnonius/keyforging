from cards.play import passFunc
# from dest import armageddon_cloak, phoenix_heart

def yo_mama_mastery(game, card, side: str, choice: int):
  """Yo Mama Mastery: Fully heal this creature
  """
  passFunc(game, card)
  if side == "fr":
    game.activePlayer.board["Creature"][choice].damage = 0
    game.activePlayer.board["Creature"][choice].taunt = True
  else:
    game.inactivePlayer.board["Creature"][choice].damage = 0
    game.inactivePlayer.board["Creature"][choice].taunt = 0

def blood_of_titans(game, card, side: str, choice: int):
  """ Blood of Titans: This creature has +5 power.
  """
  passFunc(game, card)
  if side == "fr":
    game.activePlayer.board["Creature"][choice].power += 5
  else:
    game.inactivePlayer.board["Creature"][choice].power += 5
    
def flame_wreathed (game, card, side:str, choice:int):
  """ This creature gains hazardous 2 and +2 power.
  """
  passFunc(game, card)
  if side == "fr":
    game.activePlayer.board["Creature"][choice].power += 2
    game.activePlayer.board["Creature"][choice].hazard += 2
  else:
    game.inactivePlayer.board["Creature"][choice].power += 2
    game.inactivePlayer.board["Creature"][choice].hazard += 2