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
        if self.type == "Creature":
            print(self.title)
            print("Amber:", self.amber)
            if self.maverick:
                print("Maverick", self.house, self.type)
            else:
                print(self.house, self.type)
            print("Power:", self.power, "(", self.damage, "damage )", "; Armor:", self.armor)
            print(self.traits)
            print(self.text)
            if self.flavor != None:
                print(self.flavor)
            print(self.rarity, ",", self.exp, end='\n\n')
        else:
            print(self.title)
            print("Amber:", self.amber)
            if self.maverick:
                print("Maverick", self.house, self.type)
            else:
                print(self.house, self.type)
            print(self.traits)
            print(self.text)
            if self.flavor != None:
                print(self.flavor)
            print(self.rarity, ",", self.exp, end='\n\n')

    def health(self):
        return self.power - self.damage

    def update(self):
        if self.damage >= self.power:
            self.destroyed

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')