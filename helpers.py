import decks.decks as deck
import cards.cardsAsClass as card
import cards.board as board
import decks.discards as discard
import decks.purges as purge
import decks.archives as archive

def distance(first, second):
    '''Returns the edit distance between first and second.'''

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

def responses():
    choice = input("What would you like to do? (h for help): ")
    #Potential choices: Hand, Boards, Discards, Purges
    if choice == 'h' or choice == 'H':
        print("Available commands are 'House', 'Hand', 'MyBoard', 'OppBoard', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'Keys', 'Amber', 'MyDeck', 'OppDeck', and 'EndTurn'. You may also type the name of any card to see more details about it.")
        choice2 = input("Type a command here to learn more about it, or press q to return.")
        if choice2 == 'q' or choice2 =='Q':
            responses()
        elif distance(choice2, "Hand") <= 1:
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
        elif distance(choice2, "EndTurn"):
            print("Ends your turn.")
    else:
        if distance(choice, "Hand") <= 1:
            print(deck.nameList(deck.MyHand))