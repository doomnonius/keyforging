from types import LambdaType
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, SRCALPHA, KEYDOWN, QUIT
from pygame import Rect, Surface
import decks.decks as deck
import cards.cardsAsClass as card
from cards.cardsAsClass import Invisicard
import cards.upgrades as upgrade # pylinter thinks this isn't used, but it is, just in an eval() statement
import json, random, logging, pygame, pyautogui
from helpers import return_card, willEnterReady, destroy
from cards.destroyed import basicDest, basicLeaves
from cards.reap import basicReap, spectral_tunneler as st
from typing import List, Tuple
from constants import COLORS, WIDTH, HEIGHT, CARDH, CARDW, OB

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
    self.miniRectsEnemy = []
    self.miniRectsFriend = []
    self.activeHouse = []
    self.extraFightHouses = []
    self.extraUseHouses = []
    self.playedThisTurn = {}
    self.discardedThisTurn = []
    self.usedThisTurn = {}
    self.playedLastTurn = []
    self.discardLastTurn = []
    self.usedLastTurn = []
    self.forgedThisTurn = []
    self.forgedLastTurn = []
    self.destInFight = []
    self.turnStage = None
    self.pendingReloc = []
    self.extraDraws = []
    self.dataBlits = []
    self.cardBlits = []
    self.highlight = []
    self.resetCard = []
    self.resetStates = []
    self.resetStatesNext = []
    # draw bools
    self.mini = False
    self.act = False
    self.ref_image = None
    self.ref_image_rect = Rect(-500, -500, 1, 1)
    self.ref_orig_image = None
    self.ref_orig_rect = None
    self.remaining = True
    self.drawAction = True
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
    self.FPS = 40
    self.WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=SRCALPHA) #, flags = pygame.FULLSCREEN)
    self.SMALLFONT = pygame.font.SysFont("Corbel", max(HEIGHT // 45, 14))
    self.BASICFONT = pygame.font.SysFont("Corbel", HEIGHT // 27)
    self.OTHERFONT = pygame.font.SysFont("Corbel", HEIGHT // 14)
    self.SYMBOLFONT = pygame.font.SysFont("Corbel", 30)
    self.margin = HEIGHT // 108
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
    logging.info("pygame initialized")
    pygame.display.set_caption(f'Keyforge: {self.activePlayer.name} vs {self.inactivePlayer.name}')
    logging.info(f'{self.activePlayer.name} vs {self.inactivePlayer.name}')
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
    retVal = []
    card = self.activePlayer.board[loc][cardNum]
    if not card.ready:
      return ["You can't use a card that isn't ready.", "Details"]
    if self.canFight(card, reset=False, r_click = True):
      retVal.append("Fight")
    if self.canReap(card, reset=False, r_click = True):
      retVal.append("Reap")
    if self.canAction(card, reset=False, r_click = True):
      retVal.append("Action")
    if self.canOmni(card, reset=False):
      retVal.append("Omni")
    if card.type == "Creature" and card.stun and retVal: # have to be able to use a card to unstun, so this is perfect
      return ["Unstun", "Details"]
    retVal.append("Details")
    if not retVal:
      return ["You can't use this card right now."]
    return retVal

  def handOptions(self, cardNum: int) -> List:
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
    self.mat2 = Surface((wid, hei // 2))
    self.mat2.convert()
    self.mat2_rect = self.mat2.get_rect()
    mat_third = (self.mat2.get_height()) // 3
    self.mat2.fill(COLORS["BLACK"])
    self.mat2_rect.topleft = (0, -mat_third // 2)
    self.board_blits.append((self.mat2, self.mat2_rect))

    # hand
    self.hand2 = Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.hand2.convert()
    self.hand2.fill(COLORS["GREY"])
    self.hand2_rect = self.hand2.get_rect()
    self.hand2_rect.topleft = (0, -mat_third // 2)
    self.board_blits.append((self.hand2, self.hand2_rect))

    # artifacts
    self.artifacts2 = Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.artifacts2.convert()
    self.artifacts2.fill(COLORS["GREY"])
    self.artifacts2_rect = self.artifacts2.get_rect()
    self.artifacts2_rect.topleft = (0, mat_third // 2)
    self.board_blits.append((self.artifacts2, self.artifacts2_rect))

    # discard
    self.discard2 = Surface((self.target_cardw, mat_third))
    self.discard2.convert()
    self.discard2.fill(COLORS["GREY"])
    self.discard2_rect = self.discard2.get_rect()
    self.discard2_rect.topright = (wid, 0)
    self.board_blits.append((self.discard2, self.discard2_rect))

    # creatures
    self.creatures2 = Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.creatures2.convert()
    self.creatures2.fill(COLORS["GREY"])
    self.creatures2_rect = self.creatures2.get_rect()
    self.creatures2_rect.topleft = (0, int(mat_third * 1.5))
    self.board_blits.append((self.creatures2, self.creatures2_rect))

    # deck
    self.deck2 = Surface((self.target_cardw, mat_third))
    self.deck2.convert()
    self.deck2.fill(COLORS["GREY"])
    self.deck2_rect = self.deck2.get_rect()
    self.deck2_rect.topright = (wid, mat_third)
    self.board_blits.append((self.deck2, self.deck2_rect))

    # purged2
    self.purge2 = Surface((self.target_cardw, mat_third // 2))
    self.purge2.convert()
    self.purge2_rect = self.purge2.get_rect()
    self.purge2_rect.topright = (wid, mat_third * 2)
    self.board_blits.append((self.purge2, self.purge2_rect))

    ## divider2
    self.divider2 = Surface((wid // 5, mat_third))
    self.divider2.convert()
    self.divider2.fill(COLORS["GREY"])
    self.divider2_rect = self.divider2.get_rect()
    self.divider2_rect.topright = (wid, int(mat_third * 2.5))
    self.board_blits.append((self.divider2, self.divider2_rect))

    # archive2
    self.archive2 = Surface((self.target_cardw + self.margin, mat_third))
    self.archive2.convert()
    self.archive2.fill(COLORS["BROWN"])
    self.archive2_rect = self.archive2.get_rect()
    self.archive2_rect.topright = (wid, int(mat_third * 2.5))
    self.board_blits.append((self.archive2, self.archive2_rect))

    ## divider1
    self.divider = Surface((wid // 5, mat_third))
    self.divider.convert()
    self.divider.fill(COLORS["GREEN"])
    self.divider_rect = self.divider.get_rect()
    self.divider_rect.topleft = (0, int(mat_third * 2.5))
    self.board_blits.append((self.divider, self.divider_rect))

    # archive
    self.archive1 = Surface((self.target_cardw + self.margin, mat_third))
    self.archive1.convert()
    self.archive1.fill(COLORS["BROWN"])
    self.archive1_rect = self.archive1.get_rect()
    self.archive1_rect.topleft = (0, int(mat_third * 2.5))
    self.board_blits.append((self.archive1, self.archive1_rect))

    ## active mat
    self.mat1 = Surface((wid, hei // 2))
    self.mat1.convert()
    self.mat1.fill(COLORS["BLACK"])
    self.mat1_rect = self.mat1.get_rect()
    self.mat1_rect.topleft = (0, int(mat_third * 3.5))
    self.board_blits.append((self.mat1, self.mat1_rect))

    # purged
    self.purge1 = Surface((self.target_cardw, mat_third // 2))
    self.purge1.convert()
    self.purge1_rect = self.purge1.get_rect()
    self.purge1_rect.topleft = (0, int(mat_third * 3.5))
    self.board_blits.append((self.purge1, self.purge1_rect))

    # deck
    self.deck1 = Surface((self.target_cardw, mat_third))
    self.deck1.convert()
    self.deck1.fill(COLORS["GREEN"])
    self.deck1_rect = self.deck1.get_rect()
    self.deck1_rect.topleft = (0, mat_third * 4)
    self.board_blits.append((self.deck1, self.deck1_rect))

    # creatures
    self.creatures1 = Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.creatures1.convert()
    self.creatures1.fill(COLORS["GREEN"])
    self.creatures1_rect = self.creatures1.get_rect()
    self.creatures1_rect.topright = (wid, int(mat_third * 3.5))
    self.board_blits.append((self.creatures1, self.creatures1_rect))

    # discard
    self.discard1 = Surface((self.target_cardw, mat_third))
    self.discard1.convert()
    self.discard1.fill(COLORS["GREEN"])
    self.discard1_rect = self.discard1.get_rect()
    self.discard1_rect.bottomleft = (0, HEIGHT)
    self.board_blits.append((self.discard1, self.discard1_rect))

    # artifacts
    self.artifacts1 = Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.artifacts1.convert()
    self.artifacts1.fill(COLORS["GREEN"])
    self.artifacts1_rect = self.artifacts1.get_rect()
    self.artifacts1_rect.topright = (wid, int(mat_third * 4.5))
    self.board_blits.append((self.artifacts1, self.artifacts1_rect))

    # hand
    self.hand1 = Surface((wid - (self.target_cardw + self.margin), mat_third))
    self.hand1.convert()
    self.hand1.fill(COLORS["GREEN"])
    self.hand1_rect = self.hand1.get_rect()
    self.hand1_rect.topright = (wid, int(mat_third * 5.5))
    self.board_blits.append((self.hand1, self.hand1_rect))

    ## neutral zone - easier if we have this and can blit to it's dimensions
    self.neutral = Surface(((wid // 5) * 3, mat_third))
    self.neutral.convert()
    self.neutral.fill(COLORS["BLACK"])
    self.neutral_rect = self.neutral.get_rect()
    self.neutral_rect.topleft = (self.divider.get_width(), int(mat_third * 2.5))
    self.board_blits.append((self.neutral, self.neutral_rect))

    # action surf
    self.actionBackSurf = Surface(((((mat_third * 2) // 7) * 5), mat_third * 2))
    self.actionBackSurf.convert_alpha()
    self.actionBackSurf.set_alpha(150)
    self.actionBackSurf.fill(COLORS["GREY"])
    self.actionBackRect = self.actionBackSurf.get_rect()
    self.actionBackRect.bottomleft = (0, self.divider_rect.top)

    # action close button
    self.actionMin = self.SYMBOLFONT.render("<", 1, COLORS['RED'])
    self.actionMinRect = self.actionMin.get_rect()
    self.actionMinRect.topright = self.actionBackRect.topright

    # action open button
    self.actionMax = self.SYMBOLFONT.render(">", 1, COLORS["RED"])
    self.actionMaxRect = self.actionMax.get_rect()
    self.actionMaxRect.topleft = (0, self.actionBackRect.top)

    # end turn
    self.endText = self.OTHERFONT.render(f"  End Turn  ", 1, COLORS['WHITE'])
    self.endRect = self.endText.get_rect()
    self.endBack = Surface((self.endText.get_width() + 10, self.endText.get_height() + 10))
    self.endBack.convert()
    self.endBack.fill(COLORS["GREEN"])
    self.endBackRect = self.endBack.get_rect()
    self.endBackRect.topright = (self.neutral_rect.right - self.margin, self.neutral_rect.top + self.margin)
    self.endRect.center = self.endBackRect.center

    self.setKeys()

    # check warning
    self.warnSurf = Surface((self.amber2.get_size()))
    self.warnSurf.fill(COLORS["RED"])
    self.warnRect = self.warnSurf.get_rect()
    self.warnRect.topleft = self.amber2_rect.topleft

    # log and other options submenu

    run = True

    while run:
      self.CLOCK.tick(self.FPS)

      for event in pygame.event.get():
        
        if event.type == MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = event.pos
          if not self.remaining or Rect.collidepoint(self.endBackRect, (self.mousex, self.mousey)):
            self.endBack.fill(COLORS["LIGHT_GREEN"])
          else:
            self.endBack.fill(COLORS["GREEN"])

        if event.type == QUIT:
          run = False

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
          self.hovercard = []
          self.draw() # this only works because of the display.update in doPopup
          self.doPopup()
          
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          hand = self.activePlayer.hand
          hit = [Rect.collidepoint(x.rect, (self.mousex, self.mousey)) for x in hand]
          if True in hit and True not in self.friendDraws:
            self.dragging.append(hand.pop(hit.index(True)))
            self.dragCard()
            # logging.info("Exiting dragCard, back into events.")

        
        if event.type == MOUSEBUTTONUP and event.button == 1:
          if self.dragging: # this should never trigger, because if I'm dragging something i should be in the the self.dragCard() loop
            self.activePlayer.hand.append(self.dragging.pop())
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if Rect.collidepoint(self.endBackRect, (self.mousex, self.mousey)):
            if self.remaining:
              answer = self.chooseHouse("custom", ("Are you sure you want to end your turn?", ["Yes", "No"]), highlight = lambda x: x.house in self.activeHouse and (x in self.activePlayer.hand or x.ready))[0]
              if answer == "No":
                for c in self.activePlayer.hand + self.activePlayer.board["Creature"] + self.activePlayer.board["Artifact"]:
                  c.selected = False
                break
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.inactivePlayer.discard + self.activePlayer.discard + self.activePlayer.purged + self.inactivePlayer.purged + self.activePlayer.archive + self.inactivePlayer.archive:
              card.rect.topleft = OB
            self.turnStage += 1
          elif True in self.friendDraws and Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
              card.rect.topleft = OB
            self.cardChanged()
          elif True in self.enemyDraws and Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
              card.rect.topleft = OB
            self.cardChanged()
          elif not self.drawFriendDiscard and Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          elif not self.drawFriendPurge and Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
            self.drawFriendPurge = True
          elif not self.drawEnemyPurge and Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
            self.drawEnemyPurge = True
          elif not self.drawFriendArchive and Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
            self.drawFriendArchive = True
          elif not self.drawEnemyArchive and Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
            self.drawEnemyArchive = True
          
        if event.type == KEYDOWN:
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
          self.activePlayer += 7
          self.activePlayer.hand.sort(key = lambda x: x.house)
        else:
          mull = self.chooseHouse("custom", ("Player 1, would you like to keep or mulligan?", ["Keep", "Mulligan"]), ["GREEN", "RED"])[0]
          if mull == "Mulligan":
            logging.info("Player 1 has mulliganed.")
            for card in self.activePlayer.hand:
              self.activePlayer.deck.append(card)
            random.shuffle(self.activePlayer.deck)
            self.activePlayer.hand = []
            self.activePlayer += 6
            self.activePlayer.hand.sort(key = lambda x: x.house)
        if not self.do:
          self.inactivePlayer += 6
          self.inactivePlayer.hand.sort(key = lambda x: x.house)
        else:
          mull2 = self.chooseHouse("custom", ("Player 2, would you like to keep or mulligan?", ["Keep", "Mulligan"]), ["GREEN", "RED"])[0]
          if mull2 == "Mulligan":
            logging.info("Player 2 has mulliganed.")
            for card in self.inactivePlayer.hand:
              self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
            self.activePlayer.hand.sort(key = lambda x: x.house)
          self.turnNum = 1
          self.turnStage = 0
        self.cardChanged()
        self.do = True

      ###################################
      # Step 0: "Start of turn" effects #
      ###################################

      elif self.turnStage == 0:
        logging.info(f"Starting turn {self.turnNum}")
        # start of turn effects will go here
        self.turnStage += 1
      
      ###################################################
      # step 1: check if a key is forged, then forge it #
      ###################################################

      elif self.turnStage == 1: # forge a key
        if self.canForge(): # returns True if you can forge, false if you can't (and why you can't), which in CotA is basically only Miasma
          self.forgeKey("active", self.calculateCost())
        if self.activePlayer.keys >= 3:
          pyautogui.alert(f"{self.activePlayer.name} wins!")
          logging.info(f"{self.activePlayer.name} wins!")
          run = False
        self.turnStage += 1
      
      ######################################
      # step 2: the player chooses a house #
      # and if to pick up their archive    #
      ######################################

      elif self.turnStage == 2: # choose a house, optionally pick up archive
        archive = self.activePlayer.archive
        self.activeHouse = self.chooseHouse("activeHouse")
        print(self.activeHouse)
        for c in self.activePlayer.board["Creature"] + self.activePlayer.board["Artifact"] + self.activePlayer.hand:
          c.selected = False
        self.cardChanged()
        if "jehu_the_bureaucrat" in self.activePlayer.board["Creature"] and "Sanctum" in self.activeHouse:
          self.activePlayer.gainAmber(2, self)
        highSurf = Surface(self.house1a.get_size())
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
            logging.info(f"{self.inactivePlayer.name} wins!")
            run = False
          elif self.response == "Quit":
            run = False
          
          elif self.response == "Play":
            self.playCard(self.targetCard)
          elif self.response == "Fight":
            self.fightCard(self.targetCard)
          elif self.response == "Discard":
            if len(self.playedThisTurn) + len(self.discardedThisTurn) >= 1 and self.turnNum == 1: # I shouldn't actually be able to get here I think
              logging.info("You've already taken your one action for turn one.")
            else:
              self.discardCard(self.targetCard)
          elif self.response == "Action":
            self.actionCard(self.targetCard, self.loc)
          elif self.response == "Reap":
            self.reapCard(self.targetCard)
          elif self.response == "Omni":
            self.omniCard(self.targetCard, self.loc)
          elif self.response == "Unstun":
            self.activePlayer.board["Creature"][self.targetCard].stun = False
            self.activePlayer.board["Creature"][self.targetCard].ready = False
            self.cardChanged()
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

        for creature in self.activePlayer.board["Creature"]:
          for e in creature.eot:
            e(self, creature)
        for creature in self.inactivePlayer.board["Creature"]:
          for e in creature.eot:
            e(self, creature)
        for creature in self.activePlayer.board["Creature"]:
          creature.resetArmor(self)
        for creature in self.inactivePlayer.board["Creature"]:
          creature.resetArmor(self)
        if self.forgedThisTurn:
          self.forgedLastTurn = self.forgedThisTurn.copy()
        else:
          self.forgedThisTurn = []
        self.activeHouse = []
        self.extraFightHouses = []
        self.extraUseHouses = []
        self.playedLastTurn = self.playedThisTurn.copy()
        self.playedThisTurn = {}
        self.discardedLastTurn = self.discardedThisTurn.copy()
        self.discardedThisTurn = []
        self.usedLastTurn = self.usedThisTurn.copy()
        self.usedThisTurn = {}
        self.destInFight = []
        self.remaining = True
        if self.resetStates:
          for key in self.resetStates:
            logging.info(f"Reseting {key[1]}'s state.")
            if key[0] == "a":
              self.activePlayer.states[key[1]] = 0
            if key[0] == "i":
              self.inactivePlayer.states[key[1]] = 0
        for c, toReset in self.resetCard:
          logging.info(f"Resetting {toReset.title}.")
          if toReset == "house":
            c.house = c.cardInfo["house"]
          elif toReset == "damagable":
            c.damagable = True
          elif toReset == "st":
            c.reap.remove(st)
        self.resetStates = self.resetStatesNext.copy()
        self.resetStatesNext = []
        self.endBack.fill(COLORS["GREEN"])
        if self.activePlayer.amber >= self.calculateCost(): # I'm ruling that this is the rule for declaring check - extra amber on Pocket Universe, etc doesn't count here
          pyautogui.alert(f"Check for key {self.activePlayer.keys + 1}!")
        self.highlight = []
        # switch players
        self.switch()
        self.cardChanged()
        self.setKeys()
        self.turnNum += 1
        self.turnStage = 0
        logging.info(f"Ending turn {self.turnNum}")
      
      
      self.draw() # this will need hella updates
      pygame.display.flip()

    pygame.quit()


  def check_hover (self):
    if self.dragging:
      return

    self.mini = False
    self.act = False

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
      if Rect.collidepoint(card.rect, (self.mousex, self.mousey)):
        self.hovercard = [card]
        return
      if Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)):
        self.hovercard = [card]
        return

    for loc in hoverable2:
      if Rect.collidepoint(loc, (self.mousex, self.mousey)):
        self.hovercard = [loc]
        return

    friendMinis = [Rect.collidepoint(x[0], (self.mousex, self.mousey)) for x in self.miniRectsFriend]
    enemyMinis = [Rect.collidepoint(x[0], (self.mousex, self.mousey)) for x in self.miniRectsEnemy]
    if Rect.collidepoint(self.ref_image_rect, (self.mousex, self.mousey)):
      self.hovercard = [self.ref_image_rect]
    elif True in friendMinis:
      i = friendMinis.index(True)
      self.hovercard = [self.miniRectsFriend[i][1]]
      self.mini = True
      return
    elif True in enemyMinis:
      i = enemyMinis.index(True)
      self.hovercard = [self.miniRectsEnemy[i][1]]
      self.mini = True
      return

    if self.drawAction and Rect.collidepoint(self.ref_image_rect, (self.mousex, self.mousey)):
      self.hovercard = [(self.ref_orig_image, self.ref_orig_rect)]
      self.act = True
      return


  def draw(self, drawEnd: bool = True):
    # self.allsprites.update()
    self.WIN.blits(self.board_blits)
    if self.highlight:
      self.WIN.blits(self.highlight)
    self.WIN.blits(self.dataBlits)
    
    # self.allsprites.draw(self.WIN)
    if drawEnd and self.activeHouse:
      self.WIN.blit(self.endBack, self.endBackRect)
      self.WIN.blit(self.endText, self.endRect)
    # draw discards/archive/purges
    if self.drawFriendDiscard or self.drawFriendArchive or self.drawFriendPurge:
      # if self.drawFriendDiscard:
      #   pool = self.activePlayer.discard
      # elif self.drawFriendArchive:
      #   pool = self.activePlayer.archive
      # else:
      #   pool = self.activePlayer.purged
      # discard back
      discardBackSurf = Surface((self.WIN.get_width(), self.WIN.get_height() * 5 // 12))
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
      closeBackSurf = Surface((closeSurf.get_size()))
      closeBackSurf.convert()
      closeBackSurf.fill(COLORS["RED"])
      self.closeFriendDiscard = closeBackSurf.get_rect()
      self.closeFriendDiscard.top = closeRect.top
      self.closeFriendDiscard.centerx = WIDTH // 2
      self.WIN.blit(discardBackSurf, discardBackRect)
      self.WIN.blit(closeBackSurf, self.closeFriendDiscard)
      self.WIN.blit(closeSurf, closeRect)
      # draw cards
      # x = 0
      # for card in pool[0:16]:
      #   card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + self.margin)
      #   x += 1
      #   self.WIN.blit(card.image, card.rect)
      # x = 0
      # for card in pool[16:32]:
      #   card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 2 * self.margin + self.target_cardh)
      #   x += 1
      #   self.WIN.blit(card.image, card.rect)
      # for card in pool[32:]:
      #   card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 3 * self.margin + 2 * self.target_cardh)
      #   x += 1
      #   self.WIN.blit(card.image, card.rect)
    
    if self.drawEnemyDiscard or self.drawEnemyArchive or self.drawEnemyPurge:
      # if self.drawEnemyDiscard:
      #   pool = self.inactivePlayer.discard
      # elif self.drawEnemyArchive:
      #   pool = self.inactivePlayer.archive
      # else:
      #   pool = self.inactivePlayer.purged
      # discard back
      discardBackSurf = Surface((self.WIN.get_width(), self.WIN.get_height() * 5 // 12))
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
      closeBackSurf = Surface((closeSurf.get_size()))
      closeBackSurf.convert()
      closeBackSurf.fill(COLORS["RED"])
      self.closeEnemyDiscard = closeBackSurf.get_rect()
      self.closeEnemyDiscard.top = closeRect.top
      self.closeEnemyDiscard.centerx = WIDTH // 2
      self.WIN.blit(discardBackSurf, discardBackRect)
      self.WIN.blit(closeBackSurf, self.closeEnemyDiscard)
      self.WIN.blit(closeSurf, closeRect)
      # draw cards
      # x = 0
      # for card in pool[0:16]:
      #   card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + self.margin)
      #   x += 1
      #   self.WIN.blit(card.image, card.rect)
      # x = 0
      # for card in pool[16:32]:
      #   card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 2 * self.margin + self.target_cardh)
      #   x += 1
      #   self.WIN.blit(card.image, card.rect)
    
    if self.cardBlits:
      self.WIN.blits(self.cardBlits)
    
    if self.extraDraws:
      for thing, location in self.extraDraws:
        self.WIN.blit(thing, location)
    
    if self.hovercard:
      hover = self.hovercard[0]
      if self.mini or self.act: # in this case hovercard will be a tuple
        hover, hover_rect = hover[0], hover[1]
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
      elif type(hover) != Rect and type(hover) != Invisicard:
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
        hover_back = Surface(hover.get_size())
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
      in_hand = [Rect.collidepoint(x.rect, pos) for x in self.activePlayer.hand]
      in_creature = [(Rect.collidepoint(x.rect, pos) or Rect.collidepoint(x.tapped_rect, pos)) for x in self.activePlayer.board["Creature"]]
      in_artifact = [(Rect.collidepoint(x.rect, pos) or Rect.collidepoint(x.tapped_rect, pos)) for x in self.activePlayer.board["Artifact"]]
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
        if e.type == QUIT:
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
    popupSurf = Surface((w, pygame.font.Font.get_linesize(self.BASICFONT)*len(options)))
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
      if Rect.collidepoint(textRect, (self.mousex, self.mousey)):
        return options[i]


  def make_popup(self, options, pos):
    w = max(x.get_width()+self.margin for x in [self.BASICFONT.render(y, 1, COLORS['BLUE']) for y in options])
    bot_offset = right_offset = 0
    popupSurf = Surface((w, pygame.font.Font.get_linesize(self.BASICFONT)*len(options)))
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
      textSurf = self.BASICFONT.render(options[i], 1, COLORS["WHITE"])
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
      self.key2y, self.key2y_rect = self.inactivePlayer.key_forged_y
    else:
      self.key2y, self.key2y_rect = self.inactivePlayer.key_y
    self.key2y_rect.topright = (WIDTH - (2 + self.target_cardw + self.margin), self.divider2_rect.top)
    
    if self.inactivePlayer.red:
      self.key2r, self.key2r_rect = self.inactivePlayer.key_forged_r
    else:
      self.key2r, self.key2r_rect = self.inactivePlayer.key_r
    self.key2r_rect.midright = (WIDTH - (2 + self.target_cardw + self.margin), self.divider2_rect.centery)
    
    if self.inactivePlayer.blue:
      self.key2b, self.key2b_rect = self.inactivePlayer.key_forged_b
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
      self.key1y, self.key1y_rect = self.activePlayer.key_forged_y
    else:
      self.key1y, self.key1y_rect = self.activePlayer.key_y
    self.key1y_rect.topleft = (2 + self.target_cardw + self.margin, self.divider_rect.top)

    if self.activePlayer.red:
      self.key1r, self.key1r_rect = self.activePlayer.key_forged_r
    else:
      self.key1r, self.key1r_rect = self.activePlayer.key_r
    self.key1r_rect.midleft = (2 + self.target_cardw + self.margin, self.divider_rect.centery)
    
    if self.activePlayer.blue:
      self.key1b, self.key1b_rect = self.activePlayer.key_forged_b
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
    self.amber1_rect.topleft = (2 + self.target_cardw + 10 + self.key1y.get_width(), self.mat2_rect[1] + self.mat2_rect[3] + (2 * self.margin))

    # key cost
    self.cost1 = self.BASICFONT.render(f"Cost: {self.calculateCost('active')}", 1, COLORS['WHITE'])
    self.cost1_rect = self.cost1.get_rect()
    self.cost1_rect.midleft = (2 + self.target_cardw + 10 + self.key1y.get_width(), self.divider2_rect.centery)

    # chains
    self.chains1 = self.BASICFONT.render(f"{self.activePlayer.chains} chains", 1, COLORS['WHITE'])
    self.chains1_rect = self.chains1.get_rect()
    self.chains1_rect.bottomleft = (2 + self.target_cardw + 10 + self.key1y.get_width(), self.mat1_rect[1] - (2 * self.margin))
   
    # amber
    self.amber2 = self.BASICFONT.render(f"{self.inactivePlayer.amber} amber", 1, COLORS['BLACK'])
    self.amber2_rect = self.amber2.get_rect()
    self.amber2_rect.topright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key1y.get_width(), self.mat2_rect[1] + self.mat2_rect[3] + (2 * self.margin))

    # key cost
    self.cost2 = self.BASICFONT.render(f"Cost: {self.calculateCost('inactive')}", 1, COLORS['BLACK'])
    self.cost2_rect = self.cost2.get_rect()
    self.cost2_rect.midright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key1y.get_width(), self.divider2_rect.centery)

    # chains
    self.chains2 = self.BASICFONT.render(f"{self.inactivePlayer.chains} chains", 1, COLORS['BLACK'])
    self.chains2_rect = self.chains2.get_rect()
    self.chains2_rect.bottomright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key1y.get_width(), self.mat1_rect[1] - (2 * self.margin))

    if self.inactivePlayer.amber >= self.calculateCost("inactive"):
      self.warnRect.topleft = self.amber2_rect.topleft
      self.dataBlits = [(self.warnSurf, self.warnRect)]
    else:
      self.dataBlits = []
    self.dataBlits += [(self.key1y, self.key1y_rect), (self.key1r, self.key1r_rect), (self.key1b, self.key1b_rect), (self.key2y, self.key2y_rect), (self.key2r, self.key2r_rect), (self.key2b, self.key2b_rect), (self.house2a, self.house2a_rect), (self.house2b, self.house2b_rect), (self.house2c, self.house2c_rect), (self.house1a, self.house1a_rect), (self.house1b, self.house1b_rect), (self.house1c, self.house1c_rect), (self.amber1, self.amber1_rect), (self.amber2, self.amber2_rect), (self.chains1, self.chains1_rect), (self.chains2, self.chains2_rect), (self.cost1, self.cost1_rect), (self.cost2, self.cost2_rect)]
  
  def calculateCost(self, side: str = "active"):
    """ Calculates the cost of a key considering current board state. For future proofing, have to consider that the inactive player can potentially forge a key.
    """
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    activeA = self.activePlayer.board["Artifact"]
    inactiveA = self.inactivePlayer.board["Artifact"]
    activeS = self.activePlayer.states
    inactiveS = self.inactivePlayer.states
    cost = 6
    if side == "active":
      for c in inactiveA:
        if c.title == "iron_obelisk":
          cost += sum(x.damage > 0 and (x.house == "Brobnar" or "experimental_therapy" in [y.title for y in x.upgrade]) for x in inactive)
      if "lash_of_broken_dreams" in inactiveS:
        cost += 3 * activeS["lash_of_broken_dreams"]
      for c in inactive:
        if "jammer_pack" in [x.title for x in c.upgrade]:
          cost += 2
        if c.title == "grabber_jammer":
          cost += 1
        elif c.title == "titan_mechanic" and c.isFlank(self):
          cost -= 1
        elif c.title == "murmook":
          cost += 1
      for c in active:
        if c.title == "titan_mechanic" and c.isFlank(self):
          cost -= 1
    else:
      for c in activeA:
        if c.title == "iron_obelisk":
          cost += sum(x.damage > 0 and (x.house == "Brobnar" or "experimental_therapy" in [y.title for y in x.upgrade]) for x in active)
      if "lash_of_broken_dreams" in activeS:
        cost += 3 * activeS["lash_of_broken_dreams"]
      for c in active:
        if "jammer_pack" in [x.title for x in c.upgrade]:
          cost += 2
        if c.title == "grabber_jammer":
          cost += 1
        elif c.title == "titan_mechanic" and c.isFlank(self):
          cost -= 1
        elif c.title == "murmook":
          cost += 1
      for c in inactive:
        if c.title == "titan_mechanic" and c.isFlank(self):
          cost -= 1

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
    activeA = self.activePlayer.board["Artifact"]
    if "miasma" in self.inactivePlayer.states and self.inactivePlayer.states["miasma"]:
      logging.info("You skip your forge a key step this turn because your opponent played 'Miasma' last turn.")
      self.inactivePlayer.states["miasma"] = 0
      return False
    if "the_sting" in [x.title for x in self.activePlayer.board["Artifact"]]:
      logging.info("You skip your forge a key step this turn because you have 'The Sting' in play.")
      return False
    if "pocket_universe" in activeA:
      initial = self.activePlayer.amber
      initial += sum(x.captured for x in activeA if x.title == "pocket_universe")
      if initial < self.calculateCost():
        return False
    return True
    

##################
# Card functions #
##################

  def actionCard(self, cardNum: int, loc: str, cheat: bool = False):
    """ Trigger a card's action from within the turn.
    """
    card = self.activePlayer.board[loc][cardNum]
    if not self.canAction(card, r_click=True, cheat=cheat):
      logging.info(f"{card.title} can't use action/omni right now")
      return
    if card.type == "Creature" and card.stun:
      logging.info("Creature is stunned and unable to act. Unstunning creature instead.")
      card.stun = False
      card.ready = False
      if card not in self.usedThisTurn:
        self.usedThisTurn[card] = 1
      else:
        self.usedThisTurn[card] += 1
      self.cardChanged()
      return
    if len(card.action) > 1:
      pass # TODO: choose which action to do
    else:
      for a in card.action:
        a(self, card)
    card.ready = False
    if card.type == "Artifact" and "veylan_analyst" in self.activePlayer.board["Creature"]:
      logging.info("Veylan Analyst gives you 1 amber for using an artifact.")
    if card not in self.usedThisTurn:
      self.usedThisTurn[card] = 1
    else:
      self.usedThisTurn[card] += 1
    self.cardChanged(True)
  
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
    if self.canDiscard(card, cheat = cheat):
      self.activePlayer.discard.append(self.activePlayer.hand.pop(cardNum))
      self.cardChanged()
      if "rock_hurling_giant" in [x.title for x in active] and card.house == "Brobnar":
        target = self.chooseCards("Creature", "Deal 4 damage to:")
        if target:
          target = target[0]
        target.damageCalc(self, 4)
        target.updateHealth()
        if target.destroyed:
          pending.append(target)
        self.pending()
      self.discardedThisTurn.append(card)
    self.cardChanged(True)


  def fightCard(self, attacker: int, cheat: bool = True, defender = None):
    """ This is needed for cards that trigger fights (eg anger, gauntlet of command). If attacker is fed in to the function (which will only be done by cards that trigger fights), the house check is skipped.
    """
    # This will actually probably need to be incorporated into the main loop in some way
    card = self.activePlayer.board["Creature"][attacker]
    # this check is also in cardOptions, but sometimes things let you trigger a fight other ways
    if len(self.inactivePlayer.board["Creature"]) == 0:
      logging.info("Fight canceled because no opposing creatures.")
      return self
    if not self.canFight(card, cheat=cheat, r_click = True):
      logging.info("This card can't fight right now.")
    if card.stun:
      logging.info("Creature is stunned and unable to fight. Unstunning creature instead.")
      logging.info(f"Unstunning {card.title}.")
      card.stun = False
      card.ready = False
      if card not in self.usedThisTurn:
        self.usedThisTurn[card] = 1
      else:
        self.usedThisTurn[card] += 1
      self.cardChanged()
      return
    if defender == None:
      if card.title == "bigtwig":
        defender = self.chooseCards("Creature", "Choose an enemy creature to attack:", "enemy", condition = lambda x: (x.taunt or not (True in [y.taunt for y in x.neighbors(self)])) and x.stun, con_message = "This minion is protected by taunt and/or is not stunned.")[0]#[1]
      elif card.title == "niffle_ape":
        defender = self.chooseCards("Creature", "Choose an enemy minion to attack:", "enemy")[0]#[1]
      else:
        defender = self.chooseCards("Creature", "Choose an enemy creature to attack:", "enemy", condition = lambda x: x.taunt or not (True in [y.taunt for y in x.neighbors(self)]), con_message = "This minion is protected by taunt.")[0]#[1]
    if defender == None:
      return
    # defenderCard = self.inactivePlayer.board["Creature"][defender]
    try:
      logging.info("Trying to fight.")
      card.fightCard(defender, self)
    except: logging.info("Fight failed.")
    if card not in self.usedThisTurn:
      self.usedThisTurn[card] = 1
    else:
      self.usedThisTurn[card] += 1
    self.cardChanged(True)

  def omniCard(self, chosen: int, location: str):
    """ This activates Omni abilities.
    """
    card = self.activePlayer.board[location][chosen]
    if not self.canOmni(card):
      logging.info(f"Can't use {card.title} right now.")
    if card.type == "Creature" and card.stun:
      logging.info("Creature is stunned and unable to act. Unstunning creature instead.")
      card.stun = False
      card.ready = False
      if card not in self.usedThisTurn:
        self.usedThisTurn[card] = 1
      else:
        self.usedThisTurn[card] += 1
      self.cardChanged()
      return
    if len(card.omni) > 1:
      pass # TODO: choose which omni to do
    else:
      card.omni(self, card)
    card.ready = False
    if card.type == "Artifact" and "veylan_analyst" in self.activePlayer.board["Creature"]:
      logging.info("Veylan Analyst gives you 1 amber for using an artifact.")
  
  def playCard(self, chosen: int, cheat: str = "Hand", flank = "Right", ask = True):
    """ This is needed for cards that play other cards (eg wild wormhole). Will also simplify responses. Booly is a boolean that tells whether or not to check if the house matches.
    """
    logging.info(f"numPlays: {sum(v for k,v in self.playedThisTurn.items())}")
    if cheat == "Deck":
      source = self.activePlayer.deck
    elif cheat == "Discard":
      source = self.activePlayer.discard
    else:
      source = self.activePlayer.hand
    card = source[chosen]
    if not self.canPlay(card, message = False):
      return
    # cardOptions() makes sure that you can't try to play a card you're not allowed to play
    # canPlay() does the same for drag and drop and cheating out cards
    # Increases amber, adds the card to the action section of the board, then calls the card's play function
    if card.amber > 0:
      self.activePlayer.gainAmber(card.amber, self)
      logging.info(f"{source[chosen].title} gave {self.activePlayer.name} {card.amber} amber. {self.activePlayer.name} now has {self.activePlayer.amber} amber.")
    if ask:
      if card.type == "Creature" and len(self.activePlayer.board["Creature"]) > 0:
        flank = self.chooseFlank(card)
    # left flank
    if card.type != "Upgrade" and flank == "Left":
      self.activePlayer.board[card.type].insert(0, source.pop(chosen))
      logging.info(f"numPlays: {sum(v for k,v in self.playedThisTurn.items())}")
    # default case: right flank
    elif card.type != "Upgrade":
      self.activePlayer.board[card.type].append(source.pop(chosen))
      logging.info(f"numPlays: {sum(v for k,v in self.playedThisTurn.items())}")
    else:
      targeted = self.chooseCards("Creature", "Choose a creature to attach the upgrade to:")
      if targeted:
        targeted = targeted[0]
      self.playUpgrade(card, targeted)
      self.cardChanged()
      return
    #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
    if card not in self.playedThisTurn:
      self.playedThisTurn[card] = 1
    else:
      self.playedThisTurn[card] += 1
    self.cardChanged(True) # definitely need to recalc power here, in case we play something next to a staunch knight so now it is dead
    self.draw()
    pygame.display.update()
    card.play(self, card)
    logging.info(f"{card.title} play ability resolved.")
    logging.info(f"numPlays: {sum(v for k,v in self.playedThisTurn.items())}")
    # if the card is an action, now add it to the discard pile - remote access or poltergeist or nexuss on masterplan can potentially play cards that belong to the other player
    if card.type == "Action":
      if card.title == "library_access":
        if card.deck == self.activePlayer.name:
          self.activePlayer.purged.append(self.activePlayer.board["Action"].pop())
        else:
          self.inactivePlayer.purged.append(self.activePlayer.board["Action"].pop())
      else:
        if card.deck == self.activePlayer.name:
          self.activePlayer.discard.append(self.activePlayer.board["Action"].pop())
        else:
          self.inactivePlayer.discard.append(self.activePlayer.board["Action"].pop())
    self.cardChanged(True)

  def reapCard(self, cardNum: int, cheat:bool = False):
    """ Triggers a card's reap effect from within the turn.
    """
    card = self.activePlayer.board["Creature"][cardNum]
    # check reap states when building cardOptions
    if not self.canReap(card, r_click = True, cheat=cheat):
      logging.info("{card.title} can't reap right now.")
      return
    if card.stun:
      logging.info(f"Unstunning {card.title}.")
      card.stun = False
      card.ready = False
      if card not in self.usedThisTurn:
        self.usedThisTurn[card] = 1
      else:
        self.usedThisTurn[card] += 1
      self.cardChanged()
      return
    basicReap(self, card)
    if card.reap:
      # they'll need to choose the order multiples resolve in
      for r in card.reap:
        r(self, card)
    card.ready = False # commented out for testing
    if card not in self.usedThisTurn:
      self.usedThisTurn[card] = 1
    else:
      self.usedThisTurn[card] += 1
    self.cardChanged(True)

  def forgeKey(self, player: str, cost: int):
    initial_cost = cost
    if cost < 0:
      cost = 0
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
      full_mando = False
      if (diff := -(forger.amber - cost)) > 0:
        optional = False
        mando = True
        collect = sum(x.capture for x in self.activePlayer.board["Artifact"] if x.title == "pocket_universe" or x.title == "safe_place")
        if collect == diff:
          full_mando = True
      else:
        spend = self.chooseHouse("custom", ("Would you like to spend amber from your artifacts?", ["Yes", "No"]))[0]
        if spend == "Yes":
          optional = True
          mando = False
        else:
          optional = False
          mando = False
      if mando:
        while diff > 0:
          for c in self.activePlayer.board["Artifact"]:
            if c.title == "pocket_universe" or c.title == "safe_place" and c.captured > 0:
              reduced = int(self.chooseHouse("custom", (f"How much amber from {c.title.replace('_', ' ').title()} would you like to spend? ({diff} needed)", list(range(c.captured + 1))))[0])
              c.captured -= reduced
              cost -= reduced
              diff -= reduced
      elif full_mando:
        for c in self.activePlayer.board["Artifact"]:
          reduced = c.captured
          c.captured -= reduced
          cost -= reduced
      elif optional:
        for c in self.activePlayer.board["Artifact"]:
          if c.title == "pocket_universe" or c.title == "safe_place" and c.captured > 0:
            reduced = int(self.chooseHouse("custom", (f"How much amber from {c.title.replace('_', ' ').title()} would you like to spend? ({cost} will currently be taken from your pool)", list(range(c.captured + 1))))[0])
            c.captured -= reduced
            cost -= reduced
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
      # TODO: these need to be ordered too, rather than in a set order that I decide
      if "the_sting" in [x.title for x in other.board["Artifact"]]:
        logging.info(f"{other.name} gains the amber used to forge this key because of The Sting.")
        other.gainAmber(initial_cost, self)
      if player == "active" and "interdimensional_graft" in other.states and other.states["interdimensional_graft"] and forger.amber > 0:
        other.gainAmber(forger.amber, self) # setKeys is called in here
        forger.amber = 0
        logging.info(f"Your opponent played 'Interdimensional Graft' last turn, so they gain your {forger.amber} leftover amber. They now have {other.amber} amber.")
        # can't use play.stealAmber b/c this isn't technically stealing so Vaultkeeper shouldn't be able to stop it
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
      if "strange_gizmo" in forger.board["Artifact"]:
        for c in forger.board["Artifact"] + other.board["Artifact"] + forger.board["Creature"] + other.board["Creature"]:
          destroy(c, self.activePlayer, self)
          if c.destroyed:
            self.pendingReloc.append(c)
        self.pending()
      logging.info(f"{forger.name} now has {forger.keys} keys and {forger.amber} amber.")
      if player == "active":
        self.forgedThisTurn.append(forged)

  def cardChanged(self, checkPower = False):
    """ I don't think this function cares what the played card was. It will be called after a card is played/used, and it will do two things: (1) update self.cardBlits and (2) update what color the endTurn button is (by calling the function that actually checks this).
    The checkPower variable is so that we don't call the part that recalcs creature power when we call card changed at times when the board hasn't change (ie just a card being moved around)
    """
    
    if checkPower:
      # check if tireless_crocag should still be alive
      active = self.activePlayer.board["Creature"]
      inactive = self.inactivePlayer.board["Creature"]
      if not inactive and "tireless_crocag" in [x.title for x in active]:
        for c in active[::-1]:
          if c.title == "tireless_crocag":
            destroy(c, self.activePlayer, self)
            if c.destroyed:
              self.pendingReloc.append(c)
      if not active and "tireless_crocag" in [x.title for x in inactive]:
        for c in inactive[::-1]:
          if c.title == "tireless_crocag":
            destroy(c, self.inactivePlayer, self)
            if c.destroyed:
              self.pendingReloc.append(c)
      # check for things that are affected by being on a flank, shoulder armor and staunch knight
      for c in active:
        c.calcPower(self.activePlayer, self.inactivePlayer, self)
        c.updateHealth()
        if c.destroyed:
          self.pendingReloc.append(c)
      for c in inactive:
        c.calcPower(self.inactivePlayer, self.activePlayer, self)
        c.updateHealth()
        if c.destroyed:
          self.pendingReloc.append(c)
      
      if self.pendingReloc:
        self.pending()
      
      
    self.cardBlits = []
    for board,area in [(self.activePlayer.board["Creature"], self.creatures1_rect), (self.inactivePlayer.board["Creature"], self.creatures2_rect), (self.activePlayer.board["Artifact"], self.artifacts1_rect), (self.inactivePlayer.board["Artifact"], self.artifacts2_rect)]:
      l = len(board)
      x = 0
      if l:
        card_h = (area.width - ((l - 1) * self.margin)) // (l + 2)
      else:
        card_h = self.target_cardh
      if card_h >= self.target_cardh:
        offset = ((area[0] + area[2]) // 2) - ((l * self.target_cardh) // 2)
        card_h = self.target_cardh
        if l and board[0].rect.height < self.target_cardh:
          rescale = True
        else:
          rescale = False
      elif card_h > board[0].rect.height * 1.5: # can't use usual image, but can also afford to scale up the image
        offset = ((area[0] + area[2]) // 2) - ((l * card_h) // 2)
        rescale = True
      elif board[0].rect.height * 1.5 >= card_h >= board[0].rect.height: # too many cards to use usual image, but current image scale works
        offset = ((area[0] + area[2]) // 2) - ((l * board[0].rect.height) // 2)
        rescale = False
      else: # need to scale down
        offset = ((area[0] + area[2]) // 2) - ((l * card_h) // 2)
        rescale = True
      if rescale:  # scale everything down or up
        ratio = CARDH / card_h
        card_w = int(CARDW // ratio)
      if True in [x.selected for x in board]:
        selectedSurf = Surface(board[0].image.get_size())
        selectedSurf.convert_alpha()
        selectedSurf.set_alpha(80)
        selectedSurf.fill(COLORS["LIGHT_GREEN"])

        selectedSurfTapped = Surface(board[0].tapped.get_size())
        selectedSurfTapped.convert_alpha()
        selectedSurfTapped.set_alpha(80)
        selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])
      if True in [x.invalid for x in board]:
        invalidSurf = Surface(board[0].image.get_size())
        invalidSurf.convert_alpha()
        invalidSurf.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])

        invalidSurfTapped = Surface(board[0].tapped.get_size())
        invalidSurfTapped.convert_alpha()
        invalidSurfTapped.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])
      for card in board:
        if rescale:
          card.image, card.rect = card.scale_image(card_w, card_h)
          card.tapped, card.tapped_rect = card.tap(card.image)
        if card.ready:
          card_image, card_rect = card.image, card.rect
          card.tapped_rect.topleft = OB
        else:
          card_image, card_rect = card.tapped, card.tapped_rect
          card.rect.topleft = OB
        card_rect.topleft = (offset + (x * min(card_h, self.target_cardh)) + self.margin * (x + 1), area.top)
        if card in self.activePlayer.board["Creature"] and not card.taunt:
          card_rect.bottom = area[1] + area[3] - self.margin
        if card in self.inactivePlayer.board["Creature"] and card.taunt:
          card_rect.bottom = area[1] + area[3] - self.margin
        x += 1
        if card.type == "Creature" and card.upgrade:
          y = len(card.upgrade)
          x += 0.25 * y
          card_rect.left += 0.25 * self.target_cardh * y
          for up in card.upgrade:
            if rescale:  # scale everything down or up
              up.image, up.rect = up.scale_image(card_w, card_h)
            up_image, up_rect = up.image, up.rect
            up.tapped_rect.topleft = OB
            up_rect.left = card_rect.left - (3 * y * self.margin)
            if card.taunt:
              up_rect.top = card_rect.top
            else:
              up_rect.bottom = card_rect.bottom
            self.cardBlits.append((up_image, up_rect))
            y -= 1
        self.cardBlits.append((card_image, card_rect))
        if card.selected:
          if card.ready:
            self.cardBlits.append((selectedSurf, card_rect))
          else:
            self.cardBlits.append((selectedSurfTapped, card_rect))
        if card.invalid:
          if card.ready:
            self.cardBlits.append((invalidSurf, card_rect))
          else:
            self.cardBlits.append((invalidSurfTapped, card_rect))
    # hands
    for board,area in [(self.activePlayer.hand, self.hand1_rect), (self.inactivePlayer.hand, self.hand2_rect)]:
      l = len(board)
      x = 0
      if l:
        card_h = (area.width - ((l - 1) * self.margin)) // (l + 2)
      else:
        card_h = self.target_cardh
      if card_h >= self.target_cardh:
        offset = ((area[0] + area[2]) // 2) - ((l * self.target_cardh) // 2)
        card_h = self.target_cardh
        if l and board[0].rect.height < self.target_cardh:
          rescale = True
        else:
          rescale = False
      elif card_h > board[0].rect.height * 1.5: # can't use usual image, but can also afford to scale up the image
        offset = ((area[0] + area[2]) // 2) - ((l * card_h) // 2)
        rescale = True
      elif board[0].rect.height * 1.5 >= card_h >= board[0].rect.height: # too many cards to use usual image, but current image scale works
        offset = ((area[0] + area[2]) // 2) - ((l * board[0].rect.height) // 2)
        rescale = False
      else: # need to scale down
        offset = ((area[0] + area[2]) // 2) - ((l * card_h) // 2)
        rescale = True
      x = 0
      if rescale: # scale everything up or down
        ratio = CARDH / card_h
        card_w = int(CARDW // ratio)
      else:
        card_w = board[0].image.get_width()
      if True in [x.selected for x in board]:
        selectedSurf = Surface(board[0].image.get_size())
        selectedSurf.convert_alpha()
        selectedSurf.set_alpha(80)
        selectedSurf.fill(COLORS["LIGHT_GREEN"])

        selectedSurfTapped = Surface(board[0].tapped.get_size())
        selectedSurfTapped.convert_alpha()
        selectedSurfTapped.set_alpha(80)
        selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])
      if True in [x.invalid for x in board]:
        invalidSurf = Surface(board[0].image.get_size())
        invalidSurf.convert_alpha()
        invalidSurf.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])

        invalidSurfTapped = Surface(board[0].tapped.get_size())
        invalidSurfTapped.convert_alpha()
        invalidSurfTapped.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])
      for card in board:
        if rescale:
          card.image, card.rect = card.scale_image(card_w, card_h)
        card_image, card_rect = card.image, card.rect
        card.tapped_rect.topleft = OB
        card_rect.topleft = (offset + (x * min(card_w, self.target_cardw)) + self.margin * (x + 1), area.top)
        if area == self.hand2_rect:
          card_rect.bottom = area.bottom
        x += 1
        self.cardBlits.append((card_image, card_rect))
        if card.selected:
          self.cardBlits.append((selectedSurf, card_rect))
        if card.invalid:
          self.cardBlits.append((invalidSurf, card_rect))
    # actions
    if self.activePlayer.board["Action"]:
      if not self.ref_image:
        c = self.activePlayer.board["Action"][-1]
        target_height = self.actionBackSurf.get_height() - (self.margin * 2)
        target_width = (target_height // 7) * 5
        self.ref_image, self.ref_image_rect = c.scale_image(target_width, target_height)
        self.ref_image_rect.center = self.actionBackRect.center
      if self.drawAction:
        self.actionBackRect.bottomleft = (0, self.divider_rect.top)
        self.cardBlits.append((self.actionBackSurf, self.actionBackRect))
        self.cardBlits.append((self.actionMin, self.actionMinRect))
      else:
        self.actionBackRect.bottomright = (30, self.divider_rect.top)
        self.cardBlits.append((self.actionBackSurf, self.actionBackRect))
        self.cardBlits.append((self.actionMax, self.actionMaxRect))
      self.cardBlits.append((self.ref_image, self.ref_image_rect))
    else:
      self.ref_image = None
      self.ref_image_rect = Rect(-500, -500, 1, 1)
      self.ref_orig_image = None
      self.ref_orig_rect = None
    # lasting effects
    ## display smaller, hoverable card images of lasting effects
    self.miniRectsFriend = []
    for k in self.activePlayer.states:
      x = 0
      if self.activePlayer.states[k]:
        mini_image, mini_rect = self.activePlayer.stateImages[k][1]
        mini_rect.bottomleft = (self.neutral_rect.left + (x * (mini_image.get_width() + 5)), self.neutral_rect.bottom - 5)
        self.miniRectsFriend.append((mini_rect, self.activePlayer.stateImages[k][0]))
        self.cardBlits.append((mini_image, mini_rect))
      x += 1
    self.miniRectsEnemy = []
    for k in self.inactivePlayer.states:
      x = 0
      if self.inactivePlayer.states[k]:
        mini_image, mini_rect = self.inactivePlayer.stateImages[k][1]
        mini_rect.topleft = (self.neutral_rect.left + (x * (mini_image.get_width() + 5)), self.neutral_rect.top + 5)
        self.miniRectsFriend.append((mini_rect, self.inactivePlayer.stateImages[k][0]))
        self.cardBlits.append((mini_image, mini_rect))
      x += 1
    # discards
    if self.activePlayer.discard:
      card_image, card_rect = self.activePlayer.discard[-1].image, self.activePlayer.discard[-1].rect
      card_rect.topleft = (self.discard1_rect.left, self.discard1_rect.top)
      self.cardBlits.append((card_image, card_rect))
    if self.inactivePlayer.discard: 
      card_image, card_rect = self.inactivePlayer.discard[-1].image, self.inactivePlayer.discard[-1].rect
      card_rect.topleft = (self.discard2_rect.left, self.discard2_rect.top)
      self.cardBlits.append((card_image, card_rect))
    # archive
    if self.activePlayer.archive:
      card_image, card_rect = self.activePlayer.archive[-1].image, self.activePlayer.archive[-1].rect
      card_rect.center = self.archive1_rect.center
      self.cardBlits.append((card_image, card_rect))
    if self.inactivePlayer.archive: 
      card_image, card_rect = self.inactivePlayer.archive[-1].image, self.inactivePlayer.archive[-1].rect
      card_rect.center = self.archive2_rect.center
      self.cardBlits.append((card_image, card_rect))
    # decks
    # going to need a card back of some sort to put here
    if self.activePlayer.deck:
      card_image, card_rect = self.activePlayer.deck[-1].image, self.activePlayer.deck[-1].rect
      card_rect.topleft = (self.deck1_rect.left, self.deck1_rect.top)
      self.cardBlits.append((card_image, card_rect))
    if self.inactivePlayer.deck:
      card_image, card_rect = self.inactivePlayer.deck[-1].image, self.inactivePlayer.deck[-1].rect
      card_rect.topleft = (self.deck2_rect.left, self.deck2_rect.top)
      self.cardBlits.append((card_image, card_rect))
    # friendly discards/archive/purges when opened
    if self.drawFriendDiscard or self.drawFriendArchive or self.drawFriendPurge:
      if self.drawFriendDiscard:
        pool = self.activePlayer.discard
      elif self.drawFriendArchive:
        pool = self.activePlayer.archive
      else:
        pool = self.activePlayer.purged
      if True in [x.selected for x in pool]:
        selectedSurf = Surface(pool[0].image.get_size())
        selectedSurf.convert_alpha()
        selectedSurf.set_alpha(80)
        selectedSurf.fill(COLORS["LIGHT_GREEN"])

        selectedSurfTapped = Surface(pool[0].tapped.get_size())
        selectedSurfTapped.convert_alpha()
        selectedSurfTapped.set_alpha(80)
        selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])
      if True in [x.invalid for x in pool]:
        invalidSurf = Surface(pool[0].image.get_size())
        invalidSurf.convert_alpha()
        invalidSurf.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])

        invalidSurfTapped = Surface(pool[0].tapped.get_size())
        invalidSurfTapped.convert_alpha()
        invalidSurfTapped.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])
      x = 0
      for card in pool[0:16]:
        card.rect.topleft = (self.mat1_rect.left + (x * self.target_cardw) + self.margin * (x + 1), self.mat1_rect.top + self.margin)
        x += 1
        self.cardBlits.append((card.image, card.rect))
        if card.selected:
          self.cardBlits.append((selectedSurf, card.rect))
        if card.invalid:
          self.cardBlits.append((invalidSurf, card.rect))
      x = 0
      for card in pool[16:32]:
        card.rect.topleft = (self.mat1_rect.left + (x * self.target_cardw) + self.margin * (x + 1), self.mat1_rect.top + 2 * self.margin + self.target_cardh)
        x += 1
        self.cardBlits.append((card.image, card.rect))
        if card.selected:
          self.cardBlits.append((selectedSurf, card.rect))
        if card.invalid:
          self.cardBlits.append((invalidSurf, card.rect))
      for card in pool[32:]:
        card.rect.topleft = (self.mat1_rect.left + (x * self.target_cardw) + self.margin * (x + 1), self.mat1_rect.top + 3 * self.margin + 2 * self.target_cardh)
        x += 1
        self.cardBlits.append((card.image, card.rect))
        if card.selected:
          self.cardBlits.append((selectedSurf, card.rect))
        if card.invalid:
          self.cardBlits.append((invalidSurf, card.rect))
    # enemy discards/archive/purges when opened
    if self.drawEnemyDiscard or self.drawEnemyArchive or self.drawEnemyPurge:
      if self.drawEnemyDiscard:
        pool = self.inactivePlayer.discard
      elif self.drawEnemyArchive:
        pool = self.inactivePlayer.archive
      else:
        pool = self.inactivePlayer.purged
      if True in [x.selected for x in pool]:
        selectedSurf = Surface(pool[0].image.get_size())
        selectedSurf.convert_alpha()
        selectedSurf.set_alpha(80)
        selectedSurf.fill(COLORS["LIGHT_GREEN"])

        selectedSurfTapped = Surface(pool[0].tapped.get_size())
        selectedSurfTapped.convert_alpha()
        selectedSurfTapped.set_alpha(80)
        selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])
      if True in [x.invalid for x in pool]:
        invalidSurf = Surface(pool[0].image.get_size())
        invalidSurf.convert_alpha()
        invalidSurf.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])

        invalidSurfTapped = Surface(pool[0].tapped.get_size())
        invalidSurfTapped.convert_alpha()
        invalidSurfTapped.set_alpha(80)
        invalidSurf.fill(COLORS["RED"])
      x = 0
      for card in pool[0:16]:
        card.rect.topleft = (0 + (x * self.target_cardw) + self.margin * (x + 1), 0 + self.margin)
        x += 1
        self.cardBlits.append((card.image, card.rect))
        if card.selected:
          self.cardBlits.append((selectedSurf, card.rect))
        if card.invalid:
          self.cardBlits.append((invalidSurf, card.rect))
      x = 0
      for card in pool[16:32]:
        card.rect.topleft = (0 + (x * self.target_cardw) + self.margin * (x + 1), 0 + 2 * self.margin + self.target_cardh)
        x += 1
        self.cardBlits.append((card.image, card.rect))
        if card.selected:
          self.cardBlits.append((selectedSurf, card.rect))
        if card.invalid:
          self.cardBlits.append((invalidSurf, card.rect))
    
    self.setKeys()
    
    if self.activeHouse:
      self.playsRemaining()
    
  def playsRemaining(self):
    # now, check if we should change the fill on endTurn
    if True not in [self.canPlay(c, reset = False, message = False) for c in self.activePlayer.hand if c.type] + [self.canDiscard(c, reset = False, message = False) for c in self.activePlayer.hand if c.type]:
      if True not in [self.canAction(c, reset = False, message = False) for c in self.activePlayer.board["Creature"]] + [self.canFight(c, reset = False, message = False) for c in self.activePlayer.board["Creature"]] + [self.canReap(c, reset = False, message = False) for c in self.activePlayer.board["Creature"]] + [self.canOmni(c, reset = False, message = False) for c in self.activePlayer.board["Creature"]]:
        if True not in [self.canAction(c, reset = False, message = False) for c in self.activePlayer.board["Artifact"]] + [self.canOmni(c, reset = False, message = False) for c in self.activePlayer.board["Artifact"]]:
          logging.info("Nothing left to do!")
          self.endBack.fill(COLORS["LIGHT_GREEN"])
          self.remaining = False
          return
    logging.info("There's stuff left to do.")
    self.remaining = True
    

  def previewHouse(self, condition: LambdaType, both: bool = False) -> List[Tuple[Surface, Rect]]:
    """ Highlights the cards that meet the selected conditions.
    """
    retVal = []

    selectedSurf = Surface((self.target_cardw, self.target_cardh))
    selectedSurf.convert_alpha()
    selectedSurf.set_alpha(80)
    selectedSurf.fill(COLORS["LIGHT_GREEN"])

    selectedSurfTapped = Surface((self.target_cardh, self.target_cardw))
    selectedSurfTapped.convert_alpha()
    selectedSurfTapped.set_alpha(80)
    selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])

    board = self.activePlayer.board["Creature"] + self.activePlayer.board["Artifact"]
    if both:
      board += self.inactivePlayer.board["Creature"] + self.inactivePlayer.board["Artifact"]

    for c in board:
      if condition(c): # or "experimental_therapy" in [x.title for x in c.upgrade]:
        c.selected = True
        # if c.ready:
        #   retVal.append((selectedSurf, c.rect))
        # else:
        #   retVal.append((selectedSurfTapped, c.tapped_rect))
    if both:
      return retVal
    for c in self.activePlayer.hand:
      if condition(c):
        c.selected = True
        # retVal.append((selectedSurf, c.rect))
    
    return retVal

  def pending(self, destination = "discard", secondary: List = [], target = None, reveal: bool = False):
    """ Pending is the function that handles when multiple cards leave play at the same time, whether it be to hand or to discard. It will trigger leaves play and destroyed effects. Allowable options for dest are 'purge', 'discard', 'hand', 'deck', 'archive'.
    """
    active = self.activePlayer.board
    inactive = self.inactivePlayer.board
    if secondary:
      L = secondary # this is for handling if destruction triggers another destruction
      logging.info("This is a nested destruction.")
    else:
      L = self.pendingReloc
      logging.info("This is an initial destruction.")

    if not L:
      self.cardChanged(True)
      return # just in case we feed it an empty list
    for c in L[::-1]:
      triggers = []
      if c.destroyed:
        if c.dest:
          for d in c.dest:
            triggers.append((d, c)) # some card.dests will put the card into a different zone, arma_cloak won't put in dif zone, but will remove from destroyed list
      else:
        # so these cards are probably leaving play, so we need to do the basic leaves play stuff (though not always, need to figure out the triggers for that)
        # I could build these things into reset, which means I wouldn't write functions for leaves play, stuff, I'd just catch it in reset
        if c.returned:
          basicLeaves(self, c) # sure, I might call this on stuff that's in hand going to an archive, but the effects will only trigger it the card's in play
        c.reset()
    # at this point I would let them order the destroyed triggers - draw the pending destroyed cards and use chooseCards to pick them one at a time, but I won't implement that yet
    for d, c in triggers:
      d(self, c)
      logging.info(f"dest trigger {d} on card {c.title} completed.")
    for c in L[::-1]:
      if c.destroyed:
        for x in c.upgrade:
          if x.title == "armageddon_cloak": # this should be redundant
            L.remove(c)
            c.upgrade.remove(x)
            L.append(x)
            # I think if there were multiple on a card both would end up destroyed?
          elif x.title == "phoenix_heart":
            L.remove(c)
        if c in L: 
          basicDest(self, c)
          if c.type == "Creature" and c.stealer:
            if c.deck == self.activePlayer.name:
              self.activePlayer.purged.append(c)
            else:
              self.inactivePlayer.purged.append(c)
            L.remove(c)
        if c.destroyed: # because arma_cloak will remove the destroyed tag
          c.reset()
          c.destroyed = True
    if destination not in ['purge', 'discard', 'hand', 'deck', 'archive', 'annihilate']:
      logging.error("Pending was given an invalid destination.")
      self.cardChanged(True)
      return
    if destination == "purge":
      for c in L[::-1]:
        if c.deck == self.activePlayer.name and not c.safe:
          self.activePlayer.purged.append(c)
        elif not c.safe:
          self.inactivePlayer.purged.append(c)
        L.remove(c)
    
    # here is where we'd want to let them make choices about order, b/c choosing order of destroyed triggers and order of things entering discard is different - so they set the order here, and then it goes to resolve
    
    # some code here that will lead to L being reordered - it will show both boards at the same time, but build one list

    # if we let them choose which one will go in first, and append the rest, we won't need to reverse the list as we already do that as part of the process
    
    # if destination == "annihilate": # we'll do this one first to remove all creatures (b/c annihilation ritual only affects creatures)

    # if we do this right, we shouldn't end up in a situation where we have some cards that were destroyed in this list and some that weren't (this is dependent on making sure dest effects only add to pendingReloc if it's empty)

    elif destination == "discard":
      for c in L[::-1]:
        if c.deck == self.activePlayer.name:
          if "annihilation_ritual" in ([x.title for x in active["Artifact"]] + [x.title for x in inactive["Artifact"]]) and c.type == "Creature" and c.destroyed == True:
            self.activePlayer.purged.append(c)
          else:
            self.activePlayer.discard.append(c)
        else:
          if "annihilation_ritual" in ([x.title for x in active["Artifact"]] + [x.title for x in inactive["Artifact"]]) and c.type == "Creature" and c.destroyed == True:
            self.inactivePlayer.purged.append(c)
          else:
            self.inactivePlayer.discard.append(c)
        c.destroyed = False
        L.remove(c)
    elif destination == "hand":
      for c in L[::-1]:
        if c.deck == self.activePlayer.name:
          for up in c.upgrade:
            if up.deck == self.activePlayer.name:
              self.activePlayer.discard.append(up)
            else:
              self.inactivePlayer.discard.append(up)
          self.activePlayer.hand.append(c)
        else:
          for up in c.upgrade:
            if up.deck == self.inactivePlayer.name:
              self.activePlayer.discard.append(up)
            else:
              self.inactivePlayer.discard.append(up)
          self.inactivePlayer.hand.append(c)
        c.reveal = True
        L.remove(c)
      # I think it would be confusing if I sorted the hand, at this point they will have chosen the order of L so things should be returned to their hand in that order
      # self.activePlayer.hand.sort(key = lambda x: x.house)
      # self.inactivePlayer.hand.sort(key = lambda x: x.house)
    elif destination == "deck":
      for c in L[::-1]:
        if c.deck == self.activePlayer.name:
          self.activePlayer.deck.append(c)
        else:
          self.inactivePlayer.deck.append(c)
        c.reveal = reveal
        L.remove(c)
    elif destination == "archive":
      if target == None:
        raise ValueError("'archive' given as argument to pending() without a target player.")
      for c in L[::-1]:
        # this is where we use target
        target.archive.append(c)
        L.remove(c)
    # check that the list was emptied
    if L:
      logging.error(f"Pending did not properly empty the list. {L}")
    self.cardChanged(True)

  
  def canAction(self, card, reset = True, r_click: bool = False, cheat: bool = False, message: bool = False):
    if self.ruleOfSix(card):
      if message: logging.info(f"Rule of six prevents using this {card.title}.")
      return False
    if not card.ready or not card.action:
      return False
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      if message: logging.info("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.house == "Mars" and "combat_pheromones" in self.activePlayer.states and self.activePlayer.states["combat_pheromones"]:
      if reset: self.activePlayer.states["combat_pheromones"] -= 1
      cheat = True
    if "deipno_spymaster" in self.activePlayer.states and card in self.activePlayer.states["deipno_spymaster"]:
      cheat = True
    if card.house not in self.activeHouse and card.house not in self.extraUseHouses and not cheat:
      if len(card.upgrade) > 0 and ("mantle_of_the_zealot" in [x.title for x in card.upgrade] or "experimental_theory" in [x.title for x in card.upgrade]):
        pass
      else:
        return False
    if card.type == "Artifact" and "tentacus" in [x.title for x in self.inactivePlayer.board["Creature"]]:
      if message: logging.info("You must pay one to Tentacus to use this artifact.")
      if not self.activePlayer.amber:
        if message: logging.info("You can't afford to pay for Tentacus.")
        return False
      else:
        if reset:
          self.activePlayer.amber -= 1
          if message: logging.info(f"You paid for Tentacus to use {card.title}.")
          return True
    if card.type == "Creature":
      if card.stun and not r_click:
        return False
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        if message: logging.info("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
        return False
    
    return True
  
  def canDiscard(self, card, reset = True, cheat = True, message: bool = False):
    if self.turnNum == 1 and (len(self.playedThisTurn) > 0 or len(self.discardedThisTurn) > 0):
      if message: logging.info("Can't discard, action for first turn already taken.")
      return False
    if card.house not in self.activeHouse or not cheat:
      if message: logging.info("Can't discard card not in activeHouse.")
      return False
    # I don't think anything messes with your ability to discard
    return True
  
  def canFight(self, card, reset = True, cheat: bool = False, r_click: bool = False, message: bool = False):
    if card.type != "Creature":
      return False
    if self.ruleOfSix(card):
      if message: logging.info(f"Rule of six prevents using this {card.title}.")
      return False
    if not card.ready or (card.stun and not r_click):
      return False
    if not self.inactivePlayer.board["Creature"]:
      return False
    if card.house == "Mars" and "combat_pheromones" in self.activePlayer.states and self.activePlayer.states["combat_pheromones"] > 0:
      if reset: self.activePlayer.states["combat_pheromones"] -= 1
      cheat = True
    if "deipno_spymaster" in self.activePlayer.states and card in self.activePlayer.states["deipno_spymaster"]:
      cheat = True
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      if message: logging.info("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.type == "Creature": # why wouldn't it?
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        if message: logging.info("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
        return False
      if card.title == "mack_the_knife":
        cheat = True
      if card.house not in self.activeHouse and card.house not in self.extraFightHouses and card.house not in self.extraUseHouses and card.title != "tireless_crocag" and not cheat:
        if len(card.upgrade) > 0 and ("mantle_of_the_zealot" in [x.title for x in card.upgrade] or "experimental_theory" in [x.title for x in card.upgrade]):
          pass
        else:
          return False

      if "foggify" in self.inactivePlayer.states and self.inactivePlayer.states["foggify"] or "fogbank" in self.inactivePlayer.states and self.inactivePlayer.states["fogbank"]:
        return False
      if card.title == "bigtwig" and True not in [x.stun for x in self.inactivePlayer.board["Creature"]]:
        return False
    

    return True

  def canOmni(self, card, r_click: bool = False, reset: bool = True, message: bool = False, cheat: bool = False):
    if self.ruleOfSix(card):
      if message: logging.info(f"Rule of six prevents using this {card.title}.")
      return False
    if not card.ready or not card.omni or (card.stun and not r_click):
      return False
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      if message: logging.info("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.type == "Artifact" and "tentacus" in [x.title for x in self.inactivePlayer.board["Creature"]]:
      if message: logging.info("You must pay one to Tentacus to use this artifact.")
      if not self.activePlayer.amber:
        if message: logging.info("You can't afford to pay for Tentacus.")
        return False
      else:
        if reset:
          answer = self.chooseHouse('custom', ("Would you like to pay for Tentacus?", ["Yes", "No"]))[0]
          if answer == "Yes":
            self.activePlayer.amber -= 1
            if message: logging.info(f"You paid for Tentacus to use {card.title}.")
          else:
            return False
        return True
    return True

  def canPlay(self, card, reset: bool = True, message: bool = False, cheat: bool = False):
    if len(self.playedThisTurn) >= 1 and self.turnNum == 1 and "wild_wormhole" not in [x.title for x in self.activePlayer.board["Action"]] and not ("phase_shift" in self.activePlayer.states and self.activePlayer.states["phase_shift"] and card.house != "Logos"):
      if message: logging.info("You cannot play more than one card on your first turn.")
      return False
    if self.ruleOfSix(card):
      if message: logging.info(f"Rule of six prevents playing {card.title}.")
      return False
    if "ember_imp" in [x.title for x in self.inactivePlayer.board["Creature"]] and len(self.playedThisTurn) >= 2: #
      if message: logging.info(f"'Ember Imp' prevents playing {card.title}")
      return False
    if "treasure_map" in self.activePlayer.states and self.activePlayer.states["treasure_map"]:
      if message: logging.info("'Treasure Map' prevents playing more cards this turn")
      return False
    if "witch_of_the_wilds" in [x.title for x in self.activePlayer.board["Creature"]] \
    and "Untamed" not in self.activeHouse \
    and sum(x.house == "Untamed" for x in self.playedThisTurn) < 2:
      return True # the problem is this probably does stack with phase shift
    if "wild_wormhole" in [x.title for x in self.activePlayer.board["Action"]]:
      if card.type == "Action":
        if "scrambler_storm" in self.inactivePlayer.states and self.inactivePlayer.states["scrambler_storm"]:
          if message: logging.info("'Scrambler Storm' prevents playing actions this turn, so you can't cheat this card out.")
          return False
      elif card.type == "Creature":
        if card.title == "kelifi_dragon" and self.activePlayer.amber < 7:
          if message: logging.info("You need 7 amber to play 'Kelifi Dragon'")
          return False
        if card.title == "truebaru" and self.activePlayer.amber < 3:
          if message: logging.info("You must have 3 amber to sacrifice in order to play 'Truebaru'")
          return False
        if "grommid" in [x.title for x in self.activePlayer.board["Creature"]]:
          if message: logging.info("You can't play creatures with 'Grommid' in play")
          return False
        if "lifeward" in self.inactivePlayer.states and self.inactivePlayer.states["lifeward"]:
          if message: logging.info("You can't play creatures because of 'Lifeward'")
          return False
      if card.house not in self.activeHouse and not cheat:
        return True
    if card.type == "Artifact":
      # if there are other things that affect playing artifacts, make sure this one is last
      if "customs_office" in [x.title for x in self.inactivePlayer.board["Artifact"]] and self.activePlayer.amber < sum(x.title == "customs_office" for x in self.inactivePlayer.board["Artifact"]):
        if message: logging.info("You are unable to pay for your opponent's custom office.")
        return False
      elif "customs_office" in [x.title for x in self.inactivePlayer.board["Artifact"]] and reset:
        self.activePlayer.amber -= 1
        self.inactivePlayer.gainAmber(1, self)
    if card.type == "Upgrade" and len(self.activePlayer.board["Creature"]) == 0 and len(self.inactivePlayer.board["Creature"]) == 0:
      if message: logging.info("No valid targets for this upgrade.")
      return False
    if (card.house not in self.activeHouse and card.house != "Logos") and ("phase_shift" in self.activePlayer.states and self.activePlayer.states["phase_shift"] > 0) and not cheat:
      if reset:
        self.activePlayer.states["phase_shift"] -= 1 # reset to false
    elif card.house not in self.activeHouse and not cheat:
      if message: logging.info("Can't play cards not from the active house.")
      return False
    return True

  def canReap(self, card, reset = True, r_click: bool = False, cheat: bool = False, message: bool = False):
    if self.ruleOfSix(card):
      if message: logging.info(f"Rule of six prevents using {card.title}.")
      return False
    if card.type != "Creature" or not card.ready or (card.stun and not r_click):
      if message: logging.info(f"Type: {card.type}, ready: {card.ready}, stun: {card.stun}")
      return False
    if "transposition_sandals" in self.activePlayer.states and card in self.activePlayer.states["transposition_sandals"]:
      cheat = True
    if card.house == "Mars" and "combat_pheromones" in self.activePlayer.states and self.activePlayer.states["combat_pheromones"] > 0:
      if reset: self.activePlayer.states["combat_pheromones"] -= 1
      cheat = True
    if "deipno_spymaster" in self.activePlayer.states and card in self.activePlayer.states["deipno_spymaster"]:
      cheat = True
    if card.title == "mack_the_knife":
      cheat = True
    if card.house not in self.activeHouse and card.house not in self.extraUseHouses and not cheat:
      if message: logging.info(f"House: {card.house}, cheat: {cheat}")
      if len(card.upgrade) > 0 and ("mantle_of_the_zealot" in [x.title for x in card.upgrade] or "experimental_theory" in [x.title for x in card.upgrade]):
        pass
      else:
        return False
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      if message: logging.info("'Skippy Timehog' is preventing you from using cards")
      return False
    if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
      if message: logging.info("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
      return False
    if card.title == "tireless_crocag":
      return False
    

    return True
  
  def ruleOfSix(self, card):
    """ Checks a card against the rule of six.
    """
    count = 0
    for k,v in self.playedThisTurn.items():
      if k.title == card.title:
        count += v
    for k,v in self.usedThisTurn.items():
      if k.title == card.title:
        count += v
    if count >= 6:
      return True
    return False

  def playUpgrade(self, card, target = None):
    """ Plays an upgrade on a creature.
    """
    logging.info(card)
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    hand = self.activePlayer.hand
    broken = False
    
    if target:
      self.activePlayer.board["Upgrade"].append(card)
      if card in hand:
        hand.remove(card)
      side, choice = target
      if side == "fr":
        active[choice].upgrade.append(card)
      else:
        inactive[choice].upgrade.append(card)
      eval(f"upgrade.{card.title}(self, card, side, choice)")
      self.cardChanged(True) # this would actually make the play abilities I put on blood of titans, a bit redundant, but redundancy is ok
      return
    
    drawMe = []
    # surfs
    selectedSurf = Surface((self.target_cardw, self.target_cardh))
    selectedSurf.convert_alpha()
    selectedSurf.set_alpha(80)
    selectedSurf.fill(COLORS["LIGHT_GREEN"])

    selectedSurfTapped = Surface((self.target_cardh, self.target_cardw))
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
      discSurf = Surface((self.target_cardw, self.target_cardh))
      discSurf.convert_alpha()
      discSurf.set_alpha(80)
      discSurf.fill(COLORS["LIGHT_GREEN"])
      discRect = discSurf.get_rect()
      discRect.topleft = self.discard1_rect.topleft
      drawMe.append((discSurf, discRect))
    
    while True:
      self.extraDraws = drawMe.copy()
      
      for e in pygame.event.get():
        if e.type == MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = e.pos
        
        if e.type == QUIT:
          pygame.quit()

        if e.type == MOUSEBUTTONUP and e.button == 1:
          activeHit = [(Rect.collidepoint(x.rect, (self.mousex, self.mousey)) or Rect.collidepoint(x.tapped_rect, (self.mousex, self.mousey))) for x in active]
          inactiveHit = [(Rect.collidepoint(x.rect, (self.mousex, self.mousey)) or Rect.collidepoint(x.tapped_rect, (self.mousex, self.mousey))) for x in inactive]
          if Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
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
          elif True in inactiveHit:
            self.activePlayer.board["Upgrade"].append(self.dragging.pop())
            side = "fo"
            choice = inactiveHit.index(True)
            inactive[choice].upgrade.append(card)
            eval(f"upgrade.{card.title}(self, card, side, choice)")
            broken = True
            break
          elif self.canDiscard(card, reset=False) and Rect.collidepoint(discRect, (self.mousex, self.mousey)):
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
          logging.error("You shouldn't be able to trigger MOUSEBUTTONDOWN in dragCard.")

      if Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
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
      logging.info(f"{card.title} gave you {str(card.amber)} amber. You now have {str(self.activePlayer.amber)} amber.\n\nChange to a log when you fix the amber display issue.""")
    self.playedThisTurn.append(card)
    self.cardChanged(True)
    return

  def dragCard(self) -> None:
    """ Enables dragging a card from your hand around the screen.
    """
    card = self.dragging[0]
    hand = self.activePlayer.hand
    drawMe = []

    if self.canDiscard(card, reset = False):
      ## discard stuff here - if you can play it, you can discard it
      discSurf = Surface((self.target_cardw, self.target_cardh))
      discSurf.convert_alpha()
      discSurf.set_alpha(80)
      discSurf.fill(COLORS["LIGHT_GREEN"])
      discRect = discSurf.get_rect()
      discRect.topleft = self.discard1_rect.topleft
      drawMe = [(discSurf, discRect)]
    
    if self.canPlay(card, reset=False):
      if card.type == "Action":
        dropSurf = Surface((self.creatures1.get_width(), (self.mat1.get_height() // 3) * 2))
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
        if e.type == MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = e.pos
        
        if e.type == QUIT:
          pygame.quit()

        if e.type == MOUSEBUTTONUP and e.button == 1:
          if Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
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
          elif self.canPlay(card, reset=False) and Rect.collidepoint(dropRect, (self.mousex, self.mousey)):
            hand.append(self.dragging.pop())
            self.playCard(-1, ask = False)
            self.extraDraws = []
            self.cardChanged()
            return
          elif self.canDiscard(card, reset=False) and Rect.collidepoint(discRect, (self.mousex, self.mousey)):
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
          logging.error("You shouldn't be able to trigger MOUSEBUTTONDOWN in dragCard.")

      if Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
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
    backgroundSurf = Surface((messageSurf.get_width(), messageSurf.get_height()))
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
      ## discard stuff here
      discSurf = Surface((self.target_cardw, self.target_cardh))
      discSurf.convert_alpha()
      discSurf.set_alpha(80)
      discSurf.fill(COLORS["LIGHT_GREEN"])
      discRect = discSurf.get_rect()
      discRect.topleft = self.discard1_rect.topleft
      drawMe.append((discSurf, discRect))

    if card.type == "Creature" and len(self.activePlayer.board[card.type]) > 0:
      board = self.activePlayer.board[card.type]
      # right
      c = board[-1]
      if willEnterReady(self, card, False):
        self.flankRectRightTapped.topleft = OB
        if c.ready: # both ready
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectRight.topleft = (c.rect.topright)
            self.flankRectRight.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectRight.topleft = (c.rect.topright)
            self.flankRectRight.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRight.topleft = (c.rect.topright)
          self.flankRectRight.right += self.margin
        else: # played ready, in play not
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectRight.bottomleft = (c.tapped_rect.bottomright)
            self.flankRectRight.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectRight.bottomleft = (c.tapped_rect.bottomright)
            self.flankRectRight.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRight.bottomleft = (c.tapped_rect.bottomright)
          self.flankRectRight.right += self.margin
        drawMe.append((self.flankSurf, self.flankRectRight))
      else:
        self.flankRectRight.topleft = OB
        if c.ready: # played not ready, in play ready
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectRightTapped.bottomleft = (c.rect.bottomright)
            self.flankRectRightTapped.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectRightTapped.topleft = (c.rect.topright)
            self.flankRectRightTapped.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRightTapped.bottomleft = (c.rect.bottomright)
          self.flankRectRightTapped.right += self.margin
        else: # played not ready, in play not ready
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectRightTapped.topleft = (c.tapped_rect.topright)
            self.flankRectRightTapped.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectRightTapped.topleft = (c.tapped_rect.topright)
            self.flankRectRightTapped.top -= self.margin * 3
          else: # both taunt or both not
            self.flankRectRightTapped.topleft = (c.tapped_rect.topright)
          self.flankRectRightTapped.right += self.margin
        drawMe.append((self.flankSurfTapped, self.flankRectRightTapped))
      # left
      c = board[0]
      if willEnterReady(self, card, False):
        self.flankRectLeftTapped.topright = OB
        if c.ready: # both ready
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeft.topright = (c.rect.topleft)
            self.flankRectLeft.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectLeft.topright = (c.rect.topleft)
            self.flankRectLeft.top -= self.margin * 3
          else: # both same
            self.flankRectLeft.topright = (c.rect.topleft)
          self.flankRectLeft.left -= self.margin
        else: # played ready, in play not
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeft.bottomright = (c.tapped_rect.bottomleft)
            self.flankRectLeft.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectLeft.bottomright = (c.tapped_rect.bottomleft)
            self.flankRectLeft.top -= self.margin * 3
          else: # both same
            self.flankRectLeft.bottomright = (c.tapped_rect.bottomleft)
          self.flankRectLeft.left -= self.margin * (len(c.upgrade) + 1)
        drawMe.append((self.flankSurf, self.flankRectLeft))
      else:
        self.flankRectLeft.topright = OB
        if c.ready: # in play ready, played not
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeftTapped.bottomright = (c.rect.bottomleft)
            self.flankRectLeftTapped.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectLeftTapped.topright = (c.rect.topleft)
            self.flankRectLeftTapped.top -= self.margin * 3
          else: # both same
            self.flankRectLeftTapped.bottomright = (c.rect.bottomleft)
          self.flankRectLeftTapped.left -= self.margin * (len(c.upgrade) + 1)
        else: # neither ready
          if c.taunt and not card.taunt: # in play taunt, played not
            self.flankRectLeftTapped.topright = (c.tapped_rect.topleft)
            self.flankRectLeftTapped.top += self.margin * 3
          elif not c.taunt and card.taunt: # played taunt, in play not
            self.flankRectLeftTapped.topright = (c.tapped_rect.topleft)
            self.flankRectLeftTapped.top -= self.margin * 3
          else: # both same
            self.flankRectLeftTapped.topright = (c.tapped_rect.topleft)
          self.flankRectLeftTapped.left -= self.margin * (len(c.upgrade) + 1)
        drawMe.append((self.flankSurfTapped, self.flankRectLeftTapped))
    else: # empty board
      if willEnterReady(self, card, False):
        self.flankRectRight.center = self.creatures1_rect.center
        self.flankRectLeft.topright = OB
        self.flankRectLeftTapped.topright = OB
        self.flankRectRightTapped.topright = OB
        drawMe.append((self.flankSurf, self.flankRectRight))
      else:
        self.flankRectRightTapped.center = self.creatures1_rect.center
        self.flankRectLeftTapped.topright = OB
        self.flankRectLeft.topright = OB
        self.flankRectRight.topright = OB
        drawMe.append((self.flankSurfTapped, self.flankRectRightTapped))
    
    if card.type == "Artifact":
      artifact = self.activePlayer.board["Artifact"]
      if willEnterReady(self, card, False):
        self.flankRectRight.center = self.artifacts1_rect.center
        if artifact:
          if artifact[-1].ready:
            self.flankRectRight.left = artifact[-1].rect.right + self.margin
          else:
            self.flankRectRight.left = artifact[-1].tapped_rect.right + self.margin
        self.flankRectLeft.topright = OB
        self.flankRectLeftTapped.topright = OB
        self.flankRectRightTapped.topright = OB
        drawMe.append((self.flankSurf, self.flankRectRight))
      else:
        self.flankRectRightTapped.center = self.artifacts1_rect.center
        if artifact:
          if artifact[-1].ready:
            self.flankRectRightTapped.left = artifact[-1].rect.right + self.margin
          else:
            self.flankRectRightTapped.left = artifact[-1].tapped_rect.right + self.margin
        self.flankRectLeftTapped.topright = OB
        self.flankRectLeft.topright = OB
        self.flankRectRight.topright = OB
        drawMe.append((self.flankSurfTapped, self.flankRectRightTapped))

    print("About to enter the loop.")
    while True:
      self.extraDraws = drawMe.copy()
      for e in pygame.event.get():
        if e.type == QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          print("Button up.")
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          print(f"True not in self.friendDraws: {True not in self.friendDraws}. {[Rect.collidepoint(x, (self.mousex, self.mousey)) for x in [self.flankRectLeft, self.flankRectLeftTapped, self.flankRectRight, self.flankRectRightTapped]]}")
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          ## DONE: Figure out why this function isn't returning, like ever - REASON: thoughtless use of elif matched something before the check that would return the flank choice
          if Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
            l = len(hand)
            for x in range(len(hand)):
              temp_card = hand[x]
              if x == 0 and self.mousex < temp_card.rect.centerx:
                hand.insert(0, self.dragging.pop())
                self.extraDraws = []
                card.tapped.set_alpha(255)
                card.image.set_alpha(255)
                self.cardChanged()
                print("Returning empty.")
                return
              elif temp_card.rect.centerx < self.mousex and x < l-1 and self.mousex < hand[x+1].rect.centerx:
                hand.insert(x + 1, self.dragging.pop())
                self.extraDraws = []
                card.tapped.set_alpha(255)
                card.image.set_alpha(255)
                self.cardChanged()
                print("Returning empty.")
                return
            hand.append(self.dragging.pop())
            self.extraDraws = []
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            self.cardChanged()
            print("Returning empty.")
            return
          elif True not in self.friendDraws and True in [Rect.collidepoint(x, (self.mousex, self.mousey)) for x in [self.flankRectLeft, self.flankRectLeftTapped, self.flankRectRight, self.flankRectRightTapped]]:
            print("Am I at least getting here?")
            if Rect.collidepoint(self.flankRectLeft, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              print("Returning left.")
              return "Left"
            elif Rect.collidepoint(self.flankRectLeftTapped, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              print("Returning left.")
              return "Left"
            elif Rect.collidepoint(self.flankRectRight, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              print("Returning right.")
              return "Right"
            elif Rect.collidepoint(self.flankRectRightTapped, (self.mousex, self.mousey)):
              self.extraDraws = []
              card.tapped.set_alpha(255)
              card.image.set_alpha(255)
              self.cardChanged()
              print("Returning right.")
              return "Right"
          elif discard and Rect.collidepoint(discRect, (self.mousex, self.mousey)):
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            hand.append(self.dragging.pop())
            self.discardCard(-1)
            self.extraDraws = []
            self.cardChanged()
            print("Returning empty.")
            return
          elif True not in self.friendDraws and self.dragging:
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            self.activePlayer.hand.append(self.dragging.pop())
            self.extraDraws = []
            self.cardChanged()
            print("Returning empty.")
            return None
          elif not self.dragging:
            if True in self.friendDraws and Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
              self.drawFriendDiscard = False
              self.drawFriendArchive = False
              self.drawFriendPurge = False
              for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
                card.rect.topleft = OB
              self.cardChanged()
            elif True not in self.enemyDraws:
              if self.drawAction:
                if Rect.collidepoint(self.actionMinRect, (self.mousex, self.mousey)):
                  self.drawAction = False
                  self.cardChanged()
              else:
                if Rect.collidepoint(self.actionMaxRect, (self.mousex, self.mousey)):
                  self.drawAction = True
                  self.cardChanged()
            elif True in self.enemyDraws and Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
              self.drawEnemyDiscard = False
              self.drawEnemyArchive = False
              self.drawEnemyPurge = False
              for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
                card.rect.topleft = OB
              self.cardChanged()
            elif not self.drawFriendDiscard and Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
              self.drawFriendDiscard = True
            elif not self.drawEnemyDiscard and Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
              self.drawEnemyDiscard = True
            elif not self.drawFriendPurge and Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
              self.drawFriendPurge = True
            elif not self.drawEnemyPurge and Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
              self.drawEnemyPurge = True
            elif not self.drawFriendArchive and Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
              self.drawFriendArchive = True
            elif not self.drawEnemyArchive and Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
              self.drawEnemyArchive = True
          else:
            card.tapped.set_alpha(255)
            card.image.set_alpha(255)
            self.extraDraws = []
            self.cardChanged()
            print("Returning empty.")
            return None
      
      if Rect.collidepoint(self.hand1_rect, (self.mousex, self.mousey)):
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
    backgroundSurf = Surface((messageSurf.get_width(), messageSurf.get_height()))
    backgroundSurf.convert()
    backgroundRect = backgroundSurf.get_rect()
    backgroundRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # keep
    keepSurf = self.BASICFONT.render("   KEEP   ", 1, COLORS["WHITE"])
    keepRect = keepSurf.get_rect()
    keepRect.topright = ((WIDTH // 2) - (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)
    # keep background
    keepBack = Surface((keepSurf.get_width(), keepSurf.get_height()))
    keepBack.convert()
    keepBack.fill(COLORS["LIGHT_GREEN"])
    keepBackRect = keepBack.get_rect()
    keepBackRect.topright = ((WIDTH // 2) - (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)
    # mulligan
    mullSurf = self.BASICFONT.render(" MULLIGAN ", 1, COLORS["WHITE"])
    mullRect = mullSurf.get_rect()
    mullRect.topleft = ((WIDTH // 2) + (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)
    # mulligan background
    mullBack = Surface((mullSurf.get_width(), mullSurf.get_height()))
    mullBack.convert()
    mullBack.fill(COLORS["RED"])
    mullBackRect = mullBack.get_rect()
    mullBackRect.topleft = ((WIDTH // 2) + (self.margin // 2), messageRect[1] + messageRect[3] + self.margin)

    while True:
      self.extraDraws = [(backgroundSurf, backgroundRect), (messageSurf, messageRect),  (keepBack, keepBackRect), (keepSurf, keepRect), (mullBack, mullBackRect), (mullSurf, mullRect)]
      for e in pygame.event.get():
        if e.type == QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.extraDraws = []
          if Rect.collidepoint(keepBackRect, (self.mousex, self.mousey)):
            return False
          elif Rect.collidepoint(mullBackRect, (self.mousex, self.mousey)):
            return True
      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      pygame.display.flip()
      self.extraDraws = []

  
  def chooseHouse(self, varAsStr: str, custom: Tuple[str, List[str]] = (), colors: List[str] = [], highlight: LambdaType = None) -> List[str]:
    """ Makes the user choose a house to be used for some variable, typically will be active house, but could be cards like control the weak.
    """
    if varAsStr == "activeHouse":
      message = "Choose your house for this turn:"
      if "control_the_weak" in self.inactivePlayer.states and self.inactivePlayer.states["control_the_weak"]:
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
    if not houses:
      houses == ["OK"]
    houses_rects = []
    # message
    messageSurf = self.BASICFONT.render(message, 1, COLORS["WHITE"])
    messageRect = messageSurf.get_rect()
    messageRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # message background
    messageBackSurf = Surface((messageSurf.get_width(), messageSurf.get_height()))
    messageBackSurf.convert()
    messageBackRect = messageBackSurf.get_rect()
    messageBackRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # confirm
    confirmSurf = self.BASICFONT.render("  CONFIRM  ", 1, COLORS["WHITE"])
    confirmRect = confirmSurf.get_rect()
    confirmRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # confirm background
    confirmBack = Surface((confirmSurf.get_width(), confirmSurf.get_height()))
    confirmBack.convert()
    confirmBack.fill(COLORS["GREEN"])
    confirmBackRect = confirmBack.get_rect()
    confirmBackRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # house buttons
    for house in houses:
      houseMessageSurf = self.BASICFONT.render(f"  {house}  ", 1, COLORS["BLACK"])
      houseMessageRect = houseMessageSurf.get_rect()
      houseMessageRect.top = messageRect[1] + messageRect[3] + self.margin
      houseBackSurf = Surface((houseMessageSurf.get_width(), houseMessageSurf.get_height()))
      if colors:
        houseBackSurf.fill(COLORS[colors[houses.index(house)]])
      else:
        houseBackSurf.fill(COLORS["YELLOW"])
      houseBackRect = houseBackSurf.get_rect()
      houseBackRect.top = messageRect[1] + messageRect[3] + self.margin
      houses_rects.append(( houseBackSurf, houseBackRect, houseMessageSurf, houseMessageRect))
    length = sum(house[1][2] for house in houses_rects) + (self.margin * (len(houses_rects) - 1))
    left = (WIDTH // 2) - (length // 2)
    for house_rect in houses_rects:
      house_rect[1].left = left
      house_rect[3].left = left
      left += house_rect[1][2] + self.margin
    # then this loop will handle drawing those options
    selected = 0
    while True:
      if highlight:
        self.extraDraws = self.previewHouse(highlight)
        self.cardChanged()
      else:
        self.extraDraws = []
      if selected:
        self.extraDraws += [(confirmBack, confirmBackRect), (confirmSurf, confirmRect)] + [item for sublist in [[(x[0], x[1]), (x[2], x[3])] for x in houses_rects] for item in sublist]
        if varAsStr == "activeHouse":
          for c in self.activePlayer.hand + self.activePlayer.board["Creature"] + self.activePlayer.board["Artifact"]:
            c.selected = False
          self.extraDraws += self.previewHouse(lambda x: x.house == self.activePlayer.houses[selected - 1] or (x.type == "Creature" and "experimental_therapy" in [y.title for y in x.upgrade]))
          self.cardChanged()
      else:
        self.extraDraws += [(messageBackSurf, messageBackRect), (messageSurf, messageRect)] + [item for sublist in [[(x[0], x[1]), (x[2], x[3])] for x in houses_rects] for item in sublist]
        if varAsStr == "activeHouse":
          for c in self.activePlayer.hand + self.activePlayer.board["Creature"] + self.activePlayer.board["Artifact"]:
            c.selected = False
      for e in pygame.event.get():
        if e.type == QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if selected and Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
            self.extraDraws = []
            self.cardChanged()
            return [houses[clicked]]
          click = [Rect.collidepoint(x[1], (self.mousex, self.mousey)) for x in houses_rects]
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
          elif True in self.friendDraws and Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
              card.rect.topleft = OB
            self.cardChanged()
          elif True not in self.enemyDraws:
            if self.drawAction:
              if Rect.collidepoint(self.actionMinRect, (self.mousex, self.mousey)):
                self.drawAction = False
                self.cardChanged()
            else:
              if Rect.collidepoint(self.actionMaxRect, (self.mousex, self.mousey)):
                self.drawAction = True
                self.cardChanged()
          elif True in self.enemyDraws and Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
              card.rect.topleft = OB
            self.cardChanged()
          elif not self.drawFriendDiscard and Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          elif not self.drawFriendPurge and Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
            self.drawFriendPurge = True
          elif not self.drawEnemyPurge and Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
            self.drawEnemyPurge = True
          elif not self.drawFriendArchive and Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
            self.drawFriendArchive = True
          elif not self.drawEnemyArchive and Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
            self.drawEnemyArchive = True
      if Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
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
        Valid targetPool options: Creature, Artifact, [in progress: Board (ie Creature or Artifact)], Hand, Discard, [future set: Archive]\n
        Valid message: any string
        Valid canHit: either, both, enemy, friend\n
        Count is max number of choices\n
        If full is True, you can only submit when your target list length is equal to count\n
        If a condition is set, only cards that match the condition can be picked\n
        If condition isn't met, the con_message is displayed
    """
    self.cardChanged(True)

    # message
    messageSurf = self.BASICFONT.render(message, 1, COLORS["WHITE"])
    messageRect = messageSurf.get_rect()
    messageRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # message background
    backgroundSurf = Surface((messageSurf.get_width(), messageSurf.get_height()))
    backgroundSurf.convert()
    backgroundRect = backgroundSurf.get_rect()
    backgroundRect.center = (WIDTH // 2, (HEIGHT // 2) - (self.target_cardh // 4))
    # confirm
    confirmSurf = self.BASICFONT.render("  CONFIRM  ", 1, COLORS["WHITE"])
    confirmRect = confirmSurf.get_rect()
    confirmRect.top = messageRect[1] + messageRect[3] + self.margin
    confirmRect.right = (WIDTH // 2) - (self.margin // 2)
    # confirm background
    confirmBack = Surface((confirmSurf.get_width(), confirmSurf.get_height()))
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
    cancelBack = Surface((cancelSurf.get_width(), cancelSurf.get_height()))
    cancelBack.convert()
    cancelBack.fill(COLORS["RED"])
    cancelBackRect = cancelBack.get_rect()
    cancelBackRect.top = messageRect[1] + messageRect[3] + self.margin
    cancelBackRect.left = (WIDTH // 2)  + (self.margin // 2)
    
    # selectedSurf = Surface((self.target_cardw, self.target_cardh))
    # selectedSurf.convert_alpha()
    # selectedSurf.set_alpha(80)
    # selectedSurf.fill(COLORS["LIGHT_GREEN"])

    # selectedSurfTapped = Surface((self.target_cardh, self.target_cardw))
    # selectedSurfTapped.convert_alpha()
    # selectedSurfTapped.set_alpha(80)
    # selectedSurfTapped.fill(COLORS["LIGHT_GREEN"])

    # invalidSurf = Surface((self.target_cardw, self.target_cardh))
    # invalidSurf.convert_alpha()
    # invalidSurf.set_alpha(80)
    # invalidSurf.fill(COLORS["RED"])

    # invalidSurfTapped = Surface((self.target_cardh, self.target_cardw))
    # invalidSurfTapped.convert_alpha()
    # invalidSurfTapped.set_alpha(80)
    # invalidSurf.fill(COLORS["RED"])
    

    # invalid = []

    if canHit == "friend":
      target = self.activePlayer
      other = self.inactivePlayer
      for c in other.board["Creature"] + other.board["Artifact"] + other.hand + other.discard + other.archive:
        c.invalid = True
    elif canHit == "enemy":
      target = self.inactivePlayer
      other = self.activePlayer
      for c in other.board["Creature"] + other.board["Artifact"] + other.hand + other.discard + other.archive:
        c.invalid = True
    elif canHit == "both":
      target = self.activePlayer
      other = self.inactivePlayer
    elif canHit == "either":
      target = self.activePlayer
      other = self.inactivePlayer
    else:
      logging.error(f"Invalid canhit: {canHit}")
      raise ValueError
    
    if targetPool == "Hand":
      for card in target.hand:
        if not condition(card):
          card.invalid = True
      for card in target.board["Creature"] + target.board["Artifact"] + target.discard + target.archive:
        card.invalid = True
    elif targetPool == "Discard":
      for card in target.discard:
        if not condition(card):
          card.invalid = True
      for card in target.board["Creature"] + target.board["Artifact"] + target.hand + target.archive:
        card.invalid = True
    elif targetPool == "Archive":
      for card in target.archive:
        if not condition(card):
          card.invalid = True
      for card in target.board["Creature"] + target.board["Artifact"] + target.hand + target.discard:
        card.invalid = True
    elif targetPool == "Board":
      targetPool = "Creature"
      otherPool = "Artifact"
      for card in target.hand + target.discard + target.archive + other.hand + other.discard + other.archive:
        card.invalid = True
    else: # targetPool == "Artifact" or "Creature"
      if targetPool == "Artifact":
        otherPool = "Creature"
      elif targetPool == "Creature":
        otherPool = "Artifact"
      else:
        logging.error("Invalid targetPool")
      for card in target.hand + target.discard + target.archive + other.hand + other.discard + other.archive:
        card.invalid = True
      if canHit == "both" or canHit == "either":
        allowable = target.board[targetPool] + other.board[targetPool]
        unallowable = target.board[otherPool] + other.board[otherPool]
        for card in allowable:
          if not condition(card):
            card.invalid = True
        for card in unallowable:
          card.invalid = True
            # if card.ready:
            #   card.invalid = True # invalid.append((invalidSurf, card.rect))
            # else:
            #   card.invalid = True # invalid.append((invalidSurfTapped, card.tapped_rect))
      if canHit == "friend" or canHit == "enemy":
        for card in target.board[targetPool]:
          if not condition(card):
            card.invalid = True
            # if card.ready:
            #   card.invalid = True # invalid.append((invalidSurf, card.rect))
            # else:
            #   card.invalid = True # invalid.append((invalidSurfTapped, card.tapped_rect))  
        for card in target.board[otherPool] + other.board[targetPool] + other.board[otherPool]:
          card.invalid = True
        
    # selected = []
    retVal = []
    every = target.board["Creature"] + target.board["Artifact"] + other.board["Creature"] + other.board["Artifact"] + target.discard + other.discard + target.hand + other.hand + target.archive + other.archive
    if sum(c.invalid for c in every) == len(every):
      logging.info("No valid targets.")
      for c in every:
        c.invalid = False
      self.cardChanged()
      logging.info(f"Nothing targeted.")
      return retVal
    self.cardChanged()
    while True:
      self.extraDraws = [(backgroundSurf, backgroundRect), (messageSurf, messageRect), (confirmBack, confirmBackRect), (confirmSurf, confirmRect), (cancelBack, cancelBackRect), (cancelSurf, cancelRect)] # + invalid + selected
      for e in pygame.event.get():
        if e.type == QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          self.friendDraws = [self.drawFriendDiscard, self.drawFriendArchive, self.drawFriendPurge]
          self.enemyDraws = [self.drawEnemyDiscard, self.drawEnemyArchive, self.drawEnemyPurge]
          if Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
            self.extraDraws = []
            if retVal and not full:
              if len(retVal) <= count and not full:
                for c in every:
                  c.selected = False
                  c.invalid = False
                self.cardChanged()
                logging.info(f"{[c.title for c in retVal]} targeted.")
                return retVal
              else:
                pyautogui.alert("Not enough targets selected!")
            elif retVal and full and len(retVal) == count:
              for c in every:
                c.selected = False
                c.invalid = False
              self.cardChanged()
              logging.info(f"{[c.title for c in retVal]} targeted.")
              return retVal
            elif not full:
              incomplete = None
              while not incomplete:
                incomplete = self.chooseHouse("custom", ("Are you sure you want to target nothing?", ["Yes", "No"]))
              if incomplete == "Yes":
                for c in every:
                  c.selected = False
                  c.invalid = False
                self.cardChanged()
                logging.info(f"{[c.title for c in retVal]} targeted. Should be nothing.")
                return retVal
          elif Rect.collidepoint(cancelBackRect, (self.mousex, self.mousey)):
            for c in retVal:
              c.selected = False
            retVal = []
            if canHit == "either": # in which case, otherPool and targetPool will be defined
              allowable = target.board[targetPool] + other.board[targetPool]
              unallowable = target.board[otherPool] + other.board[otherPool] + target.hand + target.discard + target.archive + other.hand + other.discard + other.archive
              for card in allowable:
                if not condition(card):
                  card.invalid = True
                else:
                  card.invalid = False
              for card in unallowable:
                card.invalid = True
            confirmBack.fill(COLORS["GREEN"])
            self.cardChanged()
          elif True in self.friendDraws and Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            self.drawFriendArchive = False
            self.drawFriendPurge = False
            for card in self.activePlayer.discard + self.activePlayer.purged + self.activePlayer.archive:
              card.rect.topleft = OB
            self.cardChanged()
          elif True not in self.enemyDraws:
            if self.drawAction:
              if Rect.collidepoint(self.actionMinRect, (self.mousex, self.mousey)):
                self.drawAction = False
                self.cardChanged()
            else:
              if Rect.collidepoint(self.actionMaxRect, (self.mousex, self.mousey)):
                self.drawAction = True
                self.cardChanged()
          elif True in self.enemyDraws and Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawEnemyArchive = False
            self.drawEnemyPurge = False
            for card in self.inactivePlayer.discard + self.inactivePlayer.purged + self.inactivePlayer.archive:
              card.rect.topleft = OB
            self.cardChanged()
          elif not self.drawFriendDiscard and Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          elif not self.drawFriendPurge and Rect.collidepoint(self.purge1_rect, (self.mousex, self.mousey)):
            self.drawFriendPurge = True
          elif not self.drawEnemyPurge and Rect.collidepoint(self.purge2_rect, (self.mousex, self.mousey)):
            self.drawEnemyPurge = True
          elif not self.drawFriendArchive and Rect.collidepoint(self.archive1_rect, (self.mousex, self.mousey)):
            self.drawFriendArchive = True
          elif not self.drawEnemyArchive and Rect.collidepoint(self.archive2_rect, (self.mousex, self.mousey)):
            self.drawEnemyArchive = True
          if canHit == "either": # in which case, otherPool and targetPool will be defined
            for c in every:
              if True in [Rect.collidepoint(c.rect, (self.mousex, self.mousey)), Rect.collidepoint(c.tapped_rect, (self.mousex, self.mousey))]:
                if not c.invalid:
                  if len(retVal) <= count:
                    if c.selected:
                      c.selected = False
                      retVal.remove(c)
                      if not retVal:
                        allowable = target.board[targetPool] + other.board[targetPool]
                        unallowable = target.board[otherPool] + other.board[otherPool] + target.hand + target.discard + target.archive + other.hand + other.discard + other.archive
                        for card in allowable:
                          if not condition(card):
                            card.invalid = True
                          else:
                            card.invalid = False
                        for card in unallowable:
                          card.invalid = True
                    elif len(retVal) < count:
                      c.selected = True
                      retVal.append(c)
                      if c in target.board[targetPool] + target.board[otherPool] + target.hand + target.archive + target.discard:
                        for c2 in other.board[targetPool] + other.board[otherPool] + other.hand + other.archive + other.discard:
                          c2.invalid = True
                      else:
                        for c2 in target.board[targetPool] + target.board[otherPool] + target.hand + target.archive + target.discard:
                          c2.invalid = True
                  else:
                    logging.info(f"{c.title} is not a valid target.")
                self.cardChanged()
            # if retVal is empty, figure out which side has been selected and mark the other side as invalid now
            # now for future selections we'll only need to make sure the target is valid
          else:
            # we can just check if the target is invalid or selected
            for c in every:
              if True in [Rect.collidepoint(c.rect, (self.mousex, self.mousey)), Rect.collidepoint(c.tapped_rect, (self.mousex, self.mousey))]:
                if not c.invalid:
                  if len(retVal) <= count:
                    if c.selected:
                      c.selected = False
                      retVal.remove(c)
                    elif len(retVal) < count:
                      c.selected = True
                      retVal.append(c)
                else:
                  logging.info(f"{c.title} is not a valid target.")
                self.cardChanged()
          # if targetPool != "Hand":
          #   if targetPool == "Discard":
          #     if canHit == "both": # this means I can select from both boards at the same time, eg natures call
          #       friend = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
          #       if True in friend:
          #         index = friend.index(True)
          #         card = self.activePlayer.discard[index]
          #         if condition(card):
          #           toAdd = ("fr", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             card.selected = True # selected.append((selectedSurf, card.rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             card.selected = False # selected.remove((selectedSurf, card.rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #       foe = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
          #       if True in foe:
          #         index = foe.index(True)
          #         card = self.inactivePlayer.discard[index]
          #         if condition(card):
          #           toAdd = ("fo", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             card.selected = True # selected.append((selectedSurf, card.rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             card.selected = False # selected.remove((selectedSurf, card.rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #     elif canHit == "either": # this means I can select multiples, but only all from same side
          #       friend = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
          #       if True in friend and (not retVal or retVal[0][0] == "fr"):
          #         index = friend.index(True)
          #         card = self.activePlayer.discard[index]
          #         if condition(card):
          #           toAdd = ("fr", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             card.selected = True # selected.append((selectedSurf, card.rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             card.selected = False # selected.remove((selectedSurf, card.rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #       foe = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
          #       if True in foe and (not retVal or retVal[0][0] == "fo"):
          #         index = foe.index(True)
          #         card = self.inactivePlayer.discard[index]
          #         if condition(card):
          #           toAdd = ("fo", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             card.selected = True # selected.append((selectedSurf, card.rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             card.selected = False # selected.remove((selectedSurf, card.rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #     elif canHit == "enemy": # this means I can only target unfriendlies
          #       foe = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
          #       if True in foe:
          #         index = foe.index(True)
          #         card = self.inactivePlayer.discard[index]
          #         if condition(card):
          #           toAdd = ("fo", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             card.selected = True # selected.append((selectedSurf, card.rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             card.selected = False # selected.remove((selectedSurf, card.rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #     elif canHit == "friend": # this means I can only target friendlies
          #       friend = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
          #       if True in friend:
          #         index = friend.index(True)
          #         card = self.activePlayer.discard[index]
          #         if condition(card):
          #           toAdd = ("fr", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             card.selected = True # selected.append((selectedSurf, card.rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             card.selected = False # selected.remove((selectedSurf, card.rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #   else: # Creature or Artifact
          #     if canHit == "both": # this means I can select from both boards at the same time, eg natures call
          #       friend = [(Rect.collidepoint(card.rect, (self.mousex, self.mousey)) or Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey))) for card in active[targetPool]]
          #       if True in friend:
          #         index = friend.index(True)
          #         card = active[targetPool][index]
          #         if condition(card):
          #           toAdd = ("fr", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             if card.ready:
          #               card.selected = True # selected.append((selectedSurf, card.rect))
          #             else:
          #               card.selected = True # selected.append((selectedSurfTapped, card.tapped_rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             if card.ready:
          #               card.selected = False # selected.remove((selectedSurf, card.rect))
          #             else:
          #               card.selected = False # selected.remove((selectedSurfTapped, card.tapped_rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #       foe = [(Rect.collidepoint(card.rect, (self.mousex, self.mousey)) or Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey))) for card in inactive[targetPool]]
          #       if True in foe:
          #         index = foe.index(True)
          #         card = inactive[targetPool][index]
          #         if condition(card):
          #           toAdd = ("fo", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             if card.ready:
          #               card.selected = True # selected.append((selectedSurf, card.rect))
          #             else:
          #               card.selected = True # selected.append((selectedSurfTapped, card.tapped_rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             if card.ready:
          #               card.selected = False # selected.remove((selectedSurf, card.rect))
          #             else:
          #               card.selected = False # selected.remove((selectedSurfTapped, card.tapped_rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #     elif canHit == "either": # this means I can select multiples, but only all from same side
          #       friend = [(Rect.collidepoint(card.rect, (self.mousex, self.mousey)) or Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey))) for card in active[targetPool]]
          #       if True in friend and (not retVal or retVal[0][0] == "fr"):
          #         index = friend.index(True)
          #         card = active[targetPool][index]
          #         if condition(card):
          #           toAdd = ("fr", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             if card.ready:
          #               card.selected = True # selected.append((selectedSurf, card.rect))
          #             else:
          #               card.selected = True # selected.append((selectedSurfTapped, card.tapped_rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             if card.ready:
          #               card.selected = False # selected.remove((selectedSurf, card.rect))
          #             else:
          #               card.selected = False # selected.remove((selectedSurfTapped, card.tapped_rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #       foe = [(Rect.collidepoint(card.rect, (self.mousex, self.mousey)) or Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey))) for card in inactive[targetPool]]
          #       if True in foe and (not retVal or retVal[0][0] == "fo"):
          #         index = foe.index(True)
          #         card = inactive[targetPool][index]
          #         if condition(card):
          #           toAdd = ("fo", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             if card.ready:
          #               card.selected = True # selected.append((selectedSurf, card.rect))
          #             else:
          #               card.selected = True # selected.append((selectedSurfTapped, card.tapped_rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             if card.ready:
          #               card.selected = False # selected.remove((selectedSurf, card.rect))
          #             else:
          #               card.selected = False # selected.remove((selectedSurfTapped, card.tapped_rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #     elif canHit == "enemy": # this means I can only target unfriendlies
          #       foe = [(Rect.collidepoint(card.rect, (self.mousex, self.mousey)) or Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey))) for card in inactive[targetPool]]
          #       if True in foe:
          #         index = foe.index(True)
          #         card = inactive[targetPool][index]
          #         if condition(card):
          #           toAdd = ("fo", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             if card.ready:
          #               card.selected = True # selected.append((selectedSurf, card.rect))
          #             else:
          #               card.selected = True # selected.append((selectedSurfTapped, card.tapped_rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             if card.ready:
          #               card.selected = False # selected.remove((selectedSurf, card.rect))
          #             else:
          #               card.selected = False # selected.remove((selectedSurfTapped, card.tapped_rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          #     elif canHit == "friend": # this means I can only target friendlies
          #       friend = [(Rect.collidepoint(card.rect, (self.mousex, self.mousey)) or Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey))) for card in active[targetPool]]
          #       if True in friend:
          #         index = friend.index(True)
          #         card = active[targetPool][index]
          #         if condition(card):
          #           toAdd = ("fr", index)
          #           if toAdd not in retVal and len(retVal) < count:
          #             if card.ready:
          #               card.selected = True # selected.append((selectedSurf, card.rect))
          #             else:
          #               card.selected = True # selected.append((selectedSurfTapped, card.tapped_rect))
          #             retVal.append(toAdd)
          #           elif toAdd in retVal:
          #             retVal.remove(toAdd)
          #             if card.ready:
          #               card.selected = False # selected.remove((selectedSurf, card.rect))
          #             else:
          #               card.selected = False # selected.remove((selectedSurfTapped, card.tapped_rect))
          #         else:
          #           logging.info(con_message)
          #           self.cardChanged()
          #           break
          # else:
          #   if canHit == "enemy":
          #     hand = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.hand]
          #     if True in hand:
          #       index = hand.index(True)
          #       card = self.activePlayer.hand[index]
          #       if condition(card):
          #         toAdd = ("fo", index)
          #         if toAdd not in retVal and len(retVal) < count:
          #           card.selected = True # selected.append((selectedSurf, card.rect))
          #           retVal.append(toAdd)
          #         elif toAdd in retVal:
          #           retVal.remove(toAdd)
          #           card.selected = False # selected.remove((selectedSurf, card.rect))
          #       else:
          #         logging.info(con_message)
          #         self.cardChanged()
          #         break
          #   else:
          #     hand = [Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.hand]
          #     if True in hand:
          #       index = hand.index(True)
          #       card = self.activePlayer.hand[index]
          #       if condition(card):
          #         toAdd = ("fr", index)
          #         if toAdd not in retVal and len(retVal) < count:
          #           card.selected = True # selected.append((selectedSurf, card.rect))
          #           retVal.append(toAdd)
          #         elif toAdd in retVal:
          #           retVal.remove(toAdd)
          #           card.selected = False # selected.remove((selectedSurf, card.rect))
          #       else:
          #         logging.info(con_message)
          #         self.cardChanged()
          #         break
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


  def chooseTriggers(self, triggers: List) -> List:
    """ Will let the active player order triggers or choose one of a list of triggers (for instances where a card might have gained multiple action triggers).
    """
    ## TODO: Figure out how to describe the triggers.



                #####################
                # End of Game Class #
                #####################

def developer(game):
  """Developer functions for manually changing the game state.
  """


