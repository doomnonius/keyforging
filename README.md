<h1>This project will attempt to create a graphical version of keyforge. If things go real well, I may attempt online play and a simple ai, but I've got a lot of work ahead of me.<h1>

<h2>This project uses pygame: https://www.pygame.org/docs/genindex.html</h2>

<h3>Dependencies:<h3>
<ul>
  <li>types</li>
  <li>pygame</li>
  <li>json</li>
  <li>random</li>
  <li>logging</li>
  <li>pyautogui</li>
  <li>os</li>
  <li>sys</li>
  <li>argparse</li>
  <li>typing</li>
  <li>requests</li>
  <li>time</li>
  <li></li>
  <li></li>
</ul>

<h3>Planned features / Current Goals:<h3>
<ul>
 <li>If an effect (like lash of broken dreams) is applied more than once, show that in the mini image.</li>
 <li>Update choose flank to choose which side an opponent's creature entering will go on.</li>
 <li>If a state thing targets something specific, that should also be shown in the hover.</li>
 <li>If collar of subordination leaves play, the creature should return to its owner.</li>
 <li>A whole lot more game assets, for stun, enrage, damage, card backs, rest of house symbols, etc.</li>
 <li>Handling Mavericks? - atm back end will know, but player won't - want to handle this kind of like how I will handle drawing counters</li>
 <li>Settings button (immediately below end turn?) and menu.</li>
 <li>Make some selection windows not ask for confirmation (particularly the end turn one)</li>
 <li>If autocannon (or pingle) kills a creature, its play ability will not resolve - but activePlayer should decide the order of those things, since they are in the same timing window, so they could choose the proper order. - This is related to the whole library access trigger/card play effect trigger I have noted immediately below.</li>
 <li>A function for ordering simultaneous things or choosing a number of items from the list of abilities.</li>
 <li>Code reap, fight, action, abilities with knowledge that there might be more than one</li>
 <li>basic dest called from pending, not tied to the card, same with basicReap and basicFight</li>
 <li>game.pending() needs updates - including handling cards with upgrades attached or cards under them and handling card.reveal - everytime a function tries to ref pendingReloc, it needs to check if pendingReloc contains something - if it does, then this is a nested destroy, and secondary needs to be used instead - I think this shouldn't matter for play effects in CotA</li>
 <li>Have spangler box use card.under?</li>
 <li>Display the card that's under Masterplan - based on ruling on Jargogle, it can be looked at by controller of Jargogle</li>
 <li>card.reveal should be being changed constantly as cards move around, ie you can see your cards in opp's archives, but not theirs, unless it is revealed</li>
 <li>Picking decks within game window - will be another while loop</li>
 <li>Verify game integrity at ends of turns.</li>
 <li>Arrows like H*********e for fighting?</li>
 <li>Ready creature entering next to tapped taunt looks like it has taunt in chooseFlank</li>
 <li>things in later sets that give other cards abilities</li>
 <li>What about having the background color of the active Player's mat match the color of the house they've chosen?- No, if only because of the tide coming in later sets.</li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li><s>Reworked damageCalc and capture to be consistent with gainAmber</s></li>
 <li><s>Capture is wrong in a number of instances (order of variables).</s></li>
 <li><s>Remove helpers.destroy()'s middle argument</s></li>
 <li><s>Get rid of remaining print statements/turn into log statements.</s></li>
 <li><s>need to implement upgrades (and then figure out how to work them into pending): initial thought: upgrades have their own list and creatures are linked to them</s></li>
 <li><s>If a card is trying to find it's own index, can it tell itself apart from another card with the same name?</s> - Yes</li>
 <li><s>Implement the check step, and make it obvious opponent is in check (have an idea that involves using self.highlight)</s></li>
 <li><s>I need a destroy function for handling ward and invulnerable -> or make changes to updateHealth.</s> - both and, and seems to be working</li>
 <li><s>Obsolete the chooseMulligan function by adding a color option to chooseHouse, which is now a misnamed function</s></li>
 <li><s>Room for optimizing draw, along the lines of what I did with keys, amber, and houses. For example, putting a function in passFunc that updates the board draws.</s></li>
 <li><s>Change color of End Turn button when no more available actions. - save until done with all activatable things - create a function to use canPlay, canDiscard, etc for this, but don't check every loop, only after each card is played (and there are a lot of ways to do that so that will be tough)</s></li>
 <li><s>The checks for if you can fight/play/reap with a card need to be in the playCard/etc. sections because "cheating" out those things shouldn't work. - creating canPlay, canDiscard, etc. functions for this</s> - This should be implemented now, though could use more testing. Amusingly, I had features like this from the first run that I actually removed.</li>
 <li><s>Artifacts use chooseFlank too</s></li>
 <li><s>Highlight active house</s></li>
 <li><s>Upgrades don't work.</s></li>
 <li><s>Keys don't flip - going to need to switch keys each turn too</s></li>
 <li><s>Drag to discard.</s></li>
 <li><s>Put upgrades into their own file so we don't have to import play into main, will have to import passFunc into upgrades though.</s></li>
 <li><s>Enable dragging and dropping cards.</s></li>
 <li><s>Choosing what flank a creature goes on - use a bool like for drawing discards (I used chooseHouse as a temporary solution)</s></li>
 <li><s>Add archive to the board, viewable.</s></li>
 <li><s>Make purge list viewable.</s></li>
 <li><s>After you preselect a house, highlight all cards on your board (and archive) of that house.</s></li>
 <li><s>Wild wormhole doesn't work - we'll get there</s></li>
 <li><s>Hovering over deck or discard says how many cards are in it.</s></li>
 <li><s>Clicking on discard shows what cards are in it.</s></li>
 <li><s>Incorporate a condition into chooseCards</s></li>
 <li><s>Put a red layer over items that aren't allowed to be selected.</s></li>
 <li><s>I want the algo for drawing creatures, artifacts, to put them in the middle of their area. For now I'm not going to do this for hands.</s> - That was easier than I thought it was going to be.</li>
 <li><s>Interacting with the state dictionaries.</s> - in progress</li>
 <li><s>If a card is tapped, it's untapped rect should be outside the board, and vice versa - this could be put in game.switch()</s> - actually put it in draw</li>
 <li><s>game.chooseCards: (1) can infinite loop if the list they try to target is empty (2) can't handle choosing from different lists at the same time (3) should highlight chosen cards</s></li>
 <li><s>Key locations not scaled to size of display.</s></li>
 <li><s>Should be able to cancel out of the chooseCards menu (this could also allow for selecting less than the full number of targets)</s></li>
 <li><s>Mulligan phase - should be able to hover cards while choosing whether to keep.</s></li>
 <li><s>Something I don't quite understand in line 1322 of game.py about things with play effects</s> - changed implementation, still refactoring but should be much better.</li>
 <li><s>Code not yet implemented to differentiate action from artifact v action from creature.</s> - pretty sure this is fixed, but also not sure what I meant</li>
 <li><s>Check status of fighters after fight.</s> Actually problem here was checking the attacker twice, instead of checking attacker and defender. So if attacker survived, so did defender.</li>
 <li><s>Losing Amber from playing Truebaru</s></li>
 <li><s>The '#other play effects' section of checkPlayStates should be incorporated in checks made when a card ETBs.</s></li>
 <li><s>Lifeward preventing playing creatures</s></li>
 <li><s>Aember imp preventing playing more than two cards.</s></li>
 <li><s>Be able to import and save decks</s> - <b>Done</b></li>
 <li><s>Create initial game setup:</s></li>
 <li><s>Choosing which decks to play</s> - <b>Done</b></li>
 <li><s>Deciding who goes first</s> - <b>Done</b></li>
 <li><s>Drawing up to a full hand</s> - <b>Done</b></li>
 <li><s>>when do I check for taunt?</s></li>
 <li><s>Playing the first turn (because it has its own special requirements)</s> - <b>Done</b></li>
 <li>Create the turn, including:
    <ol>
      <li><s>Forge a key</s>- <b>Done</b></li>
      <li><s>Choose a house</s> - <b>Done</b></li>
      <li><s>At this point they may pick up their archive</s></li>
      <li><s>Play, discard and use cards of the active house.</s> Using includes:
        <ul>
          <li>Fighting</li> Done, except for after fight effects
          <li>Reaping</li> Implemented, but w/o effects
          <li>Actions</li> Implemented, but w/o effects
        </ul>
      </li>
      <li><s>Ready Cards</s> - <b>Done</b></li>
      <li><s>Draw Cards</s> - <b>Done</b></li>
      <li><s>EOT effects, and declare "Check!" - Also making more obvious that opponent is about to forge</s></li>
   </ol>
 </li>
 <li><s>Build a state dict that only has the relevant information</s></li>
 <li><s>Logger wil be defined in main, and imported into everything else and called there.</s></li>
 <li><s>Sort hand by house</s></li>
 <li><s>Rewrite the base code to reflect the implementation of the cards (ie in responses())</s></li>
 <li><s>update the play card function to tell the player how much amber they got for playing the card.</s></li>
 <li><s>Also, update playCard to make it more succinct</s></li>
 <li><s>figure out where destroyed abilities get called from <b>Answer: from pending, if destroyed = True</b></s></li>
 <li><s>https://stackoverflow.com/questions/20264403/how-to-make-a-popup-radial-menu-in-pygame</s></li>
 <li></li>
 <li></li>
</ul>

<h2>Testing / Rules: </h2>
<ol>
<li>Make choose house use houseSymbols instead</li>
<li>Update the lambda for "Are you sure you want to end your turn" to highlight all usable things.</li>
<li>Armor recalc for Bulwark and Shoulder armor in calcPower</li>
<li>Only display valid options for items, instead of all</li>
<li>Log if an attempt to play a card failed</li>
<li>I really need to throw in a whole bunch of logging all over the place.</li>
<li>Make a tiny purged image.</li>
<li>Write all the functions for all the cards.</li>
<li>game.pending should be able to handle things going into archives from play (because of card.reset()) - used in combo with return_card</li>
<li>Gonna need some sort of calcPower function or some one offs that get called in cardChanged - <s>related: Correct power + extraPow to just power, and make sure we're regularly recalcing power</s></li>
<li>Rework calls to playCard for cheat/played_from change</li>
<li>Mimicry on Library Access? - should purge Mimicry</li>
<li>Veylan Analyst should give amber for using an opponent's artifact - need to create an option in use artifact to use an opponent's artifact, or alternatively temporarily copy it into active board then delete it - this second option won't work because it will end up getting drawn, unless we create something a bool that prevents cards from being drawn.</li>
<li>Scale the selected surf</li>
<li>Small versions of cards with turn effects drawn in the center area, hoverable.</li>
<li>End turn button off to the right of the neutral area.</li>
<li>Scale cards in hand too.</li>
<li>Handle if chooseHouse or chooseCards get called with no valid options.</li>
<li>Update how using an opponent's artifact works, then update Nexus, Poltergeist, and Remote Access to also work with Omni abilities.</li>
<li>Bug related to hover_rect.</li>
<li>While resolving the effect of an action card, have it displaying in the top left corner, but also allow it to be minimized and maximized.</li>
<li>Implement card.heal instead of subtracting damage.</li>
<li>Phase shift allows extra plays on turn 1 - partially implemented (needs to be a non Logos card played).</li>
<li>implement the rule of six: change playedThisTurn, etc into dictionaries?</li>
<li>Along the lines of the optimized game.draw, I feel like I now have more flexibility to deal with situations where cards would go outside the bounds of their area, ie with upgrades and more than 15 card in hand or more than 12(?) creatures or artifacts</li>
<li>Is captured amber returned, while amber on artifacts lost? - this will be in game.pending</li>
<li>Mantle of Zealot and Experimental Therapy in canReap, canFight, canAction: note that these actually do work differently, and Experimental Therapy is going to be a b to implement properly.</li>
<li>Reset cards back to default state after leaving the board (the function needs to written in cardsAsClass, and then called in game.pending)</li>
<li>the pending function will need to call card.dest, and definitely will need to call card.leaves</li>
<li>write after fights for Krump and creatures of his ilk - this means after fight will need to fed three variables</li>
<li>If they try to end the turn early, highlight the things they could still do.</li>
<li>Something that makes collision detection different if scaled - going to have to go in a lot of different places.</li>
<li>The dragging in chooseFlank is also tied going to need to know about scaled.</li>
<li>need to implement hazardous and assault and poison in fights</li>
<li>Get hazardous and assault working - should be easy, but I made it more difficult than it needed to be. Could use more testing.</li>
<li>Replicator won't currently interact with sequis properly</li>
<li>Can use wild wormhole to cheat out a card with ember imp in play? Rules-wise it can't, as wildwormhole only gets around the first turn rule b/c that rule applies to playing out of hand.</li>
</ol>

<h2>Bugs: </h2>
<ol>
<li>Dysania won't work. - now maybe she will</li>
<li>Picking up archive didn't work.</li>
<li>extra armor is always applied, even if it's been broken. Potential Solution: a calcExtraArmor() function, which needs to remember if a card has been hit yet this turn.</li>
<li>if Sneklifter steals an artifact and it doesn't belong to one of the active player's houses, it gets changed to house Shadows. This is good. The bug is that if the artifact leaves play it doesn't get changed back.</li>
<li>If scout gives a minion skirmish for a turn, it keeps skirmish until death. Might be fixed.</li>
<li>Nocturnal Manuevers didn't work.</li>
<li>Artifact of active house thinks it can't be used. - b/c actions aren't set up yet</li>
<li>Bug with keys that I'm pretty sure is because all forged keys are referencing the same image.</li>
<li>Technically supposed to be able to choose whether library access or a card's play effect triggers first, but that's not how it's implemented in the code.</li>
<li>Drag card overrides the close button.</li>
<li>Wild wormhole out an upgrade - does it remove upgrade from top of deck?</li>
<li>Bad Penny didn't work, nor biomatrix backup, probably will have similar issues with similar cards.</li>
<li>Francus didn't work, I though Krump did work once but he doesn't always.</li>
<li>I don't think amber is returned properly by cards leaving play - or it might just be ether spider</li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li></li>
<li><s>Ether spider doesn't work for stealing amber.</s> - updated stealAmber to use gainAmber</li>
<li><s>Experienced a glitch where extra cards I couldn't hover ended up in my hand. This was on turn one in a game. Haven't seen it replicated yet.</s> - wasn't resetting cardBlits.</li>
<li><s>add things that enter ready and/or stunned to the play list.</s></li>
<li><s>Implement self.played/discarded/used this/last turn; this includes removing self.numPlays, self.numDiscards, self.creaturesPlayed</s></li>
<li><s>Can cheat out extra fighting with stunned things, shouldn't be able to.</s></li>
<li><s>Things that could target themselves won't be drawn in yet during the targeting phase. Might be fixed.</s></li>
<li><s>Bug: Hover on left card in opp hand shows left card in your hand instead.</s></li><li><s>Fix things going beyond bound of screen.</s></li>
<li><s>Cards aren't tapped when exhausted.</s></li>
<li><s>Don't make the extra space for tapping in the hand, only the board.</s></li>
<li><s>Amber doesn't update properly.</s></li>
<li><s>Discard card always says cards aren't in active house.</s></li>
<li><s>Says who is going first twice</s></li>
<li><s>Hitboxes for tapped cards should exist.<s></li>
</ol>

<h2>Card notes: (Cards I've tested, w/ notes)</h2>
<ul>
  <li></li>
</ul>