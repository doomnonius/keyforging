from tkinter.constants import E
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, MOUSEMOTION, SRCALPHA
import decks.decks as deck
import cards.cardsAsClass as card
import json, random, logging, time, pygame, pyautogui, os
from helpers import makeChoice, buildStateDict, absa
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
    self.activeHouse = []
    self.turnNum = 0
    self.playedThisTurn = []
    self.discardedThisTurn = []
    self.usedThisTurn = []
    self.playedLastTurn = []
    self.discardLastTurn = []
    self.usedLastTurn = []
    self.extraFightHouses = []
    self.forgedThisTurn = False
    self.forgedLastTurn = False
    self.turnStage = None
    self.response = []
    self.pendingReloc = []
    self.extraDraws = []
    self.resetStates = []
    self.resetStatesNext = []
    self.drawFriendDiscard = False
    self.closeFriendDiscard = None
    self.drawEnemyDiscard = False
    self.closeEnemyDiscard = None
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
    self.FPS = 30
    self.WIN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.SRCALPHA) #, flags = pygame.FULLSCREEN)
    self.BASICFONT = pygame.font.SysFont("Corbel", HEIGHT // 27)
    self.OTHERFONT = pygame.font.SysFont("Corbel", HEIGHT // 14)
    self.margin = HEIGHT // 108
    pygame.display.set_caption('Keyforge')
    self.CLOCK = pygame.time.Clock()
    self.target_cardh = HEIGHT // 7
    ratio = CARDH / self.target_cardh
    self.target_cardw = int(CARDW // ratio)
    first = random.choice([self.first, self.second])
    self.activePlayer = deck.Deck(deck.deckName(first), self.target_cardw, self.target_cardh)
    if first == self.first:
      self.inactivePlayer = deck.Deck(deck.deckName(self.second), self.target_cardw, self.target_cardh)
    else:
      self.inactivePlayer = deck.Deck(deck.deckName(self.first), self.target_cardw, self.target_cardh)
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
      return ["You can't use a card that isn't ready."]
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      return ["'Skippy Timehog' is preventing you from using cards"]
    if card.type == "Creature":
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        return ["You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'."]
      if (card.house in self.activeHouse or card.house in self.extraFightHouses or card.title == "tireless_crocag"):
        if card.house in self.activeHouse and card.title != "tireless_crocag":
          retVal.append("Reap")
        if card.stun:
          return ["Unstun"]
        if len(self.inactivePlayer.board["Creature"]) > 0:
        # put a check here for the cards that can't fight, or things that prevent fight
          if "foggify" in self.inactivePlayer.states and self.inactivePlayer.states["foggify"] \
          or "fogbank" in self.inactivePlayer.states and self.inactivePlayer.states["fogbank"]:
          # bigtwig can only attack stunned
            pass
          else:
            retVal.append("Fight")
    if card.action:
      retVal.append("Action")
    if card.omni:
      retVal.append("Omni")
    if not retVal:
      return ["You can't use this card right now."]
    return retVal

  def handOptions(self, cardNum: int) -> List:
    # There are other things that prevent playing cards that I want to include here as well, think I have most of them
    card = self.activePlayer.hand[cardNum]
    if card.house in self.activeHouse or ("phase_shift" in self.activePlayer.states and self.activePlayer.states["phase_shift"] > 0):
      if self.turnNum == 1 and len(self.playedThisTurn) >= 1:
        return ["No remaining plays this turn"]
      if "ember_imp" in [x.title for x in self.inactivePlayer.board["Creature"]] and len(self.playedThisTurn) >= 2:
        return ["'Ember Imp' prevents playing this", "Discard"]
      if card.type == "Upgrade" and len(self.activePlayer.board["Creature"]) == 0 and len(self.inactivePlayer.board["Creature"]) == 0:
        return ["Cannot play upgrade with no creatures in play", "Discard"]
      if card.type == "Action" and "scrambler_storm" in self.inactivePlayer.states and self.inactivePlayer.states["scrambler_storm"]:
        return ["'Scrambler Storm' prevents playing actions this turn", "Discard"]
      if "treasure_map" in self.activePlayer.states and self.activePlayer.states["treasure_map"]:
        return ["'Treasure Map' prevents playing more cards this turn", "Discard"]
      if card.type == "Creature":
        if card.title == "truebaru" and self.activePlayer.amber < 3:
          return ["You must have 3 amber to sacrifice in order to play 'Truebaru'", "Discard"]
        if card.title == "kelifi_dragon" and self.activePlayer.amber < 7:
          return ["You need 7 amber to play 'Kelifi Dragon'", "Discard"]
        if "grommid" in [x.title for x in self.activePlayer.board["Creature"]]:
          return ["You can't play creatures with 'Grommid' in play", "Discard"]
        if "lifeward" in self.inactivePlayer.states and self.inactivePlayer.states["lifeward"]:
          return ["You can't play creatures because of 'Lifeward'", "Discard"]
      return ["Play", "Discard"]
    else:
      return ["Cannot interact with card not in active house."]

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

    # houses corner
    self.houses2 = pygame.Surface((self.target_cardw, mat_third // 2))
    self.houses2.convert()
    self.houses2.fill(COLORS["GREY"])
    self.houses2_rect = self.houses2.get_rect()
    self.houses2_rect.topright = (wid, mat_third * 2)
    self.board_blits.append((self.houses2, self.houses2_rect))

    ## divider2
    self.divider2 = pygame.Surface((wid // 5, mat_third))
    self.divider2.convert()
    self.divider2.fill(COLORS["GREY"])
    div2_w = self.divider2.get_width()
    self.divider2_rect = self.divider2.get_rect()
    self.divider2_rect.topright = (wid, int(mat_third * 2.5))
    self.key2y, self.key2y_rect = load_image("yellow_key_back", -1)
    self.key2y_rect.topright = (div2_w - 2 - self.target_cardw - self.margin, 0)
    self.key2r, self.key2r_rect = load_image("yellow_key_back", -1)
    self.key2r_rect.topright = (div2_w - 2 - self.target_cardw - self.margin, self.key2y.get_height() + self.margin)
    self.key2b, self.key2b_rect = load_image("yellow_key_back", -1)
    self.key2b_rect.topright = (div2_w - 2 - self.target_cardw - self.margin, self.key2y.get_height() * 2 + self.margin * 2)
    self.board_blits.append((self.divider2, self.divider2_rect))

    # purge2 / decklist2
    self.purge2 = pygame.Surface((self.target_cardw + self.margin, mat_third))
    self.purge2.convert()
    self.purge2.fill(COLORS["RED"])
    self.purge2_rect = self.purge2.get_rect()
    self.purge2_rect.topright = (wid, int(mat_third * 2.5))
    self.board_blits.append((self.purge2, self.purge2_rect))

    ## divider1
    self.divider = pygame.Surface((wid // 5, mat_third))
    self.divider.convert()
    self.divider.fill(COLORS["GREEN"])
    self.divider_rect = self.divider.get_rect()
    self.divider_rect.topleft = (0, int(mat_third * 2.5))
    self.key1y, self.key1y_rect = load_image("yellow_key_back", -1)
    self.key_forged, self.key_forged_rect = load_image("yellow_key_front", -1)
    self.key1y_rect.topleft = (2 + self.target_cardw + self.margin, 0)
    self.key1r, self.key1r_rect = load_image("yellow_key_back", -1)
    self.key1r_rect.topleft = (2 + self.target_cardw + self.margin, self.key1y.get_height() + self.margin)
    self.key1b, self.key1b_rect = load_image("yellow_key_back", -1)
    self.key1b_rect.topleft = (2 + self.target_cardw + self.margin, self.key1y.get_height() * 2 + self.margin * 2)
    self.board_blits.append((self.divider, self.divider_rect))

    # purge/decklist
    self.purge1 = pygame.Surface((self.target_cardw + self.margin, mat_third))
    self.purge1.convert()
    self.purge1.fill(COLORS["RED"])
    self.purge1_rect = self.purge1.get_rect()
    self.purge1_rect.topleft = (0, int(mat_third * 2.5))
    self.board_blits.append((self.purge1, self.purge1_rect))

    ## active mat
    self.mat1 = pygame.Surface((wid, hei // 2))
    self.mat1.convert()
    self.mat1.fill(COLORS["BLACK"])
    self.mat1_rect = self.mat1.get_rect()
    self.mat1_rect.topleft = (0, int(mat_third * 3.5))
    self.board_blits.append((self.mat1, self.mat1_rect))

    # houses
    self.houses1 = pygame.Surface((self.target_cardw, mat_third // 2))
    self.houses1.convert()
    self.houses1.fill(COLORS["GREEN"])
    self.houses1_rect = self.houses1.get_rect()
    self.houses1_rect.topleft = (0, int(mat_third * 3.5))
    self.board_blits.append((self.houses1, self.houses1_rect))

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
    self.discard1_rect.topleft = (0, mat_third * 5)
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

    ## neutral zone - easier if we have this and can blit to it
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

    # log


    run = True

    while run:
      self.CLOCK.tick(self.FPS)
      
      # this feels like a weird place to put this, but it works? as long as only one tireless on the field at a time
      active = self.activePlayer.board["Creature"]
      inactive = self.inactivePlayer.board["Creature"]
      length = len(active)
      if len(inactive) == 0 and "tireless_crocag" in [x.title for x in active]:
        for x in range(1, length+1):
          if active[length-x].title == "tireless_crocag":
            self.pendingReloc.append(active.pop(length-x))
      length = len(inactive)
      if len(active) == 0 and "tireless_crocag" in [x.title for x in inactive]:
        for x in range(1, length+1):
          if inactive[length-x].title == "tireless_crocag":
            self.pendingReloc.append(inactive.pop(length-x))
      if self.pendingReloc:
        self.pending()


      for event in pygame.event.get():
        
        if event.type == pygame.MOUSEMOTION:
          #update mouse position
          self.mousex, self.mousey = event.pos

        if event.type == pygame.QUIT:
          run = False

        if event.type == MOUSEBUTTONDOWN and event.button == 3:
          self.hovercard = []
          self.draw() # this only works because of the update in doPopup
          self.doPopup()
          
        if event.type == MOUSEBUTTONUP and event.button == 1:
          if pygame.Rect.collidepoint(self.endBackRect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            self.drawFriendDiscard = False
            for card in self.inactivePlayer.discard + self.activePlayer.discard:
              card.rect.topleft = (-500, -500)
            self.turnStage += 1
          elif self.drawFriendDiscard and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            for card in self.activePlayer.discard:
              card.rect.topleft = (-500, -500)
          elif self.drawEnemyDiscard and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            for card in self.inactivePlayer.discard:
              card.rect.topleft = (-500, -500)
          elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          
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
        self.forgedThisTurn = False
        #####################
        # Draw and mulligan #
        #####################
        if not self.do:
          logging.info(f"{self.activePlayer.name} is going first.")
          pyautogui.alert(f"\n{self.activePlayer.name} is going first.\n")
          self.activePlayer += 7
        else:
          mull = self.chooseMulligan("Player 1")
          if mull:
            for card in self.activePlayer.hand:
              self.activePlayer.deck.append(card)
            random.shuffle(self.activePlayer.deck)
            self.activePlayer.hand = []
            self.activePlayer += 6
        if not self.do:
          self.inactivePlayer += 6
        else:
          mull2 = self.chooseMulligan("Player 2")
          if mull2:
            for card in self.inactivePlayer.hand:
              self.inactivePlayer.deck.append(card)
            random.shuffle(self.inactivePlayer.deck)
            self.inactivePlayer.hand = []
            self.inactivePlayer += 5
          self.turnNum = 1
          self.turnStage = 0
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
        if self.checkForgeStates(): # returns True if you can forge, false if you can't (and why you can't), which in CotA is basically only Miasma
          self.forgeKey("active", self.calculateCost())
          # else:
          #   pyautogui.alert("No key forged this turn, not enough amber.")
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
        self.activeHouse = self.chooseHouse("activeHouse")
        if len(self.activePlayer.archive) > 0:
          # self.activePlayer.printShort(self.activePlayer.archive)
          show = 'Would you like to pick up your archive? It contains:\n\n'
          for card in self.activePlayer.archive:
            show += f"{card.title} [{card.house}]\n"
          archive = pyautogui.confirm(show, buttons=["Yes", "No"])
          if archive == "Yes":
            self.pendingReloc = self.activePlayer.archive
            self.pending('hand')
        self.turnStage += 1

      ###############################################################################
      # step 3: play, discard, or use cards (and also inquire about the game state) #
      ###############################################################################

      elif self.turnStage == 3:
        if self.response:
          # print(self.response)
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
            pyautogui.alert("There are " + str(len(self.inactivePlayer.archive) + " cards in your opponent's archive."))
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
            self.actionCard(self.targetCard, self.loc)

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
          self.forgedLastTurn = self.forgedThisTurn
        else:
          self.forgedThisTurn = False
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
        if self.resetStates:
          for key in self.resetStates:
            if key[0] == "a":
              self.activePlayer.states[key[1]] = 0
            if key[0] == "i":
              self.inactivePlayer.states[key[1]] = 0
          self.resetStates = self.resetStatesNext.copy()
        self.resetStatesNext = []
        self.switch()
        self.turnNum += 1
        self.turnStage = 0
      
      if pygame.Rect.collidepoint(self.endBackRect, (self.mousex, self.mousey)):
        self.endBack.fill(COLORS["LIGHT_GREEN"])
      else:
        self.endBack.fill(COLORS["GREEN"])
      
      self.draw() # this will need hella updates
      pygame.display.flip()

    pygame.quit()


  def check_hover (self):
    hoverable = []
    if not self.drawFriendDiscard:
      hoverable += self.activePlayer.hand + self.activePlayer.board["Creature"]  + self.activePlayer.board["Artifact"]
    if not self.drawEnemyDiscard:
      hoverable += self.inactivePlayer.hand + self.inactivePlayer.board["Creature"] + self.inactivePlayer.board["Artifact"]
    if self.drawFriendDiscard:
      hoverable += self.activePlayer.discard
    if self.drawEnemyDiscard:
      hoverable += self.inactivePlayer.discard

    for card in hoverable:
      if pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)):
        self.hovercard = [card]
        break
      if pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)):
        self.hovercard = [card]
        break
  
  def draw(self, drawEnd: bool = True):
    # self.allsprites.update()
    self.WIN.blits(self.board_blits)
    
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
    self.amber2_rect.topright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key2y.get_width(), self.mat2_rect[1] + self.mat2_rect[3] + (3 * self.margin))

    # chains
    self.chains2 = self.BASICFONT.render(f"{self.inactivePlayer.chains} chains", 1, COLORS['BLACK'])
    self.chains2_rect = self.chains2.get_rect()
    self.chains2_rect.bottomright = (self.mat2_rect[0] + self.mat2_rect[2] - 2 - self.target_cardw - 10 - self.key2y.get_width(), self.mat1_rect[1] - (3 * self.margin))

    self.active_info = [(self.key1y, self.key1y_rect), (self.key1r, self.key1r_rect), (self.key1b, self.key1b_rect)]
    self.inactive_info = [(self.key2y, self.key2y_rect), (self.key2r, self.key2r_rect), (self.key2b, self.key2b_rect)]
    self.divider.blits(self.active_info)
    self.divider2.blits(self.inactive_info)
    self.WIN.blit(self.amber1, self.amber1_rect)
    self.WIN.blit(self.amber2, self.amber2_rect)
    self.WIN.blit(self.chains1, self.chains1_rect)
    self.WIN.blit(self.chains2, self.chains2_rect)
    # card areas
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
        self.WIN.blit(card_image, card_rect)
    # hands
    for board,area in [(self.activePlayer.hand, self.hand1_rect), (self.inactivePlayer.hand, self.hand2_rect)]:
      x = 0
      for card in board:
        card_image, card_rect = card.image, card.rect
        card.tapped_rect.topleft = (-500, -500)
        card_rect.topleft = (area.left + (x * self.target_cardw) + self.margin * (x + 1), area.top)
        x += 1
        self.WIN.blit(card_image, card_rect)
    # discards
    l = len(self.activePlayer.discard)
    if l > 0:
      card_image, card_rect = self.activePlayer.discard[l - 1].image, self.activePlayer.discard[l - 1].rect
      card_rect.topleft = (self.discard1_rect.left, self.discard1_rect.top)
      self.WIN.blit(card_image, card_rect)
    l = len(self.inactivePlayer.discard)
    if l > 0: 
      card_image, card_rect = self.inactivePlayer.discard[l - 1].image, self.inactivePlayer.discard[l - 1].rect
      card_rect.topleft = (self.discard2_rect.left, self.discard2_rect.top)
      self.WIN.blit(card_image, card_rect)
    # purged
    l = len(self.activePlayer.purged)
    if l > 0:
      card_image, card_rect = self.activePlayer.purged[l - 1].image, self.activePlayer.purged[l - 1].rect
      card_rect.center = self.purge1_rect.center
      self.WIN.blit(card_image, card_rect)
    l = len(self.inactivePlayer.purged)
    if l > 0: 
      card_image, card_rect = self.inactivePlayer.purged[l - 1].image, self.inactivePlayer.purged[l - 1].rect
      card_rect.center = self.purge2_rect.center
      self.WIN.blit(card_image, card_rect)
    # decks
    # going to need a card back of some sort to put here
    l = len(self.activePlayer.deck)
    if l > 0:
      card_image, card_rect = self.activePlayer.deck[-1].image, self.activePlayer.deck[-1].rect
      card_rect.topleft = (self.deck1_rect.left, self.deck1_rect.top)
      self.WIN.blit(card_image, card_rect)
    l = len(self.inactivePlayer.deck)
    if l > 0:
      card_image, card_rect = self.inactivePlayer.deck[-1].image, self.inactivePlayer.deck[-1].rect
      card_rect.topleft = (self.deck2_rect.left, self.deck2_rect.top)
      self.WIN.blit(card_image, card_rect)
    # self.allsprites.draw(self.WIN)
    if drawEnd:
      self.WIN.blit(self.endBack, self.endBackRect)
      self.WIN.blit(self.endText, self.endRect)
    if self.drawFriendDiscard:
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
      for card in self.activePlayer.discard[0:16]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + self.margin)
        x += 1
        self.WIN.blit(card.image, card.rect)
      x = 0
      for card in self.activePlayer.discard[16:]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 2 * self.margin + self.target_cardh)
        x += 1
        self.WIN.blit(card.image, card.rect)
    if self.drawEnemyDiscard:
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
      for card in self.inactivePlayer.discard[0:16]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + self.margin)
        x += 1
        self.WIN.blit(card.image, card.rect)
      x = 0
      for card in self.inactivePlayer.discard[16:]:
        card.rect.topleft = (discardBackRect.left + (x * self.target_cardw) + self.margin * (x + 1), discardBackRect.top + 2 * self.margin + self.target_cardh)
        x += 1
        self.WIN.blit(card.image, card.rect)
    if self.extraDraws:
      for pair in self.extraDraws:
        self.WIN.blit(pair[0], pair[1])
    if self.hovercard:
      hover, hover_rect = self.hovercard[0].orig_image, self.hovercard[0].orig_rect
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
      self.WIN.blit(hover, hover_rect)

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

  def checkForgeStates(self):
    """ Checks if there is anything in Deck.states["Forge"]. This isn't checking if you have enough amber.
    """
    if True: #optimization: if no cards in deck with this effect, just return
      pass # return True
    if "miasma" in self.inactivePlayer.states and self.inactivePlayer.states["miasma"]:
      pyautogui.alert("You skip your forge a key step this turn because your opponent played 'Miasma' last turn.")
      self.activePlayer.states["miasma"] = 0
      return False
    if "The Sting" in [x.title for x in self.activePlayer.board["Artifact"]]:
      pyautogui.alert("You skip your forge a key step this turn because you have 'The Sting' in play.")
      return False
    return True
    

##################
# Card functions #
##################

  def actionCard(self, cardNum: int, loc: str, omni: bool = False):
    """ Trigger a card's action from within the turn.
    """
    card = self.activePlayer.board[loc][cardNum]
    if card.house in self.activeHouse and not card.stun:
      # Trigger action
      try:
        eval(f"actions.key{card.number}(self, card)")
        # act.action(self, act)
      except:
        pyautogui.alert("Action failed.")
    elif card.stun:
      card.stun = False
    elif omni:
      try:
        eval(f"actions.key{card.number}(self, card)")
      except:
        pyautogui.alert("Omni failed.")
    card.ready = False
    self.usedThisTurn.append(card)
      
  
  def discardCard(self, cardNum: int):
    """ Discard a card from hand, within the turn. Doesn't need to use pending for discards, but does use it for Rock-Hurling Giant.
    """
    active = self.activePlayer.board["Creature"]
    inactive = self.inactivePlayer.board["Creature"]
    card = self.activePlayer.hand[cardNum]
    if card.house in self.activeHouse:
      self.activePlayer.discard.append(self.activePlayer.hand.pop(cardNum))
      if "rock_hurling_giant" in [x.title for x in active] and self.activePlayer.discard[-1].house == "Brobnar":
        targeting = self.chooseCards("Creature", "Deal 4 damage to:")[0]
        if targeting[0] == "fr":
          target = active[targeting[1]]
        else:
          target = inactive[targeting[1]]
        active[target].damageCalc(self, 4)
        if active[target].updateHealth():
          self.pendingReloc.append(active.pop(target))
        self.pending()
      self.discardedThisTurn.append(card)
    else:
      pyautogui.alert("You can only discard cards of the active house.")


  def fightCard(self, attacker: int):
    """ This is needed for cards that trigger fights (eg anger, gauntlet of command). If attacker is fed in to the function (which will only be done by cards that trigger fights), the house check is skipped.
    """
    # This will actually probably need to be incorporated into the main loop in some way
    card = self.activePlayer.board["Creature"][attacker]
    # this check is also in cardOptions, but sometimes things let you trigger a fight other ways
    if len(self.inactivePlayer.board["Creature"]) == 0:
      pyautogui.alert("Your opponent has no creatures for you to attack. Fight canceled.")
      return self
    if "foggify" in self.inactivePlayer.states and self.inactivePlayer.states["foggify"] \
    or "fogbank" in self.inactivePlayer.states and self.inactivePlayer.states["fogbank"]:
      pyautogui.alert("Fighting prevented by a fog effect.")
      return self
    if card.stun:
      pyautogui.alert("Creature is stunned and unable to fight. Unstunning creature instead.")
      card.stun = False
      card.ready = False
      self.usedThisTurn.append(card)
      return
    if attacker.title != "niffle_ape":
      defender = self.chooseCards("Creature", "Choose an enemy minion to attack:", "enemy", condition = lambda x: x.taunt or not (True in [y.taunt for y in x.neighbors()]), con_message = "This minion is protected by taunt.")[0][1]
    else:
      defender = self.chooseCards("Creature", "Choose an enemy minion to attack:", "enemy")[0][1]
    defenderCard = self.inactivePlayer.board["Creature"][defender]
    try:
      print("Trying to fight.")
      card.fightCard(defenderCard, self)
    except: print("Fight failed.")
    self.usedThisTurn.append(card)

  def pending(self, destination = "discard", destroyed = True):
    """ Pending is the function that handles when multiple cards leave play at the same time, whether it be to hand or to discard. It will trigger leaves play and destroyed effects. Allowable options for dest are 'purge', 'discard', 'hand', 'deck'.
    """
    active = self.activePlayer.board
    inactive = self.inactivePlayer.board
    L = self.pendingReloc

    if not L:
      return # just in case we feed it an empty list
    if destination not in ['purge', 'discard', 'hand', 'deck']:
      pyautogui.alert("Pending was given an invalid destination.")
      return
    if "annihilation_ritual" in ([x.title for x in active["Artifact"]] + [x.title for x in inactive["Artifact"]]) and destroyed:
      destination = "annihilate"
    if destination == "purge":
      length = len(L)
      for x in range(length):
        if L[absa(x, length)].deck == self.activePlayer.name:
          self.activePlayer.purge.append(L.pop(absa(x, length)))
        elif L[absa(x, length)].deck == self.inactivePlayer.name:
          self.inactivePlayer.purge.append(L.pop(absa(x, length)))
    if destination == "annihilate": # we'll do this one first to remove all creatures (b/c annihilation ritual only affects creatures)
      length = len(L)
      for x in range(length):
        if L[absa(x, length)].deck == self.activePlayer.name and L[absa(x, length)].type == "Creature":
          self.activePlayer.purge.append(L.pop(absa(x, length)))
        elif L[absa(x, length)].deck == self.inactivePlayer.name and L[absa(x, length)].type == "Creature":
          self.inactivePlayer.purge.append(L.pop(absa(x, length)))
        destination = "discard" #now that all the creatures are out
    if destination == "discard":
      length = len(L)
      pendingA = []
      pendingI = []
      for x in range(length):
        if L[absa(x, length)].deck == self.activePlayer.name:
          pendingA.append(L.pop(absa(x, length)))
        elif L[absa(x, length)].deck == self.inactivePlayer.name:
          pendingI.append(L.pop(absa(x, length)))
        # now that they're sorted by owner
      if len(pendingA) > 0:
        while len(pendingA) > 1:
          # choice = makeChoice("Choose which card to add to your discard first: ", pendingA)
          choice = 0
          self.activePlayer.discard.append(pendingA.pop(choice))
        self.activePlayer.discard.append(pendingA.pop())
      if len(pendingI) > 0:
        while len(pendingI) > 1:
          # choice = makeChoice("Choose which card to add to your opponent's discard first: ", pendingI)
          choice = 0
          if not destroyed:
            self.inactivePlayer.hand.append(pendingI.pop(choice))
          else:
            self.inactivePlayer.discard.append(pendingI.pop(choice))
        # this is for the edge case of discarding cards from your opponents archive - if you have cards in your opponent's archive, they don't get discarded but added to your hand
        choice = 0
        if not destroyed:
          self.inactivePlayer.hand.append(pendingI.pop(choice))
        else:
          self.inactivePlayer.discard.append(pendingI.pop(choice))
    if destination == "hand":
      length = len(L)
      for x in range(length):
        if L[absa(x, length)].deck == self.activePlayer.name:
          self.activePlayer.hand.append(L.pop(absa(x, length)))
        elif L[absa(x, length)].deck == self.inactivePlayer.name:
          self.inactivePlayer.hand.append(L.pop(absa(x, length)))
      self.activePlayer.hand.sort(key = lambda x: x.house)
      self.inactivePlayer.hand.sort(key = lambda x: x.house)
    if destination == "deck":
      length = len(L)
      pendingA = []
      pendingI = []
      for x in range(length):
        if L[absa(x, length)].deck == self.activePlayer.name:
          pendingA.append(L.pop(absa(x, length)))
        elif L[absa(x, length)].deck == self.inactivePlayer.name:
          pendingI.append(L.pop(absa(x, length)))
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
      pyautogui.alert("Pending did not properly empty the list.")


  def playCard(self, chosen: int, cheat: str = "Hand"):
    """ This is needed for cards that play other cards (eg wild wormhole). Will also simplify responses. Booly is a boolean that tells whether or not to check if the house matches.
    """
    print(f"numPlays: {len(self.playedThisTurn)}")
    if len(self.playedThisTurn) >= 1 and self.turnNum == 1 and "wild_wormhole" not in [x.title for x in self.activePlayer.board["Action"]]:
      pyautogui.alert("You cannot play another card this turn. But how'd you get here?")
      return
    if cheat == "Deck":
      source = self.activePlayer.deck
    elif cheat == "Discard":
      source = self.activePlayer.discard
    else:
      source = self.activePlayer.hand
    card = source[chosen]
    if "wild_wormhole" in [x.title for x in self.activePlayer.board["Action"]]:
      if card.type == "Action":
        if "scrambler_storm" in self.inactivePlayer.states and self.inactivePlayer.states["scrambler_storm"]:
          pyautogui.alert("'Scrambler Storm' prevents playing actions this turn, so you can't cheat this card out.")
          return
      elif card.type == "Creature":
        # game.inactivePlayer.states["lifeweb"] += 1
        if card.title == "kelifi_dragon" and self.activePlayer.amber < 7:
          pyautogui.alert("You need 7 amber to play 'Kelifi Dragon'")
          return
        if card.title == "truebaru" and self.activePlayer.amber < 3:
          pyautogui.alert("You must have 3 amber to sacrifice in order to play 'Truebaru'")
          return
        if "grommid" in [x.title for x in self.activePlayer.board["Creature"]]:
          pyautogui.alert("You can't play creatures with 'Grommid' in play")
          return
        if "lifeward" in self.inactivePlayer.states and self.inactivePlayer.states["lifeward"]:
          pyautogui.alert("You can't play creatures because of 'Lifeward'")
          return
    if (card.house not in self.activeHouse and card.house != "Logos") and ("phase_shift" in self.activePlayer.states and self.activePlayer.states["phase_shift"] > 0) and not cheat:
      self.activePlayer.states["phase_shift"] -= 1 # reset to false
      # Increases amber, adds the card to the action section of the board, then calls the card's play function
      # cardOptions() makes sure that you can't try to play a card you're not allowed to play
    flank = "Right"
    if card.amber > 0:
      self.activePlayer.gainAmber(card.amber, self)
      pyautogui.alert(f"{source[chosen].title} gave you {str(card.amber)} amber. You now have {str(self.activePlayer.amber)} amber.\n\nChange to a log when you fix the amber display issue.""")
    if card.type == "Creature" and len(self.activePlayer.board["Creature"]) > 0:
      flank = self.chooseHouse("custom", ("Choose which flank to play this creature on:", ["Left", "Right"]))[0]
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
      if len(self.activePlayer.board["Creature"]) == 0 and len(self.inactivePlayer.board["Creature"]) == 0:
        pyautogui.alert("No valid targets for this upgrade.")
        return self
      print("Choose a creature to play this upgrade on: ")
      targeted = self.chooseCards("Creature", "Choose a creature to attach the upgrade to:")[0]
      if targeted[0] == "fr":
        card = self.activePlayer.board["Creature"][targeted[1]]
      else:
        card = self.activePlayer.board["Creature"][targeted[1]]
      self.playUpgrade(card)
    #once the card has been added, then we trigger any play effects (eg smaaash will target himself if played on an empty board), use stored new position
    self.playedThisTurn.append(card)
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

  def playUpgrade(self, card: card.Card):
    """ Plays an upgrade on a creature.
    """

  def reapCard(self, cardNum: int):
    """ Triggers a card's reap effect from within the turn.
    """
    card = self.activePlayer.board["Creature"][cardNum]
    # check reap states when building cardOptions
    if not card.ready:
      pyautogui.alert("Can't reap with a card that isn't ready.")
      return
    if "skippy_timehog" in self.inactivePlayer.states and self.inactivePlayer.states["skippy_timehog"]:
      pyautogui.alert("'Skippy Timehog' is preventing you from using cards")
      return
    if card.type == "Creature":
      if card.title == "giant_sloth" and "Untamed" not in [x.house for x in self.discardedThisTurn]:
        pyautogui.alert("You haven't discarded an Untamed card this turn, so you cannot use 'Giant Sloth'.")
        return
      if card.title == "tireless_crocag":
        pyautogui.alert("'Tireless Crocag' can't reap")
    card.reap(self, card)
    # reaper.ready = False # commented out for testing
    return

  def forgeKey(self, player: str, cost: int):
    if "active":
      forger = self.activePlayer
      other = self.inactivePlayer
    else:
      forger = self.inactivePlayer
      other = self.activePlayer
    if forger.amber >= cost:
      forger.amber -= cost
      forger.keys += 1
      pyautogui.alert(f"You forged a key for {cost} amber. You now have {forger.keys} key(s) and {forger.amber} amber.\n")
      if player == "active" and "interdimensional_graft" in other.states and other.states["interdimensional_graft"] and forger.amber > 0:
        pyautogui.alert(f"Your opponent played 'Interdimensional Graft' last turn, so they gain your {forger.amber} leftover amber.")
        # can't use play.stealAmber b/c this isn't technically stealing so Vaultkeeper shouldn't be able to stop it
        other.gainAmber(forger.amber, self)
        forger.amber = 0
        pyautogui.alert(f"They now have {other.amber} amber.")
      if "bilgum_avalanche" in [x.title for x in forger.board["Creature"]]:
        # deal two damage to each enemy creature. I don't remember how I set this up to work
        length = len(other.board["Creature"])
        for x in range(1, length+1):
          card = other.board["Creature"][length-x]
          card.damageCalc(self, 2)
          if card.updateHealth():
            self.pendingReloc.append(other.board["Creature"].pop(length-x))
        self.pending()
      pyautogui.alert(f"{forger.name} now has {forger.keys} keys and {forger.amber} amber.")
      if player == "active":
        self.forgedThisTurn = True

  def chooseSide(self):
    side = None
    if not self.activePlayer.board["Creature"]:
      side = "Enemy"
    if not self.inactivePlayer.board["Creature"]:
      side = "Friendly"
    while side == None:
      side = pyautogui.confirm("Will you target an enemy creature or a friendly creature?", buttons=["Enemy", "Friendly"])
    return side
  

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

  
  def chooseHouse(self, varAsStr: str, custom: Tuple[str, List[str]] = ()) -> List[str]:
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
      else:
        self.extraDraws = [(messageBackSurf, messageBackRect), (messageSurf, messageRect)] + [item for sublist in [[(x[0], x[1]), (x[2], x[3])] for x in houses_rects] for item in sublist]
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          if selected and pygame.Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
            self.extraDraws = []
            return [houses[clicked]]
          click = [pygame.Rect.collidepoint(x[1], (self.mousex, self.mousey)) for x in houses_rects]
          if True in click:
            if selected and click.index(True) == clicked:
              for x in houses_rects:
                x[0].fill(COLORS["YELLOW"])
                selected = 0
            else:
              for x in houses_rects:
                x[0].fill(COLORS["YELLOW"])
              clicked = click.index(True)
              selected = clicked + 1
              houses_rects[clicked][0].fill(COLORS["LIGHT_GREEN"])
          elif self.drawFriendDiscard and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            for card in self.activePlayer.discard:
              card.rect.topleft = (-500, -500)
          elif self.drawEnemyDiscard and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            for card in self.inactivePlayer.discard:
              card.rect.topleft = (-500, -500)
          elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
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

    selected = []
    retVal = []
    while True:
      self.extraDraws = [(backgroundSurf, backgroundRect), (messageSurf, messageRect), (confirmBack, confirmBackRect), (confirmSurf, confirmRect), (cancelBack, cancelBackRect), (cancelSurf, cancelRect)] + selected
      for e in pygame.event.get():
        if e.type == pygame.QUIT:
          pygame.quit()
        elif e.type == MOUSEMOTION:
          self.mousex, self.mousey = e.pos
        elif e.type == MOUSEBUTTONUP and e.button == 1:
          if pygame.Rect.collidepoint(confirmBackRect, (self.mousex, self.mousey)):
            self.extraDraws = []
            if retVal and not full:
              if len(retVal) <= count and not full:
                return retVal
              else:
                pyautogui.alert("Not enough targets selected!")
            elif retVal and full and len(retVal) == count:
              return retVal
            elif not full:
              incomplete = None
              while not incomplete:
                incomplete = pyautogui.confirm("Are you sure you want to target less than the full number of targets?", buttons=["Yes", "No"])
              if incomplete == "Yes":
                return retVal
          elif pygame.Rect.collidepoint(cancelBackRect, (self.mousex, self.mousey)):
            retVal = []
            selected = []
            confirmBack.fill(COLORS["GREEN"])
          elif self.drawFriendDiscard and pygame.Rect.collidepoint(self.closeFriendDiscard, (self.mousex, self.mousey)):
            self.drawFriendDiscard = False
            for card in self.activePlayer.discard:
              card.rect.topleft = (-500, -500)
          elif self.drawEnemyDiscard and pygame.Rect.collidepoint(self.closeEnemyDiscard, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = False
            for card in self.inactivePlayer.discard:
              card.rect.topleft = (-500, -500)
          elif not self.drawFriendDiscard and pygame.Rect.collidepoint(self.discard1_rect, (self.mousex, self.mousey)):
            self.drawFriendDiscard = True
          elif not self.drawEnemyDiscard and pygame.Rect.collidepoint(self.discard2_rect, (self.mousex, self.mousey)):
            self.drawEnemyDiscard = True
          # if the list is full, don't let more be added
          if len(retVal) == count:
            break
          # selection
          if targetPool != "Hand":
            if targetPool == "Discard":
              ### start section that needs updating
              if canHit == "both": # this means I can select from both boards at the same time, eg natures call
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
                if True in friend:
                  index = friend.index(True)
                  card = self.activePlayer.discard[index]
                  if condition(card):
                    selected.append((selectedSurf, card.rect))
                    toAdd = ("fr", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
                if True in foe:
                  index = foe.index(True)
                  card = self.inactivePlayer.discard[index]
                  if condition(card):
                    selected.append((selectedSurf, card.rect))
                    toAdd = ("fo", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
              elif canHit == "either": # this means I can select multiples, but only all from same side
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
                if True in friend and (not retVal or retVal[0][0] == "fr"):
                  index = friend.index(True)
                  card = self.activePlayer.discard[index]
                  if condition(card):
                    selected.append((selectedSurf, card.rect))
                    toAdd = ("fr", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
                if True in foe and (not retVal or retVal[0][0] == "fo"):
                  index = foe.index(True)
                  card = self.inactivePlayer.discard[index]
                  if condition(card):
                    selected.append((selectedSurf, card.rect))
                    toAdd = ("fo", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
              elif canHit == "enemy": # this means I can only target unfriendlies
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.discard]
                if True in foe:
                  index = foe.index(True)
                  card = self.inactivePlayer.discard[index]
                  if condition(card):
                    selected.append((selectedSurf, card.rect))
                    toAdd = ("fo", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
              elif canHit == "friend": # this means I can only target friendlies
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.discard]
                if True in friend:
                  index = friend.index(True)
                  card = self.activePlayer.discard[index]
                  if condition(card):
                    selected.append((selectedSurf, card.rect))
                    toAdd = ("fr", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
                  ##### end section that needs updating
            else: # Creature or Artifact
              if canHit == "both": # this means I can select from both boards at the same time, eg natures call
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True not in friend:
                  friend = [pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True in friend:
                  index = friend.index(True)
                  card = active[targetPool][index]
                  if condition(card):
                    if card.ready:
                      selected.append((selectedSurf, card.rect))
                    else:
                      selected.append((selectedSurfTapped, card.tapped_rect))
                    toAdd = ("fr", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in inactive[targetPool]]
                if True in foe:
                  index = foe.index(True)
                  card = inactive[targetPool][index]
                  if condition(card):
                    if card.ready:
                      selected.append((selectedSurf, card.rect))
                    else:
                      selected.append((selectedSurfTapped, card.tapped_rect))
                    toAdd = ("fo", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
              elif canHit == "either": # this means I can select multiples, but only all from same side
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True not in friend:
                  friend = [pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True in friend and (not retVal or retVal[0][0] == "fr"):
                  index = friend.index(True)
                  card = active[targetPool][index]
                  if condition(card):
                    if card.ready:
                      selected.append((selectedSurf, card.rect))
                    else:
                      selected.append((selectedSurfTapped, card.tapped_rect))
                    toAdd = ("fr", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in inactive[targetPool]]
                if True in foe and (not retVal or retVal[0][0] == "fo"):
                  index = foe.index(True)
                  card = inactive[targetPool][index]
                  if condition(card):
                    if card.ready:
                      selected.append((selectedSurf, card.rect))
                    else:
                      selected.append((selectedSurfTapped, card.tapped_rect))
                    toAdd = ("fo", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
              elif canHit == "enemy": # this means I can only target unfriendlies
                foe = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in inactive[targetPool]]
                if True in foe:
                  index = foe.index(True)
                  card = inactive[targetPool][index]
                  if condition(card):
                    if card.ready:
                      selected.append((selectedSurf, card.rect))
                    else:
                      selected.append((selectedSurfTapped, card.tapped_rect))
                    toAdd = ("fo", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
              elif canHit == "friend": # this means I can only target friendlies
                friend = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True not in friend:
                  friend = [pygame.Rect.collidepoint(card.tapped_rect, (self.mousex, self.mousey)) for card in active[targetPool]]
                if True in friend:
                  index = friend.index(True)
                  card = active[targetPool][index]
                  if condition(card):
                    if card.ready:
                      selected.append((selectedSurf, card.rect))
                    else:
                      selected.append((selectedSurfTapped, card.tapped_rect))
                    toAdd = ("fr", index)
                    if toAdd not in retVal:
                      retVal.append(toAdd)
                    print(retVal)
                  else:
                    pyautogui.alert("This target does not meet the conditions.")
                    break
          else:
            if canHit == "enemy":
              hand = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.inactivePlayer.hand]
              if True in hand:
                index = hand.index(True)
                card = self.activePlayer.hand[index]
                if condition(card):
                  selected.append((selectedSurf, card.rect))
                  toAdd = ("fo", index)
                  if toAdd not in retVal:
                    retVal.append(toAdd)
                  print(retVal)
                else:
                  pyautogui.alert("This target does not meet the conditions.")
                  break
            else:
              hand = [pygame.Rect.collidepoint(card.rect, (self.mousex, self.mousey)) for card in self.activePlayer.hand]
              if True in hand:
                index = hand.index(True)
                card = self.activePlayer.hand[index]
                if condition(card):
                  selected.append((selectedSurf, card.rect))
                  toAdd = ("fr", index)
                  if toAdd not in retVal:
                    retVal.append(toAdd)
                  print(retVal)
                else:
                  pyautogui.alert("This target does not meet the conditions.")
                  break
      if not full or (full and len(retVal) == count):
        confirmBack.fill(COLORS["LIGHT_GREEN"])
      self.CLOCK.tick(self.FPS)
      self.hovercard = []
      self.check_hover()
      self.draw(False)
      pygame.display.flip()
      self.extraDraws = []
  
                #####################
                # End of Game Class #
                #####################

def load_image(title, colorkey=None): # this loads keys and house symbols
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
  scaled = pygame.transform.scale(image, (HEIGHT // 21, HEIGHT // 21))
  return scaled, scaled.get_rect()

def developer(game):
  """Developer functions for manually changing the game state.
  """


