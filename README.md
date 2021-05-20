<h1>This is a very complicated project</h1>

<h2>This project will attempt to create a graphical version of keyforge. If things go real well, I may attempt online play and a simple ai, but I've got a lot of work ahead of me.<h2>
<h3>BUGS:<h3>
<ul>
 <li>https://stackoverflow.com/questions/20264403/how-to-make-a-popup-radial-menu-in-pygame</li>
 <li>https://www.pygame.org/docs/genindex.html</li>
 <li>https://www.pygame.org/docs/tut/ChimpLineByLine.html</li>
 <li><s>Says who is going first twice</s> (though really a lot of the mulligan phase needs to be updated, not just that)</li>
 <li>The game usually doesn't currently tell you if an attempt to play a card failed, or why it failed.</li>
 <li>Cards aren't tapped when exhausted.</li>
 <li>Code not yet implemented to differentiate action from artifact v action from creature.</li>
 <li>Code not yet implemented to only display valid options for items, instead of all.</li>
 <li>Upgrades don't work</li>
 <li>Wild wormhole doesn't work</li>
 <li>Something I don't quite understand in line 1322 of game.py about things with play effects</li>
 <li>State dictionaries.</li>
 <li>Hovering over deck or discard says how many cards are in it.</li>
 <li>Clicking on discard shows what cards are in it.</li>
 <li>Get rid of basically all print statements.</li>
 <li>Enable dragging and dropping cards.</li>
 <li>Upgrades don't work. (Or things in later sets that give other cards abilities).</li>
 <li>Check all the card options properly (for example, checkActionStates tries to check if an artifact is stunned and crashes).</li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li></li>
 <li><s>Amber doesn't update properly.</s></li>
 <li><s>Discard card always says cards aren't in active house.</s></li>
</ul>

<h3>Current Goals:</h3>
<ul>
 <li><s>Be able to import and save decks</s> - <b>Done</b></li>
 <li><s>Create initial game setup:</s></li>
 <li><s>Choosing which decks to play</s> - <b>Done</b></li>
 <li><s>Deciding who goes first</s> - <b>Done</b></li>
 <li><s>Drawing up to a full hand</s> - <b>Done</b></li>
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
   </ol>
 </li>
 <li>Build a state dict that only has the relevant information</li>
 <li>Sort hand by house</li>
 <li>Update Decks option from startup() so that people can examine what is in a deck</li>
 <li>Write all the functions for all the cards, which will include a whole lot of states, so I'm also going to want to figure out a way for a game that is called to only pay attention to the relevant states.</li>
 <li><s>Rewrite the base code to reflect the implementation of the cards (ie in responses())</s></li>
 <li><s>update the play card function to tell the player how much amber they got for playing the card.</s></li>
 <li>Also, update it to make it more succinct (hint: use return statements?). - I think its good enough as is for now</li>
 <li>need to implement hazardous and assault in fights</li>
 <li>need to implement upgrades (and then figure out how to work them into pending): initial thought: upgrades have their own list and creatures are linked to them</li>
 <li>figure out where destroyed abilities get called from <b>Answer: from pending, if destroyed = True</b></li>
 <li>write one-offs for Krump and creatures of his ilk</li>
 <li>the pending function will need to call card.dest, and definitely will need to call card.leaves</li>
 <li>when do I check for taunt?</li>
 <li>implement a "Check for x key!" step</li>
 <li>implement the rule of six</li>
</ul>

<h2>Bugs: </h2>
<ol>
<li>extra armor is always applied, even if it's been broken. Potential Solution: a calcExtraArmor() function, which needs to remember if a card has been hit yet this turn.</li>
<li>if Sneklifter steals an artifact and it doesn't belong to one of the active player's houses, it gets changed to house Shadows. This is good. The bug is that if the artifact leaves play it doesn't get changed back.</li>
<li>If scout gives a minion skirmish for a turn, it keeps skirmish until death. Might be fixed.</li>
<li>Nocturnal Manuevers didn't work.</li>
</ol>

<h2>Card notes: (Cards I've implemented, w/ notes on implementation)</h2>
<ul>
  <li>44: Rock-Hurling Giant - not sure I implemented this well</li>
  <li>261: The Vaultkeeper</li>
  <li>295: The Sting</li>
  <li>298: Carlo Phantom</li>
  <li>354: Giant Sloth - needs to be finished in card reset</li>
  <li>366: Teliga</li>
  <li>367: Hunting Witch
</ul>

<h3>Randoms (one-offs that will get their own special checks):</h3>
<ul>
  <li>192: Ether Spider - won't have a state, will just check for it everytime amber is gained (event emitter?)</li>
</ul>


<h3>Play:</h3>
<h4>Brobnar:</h4>
<ul>
  <li>1: Anger - tested</li>
  <li>2: Barehanded - needs retested after creating cards.pending() - passed retest</li>
  <li>3: Blood Money</li>
  <li>4: Brothers in Battle - made changes to Game.chooseHouse() for this</li>
  <li>5: Burn the Stockpile</li>
  <li>6: Champion's Challenge - possily janky stuff here</li>
  <li>7: Cowards End</li>
  <li>8: Follow the Leader - also uses Game.chooseHouse()</li>
  <li>9: Lava Ball - uses Card.damageCalc()</li>
  <li>10: <u>Loot the Bodies</u> - skipped for now</li>
  <li>11: Take that, Smartypants - uses cards.stealAmber()</li>
  <li>12: Punch - also uses Card.damageCalc()</li>
  <li>13: Relentles Assault - pretty janky b/c I have to make sure they don't target the same minion more than once</li>
  <li>14: Smith - easy</li>
  <li>15: Sound the Horns</li>
  <li>16: Tremor</li>
  <li>17: Unguarded Camp</li>
  <li>18: Warsong - doesn't account for multiple copies</li>
  <li>30: Bumpsy - tested</li>
  <li>31: Earthshaker - <u><b>passed</u></b></li>
  <li>33: Ganger Chieftain</li>
  <li>36: Hebe the Huge</li>
  <li>40: Lomir Flamefist</li>
  <li>46: Smaaash</li>
  <li>49: Wardrummer - not sure won't return self to hand - <u><b>passed</u></b></li>
  <li>52: Yo Mama Mastery - only handles the healing part</li>
</ul>
<h4>Dis:</h4>
<ul>
  <li>53: A Fair Game</li>
  <li>54: Arise</li>
  <li>55: Control the Weak - will need an EOT state reset</li>
  <li>56: Creeping Oblivion</li>
  <li>57: Dance of Doom</li>
  <li>58: Fear - need to implemenet a reset function to reset cards to default state when leave board</li>
  <li>59: Gateway to Dis - foreseen difficulties: Armageddon Cloak</li>
  <li>60: Gongoozle</li>
  <li>61: Guilty Hearts</li>
  <li>62: Hand of Dis</li>
  <li>63: Hecatomb</li>
  <li>64: Tendrils of Pain - added a self.forgedLastTurn value to game</li>
  <li>65: Hysteria</li>
  <li>66: Key Hammer</li>
  <li>67: Mind Barb</li>
  <li>68: Pandemonium - created self.capture(game, num) function in Card</li>
  <li>69: Poltergeist - modified chooseSide() to work for artifacts too</li>
  <li>70: Red-Hot Armor</li>
  <li>71: Three Fates - this one was surprisingly tough</li>
  <li>81: Charette - one line</li>
  <li>82: Drumble - two lines</li>
  <li>88: Guardian Demon</li>
  <li>94: Restringuntus: added to game.chooseHouse</li>
  <li>96: Shooler</li>
  <li>101: The Terror</li>
</ul>
<h4>Logos:</h4>
<ul>
  <li>107: Bouncing Death Quark</li>
  <li>108: Dimension Door - still need to update the reaping function to deal check for this</li>
  <li>109: Effervescent Principle</li>
  <li>110: Foggify</li>
  <li>111: Help from Future Self</li>
  <li>112: Interdimensional Graft</li>
  <li>113: Knowledge is Power</li>
  <li>114: Labwork</li>
  <li>115: Library Access</li>
  <li>116: Neuro Syphon</li>
  <li>117: Phase Shift</li>
  <li>118: Positron Bolt</li>
  <li>119: Random Access Archives</li>
  <li>120: Remote Access - waiting on implementation of actions</li>
  <li>121: Reverse Time</li>
  <li>122: Scrambler Storm</li>
  <li>123: Sloppy Labwork</li>
  <li>124: Twin Bolt Emission</li>
  <li>125: Wild Wormhole</li>
  <li>138: Dextre</li>
  <li>140: Dr. Escotera</li>
  <li>141: Dysania</li>
  <li>143: Harland Mindlock</li>
  <li>146: Neutron Shark - kind of complicated</li>
  <li>149: Psychic Bug</li>
  <li>152: Skippy Timehog - created checkReapState and checkActionState</li>
  <li>153: Timetraveller</li>
  <li>157: Experimental Therapy</li>
</ul>
<h4>Mars:</h4>
<ul>
  <li>160: Ammonia Clouds</li>
  <li>161: Battle Fleet</li>
  <li>162: Deep Probe - create an OppHouses option in responses</li>
  <li>163: EMP Blast</li>
  <li>164: Hypnotic Command</li>
  <li>165: Irradiated Aember</li>
  <li>166: Key Abduction</li>
  <li>167: Martian Hounds</li>
  <li>168: Martians Make Bad Allies - found a couple bugs that I had already implemented several times in my code. Think I fixed them all</li>
  <li>169: Mass </li>
  <li>170: Mating Season</li>
  <li>171: Mothership Support</li>
  <li>172: Orbital Bombardment</li>
  <li>173: Phosphorous Stars</li>
  <li>174: Psychic Network</li>
  <li>175: Sample Collection</li>
  <li>176: Shatter Storm</li>
  <li>177: Soft Landing - another thing for states</li>
  <li>178: Squawker</li>
  <li>179: Total Recall</li>
  <li>203: Yxili Marauder</li>
</ul>
<h4>Sanctum:</h4>
<ul>
  <li>212: Begone</li>
  <li>213: Blinding Light</li>
  <li>214: Charge</li>
  <li>215: Cleansing Wave</li>
  <li>216: Clear Mind</li>
  <li>217: Doorstep to Heaven</li>
  <li>218: Glorious Few</li>
  <li>219: Honorable Claim</li>
  <li>220: Inspiration</li>
  <li>221: Mighty Lance</li>
  <li>222: Oath of Poverty</li>
  <li>223: One Stood Against Many</li>
  <li>224: Radiant Truth</li>
  <li>225: Shield of Justice</li>
  <li>226: Take Hostages</li>
  <li>227: Terms of Redress</li>
  <li>228: The Harder They Come</li>
  <li>229: The Spirit's Way</li>
  <li>231: Epic Quest</li>
  <li>246: Horseman of Death</li>
  <li>247: Horseman of Famine</li>
  <li>248: Horseman of Pestilence</li>
  <li>249: Horseman of War</li>
  <li>251: Lady Maxena</li>
  <li>253: Raiding Knight</li>
  <li>258: Sergeant Zakiel</li>
  <li>260: Gatekeeper</li>
  <li>262: Veemos Lightbringer</li>
</ul>
<h4>Shadows:</h4>
<ul>
  <li>267: Bait and Switch (nerfed version)</li>
  <li>268: Booby Trap</li>
  <li>269: Finishing Blow</li>
  <li>270: Ghostly Hand</li>
  <li>271: Hidden Stash</li>
  <li>272: Imperial Traitor</li>
  <li>273: Key of Darkness</li>
  <li>274: Lights Out</li>
  <li>275: Miasma</li>
  <li>276: Nerve Blast</li>
  <li>277: One Last Job</li>
  <li>278: Oubliette</li>
  <li>279: Pawn Sacrifict</li>
  <li>280: Poison Wave</li>
  <li>281: Relentless Whispers</li>
  <li>282: Routine Job</li>
  <li>283: Too Much to Protect</li>
  <li>284: Treasure Map</li>
  <li>288: Masterplan</li>
  <li>303: Magda the Rat</li>
  <li>307: Old Bruno</li>
  <li>313: Sneklifter</li>
  <li>315: Urchin</li>
</ul>
<h4>Untamed</h4>
<ul>
  <li>319: Cooperative Hunting</li>
  <li>320: Curiosity</li>
  <li>321: Fertility Chant</li>
  <li>322: Fogbank</li>
  <li>323: Full Moon</li>
  <li>324: Grasping Vines</li>
  <li>325: Key Charge</li>
  <li>326: Lifeweb</li>
  <li>327: Lost in the Woods</li>
  <li>328: Mimicry</li>
  <li>329: Nature's Call</li>
  <li>330: Nocturnal Maneuver</li>
  <li>331: Perilous Wild</li>
  <li>332: Regrowth</li>
  <li>333: Save the Pack</li>
  <li>334: Scout</li>
  <li>335: Stampede</li>
  <li>336: The Common Cold</li>
  <li>337: Troop Call</li>
  <li>338: Vigor</li>
  <li>339: Word of Returning</li>
  <li>349: Chota Hazri</li>
  <li>352: Flaxia</li>
  <li>353: Fuzzy Gruen</li>
  <li>356: Inka the Spider</li>
  <li>359: Lupo the Scarred</li>
  <li>360: Mighty Tiger</li>
  <li>365: Piranha Monkeys</li>
</ul>