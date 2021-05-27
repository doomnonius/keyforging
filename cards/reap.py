from helpers import stealAmber

def basicReap(game, card):
    if "dimension_door" in game.activePlayer.states and game.activePlayer.states["dimension_door"]:
        stealAmber(game.activePlayer, game.inactivePlayer, 1)
    else:
        game.activePlayer.gainAmber(1, game)
    # game.log("You now have " + str(game.activePlayer.amber) + " amber.")