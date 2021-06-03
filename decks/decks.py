import random, os, pygame, requests, json, pyautogui
import cards.cardsAsClass as cards
import cards.destroyed as dest
from constants import WIDTH, HEIGHT

class Deck:
    def __init__(self, name, card_width, card_height, margin):
        with open('decks/deckList.json', encoding='UTF-8') as f:
            data = json.load(f)
            for deck in data:
                if name == deck['name']:
                    self.houses = deck['houses']
                    self.name = deck['name']
                    deckcards = deck['deck']
                    self.deck = []
                    for card in deckcards:
                        self.deck.append(cards.Card(card, self.name, card_width, card_height))
                        # eventually will add edge cases here for errata, i.e. if self.deck[len(self.deck)-1].title == "Bait and Switch"
                    # card creation will give them the appropriate reap  and etc functions
                    random.shuffle(self.deck)
        self.hand = [] #first index is always size of full hand
        self.handSize = 16
        self.chains = 0
        self.discard = []
        self.archive = []
        self.purged = []
        self.board = {"Creature": [], "Artifact": [], "Action": [], "Upgrade": []}
        self.keys = 0
        self.amber = 0
        self.keyCost = 6
        self.yellow = False
        self.blue = False
        self.red = False
        self.states = {card.title:0 for card in self.deck}
        # keys
        self.key_forged_y = self.load_image("yellow_key_front")
        self.key_y = self.load_image("yellow_key_back")
        self.key_forged_r = self.load_image("yellow_key_front")
        self.key_r = self.load_image("yellow_key_back")
        self.key_forged_b = self.load_image("yellow_key_front")
        self.key_b = self.load_image("yellow_key_back")
        # houses
        self.house1 = self.load_image(self.houses[0].lower())
        self.house2 = self.load_image(self.houses[1].lower())
        self.house3 = self.load_image(self.houses[2].lower())
        
    def __repr__(self):
        """ How to represent a deck when called.
        """
        s = ''
        s += self.name
        s += ': \n'
        for x in self.deck:
            s += x.title
            if self.deck.index(x) != 35:
                s += ', '
            else:
                s += '.\n'
        return s

    def drawEOT(self, game):
        """Draws until hand is full. Index 0 of each hand is the number of cards a hand should have.
        """
        draw = self.handSize
        # howling pit
        activeA = [x.title for x in game.activePlayer.board["Artifact"]]
        inactiveA = [x.title for x in game.inactivePlayer.board["Artifact"]]
        activeC = [x.title for x in game.activePlayer.board["Creature"]]
        inactiveC = [x.title for x in game.inactivePlayer.board["Creature"]]
        if "howling_pit" in activeA + inactiveA:
            draw += sum("howling_pit" == x for x in activeA + inactiveA)
        # mother
        if "mother" in activeC:
            draw += sum("mother" == x for x in activeC)
        # succubus
        if "succubus" in inactiveC:
            draw -= sum("succubus" == x for x in inactiveC)
        # etc.
        if self.chains > 0:
            reduced = self.chains // 6
            if self.chains % 6 != 0:
                reduced += 1
            draw -= reduced
            if len(self.hand) <= draw:
                self.chains -= 1
        while (len(self.hand)) < draw:
            if self.deck:
                self.hand.append(self.deck.pop())
            else:
                self.shuffleDiscard()
        self.hand.sort(key = lambda x: x.house, reverse=True)
        # self.deck.sort(key = lambda x: x.house, reverse=True) # why was this even here? testing
    
    def shuffleDiscard(self):
        """ Deals with an empty deck.
        """
        if self.deck == []:
            self.deck = self.discard
            self.discard = []
        else:
            self.deck.extend(self.discard)
            self.discard = []
        random.shuffle(self.deck)

    def gainAmber(self, count, game):
        """ This function will handle the possiblity of ether spider.
        """
        active = game.activePlayer.board["Creature"]
        inactive = game.inactivePlayer.board["Creature"]
        self.amber += count
        if self == game.activePlayer:
            count = sum(x.title == "ether_spider" for x in inactive)
            if count > 1:
                choice = inactive[game.chooseCards("Creature", "Choose which Ether Spider will capture the amber:", "enemy", condition = lambda x: x.title == "ether_spider", con_message = "That's not an ether spider")[0][1]] # choose which one captures
                choice.capture(game, count)
            elif count == 1:
                for c in inactive:
                    if c.title == "ether_spider":
                        c.capture(game, count)
        if self == game.inactivePlayer:
            count = sum(x.title == "ether_spider" for x in active)
            if count > 1:
                choice = active[game.chooseCards("Creature", "Choose which Ether Spider will capture the amber:", "friend", condition = lambda x: x.title == "ether_spider", con_message = "That's not an ether spider")[0][1]] # choose which one captures
                choice.capture(game, count)
            elif count == 1:
                for c in active:
                    if c.title == "ether_spider":
                        c.capture(game, count)
                
        game.setKeys()

    def __iadd__(self, num):
        """ Draws num cards.
        """
        while num > 0:
            if self.deck == []:
                self.shuffleDiscard()
            self.hand.append(self.deck.pop())
            num -= 1
        # self.hand.sort(key = lambda x: x.house)
        return self

    def load_image(self, title): # this loads keys and house symbols
        fullname = os.path.join(f'game_assets', title + '.png')
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            # logging.error(f'Cannot load image: {title}, {message}')
            raise SystemExit(message)
        image = image.convert_alpha()
        scaled = pygame.transform.scale(image, (HEIGHT // 21, HEIGHT // 21))
        return scaled, scaled.get_rect()

url1 = "https://www.keyforgegame.com/api/decks/?page=1&page_size=1&links=cards&search="
url2 = "https://www.keyforgegame.com/deck-details/"

def deckName(listIndex):
    """ Will take a list index, returns the deck name from that index.
    """
    with open('decks/deckList.json', encoding='UTF-8') as f:
        data = json.load(f)
        return data[listIndex]['name']

def sortName(val):
        """Used to sort cards by the 'card_number' key.
        """
        return val['card_number']

def convertToHtml(string):
    """Converts a string to html to be used in a search.
    """
    if string == '' or string == None:
        return ''
    elif string[0] in 'abcdefghijklmnopqrstuvwxyz."-':
        return string[0] + convertToHtml(string[1:])
    elif string[0] == ' ':
        return '%20' + convertToHtml(string[1:])
    elif string[0] == ',':
        return '%2C' + convertToHtml(string[1:])
    elif string[0] == '\'':
        return '%27' + convertToHtml(string[1:])

def importDeck():
    """Imports a deck for the user. How it works: converts the deck name to html, appends that to the url to get the json of a dekc from the keyforge api. This data doesn't have the cards ids I need, so I regex the deck id from the json (and also check the deck is from the right expansion, that there is only one deck, and log which houses are in the deck), then add that to a second url, from which I scrape the html and use regex to find all the card ids and add them to the list.
    """

    newDeck = []
    deckname = pyautogui.prompt("Enter your deck's exact full name: ")
    # why not let them import a bunch of decks at once? because links=cards doesn't work, so I'd need to do another json call. Not willing to implement that yet
    newUrl = url1 + convertToHtml(deckname.lower())
    page = requests.get(newUrl).json()
    # print(newUrl)
    with open('decks/newdeck.json', 'w', encoding='utf-8') as f:
        json.dump(page, f, ensure_ascii=False)
    with open('decks/newdeck.json', encoding='utf-8') as f:
        data = json.load(f)
        if data['data'] == []:
            pyautogui.alert("That input returned no results.")
            return
        deckid = data['data'][0]['id']
        deckName = data['data'][0]['name']
        deckExp = data['data'][0]['expansion']
        if deckExp != 341:
            pyautogui.alert("This version of the game can only handle CotA decks.")
            return
        with open('decks/deckList.json', 'r', encoding='utf-8') as dList:
            allDecks = json.load(dList)
            for deck in allDecks:
                if deck['name'] == deckName:
                    pyautogui.alert("This deck has already been added.")
                    return
        houses = (data['data'][0]['_links']['houses'][0:3])
        # print(len(data['_linked']['cards']))
        cards = data['_linked']['cards']
        cards.sort(key = sortName)
        cardids = data['data'][0]['_links']['cards']
        for card in cards:
            for x in cardids:
                if x == card['id']:
                    newDeck.append(card)
        # print(newDeck, len(newDeck))
        addDeck = {}
        addDeck['houses'] = houses
        addDeck['id'] = deckid
        addDeck['name'] = deckName
        addDeck['deck'] = newDeck
        # Do something to append this data to a json file - the attempt at a solution below is not working
    with open('decks/deckList.json', 'w', encoding='utf-8') as f:
        new = allDecks + [addDeck]
        # print(new[0]['name']) # test line
        new.sort(key=lambda x: x["name"])
        json.dump(new, f, ensure_ascii=False)
    # ^ this works to print a dict with the houses, id, name, and deck (as a list of dicts), and can account for multiple instances of a card

"""When drawing and adding cards, use pop() and append() to work from the end of the list as it is faster
"""