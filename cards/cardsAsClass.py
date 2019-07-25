import cards.destroyed as dest
import cards.board as board
import cards.fight as fight

class Card():
    """ Feed json.loads(returns a string) called the deck list (which       will be a json file) to this to build classes.
        Possibly create a function defined here or elsewhere, if self.name = x, add these functions, if = y, add these.
    """
    def __init__(self, cardInfo, deckName):
        # These are all the things that are not in the dict data but that I need to keep track of
        self.deck = deckName
        self.title = cardInfo['card_title']
        self.damage = 0
        self.power = cardInfo['power']
        self.base_armor = cardInfo['armor']
        self.armor = self.base_armor
        self.id = cardInfo['id']
        self.house = cardInfo["house"]
        self.type = cardInfo["card_type"]
        self.text = cardInfo["card_text"]
        self.traits = cardInfo['traits']
        self.amber = cardInfo['amber']
        self.rarity = cardInfo["rarity"]
        self.flavor = cardInfo["flavor_text"]
        self.number = int(cardInfo['card_number'])
        self.exp = cardInfo["expansion"]
        self.maverick = cardInfo['is_maverick']
        # conditionals to add?
        # status effects
        self.ready = False
        self.stun = False
        self.captured = 0
        # abilities
        self.destroyed = False
        self.play = False
        self.fight = False
        self.action = False
        self.reap = False
        self.skirmish = False
        self.elusive = False

    def __repr__(self):
        """ How to represent a card when called.
        """
        s = self.title + '\n' + "Amber: " + str(self.amber) + '\n'
        if self.maverick:
            s += "Maverick" + self.house + self.type + '\n'
        else:
            s += self.house + self.type + '\n'
        if self.type == "Creature":
            s += "Power: " + str(self.power) + " (" + str(self.damage) + " damage )" + "; Armor: " + str(self.armor) + '\n'
        if self.traits != None:
            s += self.traits + '\n' + self.text + '\n'
        else:
            s += self.text + '\n'
        if self.flavor != None:
            s += self.flavor + '\n'
        s += str(self.rarity) +  ", " + str(self.exp) + '\n\n'
        return s

    def health(self):
        return self.power - self.damage

    def update(self):
        if self.damage >= self.power:
            self.destroyed

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')