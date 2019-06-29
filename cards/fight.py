import actions
import destroyed
import play
import reap
import cards
import creatures

def fight(attacker, target):
    """This fight function is called by a different fight function which gets user input to determine the target.
    """
    target.damage = attacker.power
    attacker.damage = target.power
    #checking for death is within the class of each creature itself