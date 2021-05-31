from tkinter.constants import E
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, SRCALPHA
import decks.decks as deck
import cards.cardsAsClass as card
import cards.upgrades as upgrade
import json, random, logging, time, pygame, pyautogui, os
from helpers import makeChoice, willEnterReady, absa, destroy
from typing import Dict, List, Set, Tuple
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
        show += f"{x}: {data[x]['name']} {data[x]['houses']}\n"
        b.append(str(x))
    self.first = int(pyautogui.confirm(show, buttons=b)) # None
    show = "Player 2, choose a deck number:\n"
    b = []
    with open('decks/deckList.json', encoding='utf-8') as f:
      data = json.load(f)
      for x in range(0, len(data)):
        if x != self.first:
          show += f"{x}: {data[x]['name']} {data[x]['houses']}\n"
          b.append(str(x))
    self.second = int(pyautogui.confirm(show, buttons=b))
    self.top = 0
    self.left = 0
    self.mousex = 0
    self.mousey = 0
    self.dragging = []
    self.response = []
    self.turnNum = 0
    # reset each turn cycle
    self.activeHouse = []
    self.extraFightHouses = []
    self.extraUseHouses = []
    self.playedThisTurn = []
    self.discardedThisTurn = []
    self.usedThisTurn = []
    self.playedLastTurn = []
    self.discardLastTurn = []
    self.usedLastTurn = []
    self.forgedThisTurn = []
    self.forgedLastTurn = []
    self.turnStage = None
    self.pendingReloc = []
    self.extraDraws = []
    self.dataBlits = []
    self.cardBlits = []
    self.highlight = []
    self.resetStates = []
    self.resetStatesNext = []
    # draw bools
    self.remaining = True
    self.drawFriendDiscard = False
    self.closeFriendDiscard = None
    self.drawEnemyDiscard = False
    self.closeEnemyDiscard = None
    self.drawFlanks = False
    self.deploy = False
    self.drawFriendPurge = False
    self.closeFriendPurge = None
    self.drawEnemyPurge = False
    self.closeFriendPurge = None
    self.drawFriendArchive = False
    self.closeFriendArchive = None
    self.drawEnemyArchive = False
    self.closeEnemyArchive = None
    self.friendDraws = []
    self.enemyDraws = []
    self.do = False
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
    self.FPS = 30
    self.WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SRCALPHA) #, flags = pygame.FULLSCREEN)
    self.SMALLFONT = pygame.font.SysFont("Corbel", max(HEIGHT // 45, 14))
    self.BASICFONT = pygame.font.SysFont("Corbel", HEIGHT // 27)
    self.OTHERFONT = pygame.font.SysFont("Corbel", HEIGHT // 14)
    self.margin = HEIGHT // 108
    pygame.display.set_caption('Keyforge')
    self.CLOCK = pygame.time.Clock()
    self.target_cardh = HEIGHT // 7
    ratio = CARDH / self.target_cardh
    self.target_cardw = int(CARDW // ratio)
    self.invisicard = card.Invisicard(self.target_cardw, self.target_cardh)
    first = random.choice([self.first, self.second])
    self.activePlayer = deck.Deck(deck.deckName(first), self.target_cardw, self.target_cardh, self.margin)
    if first == self.first:
      self.inactivePlayer = deck.Deck(deck.deckName(self.second), self.target_cardw, self.target_cardh, self.margin)
    else:
      self.inactivePlayer = deck.Deck(deck.deckName(self.first), self.target_cardw, self.target_cardh, self.margin)
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
    return ['House', 'Turn', 'MyDiscard', 'OppDiscard', 'MyPurge', 'OppPurge', 'MyArchive', 'OppArchive', 'OppHouses', 'Keys', 'Card', 'MyDeck', 'OppDeck','OppHand', 'Concede', 'Quit']
    
  def cardOptions(self, cardNum: int, loc: str) -> List:
    retVal = ["Details"]
    card = self.activePlayer.board[loc][cardNum]
    if not card.ready:
      return ["You can't use a card that isn't ready."]
    if self.canFight(card, reset=False, r_click = True):
      retVal.append("Fight")
    if self.canReap(card, reset=False, r_click = True):
      retVal.append("Reap")
    if self.canAction(card, reset=False, r_click = True):
      retVal.append("Action/Omni")
    if card.type == "Creature" and card.stun and retVal: # have to be able to use a card to unstun, so this is perfect
      return ["Unstun"]
    if not retVal:
      return ["You can't use this card right now."]
    return retVal

  def handOptions(self, cardNum: int) -> List:
    # There are other things that prevent playing cards that I want to include here as well, think I have most of them
    retVal = []
    card = self.activePlayer.hand[cardNum]
    if self.canPlay(card):
      retVal.append("Play")
    if self.canDiscard(card):
      retVal.append("Discard")
    if not retVal:
      return ["You can't play or discard this card."]
    return retVal

  def main(self):
    wid, hei = [int(x) for x in self.WIN.get_size()]
    self.board_blits = []
    
    ## inactive mat
    self.mat2 = pygame.Surface((wid, hei // 2))
    self.mat2.convert()
    self.mat2_rect = self.mat2.get_rect()
    mat_third = (self.mat2.get_height()) // 3
    self.mat2.fill(COLORS["BLACK"])
    self.mat2_rect.topleft = (0, -mat_third // 2)
    self.board_blits.append((self.mat2, self.mat2_rect))

    # hand
    self.hand2 = pygame.Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.hand2.convert()
    self.hand2.fill(COLORS["GREY"])
    self.hand2_rect = self.hand2.get_rect()
    self.hand2_rect.topleft = (0, -mat_third // 2)
    self.board_blits.append((self.hand2, self.hand2_rect))

    # artifacts
    self.artifacts2 = pygame.Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.artifacts2.convert()
    self.artifacts2.fill(COLORS["GREY"])
    self.artifacts2_rect = self.artifacts2.get_rect()
    self.artifacts2_rect.topleft = (0, mat_third // 2)
    self.board_blits.append((self.artifacts2, self.artifacts2_rect))

    # discard
    self.discard2 = pygame.Surface((self.target_cardw, mat_third))
    self.discard2.convert()
    self.discard2.fill(COLORS["GREY"])
    self.discard2_rect = self.discard2.get_rect()
    self.discard2_rect.topright = (wid, 0)
    self.board_blits.append((self.discard2, self.discard2_rect))

    # creatures
    self.creatures2 = pygame.Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.creatures2.convert()
    self.creatures2.fill(COLORS["GREY"])
    self.creatures2_rect = self.creatures2.get_rect()
    self.creatures2_rect.topleft = (0, int(mat_third * 1.5))
    self.board_blits.append((self.creatures2, self.creatures2_rect))

    # deck
    self.deck2 = pygame.Surface((self.target_cardw, mat_third))
    self.deck2.convert()
    self.deck2.fill(COLORS["GREY"])
    self.deck2_rect = self.deck2.get_rect()
    self.deck2_rect.topright = (wid, mat_third)
    self.board_blits.append((self.deck2, self.deck2_rect))

    # purged2
    self.purge2 = pygame.Surface((self.target_cardw, mat_third // 2))
    self.purge2.convert()
    self.purge2_rect = self.purge2.get_rect()
    self.purge2_rect.topright = (wid, mat_third * 2)
    self.board_blits.append((self.purge2, self.purge2_rect))

    ## divider2
    self.divider2 = pygame.Surface((wid // 5, mat_third))
    self.divider2.convert()
    self.divider2.fill(COLORS["GREY"])
    self.divider2_rect = self.divider2.get_rect()
    self.divider2_rect.topright = (wid, int(mat_third * 2.5))
    self.board_blits.append((self.divider2, self.divider2_rect))

    # archive2
    self.archive2 = pygame.Surface((self.target_cardw + self.margin, mat_third))
    self.archive2.convert()
    self.archive2.fill(COLORS["BROWN"])
    self.archive2_rect = self.archive2.get_rect()
    self.archive2_rect.topright = (wid, int(mat_third * 2.5))
    self.board_blits.append((self.archive2, self.archive2_rect))

    ## divider1
    self.divider = pygame.Surface((wid // 5, mat_third))
    self.divider.convert()
    self.divider.fill(COLORS["GREEN"])
    self.divider_rect = self.divider.get_rect()
    self.divider_rect.topleft = (0, int(mat_third * 2.5))
    self.board_blits.append((self.divider, self.divider_rect))

    # archive
    self.archive1 = pygame.Surface((self.target_cardw + self.margin, mat_third))
    self.archive1.convert()
    self.archive1.fill(COLORS["BROWN"])
    self.archive1_rect = self.archive1.get_rect()
    self.archive1_rect.topleft = (0, int(mat_third * 2.5))
    self.board_blits.append((self.archive1, self.archive1_rect))

    ## active mat
    self.mat1 = pygame.Surface((wid, hei // 2))
    self.mat1.convert()
    self.mat1.fill(COLORS["BLACK"])
    self.mat1_rect = self.mat1.get_rect()
    self.mat1_rect.topleft = (0, int(mat_third * 3.5))
    self.board_blits.append((self.mat1, self.mat1_rect))

    # purged
    self.purge1 = pygame.Surface((self.target_cardw, mat_third // 2))
    self.purge1.convert()
    self.purge1_rect = self.purge1.get_rect()
    self.purge1_rect.topleft = (0, int(mat_third * 3.5))
    self.board_blits.append((self.purge1, self.purge1_rect))

    # deck
    self.deck1 = pygame.Surface((self.target_cardw, mat_third))
    self.deck1.convert()
    self.deck1.fill(COLORS["GREEN"])
    self.deck1_rect = self.deck1.get_rect()
    self.deck1_rect.topleft = (0, mat_third * 4)
    self.board_blits.append((self.deck1, self.deck1_rect))

    # creatures
    self.creatures1 = pygame.Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.creatures1.convert()
    self.creatures1.fill(COLORS["GREEN"])
    self.creatures1_rect = self.creatures1.get_rect()
    self.creatures1_rect.topright = (wid, int(mat_third * 3.5))
    self.board_blits.append((self.creatures1, self.creatures1_rect))

    # discard
    self.discard1 = pygame.Surface((self.target_cardw, mat_third))
    self.discard1.convert()
    self.discard1.fill(COLORS["GREEN"])
    self.discard1_rect = self.discard1.get_rect()
    self.discard1_rect.bottomleft = (0, HEIGHT)
    self.board_blits.append((self.discard1, self.discard1_rect))

    # artifacts
    self.artifacts1 = pygame.Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.artifacts1.convert()
    self.artifacts1.fill(COLORS["GREEN"])
    self.artifacts1_rect = self.artifacts1.get_rect()
    self.artifacts1_rect.topright = (wid, int(mat_third * 4.5))
    self.board_blits.append((self.artifacts1, self.artifacts1_rect))

    # hand
    self.hand1 = pygame.Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.hand1.convert()
    self.hand1.fill(COLORS["GREEN"])
    self.hand1_rect = self.hand1.get_rect()
    self.hand1_rect.topright = (wid, int(mat_third * 5.5))
    self.board_blits.append((self.hand1, self.hand1_rect))

    ## neutral zone - easier if we have this and can blit to it's dimensions
    self.neutral = pygame.Surface(((wid // 5) * 3, mat_third))
    self.neutral.convert()
    self.neutral.fill(COLORS["BLACK"])
    self.neutral_rect = self.neutral.get_rect()
    self.neutral_rect.topleft = (self.divider.get_width(), int(mat_third * 2.5))
    self.board_blits.append((self.neutral, self.neutral_rect))

    # end turn
    self.endText = self.OTHERFONT.render(f"  End Turn  ", 1, COLORS['WHITE'])
    self.endRect = self.endText.get_rect()
    self.endRect.centerx = wid // 2
    self.endRect.centery = hei // 2
    self.endBack = pygame.Surface((self.endText.get_width() + 10, self.endText.get_height() + 10))
    self.endBack.convert()
    self.endBack.fill(COLORS["GREEN"])
    self.endBackRect = self.endBack.get_rect()
    self.endBackRect.centerx = wid // 2
    self.endBackRect.centery = hei // 2

    self.setKeys()

    # check warning
    self.warnSurf = pygame.Surface((self.amber2.get_size()))
    self.warnSurf.fill(COLORS["RED"])
    self.warnRect = self.warnSurf.get_rect()
    self.warnRect.topleft = self.amber2_rect.topleft

    # log and other options submenu

    run = True

    while run:
      self.CLOCK.tick(self.FPS)

      for event in pygame.event.get():
        
        if event.type == pygame.MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = event.pos
          if not self.remaining or pygame.Rect.collidepoint(self.endBackRect, (self.mousex, self.mousey)):
            self.endBack.fill(COLORS["LIGHT_GREEN"])
          else:
            self.endBack.fill(COLORS["GREEN"])

        if event.type == pygame.QUIT:
          run = False

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
          self.hovercard = []
          self.draw() # this only works because of the update in doPopup
          self.doPopup()
          
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          hand = self.activePlayer.hand
          hit = [pygame.Rect.collidepoint(x.rect, (self.mousex, self.mousey)) for x in hand]
          if True in hit:
            self.dragging.append(hand.pop(hit.index(True)))
            self.dragCard()
            print("Exiting dragCard, back into events.")

        
        if event.type == MOUSEBUTTONUP and event.button == 1:
          if self.dragging:
            self.activePlayer.hand.append(self.dragging.pop())
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if pygame.Rect.collidepoint(self.endBackRect, (self.mousex, self.mousey)):
            if self.remaining:
              answer = self.chooseHouse("custom", ("Are you sure you want to end your turn?", ["Yes", "No"]))[0]
              if answer == "No":
                break
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.inactivePlayer.discard + self.activePlayer.discard + self.activePlayer.purged + self.inactivePlayer.purged + self.activePlayer.archive + self.inactivePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.turnStage += 1
          elif True in self.friendDraws and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.cardChanged()
          elif True in self.enemyDraws and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.cardChanged()
          elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          elif not self.drawFriendPurge and pygame.Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
            self.drawFriendPurge = True
          elif not self.drawEnemyPurge and pygame.Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
            self.drawEnemyPurge = True
          elif not self.drawFriendArchive and pygame.Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
            self.drawFriendArchive = True
          elif not self.drawEnemyArchive and pygame.Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
            self.drawEnemyArchive = True
          
        if event.type == pygame.KEYDOWN:
          # print(event)
          if event.key == 113 and (event.mod == 64 or event.mod == 4160):
            run = False

      # handle card hovering

      self.hovercard = []
      self.check_hover()

      ######################
      # Initial hand fill  #
      ######################

      if self.turnStage == None:
        #####################
        # Draw and mulligan #
        #####################
        if not self.do:
          logging.info(f"{self.activePlayer.name} is going first.")
          pyautogui.alert(f"\n{self.activePlayer.name} is going first.\n")
          self.activePlayer += 7
        else:
          mull = self.chooseHouse("custom", ("Player 1, would you like to keep or mulligan?", ["Keep", "Mulligan"]), ["GREEN", "RED"])[0]
          if mull == "Mulligan":
            for card in self.activePlayer.hand:
              self.activePlayer.deck.append(card)
            random.shuffle(self.activePlayer.deck)
            self.activePlayer.hand = []
            self.activePlayer += 6
        if not self.do:
          self.inactivePlayer += 6
        else:
          mull2 = self.chooseHouse("custom", ("Player 2, would you like to keep or mulligan?", ["Keep", "Mulligan"]), ["GREEN", "RED"])[0]
          if mull2 == "Mulligan":
            for card in self.inactivePlayer.hand:
              self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
          self.turnNum = 1
          self.turnStage = 0
        self.cardChanged()
        self.do = True

      ###################################
      # Step 0: "Start of turn" effects #
      ###################################

      elif self.turnStage == 0:
        # start of turn effects will go here
        self.turnStage += 1
      
      ###################################################
      # step 1: check if a key is forged, then forge it #
      ###################################################

      elif self.turnStage == 1: # forge a key
        if self.canForge(): # returns True if you can forge, false if you can't (and why you can't), which in CotA is basically only Miasma
          self.forgeKey("active", self.calculateCost())
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
        archive = self.activePlayer.archive
        self.activeHouse = self.chooseHouse("activeHouse")
        highSurf = pygame.Surface(self.house1a.get_size())
        highSurf.convert()
        highSurf.fill(COLORS["LIGHT_GREEN"])
        i = self.activePlayer.houses.index(self.activeHouse[0])
        if i == 0:
          self.highlight.append((highSurf, self.house1a_rect))
        elif i == 1:
          self.highlight.append((highSurf, self.house1b_rect))
        elif i == 2:
          self.highlight.append((highSurf, self.house1c_rect))
        self.draw(False)
        pygame.display.flip()
        if len(self.activePlayer.archive) > 0:
          show = self.chooseHouse("custom", ("Would you like to pick up your archive?", ["Yes", "No"], ["GREEN", "RED"]))
          if archive == "Yes":
            for card in archive:
              self.pendingReloc.append(archive.pop(0)) # this is in case you archive an enemy card - it needs to return to their hand
            self.pending('hand')
        self.turnStage += 1

      ###############################################################################
      # step 3: play, discard, or use cards (and also inquire about the game state) #
      ###############################################################################

      elif self.turnStage == 3:
        if self.response:
          l = len(self.response)
          if l == 1:
            self.response = self.response[0]
          elif l == 3:
            self.response, self.targetCard, self.loc = self.response
          
          if self.response == "House":
            pyautogui.alert(self.activeHouse)
          # elif self.response == "Board":
            # print(self)
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
            pyautogui.alert("There are " + str(len(self.inactivePlayer.archive)) + " cards in your opponent's archive.")
          elif self.response == "OppHouses":
            show = 'Your opponent\'s houses are:\n'
            for house in self.inactivePlayer.houses:
              show += f"{house}\n"
            pyautogui.alert(show)
          elif self.response == "Keys":
            pyautogui.alert(f"You have {self.activePlayer.amber} amber and {self.activePlayer.keys} keys. Your opponent has {self.inactivePlayer.amber} amber and {self.inactivePlayer.keys} keys.")
          elif self.response == "Card":
            cardName = pyautogui.prompt("Enter the name of a card from one of the active decks:").lower()
            for x in [deck.Deck(deck.deckName(self.first), self.target_cardw, self.target_cardh), deck.Deck(deck.deckName(self.second), self.target_cardw, self.target_cardh)]:
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
          elif self.response == "Concede":
            pyautogui.alert(f"{self.inactivePlayer.name} wins!")
            run = False
          elif self.response == "Quit":
            run = False
          
          elif self.response == "Play":
            self.playCard(self.targetCard)
          elif self.response == "Fight":
            self.fightCard(self.targetCard)
          elif self.response == "Discard":
            if len(self.playedThisTurn) + len(self.discardedThisTurn) >= 1 and self.turnNum == 1: # I shouldn't actually be able to get here I think
              pyautogui.alert("You've already taken your one action for turn one.")
            else:
              self.discardCard(self.targetCard)
          elif self.response == "Action":
            self.actionCard(self.targetCard, self.loc)
          elif self.response == "Reap":
            self.reapCard(self.targetCard)
          elif self.response == "Omni":
            self.actionCard(self.targetCard, self.loc, True)
          elif self.response == "Unstun":
            self.activePlayer.board["Creature"][self.targetCard].stun = False
            self.activePlayer.board["Creature"][self.targetCard].ready = False
            self.cardChanged()
            # self.actionCard(self.targetCard, self.loc)
          elif self.response == "Details":
            print(self.activePlayer.board[self.loc][self.targetCard])

          self.response = []
          self.targetCard = None
          self.loc = None


      ########################
      # step 4: ready cards  #
      ########################

      elif self.turnStage == 4: # ready and reset armor
        for creature in self.activePlayer.board["Creature"]:
          creature.ready = True
        for artifact in self.activePlayer.board["Artifact"]:
          artifact.ready = True
        self.turnStage += 1
      
      ######################
      # step 5: draw cards #
      ######################

      elif self.turnStage == 5: # end of turn draw and end of turn effects
        self.activePlayer.drawEOT(self)
        
        self.checkEOTStates()

        # switch players
        for creature in self.activePlayer.board["Creature"]:
          creature.eot(self, creature)
        for creature in self.inactivePlayer.board["Creature"]:
          creature.eot(self, creature)
        if self.forgedThisTurn:
          self.forgedLastTurn = self.forgedThisTurn.copy()
        else:
          self.forgedThisTurn = []
        if "stampede" in self.activePlayer.states:
          self.activePlayer.states["stampede"] = 0
        self.activeHouse = []
        self.extraFightHouses = []
        self.playedLastTurn = self.playedThisTurn.copy()
        self.playedThisTurn = []
        self.discardedLastTurn = self.discardedThisTurn.copy()
        self.discardedThisTurn = []
        self.usedLastTurn = self.usedThisTurn.copy()
        self.usedThisTurn = []
        self.remaining = True
        # print(f"States: {self.resetStates}")
        # print(f"Next states: {self.resetStatesNext}")
        if self.resetStates:
          for key in self.resetStates:
            if key[0] == "a":
              self.activePlayer.states[key[1]] = 0
            if key[0] == "i":
              self.inactivePlayer.states[key[1]] = 0
        self.resetStates = self.resetStatesNext.copy()
        self.resetStatesNext = []
        # print(f"States: {self.resetStates}")
        # print(f"Next states: {self.resetStatesNext}")
        self.endBack.fill(COLORS["GREEN"])
        if self.activePlayer.amber >= self.calculateCost():
          pyautogui.alert(f"Check for key {self.activePlayer.keys + 1}!")
          self.highlight = [(self.warnSurf, self.warnRect)]
        else:
          self.highlight = []
        self.switch()
        self.cardChanged()
        self.setKeys()
        self.turnNum += 1
        self.turnStage = 0
      
      
      self.draw() # this will need hella updates
      pygame.display.flip()

    pygame.quit()


  def check_hover (self):
    if self.dragging:
      return

    hoverable = []
    hoverable2 = []
    if sum(self.friendDraws) == 0:
      hoverable += self.activePlayer.hand + self.activePlayer.board["Creature"]  + self.activePlayer.board["Artifact"] + self.activePlayer.board["Upgrade"]
      hoverable2 += [self.discard1_rect, self.deck1_rect, self.archive1_rect, self.purge1_rect]
    if sum(self.enemyDraws) == 0:
      hoverable += self.inactivePlayer.hand + self.inactivePlayer.board["Creature"] + self.inactivePlayer.board["Artifact"] + self.inactivePlayer.board["Upgrade"]
      hoverable2 += [self.discard2_rect, self.deck2_rect, self.archive2_rect, self.purge2_rect]
    if self.drawFriendDiscard:
      hoverable += self.activePlayer.discard
    if self.drawEnemyDiscard:
      hoverable += self.inactivePlayer.discard

    for card in hoverable:
      if pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)):
        self.hovercard = [card]
        return
      if pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)):
        self.hovercard = [card]
        return

    for loc in hoverable2:
      if pygame.Rect.collidepoint(loc, (self.mousex, self.mousey)):
        self.hovercard = [loc]
        return

  def draw(self, drawEnd: bool = True):
    # self.allsprites.update()
    self.WIN.blits(self.board_blits)
    if self.highlight:
      self.WIN.blits(self.highlight)
    self.WIN.blits(self.dataBlits)
    if self.cardBlits:
      self.WIN.blits(self.cardBlits)
    
    # self.allsprites.draw(self.WIN)
    if drawEnd and self.activeHouse:
      self.WIN.blit(self.endBack, self.endBackRect)
      self.WIN.blit(self.endText, self.endRect)
    # draw discards/archive/purges
    if self.drawFriendDiscard or self.drawFriendArchive or self.drawFriendPurge:
      if self.drawFriendDiscard:
        pool = self.activePlayer.discard
      elif self.drawFriendArchive:
        pool = self.activePlayer.archive
      else:
        pool = self.activePlayer.purged
      # discard back
      discardBackSurf = pygame.Surface((self.WIN.get_width(), self.WIN.get_height() * 5 // 12))
      discardBackSurf.convert_alpha()
      discardBackSurf.set_alpha(200)
      discardBackSurf.fill(COLORS["WHITE"])
      discardBackRect = discardBackSurf.get_rect()
      discardBackRect.topleft = self.mat1_rect.topleft
      # discard close button
      closeSurf = self.OTHERFONT.render("  CLOSE  ", 1, COLORS["WHITE"])
      closeRect = closeSurf.get_rect()
      closeRect.top = self.hand1_rect.top
      closeRect.centerx = WIDTH // 2
      closeBackSurf = pygame.Surface((closeSurf.get_size()))
      closeBackSurf.convert()
      closeBackSurf.fill(COLORS["RED"])
      self.closeFriendDiscard = closeBackSurf.get_rect()
      self.closeFriendDiscard.top = closeRect.top
      self.closeFriendDiscard.centerx = WIDTH // 2
      self.WIN.blit(discardBackSurf, discardBackRect)
      self.WIN.blit(closeBackSurf, self.closeFriendDiscard)
      self.WIN.blit(closeSurf, closeRect)
      # draw cards
      x = 0
      for card in pool[0:16]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + self.margin)
        x += 1
        self.WIN.blit(card.image, card.rect)
      x = 0
      for card in pool[16:]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 2 * self.margin + self.target_cardh)
        x += 1
        self.WIN.blit(card.image, card.rect)
    if self.drawEnemyDiscard or self.drawEnemyArchive or self.drawEnemyPurge:
      if self.drawEnemyDiscard:
        pool = self.inactivePlayer.discard
      elif self.drawEnemyArchive:
        pool = self.inactivePlayer.archive
      else:
        pool = self.inactivePlayer.purged
      # discard back
      discardBackSurf = pygame.Surface((self.WIN.get_width(), self.WIN.get_height() * 5 // 12))
      discardBackSurf.convert_alpha()
      discardBackSurf.set_alpha(200)
      discardBackSurf.fill(COLORS["WHITE"])
      discardBackRect = discardBackSurf.get_rect()
      discardBackRect.topleft = (0, 0)
      # discard close button
      closeSurf = self.OTHERFONT.render("  CLOSE  ", 1, COLORS["WHITE"])
      closeRect = closeSurf.get_rect()
      closeRect.centery = self.creatures2_rect[1] + (self.creatures2_rect[3] // 2)
      closeRect.centerx = WIDTH // 2
      closeBackSurf = pygame.Surface((closeSurf.get_size()))
      closeBackSurf.convert()
      closeBackSurf.fill(COLORS["RED"])
      self.closeEnemyDiscard = closeBackSurf.get_rect()
      self.closeEnemyDiscard.top = closeRect.top
      self.closeEnemyDiscard.centerx = WIDTH // 2
      self.WIN.blit(discardBackSurf, discardBackRect)
      self.WIN.blit(closeBackSurf, self.closeEnemyDiscard)
      self.WIN.blit(closeSurf, closeRect)
      # draw cards
      x = 0
      for card in pool[0:16]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + self.margin)
        x += 1
        self.WIN.blit(card.image, card.rect)
      x = 0
      for card in pool[16:]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 2 * self.margin + self.target_cardh)
        x += 1
        self.WIN.blit(card.image, card.rect)
    if self.extraDraws:
      for pair in self.extraDraws:
        self.WIN.blit(pair[0], pair[1])
    if self.hovercard:
      hover = self.hovercard[0]
      if type(hover) != pygame.Rect:
        hover, hover_rect = hover.orig_image, hover.orig_rect
        if self.mousey > HEIGHT / 2:
          hover_rect.top = self.mousey - CARDH
          while hover_rect.top < 0:
            hover_rect.top += 10
        else:
          hover_rect.top = self.mousey
          while hover_rect.bottom > HEIGHT:
            hover_rect.bottom -= 10
        if self.mousex > WIDTH / 2:
          hover_rect.left = self.mousex - CARDW
        else:
          hover_rect.left = self.mousex
      else:
        if hover == self.purge1_rect:
          hover = self.SMALLFONT.render(f"{len(self.activePlayer.purged)} of your cards have been purged.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomleft = (self.mousex, self.mousey)
        elif hover == self.purge2_rect:
          hover = self.SMALLFONT.render(f"{len(self.inactivePlayer.purged)} of your opponent's cards have been purged.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomright = (self.mousex, self.mousey)
        elif hover == self.discard1_rect:
          hover = self.SMALLFONT.render(f"There are {len(self.activePlayer.discard)} cards in your discard.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomleft = (self.mousex, self.mousey)
        elif hover == self.discard2_rect:
          hover = self.SMALLFONT.render(f"There are {len(self.inactivePlayer.discard)} cards in your opponent's discard.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomright = (self.mousex, self.mousey)
        elif hover == self.deck1_rect:
          hover = self.SMALLFONT.render(f"There are {len(self.activePlayer.deck)} cards in your deck.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomleft = (self.mousex, self.mousey)
        elif hover == self.deck2_rect:
          hover = self.SMALLFONT.render(f"There are {len(self.inactivePlayer.deck)} cards in your opponent's deck.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomright = (self.mousex, self.mousey)
        elif hover == self.archive1_rect:
          hover = self.SMALLFONT.render(f"There are {len(self.activePlayer.archive)} cards in your archive.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomleft = (self.mousex, self.mousey)
        elif hover == self.archive2_rect:
          hover = self.SMALLFONT.render(f"There are {len(self.inactivePlayer.archive)} cards in your opponent's archive.", 1, COLORS["BLACK"])
          hover_rect = hover.get_rect()
          hover_rect.bottomright = (self.mousex, self.mousey)
        hover_back = pygame.Surface(hover.get_size())
        hover_back.fill(COLORS["WHITE"])
        hover_back_rect = hover_back.get_rect()
        hover_back_rect.topleft = hover_rect.topleft
        self.WIN.blit(hover_back, hover_back_rect)
      self.WIN.blit(hover, hover_rect)
    if self.dragging:
      drag = self.dragging[0]
      self.WIN.blit(drag.image, (self.mousex, self.mousey))

  def doPopup(self):
    pos = pygame.mouse.get_pos()
    board = False
    loc = 0
    while True:
      in_hand = [pygame.Rect.collidepoint(x.rect, pos) for x in self.activePlayer.hand]
      in_creature = [(pygame.Rect.collidepoint(x.rect, pos) or pygame.Rect.collidepoint(x.tapped_rect, pos)) for x in self.activePlayer.board["Creature"]]
      in_artifact = [(pygame.Rect.collidepoint(x.rect, pos) or pygame.Rect.collidepoint(x.tapped_rect, pos)) for x in self.activePlayer.board["Artifact"]]
      if True in in_hand: # check for collisions with a card: action options from clicking on a card
        card_pos = in_hand.index(True)
        opt = self.handOptions(card_pos)
        loc = "hand"
      elif True in in_creature:
        card_pos = in_creature.index(True)
        loc = "Creature"
        opt = self.cardOptions(card_pos, loc)
      elif True in in_artifact:
        card_pos = in_artifact.index(True)
        loc = "Artifact"
        opt = self.cardOptions(card_pos, loc)
      else: # action options from clicking not on a card: then check for a collision with a mat
        opt = self.turnOptions()
        board = True
      self.make_popup(opt, pos)
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          OPTION = self.option_selected(opt, pos)
          if OPTION != None:
            if board:
              self.response = [OPTION]
            else:
              self.response = [OPTION, card_pos, loc]
            self.extraDraws = []
            return OPTION
          else:
            self.extraDraws = []
            return None
      self.CLOCK.tick(self.FPS)
      # self.draw()
  

  def option_selected(self, options, pos):
    w = max(x.get_width()+self.margin for x in [self.BASICFONT.render(y, 1, COLORS['BLUE']) for y in options])
    bot_offset = right_offset = 0
    popupSurf = pygame.Surface((w, pygame.font.Font.get_linesize(self.BASICFONT)*len(options)))
    popupSurf.convert()
    popupRect = popupSurf.get_rect()
    popupRect.centerx = pos[0] + w//2
    popupRect.centery = pos[1] + (pygame.font.Font.get_linesize(self.BASICFONT)*len(options))/2
    while popupRect.bottom > HEIGHT:
      popupRect.bottom -= 10
      bot_offset += 10
    while popupRect.right > WIDTH:
      popupRect.right -= 10
      right_offset += 10
    #draw up the surf, but don't blit it to the screen
    top = pos[1]
    for i in range(len(options)):
      textSurf = self.BASICFONT.render(options[i], 1, COLORS['BLUE'])
      textRect = textSurf.get_rect()
      textRect.top = top - bot_offset
      textRect.left = pos[0] - right_offset
      top += pygame.font.Font.get_linesize(self.BASICFONT)
      popupSurf.blit(textSurf, textRect)
      if pygame.Rect.collidepoint(textRect, (self.mousex, self.mousey)):
        # print(options)
        return options[i]


  def make_popup(self, options, pos):
    w = max(x.get_width()+self.margin for x in [self.BASICFONT.render(y, 1, COLORS['BLUE']) for y in options])
    bot_offset = right_offset = 0
    popupSurf = pygame.Surface((w, pygame.font.Font.get_linesize(self.BASICFONT)*len(options)))
    popupSurf.fill(COLORS["BLACK"])
    top = pos[1]
    popupRect = popupSurf.get_rect()
    popupRect.centerx = pos[0] + w // 2
    popupRect.centery = pos[1] + (pygame.font.Font.get_linesize(self.BASICFONT)*len(options))/2
    while popupRect.bottom > HEIGHT:
      popupRect.bottom -= 10
      bot_offset += 10
    while popupRect.right > WIDTH:
      popupRect.right -= 10
      right_offset += 10
    self.WIN.blit(popupSurf, popupRect)
    for i in range(len(options)):
      textSurf = self.BASICFONT.render(options[i], 1, COLORS["YELLOW"])
      textRect = textSurf.get_rect()
      textRect.top = top - bot_offset
      textRect.left = pos[0] - right_offset
      top += pygame.font.Font.get_linesize(self.BASICFONT)
      self.WIN.blit(textSurf, textRect)
    pygame.display.update()


  def switch(self):
    """ Swaps active and inactive players.
    """
    self.activePlayer, self.inactivePlayer = self.inactivePlayer, self.activePlayer

  def setKeys(self):
    """ Sets the keys at the beginning of the game and swaps them each round.
    """
    if self.inactivePlayer.yellow:
      print("Yellow key is forged.")
      self.key2y, self.key2y_rect = self.inactivePlayer.key_forged
    else:
      self.key2y, self.key2y_rect = self.inactivePlayer.key_y
    self.key2y_rect.topright = (WIDTH - (2 + self.target_cardw + self.margin), self.divider2_rect.top)
    
    if self.inactivePlayer.red:
      print("Red key is forged.")
      self.key2r, self.key2r_rect = self.inactivePlayer.key_forged
    else:
      self.key2r, self.key2r_rect = self.inactivePlayer.key_r
    self.key2r_rect.midright = (WIDTH - (2 + self.target_cardw + self.margin), self.divider2_rect.centery)
    
    if self.inactivePlayer.blue:
      print("Blue key is forged.")
      self.key2b, self.key2b_rect = self.inactivePlayer.key_forged
    else:
      self.key2b, self.key2b_rect = self.inactivePlayer.key_b
    self.key2b_rect.bottomright = (WIDTH - (2 + self.target_cardw + self.margin), self.divider2_rect.bottom)

    self.house2a, self.house2a_rect = self.inactivePlayer.house1
    self.house2a_rect.topleft = self.divider2_rect.topleft
    self.house2b, self.house2b_rect = self.inactivePlayer.house2
    self.house2b_rect.midleft = self.divider2_rect.midleft
    self.house2c, self.house2c_rect = self.inactivePlayer.house3
    self.house2c_rect.bottomleft = self.divider2_rect.bottomleft

    if self.activePlayer.yellow:
      print("Yellow key is forged.")
      self.key1y, self.key1y_rect = self.activePlayer.key_forged
    else:
      self.key1y, self.key1y_rect = self.activePlayer.key_y
    self.key1y_rect.topleft = (2 + self.target_cardw + self.margin, self.divider_rect.top)

    if self.activePlayer.red:
      print("Red key is forged.")
      self.key1r, self.key1r_rect = self.activePlayer.key_forged
    else:
      self.key1r, self.key1r_rect = self.activePlayer.key_r
    self.key1r_rect.midleft = (2 + self.target_cardw + self.margin, self.divider_rect.centery)
    
    if self.activePlayer.blue:
      print("Blue key is forged.")
      self.key1b, self.key1b_rect = self.activePlayer.key_forged
    else:
      self.key1b, self.key1b_rect = self.activePlayer.key_b
    self.key1b_rect.bottomleft = (2 + self.target_cardw + self.margin, self.divider_rect.bottom)

    self.house1a, self.house1a_rect = self.activePlayer.house1
    self.house1a_rect.topright = self.divider_rect.topright
    self.house1b, self.house1b_rect = self.activePlayer.house2
    self.house1b_rect.midright = self.divider_rect.midright
    self.house1c, self.house1c_rect = self.activePlayer.house3
    self.house1c_rect.bottomright = self.divider_rect.bottomright

    # amber
    self.amber1 = self.BASICFONT.render(f"{self.activePlayer.amber} amber", 1, COLORS['WHITE'])
    self.amber1_rect = self.amber1.get_rect()
    self.amber1_rect.topleft = (2 + self.target_cardw + 10 + self.key1y.get_width(), self.mat2_rect[1] + self.mat2_rect[3] + (3 * self.margin))

    # chains
    self.chains1 = self.BASICFONT.render(f"{self.activePlayer.chains} chains", 1, COLORS['WHITE'])
    self.chains1_rect = self.chains1.get_rect()
    self.chains1_rect.bottomleft = (2 + self.target_cardw + 10 + self.key1y.get_width(), self.mat1_rect[1] - (3 * self.margin))
   
    # amber
    self.amber2 = self.BASICFONT.render(f"{self.inactivePlayer.amber} amber", 1, COLORS['BLACK'])
    self.amber2_rect = self.amber2.get_rect()
    self.amber2_rect.topright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key1y.get_width(), self.mat2_rect[1] + self.mat2_rect[3] + (3 * self.margin))

    # chains
    self.chains2 = self.BASICFONT.render(f"{self.inactivePlayer.chains} chains", 1, COLORS['BLACK'])
    self.chains2_rect = self.chains2.get_rect()
    self.chains2_rect.bottomright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key1y.get_width(), self.mat1_rect[1] - (3 * self.margin))

    self.dataBlits = [(self.key1y, self.key1y_rect), (self.key1r, self.key1r_rect), (self.key1b, self.key1b_rect), (self.key2y, self.key2y_rect), (self.key2r, self.key2r_rect), (self.key2b, self.key2b_rect), (self.house2a, self.house2a_rect), (self.house2b, self.house2b_rect), (self.house2c, self.house2c_rect), (self.house1a, self.house1a_rect), (self.house1b, self.house1b_rect), (self.house1c, self.house1c_rect), (self.amber1, self.amber1_rect), (self.amber2, self.amber2_rect), (self.chains1, self.chains1_rect), (self.chains2, self.chains2_rect)]
  
  def calculateCost(self):
    """ Calculates the cost of a key considering current board state.
    """
    if True: # check if things that affect cost are even in any decks
      pass # return cost
    
    # Things to check: That annoying Dis artifact, Murmook, Grabber Jammer, that Mars upgrade, Titan Mechanic
    # Need to add a tag for affecting amber cost.
    cost = 6
    return cost


############################
# State Checking Functions #
############################

  def checkEOTStates(self):
    """ Checks for end of turn effects, and resets things that need to be reset.
    """
    # Check for Scout, and unskirmish those minions
    if "scout" in self.activePlayer.states and self.activePlayer.states["scout"] > 0:
      for x in self.activePlayer.board["Creature"]:
        if "Skirmish" in x.text: x.skirmish = True
        else: x.skirmish = False

  def canForge(self):
    """ Checks if there is anything in Deck.states["Forge"]. This isn't checking if you have enough amber.
    """
    if "miasma" in self.inactivePlayer.states and self.inactivePlayer.states["miasma"]:
      pyautogui.alert("You skip your forge a key step this turn because your opponent played 'Miasma' last turn.")
      self.activePlayer.states["miasma"] = 0
      return False
    if "the_sting" in [x.title for x in self.activePlayer.board["Artifact"]]:
      pyautogui.alert("You skip your forge a key step this turn because you have 'The Sting' in play.")
      return False
    return True
    

##################
# Card functions #
##################

  def actionCard(self, cardNum: int, loc: str, omni: bool = False, cheat: bool = False):
    """ Trigger a card's action from within the turn.
    """
    card = self.activePlayer.board[loc][cardNum]
    if not self.canAction(card, r_click=True, cheat=cheat):
      pyautogui.alert(f"{card.title} can't use action right now")
      return
    if card.type == "Creature" and card.stun:
      pyautogui.alert("Creature is stunned and unable to act. Unstunning creature instead.")
      card.stun = False
      card.ready = False
      self.usedThisTurn.append(card)
      self.cardChanged()
      return
    # Trigger action
    if card.action:
      try:
        card.action(self, card)
        # act.action(self, act)
      except:
        pyautogui.alert("Action failed.")
    elif card.omni:
      try:
        card.omni(self, card)
      except:
        pyautogui.alert("Omni failed.")
    card.ready = False
    if card not in self.usedThisTurn:
      self.usedThisTurn.append(card)
    self.cardChanged()
  
  def discardCard(self, cardNum: int, cheat: bool = False):
    """ Discard a card from hand, within the turn. Doesn't need to use pending for discards, but does use it for Rock-Hurling Giant.
    """
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    card = self.activePlayer.hand[cardNum]
    if self.pendingReloc:
      pending = []
    else:
      pending = self.pendingReloc
    if card.house in self.activeHouse or cheat:
      self.activePlayer.discard.append(self.activePlayer.hand.pop(cardNum))
      self.cardChanged()
      if "rock_hurling_giant" in [x.title for x in active] and card.house == "Brobnar":
        targeting = self.chooseCards("Creature", "Deal 4 damage to:")[0]
        if targeting[0] == "fr":
          target = active[targeting[1]]
          target.damageCalc(self, 4)
          target.updateHealth(self.activePlayer)
        else:
          target = inactive[targeting[1]]
          target.damageCalc(self, 4)
          target.updateHealth(self.inactivePlayer)
        if target.destroyed:
          pending.append(target)
        self.pending()
      self.discardedThisTurn.append(card)
    else:
      pyautogui.alert("You can only discard cards of the active house.")
    self.cardChanged()


  def fightCard(self, attacker: int, cheat: bool = True, defender = None):
    """ This is needed for cards that trigger fights (eg anger, gauntlet of command). If attacker is fed in to the function (which will only be done by cards that trigger fights), the house check is skipped.
    """
    # This will actually probably need to be incorporated into the main loop in some way
    card = self.activePlayer.board["Creature"][attacker]
    # this check is also in cardOptions, but sometimes things let you trigger a fight other ways
    if len(self.inactivePlayer.board["Creature"]) == 0:
      pyautogui.alert("Your opponent has no creatures for you to attack. Fight canceled.")
      return self
    if not self.canFight(card, cheat=cheat, r_click = True):
      pyautogui.alert("This card can't fight right now.")
    if card.stun:
      pyautogui.alert("Creature is stunned and unable to fight. Unstunning creature instead.")
      card.stun = False
      card.ready = False
      self.usedThisTurn.append(card)
      self.cardChanged()
      return
    if defender == None:
      if card.title != "niffle_ape":
        defender = self.chooseCards("Creature", "Choose an enemy creature to attack:", "enemy", condition = lambda x: x.taunt or not (True in [y.taunt for y in x.neighbors(self)]), con_message = "This minion is protected by taunt.")[0][1]
      else:
        defender = self.chooseCards("Creature", "Choose an enemy minion to attack:", "enemy")[0][1]
    if defender == None:
      return
    defenderCard = self.inactivePlayer.board["Creature"][defender]
    try:
      print("Trying to fight.")
      card.fightCard(defenderCard, self)
    except: print("Fight failed.")
    if card not in self.usedThisTurn:
      self.usedThisTurn.append(card)
    self.cardChanged()

  def playCard(self, chosen: int, cheat: str = "Hand", flank = "Right", ask = True):
    """ This is needed for cards that play other cards (eg wild wormhole). Will also simplify responses. Booly is a boolean that tells whether or not to check if the house matches.
    """
    print(f"numPlays: {len(self.playedThisTurn)}")
    if cheat == "Deck":
      source = self.activePlayer.deck
    elif cheat == "Discard":
      source = self.activePlayer.discard
    else:
      source = self.activePlayer.hand
    card = source[chosen]
    if not self.canPlay(card, message = True):
      return
    # cardOptions() makes sure that you can't try to play a card you're not allowed to play
    # canPlay() does the same for drag and drop and cheating out cards
    # Increases amber, adds the card to the action section of the board, then calls the card's play function
    if card.amber > 0:
      self.activePlayer.gainAmber(card.amber, self)
      pyautogui.alert(f"{source[chosen].title} gave you {str(card.amber)} amber. You now have {str(self.activePlayer.amber)} amber.\n\nChange to a log when you fix the amber display issue.""")
    if ask:
      if card.type == "Creature" and len(self.activePlayer.board["Creature"]) > 0:
        flank = self.chooseFlank(card)
    # left flank
    if card.type != "Upgrade" and flank == "Left":
      self.activePlayer.board[card.type].insert(0, source.pop(chosen))
      print(f"numPlays: {len(self.playedThisTurn)}") # test line
    # default case: right flank
    elif card.type != "Upgrade":
      print(card.type)
      self.activePlayer.board[card.type].append(source.pop(chosen))
      print(f"numPlays: {len(self.playedThisTurn)}") # test line
    else:
      print("Choose a creature to play this upgrade on: ")
      targeted = self.chooseCards("Creature", "Choose a creature to attach the upgrade to:")[0]
      self.playUpgrade(card, targeted)
      self.cardChanged()
      return
    #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
    self.playedThisTurn.append(card)
    self.cardChanged()
    self.draw()
    pygame.display.update()
    card.play(self, card)
    print(f"numPlays: {len(self.playedThisTurn)}")
    # if the card is an action, now add it to the discard pile
    if card.type == "Action":
      if card.title == "library_access":
        self.activePlayer.purged.append(self.activePlayer.board["Action"].pop())
      else:
        self.activePlayer.discard.append(self.activePlayer.board["Action"].pop())
    self.cardChanged()

  def reapCard(self, cardNum: int, cheat:bool = False):
    """ Triggers a card's reap effect from within the turn.
    """
    card = self.activePlayer.board["Creature"][cardNum]
    # check reap states when building cardOptions
    if not self.canReap(card, r_click = True, cheat=cheat):
      # pyautogui.alert("{card.title} can't reap right now.")
      return
    if card.stun:
      pyautogui.alert("Creature is stunned and unable to reap. Unstunning creature instead.")
      card.stun = False
      card.ready = False
      self.usedThisTurn.append(card)
      self.cardChanged()
      return
    card.reap(self, card)
    # reaper.ready = False # commented out for testing
    if card not in self.usedThisTurn:
      self.usedThisTurn.append(card)
    self.cardChanged()

  def forgeKey(self, player: str, cost: int):
    if player == "active":
      forger = self.activePlayer
      other = self.inactivePlayer
    else:
      forger = self.inactivePlayer
      other = self.activePlayer
    if forger.amber >= cost:
      keys = [] #["Blue", "Red", "Yellow"]
      colors = []
      if not forger.blue:
        keys.append("Blue")
        colors.append("BLUE")
      if not forger.yellow:
        keys.append("Yellow")
        colors.append("YELLOW")
      if not forger.red:
        keys.append("Red")
        colors.append("RED")
      forged = self.chooseHouse("custom", ("Which key would you like to forge?", keys), colors)[0]
      forger.amber -= cost
      forger.keys += 1
      if forged == "Yellow":
        forger.yellow = True
      if forged == "Blue":
        forger.blue = True
      if forged == "Red":
        forger.red = True
      self.setKeys()
      if player == "active" and "interdimensional_graft" in other.states and other.states["interdimensional_graft"] and forger.amber > 0:
        pyautogui.alert(f"Your opponent played 'Interdimensional Graft' last turn, so they gain your {forger.amber} leftover amber.")
        # can't use play.stealAmber b/c this isn't technically stealing so Vaultkeeper shouldn't be able to stop it
        other.gainAmber(forger.amber, self) # setKeys is called in here
        forger.amber = 0
        pyautogui.alert(f"They now have {other.amber} amber.")
      if "bilgum_avalanche" in [x.title for x in forger.board["Creature"]]:
        # deal two damage to each enemy creature. I don't remember how I set this up to work
        length = len(other.board["Creature"])
        for x in range(1, length+1):
          card = other.board["Creature"][length-x]
          card.damageCalc(self, 2)
          card.updateHealth(self.inactivePlayer)
          if card.destroyed:
            self.pendingReloc.append(card) # this trigger shouldn't end up nested, though it could create a nest
        self.pending()
      pyautogui.alert(f"{forger.name} now has {forger.keys} keys and {forger.amber} amber.")
      if player == "active":
        self.forgedThisTurn.append(forged)

  def cardChanged(self):
    """ I don't think this function cares what the played card was. It will be called after a card is played/used, and it will do two things: (1) update self.cardBlits and (2) update what color the endTurn button is (by calling the function that actually checks this). The real question is where to call this from.
    """
    
    # check if tireless_crocag should still be alive
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    if len(inactive) == 0 and "tireless_crocag" in [x.title for x in active]:
      for card in active[::-1]:
        if card.title == "tireless_crocag":
          destroy(card, self.activePlayer, self)
    if len(active) == 0 and "tireless_crocag" in [x.title for x in inactive]:
      for card in inactive[::-1]:
        if card.title == "tireless_crocag":
          destroy(card, self.inactivePlayer, self)
    if self.pendingReloc:
      self.pending()
      
    self.cardBlits = []
    for board,area in [(self.activePlayer.board["Creature"], self.creatures1_rect), (self.inactivePlayer.board["Creature"], self.creatures2_rect), (self.activePlayer.board["Artifact"], self.artifacts1_rect), (self.inactivePlayer.board["Artifact"], self.artifacts2_rect)]:
      x = 0
      offset = ((area[0] + area[2]) // 2) - ((len(board) * self.target_cardh) // 2)
      for card in board:
        if card.ready:
          card_image, card_rect = card.image, card.rect
          card.tapped_rect.topleft = (-500, -500)
        else:
          card_image, card_rect = card.tapped, card.tapped_rect
          card.rect.topleft = (-500, -500)
        card_rect.topleft = (offset + (x * self.target_cardh) + self.margin * (x + 1), area.top)
        if card in self.activePlayer.board["Creature"] and not card.taunt:
          card_rect.bottom = area[1] + area[3] - self.margin
        if card in self.inactivePlayer.board["Creature"] and card.taunt:
          card_rect.bottom = area[1] + area[3] - self.margin
        x += 1
        if card.upgrade:
          y = len(card.upgrade)
          for up in card.upgrade:
            up_image, up_rect = up.image, up.rect
            up.tapped_rect.topleft = (-500, -500)
            up_rect.left = card_rect.left - (3 * y * self.margin)
            up_rect.bottom = card_rect.bottom
            self.cardBlits.append((up_image, up_rect))
            y -= 1
        self.cardBlits.append((card_image, card_rect))
    # card areas
    for board,area in [(self.activePlayer.hand, self.hand1_rect), (self.inactivePlayer.hand, self.hand2_rect)]:
      x = 0
      for card in board:
        card_image, card_rect = card.image, card.rect
        card.tapped_rect.topleft = (-500, -500)
        card_rect.topleft = (area.left + (x * self.target_cardw) + self.margin * (x + 1), area.top)
        x += 1
        self.cardBlits.append((card_image, card_rect))
    # discards
    l = len(self.activePlayer.discard)
    if l > 0:
      card_image, card_rect = self.activePlayer.discard[l - 1].image, self.activePlayer.discard[l - 1].rect
      card_rect.topleft = (self.discard1_rect.left, self.discard1_rect.top)
      self.cardBlits.append((card_image, card_rect))
    l = len(self.inactivePlayer.discard)
    if l > 0: 
      card_image, card_rect = self.inactivePlayer.discard[l - 1].image, self.inactivePlayer.discard[l - 1].rect
      card_rect.topleft = (self.discard2_rect.left, self.discard2_rect.top)
      self.cardBlits.append((card_image, card_rect))
    # archive
    l = len(self.activePlayer.archive)
    if l > 0:
      card_image, card_rect = self.activePlayer.archive[l - 1].image, self.activePlayer.archive[l - 1].rect
      card_rect.center = self.archive1_rect.center
      self.cardBlits.append((card_image, card_rect))
    l = len(self.inactivePlayer.archive)
    if l > 0: 
      card_image, card_rect = self.inactivePlayer.archive[l - 1].image, self.inactivePlayer.archive[l - 1].rect
      card_rect.center = self.archive2_rect.center
      self.cardBlits.append((card_image, card_rect))
    # decks
    # going to need a card back of some sort to put here
    l = len(self.activePlayer.deck)
    if l > 0:
      card_image, card_rect = self.activePlayer.deck[-1].image, self.activePlayer.deck[-1].rect
      card_rect.topleft = (self.deck1_rect.left, self.deck1_rect.top)
      self.cardBlits.append((card_image, card_rect))
    l = len(self.inactivePlayer.deck)
    if l > 0:
      card_image, card_rect = self.inactivePlayer.deck[-1].image, self.inactivePlayer.deck[-1].rect
      card_rect.topleft = (self.deck2_rect.left, self.deck2_rect.top)
      self.cardBlits.append((card_image, card_rect))
    
    if self.activeHouse:
      self.playsRemaining()
    
  def playsRemaining(self):
    # now, check if we should change the fill on endTurn
    if True not in [self.canPlay(c, reset = False) for c in self.activePlayer.hand if c.type] + [self.canDiscard(c, reset = False) for c in self.activePlayer.hand if c.type]:
      if True not in [self.canAction(c, reset = False) for c in self.activePlayer.board["Creature"]] + [self.canFight(c, reset = False) for c in self.activePlayer.board["Creature"]] + [self.canReap(c, reset = False) for c in self.activePlayer.board["Creature"]]:
        if True not in [self.canAction(c, reset = False) for c in self.activePlayer.board["Artifact"]]:
          print("Nothing left to do!")
          self.endBack.fill(COLORS["LIGHT_GREEN"])
          self.remaining = False
          return
    print("There's stuff left to do.")
    self.remaining = True
    

  def previewHouse(self, house: str) -> List[Tuple[pygame.Surface, pygame.Rect]]:
    """ Highlights the cards in the selected house during the choose house step.
    """
    retVal = []

    selectedSurf = pygame.Surface((self.target_cardw, self.target_cardh))
    selectedSurf.convert_alpha()
    selectedSurf.set_alpha(80)
    selectedSurf.fill(COLORS["LIGHT_GREEN"])

    selectedSurfTapped = pygame.Surface((self.target_cardh, self.target_cardw))
    selectedSurfTapped.convert_alpha()
    selectedSurfTapped.set_alpha(80)
    selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])

    for card in self.activePlayer.board["Creature"] + self.activePlayer.board["Artifact"]:
      if card.house == house:
        if card.ready:
          retVal.append((selectedSurf, card.rect))
        else:
          retVal.append((selectedSurfTapped, card.tapped_rect))
    for card in self.activePlayer.hand:
      if card.house == house:
        retVal.append((selectedSurf, card.rect))
    
    return retVal

  def pending(self, destination = "discard", secondary: List = [], target = None):
    """ Pending is the function that handles when multiple cards leave play at the same time, whether it be to hand or to discard. It will trigger leaves play and destroyed effects. Allowable options for dest are 'purge', 'discard', 'hand', 'deck', 'archive'.
    """
    active = self.activePlayer.board
    inactive = self.inactivePlayer.board
    if secondary:
      L = secondary # this is for handling if destruction triggers another destruction
    else:
      L = self.pendingReloc

    if not L:
      self.cardChanged()
      return # just in case we feed it an empty list
    # at this point I would let them order the destroyed triggers - draw the pending destroyed cards and use chooseCards to pick them one at a time, but I won't implement that yet
    for card in L[::-1]:
      if card.destroyed:
        # here will be all the stuff I was going to put in basicDest
        # loot the bodies
        # return captured amber if a creature, don't if an artifact
        # handle upgrades
        card.dest(self, card) # some card.dests will put the card into a different zone, arma_cloak won't though (I think)
        card.reset()
        if "armageddon_cloak" in [x.title for x in card.upgrade]:
          L.remove(card)
        destroyed = True
      else:
        # so these cards are probably leaving play, so we need to do the basic leaves play stuff (though not always, need to figure out the triggers for that)
        # I could build these things into reset, which means I wouldn't write functions for leaves play, stuff, I'd just catch it in reset
        card.reset()
    if destination not in ['purge', 'discard', 'hand', 'deck', 'archive', 'annihilate']:
      pyautogui.alert("Pending was given an invalid destination.")
      self.cardChanged()
      return
    if destination == "purge":
      for card in L[::-1]:
        if card.deck == self.activePlayer.name:
          self.activePlayer.purge.append(card)
        else:
          self.inactivePlayer.purge.append(card)
        L.remove(card)
    
    # here is where we'd want to let them make choices about order, b/c choosing order of destroyed triggers and order of things entering discard is different - so they set the order here, and then it goes to resolve
    
    # some code here that will lead to L being reordered - it will show both boards at the same time, but build one list

    # if we let them choose which one will go in first, and append the rest, we won't need to reverse the list as we already do that as part of the process
    
    # if destination == "annihilate": # we'll do this one first to remove all creatures (b/c annihilation ritual only affects creatures)

    # if we do this right, we shouldn't end up in a situation where we have some cards that were destroyed in this list and some that weren't (this is dependent on making sure dest effects only add to pendingReloc if it's empty)

    elif destination == "discard":
      for card in L[::-1]:
        if card.deck == self.activePlayer.name:
          if "annihilation_ritual" in ([x.title for x in active["Artifact"]] + [x.title for x in inactive["Artifact"]]) and card.type == "Creature" and destroyed == True:
            self.activePlayer.discard.append(card)
          else:
            self.activePlayer.discard.append(card)
        else:
          if "annihilation_ritual" in ([x.title for x in active["Artifact"]] + [x.title for x in inactive["Artifact"]]) and card.type == "Creature" and destroyed == True:
            self.inactivePlayer.purge.append(card)
          else:
            self.inactivePlayer.discard.append(card)
        L.remove(card)
    elif destination == "hand":
      for card in L[::-1]:
        if card.deck == self.activePlayer.name:
          for up in card.upgrade:
            if up.deck == self.activePlayer.name:
              self.activePlayer.discard.append(up)
            else:
              self.inactivePlayer.discard.append(up)
          self.activePlayer.hand.append(card)
        else:
          for up in card.upgrade:
            if up.deck == self.inactivePlayer.name:
              self.activePlayer.discard.append(up)
            else:
              self.inactivePlayer.discard.append(up)
          self.inactivePlayer.hand.append(card)
        card.reset()
        card.reveal = True
        L.remove(card)
      # I think it would be confusing if I sorted the hand, at this point they will have chosen the order of L so things should be returned to their hand in that order
      # self.activePlayer.hand.sort(key = lambda x: x.house)
      # self.inactivePlayer.hand.sort(key = lambda x: x.house)
    elif destination == "deck":
      for card in L[::-1]:
        if card.name == self.activePlayer.name:
          self.activePlayer.deck.append(card)
        else:
          self.inactivePlayer.deck.append(card)
        card.reset()
        card.reveal = True
        L.remove(card)
    elif destination == "archive":
      if target == None:
        raise ValueError("'archive' given as argument to pending() without a target player.")
      for card in L[::-1]:
        # this is where we use target
        target.archive.append(card)
    # check that the list was emptied
    if L:
      pyautogui.alert("Pending did not properly empty the list.")
    self.cardChanged()


  def canPlay(self, card, reset: bool = True, message: bool = False, cheat: bool = False):
    if len(self.playedThisTurn) >= 1 and self.turnNum == 1 and "wild_wormhole" not in [x.title for x in self.activePlayer.board["Action"]]:
      if message: pyautogui.alert("You cannot play more than one card on your first turn.")
      return False
    if "ember_imp" in [x.title for x in self.inactivePlayer.board["Creature"]] and len(self.playedThisTurn) >= 2: #
      if message: pyautogui.alert("'Ember Imp' prevents playing this")
      return False
    if "treasure_map" in self.activePlayer.states and self.activePlayer.states["treasure_map"]:
      pyautogui.alert("'Treasure Map' prevents playing more cards this turn")
      return False
    if "wild_wormhole" in [x.title for x in self.activePlayer.board["Action"]]:
      if card.type == "Action":
        if "scrambler_storm" in self.inactivePlayer.states and self.inactivePlayer.states["scrambler_storm"]:
          if message: pyautogui.alert("'Scrambler Storm' prevents playing actions this turn, so you can't cheat this card out.")
          return False
      elif card.type == "Creature":
        if card.title == "kelifi_dragon" and self.activePlayer.amber < 7:
          if message: pyautogui.alert("You need 7 amber to play 'Kelifi Dragon'")
          return False
        if card.title == "truebaru" and self.activePlayer.amber < 3:
          if message: pyautogui.alert("You must have 3 amber to sacrifice in order to play 'Truebaru'")
          return False
        if "grommid" in [x.title for x in self.activePlayer.board["Creature"]]:
          if message: pyautogui.alert("You can't play creatures with 'Grommid' in play")
          return False
        if "lifeward" in self.inactivePlayer.states and self.inactivePlayer.states["lifeward"]:
          if message: pyautogui.alert("You can't play creatures because of 'Lifeward'")
          return False
      if card.house not in self.activeHouse:
        return True
    if card.type == "Upgrade" and len(self.activePlayer.board["Creature"]) == 0 and len(self.inactivePlayer.board["Creature"]) == 0:
      if message: pyautogui.alert("No valid targets for this upgrade.")
      return False
    if (card.house not in self.activeHouse and card.house != "Logos") and ("phase_shift" in self.activePlayer.states and self.activePlayer.states["phase_shift"] > 0) and not cheat:
      if reset:
        self.activePlayer.states["phase_shift"] -= 1 # reset to false
    elif card.house not in self.activeHouse:
      if message: pyautogui.alert("Can't play cards not from the active house.")
      return False
    return True
  
  def canFight(self, card, reset = True, cheat: bool = False, r_click: bool = False):
    if not card.ready or (card.stun and not r_click):
      return False
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      pyautogui.alert("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.type == "Creature": # why wouldn't it?
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        pyautogui.alert("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
        return False
      if card.house not in self.activeHouse and card.house not in self.extraFightHouses and card.house not in self.extraUseHouses and card.title != "tireless_crocag" and not cheat:
        return False
      if "foggify" in self.inactivePlayer.states and self.inactivePlayer.states["foggify"] or "fogbank" in self.inactivePlayer.states and self.inactivePlayer.states["fogbank"]:
        return False
      if card.title == "bigtwig" and True not in [x.stun for x in self.inactivePlayer.board["Creature"]]:
        return False
    

    return True

  def canReap(self, card, reset = True, r_click: bool = False, cheat: bool = False):
    if card.type != "Creature" or not card.ready or (card.stun and not r_click):
      return False
    if card.house not in self.activeHouse and card.house not in self.extraUseHouses and not cheat:
      return False
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      pyautogui.alert("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.type == "Creature":
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        pyautogui.alert("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
        return False
      if card.title == "tireless_crocag":
        return False
    

    return True

  def canAction(self, card, reset = True, r_click: bool = False, cheat: bool = False):
    if not card.ready:
      return False
    if card.house not in self.activeHouse and card.house not in self.extraUseHouses and not cheat:
      return False
    if card.type == "Creature" and (card.stun and not r_click):
      return False
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      pyautogui.alert("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.type == "Creature":
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        pyautogui.alert("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
        return False
    

    if card.action or card.omni:
      return True
    else:
      return False
  
  def canDiscard(self, card, reset = True):
    if self.turnNum == 1 and (len(self.playedThisTurn) > 0 or len(self.discardedThisTurn) > 0):
      return False
    if card.house in self.activeHouse:
      return True
    # I don't think anything messes with your ability to discard
    # print(f"{card.title} belongs to house {card.house}")
    return False
  
  def playUpgrade(self, card, target = None):
    """ Plays an upgrade on a creature.
    """
    print(card)
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    hand = self.activePlayer.hand
    broken = False
    
    if target:
      self.activePlayer.board["Upgrade"].append(hand.pop(hand.index(card)))
      side, choice = target
      if side == "fr":
        active[choice].upgrade.append(card)
      else:
        inactive[choice].upgrade.append(card)
      eval(f"upgrade.{card.title}(self, card, side, choice)")
      self.cardChanged()
      return
    
    drawMe = []
    # surfs
    selectedSurf = pygame.Surface((self.target_cardw, self.target_cardh))
    selectedSurf.convert_alpha()
    selectedSurf.set_alpha(80)
    selectedSurf.fill(COLORS["LIGHT_GREEN"])

    selectedSurfTapped = pygame.Surface((self.target_cardh, self.target_cardw))
    selectedSurfTapped.convert_alpha()
    selectedSurfTapped.set_alpha(80)
    selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])
    # draw all targets
    for temp_card in active + inactive:
      if temp_card.ready:
        drawMe.append((selectedSurf, temp_card.rect))
      else:
        drawMe.append((selectedSurfTapped, temp_card.tapped_rect))
  
    if self.canDiscard(card, reset = False):
      ## discard stuff here - if you can play it, you can discard it
      discSurf = pygame.Surface((self.target_cardw, self.target_cardh))
      discSurf.convert_alpha()
      discSurf.set_alpha(80)
      discSurf.fill(COLORS["LIGHT_GREEN"])
      discRect = discSurf.get_rect()
      discRect.topleft = self.discard1_rect.topleft
      drawMe.append((discSurf, discRect))
    
    while True:
      self.extraDraws = drawMe.copy()
      
      for e in pygame.event.get():
        if e.type == pygame.MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = e.pos
        
        if e.type == pygame.QUIT:
          pygame.quit()

        if e.type == MOUSEBUTTONUP and e.button == 1:
          activeHit = [pygame.Rect.collidepoint(x.rect, (self.mousex, self.mousey)) for x in active]
          activeHitTapped = [pygame.Rect.collidepoint(x.tapped_rect, (self.mousex, self.mousey)) for x in active]
          inactiveHit = [pygame.Rect.collidepoint(x.rect, (self.mousex, self.mousey)) for x in inactive]
          inactiveHitTapped = [pygame.Rect.collidepoint(x.tapped_rect, (self.mousex, self.mousey)) for x in inactive]
          if pygame.Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
            l = len(hand)
            for x in range(len(hand)):
              temp_card = hand[x]
              if x == 0 and self.mousex < temp_card.rect.centerx:
                hand.insert(0, self.dragging.pop())
                self.extraDraws = []
                self.cardChanged()
                return
              elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
                hand.insert(x + 1, self.dragging.pop())
                self.extraDraws = []
                self.cardChanged()
                return
            hand.append(self.dragging.pop())
            self.extraDraws = []
            return
          elif True in activeHit:
            self.activePlayer.board["Upgrade"].append(self.dragging.pop())
            side = "fr"
            choice = activeHit.index(True)
            active[choice].upgrade.append(card)
            eval(f"upgrade.{card.title}(self, card, side, choice)")
            broken = True
            break
          elif True in activeHitTapped:
            self.activePlayer.board["Upgrade"].append(self.dragging.pop())
            side = "fr"
            choice = activeHitTapped.index(True)
            active[choice].upgrade.append(card)
            eval(f"upgrade.{card.title}(self, card, side, choice)")
            broken = True
            break
          elif True in inactiveHit:
            self.activePlayer.board["Upgrade"].append(self.dragging.pop())
            side = "fo"
            choice = inactiveHit.index(True)
            inactive[choice].upgrade.append(card)
            eval(f"upgrade.{card.title}(self, card, side, choice)")
            broken = True
            break
          elif True in inactiveHitTapped:
            self.activePlayer.board["Upgrade"].append(self.dragging.pop())
            side = "fo"
            choice = inactiveHitTapped.index(True)
            inactive[choice].upgrade.append(card)
            eval(f"upgrade.{card.title}(self, card, side, choice)")
            broken = True
            break
          elif self.canDiscard(card, reset=False) and pygame.Rect.collidepoint(discRect, (self.mousex, self.mousey)):
            hand.append(self.dragging.pop())
            self.discardCard(-1)
            self.extraDraws = []
            self.cardChanged()
            return
          else:
            hand.append(self.dragging.pop())
            self.extraDraws = []
            self.cardChanged()
            return

        if e.type == MOUSEBUTTONDOWN and e.button == 1:
          print("You shouldn't be able to do that here.")

      if pygame.Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
        l = len(hand)
        for x in range(len(hand)):
          temp_card = hand[x]
          if x == 0 and self.mousex < temp_card.rect.centerx:
            hand.insert(0, self.invisicard)
            self.cardChanged()
            break
          elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
            hand.insert(x + 1, self.invisicard)
            self.cardChanged()
            break

      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      try:
        hand.remove(self.invisicard)
      except:
        pass
      pygame.display.flip()
      self.extraDraws = []
      if broken:
        self.cardChanged()
        break
    
    if not target and card.amber > 0:
      self.activePlayer.gainAmber(card.amber, self)
      pyautogui.alert(f"{card.title} gave you {str(card.amber)} amber. You now have {str(self.activePlayer.amber)} amber.\n\nChange to a log when you fix the amber display issue.""")
    self.playedThisTurn.append(card)
    self.cardChanged()
    return

  def dragCard(self) -> None:
    """ Enables dragging a card from your hand around the screen.
    """
    card = self.dragging[0]
    hand = self.activePlayer.hand
    drawMe = []

    if self.canDiscard(card, reset = False):
      ## discard stuff here - if you can play it, you can discard it
      discSurf = pygame.Surface((self.target_cardw, self.target_cardh))
      discSurf.convert_alpha()
      discSurf.set_alpha(80)
      discSurf.fill(COLORS["LIGHT_GREEN"])
      discRect = discSurf.get_rect()
      discRect.topleft = self.discard1_rect.topleft
      drawMe = [(discSurf, discRect)]
    
    if self.canPlay(card, reset=False):
      if card.type == "Action":
        dropSurf = pygame.Surface((self.creatures1.get_width(), (self.mat1.get_height() // 3) * 2))
        dropSurf.convert_alpha()
        dropSurf.set_alpha(80)
        dropSurf.fill(COLORS["LIGHT_GREEN"])
        dropRect = dropSurf.get_rect()
        dropRect.topleft = self.creatures1_rect.topleft
        drawMe.append((dropSurf, dropRect))
      elif card.type == "Upgrade":
        self.playUpgrade(card)
        return
      elif card.type == "Creature" or card.type == "Artifact":
        flank = self.chooseFlank(card)
        print(flank)
        if flank:
          self.activePlayer.hand.append(self.dragging.pop())
          self.playCard(-1, flank=flank, ask=False)
        elif self.dragging:
          self.activePlayer.hand.append(self.dragging.pop())
        self.extraDraws = []
        return

    while True:
      self.extraDraws = drawMe.copy()
      
      for e in pygame.event.get():
        if e.type == pygame.MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = e.pos
        
        if e.type == pygame.QUIT:
          pygame.quit()

        if e.type == MOUSEBUTTONUP and e.button == 1:
          if pygame.Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
            l = len(hand)
            for x in range(len(hand)):
              temp_card = hand[x]
              if x == 0 and self.mousex < temp_card.rect.centerx:
                hand.insert(0, self.dragging.pop())
                self.extraDraws = []
                self.cardChanged()
                return
              elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
                hand.insert(x + 1, self.dragging.pop())
                self.extraDraws = []
                self.cardChanged()
                return
            hand.append(self.dragging.pop())
            self.extraDraws = []
            self.cardChanged()
            return
          elif self.canPlay(card, reset=False) and pygame.Rect.collidepoint(dropRect, (self.mousex, self.mousey)):
            hand.append(self.dragging.pop())
            self.playCard(-1, ask = False)
            self.extraDraws = []
            self.cardChanged()
            return
          elif self.canDiscard(card, reset=False) and pygame.Rect.collidepoint(discRect, (self.mousex, self.mousey)):
            hand.append(self.dragging.pop())
            self.discardCard(-1)
            self.extraDraws = []
            self.cardChanged()
            return
          else:
            hand.append(self.dragging.pop())
            self.extraDraws = []
            self.cardChanged()
            return

        if e.type == MOUSEBUTTONDOWN and e.button == 1:
          print("You shouldn't be able to do that here.")

      if pygame.Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
        l = len(hand)
        for x in range(len(hand)):
          temp_card = hand[x]
          if x == 0 and self.mousex < temp_card.rect.centerx:
            hand.insert(0, self.invisicard)
            self.cardChanged()
            break
          elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
            hand.insert(x + 1, self.invisicard)
            self.cardChanged()
            break

      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.draw(False)
      try:
        hand.remove(self.invisicard)
      except:
        pass
      pygame.display.flip()
      self.extraDraws = []



  def chooseFlank(self, card) -> str:
    """ Lets the user choose which flank to put play their creature on.
    """
    hand = self.activePlayer.hand
    # message
    messageSurf = self.BASICFONT.render(f"Choose which flank to play this {card.type.lower()} on:", 1, COLORS["WHITE"])
    messageRect = messageSurf.get_rect()
    messageRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # message background
    backgroundSurf = pygame.Surface((messageSurf.get_width(), messageSurf.get_height()))
    backgroundSurf.convert()
    backgroundRect = backgroundSurf.get_rect()
    backgroundRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    
    # flanks
    self.flankSurf = card.image
    self.flankSurf.set_alpha(80)
    self.flankRectLeft = self.flankSurf.get_rect()
    self.flankRectRight = self.flankSurf.get_rect()
    
    self.flankSurfTapped = card.tapped
    self.flankSurfTapped.set_alpha(80)
    self.flankRectLeftTapped = self.flankSurfTapped.get_rect()
    self.flankRectRightTapped = self.flankSurfTapped.get_rect()

    drawMe = [(messageSurf, messageRect)]
    discard = self.canDiscard(card, reset = False)

    if discard:
      ## discard stuff here - if you can play it, you can discard it
      discSurf = pygame.Surface((self.target_cardw, self.target_cardh))
      discSurf.convert_alpha()
      discSurf.set_alpha(80)
      discSurf.fill(COLORS["LIGHT_GREEN"])
      discRect = discSurf.get_rect()
      discRect.topleft = self.discard1_rect.topleft
      drawMe.append((discSurf, discRect))

    if card.type == "Creature" and len(self.activePlayer.board[card.type]) > 0:
      board = self.activePlayer.board[card.type]
      # right
      if willEnterReady(self, card, False):
        self.flankRectRightTapped.topleft = (-500, -500)
        if board[-1].ready: # both ready
          if board[-1].taunt and not card.taunt: # in play taunt, played not
            self.flankRectRight.topleft = (board[-1].rect.topright)
            self.flankRectRight.top += self.margin * 3
          elif not board[-1].taunt and card.taunt: # played taunt, in play not
            self.flankRectRight.topleft = (board[-1].rect.topright)
            self.flankRectRight.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRight.topleft = (board[-1].rect.topright)
          self.flankRectRight.right += self.margin
        else: # played ready, in play not
          if board[-1].taunt and not card.taunt: # in play taunt, played not
            self.flankRectRight.bottomleft = (board[-1].tapped_rect.bottomright)
            self.flankRectRight.top += self.margin * 3
          elif not board[-1].taunt and card.taunt: # played taunt, in play not
            self.flankRectRight.bottomleft = (board[-1].tapped_rect.bottomright)
            self.flankRectRight.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRight.bottomleft = (board[-1].tapped_rect.bottomright)
          self.flankRectRight.right += self.margin
        drawMe.append((self.flankSurf, self.flankRectRight))
      else:
        self.flankRectRight.topleft = (-500, -500)
        if board[-1].ready: # played not ready, in play ready
          if board[-1].taunt and not card.taunt: # in play taunt, played not
            self.flankRectRightTapped.bottomleft = (board[-1].rect.bottomright)
            self.flankRectRightTapped.top += self.margin * 3
          elif not board[-1].taunt and card.taunt: # played taunt, in play not
            self.flankRectRightTapped.topleft = (board[-1].rect.topright)
            self.flankRectRightTapped.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRightTapped.bottomleft = (board[-1].rect.bottomright)
          self.flankRectRightTapped.right += self.margin
        else: # played not ready, in play not ready
          if board[-1].taunt and not card.taunt: # in play taunt, played not
            self.flankRectRightTapped.topleft = (board[-1].tapped_rect.topright)
            self.flankRectRightTapped.top += self.margin * 3
          elif not board[-1].taunt and card.taunt: # played taunt, in play not
            self.flankRectRightTapped.topleft = (board[-1].tapped_rect.topright)
            self.flankRectRightTapped.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRightTapped.topleft = (board[-1].tapped_rect.topright)
          self.flankRectRightTapped.right += self.margin
        drawMe.append((self.flankSurfTapped, self.flankRectRightTapped))
      # left
      if willEnterReady(self, card, False):
        self.flankRectLeftTapped.topright = (-500, -500)
        if board[0].ready: # both ready
          if board[0].taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeft.topright = (board[0].rect.topleft)
            self.flankRectLeft.top += self.margin * 3
          elif not board[0].taunt and card.taunt: # played taunt, in play not
            self.flankRectLeft.topright = (board[0].rect.topleft)
            self.flankRectLeft.top -= self.margin * 3
          else: # both same
            self.flankRectLeft.topright = (board[0].rect.topleft)
          self.flankRectLeft.left -= self.margin
        else: # played ready, in play not
          if board[0].taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeft.bottomright = (board[0].tapped_rect.bottomleft)
            self.flankRectLeft.top += self.margin * 3
          elif not board[0].taunt and card.taunt: # played taunt, in play not
            self.flankRectLeft.bottomright = (board[0].tapped_rect.bottomleft)
            self.flankRectLeft.top -= self.margin * 3
          else: # both same
            self.flankRectLeft.bottomright = (board[0].tapped_rect.bottomleft)
          self.flankRectLeft.left -= self.margin
        drawMe.append((self.flankSurf, self.flankRectLeft))
      else:
        self.flankRectLeft.topright = (-500, -500)
        if board[0].ready: # in play ready, played not
          if board[0].taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeftTapped.bottomright = (board[0].rect.bottomleft)
            self.flankRectLeftTapped.top += self.margin * 3
          elif not board[0].taunt and card.taunt: # played taunt, in play not
            self.flankRectLeftTapped.topright = (board[0].rect.topleft)
            self.flankRectLeftTapped.top -= self.margin * 3
          else: # both same
            self.flankRectLeftTapped.bottomright = (board[0].rect.bottomleft)
          self.flankRectLeftTapped.left -= self.margin
        else: # neither ready
          if board[0].taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeftTapped.topright = (board[0].tapped_rect.topleft)
            self.flankRectLeftTapped.top += self.margin * 3
          elif not board[0].taunt and card.taunt: # played taunt, in play not
            self.flankRectLeftTapped.topright = (board[0].tapped_rect.topleft)
            self.flankRectLeftTapped.top -= self.margin * 3
          else: # both same
            self.flankRectLeftTapped.topright = (board[0].tapped_rect.topleft)
          self.flankRectLeftTapped.left -= self.margin
        drawMe.append((self.flankSurfTapped, self.flankRectLeftTapped))
    else: # empty board
      if willEnterReady(self, card, False):
        self.flankRectRight.center = self.creatures1_rect.center
        self.flankRectLeft.topright = (-500, -500)
        self.flankRectLeftTapped.topright = (-500, -500)
        self.flankRectRightTapped.topright = (-500, -500)
        drawMe.append((self.flankSurf, self.flankRectRight))
      else:
        self.flankRectRightTapped.center = self.creatures1_rect.center
        self.flankRectLeftTapped.topright = (-500, -500)
        self.flankRectLeft.topright = (-500, -500)
        self.flankRectRight.topright = (-500, -500)
        drawMe.append((self.flankSurfTapped, self.flankRectRightTapped))
    
    if card.type == "Artifact":
      artifact = self.activePlayer.board["Artifact"]
      if willEnterReady(self, card, False):
        self.flankRectRight.center = self.artifacts1_rect.center
        if len(artifact) > 0:
          if artifact[-1].ready:
            self.flankRectRight.left = artifact[-1].rect.right + self.margin
          else:
            self.flankRectRight.left = artifact[-1].tapped_rect.right + self.margin
        self.flankRectLeft.topright = (-500, -500)
        self.flankRectLeftTapped.topright = (-500, -500)
        self.flankRectRightTapped.topright = (-500, -500)
        drawMe.append((self.flankSurf, self.flankRectRight))
      else:
        self.flankRectRightTapped.center = self.artifacts1_rect.center
        if len(artifact) > 0:
          if artifact[-1].ready:
            self.flankRectRightTapped.left = artifact[-1].rect.right + self.margin
          else:
            self.flankRectRightTapped.left = artifact[-1].tapped_rect.right + self.margin
        self.flankRectLeftTapped.topright = (-500, -500)
        self.flankRectLeft.topright = (-500, -500)
        self.flankRectRight.topright = (-500, -500)
        drawMe.append((self.flankSurfTapped, self.flankRectRightTapped))


    while True:
      self.extraDraws = drawMe.copy()
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if pygame.Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
            l = len(hand)
            for x in range(len(hand)):
              temp_card = hand[x]
              if x == 0 and self.mousex < temp_card.rect.centerx:
                hand.insert(0, self.dragging.pop())
                self.extraDraws = []
                card.tapped.set_alpha(255)
                card.image.set_alpha(255)
                self.cardChanged()
                return
              elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
                hand.insert(x + 1, self.dragging.pop())
                self.extraDraws = []
                card.tapped.set_alpha(255)
                card.image.set_alpha(255)
                self.cardChanged()
                return
            hand.append(self.dragging.pop())
            self.extraDraws = []
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            self.cardChanged()
            return
          elif True not in self.friendDraws and True in [pygame.Rect.collidepoint(x, (self.mousex, self.mousey)) for x in [self.flankRectLeft, self.flankRectLeftTapped, self.flankRectRight, self.flankRectRightTapped]]:
            if pygame.Rect.collidepoint(self.flankRectLeft, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              return "Left"
            elif pygame.Rect.collidepoint(self.flankRectLeftTapped, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              return "Left"
            elif pygame.Rect.collidepoint(self.flankRectRight, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              return "Right"
            elif pygame.Rect.collidepoint(self.flankRectRightTapped, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              return "Right"
          elif discard and pygame.Rect.collidepoint(discRect, (self.mousex, self.mousey)):
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            hand.append(self.dragging.pop())
            self.discardCard(-1)
            self.extraDraws = []
            self.cardChanged()
            return
          elif True not in self.friendDraws and self.dragging:
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            self.activePlayer.hand.append(self.dragging.pop())
            self.extraDraws = []
            self.cardChanged()
            return None
          elif not self.dragging:
            if True in self.friendDraws and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
              self.drawFriendDiscard = False
              self.drawFriendArchive = False
              self.drawFriendPurge = False
              for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
                card.rect.topleft = (-500, -500)
              self.cardChanged()
            elif True in self.enemyDraws and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
              self.drawEnemyDiscard = False
              self.drawEnemyArchive = False
              self.drawEnemyPurge = False
              for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
                card.rect.topleft = (-500, -500)
              self.cardChanged()
            elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
              self.drawFriendDiscard = True
            elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
              self.drawEnemyDiscard = True
            elif not self.drawFriendPurge and pygame.Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
              self.drawFriendPurge = True
            elif not self.drawEnemyPurge and pygame.Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
              self.drawEnemyPurge = True
            elif not self.drawFriendArchive and pygame.Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
              self.drawFriendArchive = True
            elif not self.drawEnemyArchive and pygame.Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
              self.drawEnemyArchive = True
          else:
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            self.extraDraws = []
            self.cardChanged()
            return None
      
      if pygame.Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
        l = len(hand)
        for x in range(len(hand)):
          temp_card = hand[x]
          if x == 0 and self.mousex < temp_card.rect.centerx:
            hand.insert(0, self.invisicard)
            self.cardChanged()
            break
          elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
            hand.insert(x + 1, self.invisicard)
            self.cardChanged()
            break
      
      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      try:
        hand.remove(self.invisicard)
      except:
        pass
      pygame.display.flip()
      self.extraDraws = []

  def chooseMulligan(self, player: str) -> bool:
    """ Lets the user choose whether or not to keep their opening hand.
    """
    # message
    messageSurf = self.BASICFONT.render(f"{player}, Keep or Mulligan?", 1, COLORS["WHITE"])
    messageRect = messageSurf.get_rect()
    messageRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # message background
    backgroundSurf = pygame.Surface((messageSurf.get_width(), messageSurf.get_height()))
    backgroundSurf.convert()
    backgroundRect = backgroundSurf.get_rect()
    backgroundRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # keep
    keepSurf = self.BASICFONT.render("   KEEP   ", 1, COLORS["WHITE"])
    keepRect = keepSurf.get_rect()
    keepRect.topright = ((WIDTH // 2) - (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)
    # keep background
    keepBack = pygame.Surface((keepSurf.get_width(), keepSurf.get_height()))
    keepBack.convert()
    keepBack.fill(COLORS["LIGHT_GREEN"])
    keepBackRect = keepBack.get_rect()
    keepBackRect.topright = ((WIDTH // 2) - (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)
    # mulligan
    mullSurf = self.BASICFONT.render(" MULLIGAN ", 1, COLORS["WHITE"])
    mullRect = mullSurf.get_rect()
    mullRect.topleft = ((WIDTH // 2) + (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)
    # mulligan background
    mullBack = pygame.Surface((mullSurf.get_width(), mullSurf.get_height()))
    mullBack.convert()
    mullBack.fill(COLORS["RED"])
    mullBackRect = mullBack.get_rect()
    mullBackRect.topleft = ((WIDTH // 2) + (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)

    while True:
      self.extraDraws = [(backgroundSurf, backgroundRect), (messageSurf, messageRect),  (keepBack, keepBackRect), (keepSurf, keepRect), (mullBack, mullBackRect), (mullSurf, mullRect)]
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.extraDraws = []
          if pygame.Rect.collidepoint(keepBackRect, (self.mousex, self.mousey)):
            return False
          elif pygame.Rect.collidepoint(mullBackRect, (self.mousex, self.mousey)):
            return True
      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      pygame.display.flip()
      self.extraDraws = []

  
  def chooseHouse(self, varAsStr: str, custom: Tuple[str, List[str]] = (), colors: List[str] = []) -> List[str]:
    """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards like control the weak.
    """
    if varAsStr == "activeHouse":
      message = "Choose your house for this turn:"
      if "control_the_weak" in self.inactivePlayer.states and self.inactivePlayer.states["control_the_weak"]:
        # self.activeHouse = [self.inactivePlayer.states["control_the_weak"]]
        houses = self.inactivePlayer.states["control_the_weak"]
      else:
        houses = [self.activePlayer.houses[0],self.activePlayer.houses[1],self.activePlayer.houses[2]]
      if "pitlord" in [x.title for x in self.activePlayer.board["Creature"]]:
        if "control_the_weak" in self.inactivePlayer.states and self.inactivePlayer.states["control_the_weak"] and "Dis" not in houses: # other things can affect this too though...
          houses.append("Dis")
        else:
          houses = ["Dis"]
      if "restringuntus" in [x.title for x in self.inactivePlayer.board["Creature"]]:
        house = self.inactivePlayer.states["restringuntus"] # won't be more than one
        if house in houses:
          houses.remove(house)
    elif varAsStr == "extraFight": #for brothers in battle, and probably others
      message = "Choose another house to be able to fight:"
      houses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]
      for house in self.activeHouse:
        houses.remove(house)
    elif varAsStr == "control": # control the weak
      message = "Choose a house from your opponent's identity card:"
      houses = [self.inactivePlayer.houses[0],self.inactivePlayer.houses[1],self.inactivePlayer.houses[2]]
    elif varAsStr == "other":
      message = "Choose any house:"
      houses = ["Brobnar", "Dis", "Logos", "Mars", "Sanctum", "Shadows", "Untamed"]
    elif varAsStr == "custom":
      message = custom[0]
      houses = custom[1]
    # elif varAsStr == "color":
    #   message = custom[0]
    #   houses = custom[1]
    houses_rects = []
    # message
    messageSurf = self.BASICFONT.render(message, 1, COLORS["WHITE"])
    messageRect = messageSurf.get_rect()
    messageRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # message background
    messageBackSurf = pygame.Surface((messageSurf.get_width(), messageSurf.get_height()))
    messageBackSurf.convert()
    messageBackRect = messageBackSurf.get_rect()
    messageBackRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # confirm
    confirmSurf = self.BASICFONT.render("  CONFIRM  ", 1, COLORS["WHITE"])
    confirmRect = confirmSurf.get_rect()
    confirmRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # confirm background
    confirmBack = pygame.Surface((confirmSurf.get_width(), confirmSurf.get_height()))
    confirmBack.convert()
    confirmBack.fill(COLORS["GREEN"])
    confirmBackRect = confirmBack.get_rect()
    confirmBackRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # house buttons
    for house in houses:
      houseMessageSurf = self.BASICFONT.render(f"  {house}  ", 1, COLORS["BLACK"])
      houseMessageRect = houseMessageSurf.get_rect()
      houseMessageRect.top = messageRect[1] + messageRect[3] + self.margin
      houseBackSurf = pygame.Surface((houseMessageSurf.get_width(), houseMessageSurf.get_height()))
      if colors:
        houseBackSurf.fill(COLORS[colors[houses.index(house)]])
      else:
        houseBackSurf.fill(COLORS["YELLOW"])
      houseBackRect = houseBackSurf.get_rect()
      houseBackRect.top = messageRect[1] + messageRect[3] + self.margin
      houses_rects.append(( houseBackSurf, houseBackRect, houseMessageSurf, houseMessageRect))
    # print(houses_rects)
    length = sum(house[1][2] for house in houses_rects) + (self.margin * (len(houses_rects) - 1))
    left = (WIDTH // 2) - (length // 2)
    for house_rect in houses_rects:
      house_rect[1].left = left
      house_rect[3].left = left
      left += house_rect[1][2] + self.margin
    # then this loop will handle drawing those options
    selected = 0
    while True:
      if selected:
        self.extraDraws = [(confirmBack, confirmBackRect), (confirmSurf, confirmRect)] + [item for sublist in [[(x[0], x[1]), (x[2], x[3])] for x in houses_rects] for item in sublist]
        if varAsStr == "activeHouse":
          self.extraDraws += self.previewHouse(self.activePlayer.houses[selected - 1])
      else:
        self.extraDraws = [(messageBackSurf, messageBackRect), (messageSurf, messageRect)] + [item for sublist in [[(x[0], x[1]), (x[2], x[3])] for x in houses_rects] for item in sublist]
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if selected and pygame.Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
            self.extraDraws = []
            self.cardChanged()
            return [houses[clicked]]
          click = [pygame.Rect.collidepoint(x[1], (self.mousex, self.mousey)) for x in houses_rects]
          if True in click:
            if selected and click.index(True) == clicked:
              for x in houses_rects:
                if colors:
                  x[0].fill(COLORS[colors[houses_rects.index(x)]])
                else:
                  x[0].fill(COLORS["YELLOW"])
                selected = 0
            else:
              for x in houses_rects:
                if colors:
                  x[0].fill(COLORS[colors[houses_rects.index(x)]])
                else:
                  x[0].fill(COLORS["YELLOW"])
              clicked = click.index(True)
              selected = clicked + 1
              houses_rects[clicked][0].fill(COLORS["LIGHT_GREEN"])
          elif True in self.friendDraws and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.cardChanged()
          elif True in self.enemyDraws and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.cardChanged()
          elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          elif not self.drawFriendPurge and pygame.Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
            self.drawFriendPurge = True
          elif not self.drawEnemyPurge and pygame.Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
            self.drawEnemyPurge = True
          elif not self.drawFriendArchive and pygame.Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
            self.drawFriendArchive = True
          elif not self.drawEnemyArchive and pygame.Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
            self.drawEnemyArchive = True
      if pygame.Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
        confirmBack.fill(COLORS["LIGHT_GREEN"])
      else:
        confirmBack.fill(COLORS["GREEN"])
      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      pygame.display.flip()
      self.extraDraws = []


  def chooseCards(self, targetPool: str, message: str = "Choose a target:", canHit: str = "both", count: int = 1, full: bool = True, condition = lambda x: x == x, con_message: str = "This target does not meet the conditions.") -> List[int]:
    """ This can't deal with something that could target artifacts and creatures simultaneously. Also, the onus is on the caller to handle the results as creatures or artifacts or hand or discard, as appropriate.\n
        Valid targetPool options: Creature, Artifact, Hand, Discard\n
        Valid message: any string
        Valid canHit: either, both, enemy, friend\n
        Count is max number of choices\n
        If full is True, you can only submit when your target list length is equal to count\n
        If a condition is set, only cards that match the condition can be picked\n
        If condition isn't met, the con_message is displayed
    """
    active = self.activePlayer.board
    inactive = self.inactivePlayer.board

    # message
    messageSurf = self.BASICFONT.render(message, 1, COLORS["WHITE"])
    messageRect = messageSurf.get_rect()
    messageRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # message background
    backgroundSurf = pygame.Surface((messageSurf.get_width(), messageSurf.get_height()))
    backgroundSurf.convert()
    backgroundRect = backgroundSurf.get_rect()
    backgroundRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # confirm
    confirmSurf = self.BASICFONT.render("  CONFIRM  ", 1, COLORS["WHITE"])
    confirmRect = confirmSurf.get_rect()
    confirmRect.top = messageRect[1] + messageRect[3] + self.margin
    confirmRect.right = (WIDTH // 2) - (self.margin // 2)
    # confirm background
    confirmBack = pygame.Surface((confirmSurf.get_width(), confirmSurf.get_height()))
    confirmBack.convert()
    confirmBack.fill(COLORS["GREEN"])
    confirmBackRect = confirmBack.get_rect()
    confirmBackRect.top = messageRect[1] + messageRect[3] + self.margin
    confirmBackRect.right = (WIDTH // 2)  - (self.margin // 2)
    # cancel
    cancelSurf = self.BASICFONT.render("  RESET  ", 1, COLORS["WHITE"])
    cancelRect = cancelSurf.get_rect()
    cancelRect.top = messageRect[1] + messageRect[3] + self.margin
    cancelRect.left = (WIDTH // 2)  + (self.margin // 2)
    # cancel background
    cancelBack = pygame.Surface((cancelSurf.get_width(), cancelSurf.get_height()))
    cancelBack.convert()
    cancelBack.fill(COLORS["RED"])
    cancelBackRect = cancelBack.get_rect()
    cancelBackRect.top = messageRect[1] + messageRect[3] + self.margin
    cancelBackRect.left = (WIDTH // 2)  + (self.margin // 2)
    
    selectedSurf = pygame.Surface((self.target_cardw, self.target_cardh))
    selectedSurf.convert_alpha()
    selectedSurf.set_alpha(80)
    selectedSurf.fill(COLORS["LIGHT_GREEN"])

    selectedSurfTapped = pygame.Surface((self.target_cardh, self.target_cardw))
    selectedSurfTapped.convert_alpha()
    selectedSurfTapped.set_alpha(80)
    selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])

    invalidSurf = pygame.Surface((self.target_cardw, self.target_cardh))
    invalidSurf.convert_alpha()
    invalidSurf.set_alpha(80)
    invalidSurf.fill(COLORS["RED"])

    invalidSurfTapped = pygame.Surface((self.target_cardh, self.target_cardw))
    invalidSurfTapped.convert_alpha()
    invalidSurfTapped.set_alpha(80)
    invalidSurf.fill(COLORS["RED"])

    invalid = []

    if canHit == "friend":
      target = self.activePlayer
    elif canHit == "enemy":
      target = self.inactivePlayer
    elif canHit == "both":
      target = self.activePlayer
    elif canHit == "either":
      target = self.activePlayer
    else:
      print(f"Invalid canhit: {canHit}")
      raise ValueError
    
    if targetPool == "Hand":
      for card in target.hand:
        if not condition(card):
          invalid.append((invalidSurf, card.rect))
    elif targetPool == "Discard":
      for card in target.discard:
        if not condition(card):
          invalid.append((invalidSurf, card.rect))
    else: # targetPool == "Artifact" or "Creature"
      if canHit == "both" or canHit == "either":
        target = self.activePlayer.board[targetPool] + self.inactivePlayer.board[targetPool]
        for card in target:
          if not condition(card):
            if card.ready:
              invalid.append((invalidSurf, card.rect))
            else:
              invalid.append((invalidSurfTapped, card.tapped_rect))
      if canHit == "friend" or canHit == "enemy":
        for card in target.board[targetPool]:
          if not condition(card):
            if card.ready:
              invalid.append((invalidSurf, card.rect))
            else:
              invalid.append((invalidSurfTapped, card.tapped_rect))  
        
    selected = []
    retVal = []
    while True:
      self.extraDraws = [(backgroundSurf, backgroundRect), (messageSurf, messageRect), (confirmBack, confirmBackRect), (confirmSurf, confirmRect), (cancelBack, cancelBackRect), (cancelSurf, cancelRect)] + invalid + selected
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if pygame.Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
            self.extraDraws = []
            if retVal and not full:
              if len(retVal) <= count and not full:
                self.cardChanged()
                return retVal
              else:
                pyautogui.alert("Not enough targets selected!")
            elif retVal and full and len(retVal) == count:
              self.cardChanged()
              return retVal
            elif not full:
              incomplete = None
              while not incomplete:
                incomplete = pyautogui.confirm("Are you sure you want to target less than the full number of targets?", buttons=["Yes", "No"])
              if incomplete == "Yes":
                self.cardChanged()
                return retVal
          elif pygame.Rect.collidepoint(cancelBackRect, (self.mousex, self.mousey)):
            retVal = []
            selected = []
            confirmBack.fill(COLORS["GREEN"])
          elif True in self.friendDraws and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.cardChanged()
          elif True in self.enemyDraws and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
              card.rect.topleft = (-500, -500)
            self.cardChanged()
          elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          elif not self.drawFriendPurge and pygame.Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
            self.drawFriendPurge = True
          elif not self.drawEnemyPurge and pygame.Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
            self.drawEnemyPurge = True
          elif not self.drawFriendArchive and pygame.Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
            self.drawFriendArchive = True
          elif not self.drawEnemyArchive and pygame.Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
            self.drawEnemyArchive = True
          if targetPool != "Hand":
            if targetPool == "Discard":
              if canHit == "both": # this means I can select from both boards at the same time, eg natures call
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
                if True in friend:
                  index = friend.index(True)
                  card = self.activePlayer.discard[index]
                  if condition(card):
                    toAdd = ("fr", index)
                    if toAdd not in retVal and len(retVal) < count:
                      selected.append((selectedSurf, card.rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      selected.remove((selectedSurf, card.rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
                if True in foe:
                  index = foe.index(True)
                  card = self.inactivePlayer.discard[index]
                  if condition(card):
                    toAdd = ("fo", index)
                    if toAdd not in retVal and len(retVal) < count:
                      selected.append((selectedSurf, card.rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      selected.remove((selectedSurf, card.rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
              elif canHit == "either": # this means I can select multiples, but only all from same side
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
                if True in friend and (not retVal or retVal[0][0] == "fr"):
                  index = friend.index(True)
                  card = self.activePlayer.discard[index]
                  if condition(card):
                    toAdd = ("fr", index)
                    if toAdd not in retVal and len(retVal) < count:
                      selected.append((selectedSurf, card.rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      selected.remove((selectedSurf, card.rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
                if True in foe and (not retVal or retVal[0][0] == "fo"):
                  index = foe.index(True)
                  card = self.inactivePlayer.discard[index]
                  if condition(card):
                    toAdd = ("fo", index)
                    if toAdd not in retVal and len(retVal) < count:
                      selected.append((selectedSurf, card.rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      selected.remove((selectedSurf, card.rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
              elif canHit == "enemy": # this means I can only target unfriendlies
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
                if True in foe:
                  index = foe.index(True)
                  card = self.inactivePlayer.discard[index]
                  if condition(card):
                    toAdd = ("fo", index)
                    if toAdd not in retVal and len(retVal) < count:
                      selected.append((selectedSurf, card.rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      selected.remove((selectedSurf, card.rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
              elif canHit == "friend": # this means I can only target friendlies
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
                if True in friend:
                  index = friend.index(True)
                  card = self.activePlayer.discard[index]
                  if condition(card):
                    toAdd = ("fr", index)
                    if toAdd not in retVal and len(retVal) < count:
                      selected.append((selectedSurf, card.rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      selected.remove((selectedSurf, card.rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
            else: # Creature or Artifact
              if canHit == "both": # this means I can select from both boards at the same time, eg natures call
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True not in friend:
                  friend = [pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True in friend:
                  index = friend.index(True)
                  card = active[targetPool][index]
                  if condition(card):
                    toAdd = ("fr", index)
                    if toAdd not in retVal and len(retVal) < count:
                      if card.ready:
                        selected.append((selectedSurf, card.rect))
                      else:
                        selected.append((selectedSurfTapped, card.tapped_rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      if card.ready:
                        selected.remove((selectedSurf, card.rect))
                      else:
                        selected.remove((selectedSurfTapped, card.tapped_rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in inactive[targetPool]]
                if True in foe:
                  index = foe.index(True)
                  card = inactive[targetPool][index]
                  if condition(card):
                    toAdd = ("fo", index)
                    if toAdd not in retVal and len(retVal) < count:
                      if card.ready:
                        selected.append((selectedSurf, card.rect))
                      else:
                        selected.append((selectedSurfTapped, card.tapped_rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      if card.ready:
                        selected.remove((selectedSurf, card.rect))
                      else:
                        selected.remove((selectedSurfTapped, card.tapped_rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
              elif canHit == "either": # this means I can select multiples, but only all from same side
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True not in friend:
                  friend = [pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True in friend and (not retVal or retVal[0][0] == "fr"):
                  index = friend.index(True)
                  card = active[targetPool][index]
                  if condition(card):
                    toAdd = ("fr", index)
                    if toAdd not in retVal and len(retVal) < count:
                      if card.ready:
                        selected.append((selectedSurf, card.rect))
                      else:
                        selected.append((selectedSurfTapped, card.tapped_rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      if card.ready:
                        selected.remove((selectedSurf, card.rect))
                      else:
                        selected.remove((selectedSurfTapped, card.tapped_rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in inactive[targetPool]]
                if True in foe and (not retVal or retVal[0][0] == "fo"):
                  index = foe.index(True)
                  card = inactive[targetPool][index]
                  if condition(card):
                    toAdd = ("fo", index)
                    if toAdd not in retVal and len(retVal) < count:
                      if card.ready:
                        selected.append((selectedSurf, card.rect))
                      else:
                        selected.append((selectedSurfTapped, card.tapped_rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      if card.ready:
                        selected.remove((selectedSurf, card.rect))
                      else:
                        selected.remove((selectedSurfTapped, card.tapped_rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
              elif canHit == "enemy": # this means I can only target unfriendlies
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in inactive[targetPool]]
                if True in foe:
                  index = foe.index(True)
                  card = inactive[targetPool][index]
                  if condition(card):
                    toAdd = ("fo", index)
                    if toAdd not in retVal and len(retVal) < count:
                      if card.ready:
                        selected.append((selectedSurf, card.rect))
                      else:
                        selected.append((selectedSurfTapped, card.tapped_rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      if card.ready:
                        selected.remove((selectedSurf, card.rect))
                      else:
                        selected.remove((selectedSurfTapped, card.tapped_rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
              elif canHit == "friend": # this means I can only target friendlies
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True not in friend:
                  friend = [pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True in friend:
                  index = friend.index(True)
                  card = active[targetPool][index]
                  if condition(card):
                    toAdd = ("fr", index)
                    if toAdd not in retVal and len(retVal) < count:
                      if card.ready:
                        selected.append((selectedSurf, card.rect))
                      else:
                        selected.append((selectedSurfTapped, card.tapped_rect))
                      retVal.append(toAdd)
                    elif toAdd in retVal:
                      retVal.remove(toAdd)
                      if card.ready:
                        selected.remove((selectedSurf, card.rect))
                      else:
                        selected.remove((selectedSurfTapped, card.tapped_rect))
                  else:
                    pyautogui.alert(con_message)
                    self.cardChanged()
                    break
          else:
            if canHit == "enemy":
              hand = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.hand]
              if True in hand:
                index = hand.index(True)
                card = self.activePlayer.hand[index]
                if condition(card):
                  toAdd = ("fo", index)
                  if toAdd not in retVal and len(retVal) < count:
                    selected.append((selectedSurf, card.rect))
                    retVal.append(toAdd)
                  elif toAdd in retVal:
                    retVal.remove(toAdd)
                    selected.remove((selectedSurf, card.rect))
                else:
                  pyautogui.alert(con_message)
                  self.cardChanged()
                  break
            else:
              hand = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.hand]
              if True in hand:
                index = hand.index(True)
                card = self.activePlayer.hand[index]
                if condition(card):
                  toAdd = ("fr", index)
                  if toAdd not in retVal and len(retVal) < count:
                    selected.append((selectedSurf, card.rect))
                    retVal.append(toAdd)
                  elif toAdd in retVal:
                    retVal.remove(toAdd)
                    selected.remove((selectedSurf, card.rect))
                else:
                  pyautogui.alert(con_message)
                  self.cardChanged()
                  break
      if not full or (full and len(retVal) == count):
        confirmBack.fill(COLORS["LIGHT_GREEN"])
      else:
        confirmBack.fill(COLORS["GREEN"])
      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      pygame.display.flip()
      self.extraDraws = []
  
                #####################
                # End of Game Class #
                #####################

def developer(game):
  """Developer functions for manually changing the game state.
  """


