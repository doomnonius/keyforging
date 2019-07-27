# This is all the destroyed and leaves play effects
# Also include things like Krump?

funcDict = {}

###########
## Basic ##
###########

def basicDest(card, deck, purge = False, archive = False, addDeck = False):
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

def keynum():
    """ This needs to return the functions that this card will have.
    """
    def playnum():
        """ Amber increases will be done before this call, then does card effect.
        """
        return func
    def fightnum():
        """
        """
        return func
    def reapnum():
        """
        """
        return func
    def actionnum():
        """
        """
        return func
    def destnum():
        """
        """
        return func
    play = playnum()
    fight = fightnum()
    reap = reapnum()
    action = actionnum()
    dest = destnum()
    
    return play, fight, reap, action, dest

def key001():
    """ Anger: Ready and fight w/ a friendly creature.
    """

    def play001():
        """ Then ready and fight with a friendly minion.
        """
        return func
    def fight001():
        """
        """
        return func
    def reap001():
        """
        """
        return func
    def action001():
        """
        """
        return func
    def dest001():
        """
        """
        return func
    play = play001()
    fight = fight001()
    reap = reap001()
    action = action001()
    dest = dest001()
    
    return play, fight, reap, action, dest

def keyMagda(card, deck, oppamber, myamber):
    """ Opponent steals two amber from controller of this minion. Takes amber amounts as args, and returns adjusted. Also takes card and deck so it can manipulate them.
    """
    oppamber += 2
    myamber -= 2
    if card.health <= 0:
        basic(card, deck)
    return oppamber, myamber

def addFunctions(card):
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
        funcDict.update(card.title, (basic))

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')