import decks.decks as deck
import cards.cardsAsClass as card
import cards.board as board
import decks.discards as discard
import decks.purges as purge
import decks.archives as archive

active = ''

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

def startup():
    """The initial starting of the game. Includes importing the decks (and possibly loading a saved game).
    """

def turn():
    """The choices the player can make once they have chosen their active house.
    """

def responses():
    """This is called once the game is started.
    """
    choice = input("What would you like to do? (h for help): ")
    #Potential choices: Hand, Boards, Discards, Purges
    if choice == 'h' or choice == 'H':
        print("Available commands are 'House', 'Hand', 'MyBoard', 'OppBoard', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'Keys', 'Amber', 'Card', 'MyDeck', 'OppDeck', and 'EndTurn'. I might even add a save game function at some point.")
        choice2 = input("Type a command here to learn more about it, or press q to return: ")
        if choice2 == 'q' or choice2 =='Q':
            responses()
        elif distance(choice2, "Hand") <= 1:
            print("Lists the names of the cards in your hand.")
            responses()
        elif distance(choice2, "MyBoard") <= 1:
            print("Lists the creatures and artifacts on your side of the board.")
            responses()
        elif distance(choice2, "OppBoard") <= 1:
            print("Lists the creatures and artifacts on your opponent's side of the board.")
            responses()
        elif distance(choice2, "MyDiscard") <= 1:
            print("Lists the contents of your discard pile.")
            responses()
        elif distance(choice2, "OppDiscard") <= 1:
            print("Lists the contents of your opponent's discard pile.")
            responses()
        elif distance(choice2, "MyPurge") <= 1:
            print("Lists your purged cards.")
            responses()
        elif distance(choice2, "OppPurge") <= 1:
            print("Lists your opponent's purged cards.")
            responses()
        elif distance(choice2, "Keys") <= 1:
            print("Lists how many keys each player has.")
            responses()
        elif distance(choice2, "Amber") <= 1:
            print("Lists how much amber each player has.")
            responses()
        elif distance(choice2, "MyDeck") <= 1:
            print("Returns the number of cards in your deck.")
            responses()
        elif distance(choice2, "OppDeck") <= 1:
            print("Returns the number of cards in your opponent's deck. ")
            responses()
        elif distance(choice2, "EndTurn") <= 1:
            print("Ends your turn.")
            responses()
        elif distance(choice2, "Card") <= 1:
            print("Search for a card by name (only looks at the first six letters).")
            responses()
        else:
            print("That is not recognized as a command.")
            responses()
    elif choice == "developer":
        developer()
    elif distance(choice, "Hand") <= 1:
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
    