import decks.decks as deck
import cards.cardsAsClass as card
import cards.board as board
import decks.discards as discard
import decks.purges as purge
import decks.archives as archive
import json
import random

##################
# Contains modules:
# choosedecks
# developer (incomplete)
# distance
# load
# startup
# startGame
# turn
# responses
##################

active = ''
Deck1 = {}
Deck2 = {}

def distance(first, second):
    '''Returns the edit distance between the strings first and second.'''

    if first == '':
        return len(second)
    elif second == '':
        return len(first)
    elif first[0] == second[0]:
        return distance(first[1:], second[1:])
    else:
        substitution = 1 + distance(first[1:], second[1:])
        deletion = 1 + distance(first[1:], second)
        insertion = 1 + distance(first, second[1:])
        return min(substitution, deletion, insertion)

def developer():
    """Developer functions for manually changing the game state.
    """

def chooseDecks(): #called by startup()
    """The players choose their decks from deckDict, and if their choice isn't there they are offered the option to import a deck.
    """
    global Deck1, Deck2
    print("Available decks:")
    with open('decks/deckList.json') as f:
        data = json.load(f)
        for x in range(0, len(data)):
            print(str(x+1) + ': ' + data[x]['name'])
    deckChoice = input("Choose player 1's deck by index or name: ")
    # try:
    intChoice = int(deckChoice)
    if intChoice - 1 >= 0:
        Deck1 = deck.Deck(deck.deckName(intChoice - 1))
        print(Deck1)
        print(Deck1.deck[0])
    else:
        print("Please enter numbers only.")
        chooseDecks()
    # some code here to list player 2's options, which is all the decks except the one player 1 just chose
    print("Available decks:")
    with open('decks/deckList.json') as f:
        data = json.load(f)
        for x in range(0, len(data)):
            if data[x]['name'] != Deck1.name:
                print(str(x+1) + ': ' + data[x]['name'])
    # technically they can still choose the same deck, which I'll allow
    deckChoice2 = input("Choose player 2's deck by index or name: ")
    try:
        intChoice2 = int(deckChoice2)
        if intChoice2 - 1 >= 0:
            Deck2 = deck.Deck(deck.deckName(intChoice2 - 1))
    except:
        print("Please enter numbers only.")
        chooseDecks()
    startGame()

def load(saveFile):
    """Loads a saved game.
    """

def startup(): #Called at startup
    """The initial starting of the game. Includes importing the decks (and possibly loading a saved game).
    """
    print("Game is starting up!")
    choice = input("What would you like to do: [Import] a new deck, start a [NewGame], list imported [Decks], or [Load] a game? \n>>> ")
    if distance(choice, "Import") <= 1:
        deck.importDeck()
        another = input("Would you like to import another deck (Y/n)? ")
        while another != 'n' and another != 'N':
            deck.importDeck()
            another = input("Would you like to import another deck (Y/n)? ")
    elif distance(choice, "NewGame") <= 2:
        chooseDecks()
    elif distance(choice, "Load") <= 1:
        # Display saved games, then let them choose one.
        # display saves here !!!!
        loaded = input("Which save would you like to load?")
        load(loaded)
    elif distance(choice, "Decks") <= 1:
        while True:
            print("Available decks:")
            with open('decks/deckList.json') as f:
                data = json.load(f)
                for x in range(0, len(data)):
                    print(str(x+1) + ': ' + data[x]['name'])
            startup()
            break

def startGame(): #called by choosedecks()
    """Determines first player, fills hands, allows for mulligans and redraws, then plays the first turn, because that turn follows special rules.
    """
    global Deck1, Deck2
    first = random.choice([Deck1, Deck2])
    if first == Deck1:
        Deck1.draw(7)
        Deck2.draw(6)
        second = Deck2
    else:
        Deck2.draw(7)
        Deck1.draw(6)
        second = Deck1
    for card in first.hand:
        print(card)
    mull = input("Would you like to mulligan?")
    if mull == "Yes" or "Y" or "y":
        for card in first.hand:
            first.deck.append(card)
        random.shuffle(first.deck)
        first.hand = []
        first.draw(6)
    for card in second.hand:
        print(card)
    mull2 = input("Would you like to mulligan?")
    if mull2 == "Yes" or "Y" or "y":
        for card in second.hand:
            second.deck.append(card)
        random.shuffle(second.deck)
        second.hand = []
        second.draw(5)


def turn():
    """The choices the player can make once they have chosen their active house.
    """

def responses():
    """This is called once the game is started.
    """
    choice = input("What would you like to do? (h for help): ")
    while choice != '':
        #Potential choices: Hand, Boards, Discards, Purges
        if choice == 'h' or choice == 'H':
            print("Available commands are 'House', 'Hand', 'MyBoard', 'OppBoard', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'Keys', 'Amber', 'Card', 'MyDeck', 'OppDeck', and 'EndTurn'. I might even add a save game function at some point.")
            choice2 = input("Type a command here to learn more about it, or press enter to return: ")
            while choice2 != '':
                if distance(choice2, "Hand") <= 1:
                    print("Lists the names of the cards in your hand.")
                elif distance(choice2, "MyBoard") <= 1:
                    print("Lists the creatures and artifacts on your side of the board.")
                elif distance(choice2, "OppBoard") <= 1:
                    print("Lists the creatures and artifacts on your opponent's side of the board.")
                elif distance(choice2, "MyDiscard") <= 1:
                    print("Lists the contents of your discard pile.")
                elif distance(choice2, "OppDiscard") <= 1:
                    print("Lists the contents of your opponent's discard pile.")
                elif distance(choice2, "MyPurge") <= 1:
                    print("Lists your purged cards.")
                elif distance(choice2, "OppPurge") <= 1:
                    print("Lists your opponent's purged cards.")
                elif distance(choice2, "Keys") <= 1:
                    print("Lists how many keys each player has.")
                elif distance(choice2, "Amber") <= 1:
                    print("Lists how much amber each player has.")
                elif distance(choice2, "MyDeck") <= 1:
                    print("Returns the number of cards in your deck.")
                elif distance(choice2, "OppDeck") <= 1:
                    print("Returns the number of cards in your opponent's deck. ")
                elif distance(choice2, "EndTurn") <= 1:
                    print("Ends your turn.")
                elif distance(choice2, "Card") <= 1:
                    print("Search for a card by name (only looks at the first six letters).")
                else:
                    print("That is not recognized as a command.")
                responses()
        elif choice == "developer":
            developer()
        elif distance(choice, "Hand") <= 1:
            # get to this part later
            print(deck.nameList(deck.MyHand))
        elif distance(choice, "House") <= 1:
            house = input("Which house would you like to declare? ")
            if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
                global active
                active = house
                house = "none"
                print("You've chosen " + active + " as your active house.")
                turn()
            else:
                print("That's not a valid house.")
                responses()
        elif distance(choice, "MyBoard") <= 1:
            print("Creatures", deck.nameList(board.MyBoard))
            print("Creatures", deck.nameList(board.MyArt))
        elif distance(choice, "Card") <= 1:
            cardIn = input("Enter the name of the card you are looking for: ")
            [card.printdetails(card.listdetails(x)) for x in deck.allCards if distance(cardIn[0:7], x.title[0:7]) <= 2]
        responses()
    