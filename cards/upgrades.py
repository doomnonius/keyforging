from cards.play import passFunc

def yo_mama_mastery(game, card, side: str, choice: int):
  """Yo Mama Mastery: Fully heal this creature
  """
  passFunc(game, card)
  # I'm going to only handle the play effect, I'll write something else to handle upgrades later
  # whatever that looks like, this card is going to be attached first, so we'll need to heal the attached card
  if side == "fr":
    game.activePlayer.board["Creature"][choice].damage = 0
  else:
    game.inactivePlayer.board["Creature"][choice].damage = 0

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