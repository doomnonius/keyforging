def basicReap(game, card):
    game.activePlayer.amber += 1
    print("You now have " + str(game.activePlayer.amber) + " amber.")