# This is all the destroyed and leaves play effects
# Also include things like Krump?

###########
## Basic ##
###########

# def basicLeaves(game, card):
#     """ Called for when a card (almost only creatures, with a few unusual artifacts) leaves the board from play (not just destroyed, so to archive, hand, purge as well). It will reset the card, deal with upgrades staying behind or going away, deal with amber remaining on the card. All dest functions will call this function as their last step.
#     """
#     card.reset()

# I don't want to use a basic dest because things can have more than one destroyed effect. Going to incoporate the aspects of basic dest in pending somehow

# def basicDest(game, card):
#     """ Called for when a card is destroyed.
#     """
#     # loot the bodies
#     # return captured amber if a creature, don't if an artifact
#     # handle upgrades
#     card.reset() # I think this should be last

###########
# Brobnar #
###########

def phoenix_heart (game, card):
  """ Phoenix Heart: Return this creature to its owner's hand and deal 3 damage to each creature.
  """
  pass


#######
# Dis #
#######

#########
# Logos #
#########

# Harland mindlock too

########
# Mars #
########

def biomatrix_backup (game, card):
  """ Biomatrix Backup: Fully heal this creature and destroy armageddon cloak instead.
  """
  pass

###########
# Sanctum #
###########

def armageddon_cloak (game, card):
  """ Armageddon Cloak" If this creature would be destroyed, 
  """
  card.hazard -= 2
  card.damage = 0
  for c in card.upgrade[::-1]:
    if c.title == "armageddon_cloak":
      game.pendingReloc.append(c)
      card.upgrade.remove(c)
  game.pending()

# gray monk too

###########
# Shadows #
###########

###########
# Untamed #
###########


if __name__ == '__main__':
  print ('This statement will be executed only if this script is called directly')