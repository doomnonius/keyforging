from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
import decks.decks as deck
import cards.cardsAsClass as card
import cards.destroyed as dest
import cards.actions as action
import cards.play as play
import cards.reap as reap
import cards.fight as fight
import json, random, logging, time, pygame, pyautogui
from helpers import makeChoice, distance, buildStateDict
from typing import Dict, List, Set
from constants import COLORS, WIDTH, HEIGHT, CARDH

#####################
# Contains modules: #
# - Game class      #
#####################

class Board():
  def __init__(self):
    """ first is first player, which is determined before Game is created and entered as an input. deck.deckName is a function that pulls the right deck from the list.
    """
    self.first = None
    self.second = None
    self.top = 0
    self.left = 0
    self.xmouse = 0
    self.ymouse = 0
    self.activeHouse = []
    self.endBool = True
    self.turnNum = 0
    self.creaturesPlayed = 0
    self.extraFightHouses = []
    self.forgedLastTurn = False, 0
    # self.allRects = []
    self.backgroundColor = COLORS["WHITE"]
    # sprites
    self.allsprites = pygame.sprite.RenderUpdates()
    # hands
    self.activeHand = pygame.sprite.Group()
    self.inactiveHand = pygame.sprite.Group()
    # creatures
    self.activeCreatures = pygame.sprite.Group()
    self.inactiveCreatures = pygame.sprite.Group()
    # artifacts
    self.activeArtifacts = pygame.sprite.Group()
    self.inactiveArtifacts = pygame.sprite.Group()
    # deck
    self.activeDeck = pygame.sprite.Group()
    self.inactiveDeck = pygame.sprite.Group()
    # discard
    self.activeDiscard = pygame.sprite.Group()
    self.inactiveDiscard = pygame.sprite.Group()
    # purged
    self.activePurged = pygame.sprite.Group()
    self.inactivePurged = pygame.sprite.Group()
    # start pygame
    pygame.init()
    pygame.font.init()
    self.BASICFONT = pygame.font.SysFont("Corbel", 20)
    self.FPS = 60
    self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))#, flags = pygame.FULLSCREEN)
    pygame.display.set_caption('Keyforge')
    self.CLOCK = pygame.time.Clock()
    self.main()

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
      s += str(x) + ': ' + str(self.activePlayer.board["Creature"][x]) + "\n"
    s += "Artifacts: \n"
    for x in range(len(self.activePlayer.board["Artifact"])):
      s += str(x) + ': ' + str(self.activePlayer.board["Artifact"][x]) + '\n'
    return s

  def deckOptions(self) -> List:
    retVal = []
    c = 0
    with open('decks/deckList.json', encoding='UTF-8') as f:
      stuff = json.load(f)
      for x in stuff:
        if c != self.first:
          retVal.append(x['name'])
        c += 1
    return retVal

  def main(self):
    wid, hei = [int(x) for x in self.WIN.get_size()]
    target_cardh = hei // 7
    ratio = CARDH // target_cardh
    ## inactive mat
    self.mat1 = pygame.Surface((wid, hei//2 - 5))
    self.mat1.convert()
    self.mat1.fill(COLORS["GREY"])
    
    mat_third = (self.mat1.get_height() - 30) // 3
    
    # hand
    self.hand1 = pygame.Surface((wid-150, mat_third))
    self.hand1.convert()
    self.hand1_rect = self.hand1.get_rect()
    self.hand1_rect.top = 0
    self.hand1_rect.centerx = wid/2 + 75
    self.hand1.fill(COLORS["YELLOW"])
    # creatures

    # artifacts

    # deck

    # discard

    # purge

    # divider
    self.divider = pygame.Surface((wid, 10))
    self.divider.convert()
    self.divider.fill(COLORS["BLACK"])
    
    # active mat
    self.mat2 = pygame.Surface((wid, hei//2 - 5))
    self.mat2.convert()
    self.mat2.fill(COLORS["GREEN"])


    self.WIN.blit(self.mat1, (0, 0))
    self.mat1.blit(self.hand1, self.hand1_rect)
    self.WIN.blit(self.divider, (0, self.mat1.get_height()))
    self.WIN.blit(self.mat2, (0, self.mat1.get_height() + 10))

    run = True
    started = False

    while run:
      self.CLOCK.tick(self.FPS)
      
      if not started and self.first != None and self.second != None:
        started = True
        self.startGame()
      
      for event in pygame.event.get():
        
        if event.type == pygame.MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = event.pos

        if event.type == pygame.QUIT:
          run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
          self.doPopup()
          
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          self.backgroundColor = COLORS[random.choice(list(COLORS.keys()))]
          
        if event.type == pygame.KEYDOWN:
          print(event)
          if event.key == 113 and event.mod == 64:
            run = False

      self.draw() # this will need hella updates
      pygame.display.flip()

    pygame.quit()


  def draw(self):
    self.allsprites.update()

    self.WIN.blit(self.mat1, (0, 0))
    self.WIN.blit(self.hand1, (0, 0))
    self.WIN.blit(self.divider, (0, self.mat1.get_height()))
    self.WIN.blit(self.mat2, (0, self.mat1.get_height() + 10))

    self.allsprites.draw(self.WIN)


  def doPopup(self):
    pos = pygame.mouse.get_pos()
    while True:
      if self.first == None or self.second == None:
        opt = self.deckOptions()
      elif 1 == 2:
        opt = [] # action options from clicking on a card
      elif 2 == 3:
        opt = [] # action options from clicking not on a card
      self.make_popup(opt, pos)
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == pygame.MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
          OPTION = self.option_selected(opt, pos)
          if OPTION != None:
            return OPTION
          else:
            return None
      self.CLOCK.tick(self.FPS)
  

  def option_selected(self, options, pos):
    w = 350
    popupSurf = pygame.Surface((w, pygame.font.Font.get_linesize(self.BASICFONT)*len(options)))
    popupSurf.convert()
    #draw up the surf, but don't blit it to the screen
    top = pos[1]
    for i in range(len(options)):
      textSurf = self.BASICFONT.render(options[i], 1, COLORS['BLUE'])
      textRect = textSurf.get_rect()
      textRect.top = top
      textRect.left = pos[0]
      top += pygame.font.Font.get_linesize(self.BASICFONT)
      popupSurf.blit(textSurf, textRect)
      if pygame.Rect.collidepoint(textRect, (self.mousex, self.mousey)):
        print(options)
        if self.first == None:
          self.first = i
          return
        elif self.second == None:
          self.second = i
          if self.second >= self.first:
            self.second += 1
          return
        print(f"Returning {options[i]}")
        return options[i]
    popupRect = popupSurf.get_rect()
    popupRect.centerx = pos[0] + w//2
    popupRect.centery = pos[1] + (pygame.font.Font.get_linesize(self.BASICFONT)*len(options))/2


  def make_popup(self, options, pos):
    w = 350
    popupSurf = pygame.Surface((350, pygame.font.Font.get_linesize(self.BASICFONT)*len(options)))
    popupSurf.fill(COLORS["BLACK"])
    top = pos[1]
    popupRect = popupSurf.get_rect()
    popupRect.centerx = pos[0] + w // 2
    popupRect.centery = pos[1] + (pygame.font.Font.get_linesize(self.BASICFONT)*len(options))/2
    self.WIN.blit(popupSurf, popupRect)
    for i in range(len(options)):
      textSurf = self.BASICFONT.render(options[i], 1, COLORS["YELLOW"])
      textRect = textSurf.get_rect()
      textRect.top = top
      textRect.left = pos[0]
      top += pygame.font.Font.get_linesize(self.BASICFONT)
      # pygame.draw.rect(self.WIN, COLORS["GREY"], textRect, border_radius=2)
      # popupSurf.blit(popupSurf, textRect)#COLORS["YELLOW"], textRect)
      self.WIN.blit(textSurf, textRect)
    pygame.display.update()


##################
# Turn functions #
##################

  def startGame(self): #called by choosedecks()
    """Fills hands, allows for mulligans and redraws, then plays the first turn, because that turn follows special rules.
    """
    first = random.choice([self.first, self.second])
    self.activePlayer = deck.Deck(deck.deckName(first))
    if first == self.first:
      self.inactivePlayer = deck.Deck(deck.deckName(self.second))
    else:
      self.inactivePlayer = deck.Deck(deck.deckName(self.first))
    logging.info("{} is going first.".format(deck.deckName(first)))
    pyautogui.alert("\n" + deck.deckName(first) + " is going first.\n")
    time.sleep(1)
    ##########################
    # Build state dictionary #
    ##########################
    # self.activePlayer.states = buildStateDict(self.activePlayer, self.inactivePlayer) # will look at all the cards, and add states that might be needed, not functional yet
    # self.inactivePlayer.states = buildStateDict(self.activePlayer, self.inactivePlayer)
    #####################
    # Draw and mulligan #
    #####################
    self.activePlayer += 7 #self.activePlayer += 7
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
    self.inactivePlayer += 6 # self.inactivePlayer += 6
    print("\n" + self.inactivePlayer.name + "'s hand:")
    self.inactivePlayer.printShort(self.inactivePlayer.hand)
    mull2 = input("Player 2, would you like to mulligan? \n>>>")
    if mull2 == "Yes" or mull2 == "Y" or mull2 == "y":
      for card in self.inactivePlayer.hand:
        self.inactivePlayer.deck.append(card)
      random.shuffle(self.inactivePlayer.deck)
      self.inactivePlayer.hand = []
      self.inactivePlayer += 5
    self.numPlays = 0
    self.numDiscards = 0
    self.turnNum = 1
    self.turn()
    # From here on should be in turn(), I think

  def turn(self):
    """ The passive actions of a turn. 1: Forge key (if poss, and if miasma hasn't changed the state; also reset state); 2: Calls chooseHouse(); 3: calls responses(), which needs to be moved into this class, and represents all actions (playing, discarding, fighting, etc) and info seeking; 4: ready cards; 5: draw cards. num is the turn number.
    """
    while True:
      logging.info("Turn: {}".format(self.turnNum))
      if not self.endBool:
        break
      self.lastCreaturesPlayed = self.creaturesPlayed
      logging.info("Num creatures played last turn: {}".format(self.lastCreaturesPlayed))
      self.creaturesPlayed = 0
      print("\nTurn: " + str(self.turnNum))
      if self.turnNum == 1:
        forgedThisTurn = False, 1
      if self.turnNum > 1:
        time.sleep(1)
        print(self) # step 0: show the board state
        time.sleep(1)
        print("You have {} amber and {} keys. Your opponent has {} amber and {} keys.\n".format(self.activePlayer.amber, self.activePlayer.keys, self.inactivePlayer.amber, self.inactivePlayer.keys))
        logging.info("You have {} amber and {} keys. Your opponent has {} amber and {} keys.\n".format(self.activePlayer.amber, self.activePlayer.keys, self.inactivePlayer.amber, self.inactivePlayer.keys))
        time.sleep(1)
        #####################################
        # Step 0.5: "Start of turn" effects #
        #####################################
        
        if True: # checks if there are any cards in either deck that have start of turn effects - where and when?
          pass #but actually execute start of turn effects
        
        ###################################################
        # step 1: check if a key is forged, then forge it #
        ###################################################
        # all code is here because it's short
        if self.checkForgeStates(): # returns True if you can forge, false if you can't (and why you can't), which in CotA is basically only Miasma
          self.activePlayer.keyCost = self.calculateCost()
          if self.activePlayer.amber >= self.activePlayer.keyCost:
            self.activePlayer.amber -= self.activePlayer.keyCost
            self.activePlayer.keys += 1
            print("You forged a key for", self.activePlayer.keyCost, "amber. You now have", self.activePlayer.keys, "key(s) and", self.activePlayer.amber, "amber.\n") # it works!
            if self.activePlayer.states["Forge"]["Interdimensional Graft"] and self.activePlayer.amber > 0:
              print("Your opponent played Interdimensional Graft last turn, so they gain your " + str(self.activePlayer.amber) + " leftover amber.")
              # can't use play.stealAmber b/c this isn't technically stealing so Vaultkeeper shouldn't be able to stop it
              self.inactivePlayer.amber += self.activePlayer.amber
              self.activePlayer.amber = 0
              print("They now have " + self.inactivePlayer.amber + " amber.")
            forgedThisTurn = True, self.turnNum
        else:
          print("Forging skipped this turn!")
        if self.activePlayer.keys >= 3:
          break
      ######################################
      # step 2: the player chooses a house #
      ######################################
      self.chooseHouse("activeHouse") # this command checks if anything is affecting their ability to choose a house
      ##################################################
      # step 2.5: the player may pick up their archive #
      ##################################################
      if len(self.activePlayer.archive) > 0:
        self.activePlayer.printShort(self.activePlayer.archive)
        while True:
          archive = input("Would you like to pick up your archive [y/n]?").title()
          if archive[0] == "Y":
            self.pending(self.activePlayer.archive, 'hand')
            break
          elif archive[0] == "N":
            pass
          else:
            print("Not a valid response. Try again.")
      ###############################################################################
      # step 3: play, discard, or use cards (and also inquire about the game state) #
      ###############################################################################
      self.responses(self.turnNum)
      ###################################################
      # step 4: ready cards and reset things like armor #
      ###################################################
      self.reset(self.turnNum, forgedThisTurn)
      ######################
      # step 5: draw cards #
      ######################
      self.activePlayer.drawEOT()
      if self.activePlayer.handSize < len(self.activePlayer.hand):
        logging.warn("Player seems to have too many cards in hand.")
      ###################################
      # step 5.5: check for EOT effects #
      ###################################
      self.checkEOTStates()
      
      # self.resetEOTStates()
      
      # step 5.3: switch players
      self.switch()
      # step 5.4: increment num
      self.turnNum += 1
      self.numPlays = 0
      self.numDiscards = 0
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
        yes = True
        # if the above works, they are trying to play a card, then we check for first turn
        # try:
        #   self.playCard(chosen)
        # except:
        #   print("playCard failed.")
        # print("Got past playCard()") # Test line
      except:
        yes = False
      if yes:
        self.playCard(chosen)
      if choice == 'h' or choice == 'H':
        print("Enter a number to play that card. Available info commands are 'House', 'Hand', 'Board', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'OppArchive', 'Keys', 'Amber', 'Card', 'MyDeck', 'OppDeck', 'OppHouses', and 'OppHand'. \nAvailable action commands are 'Turn', 'Fight', 'Discard', 'Action', 'Reap', 'EndTurn', and 'Concede'.\n>>>")
        choice2 = input("Type a command here to learn more about it, or press enter to return:\n>>>").title()
        while choice2 != '':
          if distance(choice2, "Hand") <= 1:
            print("Lists the names of the cards in your hand.")
          if distance(choice2, "House") <= 1:
            print("Lists the active house.")
          elif distance(choice2, "OppHouses") <= 1:
            print("Lists your opponent's houses.")
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
          elif distance(choice2, "Turn") <= 1:
            print("Returns the turn number.")
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
        self.activePlayer.printShort(self.activePlayer.hand)
      elif distance(choice, "House") <= 1:
        [print(x) for x in self.activeHouse]
      elif distance(choice, "Turn") <= 1:
        print("It is turn " + str(turn) + ".")
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
      elif distance(choice, "OppHouses") <= 1:
        [print(x) for x in self.inactivePlayer.houses]
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
        if self.numPlays == 1 and turn == 1:
          print("You've already taken your one action for turn one.")
          break
        self.activePlayer.printShort(self.activePlayer.hand)
        disc = makeChoice("Choose a card to discard: ", self.activePlayer.hand)
        self.discardCard(disc)
      elif distance(choice, "Action") <= 1:
        # Shows friendly cards in play with "Action" keyword, prompts a choice
        self.actionCard()
      elif distance(choice, "Reap") <= 1:
        # Shows friendly board, prompts choice.
        # Checks viability
        self.reapCard()
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
      if self.inactivePlayer.states["House"]["Control the Weak"] in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
        self.activeHouse = self.inactivePlayer.states["House"]["Control the Weak"]
        return
      while True:
        choice = input("Choose a house. Your deck's houses are " + self.activePlayer.houses[0] + ", " + self.activePlayer.houses[1] + ", " + self.activePlayer.houses[2] + ".\n>>>").title()
        if choice in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
          if "Restringuntus" in [x.title for x in self.inactivePlayer.board["Creature"]]:
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
  
  def calculateCost(self):
    """ Calculates the cost of a key considering current board state.
    """
    if True: # check if things that affect cost are even in any decks
      pass # return cost
    
    # Things to check: That annoying Dis artifact, Murmook, Grabber Jammer, that Mars upgrade, Titan Mechanic
    # Need to add a tag for affecting amber cost.
    cost = 6
    return cost

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

  def checkActionStates(self, card):
    """ Checks for things that affect actions.
    """
    # things that might return false
    # These two go first, because if you can't use a card, you can't unstun it
    if self.activePlayer.states["Action"]["Skippy Timehog"]:
      print("Your opponent played 'Skippy Timehog' last turn, so you can't use your action.")
      return False
    if card.title == "Giant Sloth" and not card.usable:
      print("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
      return False
    if card.stun == True:
      card.stun = False
      card.ready = False
      print("This creature is stunned and cannot be used.")
      return False
    if card.ready == False:
      print("This creature is not ready to be used.")
      return False
    


    # things to check if card is good to go
    if card.type == "Creature":
      self.activePlayer.states["Action"]["Stampede"] += 1
    
    
    
    
      return True

  def checkEOTStates(self):
    """ Checks for end of turn effects, and resets things that need to be reset.
    """
    # Check for Scout, and unskirmish those minions
    if len(self.activePlayer.states["Fight"]["Scout"]) > 0:
      for x in self.activePlayer.states["Fight"]["Scout"]:
        if "Skirmish" in x.text: x.skirmish = True
        else: x.skirmish = False


  def checkFightStates(self, attacker = None):
    """ Checks for fight states (warsong, etc) or before fight effects, or stun or exhaust.
    """
    # if we're here, we've already checked that there are enemy minions to attack
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    pendingDiscard = []
    # things that might return false
    
    # check for taunt
    
    if attacker.title == "Giant Sloth" and not attacker.usable:
      print("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
      return False
    if self.activePlayer.states["Fight"]["Skippy Timehog"]:
      print("Your opponent played 'Skippy Timehog' last turn, so you cannot fight.")
      return False
    if attacker.stun == True:
      attacker.stun = False
      attacker.ready = False
      print("This creature is stunned and cannot fight.")
      return False
    if attacker.ready == False:
      print("This creature is not ready to fight.")
      return False
    if self.activePlayer.states["Fight"]["Foggify"]:
      print("Your opponent played 'Foggify' last turn, so you cannot fight.")
      return False
    if self.activePlayer.states["Fight"]["Fogbank"]:
      print("Your opponent played 'Fogbank' last turn, so you cannot fight.")
      return False
    
    
    
    # things to check if fight is good to go
    self.activePlayer.states["Action"]["Stampede"] += 1
    if self.activePlayer.states["Fight"]["Warsong"][0]:
      self.activePlayer.amber += len(self.activePlayer.states["Fight"]["Warsong"])
    if self.activePlayer.states["Fight"]["Take Hostages"]:
      attacker.capture(self, 1)
    if "Before fight:" in attacker.text or "Before Fight:" in attacker.text: # this is actually going to be the last part of the checkFightStates function
      # before fight effects triggered here:

      # will need to check for deaths *after* before fight, but still before the fight
      # actually probably in the fight effect itself
      [pendingDiscard.append(active.pop(abs(x - len(active) + 1))) for x in range(len(active)) if active[abs(x - len(active) + 1)].update()]
      [pendingDiscard.append(inactive.pop(abs(x - len(inactive) + 1))) for x in range(len(inactive)) if inactive[abs(x - len(inactive) + 1)].update()]
      self.pending(pendingDiscard)
      if self.activePlayer.states["Fight"]["Warsong"][0]:
        self.activePlayer.amber += len(self.activePlayer.states["Fight"]["Warsong"])
      if len(self.inactivePlayer.board["Creature"]) == 0:
        print("Your opponent no longer has any creatures to attack. Your creature is still exhausted.")
    print("About to return True") # test line
    return True

  def checkForgeStates(self):
    """ Checks if there is anything in Deck.states["Forge"]. This isn't checking if you have enough amber.
    """
    if True: #optimization: if no cards in deck with this effect, just return
      pass # return True
    if self.activePlayer.states["Forge"]["Miasma"]:
      self.activePlayer.states["Forge"]["Miasma"] = False
      print("You skip your forge a key step this turn because your opponent played 'Miasma' last turn.")
      return False
    if "The Sting" in [x.title for x in self.activePlayer.board["Artifact"]]:
      print("You skip your forge a key step this turn because you have 'The Sting' in play.")
      return False
    return True

  def checkPlayStates(self, card):
    """ Checks for play states (full moon, etc.). By the time this is called, I already know if house matches.
    """
    # lifeward and other things that might return False first
    if card.type == "Upgrade":
      if len(self.activePlayer.board["Creature"]) == 0 and len(self.inactivePlayer.board["Creature"]) == 0:
        print("There are no creatures to play this upgrade on. It is not played.")
        return False
    if self.activePlayer.states["Play"]["Scrambler Storm"]:
      if card.type == "Action":
        print("Your opponent played 'Scrambler Storm' last turn, so you cannot play actions this turn.")
        return False
    if self.activePlayer.states["Play"]["Treasure Map"]:
      print("You played 'Treasure Map' this turn and can no longer play cards.")
      return False
    if card.title == "Truebaru":
      if self.activePlayer.amber < 3:
        print("You must have 3 amber to sacrifice in order to play 'Truebaru'.")
        return False
      self.activePlayer.amber -= 3
    if "Grommid" in [x.title for x in self.activePlayer.board["Creature"]] and card.type == "Creature":
      print("You can't play creatures with 'Grommid' in play.")
      return False

    
    # other play effects - things that don't want returns
    if card.type == "Creature":
      self.inactivePlayer.states["Play"]["Lifeweb"] += 1
      if self.activePlayer.states["Play"]["Full Moon"][0]:
        self.activePlayer.amber += len(self.activePlayer.states["Play"]["Full Moon"])
      if "Teliga" in [x.title for x in self.inactivePlayer.board["Creature"]]:
        count = 0
        for x in self.inactivePlayer.board["Creature"]:
          if x.title == "Teliga":
            count += 1
        self.inactivePlayer.amber += count
      if "Hunting Witch" in [x.title for x in self.activePlayer.board["Creature"]]:
        count = 0
        for x in self.activePlayer.board["Creature"]:
          if x.title == "Hunting Witch":
            count += 1
        self.activePlayer.amber += count
      if card.house == "Mars" and "Tunk" in [x.title for x in self.activePlayer.board["Creature"]]:
        location = [self.activePlayer.board["Creature"].index(x) for x in self.activePlayer.board["Creature"] if x.title == "Tunk"]
        for x in location:
          self.activePlayer.board["Creature"][x].damage = 0
      if self.activePlayer.states["Play"]["Charge!"]:
        choice = makeChoice("Choose an enemy minion to deal 2 damage to: ", self.inactivePlayer.board["Creature"])
        self.inactivePlayer.board["Creature"][choice].damageCalc(self, 2)
        pending = []
        [pending.append(self.inactivePlayer.board["Creature"].pop(choice)) for x in range(1) if self.inactivePlayer.board["Creature"][choice].update()]
        self.pending(pending)
    if card.type == "Artifact" and "Carlo Phantom" in [x.title for x in self.activePlayer.board["Creature"]]:
      play.stealAmber(self.activePlayer, self.inactivePlayer, 1)
      print("'Carlo Phantom' stole 1 amber for you. You now have " + str(self.activePlayer.amber) + " amber.")
    if self.activePlayer.states["Play"]["Library Access"]:
      self.activePlayer += 1
      print("You draw a card because you played 'Library Access' earlier this turn.")
    if self.activePlayer.states["Play"]["Soft Landing"]:
      card.ready = True
      print(card.title + " enters play ready!")
      self.activePlayer.states["Play"]["Soft Landing"]
   





    # only return True at the very end
    return True

  def checkReapStates(self, card):
    """ Checks for things that disallow reaping.
    """
    # things that might return false
    if card.title == "Giant Sloth" and not card.usable:
      print("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
      return False
    if self.activePlayer.states["Reap"]["Skippy Timehog"]:
      print("Your opponent played 'Skippy Timehog' last turn, so you cannot reap.")
      return False
    if card.stun == True:
      card.stun = False
      card.ready = False
      print("This creature is stunned and cannot reap.")
      return False
    if card.ready == False:
      print("This creature is not ready to reap.")
      return False
    

    # things to check/do if good to go
    self.activePlayer.states["Action"]["Stampede"] += 1
    

    return True

  def checkTaunt(self, defender, attacker):
    """ Checks to make sure taunt rules are obeyed.
    """
    inactive = self.activePlayer.board["Creature"]
    neigh = defender.neighbor(self)
    if len(neigh) == 2:
      if not defender.taunt and attacker.title != "Niffle Ape" and (inactive[neigh[1]].taunt or inactive[neigh[0]].taunt): # so if the thing attacked doesn't have taunt, if the attacker isn't niffle ape, and at least one neighbor has taunt
        print("One of " + defender.title + "'s neighbors has taunt. Choose a different target.")
        return False
      else:
        return True # either defender has taunt, attacker is niffle ape, or neither neighbor has taunt
    if len(neigh) == 1:
      if not defender.taunt and attacker.title != "Niffle Ape" and inactive[neigh[0]].taunt:
        print(defender.title + "'s neighbor has taunt. Choose a different target.")
        return False
      else:
        return True
    else: return True

    

##################
# Card functions #
##################

  def actionCard(self):
    """ Trigger a card's action from within the turn.
    """
    active = self.activePlayer.board["Creature"]
    art = self.activePlayer.board["Artifact"]
    actList = []
    [(actList.append(active[x], x)) for x in range(len(active)) if active[x].action == True or active[x].omni == True]
    [(actList.append(art[x], x)) for x in range(len(art)) if art[x].action == True or art[x].omni == True]
    [print(repr(actList[x])) for x in range(len(actList))]
    act = makeChoice("Choose an artifact or minion to use: ", actList)
    if not self.checkActionStates(actList[act]): # checks stuns, ready as well
      return # action states should explain why
    if actList[act].house in self.activeHouse:
      # Trigger action
      try:
        actList[act].action(self, actList[act])
      except:
        actList[act].omni(self, actList[act])
    else:
      print("You can only use cards from the active house.")
      return
  
  def discardCard(self, cardNum):
    """ Discard a card from hand, within the turn. Doesn't need to use pending for discards, but does use it for Rock-Hurling Giant.
    """
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    pending = []
    if self.activePlayer.hand[cardNum].house == self.activeHouse[0]:
      self.activePlayer.discard.append(self.activePlayer.hand.pop(cardNum))
      if "Giant Sloth" in [x.title for x in active] and self.activePlayer.discard[-1].house == "Untamed":
        index = [active.index(x) for x in active if x.title == "Giant Sloth"]
        for x in index:
          active[x].usable = True
      if "Rock-Hurling Giant" in [x.title for x in active] and self.activePlayer.discard[-1].house == "Brobnar":
        side = play.chooseSide(self, choices = False)
        if side == 0:
          target = makeChoice("Choose a creature to target: ", active)
          active[target].damageCalc(self, 4)
          if active[target].update():
            pending.append(active.pop(target))
        else:
          target = makeChoice("Choose a creature to target: ", inactive)
          inactive[target].damageCalc(self, 4)
          if inactive[target].update():
            pending.append(inactive.pop(target))
        self.pending(pending)
      if self.turnNum == 1:
        self.numPlays += 1
    else: print("You can only discard cards of the active house.")
    self.numDiscards += 1

  def fightCard(self, attacker = 100):
    """ This is needed for cards that trigger fights (eg anger, gauntlet of command). If attacker is fed in to the function (which will only be done by cards that trigger fights), the house check is skipped.
    """
    # Shows board, then prompts to choose attacker and defender
    print(self)
    if len(self.inactivePlayer.board["Creature"]) == 0:
      print("Your opponent has no creatures for you to attack. Fight canceled.")
      return self, None
    while True:
      if attacker >= len(self.activePlayer.board["Creature"]):
        try:
          attacker = makeChoice("Choose a minion to fight with: ", self.activePlayer.board["Creature"])
          # next line basically checks if they've listed a valid option
          if self.activePlayer.board["Creature"][attacker].house not in self.activeHouse:
            if len(self.extraFightHouses) > 0:
              if self.activePlayer.board["Creature"][attacker].house not in self.extraFightHouses:
                print("\nYou can only use cards from the active house or extra declared houses.")
                return self, None
            else:
              print("\nYou can only use cards from the active house.")
              return self, None
          break
        except:
          print("Your entry was invalid. Try again.")
      else:
        break
    # self.checkFightStates(attacker) also checks before fight abilities, stuns, and exhaustion/ready
    if self.checkFightStates(self.activePlayer.board["Creature"][attacker]):
      while True:
        defender = makeChoice("Choose a minion to fight against: ", self.inactivePlayer.board["Creature"])
        if not self.checkTaunt(self.activePlayer.board["Creature"][defender], self.activePlayer.board["Creature"][attacker]):
          continue # checkTaunt says why it failed
        else:
          break
    else:
      print("You cannot fight with that minion.")
    # Checks card is viable to fight or be fought (taunt)
    try:
      print("Trying to fight.")
      self.activePlayer.board["Creature"][attacker].fightCard(self.inactivePlayer.board["Creature"][defender], self)
    except: print("Fight failed.")
    pendingDiscard = []
    if self.activePlayer.board["Creature"][attacker].update():
      pendingDiscard.append(self.activePlayer.board["Creature"].pop(attacker))
    if self.inactivePlayer.board["Creature"][defender].update():
      pendingDiscard.append(self.inactivePlayer.board["Creature"].pop(defender))
    self.pending(pendingDiscard)

  def pending(self, L, destination = "discard", destroyed = True):
    """ Pending is the function that handles when multiple cards leave play at the same time, whether it be to hand or to discard. It will trigger leaves play and destroyed effects. Allowable options for dest are 'purge', 'discard', 'hand', 'deck'.
    """
    active = self.activePlayer.board
    inactive = self.inactivePlayer.board
    
    if L == []:
      return # just in case we feed it an empty list
    if destination not in ['purge', 'discard', 'hand', 'deck']:
      print("Pending was given an invalid destination.")
      return
    if "Annihilation Ritual" in ([x.title for x in active["Artifact"]] + [x.title for x in inactive["Creature"]]) and destroyed:
      destination = "annihilate"
    if destination == "purge":
      length = len(L)
      for x in range(length):
        if L[play.absa(x, length)].deck == self.activePlayer.name:
          self.activePlayer.purge.append(L.pop(play.absa(x, length)))
        elif L[play.absa(x, length)].deck == self.inactivePlayer.name:
          self.inactivePlayer.purge.append(L.pop(play.absa(x, length)))
    if destination == "annihilate": # we'll do this one first to remove all creatures (b/c annihilation ritual only affects creatures)
      length = len(L)
      for x in range(length):
        if L[play.absa(x, length)].deck == self.activePlayer.name and L[play.absa(x, length)].type == "Creature":
          self.activePlayer.purge.append(L.pop(play.absa(x, length)))
        elif L[play.absa(x, length)].deck == self.inactivePlayer.name and L[play.absa(x, length)].type == "Creature":
          self.inactivePlayer.purge.append(L.pop(play.absa(x, length)))
        destination = "discard" #now that all the creatures are out
    if destination == "discard":
      length = len(L)
      pendingA = []
      pendingI = []
      for x in range(length):
        if L[play.absa(x, length)].deck == self.activePlayer.name:
          pendingA.append(L.pop(play.absa(x, length)))
        elif L[play.absa(x, length)].deck == self.inactivePlayer.name:
          pendingI.append(L.pop(play.absa(x, length)))
        # now that they're sorted by owner
      if len(pendingA) > 0:
        while len(pendingA) > 1:
          choice = makeChoice("Choose which card to add to your discard first: ", pendingA)
          self.activePlayer.discard.append(pendingA.pop(choice))
        self.activePlayer.discard.append(pendingA.pop())
      if len(pendingI) > 0:
        while len(pendingI) > 1:
          choice = makeChoice("Choose which card to add to your opponent's discard first: ", pendingI)
          if not destroyed:
            self.inactivePlayer.hand.append(pendingI.pop(choice))
          else:
            self.inactivePlayer.discard.append(pendingI.pop(choice))
        # this is for the edge case of discarding cards from your opponents archive - if you have cards in your opponent's archive, they don't get discarded but added to your hand
        if not destroyed:
          self.inactivePlayer.hand.append(pendingI.pop(choice))
        else:
          self.inactivePlayer.discard.append(pendingI.pop(choice))
    if destination == "hand":
      length = len(L)
      for x in range(length):
        if L[play.absa(x, length)].deck == self.activePlayer.name:
          self.activePlayer.hand.append(L.pop(play.absa(x, length)))
        elif L[play.absa(x, length)].deck == self.inactivePlayer.name:
          self.inactivePlayer.hand.append(L.pop(play.absa(x, length)))
      self.activePlayer.hand.sort(key = lambda x: x.house)
      self.inactivePlayer.hand.sort(key = lambda x: x.house)
    if destination == "deck":
      length = len(L)
      pendingA = []
      pendingI = []
      for x in range(length):
        if L[play.absa(x, length)].deck == self.activePlayer.name:
          pendingA.append(L.pop(play.absa(x, length)))
        elif L[play.absa(x, length)].deck == self.inactivePlayer.name:
          pendingI.append(L.pop(play.absa(x, length)))
      if len(pendingA) > 0:
        while len(pendingA) > 1:
          choice = makeChoice("Choose which card to add to your deck first: ", pendingA)
          self.activePlayer.deck.append(pendingA.pop(choice))
        self.activePlayer.deck.append(pendingA.pop())
      if len(pendingI) > 0:
        while len(pendingI) > 1:
          choice = makeChoice("Choose which card to add to your opponent's deck first: ", pendingI)
          self.inactivePlayer.deck.append(pendingI.pop(choice))
        self.inactivePlayer.deck.append(pendingI.pop())
    # check that the list was emptied
    if L != []:
      print("Pending did not properly empty the list.")


  def playCard(self, chosen = 50, booly = True):
    """ This is needed for cards that play other cards (eg wild wormhole). Will also simplify responses. Booly is a boolean that tells whether or not to check if the house matches.
    """
    print(self.numPlays)
    if self.numPlays == 1 and self.turnNum == 1:
      return
    if chosen < len(self.activePlayer.hand):
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
        if self.activePlayer.hand[chosen].amber > 0:
          print(self.activePlayer.hand[chosen].title + " gave you " + str(self.activePlayer.hand[chosen].amber) + " amber. You now have " + str(self.activePlayer.amber) + " amber.")
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
          self.numPlays += 1
          print(self.numPlays) # test line
        # default case: right flank
        elif self.activePlayer.hand[chosen].type != "Upgrade":
          # print("playCard area 1.5") # test line
          print(cardType)
          self.activePlayer.board[cardType].append(self.activePlayer.hand.pop(chosen))
          # set a variable with the index of the card in board
          location = self.activePlayer.board[cardType][len(self.activePlayer.board[cardType]) - 1]
          self.numPlays += 1
          print(self.numPlays)
          print([x.title for x in self.activePlayer.board["Action"]])
        else:
          print("playCard area 1.6") # test line
          if len(self.activePlayer.board["Creature"]) > 0 or len(self.inactivePlayer.board["Creature"]) > 0:
            print("Choose a creature to play this upgrade on: ")
            target, side = play.chooseSide(self)
          else:
            print("There are no creatures to play this upgrade on. It is not played.")
            return
          self.activePlayer.board[cardType].append(self.activePlayer.hand.pop(chosen))
          location = self.activePlayer.board[cardType][len(self.activePlayer.board[cardType]) - 1]
          if side == 0: # friendly
            self.playUpgrade(self.activePlayer.board["Creature"][target])
          elif side == 1: # enemy
            self.playUpgrade(self.inactivePlayer.board["Creature"][target])
          else:
            return # shouldn't end up being triggered
        #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
        print(location.text)
        # try: 
        if location.play:
          location.play(self, location)
        # except:
        #   print("this card's play action failed.")
        #   pass
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
        if not self.checkPlayStates(self.activePlayer.deck[-1]):
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
          self.numPlays += 1
        # default case: right flank
        elif cardType != "Upgrade":
          print("playCard area 2.4") # test line
          self.activePlayer.board[cardType].append(self.activePlayer.deck.pop())
          location = self.activePlayer.board[cardType][len(self.activePlayer.board[cardType])]
          self.numPlays += 1
        else:
          print("playCard area 2.5") # test line
          self.activePlayer.board[cardType].append(self.activePlayer.deck.pop())
          if len(self.activePlayer.board["Creature"]) > 0 or len(self.inactivePlayer.board["Creature"]) > 0:
            location = self.activePlayer.board[cardType][len(self.activePlayer.board[cardType]) - 1]
            print("Choose a creature to play this upgrade on: ")
            target, side = play.chooseSide(self)
          else:
            print("There are no creatures to play this upgrade on. It goes back on top of your deck.")
            self.activePlayer.deck.append(self.activePlayer.board[cardType].pop())
            return
          if side == 0: # friendly
            self.playUpgrade(self.activePlayer.board["Creature"][target])
          elif side == 1: # enemy
            self.playUpgrade(self.inactivePlayer.board["Creature"][target])
          else:
            return # shouldn't end up being triggered
        #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
        print(location.text)
        # try: 
        if location.play:
          location.play(self, location)
        # except:
        #   print("This card's play action failed.")
        #   pass
        # if the card is an action, now add it to the discard pile
        if cardType == "Action":
          self.activePlayer.discard.append(self.activePlayer.board["Action"].pop())

  def playUpgrade(self, target):
    """ Plays an upgrade on a creature.
    """

  def reapCard(self):
    """ Triggers a card's reap effect from within the turn.
    """
    reapList = self.activePlayer.board["Creature"]
    self.activePlayer.printShort(reapList)
    reaper = makeChoice("Choose a creature to reap with: ", reapList)
    if not self.checkReapStates(reapList[reaper]):
      return # Reap States will say why
    if reapList[reaper].house in self.activeHouse:
      print("Reaping.") # test line
      reapList[reaper].reap(self, reapList[reaper])
      return
  
                #####################
                # End of Game Class #
                #####################

def developer(game):
  """Developer functions for manually changing the game state.
  """


