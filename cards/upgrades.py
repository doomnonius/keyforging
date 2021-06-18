import logging
from cards.play import passFunc
from cards.destroyed import armageddon_cloak as ac, phoenix_heart as ph, biomatrix_backup as bb
from cards.reap import red_planet_ray_gun as rprg, duskrunner as dr, silent_dagger as sd
from cards.fight import rocket_boots as rb
from cards.actions import transposition_sandals as ts

###########
# Brobnar #
###########

def blood_of_titans (game, card, target):
  """ Blood of Titans: This creature has +5 power.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.power += 5

def phoenix_heart (game, card, target):
  """ Phoenix Heart: This creature gains “Destroyed: Return this creature to its owner’s hand and deal 3<D> to each creature in play.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.dest.append(ph)

def yo_mama_mastery (game, card, target):
  """Yo Mama Mastery: Fully heal this creature
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.damage = 0
  target.taunt = True

#######
# Dis #
#######

def collar_of_subordination(game, card, target):
  """ Collar of Subordiation: You control this creature
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  active = game.activePlayer.board["Creature"]
  inactive = game.inactivePlayer.board["Creature"]
  if target in active:
    logging.info("Dude, what are you doing?")
  elif target in inactive:
    flank = game.chooseFlank(target)
    if flank == "Left":
      flank = 0
    else:
      flank = len(active)
    active.insert(flank, target)
    inactive.remove(target)

def flame_wreathed (game, card, target):
  """ This creature gains hazardous 2 and +2 power.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.power += 2
  target.hazard += 2

#########
# Logos #
#########

def experimental_therapy (game, card, target):
  """ Experimental Therapy: Stun and exhaust this creature.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.stun = True
  target.ready = False

def rocket_boots (game, card, target):
  """ Rocket Boots: This creature gains, “Fight/Reap: If this is the first time this creature was used this turn, ready it.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.fight.append(rb)
  target.reap.append(rb)

def transposition_sandals (game, card, target):
  """ Transposition Sandals: This creature gains, “Action: Swap this creature with another friendly creature in the battleline. You may use that other creature this turn.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.action.append(ts)

########
# Mars #
########

def biomatrix_backup (game, card, target):
  """ Biomatrix Backup: This creature gains, “Destroyed: Put this creature into its owner's archives.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.dest.append(bb)

def brain_stem_antenna (game, card, target):
  """ Brain Stem Antenna: This creature gains, “After you play a Mars creature, ready this creature and for the remainder of the turn it belongs to house Mars.”
  """
  passFunc(game, card)

def jammer_pack (game, card, target):
  """ Jammer Pack: This creature gains, “Your opponent's keys cost +2<A>.“
  """
  passFunc(game, card)

def red_planet_ray_gun (game, card, target):
  """ Red Planet Ray Gun: This creature gains, “Reap: Choose a creature. Deal 1<D> to that creature for each Mars creature in play.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.reap.append(rprg)
  
###########
# Sanctum #
###########

def armageddon_cloak (game, card, target):
  """ Armageddon Cloak: This creature gains hazardous 2 and, “Destroyed: Fully heal this creature and destroy Armageddon Cloak instead.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.hazard += 2
  target.dest.append(ac)

def mantle_of_the_zealot (game, card, target):
  """ Mantle of the Zealot: This creature gains, “You may use this creature as if it belonged to the active house.”
  """
  passFunc(game, card)

def protect_the_weak (game, card, target):
  """ Protect the Weak: This creature gets +1 armor and gains taunt.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.extraArm += 1
  target.taunt = True

def shoulder_armor (game, card, target):
  """ Shoulder Armor: While this creature is on a flank, it get +2 armor and +2 power.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  if target.isFlank(game):
    target.extraArm += 2
  # this one will be implemented in the cardChanged function

###########
# Shadows #
###########

def duskrunner (game, card, target):
  """ Duskrunner: This creature gains, “Reap: Steal 1A.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.reap.append(dr)

def ring_of_invisibility (game, card, target):
  """ Ring of Invisibility: This creature gains elusive and skirmish.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.elusive = True
  target.skirmish = True

def silent_dagger (game, card, target):
  """ Silent Dagger: This creature gains, “Reap: Deal 4<D> to a flank creature.”
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.reap.append(sd)

###########
# Untamed #
###########

def way_of_the_bear (game, card, target):
  """ Way of the Bear: This creature gains assault 2.
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.assault += 2

def way_of_the_wolf (game, card, target):
  """ Way of the Wolf: This creature gains skirmish
  """
  passFunc(game, card)
  logging.info(f"{card.title} has been played.")
  target.skirmish = True