import os

import pygame, logging
import cards.destroyed as dest
import cards.fight as fight
import cards.play as play
import cards.actions as action
import cards.reap as reap 

def listOfWords (S):
	""" Builds from the back of the list. Either adds a new item
	to the list, or adds a character to the string at the head
	of the list
	"""
	#base case
	if len(S) == 0:
		return ['']
	else: 
		c = S[0]
		L = listOfWords(S[1:])
		if S[0] == ' ':
			return [''] + L
		else:
			return [c + L[0]] + L[1:]

class Card(pygame.sprite.Sprite):
    """ Feed json.loads(returns a string) called the deck list (which will be a json file) to this to build classes.
        Possibly create a function defined here or elsewhere, if self.name = x, add these functions, if = y, add these.
    """
    def __init__(self, cardInfo, deckName):
        # These are all the things that are not in the dict data but that I need to keep track of
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = self.load_image()
        # screen = pygame.display.get_surface()
        self.deck = deckName
        self.title = cardInfo['card_title'].lower().replace(" ", "_")
        self.damage = 0
        self.power = int(cardInfo['power'])
        self.extraPow = 0
        self.base_armor = int(cardInfo['armor'])
        self.armor = self.base_armor
        self.extraArm = 0
        self.id = cardInfo['id']
        self.house = cardInfo["house"]
        self.type = cardInfo["card_type"]
        self.text = cardInfo["card_text"]
        if cardInfo['traits'] != None:
            self.traits = cardInfo['traits']
        else:
            self.traits = ''
        if len(listOfWords(self.traits)[0]) > 0:
            self.traitList = listOfWords(self.traits)
            # print(self.traitList) # test line
        self.amber = cardInfo['amber']
        self.rarity = cardInfo["rarity"]
        self.flavor = cardInfo["flavor_text"]
        self.number = (cardInfo['card_number'])
        self.exp = cardInfo["expansion"]
        self.maverick = cardInfo['is_maverick']
        # conditionals to add?
        # status effects
        if self.type == "Creature":
            if self.title == "Giant Sloth":
                self.usable = False
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
            if "Taunt" in self.text: self.taunt = True
            else: self.taunt = False
            if "Reap:" in self.text:
                try:
                    self.reap = eval("reap.key" + self.number)
                except:
                    logging.warn("The reap effect wasn't properly applied to " + self.title)
                    self.reap = reap.basicReap
            else: self.reap = reap.basicReap
            if "Fight:" in self.text or "Fight/" in self.text:
                if "Before" in self.text:
                    try: self.before = eval("fight.before" + self.number)
                    except: 
                        logging.warn("The before fight effect wasn't applied properly to " + self.title)
                        self.before = False
                    return
                else:
                    self.before = False
                try: self.fight = eval("fight.key" + self.number)
                except:
                    logging.warn("The fight effect wasn't properly applied to " + self.title)
                    self.fight = False
            else: self.fight = False
            if "Assault" in self.text: self.assault = True, int(self.text[self.text.index("Assault") + 8])
            else: self.assault = False, 0
            if "Hazardous" in self.text: self.hazard = True, int(self.text[self.text.index("Hazardous") + 10])
            else: self.hazard = False, 0
            if "Destroyed:" in self.text:
                try:
                    self.dest = eval("dest.key" + self.number)
                except:
                    logging.warn("The destroyed effect wasn't properly applied to " + self.title)
                    self.dest = dest.basicLeaves
            else: self.dest = dest.basicLeaves
            if "Leaves Play:" in self.text:
                try:
                    self.leaves = eval("dest.lp" + self.number)
                except:
                    logging.warn("The leaves play effect wasn't properly applied to " + self.title)
                    self.leaves = dest.basicLeaves
            else: self.leaves = dest.basicLeaves
        # start of turn effects
        
        # end of turn effects
        
        # abilities
        if self.type == "Artifact":
            self.captured = False
            self.ready = False
        if "Play:" in self.text or "Play/" in self.text:
            try:
                self.play = eval("play.key" + self.number)
            except:
                logging.warn("The on play effect wasn't properly applied to " + self.title)
                self.play = play.passFunc
        else:
            self.play = play.passFunc
        if "Action:" in self.text:
            try:
                self.action = eval("action.key" + self.number)
            except:
                logging.warn("The action effect wasn't properly applied to " + self.title)
                self.action = False
        else:
            self.action = False
        if "Omni:" in self.text:
            try:
                self.omni = eval("action.omni" + self.number)
            except:
                logging.warn("The omni effect wasn't properly applied to " + self.title)
                self.omni = False
        else:
            self.omni = False
        

    def __repr__(self):
        """ How to represent a card when called.
        """
        s = '\n' + self.title + '\n' + "Amber: " + str(self.amber) + '\n'
        if self.maverick:
            s += "Maverick" + self.house + ' ' + self.type + '\n'
        else:
            s += self.house + ' ' + self.type + '\n'
        if self.type == "Creature":
            s += "Power: " + str(self.power + self.extraPow) + " (" + str(self.damage) + " damage)" + "; Armor: " + str(self.armor + self.extraArm) + '\n'
        if self.traits != None:
            s += self.traits + '\n' + self.text + '\n'
        else:
            s += self.text + '\n'
        if self.flavor != None:
            s += self.flavor + '\n'
        s += str(self.rarity) +  ", " + str(self.exp) + '\n'
        return s

    def __str__(self):
        s = ''
        if self.type == "Creature":
            s += self.title + " (" + self.house + "): (Power: " + str(self.power + self.extraPow) + " Armor: " + str(self.armor + self.extraArm) + " Damage: " + str(self.damage) + " Captured: " + str(self.captured) + ')'
            if self.elusive:
                s += " E"
            if self.taunt:
                s += " T"
            if self.hazard[0]:
                s += " H"
            if self.skirmish:
                s += " S"
            if self.assault[0]:
                s += " As"            
            if "Reap:" in self.text:
                s += " R"
            if self.fight:
                s += " F"
            if "Destroyed" in self.text:
                s += " D"
            if "Leaves Play" in self.text: s += " LP"
            if self.ready:
                s += " Ready"
            else:
                s += " Exhausted" 
        elif self.type == "Artifact":
            if not self.captured:
                s += self.title + " (" + self.house + ")"
            else:
                s += self.title + " (" + self.house + " Amber: " + self.captured + ")"
            if self.ready:
                s += " Ready"
            else:
                s += " Exhausted"
        elif self.type == "Action":
            s += self.title + " (" + self.house + ")"
        if self.play:
            s += " P"
        if self.omni:
            s += " O"
        if self.action:
            s += " Ac"
        if self.type == "Creature":
            if self.stun:
                s += ", Stunned"
        return s

    def capture(self, game, num, own = False):
        """ Num is number of amber to capture. Own is for if the amber is captured from its own side (a mars exclusive ability)
        """
        active = game.activePlayer.amber
        inactive = game.inactivePlayer.amber
        if not own:
            if self in game.activePlayer.board["Creature"]:
                if inactive > num:
                    self.captured += num
                    game.inactivePlayer.amber -=  num
                    return
                self.captured += inactive
                game.inactivePlayer.amber = 0
                return
            elif self in game.inactivePlayer.board["Creature"]:
                if active > num:
                    self.captured += num
                    game.activePlayer.amber -= num
                    return
                self.captured += active
                game.activePlayer.amber = 0
                return
            else:
                print("This card wasn't in either board.")
                return
        # else, aka if own == True: (but not needed b/c of earlier return statements)
        if inactive > num:
            self.captured += num
            game.inactivePlayer.amber -= num
            return
        self.captured += inactive
        game.inactivePlayer.amber = 0

    def damageCalc(self, game, num):
        """ Calculates damage, considering armor only.
        """
        if game.activePlayer.states["Fight"]["Shield of Justice"] and self in game.activePlayer.board["Creature"]:
            print("No damage is dealt because of Shield of Justice.")
            return
        self.armor += self.extraArm # this means that extra armor only actually ends being applied when damage actually happens, which will make the reset armor function easier
        # but it means that extraArm will always be applied, even when it shouldn't be
        # I might even only calculate
        if num >= self.armor:
            self.damage += (num - self.armor)
            self.armor = 0
        else:
            self.armor -= num
    
    def fightCard(self, other, game):
        print(self.title + " is fighting " + other.title + "!")
        # add hazardous and assault in here too
        if self.skirmish:
            print("The attacker has skirmish, and takes no damage.") # Test line
            self.damageCalc(game, 0)
        elif other.elusive:
            # print("skir elif") # Test line
            self.damageCalc(game, 0)
        else:
            # print("skir else") # Test line
            self.damageCalc(game, other.power + other.extraPow)
        if other.elusive:
            print("The defender has elusive, so no damage is dealt.")
            other.damageCalc(game, 0) #other.power - self.armor
            other.elusive = False
        else:
            # print("elu else") # test line
            other.damageCalc(game, self.power + self.extraPow)
        self.ready = False
        print(self)
        print(other)

    def health(self):
        return (self.power + self.extraPow) - self.damage

    def neighbors(self, game):
        """ Returns a list of the indexes of a card's neighbors.
        """
        active = game.activePlayer.board["Creature"]
        inactive = game.inactivePlayer.board["Creature"]
        
        if self in active:
            index = active.index(self)
            if index == 0 and len(active) == 1:
                return []
            elif index == 0:
                return [1]
            elif index == len(active) - 1:
                return [index - 1]
            else:
                return [index - 1, index + 1]
        elif self in inactive:
            index = inactive.index(self)
            if index == 0 and len(inactive) == 1:
                return []
            elif index == 0:
                return [1]
            elif index == len(inactive) - 1:
                return [index - 1]
            else:
                return [index - 1, index + 1]
        else: print("This unit is not on the board, so it has no neighbors.")

    
    def reset(self):
        """ Resets a card after it leaves the board.
        """

    def update(self):
        """ Doesn't do anything yet, but this is for the sprite
        """
    
    def updateHealth(self):
        if self.health() <= 0:
            print(self.title + " is dead.")
            return True
        return False

    def load_image(self, colorkey=None):
        fullname = os.path.join(f'card-fronts/{self.exp}', self.title)
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            fullname = os.path.join(f'card-fronts/{self.exp}', 'mighty-javelin')
            image = pygame.image.load(fullname)
            logging.error(f'Cannot load image: {self.title}, {message}')
            # raise SystemExit(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey)
        return image, image.get_rect()
            

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly, which it really shouldn\'t be.')