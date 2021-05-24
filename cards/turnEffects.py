import os

import pygame, logging

def basic_eot (game, card):
  card.armor = card.base_armor + card.extraArm


###########
# Brobnar #
###########

def eot_rogue_ogre (game, card):
  """ card text goes here
  """
  basic_eot(game, card)
  if len(game.playedThisTurn) == 1:
    card.damage -= 2
    if card.damage < 0:
      card.damage = 0
    card.capture(game, 1)