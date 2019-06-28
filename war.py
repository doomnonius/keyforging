# A test case for building up to a Keyforge prototype,
# testing random.shuffle(X) to shuffle decks and play war.
# I am playing with a more complicated ruleset of war than just the base version.
# Glitch found! There's something wrong with how I'm handling holdings!
# Fixed that glitch! Now I've got a glitch in how I'm handling a deck with less than 5 cards.
    # It's because I haven't handled the edge case of a player's last card causing a war!
# Next glitch! If a player's deck is empty, it just loops trying to shuffle their deck instead of declaring a winner!
    # I believe the problem was in shuffle(), with an if statement that checked if discard == 0 instead of len(discard)
# Now it ended, but only after losing 16 cards, which means I have a different problem with holding, I think only if you get a double war into a a double war.
    # Confirmed with a special built test case.
    # Now I realized it's not a glitch, it's just because my test statements tracking number of cards don't account for the cards in holding.
# Also it turns out return doesn't return strings, fixed game winning statements.

import random

deck = [[15, 'A of Spades'], [14, 'K of Spades'], [13, 'Q of Spades'], [12, 'J of Spades'], [11, '10 of Spades'], [10, '9 of Spades'], [9, '8 of Spades'], [8, '7 of Spades'], [7, '6 of Spades'], [6, '5 of Spades'], [5, '4 of Spades'], [4, '3 of Spades'], [3, '2 of Spades'], \
    [15, 'A of Diamonds'], [14, 'K of Diamonds'], [13, 'Q of Diamonds'], [12, 'J of Diamonds'], [11, '10 of Diamonds'], [10, '9 of Diamonds'], [9, '8 of Diamonds'], [8, '7 of Diamonds'], [7, '6 of Diamonds'], [6, '5 of Diamonds'], [5, '4 of Diamonds'], [4, '3 of Diamonds'], [3, '2 of Diamonds'], \
    [15, 'A of Clubs'], [14, 'K of Clubs'], [13, 'Q of Clubs'], [12, 'J of Clubs'], [11, '10 of Clubs'], [10, '9 of Clubs'], [9, '8 of Clubs'], [8, '7 of Clubs'], [7, '6 of Clubs'], [6, '5 of Clubs'], [5, '4 of Clubs'], [4, '3 of Clubs'], [3, '2 of Clubs'], \
    [15, 'A of Hearts'], [14, 'K of Hearts'], [13, 'Q of Hearts'], [12, 'J of Hearts'], [11, '10 of Hearts'], [10, '9 of Hearts'], [9, '8 of Hearts'], [8, '7 of Hearts'], [7, '6 of Hearts'], [6, '5 of Hearts'], [5, '4 of Hearts'], [4, '3 of Hearts'], [3, '2 of Hearts']]

# print (len(deck))

def shuffle(discard):
    '''Shuffles discard piles, and if a discard pile is empty, declares a winner.'''
    if len(discard) == 0:
        return True
    else:
        print("Shuffling!")
        print('')
        random.shuffle(discard)
        return discard

def empty(deckA, deckB, discardA, discardB):
    '''Handles an empty deck then calls flip() or declares a winner'''
    if len(deckA) == 0:
        print('Player A\'s deck is empty. Shuffling!')
        print('')
        # print("Discard A contains ", len(discardA), " cards.")
        # print("Discard B contains ", len(discardB), " cards.")
        # print("Total cards: ", (len(discardA) + len(discardB)))
        if shuffle(discardA) == True:
            print('Player A has no cards to shuffle.')
            print('')
            print('Player B wins the game!')
            return
        else:
            deckA.extend(shuffle(discardA))
            discardA = []
            # print('Called from empty deck A: Discard B (', len(discardB), ') + Discard A (', len(discardA), ') + Deck A (', len(deckA), ') + Deck B (', len(deckB), ') = ', (len(discardB) + len(deckA) + len(deckB)))
            flip(deckA, deckB, discardA, discardB)
    elif len(deckB) == 0:
        print('Player B\'s deck is empty. Shuffling!')
        print('')
        # print("Discard A contains ", len(discardA), " cards.")
        # print("Discard B contains ", len(discardB), " cards.")
        # print("Total cards (first time only): ", (len(deckA) + len(discardB)))
        if shuffle(discardB) == True:
            print('Player B has no cards to shuffle.')
            print('')
            print('Player A wins the game!')
            return
        else:
            deckB.extend(shuffle(discardB))
            discardB = []
            # print('Called from empty deck B: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', len(deckA), ') + Deck B (', len(deckB), ') = ', (len(discardA) + len(deckA) + len(deckB)))
            flip(deckA, deckB, discardA, discardB)
    else:
        if len(deckA) < 5:
            deckA.extend(shuffle(discardA))
            discardA = []
            # print('Called from <5 Deck A: Discard B (', len(discardB), ') + Discard A (', len(discardA), ') + Deck A (', len(deckA), ') + Deck B (', len(deckB), ') = ', (len(discardB) + len(discardA) + len(deckA) + len(deckB)))
            flip(deckA, deckB, discardA, discardB)
        elif len(deckB) < 5:
            deckB.extend(shuffle(discardB))
            discardB = []
            # print('Called from <5 Deck B: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', len(deckA), ') + Deck B (', len(deckB), ') = ', (len(discardA) + len(discardB) + len(deckA) + len(deckB)))
            flip(deckA, deckB, discardA, discardB)

def tie(deckA, deckB, discardA, discardB, holding = []):
    '''Handles ties, then passes back off to flip(), or to itself'''
    print('')
    print("War!")
    print('')
    # print('Called from War: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', len(deckA), ') + Deck B (', len(deckB), ') = ', (len(discardA) + len(discardB) + len(deckA) + len(deckB)))
    #base case empty deck, leading to shuffle()
    if len(deckA) == 0 or len(deckB) == 0:
        # print("Base case")
        empty(deckA, deckB, discardA, discardB)
    #if the deck has less than 5 cards and discard contains something, call empty()
    elif (len(deckA) < 5 and len(discardA) > 0) or (len(deckB) < 5 and len(discardB) > 0):
        # print("Less than 5 but discard not empty.")
        # print('Called from tie() before sending to <5 shuffle(): Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', len(deckA), ') + Deck B (', len(deckB), ') = ', (len(discardA) + len(discardB) + len(deckA) + len(deckB)))
        empty(deckA, deckB, discardA, discardB)
    #now if deck has less than 5 cards discard will be empty
    elif len(deckA) < 5: #impossible for both to be
        print('Player A reveals a ', deckA[(len(deckA)-1)][1])
        print('Player B reveals a ', deckB[4][1])
        print('')
        #find length of deckA - if it's 1, because discard will be empty, they lose by forfeit
        if len(deckA) == 1:
            print('')
            print("Player A's deck has no remaining cards with which to fight this war and is forced to forfeit.")
            print('')
            print("Player B wins the game.")
            return
        elif deckA[(len(deckA)-1)][0] > deckB[4][0]:
            print('Player A wins this war!')
            print('')
            #put cards in index 0-4 into winner's discard and call flip()
            winnings = deckA[0:] + deckB[0:5]
            discardA.extend(winnings)
            # print(len(discardA), 'in discard A after winnings.')
            discardA.extend(holding)
            # print(len(discardA), 'in discard A after holdings.')
            if len(deckB) >= 6:
                # print('Called from Player A winnings if B has 6+ cards: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', 0, ') + Deck B (', (len(deckB) - 5), ') = ', (len(discardA) + len(discardB) + 0 + len(deckB) - 5))
                flip([], deckB[5:], discardA, discardB)
            else:
                # print('Called from Player A winnings if B has <6 cards: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', 0, ') + Deck B (', 0, ') = ', (len(discardA) + len(discardB) + 0 + 0))
                flip([], [], discardA, discardB)
        elif deckA[(len(deckA)-1)][0] < deckB[4][0]:
            print("Player B wins the game!")
            return
        else:
            print('')
            print("Player A has run out of cards and is forced to forfeit")
            print('')
            print("Player B wins the game!")
            return
    elif len(deckB) < 5: #impossible for both to be
        print('Player A reveals a ', deckA[4][1])
        print('Player B reveals a ', deckB[(len(deckB)-1)][1])
        print('')
        if len(deckB) == 1:
            print('')
            print("Player B's deck has no remaining cards with which to fight this war and is forced to forfeit.")
            print('')
            print("Player B wins the game!")
            return
        elif deckB[(len(deckB)-1)][0] > deckA[4][0]:
            print('Player B wins this war!')
            print('')
            #put cards in index 0-4 into winner's discard and call flip()
            winnings = deckA[0:5] + deckB[0:]
            discardB.extend(winnings)
            # print(len(discardB), 'in discard B after winnings.')
            discardB.extend(holding)
            # print(len(discardB), 'in discard B after holdings.')
            if len(deckA) >= 6:
                # print('Called from Player B winnings if A has 6+ cards: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', (len(deckA) - 5), ') + Deck B (', 0, ') = ', (len(discardA) + len(discardB) + 0 + len(deckA) - 5))
                flip(deckA[5:], [], discardA, discardB)
            else:
                # print('Called from Player B winnings if A has 6+ cards: Discard A (', len(discardA), ') + Discard B (', len(discardB), ') + Deck A (', 0, ') + Deck B (', 0, ') = ', (len(discardA) + len(discardB) + 0 + 0))
                flip([], [], discardA, discardB)
        elif deckB[(len(deckB)-1)][0] < deckA[4][0]:
            print("Player A wins the game!")
            return
        else:
            print('')
            print("Player B has run out of cards and is forced to forfeit")
            print('')
            print("Player A wins the game!")
            return
    elif deckA[4][0] == deckB[4][0]: 
        print('Player A reveals a ', deckA[4][1])
        print('Player B reveals a ', deckB[4][1])
        print('')
        print('Double War!')
        print('')
        #put cards into holding and call tie() again
        holdings = deckA[0:4] + deckB[0:4]
        holding.extend(holdings)
        print(holding)
        tie(deckA[4:], deckB[4:], discardA, discardB, holding)
    elif deckA[4][0] > deckB[4][0]:
        print('Player A reveals a ', deckA[4][1])
        print('Player B reveals a ', deckB[4][1])
        print('')
        print('Player A wins this war!')
        print('')
        #put cards in index 0-4 into winner's discard
        winnings = deckA[0:5] + deckB[0:5]
        discardA.extend(winnings)
        # print(len(discardA), 'in discard A after winnings.')
        discardA.extend(holding)
        # print(len(discardA), 'in discard A after holdings.')
        if len(deckA) >= 6 and len(deckB) >= 6:
            flip(deckA[5:], deckB[5:], discardA, discardB)
        elif len(deckA) < 6:
            flip([], deckB[5:], discardA, discardB)
        elif len(deckB) < 6:
            flip(deckA[5:], [], discardA, discardB)
        else: #if both are less than 6
            flip([], [], discardA, discardB)
    elif deckA[4][0] < deckB[4][0]: 
        print('Player A reveals a ', deckA[4][1])
        print('Player B reveals a ', deckB[4][1])
        print('')
        print('Player B wins this war!')
        print('')
        #put cards in index 0-4 into winner's discard
        winnings = deckA[0:5] + deckB[0:5]
        discardB.extend(winnings)
        # print(len(discardB), 'in discard B after winnings.')
        discardB.extend(holding)
        # print(len(discardB), 'in discard B after holdings.')
        if len(deckA) >= 6 and len(deckB) >= 6:
            flip(deckA[5:], deckB[5:], discardA, discardB)
        elif len(deckA) < 6:
            flip([], deckB[5:], discardA, discardB)
        elif len(deckB) < 6:
            flip(deckA[5:], [], discardA, discardB)
        else: #if both are less than 6
            flip([], [], discardA, discardB)
    else:
        print("You found a different else statment that should never have been found.")
        return


def flip(deckA, deckB, discardA = [], discardB = []):
    '''The battles of the actual game'''
    #base case empty deck, calls empty(), which either calls shuffle() or declares a winner.
    if len(deckA) == 0 or len(deckB) == 0:
        empty(deckA, deckB, discardA, discardB)   
    #if flipped cards have same value calls tie(), which handles everything else
    elif deckA[0][0] == deckB[0][0]:
        print('Player A reveals a ', deckA[0][1])
        print('Player B reveals a ', deckB[0][1])
        print('')
        tie(deckA, deckB, discardA, discardB, [])
    elif deckA[0][0] > deckB[0][0]:
        print('Player A reveals a ', deckA[0][1])
        print('Player B reveals a ', deckB[0][1])
        print('')
        print('Player A wins this battle!')
        print('')
        # note to self: need append over extend in this case
        discardA.append(deckA[0])
        discardA.append(deckB[0])
        if len(deckA) == 1 and len(deckB) == 1:
            flip([], [], discardA, discardB)
        elif len(deckA) == 1:
            flip([], deckB[1:], discardA, discardB)
        elif len(deckB) == 1:
            flip(deckA[1:], [], discardA, discardB)
        else:
            flip(deckA[1:], deckB[1:], discardA, discardB)
    elif deckA[0][0] < deckB[0][0]:
        print('Player A reveals a ', deckA[0][1])
        print('Player B reveals a ', deckB[0][1])
        print('')
        print('Player B wins this battle!')
        print('')
        discardB.append(deckA[0])
        discardB.append(deckB[0])
        if len(deckA) == 1 and len(deckB) == 1:
            flip([], [], discardA, discardB)
        elif len(deckA) == 1:
            flip([], deckB[1:], discardA, discardB)
        elif len(deckB) == 1:
            flip(deckA[1:], [], discardA, discardB)
        else:
            flip(deckA[1:], deckB[1:], discardA, discardB)
    else:
        print("Congratulations, you've somehow broken the program and found a secret else statement!")
        return


def war(deck):
    '''Deals cards and starts the match by calling flip()'''
    # random.shuffle(deck)
    #deckA = deck[0:26]
    deckA = deck[1::2]
    #deckB = deck[26:37] + deck[50:52] + deck[37:50]
    deckB = deck[0::2]
    # print(len(deckA))
    # print(len(deckB))
    yes = input('Flip the next card? ')
    print('')
    if yes == 'Y' or yes == 'Yes' or yes == 'yes' or yes == 'y' or yes == '':
        flip(deckA, deckB)
    else:
        print("Well, ok then.")
        return

war(deck)