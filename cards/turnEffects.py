import os

import pygame, logging

###########
# Brobnar #
###########

def eot_rogue_ogre (game, card):
  if len(game.playedThisTurn) == 1:
    card.damage -= 2
    if card.damage < 0:
      card.damage = 0
    card.capture(game, 1)