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

def startup(choice): #Called at startup
  """The initial starting of the game. Includes importing the decks (and possibly loading a saved game).
  """
  print(choice)
  print("Game is starting up!")
  if choice != "Newgame" and choice != "Import" and choice != "Decks" and choice != "Load":
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
      startup('')
      break

class Game():
  def __init__(self, first, second):
    """ first is first player, which is determined before Game is created and entered as an input. deck.deckName is a function that pulls the right deck from the list.
    """
    self.activeHouse = []
    self.first = first
    self.second = second
    print("\n" + deck.deckName(first) + " is going first.\n")
    time.sleep(1)
    self.activePlayer = deck.Deck(deck.deckName(first))
    self.inactivePlayer = deck.Deck(deck.deckName(second))
    self.endBool = True
    self.creaturesPlayed = 0
    self.extraFightHouses = []
    self.forgedLastTurn = False, 0

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

##################
# Turn functions #
##################

  def startGame(self): #called by choosedecks()
    """Fills hands, allows for mulligans and redraws, then plays the first turn, because that turn follows special rules.
    """
    self.activePlayer += 36 #self.activePlayer += 7
    print("\n" + self.activePlayer.name + "'s hand:")
    self.activePlayer.printShort(self.activePlayer.hand)
    mull = input("Player 1, would you like to mulligan? \n>>>")
    if mull == "Yes" or mull == "Y" or mull == "y":
      for card in self.activePlayer.hand:
        self.activePlayer.deck.append(card)
      random.shuffle(self.activePlayer.deck)
      self.activePlayer.hand = []
      self.activePlayer += 6
    # for card in self.activePlayer.hand:
    #   print(card)
    self.inactivePlayer += 36 # self.inactivePlayer += 6
    print("\n" + self.inactivePlayer.name + "'s hand:")
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
        if self.checkForgeStates(): # maybe this function will determine key cost
          if self.activePlayer.amber >= self.activePlayer.keyCost:
            self.activePlayer.amber -= self.activePlayer.keyCost
            self.activePlayer.keys += 1
            print("You forged a key for", self.activePlayer.keyCost, "amber. You now have", self.activePlayer.keys, "key(s) and", self.activePlayer.amber, "amber.\n") # it works!
            if game.activePlayer.states["Forge"]["Interdimensional Graft"] and game.activePlayer.amber > 0:
              print("Your opponent played Interdimensional Graft last turn, so they gain your " + str(game.activePlayer.amber) + " leftover amber.")
              play.stealAmber(game.inactivePlayer, game.activePlayer, game.activePlayer.amber)
              print("They now have " + game.inactivePlayer.amber + " amber.")
            forgedThisTurn = True, num
        else:
          print("Forging skipped this turn!")
        if self.activePlayer.keys >= 3:
          break
      # step 2: the player chooses a house
      # outsourced b/c multipurpose
      if self.inactivePlayer.states["House"]["Control the Weak"] in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
        self.activeHouse = self.inactivePlayer.states["House"]["Control the Weak"]
      else: self.chooseHouse("activeHouse")
      # step 3: call responses
      # outsourced b/c long
      self.responses(num)
      # step 4: ready cards and reset things like armor
      # here b/c short
      self.reset(num, forgedThisTurn)
      # step 5.1: draw cards
      self.activePlayer.drawEOT()
      # print("Checking draw:", self.activePlayer.handSize == len(self.activePlayer.hand)) # test line
      # step 5.2: check for EOT effects
      self.checkEOTStates()
      self.resetEOTStates()
      # step 5.3: switch players
      self.switch()
      # step 5.4: increment num
      num += 1
      self.numPlays = 100
    self.endGame(self.endBool)

  def switch(self):
    """ Swaps active and inactive players.
    """
    self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer
    # print(self) # test line: passed on 7/25

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
        developer(self)
      elif distance(choice, "Turn") <= 1:
        print("Turn: " + str(turn))
      elif distance(choice, "Hand") <= 1:
        game.activePlayer.printShort(self.activePlayer.hand)
      elif distance(choice, "House") <= 1:
        [print(x) for x in self.activeHouse]
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
        disc = makeChoice("Choose a card to discard: ", self.activePlayer.hand)
        if self.activePlayer.hand[disc].house == self.activeHouse[0]:
          self.activePlayer.discard.append(self.activePlayer.hand.pop(disc))
          if "Rock-Hurling Giant" in [x.title for x in self.activePlayer.board["Creature"]] and self.activePlayer.discard[-1].house == "Brobnar":
            side = play.chooseSide(self)
            if side == 0:
              self.activePlayer.printShort(self.activePlayer.board["Creature"])
              target = makeChoice("Choose a creature to target: ", self.activePlayer.board["Creature"])
              self.activePlayer.board["Creature"][target].damageCalc(4)
              if self.activePlayer.board["Creature"][target].update():
                self.activePlayer.discard.append(self.activePlayer.board["Creature"].pop(target))
            else:
              self.activePlayer.printShort(self.inactivePlayer.board["Creature"])
              target = makeChoice("Choose a creature to target: ", self.inactivePlayer.board["Creature"])
              self.inactivePlayer.board["Creature"][target].damageCalc(4)
              if self.inactivePlayer.board["Creature"][target].update():
                self.inactivePlayer.discard.append(self.inactivePlayer.board["Creature"].pop(target))
          if turn == 1:
            self.numPlays -= 1
      elif distance(choice, "Action") <= 1:
        # Shows friendly cards in play with "Action" keyword, prompts a choice
        actList = []
        [(actList.append(self.activePlayer.board["Creature"][x])) for x in range(len(self.activePlayer.board["Creature"])) if self.activePlayer.board["Creature"][x].action == True or self.activePlayer.board["Creature"][x].omni == True]
        [(actList.append(self.activePlayer.board["Artifact"][x])) for x in range(len(self.activePlayer.board["Artifact"])) if self.activePlayer.board["Artifact"][x].action == True or self.activePlayer.board["Artifact"][x].omni == True]
        [print(str(x) + ": " + str(actList[x])) for x in range(len(actList))]
        act = makeChoice("Choose an artifact or minion to use: ", actList)
        if actList[act].ready and actList[act].house in self.activeHouse:
          # Trigger action
          # but remember stunned creatures
          print("Doing this thing's action.")
          break
        else:
          print("You cannot use that action right now.")
          break
      elif distance(choice, "Reap") <= 1:
        # Shows friendly board, prompts choice.
        # Checks viability
        [print(str(x) + ": " + str(self.activePlayer.board["Creature"][x])) for x in range(len(self.activePlayer.board["Creature"]))]
        reapList = self.activePlayer.board["Creature"]
        self.activePlayer.printShort(reapList)
        reaper = makeChoice("Choose a creature to reap with: ", reapList)
        if reapList[reaper].ready and reapList[reaper].house in self.activeHouse:
          print("Doing this thing's reap.") # test line
          self.reapCard(reaper)
          break
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

  def chooseHouse(self, varAsStr, num = 1):
    """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards like control the weak. Num is used for cards that allow extra houses to fight or be used.
    """
    if varAsStr == "activeHouse":
      print("\nYour hand is:\n")
      self.activePlayer.printShort(self.activePlayer.hand)
      while True:
        choice = input("Choose a house. Your deck's houses are " + self.activePlayer.houses[0] + ", " + self.activePlayer.houses[1] + ", " + self.activePlayer.houses[2] + ".\n>>>").title()
        if choice in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
          if "Restringuntus" in [x.title for x in game.inactivePlayer.board["Creature"]]:
            self.activeHouse = self.activePlayer.restring # I was able to verify that there will never be more than one copy of Restringuntus in a deck
          else:
            self.activeHouse = choice
          return
        else:
          print("\nThat's not a valid choice!\n")
          time.sleep(1)
    elif varAsStr == "extraFight": #for brothers in battle, and probably others
      print("\nYour board:\n")
      self.activePlayer.printShort(self.activePlayer.board["Creature"], False)
      if num == 1:
        while True:
          extra = input("Choose another house to fight with:\n>>>").title()
          if extra in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"] and extra != self.activeHouse:
            self.extraFightHouses.append(extra)
            break
          elif extra == self.activeHouse:
            print("\nThat's already your active house. Try again.\n")
          else:
            print("\nNot a valid input.\n")
    elif varAsStr == "Restringuntus":
      while True:
        extra = input("Choose another house to fight with:\n>>>").title()
        if extra in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
          self.inactivePlayer.restring = extra
          break
        else:
          print("\nNot a valid input.\n")  
  
  def reset(self, num, forgedThisTurn):
    """ Resets all things that need to be reset at EOT, like some states, armor, elusive, ready
    """
    for creature in self.activePlayer.board["Creature"]:
      creature.ready = True
      creature.armor = creature.base_armor
      if "Elusive" in creature.text:
        creature.elusive = True
    for artifact in self.activePlayer.board["Artifact"]:
      artifact.ready = True
    if forgedThisTurn[1] == num:
      self.forgedLastTurn = forgedThisTurn
    else:
      self.forgedLastTurn = False, num

  def endGame(self, booly):
    """ Ends the game, with a winner if someone has three keys.
    """
    if self.activePlayer.keys >= 3:
      print(self.activePlayer.name + " wins!\n")
    elif self.inactivePlayer.keys >= 3:
      print(self.inactivePlayer.name + " wins!\n")
    else:
      print("Game ended.")

############################
# State Checking Functions #
############################

  def checkActionStates(self):
    """ Checks for things that affect actions.
    """
    if self.activePlayer.states["Action"]["Skippy Timehog"]:
      print("Your opponent played Skippy Timehog last turn, so you can't use your action.")
      return False

  def checkEOTStates(self):
    """ Checks for end of turn effects. There aren't more than a couple in CotA.
    """

  def checkFightStates(self, attacker = None):
    """ Checks for fight states (warsong, etc) or before fight effects, or stun or exhaust.
    """
    # if we're here, we've already checked that there are enemy minions to attack
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    pendingDiscardA = []
    pendingDiscardI = []
    if attacker.stun == True:
      attacker.stun = False
      attacker.ready = False
      print("About to return False") # test line
      return False
    if attacker.ready == False:
      print("About to return False") # test line
      return False
    if self.activePlayer.states["Fight"]["Foggify"]:
      print("Your opponent played Foggify last turn, so you cannot fight.")
      return False
    if self.activePlayer.states["Fight"]["Skippy Timehog"]:
      print("Your opponent played Skippy Timehog last turn, so you cannot fight.")
      return False
    if "Before fight:" in attacker.text or "Before Fight:" in attacker.text:
      # before fight effects here:

      # will need to check for deaths *after* before fight, but still before the fight
      [pendingDiscardA.append(active.pop(abs(x - len(active) + 1))) for x in range(len(active)) if active[abs(x - len(active) + 1)].update()]
      [pendingDiscardI.append(inactive.pop(abs(x - len(inactive) + 1))) for x in range(len(inactive)) if inactive[abs(x - len(inactive) + 1)].update()]
      play.pending(self, pendingDiscardA, self.activePlayer.discard)
      play.pending(self, pendingDiscardI, self.inactivePlayer.discard)
      if self.activePlayer.states["Fight"]["Warsong"][0]:
        self.activePlayer.amber += len(self.activePlayer.states["Fight"]["Warsong"])
      if len(self.inactivePlayer.board["Creature"]) == 0:
        print("Your opponent no longer has any creatures to attack. Your creature is still exhausted.")
      print("About to return True") # test line
      return True
    try:
      if self.activePlayer.states["Fight"]["Warsong"]:
        self.activePlayer.amber += 1
    except:
      pass
    print("About to return True") # test line
    return True

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

  def checkPlayStates(self, card):
    """ Checks for play states (full moon, etc.). By the time this is called, I already know if house matches.
    """
    # lifeward and other things that might return False first
    if self.activePlayer.states["Play"]["Scrambler Storm"]:
      if card.type == "Action":
        print("Your opponent played Scrambler Storm last turn, so you cannot play actions this turn.")
        return False
    if card.title == "Truebaru":
      if self.activePlayer.amber < 3:
        print("You must have 3 amber to sacrifice in order to play Truebaru.")
        return False
      self.activePlayer.amber -= 3
    if "Grommid" in [x.title for x in self.activePlayer.board["Creature"]] and card.type == "Creature":
      print("You can't play creatures with Grommid in play.")
      return False

    
    # other play effects - things that don't want returns
    if self.activePlayer.states["Play"]["Library Access"]:
      self.activePlayer += 1
      print("You draw a card because you played Library Access earlier this turn.")
    if self.activePlayer.states["Play"]["Soft Landing"]:
      card.ready = True
      print(card.title + " enters play ready!")
      self.activePlayer.states["Play"]["Soft Landing"]
    if card.house == "Mars" and card.type == "Creature" and "Tunk" in [x.title for x in game.activePlayer.board["Creature"]]:
      location = [game.activePlayer.board["Creature"].index(x) for x in game.activePlayer.board["Creature"] if x.title == "Tunk"]
      for x in location:
        game.activePlayer.board["Creature"][x].damage = 0
    



    # only return True at the very end
    return True

  def checkReapStates(self):
    """ Checks for things that disallow reaping.
    """
    if self.activePlayer.states["Reap"]["Skippy Timehog"]:
      print("Your opponent played Skippy Timehog last turn, so you cannot reap.")
      return False

##################
# Card functions #
##################

  def actionCard(self):
    """ Trigger a card's action.
    """
  
  def fightCard(self, attacker = 100):
    """ This is needed for cards that trigger fights (eg anger, gauntlet of command). If attacker is fed in to the function (which will only be done by cards that trigger fights), the house check is skipped.
    """
    # Shows board, then prompts to choose attacker and defender
    print(self)
    if len(self.inactivePlayer.board["Creature"]) == 0:
      print("Your opponent has no creatures for you to attack. Fight canceled.")
      return self, None
    while True:
      if attacker > 28:
        try:
          attacker = int(input("Choose a minion to fight with: "))
          # next line basically checks if they've listed a valid option
          if self.activePlayer.board["Creature"][attacker].house not in self.activeHouse:
            if len(self.extraFightHouses) > 0:
              if self.activePlayer.board["Creature"][attacker].house not in self.extraFightHouses:
                print("\nYou can only use cards from the active house or extra declared houses.")
                return self, None
            else:
              print("\nYou can only use cards from the active house.")
              return self, None
          # next line will fail if answer is OOB
          str(self.activePlayer.board["Creature"][attacker].type)
          break
        except:
          print("Your entry was invalid. Try again.")
      else:
        break
    # self.checkFightStates(attacker) also checks before fight abilities, stuns, and exhaustion/ready
    if self.checkFightStates(self.activePlayer.board["Creature"][attacker]):
      defender = makeChoice("Choose a minion to fight against: ", self.inactivePlayer.board["Creature"])
    else:
      print("You cannot fight with that minion.")
    # Checks card is viable to fight or be fought (taunt)
    try:
      print("Trying to fight.")
      self.activePlayer.board["Creature"][attacker].fightCard(self.inactivePlayer.board["Creature"][defender])
    except: print("Fight failed.")
    pendingDiscard = []
    if self.activePlayer.board["Creature"][attacker].update():
      pendingDiscard.append(self.activePlayer.board["Creature"][attacker])
      died = True
    else:
      died = False
    play.pending(self, pendingDiscard, self.activePlayer.discard)
    if self.inactivePlayer.board["Creature"][defender].update():
      pendingDiscard.append(self.inactivePlayer.board["Creature"][defender])
    play.pending(self, pendingDiscard, self.inactivePlayer.discard())

  def playCard(self, chosen, booly = True):
    """ This is needed for cards that play other cards (eg wild wormhole). Will also simplify responses. Booly is a boolean that tells whether or not to check if the house matches.
    """
    print(self.numPlays)
    if booly and self.numPlays > 0:
      # print("playCard area 1") # test line
      if (self.activePlayer.hand[chosen].house in self.activeHouse or self.activePlayer.states["Play"]["Phase Shift"][0]) and chosen < len(self.activePlayer.hand):
        # print("playCard area 1.1") # test line
        if self.activePlayer.states["Play"]["Phase Shift"] and self.activePlayer.hand[chosen].house != "Logos":
          # then reset Phase Shift. And if the card being played is a mavericked phase shift, phase shift will be set to true again in a second
          if len(self.activePlayer.states["Play"]["Phase Shift"]) > 1:
            # remove last item
            self.activePlayer.states["Play"]["Phase Shift"].pop()
          else: self.activePlayer.states["Play"]["Phase Shift"] = [False] # reset to false
        # Increases amber, adds the card to the action section of the board, then calls the card's play function
        if not self.checkPlayStates(self.activePlayer.hand[chosen]):
          return # checkPlayStates will print the reason
        self.activePlayer.amber += self.activePlayer.hand[chosen].amber
        flank = 1
        print(self.activePlayer.hand[chosen].title + " gave you " + self.activePlayer.hand[chosen].amber + " amber. You now have " + self.activePlayer.amber + " amber.")
        cardType = self.activePlayer.hand[chosen].type
        if self.activePlayer.hand[chosen].type == "Creature" and len(self.activePlayer.board["Creature"]) > 0:
          # print("playCard area 1.3") # test line
          try:
            flank = int(input("Choose left flank [0] or right flank [1, default]:  "))
            self.creaturesPlayed += 1
          except:
            pass
        # left flank
        if self.activePlayer.hand[chosen].type != "Upgrade" and flank == 0:
          # save the cardType so I can use it after I've removed the card from the hand
          # print("playCard area 1.4") # test line
          self.activePlayer.board[cardType].insert(0, self.activePlayer.hand.pop(chosen))
          # set a variable with the index of the card in board
          location = self.activePlayer.board[cardType][0]
          self.numPlays -= 1
          print(self.numPlays) # test line
        # default case: right flank
        elif self.activePlayer.hand[chosen].type != "Upgrade":
          # print("playCard area 1.5") # test line
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
        print(location.text)
        try: location.play(self, location)
        except:
          print("this card's play action failed.")
          pass
        # if the card is an action, now add it to the discard pile
        if cardType == "Action":
          self.activePlayer.discard.append(self.activePlayer.board["Action"].pop())
        self.activePlayer.printShort(self.activePlayer.hand, False)
      else:
        print("\nYou can only play cards from the active house.")
    else:
      print("playCard area 2") # test line
      if "Wild Wormhole" in [x.title for x in self.activePlayer.board["Action"]]:
        print("playCard area 2.1") # test line
        # Increases amber, adds the card to the action section of the board, then calls the card's play function
        if not self.checkPlayStates():
          return # checkPlayStates will explain why
        self.activePlayer.amber += self.activePlayer.deck[-1].amber
        flank = 1
        cardType = self.activePlayer.deck[-1].type
        if cardType == "Creature":
          print("playCard area 2.2") # test line
          try:
            flank = int(input("Choose left flank [0] or right flank [1, default]:  "))
            self.creaturesPlayed += 1
          except:
            pass
        # left flank
        if cardType != "Upgrade" and flank == 0:
          print("playCard area 2.3") # test line
          self.activePlayer.board[cardType].insert(0, self.activePlayer.deck.pop())
          location = self.activePlayer.board[cardType][0]
          self.numPlays -= 1
        # default case: right flank
        elif cardType != "Upgrade":
          print("playCard area 2.4") # test line
          self.activePlayer.board[cardType].append(self.activePlayer.deck.pop())
          location = self.activePlayer.board[cardType][len(self.activePlayer.board[cardType])]
          self.numPlays -= 1
        else:
          print("playCard area 2.5") # test line
          self.upgrade()
        #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
        try: location.play(self, location)
        except:
          print("This card's play action failed.")
          pass
        # if the card is an action, now add it to the discard pile
        if cardType == "Action":
          self.activePlayer.discard.append(self.activePlayer.board["Action"].pop())

  def playUpgrade(self, target):
    """ Plays an upgrade on a creature.
    """

  def reapCard(self):
    """ Triggers a card's reap effect.
    """
  
                #####################
                # End of Game Class #
                #####################

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

def developer(game):
  """Developer functions for manually changing the game state.
  """

def chooseDecks(): #called by startup()
  """The players choose their decks from deckDict, and if their choice isn't there they are offered the option to import a deck.
  """
  print("Available decks:")
  with open('decks/deckList.json') as f:
    data = json.load(f)
    for x in range(0, len(data)):
      print(str(x) + ': ' + data[x]['name'])
  deckChoice = makeChoice("Choose player 1's deck by index: ", data)
  # some code here to list player 2's options, which is all the decks except the one player 1 just chose
  print("Available decks:")
  with open('decks/deckList.json') as f:
    data = json.load(f)
    for x in range(0, len(data)):
      if x+1 != deckChoice:
        print(str(x) + ': ' + data[x]['name'])
  deckChoice2 = makeChoice("Choose player 2's deck by index: ", data)
  first = random.choice([deckChoice, deckChoice2])
  # print(first)
  if first == deckChoice:
    second = deckChoice2
  else:
    second = deckChoice
  global game
  game = Game(first, second)
  game.startGame()

def makeChoice(stringy, L = []):
  """ Takes a string explaining the choice and a list, only accepts results within the length of the list.
  """
  while True:
    try:
      choice = int(input(stringy))
      if 0 <= choice < len(L):
        return choice
      else:
        raise IndexError
    except:
      pass

def load(saveFile):
  """Loads a saved game.
  """



  