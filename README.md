<h1>This is a very complicated project</h1>

<h2>This project will attempt to create a text based version of keyforge. If things go real well, I may attempt online play, a simple ai, and a graphical version, but I've got a lot of work ahead of me.<h2>
<h3>Current Goals:</h3>
 - <s>Be able to import and save decks</s> - <b>Done</b>
 - <s>Create initial game setup:</s>
   - <s>Choosing which decks to play</s> - <b>Done</b>
   - <s>Deciding who goes first</s> - <b>Done</b>
   - <s>Drawing up to a full hand</s> - <b>Done</b>
   - <s>Playing the first turn (because it has its own special requirements)</s> - <b>Done</b>
 - Create the turn, including:
   - <s>Forge a key</s>- <b>Done</b>
   - <s>Choose a house</s> - <b>Done</b>
     - <u>At this point they may pick up their archive</u>
   - Play, discard and use cards of the active house. Using includes:
     - Fighting
     - Reaping
     - Actions
   - <s>Ready Cards</s> - <b>Done</b>
   - <s>Draw Cards</s> - <b>Done</b>
- Write all the functions for all the cards, which will include a whole lot of states, so I'm also going to want to figure out a way for a game that is called to only pay attention to the relevant states.
- Rewrite the base code to reflect the implementation of the cards


<h2>Card notes: (Cards I've implemented, w/ notes on implementation)</h2>

<h3>Randoms (one-offs that get their own special checks):</h3>
- 44: Rock-Hurling Giant

<h3>Play:</h3>
- 1: Anger - tested
- 2: Barehanded - needs retested after creating cards.pending() - passed retest
- 3: Blood Money
- 4: Brothers in Battle - made changes to Game.chooseHouse() for this
- 5: Burn the Stockpile
- 6: Champion's Challenge - possily janky stuff here
- 7: Cowards End
- 8: Follow the Leader - also uses Game.chooseHouse()
- 9: Lava Ball - uses Card.damageCalc()
- 10: <u>Loot the Bodies</u> - skipped for now
- 11: Take that, Smartypants - uses cards.stealAmber()
- 12: Punch - also uses Card.damageCalc()
- 13: Relentles Assault - pretty janky b/c I have to make sure they don't target the same minion more than once
- 14: Smith - easy
- 15: Sound the Horns
- 16: Tremor
- 17: Unguarded Camp
- 18: Warsong - doesn't account for multiple copies
- 30: Bumpsy - tested
- 31: Earthshaker - <b><s>failed</b></s> (Probably b/c of backwardsList)
- 33: Ganger Chieftain
- 36: Hebe the Huge
- 40: Lomir Flamefist
- 46: Smaaash
- 49: Wardrummer - not sure won't return self to hand - <u><b>failed</u></b> (probably b/c of backwardsList)
- 52: Yo Mama Mastery - only handles the healing part
- 53: A Fair Game
- 54: Arise
- 55: Control the Weak - will need an EOT state reset
- 56: Creeping Oblivion
- 57: Dance of Doom
- 58: Fear - need to implemenet a reset function to reset cards to default state when leave board
- 59: Gateway to Dis - foreseen difficulties: Armageddon Cloak
- 60: Gongoozle
- 61: Guilty Hearts
- 62: Hand of Dis
- 63: Hecatomb
- 64: Tendrils of Pain - added a self.forgedLastTurn value to game
- 65: Hysteria
- 66: Key Hammer
- 67: Mind Barb
- 68: Pandemonium - created self.capture(game, num) function in Card
- 69: Poltergeist - modified chooseSide() to work for artifacts too
- 70: Red-Hot Armor
- 71: Three Fates - this one was surprisingly tough
- 81: Charette - one line
- 82: Drumble - two lines
- 88: Guardian Demon
- 94: Restringuntus: added to game.chooseHouse
- 96: Shooler
- 101: The Terror
- 107: Bouncing Death Quark
- 108: Dimension Door - still need to update checkReapState to check for this
- 109: Effervescent Principle
- 110: Foggify - still need to update checkFightState
- 111: Help from Future Self
- 112: Interdimensional Graft
- 113: Knowledge is Power
- 114: Labwork
- 115: Library Access
- 116: Neuro Syphon
- 117: Phase Shift
- 118: Positron Bolt
- 119: Random Access Archives
- 120: Remote Access - waiting on implementation of actions
- 121: Reverse Time
- 122: Scrambler Storm
- 123: Sloppy Labwork
- 124: Twin Bolt Emission
- 125: Wild Wormhole
- 138: Dextre
- 140: Dr. Escotera
- 141: Dysania
- 143: Harland Mindlock - update pending to make sure it puts cards in the right discard pile
- 146: Neutron Shark - kind of complicated
- 149:
- 152: 
- 153:
- 157:
