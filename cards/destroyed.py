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

#############
## Brobnar ##
#############



if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')