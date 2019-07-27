# This is all the destroyed and leaves play effects
# Also include things like Krump?

###########
## Basic ##
###########

def basicDest(game, purge = False, archive = False, addDeck = False):
    """ Basic function, decides which of these four to call. Needs to be fed the deck to check states to decide this. Optionals are for cards that explicitly purge or archive or add to deck but won't have states.
    """
    
    def addToDiscard(card, deck):
        """Add a card to the discard pile.
        """

    def addToPurge(card, deck):
        """Add a card to the purged pile.
        """
        deck.purged.append(card)
        del card

    # This only has a few states to look out for, at least. Only one state will affect purging.
    for key, value in deck.states["Destroyed"].items():
        if key == "Annihilation Ritual" and value:
            addToPurge(card, deck)

    def addToArchive(card, deck):
        """Add a card to the archive.
        """

    def addToDeck(card, deck):
        """Add a card to the deck.
        """
    
    
def sortDest(name):
    """ Defines a lot of destroyed functions, and returns the relevant one. This will be a long function.
    """
    

#############
## Brobnar ##
#############

def key001(game):
    """ Anger: Ready and fight w/ a friendly creature.
    """
    basicDest(game)

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