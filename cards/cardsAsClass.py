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
        self.rarity = self.cardInfo["rarity"]
        self.flavor = self.cardInfo["flavor_text"]
        self.number = self.cardInfo['card_number']
        self.exp = self.cardInfo["expansion"]
        self.maverick = self.cardInfo['is_maverick']
        self.reset()
        

    def reset(self):
        """ Resets a card after it leaves the board.
        """
        self.load_image()
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
            print([x for x in self.traits.split() if len(x) > 2])
        else:
            self.traits = ''
        self.stun = False
        self.amber = self.cardInfo['amber']
        self.revealed = False
        self.destroyed = False
        self.returned = False
        self.captured = 0
        self.upgrade = [] # needs to be on artifacts b/c using for masterplan
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
            self.neigh = []
            self.ready = False
            self.harland = None
            self.damagable = True
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
            if "Poison" in self.text:
                self.poison = True
            else:
                self.poison = False
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
            self.dest = []
            if self.title == "spangler_box":
                self.spangler = []
        

    def __repr__(self):
        """ How to represent a card when called.
        """
        s = '\n' + self.title + '\n' + "Amber: " + str(self.amber) + '\n'
        if self.maverick:
            s += "Maverick" + self.house + ' ' + self.type + '\n'
        else:
            s += self.house + ' ' + self.type + '\n'
        if self.type == "Creature":
            s += "Power: " + str(self.power) + " (" + str(self.damage) + " damage)" + "; Armor: " + str(self.armor + self.extraArm) + '\n'
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
            s += self.title + " (" + self.house + "): (Power: " + str(self.power) + " Armor: " + str(self.armor + self.extraArm) + " Damage: " + str(self.damage) + " Captured: " + str(self.captured) + ')'
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
        """ Num is number of amber to capture. Own is for if the amber is captured from its own side (pretty much a mars exclusive ability)
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
                logging.info("This card wasn't in either board.")
        else:  # else, aka if own == True
            if inactive > num:
                self.captured += num
                game.inactivePlayer.amber -= num
                return
            self.captured += inactive
            game.inactivePlayer.amber = 0
        logging.info(f"{self.title} captured {self.title - initial} amber.")
        if self.title == "yxili_marauder":
            self.power += self.captured - initial

    def damageCalc(self, game, num, poison = False, armor = True):
        """ Calculates damage, considering armor only.
        """
        if "shield_of_justice" in game.activePlayer.states and game.activePlayer.states["shield_of_justice"] and self in game.activePlayer.board["Creature"]:
            logging.info(f"No damage is dealt to {self.title} because of Shield of Justice.")
            return
        if not self.damagable:
            logging.info(f"No damage is dealt to {self.title} because it cannot take damage this turn.")
            return
        if not armor:
            self.damage += num
            logging.info(f"{self.title}'s armor was ignored, and {num} damage was dealt")
        if poison and num > self.armor:
            self.destroyed = True
            logging.info(f"{self.title} destroyed by poison.")
        if num >= self.armor:
            damage = (num - self.armor)
            self.armor = 0
            logging.info(f"{self.title}'s armor was dealt {num} damage. {self.armor} armor remains.")
            shadows = sum(x.title == "shadow_self" for x in self.neighbors(game))
            if not shadows or "Specter" in self.traits:
                self.damage += damage
                logging.info(f"{self.title} was dealt {num} damage, and now has {self.damage} damage.")
            elif shadows == 1:
                self.damage += 0
                for c in self.neighbors(game):
                    if c.title == "shadow_self":
                        c.damage += damage
                        logging.info(f"{c.title} took {self.title}'s {num} damage, and now has {c.damage} damage.")
            elif shadows == 2:
                self.damage += 0
                if self == game.activePlayer:
                    active = game.activePlayer.board["Creature"]
                    choice = active[game.chooseCards("Creature", "Choose which Shadow Self will take the damage:", "friend", condition = lambda x: x in self.neighbors(game))[0][1]]
                else:
                    inactive = game.inactivePlayer.board["Creature"]
                    choice = inactive[game.chooseCards("Creature", "Choose which Shadow Self will take the damage:", "enemy", condition = lambda x: x in self.neighbors(game))[0][1]]
                choice.damageCalc(game, damage)
                logging.info(f"{choice.title} took {self.title}'s {num} damage, and now has {choice.damage} damage.")
        else:
            self.armor -= num
            logging.info(f"{self.title}'s armor was dealt {num} damage. {self.armor} armor remains.")
    
    def fightCard(self, other, game) -> None:
        active = game.activePlayer.board["Creature"]
        inactive = game.inactivePlayer.board["Creature"]
        logging.info(self.title + " is fighting " + other.title + "!")
        self.ready = False
        # add hazardous and assault in here too
        logging.info(f"Hazard: {other.hazard}")
        if other.hazard:
            self.damageCalc(game, other.hazard)
            logging.info("Damage from hazard calced")
            self.updateHealth(game.activePlayer)
        logging.info(f"Assault: {self.assault}")
        if self.assault:
            other.damageCalc(game, self.assault)
            logging.info("Damage from assault calced")
            other.updateHealth(game.inactivePlayer)
        if self.destroyed:
            game.pendingReloc.append(self)
        if other.destroyed:
            game.pendingReloc.append(other)
        logging.info("Before fight effects about to trigger.")
        if self.before:
            for b in self.before:
                logging.info("Trying to run before fight.")
                b(game, self, other)
        else:
            fight.basicBeforeFight(game, self, other)
        logging.info("Up next, evasion sigil.")
        evasion = False
        sigil = sum(x.title == "evasion_sigil" for x in game.activePlayer.board["Artifact"] + game.inactivePlayer.board["Artifact"])
        if sigil:
            for _ in range(sigil):
                if game.activePlayer.deck:
                    game.activePlayer.discard.append(game.activePlayer.deck.pop())
                    if game.activePlayer.discard[-1].house in game.activeHouse:
                        evasion = True
        if self.destroyed or other.destroyed or other not in inactive or self not in active or evasion:
            logging.info(f"Exiting fight early b/c attacker {self.destroyed} or defender {other.destroyed} died during hazard/assault/before fight step, or is otherwise off the board (attacker: {other not in inactive}, defender: {self not in active}), or evasion sigil triggered: {evasion}.")
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
        logging.info("If you're reading this, it's not self.before")
        if self.skirmish or self.temp_skirmish:
            logging.info("The attacker has skirmish, and takes no damage.")
        elif self.title in ["gabos_longarms", "ether_spider", "shadow_self"]:
            logging.info("The defender deals no damage while fighting.")
        elif other.elusive and self.title != "niffle_ape":
            logging.info("The defender has elusive, so no damage is dealt to the attacker.")
        else:
            logging.info("Damage is dealt as normal to attacker.")
            self.damageCalc(game, other.power, poison = other.poison)
        if other.elusive and self.title != "niffle_ape":
            logging.info("The defender has elusive, so no damage is dealt to the defender.")
            other.elusive = False
        elif self.title in ["gabos_longarms", "ether_spider", "shadow_self"]:
            logging.info("The attacker deals no damage while fighting.")
        else:
            damage = self.power
            if self.title == "valdr" and other.isFlank(game):
                damage += 2
            logging.info(f"{damage} damage is dealt as normal to defender.")
            other.damageCalc(game, damage, self.poison)
        logging.info("After fight effects trigger here.")
        logging.info(f"Damage on attacker: {self.damage}")
        logging.info(f"Damage on defender: {other.damage}")
        self.updateHealth(game.activePlayer)
        logging.info("Updated attacker health.")
        basic = False
        if self.destroyed:
            survived = False
            game.pendingReloc.append(self)
        else:
            survived = True
            fight.basicFight(game, self, other)
            basic = True
        logging.info("Fight abilities concluded.")
        other.updateHealth(game.inactivePlayer)
        logging.info("Updated defender health.")
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
        logging.info("Pending and fight abilities completed.")

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
                self.neigh = []
            elif index == 0:
                self.neigh = [active[1]]
            elif index == len(active) - 1:
                self.neigh = [active[index - 1]]
            else:
                self.neigh = [active[index - 1], active[index + 1]]
            return self.neigh
        elif self in inactive:
            index = inactive.index(self)
            if index == 0 and len(inactive) == 1:
                self.neigh = []
            elif index == 0:
                self.neigh = [inactive[1]]
            elif index == len(inactive) - 1:
                self.neigh = [inactive[index - 1]]
            else:
                self.neigh = [inactive[index - 1], inactive[index + 1]]
            return self.neigh
        else: 
            logging.alert(f"{self.title} is not on the board, so it has no neighbors.")

    def isFlank(self, game):
        for player in [game.activePlayer, game.inactivePlayer]:
            if "spectral_tunneler" in player.states and player.states["spectral_tunneler"]:
                if self in player.states["spectral_tunneler"]:
                    return True
        if len(self.neighbors(game)) < 2:
            return True
        return False

    def update(self):
        """ Doesn't do anything yet, but this is for the sprite if I use those
        """
    
    def resetArmor(self, game):
        self.armor = self.base_armor
        if "shoulder_armor" in [x.title for x in self.upgrade] and self.isFlank(game):
            self.armor += 2
        if "grey_monk" in game.activePlayer.board["Creature"]:
            self.armor += sum(x.title == "grey_monk" for x in game.activePlayer.board["Creature"])
        if "bulwark" in [x.title for x in self.neighbors(game)]:
            self.armor += 2
        if "Elusive" in self.text:
            self.elusive = True
        self.temp_skirmish = False

    def calcPower(self, owner, other, game):
        self.power = self.base_power + self.extraPow # extraPow is counters
        if self.title == "staunch_knight" and self.isFlank(game):
            self.power += 2
        elif self.title == "yxili_marauder":
            self.power += self.captured
        elif self.title == "mushroom_man":
            self.power += 3 * (3 - owner.keys)
        if "niffle_queen" in owner.board["Creature"]:
            if "Beast" in self.traits:
                self.power += sum(x.title == "niffle_queen" for x in owner.board["Creature"])
                if self.title == "niffle_queen":
                    self.power -= 1
            if "Niffle" in self.traits:
                self.power += sum(x.title == "niffle_queen" for x in owner.board["Creature"])
                if self.title == "niffle_queen":
                    self.power -= 1
        if "shoulder_armor" in [x.title for x in self.upgrade] and self.isFlank(game):
            self.power += 2
        if "banner_of_battle" in game.activePlayer.board["Artifact"]:
            self.power += 1
        if "blood_of_titans" in [x.title for x in self.upgrade]:
            self.power += 5
        if "flame_wreathed" in [x.title for x in self.upgrade]:
            self.power += 2
        if "round_table" in owner.board["Artifact"] and "Knight" in self.traits:
            self.power += 1
            self.taunt = True
        if self.house == "Brobnar" and "king_of_the_crag" in [x.title for x in other.board["Creature"]]:
            self.power -= 2
        old_neigh = self.neigh.copy()
        if old_neigh != self.neighbors(game):
            if "shoulder_armor" in [x.title for x in self.upgrade] and self.isFlank(game) and len(old_neigh) == 2:
                self.armor += 2
            if "bulwark" in [x.title for x in self.neighbors(game)]:
                self.armor += min(0, 2 * (sum(x.title == "bulwark" for x in self.neigh) - sum(x.title == "bulwark" for x in old_neigh)))

    def updateHealth(self, player = None) -> None:
        if (self.power - self.damage) <= 0:
            logging.info(self.title + " is dead.")
            self.destroyed = True

    def tap(self, image):
        if image.get_width() > image.get_height():
            return
        rotated = pygame.transform.rotate(image, -90)
        return rotated, rotated.get_rect()
        
    def load_image(self, colorkey=None):
        fullname = os.path.join(f'cards\\card-fronts\\{self.exp}', self.title + '.png')
        try:
            image = pygame.image.load(fullname)
        except FileNotFoundError:
            logging.error(f"{fullname} not found.")
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
        self.image, self.rect = self.scale_image(self.width, self.height)
        self.tapped, self.tapped_rect = self.tap(self.image)

    def scale_image(self, width, height):
        scaled = pygame.transform.scale(self.orig_image, (width, height))
        return scaled, scaled.get_rect()
            

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