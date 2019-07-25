## This is a very complicated project
This project will attempt to create a text based version of keyforge. If things go real well, I may attempt online play, a simple ai, and a graphical version, but I've got a lot of work ahead of me.
Current Goals:
 - <s>Be able to import and save decks</s> - <b>Done</b>
 - Create initial game setup:
   - <s>Choosing which decks to play</s> - <b>Done</b>
   - <s>Deciding who goes first</s> - <b>Done</b>
   - <s>Drawing up to a full hand</s> - <b>Done</b>
   - Playing the first turn (because it has its own special requirements)
 - Create the turn, including:
   - Forge a key
   - Choose a house
     - At this point they may pick up their archive
   - Play, discard and use cards of the active house. Using includes:
     - Fighting
     - Reaping
     - Actions
   - Ready Cards
   - Draw Cards
- Write all the functions for all the cards, which will include a whole lot of states, so I'm also going to want to figure out a way for a game that is called to only pay attention to the relevant states.
