import pyautogui
from cards.play import passFunc
from cards.destroyed import armageddon_cloak as ac, phoenix_heart as ph, biomatrix_backup as bb
from cards.reap import basicReap, red_planet_ray_gun as rprg, duskrunner as dr, silent_dagger as sd
from cards.fight import basicFight, rocket_boots as rb
from cards.actions import transposition_sandals as ts


def blood_of_titans (game, card, side: str, choice: int):
  """ Blood of Titans: This creature has +5 power.
  """
  passFunc(game, card)
  if side == "fr":
    game.activePlayer.board["Creature"][choice].power += 5
  else:
    game.inactivePlayer.board["Creature"][choice].power += 5

def phoenix_heart (game, card, side:str, choice: int):
  """ Phoenix Heart: This creature gains “Destroyed: Return this creature to its owner’s hand and deal 3<D> to each creature in play.”
  """
  passFunc(game, card)
  if side == "fr":
    game.activePlayer.board["Creature"][choice].dest.append(ph)
  else:
    game.inactivePlayer.board["Creature"][choice].dest.append(ph)

def yo_mama_mastery (game, card, side: str, choice: int):
  """Yo Mama Mastery: Fully heal this creature
  """
  passFunc(game, card)
  if side == "fr":
    game.activePlayer.board["Creature"][choice].damage = 0
    game.activePlayer.board["Creature"][choice].taunt = True
  else:
    game.inactivePlayer.board["Creature"][choice].damage = 0
    game.inactivePlayer.board["Creature"][choice].taunt = 0
    
def collar_of_subordination(game, card, side:str, choice:int):
  """ Collar of Subordiation: You control this creature
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    pyautogui.alert("Dude, what are you doing?")
  else:
    c = inactive[choice]
    flank = game.chooseHouse("custom", ("Put the minion on your left flank or your right flank?", ["Left", "Right"]))
    if flank == "Left":
      flank = 0
    else:
      flank = len(active)
    active.insert(flank, c)
    inactive.remove(c)

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

def experimental_therapy (game, card, side: str, choice: int):
  """ Experimental Therapy: Stun and exhaust this creature.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.stun = True
  c.ready = False

def rocket_boots (game, card, side: str, choice: int):
  """ Rocket Boots: This creature gains, “Fight/Reap: If this is the first time this creature was used this turn, ready it.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if c.fight == [basicFight]:
    c.fight = [rb]
  else:
    c.fight.append(rb)
  if c.reap == [basicReap]:
    c.reap = [rb]
  else:
    c.reap.append(rb)

def transposition_sandals (game, card, side: str, choice: int):
  """ Transposition Sandals: This creature gains, “Action: Swap this creature with another friendly creature in the battleline. You may use that other creature this turn.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if c.action:
    c.action.append(ts)
  else:
    c.action = [ts]

def biomatrix_backup (game, card, side: str, choice: int):
  """ Biomatrix Backup: This creature gains, “Destroyed: You may put this creature into its owner's archives.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.dest.append(bb)

def brain_stem_antenna (game, card, side: str, choice: int):
  """ Brain Stem Antenna: This creature gains, “After you play a Mars creature, ready this creature and for the remainder of the turn it belongs to house Mars.”
  """
  passFunc(game, card)

def jammer_pack (game, card, side: str, choice: int):
  """ Jammer Pack: This creature gains, “Your opponent's keys cost +2<A>.“
  """
  passFunc(game, card)

def red_planet_ray_gun (game, card, side:str, choice: int):
  """ Red Planet Ray Gun: This creature gains, “Reap: Choose a creature. Deal 1<D> to that creature for each Mars creature in play.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if c.reap == [basicReap]:
    c.reap = [rprg]
  else:
    c.append(rprg)
  
def armageddon_cloak (game, card, side: str, choice: int):
  """ Armageddon Cloak: This creature gains hazardous 2 and, “Destroyed: Fully heal this creature and destroy Armageddon Cloak instead.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.hazard += 2
  c.dest.append(ac)

def mantle_of_the_zealot (game, card, side: str, choice: int):
  """ Mantle of the Zealot: This creature gains, “You may use this creature as if it belonged to the active house.”
  """
  passFunc(game, card)

def protect_the_weak (game, card, side: str, choice: int):
  """ Protect the Weak: This creature gets +1 armor and gains taunt.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.extraArm += 1
  c.taunt = True

def shoulder_armor (game, card, side: str, choice: int):
  """ Shoulder Armor: While this creature is on a flank, it get +2 armor and +2 power.
  """
  passFunc(game, card)
  # this one will be implemented in the cardChanged function

def duskrunner (game, card, side: str, choice: int):
  """ Duskrunner: This creature gains, “Reap: Steal 1A.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if c.reap == [basicReap]:
    c = [dr]
  else:
    c.append(dr)

def ring_of_invisibility (game, card, side: str, choice: int):
  """ Ring of Invisibility: This creature gains elusive and skirmish.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.elusive = True
  c.skirmish = True

def silent_dagger (game, card, side: str, choice: int):
  """ Silent Dagger: This creature gains, “Reap: Deal 4<D> to a flank creature.”
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  if c.reap == [basicReap]:
    c = [sd]
  else:
    c.append(sd)

def way_of_the_bear (game, card, side: str, choice: int):
  """ Way of the Bear: This creature gains assault 2.
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.assault += 2

def way_of_the_wolf (game, card, side:str, choice: int):
  """ Way of the Wolf: This creature gains skirmish
  """
  passFunc(game, card)
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if side == "fr":
    c = active[choice]
  else:
    c = inactive[choice]
  c.skirmish = True