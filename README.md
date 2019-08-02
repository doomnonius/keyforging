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

Play:
- 1: Anger - tested
- 2: Barehanded - needs retested after creating pending()
- 3: Blood Money
- 4: Brothers in Battle - made changes to Game.chooseHouse() for this
- 5: Burn the Stockpile
- 6: Champion's Challenge
- 7: Cowards End
- 8: Follow the Leader - also uses Game.chooseHouse()
