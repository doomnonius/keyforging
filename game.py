from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
import decks.decks as deck
import cards.cardsAsClass as card
import cards.destroyed as dest
import cards.actions as action
import cards.play as play
import cards.reap as reap
import cards.fight as fight
import json, random, logging, time, pygame, pyautogui, os
from helpers import makeChoice, buildStateDict
from typing import Dict, List, Set
from constants import COLORS, WIDTH, HEIGHT, CARDH, CARDW

#####################
# Contains modules: #
# - Game class      #
#####################

class Board():
  def __init__(self):
    """ first is first player, which is determined before the game is started. deck.deckName is a function that pulls the right deck from the list.
    """
    show = "Player 1, choose a deck number:\n"
    b = []
    with open('decks/deckList.json', encoding='utf-8') as f:
      data = json.load(f)
      for x in range(0, len(data)):
        show += f"{x}: {data[x]['name']}\n"
        b.append(str(x))
    self.first = int(pyautogui.confirm(show, buttons=b)) # None
    show = "Player 2, choose a deck number:\n"
    b = []
    with open('decks/deckList.json', encoding='utf-8') as f:
      data = json.load(f)
      for x in range(0, len(data)):
        if x != self.first:
          show += f"{x}: {data[x]['name']}\n"
          b.append(str(x))
    self.second = int(pyautogui.confirm(show, buttons=b))
    # if self.second >= self.first:
    #   self.second += 1
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
    self.turnStage = None
    self.response = []
    self.do = False
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
    self.FPS = 30
    self.WIN = pygame.display.set_mode((WIDTH, HEIGHT))#, flags = pygame.FULLSCREEN)
    pygame.display.set_caption('Keyforge')
    self.CLOCK = pygame.time.Clock()
    first = random.choice([self.first, self.second])
    self.activePlayer = deck.Deck(deck.deckName(first))
    if first == self.first:
      self.inactivePlayer = deck.Deck(deck.deckName(self.second))
    else:
      self.inactivePlayer = deck.Deck(deck.deckName(self.first))
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

  def turnOptions(self) -> List:
    return ['Hand', 'House', 'Turn', 'MyDiscard', 'OppDiscard', 'Board', 'MyPurge', 'OppPurge', 'MyArchive', 'OppArchive', 'OppHouses', 'Keys', 'Amber', 'Card', 'MyDeck', 'OppDeck','OppHand', 'EndTurn', 'Concede', 'Quit']
    
  def cardOptions(self) -> List:
    return ['Reap', 'Action', 'Fight', 'Omni']

  def handOptions(self) -> List:
    return ["Play", "Discard"]

  def main(self):
    wid, hei = [int(x) for x in self.WIN.get_size()]
    self.target_cardh = hei // 7
    ratio = CARDH / self.target_cardh
    self.target_cardw = int(CARDW // ratio)
    self.board_blits = []
    print(self.target_cardw, self.target_cardh)
    
    ## inactive mat
    self.mat1 = pygame.Surface((wid, hei//2 - 15))
    self.mat1.convert()
    self.mat1.fill(COLORS["BLACK"])
    self.board_blits.append((self.mat1, (0,0)))
    
    mat_third = (self.mat1.get_height()) // 3
    print(f"size: {self.WIN.get_size()}")
    # hand
    self.hand1 = pygame.Surface((wid - (self.target_cardw + 5), mat_third))
    self.hand1.convert()
    self.hand1.fill(COLORS["GREY"])
    self.hand1_rect = self.hand1.get_rect()
    self.hand1_rect.topleft = (0, 0)
    self.board_blits.append((self.hand1, self.hand1_rect))

    # purge/decklist
    self.purge1 = pygame.Surface((self.target_cardw, mat_third))
    self.purge1.convert()
    self.purge1.fill(COLORS["GREY"])
    self.purge1_rect = self.purge1.get_rect()
    self.purge1_rect.topright = (wid, 0)
    self.board_blits.append((self.purge1, self.purge1_rect))

    # artifacts
    self.artifacts1 = pygame.Surface((wid - (self.target_cardw + 5), mat_third))
    self.artifacts1.convert()
    self.artifacts1.fill(COLORS["GREY"])
    self.artifacts1_rect = self.artifacts1.get_rect()
    self.artifacts1_rect.topleft = (0, mat_third)
    self.board_blits.append((self.artifacts1, self.artifacts1_rect))

    # discard
    self.discard1 = pygame.Surface((self.target_cardw, mat_third))
    self.discard1.convert()
    self.discard1.fill(COLORS["GREY"])
    self.discard1_rect = self.discard1.get_rect()
    self.discard1_rect.topright = (wid, mat_third)
    self.board_blits.append((self.discard1, self.discard1_rect))
    
    # creatures
    self.creatures1 = pygame.Surface((wid - (self.target_cardw + 5), mat_third))
    self.creatures1.convert()
    self.creatures1.fill(COLORS["GREY"])
    self.creatures1_rect = self.creatures1.get_rect()
    self.creatures1_rect.topleft = (0, mat_third*2)
    self.board_blits.append((self.creatures1, self.creatures1_rect))

    # deck
    self.deck1 = pygame.Surface((self.target_cardw, mat_third))
    self.deck1.convert()
    self.deck1.fill(COLORS["GREY"])
    self.deck1_rect = self.deck1.get_rect()
    self.deck1_rect.topright = (wid, mat_third*2)
    self.board_blits.append((self.deck1, self.deck1_rect))

    ## active mat
    self.mat2 = pygame.Surface((wid, hei//2 - 15))
    self.mat2.convert()
    self.mat2.fill(COLORS["BLACK"])
    self.mat2_rect = self.mat2.get_rect()
    self.mat2_rect = (0, mat_third * 3)
    self.board_blits.append((self.mat2, self.mat2_rect))

    # deck2
    self.deck2 = pygame.Surface((self.target_cardw, mat_third))
    self.deck2.convert()
    self.deck2.fill(COLORS["GREEN"])
    self.deck2_rect = self.deck2.get_rect()
    self.deck2_rect.topleft = (0, hei - mat_third * 3)
    self.board_blits.append((self.deck2, self.deck2_rect))

    # creatures2
    self.creatures2 = pygame.Surface((wid - (self.target_cardw + 5), mat_third))
    self.creatures2.convert()
    self.creatures2.fill(COLORS["GREEN"])
    self.creatures2_rect = self.creatures2.get_rect()
    self.creatures2_rect.topright = (wid, hei - mat_third * 3)
    self.board_blits.append((self.creatures2, self.creatures2_rect))

    # discard2
    self.discard2 = pygame.Surface((self.target_cardw, mat_third))
    self.discard2.convert()
    self.discard2.fill(COLORS["GREEN"])
    self.discard2_rect = self.discard2.get_rect()
    self.discard2_rect.topleft = (0, hei - mat_third * 2)
    self.board_blits.append((self.discard2, self.discard2_rect))

    # artifacts2
    self.artifacts2 = pygame.Surface((wid - (self.target_cardw + 5), mat_third))
    self.artifacts2.convert()
    self.artifacts2.fill(COLORS["GREEN"])
    self.artifacts2_rect = self.artifacts2.get_rect()
    self.artifacts2_rect.topright = (wid, hei - mat_third * 2)
    self.board_blits.append((self.artifacts2, self.artifacts2_rect))

    # purge2
    self.purge2 = pygame.Surface((self.target_cardw, mat_third))
    self.purge2.convert()
    self.purge2.fill(COLORS["GREEN"])
    self.purge2_rect = self.purge2.get_rect()
    self.purge2_rect.topleft = (0, hei - mat_third)
    self.board_blits.append((self.purge2, self.purge2_rect))

    # hand2
    self.hand2 = pygame.Surface((wid - (self.target_cardw + 5), mat_third))
    self.hand2.convert()
    self.hand2.fill(COLORS["GREEN"])
    self.hand2_rect = self.hand2.get_rect()
    self.hand2_rect.topright = (wid, hei - mat_third)
    self.board_blits.append((self.hand2, self.hand2_rect))

    ## divider1
    self.divider = pygame.Surface((wid//2, 30))
    self.divider.convert()
    self.divider.fill(COLORS["GREY"])
    self.divider_rect = self.divider.get_rect()
    self.divider_rect.topleft = (0, self.mat1.get_height())
    self.key1y, self.key1y_rect = load_image("yellow_key_back", -1)
    self.key_forged, self.key_forged_rect = load_image("yellow_key_front", -1)
    self.key1y_rect.topleft = (2, 2)
    self.key1r, self.key1r_rect = load_image("yellow_key_back", -1)
    self.key1r_rect.topleft = (35, 2)
    self.key1b, self.key1b_rect = load_image("yellow_key_back", -1)
    self.key1b_rect.topleft = (68, 2)
    self.board_blits.append((self.divider, self.divider_rect))
    
    ## divider2
    self.divider2 = pygame.Surface((wid//2, 30))
    self.divider2.convert()
    self.divider2.fill(COLORS["GREEN"])
    div2_w = self.divider2.get_width()
    self.divider2_rect = self.divider2.get_rect()
    self.divider2_rect.topright = (wid, self.mat1.get_height())
    self.key2y, self.key2y_rect = load_image("yellow_key_back", -1)
    self.key2y_rect.topright = (div2_w - 2, 2)
    self.key2r, self.key2r_rect = load_image("yellow_key_back", -1)
    self.key2r_rect.topright = (div2_w - 35, 2)
    self.key2b, self.key2b_rect = load_image("yellow_key_back", -1)
    self.key2b_rect.topright = (div2_w - 68, 2)
    self.board_blits.append((self.divider2, self.divider2_rect))
    
    # amber1
    self.amber1 = self.BASICFONT.render(f"{self.inactivePlayer.amber} amber", 1, COLORS['BLACK'])
    self.amber1_rect = self.amber1.get_rect()
    self.amber1_rect.topright = (self.divider.get_width() - 10, 5)

    # amber2
    self.amber2 = self.BASICFONT.render(f"{self.activePlayer.amber} amber", 1, COLORS['BLACK'])
    self.amber2_rect = self.amber2.get_rect()
    self.amber2_rect.topleft = (10, 5)
    
    self.inactive_info = [(self.key1y, self.key1y_rect), (self.key1r, self.key1r_rect), (self.key1b, self.key1b_rect), (self.amber1, self.amber1_rect)]
    self.active_info = [(self.key2y, self.key2y_rect), (self.key2r, self.key2r_rect), (self.key2b, self.key2b_rect), (self.amber2, self.amber2_rect)]

    run = True
    started = False

    while run:
      self.CLOCK.tick(self.FPS)

      for event in pygame.event.get():
        
        if event.type == pygame.MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = event.pos

        if event.type == pygame.QUIT:
          run = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
          self.doPopup()
          
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
          if not started:
            started = True
            self.forgedThisTurn = False, 0
            # self.startGame() # I want to put this in the self.turnStage == None section

          self.backgroundColor = COLORS[random.choice(list(COLORS.keys()))]
          
        if event.type == pygame.KEYDOWN:
          print(event)
          if event.key == 113 and (event.mod == 64 or event.mod == 4160):
            run = False

      # handle card hovering

      self.hovercard = []
      hoverable = self.activePlayer.hand + self.inactivePlayer.hand + self.activePlayer.board["Creature"] + self.inactivePlayer.board["Creature"] + self.activePlayer.board["Artifact"] + self.inactivePlayer.board["Artifact"]

      for card in hoverable:
        if pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)):
          self.hovercard.append(card)
          break

      ######################
      # Initial hand fill  #
      ######################

      if self.turnStage == None:
        logging.info(f"{self.activePlayer.name} is going first.")
        pyautogui.alert(f"\n{self.activePlayer.name} is going first.\n")
        ##########################
        # Build state dictionary #
        ##########################
        # self.activePlayer.states = buildStateDict(self.activePlayer, self.inactivePlayer) # will look at all the cards, and add states that might be needed, not functional yet
        # self.inactivePlayer.states = buildStateDict(self.activePlayer, self.inactivePlayer)
        #####################
        # Draw and mulligan #
        #####################
        if not self.do:
          self.activePlayer += 7
        else:
          show = f'{self.activePlayer.name}\'s hand:\n'
          for card in self.activePlayer.hand:
            show += f"{card.title} ({card.house})\n"
          mull = pyautogui.confirm(f"Player 1, would you like to keep?\n{show}", buttons=["Yes","No"])
          if mull == "No":
            for card in self.activePlayer.hand:
              self.activePlayer.deck.append(card)
            random.shuffle(self.activePlayer.deck)
            self.activePlayer.hand = []
            self.activePlayer += 6
        if not self.do:
          self.inactivePlayer += 6
        else:
          show = f'{self.inactivePlayer.name}\'s hand:\n'
          for card in self.inactivePlayer.hand:
            show += f"{card.title} ({card.house})\n"
          mull2 = pyautogui.confirm(f"Player 2, would you like to keep?\n{show}", buttons=["Yes","No"])
          if mull2 == "No":
            for card in self.inactivePlayer.hand:
              self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
          self.numPlays = 0
          self.numDiscards = 0
          self.turnNum = 1
          self.turnStage = 0
        self.do = True

      ###################################
      # Step 0: "Start of turn" effects #
      ###################################

      elif self.turnStage == 0: # start of turn effects
        self.lastCreaturesPlayed = self.creaturesPlayed
        self.creaturesPlayed = 0
        self.turnStage += 1
      
      ###################################################
      # step 1: check if a key is forged, then forge it #
      ###################################################

      elif self.turnStage == 1: # forge a key
        if self.checkForgeStates(): # returns True if you can forge, false if you can't (and why you can't), which in CotA is basically only Miasma
          self.activePlayer.keyCost = self.calculateCost()
          if self.activePlayer.amber >= self.activePlayer.keyCost:
            self.activePlayer.amber -= self.activePlayer.keyCost
            self.activePlayer.keys += 1
            pyautogui.alert(f"You forged a key for {self.activePlayer.keyCost} amber. You now have {self.activePlayer.keys} key(s) and {self.activePlayer.amber} amber.\n") # it works!
            if self.activePlayer.states["Forge"]["Interdimensional Graft"] and self.activePlayer.amber > 0:
              pyautogui.alert(f"Your opponent played Interdimensional Graft last turn, so they gain your {self.activePlayer.amber} leftover amber.")
              # can't use play.stealAmber b/c this isn't technically stealing so Vaultkeeper shouldn't be able to stop it
              self.inactivePlayer.amber += self.activePlayer.amber
              self.activePlayer.amber = 0
              pyautogui.alert(f"They now have {self.inactivePlayer.amber} amber.")
            self.forgedThisTurn = True, self.turnNum
          else:
            pyautogui.alert("No key forged this turn, not enough amber.")
        else:
          pyautogui.alert("Forging skipped this turn but I'm not going to tell you why!")
        if self.activePlayer.keys >= 3:
          pyautogui.alert(f"{self.activePlayer.name} wins!")
          run = False
        self.turnStage += 1
      
      ######################################
      # step 2: the player chooses a house #
      # and if to pick up their archive    #
      ######################################

      elif self.turnStage == 2: # choose a house, optionally pick up archive
        self.chooseHouse("activeHouse")
        if len(self.activePlayer.archive) > 0:
          self.activePlayer.printShort(self.activePlayer.archive)
          while True:
            archive = pyautogui.confirm("Would you like to pick up your archive?", buttons=["Yes", "No"])
            if archive == "Yes":
              self.pending(self.activePlayer.archive, 'hand')
              break
            elif archive == "No":
              pass
            else:
              pyautogui.alert("Not a valid response. Try again.")
        self.turnStage += 1

      ###############################################################################
      # step 3: play, discard, or use cards (and also inquire about the game state) #
      ###############################################################################

      elif self.turnStage == 3:
        if self.response:
          if len(self.response) == 1:
            self.response = self.response[0]
          if len(self.response) == 2:
            self.response, self.targetCard = self.response
          
          if self.response == "Hand":
            show = ''
            for card in self.activePlayer.hand:
              show += f"{card.title} ({card.house})\n"
            pyautogui.alert(show)
          elif self.response == "House":
            pyautogui.alert(self.activeHouse)
          elif self.response == "Board":
            print(self)
          elif self.response == "Turn":
            pyautogui.alert(f"It is turn {self.turnNum}, stage {self.turnStage}.")
          elif self.response == "MyDiscard":
            show = ''
            for card in self.activePlayer.discard:
              show += f"{card.title}\n"
            pyautogui.alert(show)
          elif self.response == "OppDiscard":
            show = ''
            for card in self.inactivePlayer.discard:
              show += f"{card.title}\n"
            pyautogui.alert(show)
          elif self.response == "MyPurge":
            show = ''
            for card in self.inactivePlayer.purged:
              show += f"{card.title}\n"
            pyautogui.alert(show)
          elif self.response == "OppPurge":
            show = ''
            for card in self.inactivePlayer.purged:
              show += f"{card.title}\n"
            pyautogui.alert(show)
          elif self.response == "MyArchive":
            show = ''
            for card in self.activePlayer.archive:
              show += f"{card.title}\n"
            pyautogui.alert(show)
          elif self.response == "OppArchive":
            pyautogui.alert("There are " + str(len(self.inactivePlayer.archive) + " cards in your opponent's archive."))
          elif self.response == "OppHouses":
            show = 'Your opponent\'s houses are:\n'
            for house in self.inactivePlayer.houses:
              show += f"{house}\n"
            pyautogui.alert(show)
          elif self.response == "Keys" or self.response == "Amber":
            pyautogui.alert(f"You have {self.activePlayer.amber} amber and {self.activePlayer.keys} keys. Your opponent has {self.inactivePlayer.amber} amber and {self.inactivePlayer.keys} keys.")
          elif self.response == "Card":
            cardName = pyautogui.prompt("Enter the name of a card from one of the active decks:").lower()
            # print(f"Testing prompt: {cardName}")
            for x in [deck.Deck(deck.deckName(self.first)), deck.Deck(deck.deckName(self.second))]:
              for card in x.deck:
                if cardName == card.title.replace(" ", "_"):
                  pyautogui.alert(card.text)
                  break
          elif self.response == "MyDeck":
            pyautogui.alert("Your deck has " + str(len(self.activePlayer.deck)) + " cards.")
          elif self.response == "OppDeck":
            pyautogui.alert("Your opponent's deck has " + str(len(self.inactivePlayer.deck)) + " cards.")
          elif self.response == "OppHand":
            pyautogui.alert("Your opponent's hand has " + str(len(self.inactivePlayer.hand)) + " cards.")
          elif self.response == "EndTurn":
            pyautogui.alert("Ending Turn!")
            self.turnStage += 1
          elif self.response == "Concede":
            pyautogui.alert(f"{self.inactivePlayer.name} wins!")
            run = False
          elif self.response == "Quit":
            run = False
          
          ## these will work slightly differently
          elif self.response == "Play":
            # hands off the info to the "Fight" function
            self.playCard()
          elif self.response == "Fight":
            # hands off the info to the "Fight" function
            self.fightCard()
          elif self.response == "Discard":
            if self.numPlays == 1 and self.turnNum == 1:
              pyautogui.alert("You've already taken your one action for turn one.")
              break
            # self.activePlayer.printShort(self.activePlayer.hand)
            show = "Choose a card to discard:\n\n"
            b = []
            for x in range(len(self.activePlayer.hand)):
              show += f"{x}: {self.activePlayer.hand[x].title}"
              b += str(x)
            disc = int(pyautogui.confirm(show, buttons=b))
            self.discardCard(disc)
          elif self.response == "Action":
            # Shows friendly cards in play with "Action" keyword, prompts a choice
            self.actionCard()
          elif self.response == "Reap":
            # Shows friendly board, prompts choice.
            # Checks viability
            self.reapCard()

          self.response = []

      ###################################################
      # step 4: ready cards and reset things like armor #
      ###################################################

      elif self.turnStage == 4: # ready and reset armor
        self.reset(self.turnNum, self.forgedThisTurn)
        self.turnStage += 1
      
      ######################
      # step 5: draw cards #
      ######################

      elif self.turnStage == 5: # end of turn draw and end of turn effects
        self.activePlayer.drawEOT()
        
        self.checkEOTStates()

        # switch players
        self.switch()
        self.turnNum += 1
        self.numPlays = 0
        self.numDiscards = 0
        self.turnStage = 0
      
      self.draw() # this will need hella updates
      pygame.display.flip()

    pygame.quit()


  def draw(self):
    self.allsprites.update()
    self.WIN.blits(self.board_blits)
    self.divider.blits(self.inactive_info)
    self.divider2.blits(self.active_info)
    x = 0
    # card areas
    for board,area in [(self.activePlayer.hand, self.hand2_rect), (self.inactivePlayer.hand, self.hand1_rect), (self.activePlayer.board["Creature"], self.creatures2_rect), (self.inactivePlayer.board["Creature"], self.creatures1_rect), (self.activePlayer.board["Artifact"], self.artifacts2_rect), (self.inactivePlayer.board["Artifact"], self.artifacts1_rect)]:
      for card in board:
        card_image, card_rect = card.scaled_image(self.target_cardw, self.target_cardh)
        card_rect.topleft = (area.left + (x * self.target_cardw) + 5 * (x + 1), area.top)
        x += 1
        self.WIN.blit(card_image, card_rect)
    # discards
    l = len(self.activePlayer.discard)
    if l > 0:
      card_image, card_rect = self.activePlayer.discard[l - 1].scaled_image(self.target_cardw, self.target_cardh)
      card_rect.topright = (self.discard2_rect.left, self.discard2_rect.top)
      self.WIN.blit(card_image, card_rect)
    l = len(self.inactivePlayer.discard)
    if l > 0: 
      card_image, card_rect = self.inactivePlayer.discard[l - 1].scaled_image(self.target_cardw, self.target_cardh)
      card_rect.topleft = (self.discard1_rect.left, self.discard1_rect.top)
      self.WIN.blit(card_image, card_rect)
    # decks
    # going to need a card back of some sort to put here
    l = len(self.activePlayer.deck)
    if l > 0:
      card_image, card_rect = self.activePlayer.deck[0].scaled_image(self.target_cardw, self.target_cardh)
      card_rect.topleft = (self.deck2_rect.left, self.deck2_rect.top)
      self.WIN.blit(card_image, card_rect)
    l = len(self.inactivePlayer.deck)
    if l > 0:
      card_image, card_rect = self.inactivePlayer.deck[0].scaled_image(self.target_cardw, self.target_cardh)
      card_rect.topleft = (self.deck1_rect.left, self.deck1_rect.top)
      self.WIN.blit(card_image, card_rect)
    if self.hovercard:
      hover, hover_rect = self.hovercard[0].orig_image, self.hovercard[0].orig_rect
      if self.mousey > HEIGHT / 2:
        hover_rect.top = self.mousey - CARDH
        while hover_rect.top < 0:
          hover_rect.top += 10
      else:
        hover_rect.top = self.mousey
        while hover_rect.top > HEIGHT:
          hover_rect.top -= 10
      if self.mousex > WIDTH / 2:
        hover_rect.left = self.mousex - CARDW
      else:
        hover_rect.left = self.mousex
      self.WIN.blit(hover, hover_rect)
    self.allsprites.draw(self.WIN)


  def doPopup(self):
    pos = pygame.mouse.get_pos()
    card = False
    board = False
    while True:
      if True in [pygame.Rect.collidepoint(x.rect, pos) for x in self.activePlayer.hand]: # check for collisions with a card: action options from clicking on a card
        opt = self.handOptions()
        card = True
      elif True in []:
        opt = self.cardOptions()
      else: # action options from clicking not on a card: then check for a collision with a mat
        opt = self.turnOptions()
        board = True
      self.make_popup(opt, pos)
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == pygame.MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
          OPTION = self.option_selected(opt, pos)
          if OPTION != None:
            if card:
              pass
            elif board:
              self.response = [OPTION]
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
      self.WIN.blit(textSurf, textRect)
    pygame.display.update()


##################
# Turn functions #
##################

  def startGame(self): #called by choosedecks()
    """Fills hands, allows for mulligans and redraws, then plays the first turn, because that turn follows special rules.
    """
    logging.info(f"{self.activePlayer.name} is going first.")
    pyautogui.alert(f"\n{self.activePlayer.name} is going first.\n")
    ##########################
    # Build state dictionary #
    ##########################
    # self.activePlayer.states = buildStateDict(self.activePlayer, self.inactivePlayer) # will look at all the cards, and add states that might be needed, not functional yet
    # self.inactivePlayer.states = buildStateDict(self.activePlayer, self.inactivePlayer)
    #####################
    # Draw and mulligan #
    #####################
    self.activePlayer += 7
    self.draw()
    show = f'{self.activePlayer.name}\'s hand:\n'
    for card in self.activePlayer.hand:
      show += f"{card.title} ({card.house})\n"
    mull = pyautogui.confirm(f"Player 1, would you like to keep?\n{show}", buttons=["Yes","No"])
    if mull == "No":
      for card in self.activePlayer.hand:
        self.activePlayer.deck.append(card)
      random.shuffle(self.activePlayer.deck)
      self.activePlayer.hand = []
      self.activePlayer += 6
    self.inactivePlayer += 6
    self.draw()
    show = f'{self.inactivePlayer.name}\'s hand:\n'
    for card in self.inactivePlayer.hand:
      show += f"{card.title} ({card.house})\n"
    mull2 = pyautogui.confirm(f"Player 2, would you like to keep?\n{show}", buttons=["Yes","No"])
    if mull2 == "No":
      for card in self.inactivePlayer.hand:
        self.inactivePlayer.deck.append(card)
      random.shuffle(self.inactivePlayer.deck)
      self.inactivePlayer.hand = []
      self.inactivePlayer += 5
    self.numPlays = 0
    self.numDiscards = 0
    self.turnNum = 1
    self.turnStage = 0

  def switch(self):
    """ Swaps active and inactive players.
    """
    self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer
    # print("Players swapped") # test line: passed on 5/14/21


  def chooseHouse(self, varAsStr, num = 1):
    """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards like control the weak. Num is used for cards that allow extra houses to fight or be used.
    """
    if varAsStr == "activeHouse":
      show = 'Your hand is:\n'
      for card in self.activePlayer.hand:
        show += f"{card.title} ({card.house})\n"
      if self.inactivePlayer.states["House"]["Control the Weak"] in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
        self.activeHouse = self.inactivePlayer.states["House"]["Control the Weak"]
        return
      while True:
        choice = pyautogui.confirm(text=f"{show}\nChoose a house:", buttons=[self.activePlayer.houses[0],self.activePlayer.houses[1],self.activePlayer.houses[2]])
        if choice.title() in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
          if "restringuntus" in [x.title for x in self.inactivePlayer.board["Creature"]]:
            self.activeHouse = self.activePlayer.restring # I was able to verify that there will never be more than one copy of Restringuntus in a deck
          else:
            self.activeHouse = choice
          return
        else:
          pyautogui.alert("That's not a valid choice! And how did you even get here?")
    elif varAsStr == "extraFight": #for brothers in battle, and probably others
      if num == 1:
        while True:
          extra = pyautogui.confirm("Choose another house to fight with:", buttons=["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"])
          if extra != self.activeHouse:
          # if extra in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"] and extra != self.activeHouse:
            self.extraFightHouses.append(extra)
            break
          elif extra == self.activeHouse:
            pyautogui.alert("\nThat's already your active house. Try again.\n")
          else:
            pyautogui.alert("\nNot a valid input.\n")
    elif varAsStr == "Restringuntus":
      while True:
        extra = pyautogui.confirm("This is still incomplete", buttons=["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"])
        if extra in ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]:
          self.inactivePlayer.restring = extra
          break
        else:
          pyautogui.alert("\nNot a valid input.\n")  
  
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
  
  def discardCard(self, cardNum: int):
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
    else: pyautogui.alert("You can only discard cards of the active house.")
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

def load_image(title, colorkey=None):
  fullname = os.path.join(f'game_assets', title + '.png')
  try:
      image = pygame.image.load(fullname)
  except pygame.error as message:
      logging.error(f'Cannot load image: {title}, {message}')
      raise SystemExit(message)
  image = image.convert()
  if colorkey is not None:
      if colorkey == -1:
          colorkey = image.get_at((0,0))
      image.set_colorkey(colorkey)
  scaled = pygame.transform.scale(image, (26, 26))
  return scaled, scaled.get_rect()

def developer(game):
  """Developer functions for manually changing the game state.
  """


