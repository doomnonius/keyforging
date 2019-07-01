import actions
import destroyed
import play
import reap
import cardsAsClass
import creatures
import board

def fight(attacker, target = False):
    """This fight function is called by a different fight function which gets user input to determine the target.
    """
    print("Your opponent's creatures are: " + str(board.OppBoard))
    target = input()
    target.damage = attacker.power
    attacker.damage = target.power
    attacker.update()
    target.update()
    #checking for death is within the class of each creature itself, but we call it after the fight