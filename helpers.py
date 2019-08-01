import decks.decks as deck
import cards.cardsAsClass as card
import cards.destroyed as dest
import cards.actions as action
import cards.play as play
import cards.reap as reap
import cards.fight as fight
import json
import random
import time

##################
# Contains modules:
# Game class
# 
##################

class Game():
    def __init__(self, first, second):
        """ first is first player, which is determined before Game is created and entered as an input. deck.deckName is a function that pulls the right deck from the list.
        """
        self.activeHouse = []
        self.first = first - 1
        self.second = second - 1
        print("\n" + deck.deckName(first - 1) + " is going first.\n")
        time.sleep(1)
        self.activePlayer = deck.Deck(deck.deckName(first - 1))
        self.inactivePlayer = deck.Deck(deck.deckName(second - 1))
        self.endBool = True
        self.creaturesPlayed = 0

    def __repr__(self):
        s = ''
        s += "\nOpponent's board:\nCreatures:\n"
        for x in range(len(self.inactivePlayer.board["Creature"])):
            s += str(x) + ': ' + str(self.inactivePlayer.board["Creature"][x]) + '\n'
        s += "Artifacts: \n"
        for x in range(len(self.inactivePlayer.board["Artifact"])):
            s += str(x) + ': ' + str(self.inactivePlayer.board["Artifact"][x]) + '\n'
        s += "\nYour board:\nCreatures:\n"
        for x in range(len(self.activePlayer.board["Creature"])):
            # print(x) #test line
            s += str(x) + ': ' + str(self.activePlayer.board["Creature"][x]) + "\n"
        s += "Artifacts: \n"
        for x in range(len(self.activePlayer.board["Artifact"])):
            s += str(x) + ': ' + str(self.activePlayer.board["Artifact"][x]) + '\n'
        return s

    def switch(self):
        """ Swaps active and inactive players.
        """
        self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer
        # print(self) # test line: passed on 7/25

    def startGame(self): #called by choosedecks()
        """Fills hands, allows for mulligans and redraws, then plays the first turn, because that turn follows special rules.
        """
        self.activePlayer += 36 #self.activePlayer += 7
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
        self.inactivePlayer += 36 # self.inactivePlayer += 6
        print("\nPlayer 2's hand:")
        self.inactivePlayer.printShort(self.inactivePlayer.hand)
        mull2 = input("Player 2, would you like to mulligan? \n>>>")
        if mull2 == "Yes" or mull2 == "Y" or mull2 == "y":
            for card in self.inactivePlayer.hand:
                self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
        self.numPlays = 1
        self.turn(1)
        # From here on should be in turn(), I think

    def turn(self, num):
        """ The passive actions of a turn. 1: Forge key (if poss, and if miasma hasn't changed the state; also reset state); 2: Calls chooseHouse(); 3: calls responses(), which needs to be moved into this class, and represents all actions (playing, discarding, fighting, etc) and info seeking; 4: ready cards; 5: draw cards. num is the turn number.
        """
        while True:
            if not self.endBool:
                break
            self.lastCreaturesPlayed = self.creaturesPlayed
            self.creaturesPlayed = 0
            print("\nTurn: " + str(num))
            if num > 1:
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
            if num == 1:
                self.responses(num)
            else:
                self.responses(num)
            # step 4: ready cards and reset armor
            # here b/c short
            for creature in self.activePlayer.board["Creature"]:
                creature.ready = True
                creature.armor = creature.base_armor
                if "Elusive" in creature.text:
                    creature.elusive = True
            for artifact in self.activePlayer.board["Artifact"]:
                artifact.ready = True
            # step 5.1: draw cards
            self.activePlayer.drawEOT()
            # print("Checking draw:", self.activePlayer.handSize == len(self.activePlayer.hand)) # test line
            # step 5.2: check for EOT effects
            self.checkEOTStates()
            # step 5.3: switch players
            self.switch()
            # step 5.4: increment num
            num += 1
            self.numPlays = 100
        self.endGame(self.endBool)

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
            attacker.stun = False
            attacker.ready = False
            print("About to return False") # test line
            return False
        if attacker.ready == False:
            print("About to return False") # test line
            return False
        if "Before fight:" in attacker.text or "Before Fight:" in attacker.text:
            # before fight effects here:

            # will need to check for deaths *after* before fight, but still before the fight
            [x.update(self) for x in self.activePlayer.board["Creature"]]
            [x.update(self) for x in self.inactivePlayer.board["Creature"]]
            print("About to return True") # test line
            return True
        print("About to return True") # test line
        return True

    def chooseHouse(self, varAsStr):
        """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards like control the weak.
        """
        if varAsStr == "activeHouse":
            print("Your hand is: ")
            self.activePlayer.printShort(self.activePlayer.hand)
            choice = input("Choose a house. Your deck's houses are " + self.activePlayer.houses[0] + ", " + self.activePlayer.houses[1] + ", " + self.activePlayer.houses[2] + ".\n>>>").title()
            if choice in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
                self.activeHouse.append(choice.title())
                return
            else:
                print("\nThat's not a valid choice!\n")
                time.sleep(1)
                self.chooseHouse("activeHouse")

    def fightCard(self, attacker = 100):
        """ This is needed for cards that trigger fights (eg anger, gauntlet of command). If attacker is fed in to the function (which will only be done by cards that trigger fights), the house check is skipped.
        """
        # Shows board, then prompts to choose attacker and defender
        print(self)
        if len(self.inactivePlayer.board["Creature"]) == 0:
            print("Your opponent has no creatures for you to attack. Fight canceled.")
            return
        while True:
            if attacker > 36:
                try:
                    attacker = int(input("Choose a minion to fight with: "))
                    # next line basically checks if they've listed a valid option
                    if self.activePlayer.board["Creature"][attacker].house not in self.activeHouse:
                        print("\nYou can only use cards from the active house.")
                    # next line will fail if answer is OOB
                    str(self.activePlayer.board["Creature"][attacker].type)
                    break
                except:
                    print("Your entry was invalid. Try again.")
            else:
                break
        # self.checkFightStates(attacker) also checks before fight abilities, stuns, and exhaustion
        if self.checkFightStates(self.activePlayer.board["Creature"][attacker]):
            while True:
                try:
                    defender = int(input("Choose a minion to fight against: "))
                    # this will fail if the input is OOB
                    str(self.inactivePlayer.board["Creature"][defender].type)
                    break
                except:
                    pass
        else:
            print("You cannot fight with that minion.")
        # Checks card is viable to fight or be fought (taunt)
        try:
            print("Trying to fight.")
            self.activePlayer.board["Creature"][attacker].fightCard(self.inactivePlayer.board["Creature"][defender])
        except:
            print("Fight failed.")
            pass

    def playCard(self, chosen, booly = True):
        """ This is needed for cards that play other cards (eg wild wormhole). Will also simplify responses. Booly is a boolean that tells whether or not to check if the house matches.
        """
        print(self.numPlays)
        if booly and self.numPlays > 0:
            print("playCard area 1") # test line
            if self.activePlayer.hand[chosen].house in self.activeHouse and chosen < len(self.activePlayer.hand):
                print("playCard area 1.1") # test line
                # Increases amber, adds the card to the action section of the board, then calls the card's play function
                self.checkPlayStates() # self-explanatory?
                self.activePlayer.amber += self.activePlayer.hand[chosen].amber
                flank = 1
                cardType = self.activePlayer.hand[chosen].type
                if self.activePlayer.hand[chosen].type == "Creature" and len(self.activePlayer.board["Creature"]) > 0:
                    print("playCard area 1.3") # test line
                    try:
                        flank = int(input("Choose left flank (0) or right flank (1, default):  "))
                        self.creaturesPlayed += 1
                    except:
                        pass
                # left flank
                if self.activePlayer.hand[chosen].type != "Upgrade" and flank == 0:
                    # save the cardType so I can use it after I've removed the card from the hand
                    print("playCard area 1.4") # test line
                    self.activePlayer.board[cardType].insert(0, self.activePlayer.hand.pop(chosen))
                    # set a variable with the index of the card in board
                    location = self.activePlayer.board[cardType][0]
                    self.numPlays -= 1
                    print(self.numPlays)
                # default case: right flank
                elif self.activePlayer.hand[chosen].type != "Upgrade":
                    print("playCard area 1.5") # test line
                    print(cardType)
                    self.activePlayer.board[cardType].append(self.activePlayer.hand.pop(chosen))
                    # set a variable with the index of the card in board
                    location = self.activePlayer.board[cardType][len(self.activePlayer.board[cardType]) - 1]
                    self.numPlays -= 1
                    print(self.numPlays)
                    print([x.title for x in self.activePlayer.board["Action"]])
                else:
                    print("playCard area 1.6") # test line
                    self.upgrade()
                #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
                try:
                    if location.play:
                        print("This card has an on play effect.") # test line
                        # find the appropriate play function. how?
                        funcString = "play.key" + location.number
                        print(funcString) # test line
                        playFunc = eval(funcString)
                        print(playFunc) # test line
                        playFunc(self)
                except:
                    print("playFunc failed.")
                    pass
                # if the card is an action, now add it to the discard pile
                if cardType == "Action":
                    self.activePlayer.discard.append(self.activePlayer.board["Action"].pop())
                self.activePlayer.printShort(self.activePlayer.hand, False)
            else:
                print("\nYou can only play cards from the active house.")
        else:
            print("playCard area 2") # test line
            if (chosen < len(self.activePlayer.hand) and self.numPlays > 0) or "Wild Wormhole" in [x.title for x in self.activePlayer.board["Action"]]:
                print("playCard area 2.1") # test line
                # Increases amber, adds the card to the action section of the board, then calls the card's play function
                self.checkPlayStates() # self-explanatory?
                self.activePlayer.amber += self.activePlayer.hand[chosen].amber
                flank = 1
                if self.activePlayer.hand[chosen].type == "Creature":
                    print("playCard area 2.2") # test line
                    try:
                        flank = int(input("Choose left flank (0) or right flank (1, default):  "))
                        self.creaturesPlayed += 1
                    except:
                        pass
                # left flank
                if self.activePlayer.hand[chosen].type != "Upgrade" and flank == 0:
                    print("playCard area 2.3") # test line
                    self.activePlayer.board[self.activePlayer.hand[chosen].type].insert(0, self.activePlayer.hand.pop(chosen))
                    self.numPlays -= 1
                # default case: right flank
                elif self.activePlayer.hand[chosen].type != "Upgrade":
                    print("playCard area 2.4") # test line
                    self.activePlayer.board[self.activePlayer.hand[chosen].type].append(self.activePlayer.hand.pop(chosen))
                    self.numPlays -= 1
                else:
                    print("playCard area 2.5") # test line
                    self.upgrade()
                self.activePlayer.printShort(self.activePlayer.hand, False)
            elif self.numPlays == 0:
                print("You can only do one play or discard on turn one.")
        return



    def responses(self, turn):
        """This is called during step 3 of the turn. Turn is so that players can ask what turn it is.
        """
        choice = input("\nWhat would you like to do? (h for help):\n>>>").title()
        while True: # returns on EndTurn or Concede, or after one play on turn one
            try:
                chosen = int(choice)
                # if the above works, they are trying to play a card, then we check for first turn
                try:
                    self.playCard(chosen)
                except:
                    print("playCard failed.")
                # print("Got past playCard()") # Test line
            except:
                pass
            if choice == 'h' or choice == 'H':
                print("Enter a number to play that card. Available info commands are 'House', 'Hand', 'Board', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'OppArchive', 'Keys', 'Amber', 'Card', 'MyDeck', 'OppDeck', and 'OppHand'. \nAvailable action commands are 'Turn', 'Fight', 'Discard', 'Action', 'Reap', 'EndTurn', and 'Concede'.\n>>>")
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
            elif distance(choice, "Turn") <= 1:
                print("Turn: " + str(turn))
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
                # hands off the info to the "Fight" function
                self.fightCard()
            elif distance(choice, "Discard") <= 1:
                if self.numPlays == 0:
                    break
                self.activePlayer.printShort(self.activePlayer.hand)
                while True:
                    try:
                        disc = input("Choose a card to discard: ")
                        if disc == '':
                            disc = False
                            break
                        disc = int(disc)
                        if 0 <= disc < len(self.activePlayer.hand):
                            break
                    except:
                        pass
                if disc:
                    if self.activePlayer.hand[disc].house == self.activeHouse[0]:
                        self.activePlayer.discard.append(self.activePlayer.hand.pop(disc))
                        self.numPlays -= 1
            elif distance(choice, "Action") <= 1:
                # Shows friendly cards in play with "Action" keyword, prompts a choice
                actList = []
                [(actList.append(self.activePlayer.board["Creature"][x])) for x in range(len(self.activePlayer.board["Creature"])) if self.activePlayer.board["Creature"][x].action == True or self.activePlayer.board["Creature"][x].omni == True]
                [(actList.append(self.activePlayer.board["Artifact"][x])) for x in range(len(self.activePlayer.board["Artifact"])) if self.activePlayer.board["Artifact"][x].action == True or self.activePlayer.board["Artifact"][x].omni == True]
                [print(str(x) + ": " + str(actList[x])) for x in range(len(actList))]
                while True:
                    try:
                        if len(actList) > 0:
                            act = int(input("Choose an artifact or minion to use: "))
                        # Checks card is viable to use
                        if actList[act].ready and actList[act].ready and actList[act].house == self.activeHouse[0]:
                            # Trigger action
                            print("Doing this thing's action.")
                            break
                        else:
                            print("You cannot use that action right now.")
                            break
                    except:
                        pass
            elif distance(choice, "Reap") <= 1:
                # Shows friendly board, prompts choice.
                # Checks viability
                [print(str(x) + ": " + str(self.activePlayer.board["Creature"][x])) for x in range(len(self.activePlayer.board["Creature"]))]
                while True:
                    try:
                        act = int(input("Choose an artifact or minion to use: "))
                        if actList[act].ready and actList[act].ready and actList[act].house == self.activeHouse[0]:
                            # Trigger reap
                            print("Doing this thing's reap.")
                            break
                    except:
                        pass
            elif distance(choice, "EndTurn") <= 1:
                print("\nEnding Turn!")
                return
            elif distance(choice, "Concede") <= 1:
                self.inactivePlayer.keys = 3
                return
            elif distance(choice, "Quit") <= 1:
                self.endBool = False
            else:
                try:
                    int(choice)
                except:
                    print("Unrecognized command. Try again.\n")
            if not self.endBool:
                break
            choice = input("\nWhat would you like to do? (h for help):\n>>>").title()

    def upgrade(self):
        """ A function for applying upgrades to minions.
        """

    def endGame(self, booly):
        """ Ends the game, with a winner if booly is true, or just ends it otherwise.
        """
        if booly:
            print(self.activePlayer.name + " wins!\n")
        else:
            print("Game ended.")
    
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


    