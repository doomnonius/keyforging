import os
from typing import List

import pygame, logging
import cards.destroyed as dest
import cards.fight as fight
import cards.play as play
import cards.actions as action
import cards.reap as reap 
import cards.turnEffects as turnEffects

class Card(pygame.sprite.Sprite):
    """ Feed json.loads(returns a string) called the deck list (which will be a json file) to this to build classes.
        Possibly create a function defined here or elsewhere, if self.name = x, add these functions, if = y, add these.
    """
    def __init__(self, cardInfo, deckName, width, height):
        # These are all the things that are not in the dict data but that I need to keep track of
        pygame.sprite.Sprite.__init__(self)
        # screen = pygame.display.get_surface()
        self.deck = deckName
        self.title = cardInfo['card_title'].lower().replace(" ", "_").replace("'", "").replace('"', "").replace(",", "").replace("!", "")
        self.width = width
        self.height = height
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
        self.amber = cardInfo['amber']
        self.rarity = cardInfo["rarity"]
        self.flavor = cardInfo["flavor_text"]
        self.number = cardInfo['card_number']
        self.exp = cardInfo["expansion"]
        self.maverick = cardInfo['is_maverick']
        self.load_image()
        # conditionals to add?
        # status effects
        
        # play abilities
        if self.title in dir(play):
            self.play = eval(f"play.{self.title}")
        else:
            self.play = play.passFunc
        # action abilities
        if self.title in dir(action):
            self.action = eval(f"action.{self.title}")
        else:
            self.action = False
        # omni abilitiestry:
        if f"omni_{self.title}" in dir(action):
            self.omni = eval("action.omni" + self.number)
        else:
            self.omni = False
        if self.type == "Upgrade":
            self.attached = None
        else:
            self.attached = False
        # creature only abilities
        if self.type == "Creature":
            self.upgrade = []
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
            self.temp_skirmish = False
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
            # check for reaping abilities
            if self.title in dir(reap):
                self.reap = eval(f"reap.{self.title}")
            else:
                self.reap = reap.basicReap
            # check for before fight abilities
            if f"before_{self.title}" in dir(fight):
                self.before = eval(f"fight.before_{self.title}")
            else:
                self.before = fight.basicBeforeFight
            # check for after fight abilities
            if self.title in dir(fight):
                self.fight = eval(f"fight.{self.title}")
            else:
                self.fight = fight.basicFight
            # check for assault
            if "Assault" in self.text:
                self.assault = int(self.text[self.text.index("Assault") + 8])
            else:
                self.assault = 0
            # check for hazardous
            if "Hazardous" in self.text:
                self.hazard = int(self.text[self.text.index("Hazardous") + 10])
            else:
                self.hazard = 0
            # check for destroyed abilities
            if self.title in dir(dest):
                eval(f"dest.{self.title}")
            else:
                self.dest = dest.basicDest
            if f"lp_{self.title}" in dir(dest):
                self.leaves = eval(f"dest.lp_{self.title}")
            else:
                self.leaves = dest.basicLeaves
        # start of turn effects
        if f"eot_{self.title}" in dir(turnEffects):
            self.eot = eval(f"turnEffects.eot_{self.title}")
        else:
            self.eot = False
        # end of turn effects
        if f"sot_{self.title}" in dir(turnEffects):
            self.sot = eval(f"turnEffects.sot_{self.title}")
        else:
            self.sot = False
        # artifacts need to be able to be readied too, and can capture amber
        if self.type == "Artifact":
            self.captured = False
            self.ready = False
        

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
        if "shield_of_justice" in game.activePlayer.states and game.activePlayer.states["shield_of_justice"] and self in game.activePlayer.board["Creature"]:
            print("No damage is dealt because of Shield of Justice.")
            return
        if num >= self.armor:
            self.damage += (num - self.armor)
            self.armor = 0
        else:
            self.armor -= num
    
    def fightCard(self, other, game) -> None:
        print(self.title + " is fighting " + other.title + "!")
        # add hazardous and assault in here too
        print("Hazardous and assault currently ignored.")
        print("Before fight effects would go here too.")
        self.before(game, self)
        if self.skirmish or self.temp_skirmish:
            print("The attacker has skirmish, and takes no damage.") # Test line
            self.damageCalc(game, 0)
        elif other.elusive:
            print("The defender has elusive, so no damage is dealt to the attacker.") # Test line
            self.damageCalc(game, 0)
        else:
            print("Damage is dealt as normal to attacker.")
            self.damageCalc(game, other.power + other.extraPow)
        if other.elusive:
            print("The defender has elusive, so no damage is dealt to the defender.")
            other.damageCalc(game, 0) #other.power - self.armor
            other.elusive = False
        else:
            print("Damage is dealt as normal to defender.")
            other.damageCalc(game, self.power + self.extraPow)
        self.ready = False
        print("After fight effects would go here, if attacker survives.")
        if self.updateHealth():
            game.pendingReloc.append(game.activePlayer.board["Creature"].pop(self))
        else:
            self.fight(game, self)
        if other.updateHealth():
            game.pendingReloc.append(game.inactivePlayer.board["Creature"].pop(other))
        self.pending()
        print(other.damage)
        print(self.damage)

    def health(self) -> int:
        return (self.power + self.extraPow) - self.damage

    def neighbors(self, game) -> List[int]:
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

    def isFlank(self):
        if len(self.neighbors) < 2:
            return True
        return False

    def reset(self):
        """ Resets a card after it leaves the board.
        """

    def update(self):
        """ Doesn't do anything yet, but this is for the sprite if I use those
        """
    
    def resetArmor(self):
        self.armor = self.base_armor + self.extraArm
        if "Elusive" in self.text:
            self.elusive = True
        # I can change Gray Monk to match this by giving it a play effect and a leaves play effect.

    def updateHealth(self) -> bool:
        if self.health() <= 0:
            print(self.title + " is dead.")
            return True
        return False

    def tap(self):
        if self.image.get_width() > self.image.get_height():
            return
        rotated = pygame.transform.rotate(self.image, -90)
        return rotated, rotated.get_rect()

    def untap(self):
        if self.image.get_height() > self.image.get_width():
            return
        rotated = pygame.transform.rotate(self.image, 90)
        self.image, self.rect = rotated, rotated.get_rect()
        
    def load_image(self, colorkey=None):
        fullname = os.path.join(f'cards\\card-fronts\\{self.exp}', self.title + '.png')
        try:
            image = pygame.image.load(fullname)
        except pygame.error as message:
            fullname = os.path.join(f'cards\\card-fronts\\{self.exp}', 'mighty_javelin.png')
            image = pygame.image.load(fullname)
            logging.error(f'Cannot load image: {self.title}, {message}')
            raise SystemExit(message)
        image = image.convert()
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey)
        self.orig_image, self.orig_rect = image, image.get_rect()
        self.image, self.rect = self.scaled_image(self.width, self.height)
        self.tapped, self.tapped_rect = self.tap()

    def scaled_image(self, width, height):
        scaled = pygame.transform.scale(self.orig_image, (width, height))
        self.image, self.rect = scaled, scaled.get_rect()
        return self.image, self.rect
            

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly, which it really shouldn\'t be.')