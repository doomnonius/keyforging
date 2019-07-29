import cards.destroyed as dest
import cards.board as board
import cards.fight as fight
import cards.play as play
import cards.actions as action

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
        self.number = (cardInfo['card_number'])
        self.exp = cardInfo["expansion"]
        self.maverick = cardInfo['is_maverick']
        # conditionals to add?
        # status effects
        if self.type == "Creature":
            if "enters play ready" in self.text:
                self.ready = True
            else:
                self.ready = False
            if "enters play stunned" in self.text:
                self.stun = True
            else:
                self.stun = False
            self.captured = 0
            # check for skirmish in self.text
            if "Skirmish" in self.text:
                self.skirmish = True
            else:
                self.skirmish = False
            # check for elusive in self.text
            if "Elusive" in self.text:
                self.elusive = True
            else:
                self.elusive = False
            # check for taunt in self.text
            if "Taunt" in self.text:
                self.taunt = True
            else:
                self.taunt = False
            if "Reap:" in self.text:
                self.reap = True
            else:
                self.reap = False
            if "Fight:" in self.text:
                self.fight = True
            else:
                self.fight = False
            if "Assault" in self.text:
                self.assault = True
            else:
                self.assault = False
            if "Hazardous" in self.text:
                self.hazard = True
            else:
                self.hazard = False
        # abilities
        if self.type == "Artifact":
            self.captured = False
            self.ready = False
        # these will refer to dictionaries of functions
        # maybe dest.basic will return the right function
        # we're going to need to first create the deck with all these as false, and then go through the deck and change it for each item. It's a bit crazy.
        destList = dir(dest)
        for x in destList:
            if str(x)[0:3] == "key" and str(x)[3:6] == self.number:
                self.destroyed = destList.index(x)
        if "Play:" in self.text:
            self.play = True
        else:
            self.play = False
        if "Action:" in self.text or "Omni:" in self.text:
            self.action = True
        else:
            self.action = False
        

    def __repr__(self):
        """ How to represent a card when called.
        """
        s = self.title + '\n' + "Amber: " + str(self.amber) + '\n'
        if self.maverick:
            s += "Maverick" + self.house + ' ' + self.type + '\n'
        else:
            s += self.house + ' ' + self.type + '\n'
        if self.type == "Creature":
            s += "Power: " + str(self.power) + " (" + str(self.damage) + " damage )" + "; Armor: " + str(self.armor) + '\n'
        if self.traits != None:
            s += self.traits + '\n' + self.text + '\n'
        else:
            s += self.text + '\n'
        if self.flavor != None:
            s += self.flavor + '\n'
        s += str(self.rarity) +  ", " + str(self.exp)
        return s

    def __str__(self):
        s = ''
        if self.type == "Creature":
            s += self.title + " (" + self.house + "): (Power: " + str(self.power) + " Armor: " + str(self.armor) + " Damage: " + str(self.damage) + " Captured: " + str(self.captured) + ')'
        elif self.type == "Artifact":
            if not self.captured:
                s += self.title + " (" + self.house + ")"
            else:
                s += self.title + " (" + self.house + " Amber: " + self.captured + ")"
        elif self.type == "Action":
            s += self.title + " (" + self.house + ")"
        if self.ready:
            s += " Ready"
        else:
            s += " Exhausted"
        if self.type == "Creature":
            if self.stun:
                s += ", Stunned"
        return s

    def __mul__(self, other):
        if self.skirmish:
            self.damage += 0
        else:
            self.damage += (other.power - self.armor)
            self.armor -= other.power
            if self.armor < 0: self.armor = 0
        
        if other.elusive:
            other.damage += 0 #other.power - self.armor
            other.elusive = False
        else:
            other.damage += (self.power - other.armor)
            other.armor -= self.power
            if other.armor < 0: other.armor = 0
        
        return

    def health(self):
        return self.power - self.damage

    def update(self):
        if self.damage >= self.power:
            self.destroyed

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')