import json
import cards
import actions
import creatures
import destroyed
import fight
import play
import reap

def buildDeck(json):
    """Takes json data imported via the keyforge API that I'm ripping off from the internet, then uses it to build a deck (outputting as a list) by searching for a card's ID, then adding the card to the list if it is found.
    """