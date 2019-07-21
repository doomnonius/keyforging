import cards.cardsAsClass as cards
from cards.cardsAsList import listt
import random
import requests
import json
import re
from decks.deckList import deckDict

class Deck:
    # idea: use composition, these five classes will go under the deck class. Not sure if this makes more sense then having them all as an individual list.
    def __init__(self):
        with open('decks/newdeck.json') as f:
            data = json.load(f)
            self.houses = data['data'][0]['_links']['houses']
            self.name = data['data'][0]['name']
            deckcards = data['_linked']['cards']
            deckcards.sort(key = sortName)
            cardids = data['data'][0]['_links']['cards']
            self.deck = []
            for card in deckcards:
                for x in cardids:
                    if x == card['id']:
                        self.deck.append(cards.Card(card, self.name))
    
    def __repr__(self):
        """ How to represent a deck when called.
        """
        for x in self.deck:
            print(x.title + ', ', end='')
        print('')

# class Discard:

# class Draw:

# class Archive:

# class Hand:

# class Purged:

# class Deck:

url1 = "https://www.keyforgegame.com/api/decks/?page=1&page_size=1&links=cards&search="
url2 = "https://www.keyforgegame.com/deck-details/"

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
    deckname = input("Enter your deck's exact full name: ")
    # why not let them import a bunch of decks at once? because links=cards doesn't work, so I'd need to do another json call. Not willing to implement that yet
    newUrl = url1 + convertToHtml(deckname.lower())
    page = requests.get(newUrl).json()
    # print(newUrl)
    with open('decks/newdeck.json', 'w') as f:
        json.dump(page, f, ensure_ascii=False)
    with open('decks/newdeck.json') as f:
        data = json.load(f)
        if data['data'] == []:
            print("That input returned no results.")
            return
        deckid = data['data'][0]['id']
        deckName = data['data'][0]['name']
        deckExp = data['data'][0]['expansion']
        if deckExp != 341:
            print("This version of the game can only handle CotA decks.")
            return
        with open('decks/deckList.json', 'r') as f:
            data2 = json.load(f)
            for x in data2:
                if x['name'] == deckName:
                    print("This deck has already been added.")
                    return
            original = data2[0:]
            print(original)
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
    with open('decks/deckList.json', 'a') as f:
        new = original + addDeck
        json.dump(new, f, ensure_ascii=False)


    # ^ this works to print a dict with the houses, id, name, and deck (as a list of dicts), and can account for multiple instances of a card

"""When drawing and adding cards, use pop() and append() to work from the end of the list as it is faster
"""
MyDeck = []
OppDeck = []
MyHand = [6]
OppHand = [6]

def buildDeck(L, L2 = [], n = 1):
    """Takes a list of card numbers and builds a deck to L2. What this should do (and doesn't at this point), is to create a whole bunch of variables that are tied to instantiations of the appropriate classes.
    """
    # print("Calling build deck: " + str(n))
    # def search(n, L):
    #     """A helper function that finds the card in cardsAsList that has card.number == n.
    #     """
    #     # print("Calling search: " + str(n))
    #     if L[0].number == n:
    #         return L[0]
    #     else:
    #         return search(n, L[1:])
    # # optimization: split cards into houses
    # # base case: empty list
    # if len(L) == 3:
    #     print(len(L2))
    #     return L2
    # elif L[0] == "Brobnar":
    #     if len(L) == 27:
    #         L[0] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, brobnar)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[0] == "Dis":
    #     if len(L) == 27:
    #         L[0] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, dis)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[0] == "Logos":
    #     if len(L) == 27:
    #         L[0] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, logos)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[0] == "Mars":
    #     if len(L) == 27:
    #         L[0] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, mars)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[0] == "Sanctum":
    #     if len(L) == 27:
    #         L[0] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, sanctum)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[1] == "Dis":
    #     if len(L) == 15:
    #         L[1] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, dis)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[1] == "Logos":
    #     if len(L) == 15:
    #         L[1] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, logos)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[1] == "Mars":
    #     if len(L) == 15:
    #         L[1] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, mars)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[1] == "Sanctum":
    #     if len(L) == 15:
    #         L[1] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, sanctum)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[1] == "Shadows":
    #     if len(L) == 15:
    #         L[1] = "done"
    #         buildDeck(L, L2, n)
    #     elif L[3] == n:
    #         L2.append(card.listdetails(search(n, shadows)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[2] == "Logos":
    #     if L[3] == n:
    #         L2.append(card.listdetails(search(n, logos)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[2] == "Mars":
    #     if L[3] == n:
    #         L2.append(card.listdetails(search(n, mars)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[2] == "Sanctum":
    #     if L[3] == n:
    #         L2.append(card.listdetails(search(n, sanctum)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[2] == "Shadows":
    #     if L[3] == n:
    #         L2.append(card.listdetails(search(n, shadows)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # elif L[2] == "Untamed":
    #     if L[3] == n:
    #         L2.append(card.listdetails(search(n, untamed)))
    #         buildDeck(L[0:3] + L[4:], L2, n)
    #     else:
    #         buildDeck(L, L2, n + 1)
    # else:
    #     buildDeck(L, L2, n + 1)

def nameList(L):
    """Takes the listdetails() function output and returns only card names.
    """
    # Since L[0] of MyHand is an int and not another list, we need to ignore the first item of those lists.
    if L == []:
        return
    elif type(L[0]) == int:
        L = L[1:]
    # The first three indexes of MyDeck will be the houses.
    while type(L[0]) == str:
        L = L[1:]
    return [x[0] for x in L]

def drawEOT(hand, n = 0):
    """Draws until hand is full. Index 0 of each hand is the number of cards a hand should have. Also does all other end of turn actions.
    """
    while (len(hand) - 1) < hand[0]:
        x = MyDeck.pop()
        print(x)
        hand.append(x)
     #Going to need to add end of turn stuff

