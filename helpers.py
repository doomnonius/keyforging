import decks.decks as deck
import cards.cardsAsClass as card
import cards.destroyed as dest
import cards.actions as action
import cards.play as play
import cards.reap as reap
import cards.fight as fight
# import cards.board as board # not using this
# import decks.discards as discard # not using this
# import decks.purges as purge # not using this
# import decks.archives as archive # not using this
import json
import random
import time

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

class Game():
    def __init__(self, first, second):
        """ first is first player, which is determined before Game is created and entered as an input. deck.deckName is a function that pulls the right deck from the list.
        """
        self.activeHouse = ''
        self.first = first - 1
        self.second = second - 1
        self.activePlayer = deck.Deck(deck.deckName(first - 1))
        self.inactivePlayer = deck.Deck(deck.deckName(second - 1))

    def __repr__(self):
        s = ''
        s += "\nOpponent's board:\nCreatures:\n"
        for x in range(len(self.inactivePlayer.board["Creature"])):
            s += str(x+1) + ': ' + str(self.inactivePlayer.board["Creature"][x]) + '\n'
        s += "Artifacts: \n"
        for x in range(len(self.inactivePlayer.board["Artifact"])):
            s += str(x+1) + ': ' + str(self.inactivePlayer.board["Artifact"][x]) + '\n'
        s += "\nYour board:\nCreatures:\n"
        for x in range(len(self.activePlayer.board["Creature"])):
            # print(x) #test line
            s += str(x+1) + ': ' + str(self.activePlayer.board["Creature"][x]) + "\n"
        s += "Artifacts: \n"
        for x in range(len(self.activePlayer.board["Artifact"])):
            s += str(x+1) + ': ' + str(self.activePlayer.board["Artifact"][x]) + '\n'
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
        print("\nPlayer 1's hand:")
        self.activePlayer.printShort(self.activePlayer.hand)
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
        print("\nPlayer 2's hand:")
        self.inactivePlayer.printShort(self.inactivePlayer.hand)
        mull2 = input("Player 2, would you like to mulligan? \n>>>")
        if mull2 == "Yes" or mull2 == "Y" or mull2 == "y":
            for card in self.inactivePlayer.hand:
                self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
        self.activePlayer.printShort(self.activePlayer.hand)
        while True:
            try:
                chosen = int(input("Player 1, enter the number of the card you would like to play: "))
                break
            except:
                pass
        x = self.activePlayer.hand[chosen].type
        while chosen != '':
            if x != "Upgrade": #technically don't need this here, no upgrades first turn
                self.activePlayer.board[x].append(self.activePlayer.hand.pop(chosen))
                # print(self) # test line
                break
            else:
                # make them try again
                print("You can't play an upgrade on an empty board. Try again.")
                time.sleep(1)
                while True:
                    try:
                        chosen = int(input("Player 1, enter the number of the card you would like to play: "))
                        break
                    except:
                        pass
        # ready played card
        for creature in self.activePlayer.board["Creature"]:
            creature.ready = True
            creature.armor = creature.base_armor
        for artifact in self.activePlayer.board["Artifact"]:
            artifact.ready = True
        self.activePlayer.drawEOT()
        self.switch() # switches active and inactive players
        self.turn(2)

    def turn(self, num):
        """ The passive actions of a turn. 1: Forge key (if poss, and if miasma hasn't changed the state; also reset state); 2: Calls chooseHouse(); 3: calls responses(), which needs to be moved into this class, and represents all actions (playing, discarding, fighting, etc) and info seeking; 4: ready cards; 5: draw cards. num is the turn number.
        """
        while True:
            print("\nTurn: " + str(num))
            time.sleep(1)
            print(self) # step 0: show the board state
            time.sleep(1)
            print("You have", self.activePlayer.amber, "amber and", self.activePlayer.keys, "keys. Your opponent has", self.inactivePlayer.amber, "amber and", self.inactivePlayer.keys, "keys.\n")
            time.sleep(1)
            # step 1: check if a key is forged, then forge it
            # all code is here because it's short
            if self.checkForgeStates():
                if self.activePlayer.amber >= self.activePlayer.keyCost:
                    self.activePlayer.amber -= self.activePlayer.keyCost
                    self.activePlayer.keys += 1
                    print("You forged a key for", self.activePlayer.keyCost, "amber. You now have", self.activePlayer.keys, "key(s) and", self.activePlayer.amber, "amber.\n") # it works!
            else:
                print("Forging skipped this turn!")
            if self.activePlayer.keys >= 3:
                break
            # step 2: the player chooses a house
            # outsourced b/c multipurpose
            self.chooseHouse("activeHouse")
            # step 3: call responses
            # outsourced b/c long
            self.responses()
            # step 4: ready cards and reset armor
            # here b/c short
            for creature in self.activePlayer.board["Creature"]:
                creature.ready = True
                creature.armor = creature.base_armor
            for artifact in self.activePlayer.board["Artifact"]:
                artifact.ready = True
            # step 5.1: draw cards
            self.activePlayer.drawEOT()
            print("Checking draw:", self.activePlayer.handSize == len(self.activePlayer.hand)) # test line
            # step 5.2: check for EOT effects
            self.checkEOTStates()
            # step 5.3: switch players
            self.switch()
            # step 5.4: increment num
            num += 1
        self.endGame()

    def checkForgeStates(self):
        """ Checks if there is anything in Deck.states["Forge"]. Implementation for other things is still hazy.
        """
        if len(self.activePlayer.states["Forge"]) != 0:
            for key in self.activePlayer.states["Forge"]:
                # I don't see anything to do but have each possible card here, but for testing purposes I'm only going to include Miasma
                if key == True:
                    if self.activePlayer.states["Forge"]["Miasma"]:
                        self.activePlayer.states["Forge"]["Miasma"] = False
                    return False
        return True

    def checkEOTStates(self):
        """ Checks for end of turn effects. There aren't more than a couple in CotA.
        """

    def checkPlayStates(self):
        """ Checks for play states (full moon, etc.)
        """

    def checkFightStates(self, attacker = None):
        """ Checks for fight states (warsong, etc) or before fight effects, or stun or exhaust.
        """
        if attacker.stun == True:
            return False
        if attacker.ready == False:
            return False
        if "Before fight:" in attacker.text or "Before Fight:" in attacker.text:
            return True
        return True

    def chooseHouse(self, varAsStr):
        """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards like control the weak.
        """
        if varAsStr == "activeHouse":
            print("Your hand is: ")
            self.activePlayer.printShort(self.activePlayer.hand)
            choice = input("Choose a house. Your deck's houses are " + self.activePlayer.houses[0] + ", " + self.activePlayer.houses[1] + ", " + self.activePlayer.houses[2] + ".\n>>>").title()
            if choice in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
                self.activeHouse = choice.title()
                return
            else:
                print("\nThat's not a valid choice!\n")
                time.sleep(3)
                self.chooseHouse("activeHouse")

    
    def responses(self):
        """This is called during step 3 of the turn.
        """
        choice = input("\nWhat would you like to do? (h for help):\n>>>").title()
        while True: # returns on EndTurn or Concede
            try:
                chosen = int(choice)
                # Checks card is viable play
                if self.activePlayer.hand[chosen].house == self.activeHouse and chosen < len(self.activePlayer.hand):
                    # Increases amber, adds the card to the action section of the board, then calls the card's play function
                    self.checkPlayStates() # self-explanatory?
                    self.activePlayer.amber += self.activePlayer.hand[chosen].amber
                    flank = 1
                    if self.activePlayer.hand[chosen].type == "Creature":
                        try:
                            flank = int(input("Choose left flank (0) or right flank (1, default):  "))
                        except:
                            pass
                    if self.activePlayer.hand[chosen].type != "Upgrade" and flank == 0:
                        self.activePlayer.board[self.activePlayer.hand[chosen].type].insert(0, self.activePlayer.hand.pop(chosen))
                    elif self.activePlayer.hand[chosen].type != "Upgrade":
                        self.activePlayer.board[self.activePlayer.hand[chosen].type].append(self.activePlayer.hand.pop(chosen))
                    else:
                        self.upgrade()
                    self.activePlayer.printShort(self.activePlayer.hand, False)
                else:
                    print("\nYou can only play cards from the active house.")
            except:
                pass
            if choice == 'h' or choice == 'H':
                print("Available info commands are 'House', 'Hand', 'Board', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'OppArchive', 'Keys', 'Amber', 'Card', 'MyDeck', 'OppDeck', and 'OppHand'. \nAvailable action commands are 'Play', 'Fight', 'Discard', 'Action', 'Reap', 'EndTurn', and 'Concede'.\n>>>")
                choice2 = input("Type a command here to learn more about it, or press enter to return:\n>>>").title()
                while choice2 != '':
                    if distance(choice2, "Hand") <= 1:
                        print("Lists the names of the cards in your hand.")
                    if distance(choice2, "House") <= 1:
                        print("Lists the active house.")
                    elif distance(choice2, "Board") <= 1:
                        print("Lists the creatures and artifacts on the board.")
                    elif distance(choice2, "MyDiscard") <= 1:
                        print("Lists the contents of your discard pile.")
                    elif distance(choice2, "OppDiscard") <= 1:
                        print("Lists the contents of your opponent's discard pile.")
                    elif distance(choice2, "MyPurge") <= 1:
                        print("Lists your purged cards.")
                    elif distance(choice2, "OppPurge") <= 1:
                        print("Lists your opponent's purged cards.")
                    elif distance(choice2, "MyArchive") <= 1:
                        print("Lists your archive.")
                    elif distance(choice2, "OppArchive") <= 1:
                        print("Returns the number of cards in your opponent's archive.")
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
                        print("Search for a card in one of the active decks by name.")
                    elif distance(choice2, "OppHand") <= 1:
                        print("Returns the number of cards in your opponent's hand.")
                    elif distance(choice2, "OppHand") <= 1:
                        print("Concede the game.")
                    elif distance(choice2, "Play") <= 1:
                        print("Play a card from hand.")
                    elif distance(choice2, "Fight") <= 1:
                        print("Choose a creature to fight with and a creature to fight against.")
                    elif distance(choice2, "Discard") <= 1:
                        print("Choose a card from hand to discard.")
                    elif distance(choice2, "Action") <= 1:
                        print("Choose a card with an action, and use that action.")
                    elif distance(choice2, "Reap") <= 1:
                        print("Choose a friendly creature to reap with.")
                    else:
                        print("That is not recognized as a command.")
                    break
                    # self.responses() # probably unnecessary line
            elif choice == "developer":
                developer()
            elif distance(choice, "Hand") <= 1:
                game.activePlayer.printShort(self.activePlayer.hand)
            elif distance(choice, "House") <= 1:
                print(self.activeHouse)
            elif distance(choice, "Board") <= 1:
                print(self)
            elif distance(choice, "MyDiscard") <= 1:
                self.activePlayer.printShort(self.activePlayer.discard, False)
            elif distance(choice, "OppDiscard") <= 1:
                self.inactivePlayer.printShort(self.inactivePlayer.discard, False)
            elif distance(choice, "MyPurge") <= 1:
                self.activePlayer.printShort(self.activePlayer.purges, False)
            elif distance(choice, "OppPurge") <= 1:
                self.inactivePlayer.printShort(self.inactivePlayer.discard, False)
            elif distance(choice, "MyArchive") <= 1:
                self.activePlayer.printShort(self.activePlayer.archive)
            elif distance(choice, "OppArchive") <= 1:
                print("There are " + str(len(self.inactivePlayer.archive) + " cards in your opponent's archive."))
            elif distance(choice, "Keys") <= 1 or distance(choice, "Amber") <= 1:
                print("You have", self.activePlayer.amber, "amber and", self.activePlayer.keys, "keys. Your opponent has", self.inactivePlayer.amber, "amber and", self.inactivePlayer.keys, "keys.\n")
            elif distance(choice, "Card") <= 1:
                cardName = input("Enter the name of a card from one of the active decks:\n>>>").title()
                for x in [deck.Deck(deck.deckName(self.first)), deck.Deck(deck.deckName(self.second))]:
                    for card in x.deck:
                        if cardName == card.title.title():
                            print(repr(card))
                            break
            elif distance(choice, "MyDeck") <= 1:
                print("Your deck has " + str(len(self.activePlayer.deck)) + " cards.")
            elif distance(choice, "OppDeck") <= 1:
                print("Your opponent's deck has " + str(len(self.inactivePlayer.deck)) + " cards.")
            elif distance(choice, "OppHand") <= 1:
                print("Your opponent's hand has " + str(len(self.inactivePlayer.hand)) + " cards.")
            elif distance(choice, "Fight") <= 1:
                # Shows board, then prompts to choose attacker and defender
                print(self)
                while True:
                    try:
                        attacker = int(input("Choose a minion to fight with: ")) - 1
                        str(self.activePlayer.board["Creature"][attacker].type)
                        break
                    except:
                        pass
                # self.checkFightStates(attacker) also checks before fight abilities, stuns, and exhaustion
                if self.checkFightStates(self.activePlayer.board["Creature"][attacker]):
                    while True:
                        try:
                            defender = int(input("Choose a minion to fight against: ")) - 1
                            str(self.inactivePlayer.board["Creature"][defender].type)
                            break
                        except:
                            pass
                else:
                    print("You cannot fight with that minion.")
                # Checks card is viable to fight or be fought (taunt)
                try:
                    defender > 0
                    if self.activePlayer.board["Creature"][attacker].house == self.activeHouse:
                        self.activePlayer.board["Creature"][attacker] * self.activePlayer.board["Creature"][defender]
                        self.activePlayer.board["Creature"][attacker].ready = False
                    else:
                        print("\nYou can only use cards from the active house.")
                except:
                    pass
            elif distance(choice, "Discard") <= 1:
                # Shows hand, then prompts to choose a card to discard.
                # Checks card is viable to discard
                pass
            elif distance(choice, "Action") <= 1:
                # Shows friendly cards with "Action" keyword, prompts a choice
                # Checks card is viable to use
                pass
            elif distance(choice, "Reap") <= 1:
                # Shows friendly board, prompts choice.
                # Checks viability
                pass
            elif distance(choice, "EndTurn") <= 1:
                print("Ending Turn!")
                return
            elif distance(choice, "Concede") <= 1:
                self.inactivePlayer.keys = 3
                return
            else:
                try:
                    int(choice)
                except:
                    print("Unrecognized command. Try again.\n")
            choice = input("\nWhat would you like to do? (h for help):\n>>>").title()

    def upgrade(self):
        """ A function for applying upgrades to minions.
        """

    def endGame(self):
        """ Declares a winner and ends the game.
        """
        print(self.activePlayer.name + " wins!\n")
    
###############################################


def distance(first, second):
    """Returns the edit distance between the strings first and second.
    """

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
    while True:
        try:
            deckChoice = int(input("Choose player 1's deck by index: "))
        except:
            deckChoice = -1
        if deckChoice - 1 < 0 or deckChoice > len(data):
            pass
        else:
            break
    # some code here to list player 2's options, which is all the decks except the one player 1 just chose
    print("Available decks:")
    with open('decks/deckList.json') as f:
        data = json.load(f)
        for x in range(0, len(data)):
            if x+1 != deckChoice:
                print(str(x+1) + ': ' + data[x]['name'])
    while True:
        try:
            deckChoice2 = int(input("Choose player 2's deck by index: "))
        except:
            deckChoice2 = -1
        if deckChoice2 - 1 < 0 or deckChoice2 > len(data) or deckChoice2 == deckChoice:
            pass
        else:
            break
    first = random.choice([deckChoice, deckChoice2])
    # print(first)
    if first == deckChoice:
        second = deckChoice2
    else:
        second = deckChoice
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


    