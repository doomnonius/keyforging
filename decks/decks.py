import pyautogui
import cards.cardsAsClass as cards
import random
import cards.destroyed as dest
import requests
import json

class Deck:
    def __init__(self, name, card_width, card_height):
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
        self.handSize = 6
        self.chains = 0
        self.discard = []
        self.archive = []
        self.purged = []
        self.board = {"Creature": [], "Artifact": [], "Action": [], "Upgrade": []}
        self.keys = 0
        self.amber = 0
        self.keyCost = 6
        # whenever a state-creating card is played, it will add its state to this dict (use .update({key:value}) or [key]=value)
        # a couple notes: (1) I don't think I need the subcategories (2) 0 is equivalent to false
        self.states = {card.title:0 for card in self.deck}
        
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

    def drawEOT(self):
        """Draws until hand is full. Index 0 of each hand is the number of cards a hand should have.
        """
        draw = self.handSize
        if self.chains > 0:
            reduced = self.chains // 6
            if self.chains % 6 != 0:
                reduced += 1
            draw -= reduced
            if len(self.hand) >= self.handSize:
                pass
            else:
                self.chains -= 1
        while (len(self.hand)) < draw:
            if self.deck != []:
                self.hand.append(self.deck.pop())
            else:
                self.shuffleDiscard()
        # self.deck.sort(key = lambda x: x.house) # why was this even here?
    
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

    def printShort(self, listt, booly = True):
        """ Prints names and houses of cards in specified list (hand, discard, purge, etc.).
        """
        for x in range (0, len(listt)):
            print(str(x) + ": " + listt[x].title + " (" + listt[x].house + ")")
        if booly:
            full = input("Enter a number to see full details for that card, or press enter to continue: ")
        else:
            full = ''
        while full != '':
            try:
                print(repr(listt[int(full)]))
                print(str(listt[int(full)]))
            except:
                print("Error: input was not a number.")
            if booly:
                full = input("Enter a number to see full details for that card, or press enter to continue: ")
            else:
                full = ''

    def __iadd__(self, num):
        """ Draws num cards.
        """
        while num > 0:
            if self.deck == []:
                self.shuffleDiscard()
            self.hand.append(self.deck.pop())
            num -= 1
        self.hand.sort(key=lambda x: x.house)
        return self

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
    if string == '':
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
    with open('decks/newdeck.json', 'w') as f:
        json.dump(page, f, ensure_ascii=False)
    with open('decks/newdeck.json') as f:
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
        with open('decks/deckList.json', 'r') as dList:
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
    with open('decks/deckList.json', 'w') as f:
        new = allDecks + [addDeck]
        # print(new[0]['name']) # test line
        new.sort(key=lambda x: x["name"])
        json.dump(new, f, ensure_ascii=False)
    # ^ this works to print a dict with the houses, id, name, and deck (as a list of dicts), and can account for multiple instances of a card

"""When drawing and adding cards, use pop() and append() to work from the end of the list as it is faster
"""