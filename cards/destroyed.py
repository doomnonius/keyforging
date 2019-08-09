# This is all the destroyed and leaves play effects
# Also include things like Krump?

###########
## Basic ##
###########

def basicLeaves(game, card):
    """ Called for when a card (almost only creatures, with a few unusual artifacts) leaves the board from play (not just destroyed, so to archive, hand, purge as well). It will reset the card, deal with upgrades staying behind or going away, deal with amber remaining on the card. All dest functions will call this function as their last step.
    """

#############
## Brobnar ##
#############


funcDict = {}

def keyMagda(card, deck, oppamber, myamber):
    """ Opponent steals two amber from controller of this minion. Takes amber amounts as args, and returns adjusted. Also takes card and deck so it can manipulate them.
    """
    oppamber += 2
    myamber -= 2
    if card.health <= 0:
        basic(card, deck)
    return oppamber, myamber

def addFunctions(card):
    """ Returns value, which should be a tuple of 5 different functions.
    """
    for x in range(1, 371):
        if x == int(card.number):
            for key, value in funcDict.items():
                if key == card.title:
                    return value

def makeFuncList(deck):
    dirList = []
    for x in dir():
        if str(x)[0:3] == "key":
            dirList.append(x)
    global funcDict
    for card in deck:
        funcDict.update(card.title, addFunctions(card))

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')