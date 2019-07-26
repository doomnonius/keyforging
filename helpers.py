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

# I should make a Game class, so I can have activeHouse and activePlayer and Deck1 and Deck2 effectively as global variables
class Game():
    def __init__(self, first, second):
        """ first is first player, which is determined before Game is created.
        """
        self.activeHouse = ''
        self.activePlayer = deck.Deck(deck.deckName(first - 1))
        self.inactivePlayer = deck.Deck(deck.deckName(second - 1))

    def __repr__(self):
        s = ''
        s += "Opponent's board:\nCreatures:\n"
        for x in range(len(self.inactivePlayer.board["Creature"])):
            s += str(x+1) + ': ' + self.inactivePlayer.board["Creature"][x].title + '\n'
        s += "Artifacts: \n"
        for x in range(len(self.inactivePlayer.board["Artifact"])):
            s += str(x+1) + ': ' + self.inactivePlayer.board["Artifact"][x].title + '\n'
        s += "Your board:\nCreatures:\n"
        for x in range(len(self.activePlayer.board["Creature"])):
            # print(x) #test line
            s += str(x+1) + ': ' + self.activePlayer.board["Creature"][x].title + '\n'
        s += "Artifacts: \n"
        for x in range(len(self.activePlayer.board["Artifact"])):
            s += str(x+1) + ': ' + self.activePlayer.board["Artifact"][x].title + '\n'
        return s

    def switch(self):
        """ Swaps active and inactive players.
        """
        self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer
        # print(self) # test line: passed on 7/25

    def startGame(self): #called by choosedecks()
        """Fills hands, allows for mulligans and redraws, then plays the first turn, because that turn follows special rules.
        """
        self.activePlayer += 7
        self.activePlayer.printHand()
        mull = input("Player 1, would you like to mulligan? \n>>>")
        if mull == "Yes" or mull == "Y" or mull == "y":
            for card in self.activePlayer.hand:
                self.activePlayer.deck.append(card)
            random.shuffle(self.activePlayer.deck)
            self.activePlayer.hand = []
            self.activePlayer += 6
        # for card in self.activePlayer.hand:
        #     print(card)
        self.inactivePlayer += 6
        self.inactivePlayer.printHand()
        mull2 = input("Player 2, would you like to mulligan? \n>>>")
        if mull2 == "Yes" or mull2 == "Y" or mull2 == "y":
            for card in self.inactivePlayer.hand:
                self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
        self.activePlayer.printHand()
        try:
            play = int(input("Player 1, enter the number of the card you would like to play: "))
        except:
            play = int(input("Player 1, enter the *number* of the card you would like to play: "))
        x = self.activePlayer.hand[play].type
        if x != "Upgrade": #technically don't need this here, no upgrades first turn
            self.activePlayer.board[x].append(self.activePlayer.hand.pop(play))
            print(self) # test line
        self.switch() # switches active and inactive players
        self.turn()

    def turn(self):
        """ The passive actions of a turn. 1: Forge key (if poss, and if miasma hasn't changed the state; also reset state); 2: Calls chooseHouse(); 3: calls responses(), which needs to be moved into this class, and represents all actions (playing, discarding, fighting, etc) and info seeking; 4: ready cards; 5: draw cards.
        """

    def chooseHouse(self, var):
        """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards.
        """

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
        # print(Deck1)
        # print(Deck1.deck[0])
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
    except:
        print("Please enter numbers only.")
        chooseDecks()
    first = random.choice([intChoice, intChoice2])
    # print(first)
    if first == intChoice:
        second = intChoice2
    else:
        second = intChoice
    global game
    game = Game(first, second)
    game.startGame()

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
            game.activePlayer.printHand()
        elif distance(choice, "House") <= 1:
            house = input("Which house would you like to declare? ")
            if house in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
                global activeHouse
                activeHouse = house
                house = "none"
                print("You've chosen " + activeHouse + " as your active house.")
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
    