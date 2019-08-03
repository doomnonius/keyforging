## This is a very complicated project
This project will attempt to create a text based version of keyforge. If things go real well, I may attempt online play, a simple ai, and a graphical version, but I've got a lot of work ahead of me.
Current Goals:
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


Card notes: Cards I've implemented, w/ notes on implementation

Randoms (one-offs that get their own special checks):
- 44: Rock-Hurling Giant - has a fake(?) error

Play:
- 1: Anger - tested
- 2: Barehanded - needs retested after creating cards.pending()
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
- 30: Bumpsy - easy
- 31: Earthshaker
- 33: Ganger Chieftain
- 36: Hebe the Huge
- 40: Lomir Flamefist
- 46: Smaaash
- 49: Wardrummer - not sure won't return self to hand
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
- 

