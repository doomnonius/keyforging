import os
from typing import List
import pyautogui

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
        self.cardInfo = cardInfo
        self.deck = deckName
        self.title = cardInfo['card_title'].lower().replace(" ", "_").replace("’", "").replace('“', "").replace(",", "").replace("!", "").replace("”", "").replace("-", "_")
        self.width = width
        self.height = height
        self.reset()
        

    def reset(self):
        """ Resets a card after it leaves the board.
        """
        self.damage = 0
        self.base_power = int(self.cardInfo['power'])
        self.power = self.base_power
        self.extraPow = 0 # will remove this one if I can determine it's not being used
        self.base_armor = int(self.cardInfo['armor'])
        self.armor = self.base_armor
        self.extraArm = 0
        self.id = self.cardInfo['id']
        self.house = self.cardInfo["house"]
        self.type = self.cardInfo["card_type"]
        self.text = self.cardInfo["card_text"]
        if self.cardInfo['traits'] != None:
            self.traits = self.cardInfo['traits']
        else:
            self.traits = ''
        self.amber = self.cardInfo['amber']
        self.rarity = self.cardInfo["rarity"]
        self.flavor = self.cardInfo["flavor_text"]
        self.number = self.cardInfo['card_number']
        self.exp = self.cardInfo["expansion"]
        self.maverick = self.cardInfo['is_maverick']
        self.revealed = False
        self.destroyed = False
        self.returned = False
        self.captured = 0
        self.upgrade = [] # needs to be on artifacts b/c using for masterplan
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
            self.action = [eval(f"action.{self.title}")]
        else:
            self.action = []
        # omni abilitiestry:
        if f"omni_{self.title}" in dir(action):
            self.omni = eval("action.omni" + self.number)
        else:
            self.omni = False
        if self.type == "Upgrade":
            # self.attached = None
            self.play = play.passFunc
        # else:
        #     self.attached = False
        # creature only abilities
        if self.type == "Creature":
            self.safe = False
            self.greking = False
            self.stealer = False
            self.taunt = False
            self.ward = False
            self.enrage = False
            self.upgrade = []
            self.ready = False
            self.stun = False
            self.harland = None
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
                self.reap = [eval(f"reap.{self.title}")]
            else:
                self.reap = []
            # check for before fight abilities
            if f"before_{self.title}" in dir(fight):
                self.before = [eval(f"fight.before_{self.title}")]
            else:
                self.before = []
            # check for after fight abilities
            if self.title in dir(fight):
                self.fight = [eval(f"fight.{self.title}")]
            else:
                self.fight = []
            # check for destroyed abilities
            if self.title in dir(dest):
                self.dest = [eval(f"dest.{self.title}")]
            else:
                self.dest = []
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
            if f"lp_{self.title}" in dir(dest):
                self.leaves = eval(f"dest.lp_{self.title}")
            else:
                self.leaves = []
        # start of turn effects
        if f"eot_{self.title}" in dir(turnEffects):
            self.eot = eval(f"turnEffects.eot_{self.title}")
        else:
            self.eot = turnEffects.basic_eot
        # end of turn effects
        if f"sot_{self.title}" in dir(turnEffects):
            self.sot = eval(f"turnEffects.sot_{self.title}")
        else:
            self.sot = False
        # artifacts need to be able to be readied too, and can capture amber
        if self.type == "Artifact":
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
            if self.hazard:
                s += f" H: {self.hazard}"
            if self.skirmish:
                s += " S"
            if self.assault:
                s += f" As: {self.assault}"            
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
        initial = self.captured
        if not own:
            if self in game.activePlayer.board["Creature"]:
                if inactive > num:
                    self.captured += num
                    game.inactivePlayer.amber -=  num
                else:
                    self.captured += inactive
                    game.inactivePlayer.amber = 0
            elif self in game.inactivePlayer.board["Creature"]:
                if active > num:
                    self.captured += num
                    game.activePlayer.amber -= num
                else:
                    self.captured += active
                    game.activePlayer.amber = 0
            else:
                pyautogui.alert("This card wasn't in either board.")
        # else, aka if own == True: (but not needed b/c of earlier return statements)
        else:
            if inactive > num:
                self.captured += num
                game.inactivePlayer.amber -= num
                return
            self.captured += inactive
            game.inactivePlayer.amber = 0
        if self.title == "yxili_marauder":
            self.power += self.captured - initial

    def damageCalc(self, game, num, poison = False, armor = True):
        """ Calculates damage, considering armor only.
        """
        if "shield_of_justice" in game.activePlayer.states and game.activePlayer.states["shield_of_justice"] and self in game.activePlayer.board["Creature"]:
            pyautogui.alert(f"No damage is dealt to {self.title} because of Shield of Justice.")
            return
        if armor == False:
            self.damage += num
        if poison and num > self.armor:
            self.destroyed = True
        if num >= self.armor:
            damage = (num - self.armor)
            self.armor = 0
            shadows = sum(x.title == "shadow_self" for x in self.neighbors(game))
            if not shadows or "Specter" in self.traits:
                self.damage += damage
            elif shadows == 1:
                self.damage += 0
                for c in self.neighbors(game):
                    if c.title == "shadow_self":
                        c.damage += damage
            elif shadows == 2:
                self.damage += 0
                if self == game.activePlayer:
                    active = game.activePlayer.board["Creature"]
                    choice = active[game.chooseCards("Creature", "Choose which Shadow Self will take the damage:", "friend", condition = lambda x: x in self.neighbors(game))[0][1]]
                else:
                    inactive = game.inactivePlayer.board["Creature"]
                    choice = inactive[game.chooseCards("Creature", "Choose which Shadow Self will take the damage:", "enemy", condition = lambda x: x in self.neighbors(game))[0][1]]
                choice.damageCalc(game, damage)
        else:
            self.armor -= num
    
    def fightCard(self, other, game) -> None:
        active = game.activePlayer.board["Creature"]
        inactive = game.activePlayer.board["Creature"]
        print(self.title + " is fighting " + other.title + "!")
        self.ready = False
        # add hazardous and assault in here too
        print(f"Hazard: {other.hazard}")
        if other.hazard:
            self.damageCalc(game, other.hazard)
            print("Damage from hazard calced")
            self.updateHealth(game.activePlayer)
        print(f"Assault: {self.assault}")
        if self.assault:
            other.damageCalc(game, self.assault)
            print("Damage from assault calced")
            other.updateHealth(game.inactivePlayer)
        if self.destroyed:
            game.pendingReloc.append(self)
        if other.destroyed:
            game.pendingReloc.append(other)
        print("Before fight effects would go here too.")
        if self.before:
            for b in self.before:
                b(game, self, other)
        else:
            fight.basicBeforeFight(game, self, other)
        evasion = False
        sigil = sum(x.title == "evasion_sigil" for x in game.activePlayer.board["Creature"] + game.activePlayer.board["Creature"])
        if sigil:
            for _ in range(sigil):
                if game.activePlayer.deck:
                    game.activePlayer.discard.append(game.activePlayer.deck.pop())
                    if game.activePlayer.discard[-1].house != self.house:
                        evasion = True
        if self.destroyed or other.destroyed or other not in inactive or self not in active or evasion:
            print(f"Exiting fight early b/c attacker or defender died during hazard/assault/before fight step, or evasion sigil triggered: {evasion}.")
            game.pending()
            basic = False
            if self.destroyed:
                survived = False
                game.pendingReloc.append(self)
            else:
                survived = True
                fight.basicFight(game, self, other)
                basic = True
            if not basic:
                fight.basicFight(game, self, other)
            if survived:
                for f in self.fight:
                    f(game, self, other)
            return
        print("If you're reading this, it's not self.before")
        if self.skirmish or self.temp_skirmish:
            print("The attacker has skirmish, and takes no damage.") # Test line
        elif self.title in ["gabos_longarms", "ether_spider", "shadow_self"]:
            print("The defender deals no damage while fighting.")
        elif other.elusive and self.title != "niffle_ape":
            print("The defender has elusive, so no damage is dealt to the attacker.") # Test line
        else:
            print("Damage is dealt as normal to attacker.")
            self.damageCalc(game, other.power, poison = other.poison)
        if other.elusive and self.title != "niffle_ape":
            print("The defender has elusive, so no damage is dealt to the defender.")
            other.elusive = False
        elif self.title in ["gabos_longarms", "ether_spider", "shadow_self"]:
            print("The attacker deals no damage while fighting.")
        else:
            damage = self.power + self.extraPow
            if self.title == "valdr" and other.isFlank(game):
                damage += 2
            print(f"{damage} damage is dealt as normal to defender.")
            other.damageCalc(game, damage, self.poison)
        print("After fight effects would go here, if attacker survives.")
        print(f"Damage on attacker: {self.damage}")
        print(f"Damage on defender: {other.damage}")
        self.updateHealth(game.activePlayer)
        print("Updated attacker health.")
        basic = False
        if self.destroyed:
            survived = False
            game.pendingReloc.append(self)
        else:
            survived = True
            fight.basicFight(game, self, other)
            basic = True
        print("I know it isn't self.fight that's failing.")
        other.updateHealth(game.inactivePlayer)
        print("Updated defender health.")
        if other.destroyed:
            game.pendingReloc.append(other)
        elif not basic:
            fight.basicFight(game, self, other)
            basic = True
        if not basic:
            fight.basicFight(game, self, other)
        game.pending()
        if survived:
            for f in self.fight:
                f(game, self, other)
        print("Another comment after pending has completed.")

    # def health(self) -> int:
    #     return (self.power + self.extraPow) - self.damage

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
                return [active[1]]
            elif index == len(active) - 1:
                return [active[index - 1]]
            else:
                return [active[index - 1], active[index + 1]]
        elif self in inactive:
            index = inactive.index(self)
            if index == 0 and len(inactive) == 1:
                return []
            elif index == 0:
                return [inactive[1]]
            elif index == len(inactive) - 1:
                return [inactive[index - 1]]
            else:
                return [inactive[index - 1], inactive[index + 1]]
        else: 
            pyautogui.alert("This unit is not on the board, so it has no neighbors.")

    def isFlank(self, game):
        if len(self.neighbors(game)) < 2:
            return True
        return False


    def update(self):
        """ Doesn't do anything yet, but this is for the sprite if I use those
        """
    
    def resetArmor(self, game):
        self.armor = self.base_armor + self.extraArm
        if "Elusive" in self.text:
            self.elusive = True
        self.temp_skirmish = False
        # I can change Gray Monk to match this by giving it a play effect and a leaves play effect.

    def updateHealth(self, player = None) -> None:
        if (self.power + self.extraPow - self.damage) <= 0:
            print(self.title + " is dead.")
            self.destroyed = True
            # if "armageddon_cloak" not in [x.title for x in self.upgrade]:
            #     print("Did we at least get here?")
            #     player.board["Creature"].remove(self)
        #     return True
        # return False

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
        except FileNotFoundError:
            print(fullname)
        except pygame.error as message:
            fullname = os.path.join(f'cards\\card-fronts\\{self.exp}', 'mighty_javelin.png')
            image = pygame.image.load(fullname)
            logging.error(f'Cannot load image: {self.title}, {message}')
            raise SystemExit(message)
        image = image.convert_alpha()
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
            

class Invisicard():
    """ Used for reorganizing the hand.
    """
    def __init__(self, width,  height):
        self.image = pygame.Surface((width, height))
        self.image.convert_alpha()
        self.image.set_alpha(0)
        self.rect = self.image.get_rect()
        self.tapped_rect = self.image.get_rect()
        self.type = False


if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly, which it really shouldn\'t be.')