__package__ = 'cards'

from cards.board import MyBoard, OppBoard

def fighting(attacker, target = False):
    """This fight function is called by a different fight function which gets user input to determine the target.
    """
    print("Your opponent's creatures are: " + str(OppBoard))
    target = input()
    target.damage = attacker.power
    attacker.damage = target.power
    attacker.update()
    target.update()
    #checking for death is within the class of each creature itself, but we call it after the fight

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')