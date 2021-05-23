def fighting(attacker, target = False):
    """This fight function is called by a different fight function which gets user input to determine the target.
    """
    target = input()
    target.damage = attacker.power
    attacker.damage = target.power
    attacker.update()
    target.update()
    #checking for death is within the class of each creature itself, but we call it after the fight

def basicFight():
    """This checks for things that create before fight effects, if there are any.
    """

def basicBeforeFight(game, card):
    """ This checks for things that create before fight effects, like take hostages
        It will be called by all before fight effects, or 
    """
    if "warsong" in game.activePlayer.states:
      game.activePlayer.amber += game.activePlayer.states["warsong"]
    if "take_hostages" in game.activePlayer.states:
      card.capture(game, game.activePlayer.states["take_hostages"])

if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')