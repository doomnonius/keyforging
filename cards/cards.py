import actions
import creatures
import destroyed
import fight
import play
import reap

def printdetails(card):
    """Prints a card's details by calling listdetails()."""
    # Maybe edit this to create a list of a card's details?
    # This won't live update, so only for describing hand/deck/discard/purge
    x = listdetails(card)
    if x[3] == "Creature":
        print(x[0]) #title
        print("Amber:", x[1]) #amber
        print(x[2], x[3]) #house and type
        print("Power:", x[4], "(", x[6], "damage )", "; Armor:", x[5]) #power and armor
        print(x[7]) #traits
        print(x[8]) #text
        if x[9] != False:
            print(x[9]) #flavor
        print(x[10], ",", x[11]) #rarity and expansion
        print('')
    else:
        print(x[0]) #title
        print("Amber:", x[1]) #amber
        print(x[2], x[3]) #house and type
        print(x[4]) #text
        if x[5] != False:
            print(x[5]) #flavor
        print(x[6], ",", x[7]) #rarity and expansion
        print('')

def listdetails(card):
    """Creates and returns a list of a card's details."""
    # if action
    if card.typ == "Action":
        details = [card.title, card.amber, card.house, card.typ, card.text, card.flavor, card.rarity, card.expansion]
    # if creature
    elif card.typ == "Creature":
        details = [card.title, card.amber, card.house, card.typ, card.power, card.armor, card.damage, card.traits, card.text, card.flavor, card.rarity, card.expansion]
    # if upgrade or artifact
    else:
        details = [card.title, card.amber, card.house, card.typ, card.text, card.flavor, card.rarity, card.expansion]
    return details

# Or create an array/list for each card, and class Card: takes a list and creates a card out of it?
# This idea is feasible, but I can just use subclasses. This will create unique versions of each card, even if the card itself appears many times in a deck or game.

# Seems redundant. At least use as a test of inheritance.
# Maybe could use this to create mavericks (inheritance at least, if not the Card class also)

class Card:
    title = "title"
    house = "house"
    typ = "type"
    text = "type"
    traits = False
    amber = 0
    power = 0
    damage = 0
    health = power - damage
    armor = 0
    rarity = "rarity"
    flavor = "flavor"
    number = 0
    expansion = "exp"
    is_maverick = False

class Anger(Card):
    title = "Anger"
    house = "Brobnar"
    typ = "Action"
    text = "Play: Ready and fight with a friendly creature."
    traits = False
    amber = 1
    power = 0
    armor = 0
    rarity = "Common"
    flavor = "'Don’t make them angry you say? Heh. The Brobnar are born angry.' –Old Bruno"
    number = 1
    expansion = "CoA"
    is_maverick = False
    play = play.anger

printdetails(Anger)

class Barehanded(Card):
    title = "Barehanded"
    house = "Brobnar"
    typ = "Action"
    text = "Play: Put each artifact on top of its owner’s deck."
    traits = False
    amber = 1
    power = 0
    armor = 0
    rarity = "Rare"
    flavor = 0
    number = 2
    expansion = "CoA"
    is_maverick = False
    play = play.barehanded

printdetails(Barehanded)

class BilgumAvalanche(Card):
    title = "Bilgum Avalanche"
    house = "Brobnar"
    typ = "Creature"
    text = "After you forge a key deal 2 damage to each enemy creature."
    traits = "Giant"
    amber = 0
    power = 5
    damage = 0
    health = power - damage
    armor = 0
    rarity = "Rare"
    flavor = "''Some call her 'warleader.' Some call her 'demon.' I just call her 'Avalanche.'' –Dodger'"
    number = 28
    expansion = "CoA"
    is_maverick = False
    # def afterKey(boo):
        # """A function to apply the card text."""
        # if boo:
            # health of each enemy creature - 2
            # x.damage + 2 for x in [Enemy Board]
        # else:
            #nothing

printdetails(BilgumAvalanche)

class BloodMoney(Card):
    title = "Blood Money"
    house = "Brobnar"
    typ = "Action"
    text = "Play: Place 2 amber from the common supply on an enemy creature."
    traits = False
    amber = 0
    power = 0
    armor = 0
    rarity = "Uncommon"
    flavor = "You! Æmber lover. You’re next."
    number = 3
    expansion = "CoA"
    is_maverick = False

class BrothersInBattle:
    title = "Brothers in Battle"
    house = "Brobnar"
    typ = "Action"
    text = "Play: Choose a house. For the remainder of the turn each friendly creature of that house may fight."
    traits = False
    amber = 1
    power = 0
    armor = 0
    rarity = "Rare"
    flavor = 0
    number = 4
    expansion = "CoA"
    is_maverick = False


#     id = 469dd68d-cdd6-40e0-8fc9-a167c45a9aea
#     title = Grasping Vines
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_324_VH9R4P26824V_en.png
#     text = Play: Return up to 3 artifacts to their owners’ hands.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 324
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1a84631d-7fcb-4c9a-a50c-9539dcb84928
#     title = Yxilo Bolter
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_204_H9HQ5F59FJQX_en.png
#     text = Fight/Reap: Deal 2<D> to a "Creature". If this damage destroys that "Creature" purge it.
#     traits = Martian • Soldier
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = ""Common""
#     flavor = 0
#     number = 204
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b8343462-b5d7-48b0-9e3b-f020c5e73c55
#     title = Tocsin
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_102_CG7PMM7PJ3G6_en.png
#     text = Reap: Your opponent discards a random card from their hand.
#     traits = Demon
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 102
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c08c91f0-043a-4a8a-8761-6080e9f46183
#     title = Titan Mechanic
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_154_M7WH2HV6J2FX_en.png
#     text = While Titan Mechanic is on a flank each key costs –1<A>.
#     traits = Cyborg • Scientist
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Common"
#     flavor = If they come they will build it. 
#     number = 154
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ce051448-1745-4606-95a0-e44e70401ba1
#     title = Foggify
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_110_4W42XPXRVP7V_en.png
#     text = Play: Your opponent cannot use "Creature"s to fight on their next turn.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 110
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 622f072b-bdab-412b-9da4-f59116940a95
#     title = Troop Call
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_337_WP75XF628MRC_en.png
#     text = Play: Return each friendly Niffle "Creature" from your discard pile and from play to your hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 337
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = aabeebf7-1da5-4149-afab-e7e221b47d93
#     title = Uxlyx the Zookeeper
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_201_69W23Q88QWW4_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: Put an enemy "Creature" into your archives. If that "Creature" leaves your archives it is put into its owner’s hand instead.
#     traits = Martian • Scientist
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 201
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 699f06e3-e47b-4910-90b9-c67fac157d6e
#     title = Dance of Doom
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_57_QR3X35J5GWCR_en.png
#     text = Play: Choose a number. Destroy each "Creature" with power equal to that number.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 57
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c7f70ade-d2e2-4032-a843-0fca6076d243
#     title = Grenade Snib
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_34_WJXC3F32R7CP_en.png
#     text = Destroyed: Your opponent loses 2<A>.
#     traits = Goblin
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 34
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 6bf5d9fa-1fbb-4609-8671-986a4709d3aa
#     title = Lifeward
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_77_46M5PVW2VRX9_en.png
#     text = Omni: Sacrifice Lifeward. Your opponent cannot play "Creature"s on their next turn.
#     traits = Power
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 77
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5aba3999-2489-4073-92be-cc0ec93ee65f
#     title = Lady Maxena
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_251_P4MXH8G4VPX4_en.png
#     text = Play: Stun a "Creature". \u000b"Action": Return Lady Maxena to its owner’s hand.
#     traits = Knight • Spirit
#     amber = 0
#     power = 5
#     armor = 2
#     rarity = "Uncommon"
#     flavor = 0
#     number = 251
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = afe27535-5cb7-43a1-8eab-ff9a6a472edb
#     title = Vigor
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_338_CR6PV8PPC85R_en.png
#     text = Play: Heal up to 3 damage from a "Creature". If you healed 3 damage gain 1<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 338
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c39567bb-4695-4518-8b8d-8ac882894d1e
#     title = Round Table
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_235_MJMGJPH3545P_en.png
#     text = Each friendly Knight "Creature" gets +1 power and gains taunt.
#     traits = Location
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “Come my friends let us ready for battle.” –King Godfrey Greywind
#     number = 235
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2f9f20aa-b110-4df8-8f4e-560a11f0ae49
#     title = Novu Archaeologist
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_147_X27M5CQW494F_en.png
#     text = "Action": Archive a card from your discard pile.
#     traits = Cyborg • Scientist
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “One civilization’s trash is... nope still trash.”
#     number = 147
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9095c1fe-1783-4b09-9d90-6164234a73aa
#     title = Shoulder Armor
#     house = Sanctum
#     typ = "Upgrade"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_266_F6GMMXCFJ9PC_en.png
#     text = While this "Creature" is on a flank it gets +2 armor and +2 power.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “I can’t see anything. Do I look cool?” 
#     number = 266
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a8b24d43-1940-4852-afcb-d034d99da55d
#     title = Protect the Weak
#     house = Sanctum
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_265_36392V5F286G_en.png
#     text = This "Creature" gets +1 armor and gains taunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 265
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5607fecd-b90e-4e12-84bc-cb36d079117c
#     title = Hysteria
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_65_HX7W9345R87F_en.png
#     text = Play: Return each "Creature" to its owner’s hand.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Help! I can’t stop this feeling!”
#     number = 65
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3056e60c-8f7c-40da-951c-6e0e9cfb9d46
#     title = Inspiration
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_220_J4PRQX77RXV8_en.png
#     text = Play: Ready and use a friendly "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “The Sanctum gives meaning to my life.” - Duma the Martyr
#     number = 220
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 459a6725-dcc0-4967-8cd4-a9bbb1548eda
#     title = Lost in the Woods
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_327_W6VV383R4X8P_en.png
#     text = Play: Choose 2 friendly "Creature"s and 2 enemy "Creature"s. Shuffle each chosen "Creature" into its owner’s deck.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 327
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f0c4cb0f-8e5f-454c-a6ad-35f35ac3c98a
#     title = Dew Faerie
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_350_6X8HWG4MJPCC_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: Gain 1<A>.
#     traits = Faerie
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 350
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = aa9b8dfe-3817-4f9d-b4c8-95c5c303c513
#     title = Effervescent Principle
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_109_9382CVHW3F7H_en.png
#     text = Play: Each player loses half their <A> (rounding down the loss). Gain 1 chain.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 109
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 19b74b4e-bec8-4fbb-bd35-cb635f500249
#     title = Soft Landing
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_177_F3R3FCFQQQG8_en.png
#     text = Play: The next "Creature" or artifact you play this turn enters play ready.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Any landing you walk away from…
#     number = 177
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b97236a0-5a0e-437b-b3be-d13834c0dc2d
#     title = Tireless Crocag
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_47_QHVVFWHGJM8R_en.png
#     text = Tireless Crocag cannot reap.\u000bYou may use Tireless Crocag as if it belonged to the active house.\u000bIf your opponent has no "Creature"s in play destroy Tireless Crocag.
#     traits = "Giant"
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 47
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d42dd1d0-3462-410f-b683-dd0768b84188
#     title = Hand of Dis
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_62_8WF3JF84X9VM_en.png
#     text = Play: Destroy a "Creature" that is not on a flank.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Let me give you a hand...”
#     number = 62
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8717beaa-79ff-44ba-b4e1-700235535844
#     title = Soul Snatcher
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_80_79QFRXPXVQ33_en.png
#     text = Each time a "Creature" is destroyed its owner gains 1<A>.
#     traits = Vehicle
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = No one goes in no one comes out. And yet the fires burn.
#     number = 80
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f75dda7d-680c-4bd5-8813-d04646857753
#     title = Red Planet Ray Gun
#     house = Mars
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_211_PQFJWQ3VVVGJ_en.png
#     text = This "Creature" gains “Reap: Choose a "Creature". Deal 1<D> to that "Creature" for each Mars "Creature" in play.”
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 211
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 64f0e039-dd33-49f0-8e9c-42ec38aba8a1
#     title = Skeleton Key
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_291_7FCVJGVJQF96_en.png
#     text = "Action": A friendly "Creature" captures 1<A>.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Skeleton sold separately. 
#     number = 291
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 57bccc52-b6a1-4d11-b9d9-6356d8ac279c
#     title = Mother
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_145_65HF32HQGF2G_en.png
#     text = During your “draw cards” step refill your hand to 1 additional card.
#     traits = Robot • Scientist
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “Of course she’s necessary she’s the mother of all invention!”
#     number = 145
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 59cb3ad9-cc98-4fe5-8589-a8967d32af00
#     title = Library of Babble
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_129_WR7JW9MF9F2R_en.png
#     text = "Action": Draw a card.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = When you make an archive of all knowledge in the galaxy don’t be surprised when you understand almost none of it. 
#     number = 129
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1d17903e-5c7a-4882-833f-707ce03d1228
#     title = Curiosity
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_320_Q6Q7VG34P9GF_en.png
#     text = Play: Destroy each Scientist "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “It started with Schrödinger’s cat and just kept going from there.” – Quixo the “Adventurer”
#     number = 320
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 05fa104f-3719-41d0-9189-57ff3ec5edc1
#     title = Witch of the Eye
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_368_MC5PG9FQ3766_en.png
#     text = Reap: Return a card from your discard pile to your hand.
#     traits = Human • Witch
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “Waste not want not.”
#     number = 368
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = aeed12e9-7b9d-43f4-8bf7-04f076c3ea79
#     title = Psychic Network
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_174_Q59H8QWGHQCR_en.png
#     text = Play: Steal 1<A> for each friendly ready Mars "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 174
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 16168a85-bbfa-4e54-8c84-5ea02e2a7da1
#     title = Mating Season
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_170_6C5MPJVJ5G9R_en.png
#     text = Play: Shuffle each Mars "Creature" into its owner’s deck. Each player gains 1<A> for each "Creature" shuffled into their deck this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 170
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e5746977-89c3-4300-8125-c8fd776a020f
#     title = Sniffer
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_188_JXXCR37F52MR_en.png
#     text = "Action": For the remainder of the turn each "Creature" loses elusive.
#     traits = Ally
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = Even the Martians’ pets have a bone to pick with the other lifeforms on the Crucible.
#     number = 188
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 20c810de-ad56-49ad-a57c-7fe7262b3cda
#     title = Nepenthe Seed
#     house = Untamed
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_"CoA"_M3P5Q4RWG42_en.png
#     text = Omni: Sacrifice Nepenthe Seed. Return a card from your discard pile to your hand.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = "CoA"
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bda929e2-962a-438c-a210-47f21228dfbc
#     title = Mothergun
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_187_886VP3RR6C5F_en.png
#     text = "Action": Reveal any number of Mars cards from your hand. Deal damage to a "Creature" equal to the number of Mars cards revealed this way.
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 187
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c9625085-6eb2-4555-87cd-cda180af9f71
#     title = Pitlord
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_93_95PVMCCHQ7P2_en.png
#     text = Taunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)\u000bWhile Pitlord is in play you must choose Dis as your active house.
#     traits = Demon
#     amber = 2
#     power = 9
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 93
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ff5917ee-ddb9-42d1-8a2a-ecc8c1a6ab84
#     title = Dimension Door
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_108_XHW22F7FH9FM_en.png
#     text = Play: For the remainder of the turn any <A> you would gain from reaping is stolen from your opponent instead.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 108
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 87ebd58d-d08f-41f7-a3fd-67b476d13673
#     title = Mothership Support
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_171_C9HXR9JCPGP9_en.png
#     text = Play: For each friendly ready Mars "Creature" deal 2<D> to a "Creature". (You may choose a different "Creature" each time.)
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 171
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e40df662-6506-4a35-816d-efe29a0e4a6f
#     title = Sequis
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_257_WC74XH7M2MJW_en.png
#     text = Reap: Capture 1<A>.
#     traits = Human • Knight
#     amber = 0
#     power = 4
#     armor = 2
#     rarity = "Common"
#     flavor = “I follow the Æmber light of the Sanctum the light of truth and hope. What is it you follow?”
#     number = 257
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9779c7a8-419a-4c99-9460-a48ddf33b963
#     title = Champion Anaphiel
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_239_FR9V84W6X65C_en.png
#     text = Taunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)
#     traits = Knight • Spirit
#     amber = 0
#     power = 6
#     armor = 1
#     rarity = "Common"
#     flavor = “Steel thyself Knave. To harm them you must first defeat me.”
#     number = 239
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a8c4f41a-0d6b-4f0b-ac8f-27b2db518dce
#     title = Punch
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_12_8QF6VM4C23R9_en.png
#     text = Play: Deal 3<D> to a "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Three for flinching.
#     number = 12
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f04a582c-c50b-453e-afc8-9d459c46cc22
#     title = Nocturnal Maneuver
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_330_R4Q6P7M74J89_en.png
#     text = Play: Exhaust up to 3 "Creature"s.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Every world has its fearsome "Creature"s that thrive in the darkness and the Crucible has them all. 
#     number = 330
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c8ed04c1-d938-4d96-a284-6e0f6a2b116e
#     title = Teliga
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_366_F2PF3262P9XJ_en.png
#     text = Each time your opponent plays a "Creature" gain 1<A>.
#     traits = Human • Witch
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = “Don’t try to change the Crucible to suit your needs. Let it change you.”
#     number = 366
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ff290bf3-dd57-48b3-add3-c6baf605967c
#     title = Magda the Rat
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_303_JJPCRGJ7CFPW_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bPlay: Steal 2<A>.\u000bLeaves Play: Your opponent steals 2<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 303
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 27a6e4f0-4770-4ce0-89ff-8b2fd5a99f4a
#     title = Relentless Assault
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_13_967HJV9Q3J5P_en.png
#     text = Play: Ready and fight with up to 3 different friendly "Creature"s one at a time.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 13
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0b20bfe2-5664-4c1a-9e1a-22aa108d3786
#     title = Cleansing Wave
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_215_RFRWH2MX953_en.png
#     text = Play: Heal 1 damage from each "Creature". Gain 1<A> for each "Creature" healed this way.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 215
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 22c50a42-0b6e-4681-9632-3d315a76e849
#     title = Save the Pack
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_333_4J9WMP4Q2F2G_en.png
#     text = Play: Destroy each damaged "Creature". Gain 1 chain.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 333
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d6aae364-d547-49ec-83dd-be3ffbcb80c6
#     title = Ganymede Archivist
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_142_9RC9J993WM9F_en.png
#     text = Reap: Archive a card.
#     traits = Human • Scientist
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “They offered to let my crew stay with them. I politely declined.” –Captain Val Jericho
#     number = 142
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b361d7e2-6873-4890-8f87-702d9c89c5ad
#     title = Anger
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_1_7C854VPW72RH_en.png
#     text = Play: Ready and fight with a friendly "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Don’t make them angry you say? Heh. The "Brobnar" are born angry.” –Old Bruno
#     number = 1
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3e4d74e3-8080-402f-9444-b069ce4e56d7
#     title = Glorious Few
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_218_63PVJ7PJP3GP_en.png
#     text = Play: For each "Creature" your opponent controls in excess of you gain 1<A>.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 218
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 45bc71b4-3465-4917-a67f-f4928d22d795
#     title = Tendrils of Pain
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_64_WCMG558RP6QV_en.png
#     text = Play: Deal 1<D> to each "Creature". Deal an additional 3<D> to each "Creature" if your opponent forged a key on their previous turn.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 64
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2cb1f58c-5979-4d3a-ae86-9dadc6000288
#     title = Phase Shift
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_117_HP2M3PV8GPJ7_en.png
#     text = Play: You may play one non-Logos card this turn.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 117
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = dc18cfc1-9dd9-440d-93be-50c2c114b3c8
#     title = Spangler Box
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_132_XQ93M42M9FR5_en.png
#     text = "Action": Purge a "Creature" in play. If you do your opponent gains control of Spangler Box. If Spangler Box leaves play return to play all cards purged by Spangler Box.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 132
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 67ac26ce-b816-4ae1-9bea-9f38059f3b46
#     title = Longfused Mines
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_287_H6CGFG593XMM_en.png
#     text = Omni: Sacrifice Longfused Mines. Deal 3<D> to each enemy "Creature" not on a flank.
#     traits = Weapon
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 287
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a429a71c-e558-4ee6-af48-6326df3d4b0f
#     title = Library Access
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_115_4J2C745JC5V2_en.png
#     text = Play: For the remainder of the turn each time you play another card draw a card.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 115
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1838fbaa-a062-4593-acbe-53ecfadfb5cc
#     title = Labwork
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_114_X6V5QX33Q589_en.png
#     text = Play: Archive a card.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Attention to detail is the key to all progress.
#     number = 114
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f74c96d8-ccec-4201-af7c-755df49d0025
#     title = Jammer Pack
#     house = Mars
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_210_HCXQ277C22FW_en.png
#     text = This "Creature" gains “Your opponent's keys cost +2<A>.“
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “The humans make it. It’s called ‘moo-zak.’”
#     number = 210
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3515de43-9c9a-4ec8-bced-d2d21ff24824
#     title = Remote Access
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_120_V59VPJJ255WQ_en.png
#     text = Play: Use an opponent's artifact as if it were yours.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 120
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8023cf81-ac80-499e-b8bb-3bfa2511fd63
#     title = Red-Hot Armor
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_70_QXV6993G25X7_en.png
#     text = Play: Each enemy "Creature" with armor loses all of its armor until the end of the turn and is dealt 1<D> for each point of armor it lost this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 70
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 06ab14e9-ec4f-4f2d-908e-20940241590c
#     title = Krump
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_39_Q64CQC29J542_en.png
#     text = After an enemy "Creature" is destroyed fighting Krump its controller loses 1<A>.
#     traits = "Giant"
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 39
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a936b45d-5de6-4b43-889b-9c58f0ab4c35
#     title = Nerve Blast
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_276_833RV7MVFCH8_en.png
#     text = Play: Steal 1<A>. If you do deal 2<D> to a "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Don’t look so shocked to see me!”
#     number = 276
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = aa73a693-e1e6-4097-8010-ddc820cc6d96
#     title = Gongoozle
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_60_8J78GV8GV57Q_en.png
#     text = Play: Deal 3<D> to a "Creature". If it is not destroyed its owner discards a random card from their hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Just trying to understand these...’things’ gives me a headache.”
#     number = 60
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f5019c91-eea0-4883-9946-297bbf1c6822
#     title = Anomaly Exploiter
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_126_F66C7VF2HR8Q_en.png
#     text = "Action": Destroy a damaged "Creature".
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 126
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 6ae428ad-1ac3-4419-be83-7c7790b8fd96
#     title = Too Much to Protect
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_283_J93HJ73F4PMQ_en.png
#     text = Play: Steal all but 6 of your opponent’s <A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Not taking it would be the real crime.
#     number = 283
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5ad003a2-8572-4fbd-b9fb-a2e94e4bdc7c
#     title = Poltergeist
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_69_P2P8M5XWMHCW_en.png
#     text = Play: Use an artifact controlled by any player as if it were yours. Destroy that artifact.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 69
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 179f877a-9b59-46d6-a43e-15b4524af3c6
#     title = Ether Spider
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_192_P52JHFXR9X8X_en.png
#     text = Ether Spider deals no damage when fighting.\u000bEach <A> that would be added to your opponent’s pool is captured by Ether Spider instead.
#     traits = Beast
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 192
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c5ed37f7-0d05-48bc-a595-4f25c0ec1e6d
#     title = Charette
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_81_GM7WM322M4_en.png
#     text = Play: Capture 3<A>.
#     traits = Demon
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Common"
#     flavor = It doesn’t like to share.
#     number = 81
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 53f7d3ec-a65f-4b05-8c82-74f44a7bdc44
#     title = Research Smoko
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_151_XC9823CQ2V92_en.png
#     text = Destroyed: Archive the top card of your deck.
#     traits = Mutant
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 151
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 916f271b-9928-437c-bfc4-d60d32af8c7c
#     title = Ember Imp
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_85_C72X25358RG2_en.png
#     text = Your opponent cannot play more than 2 cards each turn.
#     traits = Imp
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 85
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d71c36b7-c4be-427a-8038-2033ba9bf07e
#     title = Commander Remiel
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_241_C472V3C68C9_en.png
#     text = Reap: Use a friendly non-Sanctum "Creature".
#     traits = Human • Knight
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “I was not always a knight. Perhaps someday you will stand where I stand and see what I see.” 
#     number = 241
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3f0f006a-10bc-4f1a-a90a-a64abb14d5a0
#     title = Lifeweb
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_326_X574G5FJP676_en.png
#     text = Play: If your opponent played 3 or more "Creature"s on their previous turn steal 2<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 326
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9c75188a-8cb2-4201-9f10-d13f6cd00255
#     title = Pawn Sacrifice
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_279_RJJJ2R3P5FHC_en.png
#     text = Play: Sacrifice a friendly "Creature". If you do deal 3<D> each to 2 "Creature"s.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Pawn to Queen’s Bishop four.
#     number = 279
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 79be4a3f-0f51-4cf7-a199-819244879eac
#     title = Custom Virus
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_183_3G89HPF6R2GX_en.png
#     text = Omni: Sacrifice Custom Virus. Purge a "Creature" from your hand. Destroy each "Creature" that shares a trait with the purged "Creature".
#     traits = Weapon
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 183
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 21d11426-7870-44ec-a16f-bf3724271d21
#     title = Begone!
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_212_W36G9HXF9RQ7_en.png
#     text = Play: Choose one: destroy each Dis "Creature" or gain 1<A>.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 212
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3d650fe4-817a-4922-ba0f-297c1ebf816d
#     title = Screechbomb
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_26_WGX3X54PQCMP_en.png
#     text = Omni: Sacrifice Screechbomb. Your opponent loses 2<A>.
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “I think that thing made me deaf!”\u000b“What? I can’t hear you! I think that thing made me deaf!” 
#     number = 26
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ba8d348b-5c05-44d1-88f1-3945f9a485d8
#     title = Old Bruno
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_307_7M48G5WCGGX9_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bPlay: Capture 3<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “I raise.”
#     number = 307
#     expansion = "CoA"
#     is_maverick = False
  

  
  
#     id = d2edea65-7c2f-487f-a6f4-f44a077c4a65
#     title = Control the Weak
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_55_7CJ4H2WMJWQ2_en.png
#     text = Play: Choose a house on your opponent’s identity card. Your opponent must choose that house as their active house on their next turn.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 55
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 448c1335-d45b-473e-b222-d71f31ba0292
#     title = Sloppy Labwork
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_123_R3C97J8JMPRV_en.png
#     text = Play: Archive a card. Discard a card.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Don’t fret the details. Progress happens when you least expect it.
#     number = 123
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1da26e11-d319-4980-a2c3-931054ff008c
#     title = Epic Quest
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_231_9CW6R752CCQG_en.png
#     text = Play: Archive each friendly Knight "Creature" in play.\u000bOmni: If you have played 7 or more Sanctum cards this turn sacrifice Epic Quest and forge a key at no cost.
#     traits = Quest
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 231
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 87197e65-0d83-42a8-bec9-9e0e1fb75f34
#     title = Gatekeeper
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_260_MJV7XGGFVMQC_en.png
#     text = Play: If your opponent has 7 or more <A> capture all but 5 of it.
#     traits = Knight • Spirit
#     amber = 0
#     power = 5
#     armor = 1
#     rarity = "Uncommon"
#     flavor = 0
#     number = 260
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e8276e78-a5f3-42c0-b030-a08e25137dc0
#     title = Fuzzy Gruen
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_353_5P9MP78G2R8Q_en.png
#     text = Play: Your opponent gains 1<A>.
#     traits = Beast
#     amber = 2
#     power = 5
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 353
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 52e685bc-df93-42b5-b8e6-bad9357c48da
#     title = Hypnotic Command
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_164_QCCQ9VXCQH7X_en.png
#     text = Play: For each friendly Mars "Creature" choose an enemy "Creature" to capture 1<A> from their own side.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 164
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 68fbba20-4516-4e8a-8d3d-47e2cb401032
#     title = Key Charge
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_325_66XVRV5PWMVG_en.png
#     text = Play: Lose 1<A>. If you do you may forge a key at current cost.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “You might call it madness but for all we know madness is a key ingredient.” –Inka the Spider
#     number = 325
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = df6e4b5b-9f0a-4bd5-808a-6ccd46d973c4
#     title = Chaos Portal
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_127_R2424CG64G8M_en.png
#     text = "Action": Choose a house. Reveal the top card of your deck. If it is of that house play it.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 127
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ea2a390e-e121-4cbd-96c5-2430cc600e81
#     title = Mind Barb
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_67_GJXV3PCXVPMW_en.png
#     text = Play: Your opponent discards a random card from their hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 67
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ac8fb9f6-ee8e-4434-85e8-d084a66c50db
#     title = Zorg
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_206_4XXWX9CP9XGJ_en.png
#     text = Zorg enters play stunned. \u000bBefore Fight: Stun the "Creature" Zorg fights and each of that "Creature"’s neighbors.
#     traits = Beast
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 206
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 22fdfc0f-5ea1-42bd-984a-8c9edd8b16b7
#     title = Hallowed Blaster
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_233_V3CVPF24W8MR_en.png
#     text = "Action": Heal 3 damage from a "Creature".
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Swords into plowshares is thinking too small.
#     number = 233
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 6f6b30f0-c2b5-4824-b836-b5f45ca5fb6d
#     title = Blypyp
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_190_8XHXRR6J7CH2_en.png
#     text = Reap: The next Mars "Creature" you play this turn enters play ready.
#     traits = Martian • Scientist
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Soooon…”
#     number = 190
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f26caba2-7ab6-477c-8a53-45e5fb666a90
#     title = Screaming Cave
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_79_WQCG263H8RWW_en.png
#     text = "Action": Shuffle your hand and discard pile into your deck.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = ”Was that you or the cave?” - Captain<nonbreak>Val<nonbreak>Jericho
#     number = 79
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 4e9e09ba-66b9-4fc8-a61d-ca2dad320a5c
#     title = Clear Mind
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_216_4CVXQJV2QG3P_en.png
#     text = Play: Unstun each friendly "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = Thy body is an illusion. Only thy spirit is eternal.
#     number = 216
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 37a73724-a6e5-457f-8fde-fa792efa18ab
#     title = Ozmo Martianologist
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_148_R25C9WHJ9V29_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bFight/Reap: Heal 3 damage from a Mars "Creature" or stun a Mars "Creature". 
#     traits = Human • Scientist
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 148
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3680b506-9a5c-4afb-956d-15b08d1e9ecc
#     title = Dust Pixie
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_351_PFJXP2G7VWVP_en.png
#     text = (Vanilla)
#     traits = Faerie
#     amber = 2
#     power = 1
#     armor = 0
#     rarity = "Common"
#     flavor = The faeries are believed to be created by the Architects to tend to the plants and animals of the Crucible. In the eons since their creation some have become…quirky.  
#     number = 351
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ceecd78b-f0bb-4de9-a3c6-dff6686be13d
#     title = Combat Pheromones
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_180_HQXG9V9X249X_en.png
#     text = Omni: Sacrifice Combat Pheromones. You may use up to 2 other Mars cards this turn.
#     traits = Item
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Don’t worry this will only sting a lot.”
#     number = 180
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 49183ec5-6dad-48fb-9d86-253db31d72cf
#     title = “John Smyth”
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_195_8VX38X5J32VV_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bFight/Reap: Ready a non-Agent Mars "Creature".
#     traits = Agent • Martian
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 195
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 466deee8-d9c0-4e08-af87-da5cbf80ce69
#     title = Brain Eater
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_137_F8PFV5JC764_en.png
#     text = After a "Creature" is destroyed fighting Brain Eater draw a card.
#     traits = Cyborg • Beast
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 137
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e5a1f190-6964-4b2e-bcb3-696d3f6f2713
#     title = Gabos Longarms
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_86_33RP646XMQ93_en.png
#     text = Before Fight: Choose a "Creature". Gabos Longarms deals damage to that "Creature" rather than the one it is fighting.
#     traits = Demon
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 86
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 22476b3c-d05c-4274-ad8f-ec1efabad116
#     title = Cannon
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_21_CRMGW6QVC5HC_en.png
#     text = "Action": Deal 2<D> to a "Creature".
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 21
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 575d4804-78ff-4afa-8d44-2507126af6da
#     title = Tunk
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_199_FW92QH6WPGCW_en.png
#     text = After you play another Mars "Creature" fully heal Tunk.
#     traits = Robot
#     amber = 0
#     power = 6
#     armor = 1
#     rarity = "Common"
#     flavor = “Who’s driving?” \u000b“I thought you were.”\u000b“Let’s…not tell the Elders.” 
#     number = 199
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ddd62eb0-4699-4fb0-9b63-43769186b509
#     title = Snufflegator
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_358_C2FM8V788JM5_en.png
#     text = Skirmish. (When you use this "Creature" to fight it is dealt no damage in return.)
#     traits = Beast
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Common"
#     flavor = “Well it’s a snufflegator ain’t it?” –Dodger
#     number = 358
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 652c4e38-c4fa-4e30-8f8d-036e95249529
#     title = Valdr
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_29_97VGG57XM738_en.png
#     text = Valdr deals +2<D> while attacking an enemy "Creature" on the flank.
#     traits = "Giant"
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Common"
#     flavor = “Gather that Æmber! And you’re welcome.”
#     number = 29
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bb0dc3dc-b591-447d-a181-1dc4907e3eaa
#     title = Troll
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_48_CPX86RFXW765_en.png
#     text = Reap: Troll heals 3 damage.
#     traits = "Giant"
#     amber = 0
#     power = 8
#     armor = 0
#     rarity = "Common"
#     flavor = Don’t feed it it’ll go away.
#     number = 48
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9ed7d241-1ca3-4a2a-b067-bb44776f7d4b
#     title = The Terror
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_101_9W755VJWMG92_en.png
#     text = Play: If your opponent has no <A> gain 2<A>.
#     traits = Demon • Knight
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “I once thought that these "Creature"s could be redeemed. Now I know better.” –Champion Anaphiel
#     number = 101
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2d5666d0-5a93-4f75-b5f4-5085e4ee9b0f
#     title = Squawker
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_178_7J9MG8W9F6GM_en.png
#     text = Play: Ready a Mars "Creature" or stun a non-Mars "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 178
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f6202f7a-e204-482c-91d6-e8d1f5117d28
#     title = Yxili Marauder
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_203_8JJ739HGPCPC_en.png
#     text = Yxili Marauder gets +1 power for each <A> on it.\u000bPlay: Capture 1<A> for each friendly ready Mars "Creature".
#     traits = Martian • Soldier
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 203
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0ef760a3-68b9-42a9-93fa-419ea171917b
#     title = Smith
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_14_CV3QCM67C9GM_en.png
#     text = Play: Gain 2<A> if you control more "Creature"s than your opponent.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 14
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 45cf7fd4-6f40-4ee7-89ff-6f11ed80377a
#     title = The Vaultkeeper
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_261_GRHXCM2HH6W2_en.png
#     text = Your <A> cannot be stolen.
#     traits = Knight • Spirit
#     amber = 0
#     power = 4
#     armor = 1
#     rarity = "Rare"
#     flavor = 0
#     number = 261
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8604d465-8154-4354-9b77-9d4ad7eb3a02
#     title = King of the Crag
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_38_VH6FGMM4HCH4_en.png
#     text = Each enemy "Brobnar" "Creature" gets –2 power.
#     traits = "Giant"
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Rare"
#     flavor = Overthrowing this king is an uphill battle. 
#     number = 38
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ccfd5033-ffd1-4d9a-b4be-2f9dc90095c8
#     title = Treasure Map
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_284_Q7HHRF75F97J_en.png
#     text = Play: If you have not played any other cards this turn gain 3<A>. For the remainder of the turn you cannot play cards.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 284
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c1494f7b-eb87-4c64-9405-871579af1f80
#     title = Guilty Hearts
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_61_HM8RPQWR5X46_en.png
#     text = Play: Destroy each "Creature" with any <A> on it.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = C’mon take it. You know you want to.
#     number = 61
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 116f4590-792e-4d5f-ab06-94dbf7ba85d3
#     title = Sergeant Zakiel
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_258_96FR2MX3FJWF_en.png
#     text = Play: You may ready and fight with a neighboring "Creature".
#     traits = Human • Knight
#     amber = 0
#     power = 4
#     armor = 1
#     rarity = "Common"
#     flavor = “Together!” 
#     number = 258
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ce019a46-29ac-4e54-a12e-ec9ad8e0d200
#     title = Gorm of Omm
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_232_9XQ8F9638GX2_en.png
#     text = Omni: Sacrifice Gorm of Omm. Destroy an artifact.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “An object no matter how sacred is just a thing.”
#     number = 232
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a8f25ae7-75f4-4768-94f0-87d62036516c
#     title = Umbra
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_314_VHG44C64WFXQ_en.png
#     text = Skirmish. (When you use this "Creature" to fight it is dealt no damage in return.)\u000bFight: Steal 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = “When the fightin’s done the real work begins.” 
#     number = 314
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 740e0810-14e8-4278-bb44-e2e5c98184f9
#     title = Halacor
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_355_XCPG4GRFR6PR_en.png
#     text = Each friendly flank "Creature" gains skirmish. (When you use a "Creature" with skirmish to fight it is dealt no damage in return.)
#     traits = Beast
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Forget the others have you seen the teeth on that one?!”
#     number = 355
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 37f09612-6ebb-4374-b598-ad0614f2d729
#     title = Take Hostages
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_226_VMCJ79WHJVR2_en.png
#     text = Play: For the remainder of the turn each time a friendly "Creature" fights it captures 1<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 226
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 45d564a2-fcc9-4baa-8dc8-8e1a0fe2a37a
#     title = Dextre
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_138_WVWFRR3PMG3H_en.png
#     text = Play: Capture 1<A>.\u000bDestroyed: Put Dextre on top of your deck.
#     traits = Human • Scientist
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 138
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9c613507-63b6-447b-9df5-a72a5d62fdf3
#     title = Warsong
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_18_Q84XVC2GVCPR_en.png
#     text = Play: For the remainder of the turn gain 1<A> each time a friendly "Creature" fights.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 18
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 35983b27-9674-448e-b066-63b0c6067668
#     title = One Last Job
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_277_HGVF3P4J7PVJ_en.png
#     text = Play: Purge each friendly Shadows "Creature". Steal 1<A> for each "Creature" purged this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 277
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = be492d70-5c87-441e-8223-79fb2bce85c9
#     title = Gateway to Dis
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_59_WW6PQP2CGM8H_en.png
#     text = Play: Destroy each "Creature". Gain 3 chains.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 59
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3d6a02d0-b5c8-49be-93e4-dfdd5c1200eb
#     title = Guardian Demon
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_88_W95JX5C22HW7_en.png
#     text = Play/Fight/Reap: Heal up to 2 damage from a "Creature". Deal that amount of damage to another "Creature".
#     traits = Demon
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 88
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ba26515f-1705-45ba-ae42-dcb65685a0ec
#     title = Tentacus
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_100_WQWQX27FH7M2_en.png
#     text = Your opponent must pay you 1<A> in order to use an artifact.
#     traits = Demon
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 100
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 09101020-58c5-4d9f-b93b-7fb25d684ff0
#     title = Burn the Stockpile
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_5_7WCGR88265CM_en.png
#     text = Play: If your opponent has 7<A> or more they lose 4<A>.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “If you can’t protect it you don’t deserve it.” –Bilgum Avalanche
#     number = 5
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8e3d6aaf-e740-4924-86aa-57689c7cbdab
#     title = Rocket Boots
#     house = Logos
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_158_WMW7JV5QGXW6_en.png
#     text = This "Creature" gains “Fight/Reap: If this is the first time this "Creature" was used this turn ready it.”
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = ”Wheeeee!”
#     number = 158
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 89b647b4-74b1-4e74-9812-1581e088f32e
#     title = Terms of Redress
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_227_VC53Q7XQ4C33_en.png
#     text = Play: Choose a friendly "Creature" to capture 2<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Thou shalt wear pants.”
#     number = 227
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 60f095d7-1816-4f14-88ec-04412ebde43b
#     title = Veylan Analyst
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_156_4F6VP56RFQQ5_en.png
#     text = Each time you use an artifact gain 1<A>.
#     traits = Cyborg • Scientist
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Logos are divided into two camps: Theorists and Mechanists. Each believes themselves to be superior to the other. 
#     number = 156
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = eb91efae-9fbe-46e2-a6f4-f93d290703a9
#     title = Speed Sigil
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_293_6Q53JFFFWX8F_en.png
#     text = The first "Creature" played each turn enters play ready.
#     traits = Power
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 293
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3c4513a3-260e-441f-8abf-b27c1c4e23ef
#     title = Succubus
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_99_C63GPXC7XM83_en.png
#     text = During their “draw cards” step your opponent refills their hand to 1 less card.
#     traits = Demon
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 99
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = cd83ebe7-f961-4e5e-a00e-046d1be5e5d3
#     title = Psychic Bug
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_149_GW4755VJMRRP_en.png
#     text = Play/Reap: Look at your opponent’s hand.
#     traits = Cyborg • Insect
#     amber = 1
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = “I’d make more but I discovered lesser minds aren’t worth reading.” – Biologician Moreau
#     number = 149
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 05193f38-c59c-4cf1-92e9-87e69b3bb76e
#     title = Earthshaker
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_31_C7RGGJ9WG7XW_en.png
#     text = Play: Destroy each "Creature" with power 3 or lower.
#     traits = "Giant"
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Did you feel that?”
#     number = 31
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1983bc1e-a6e5-4fd4-b620-5e3d691c6851
#     title = The Spirit’s Way
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_229_J233WVWH3WPR_en.png
#     text = Play: Destroy each "Creature" with power 3 or higher.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “The spirit is eternal. The flesh is weak. Let go the flesh for your earthly strength is the greatest prison.” - The Last Book
#     number = 229
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1ca5f524-5a24-4a58-aacf-8204bdb46a32
#     title = Neuro Syphon
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_116_CW34G484FFRV_en.png
#     text = Play: If your opponent has more <A> than you steal 1<A> and draw a card.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 116
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 40587911-1857-4947-87e7-867cfd7fbab4
#     title = Shadow Self
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_310_C33C4J4W6726_en.png
#     text = Shadow Self deals no damage when fighting.  \u000bDamage dealt to non-Specter neighbors is dealt to Shadow Self instead.
#     traits = Specter
#     amber = 0
#     power = 9
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 310
#     expansion = "CoA"
#     is_maverick = true
  
  
#     id = d5aabe84-2155-4e26-96bc-67e1cbaa1b9d
#     title = Witch of the Wilds
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_347_44X322787G78_en.png
#     text = During each turn in which Untamed is not your active house you may play one Untamed card.
#     traits = Beast • Witch
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 347
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3d3f65df-f6f5-44e3-979c-c9b3fda94ddd
#     title = Booby Trap
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_268_6P3M73RFGR8W_en.png
#     text = Play: Deal 4<D> to a "Creature" that is not on a flank with 2<D> splash.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 268
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 253588cf-4fd5-4022-9c5c-a2b3693e21f0
#     title = Poison Wave
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_280_3W4H8F78V4FG_en.png
#     text = Play: Deal 2<D> to each "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Totally Tubular!” – Quixo the “Adventurer”
#     number = 280
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f65fea34-6c03-4d02-8434-02192dba72be
#     title = Briar Grubbling
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_348_X9R7J6J64H38_en.png
#     text = Hazardous 5. (Before this "Creature" is attacked deal 5<D> to the attacking enemy.)
#     traits = Beast • Insect
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = Nature says “do not touch” in so many creative ways. 
#     number = 348
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f14abd8e-6732-4afe-8679-c1059fc31edf
#     title = Twin Bolt Emission
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_124_636R5683G3F_en.png
#     text = Play: Deal 2<D> to a "Creature" and deal 2<D> to a different "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 124
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 23099339-dbe2-4b35-b26b-9dfb4c0fb35a
#     title = Mack the Knife
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_302_RP49F4QFW3FM_en.png
#     text = Elusive.\u000bYou may use Mack the Knife as if it belonged to the active house.\u000b"Action": Deal 1<D> to a "Creature". If this damage destroys that "Creature" gain 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 302
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c0ab6f27-619e-4b17-a623-c70f4cd84026
#     title = Nature’s Call
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_329_387QVR6XM2M3_en.png
#     text = Play: Return up to 3 "Creature"s to their owners’ hands.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Gotta go gotta go gotta go...”
#     number = 329
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 429e5d71-40bc-4ff4-ae81-4d5c0c10d15e
#     title = Dodger
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_308_4VWXF7969J9H_en.png
#     text = Fight: Steal 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “What did you do Tiny?” –Valdr
#     number = 308
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ac834ffc-01d5-4f35-8efe-982a746bdf3d
#     title = Total Recall
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_179_69V9P82V8QCF_en.png
#     text = Play: For each friendly ready "Creature" gain 1<A>. Return each friendly "Creature" to your hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 179
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 78f1a306-5e1d-4155-90d4-a4f0646c5c4c
#     title = Bigtwig
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_346_GFJP96HGWG24_en.png
#     text = Bigtwig can only fight stunned "Creature"s. \u000bReap: Stun and exhaust a "Creature".
#     traits = Beast
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 346
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b68e10b3-275e-46b8-8227-fe02984ff525
#     title = Replicator
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_150_8QGJM4R2RQQW_en.png
#     text = Reap: Trigger the reap effect of another "Creature" in play as if you controlled that "Creature". (That "Creature" does not exhaust.)
#     traits = Mutant
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 150
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 10715fd2-031a-47ca-9119-9b7b2ec1d2c0
#     title = Fear
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_58_7RV7CX53R83P_en.png
#     text = Play: Return an enemy "Creature" to its owner’s hand.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 58
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2d0d0224-b954-47df-9bed-9161a7742815
#     title = Library of the Damned
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_76_QR2M3J84P2GX_en.png
#     text = "Action": Archive a card.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = ”This place takes the idea of losing yourself in a book to a whole new level.” – Doc Bookton
#     number = 76
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 62c1aa96-491a-4dbe-a5a3-6895d55e2311
#     title = Key Hammer
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_66_RR9GCHVXP44C_en.png
#     text = Play: If your opponent forged a key on their previous turn unforge it. Your opponent gains 6<A>. 
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = What time is it?
#     number = 66
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 39f255c4-2ca4-4e7e-ba44-88ac0fcaeb1b
#     title = Pit Demon
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_92_CRW34FMH3JF2_en.png
#     text = "Action": Steal 1<A>.
#     traits = Demon
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “They come from another world they are pure evil made flesh and steel and they lurk in the darkest corners of the land. Yes I’m comfortable calling them ‘demons.’” –Science Officer Wu
#     number = 92
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8bd62dbc-77ac-400d-a31a-ca2e9c57728e
#     title = Sample Collection
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_175_6FF5HPJG5FFV_en.png
#     text = Play: Put an enemy "Creature" into your archives for each key your opponent has forged. If any of these "Creature"s leave your archives they are put into their owner’s hand instead.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 175
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e52d5652-7365-4644-8b7f-e929035ca2c5
#     title = "Giant" Sloth
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_354_9QP6FJMQC6W8_en.png
#     text = You cannot use this card unless you have discarded an Untamed card from your hand this turn.\u000b"Action": Gain 3<A>.
#     traits = Beast
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 354
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 953bbe23-df2b-4459-a3f6-beca7cd49a34
#     title = Wild Wormhole
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_125_H2RWQ5VF7V7_en.png
#     text = Play: Play the top card of your deck.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “But if we ever do recover the dataprobe think of what we will learn!” 
#     number = 125
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 7402a14d-d397-4a4c-9415-b84e231e0aa6
#     title = One Stood Against Many
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_223_PHQJHJ4P73J2_en.png
#     text = Play: Ready and fight with a friendly "Creature" 3 times each time against a different enemy "Creature". Resolve these fights one at a time.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 223
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bc22a9d4-8d8d-4c56-a879-262b68d6704a
#     title = Skippy Timehog
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_152_3PXCFH529CPG_en.png
#     text = Play: Your opponent cannot use any cards next turn. (Cards can still be played and discarded.)
#     traits = Mutant
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 152
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c225caa0-5e29-4b7d-8b89-aa7cbf3f4b14
#     title = Drumble
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_82_HVV8PJ352J78_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bPlay: If your opponent has 7<A> or more capture all of it.
#     traits = Imp
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 82
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 753bfb51-4ba7-4c0a-b141-a5b6388498c0
#     title = Battle Fleet
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_161_FPHCPHPMX8W8_en.png
#     text = Play: Reveal any number of Mars cards from your hand. For each card revealed this way draw 1 card.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 161
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c88c632e-743e-4f81-a9de-f61cddcbcaf5
#     title = Virtuous Works
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_230_848RC8PR567J_en.png
#     text = (Vanilla)
#     traits = False
#     amber = 3
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = On the Crucible there is no sanctimony. There is only Sanctumony.
#     number = 230
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9300339c-18a0-43f2-93cc-1937cfafb17b
#     title = Irradiated Æmber
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_165_V5XGG2973F82_en.png
#     text = Play: If your opponent has 6<A> or more deal 3<D> to each enemy "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “They poisoned Mars. We must not let them do the same here.” –Eldest Bear
#     number = 165
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1283215c-3ea2-4d2b-9af4-452d7c0d57d9
#     title = Scrambler Storm
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_122_HRQG3433R5R4_en.png
#     text = Play: Your opponent cannot play "Action" cards on their next turn.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 122
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9152cbad-d83f-4ee4-9846-87cc60d185f1
#     title = Snudge
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_97_RM5XHC9QXGC5_en.png
#     text = Fight/Reap: Return an artifact or flank "Creature" to its owner’s hand.
#     traits = Demon
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Uncommon"
#     flavor = It’s only sensible to fear the dark. 
#     number = 97
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 189c881e-f5bc-4d2d-b97e-3166980aa1c9
#     title = Special Delivery
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_292_C98PWPG7H4FC_en.png
#     text = Omni: Sacrifice Special Delivery. Deal 3<D> to a flank "Creature". If this damage destroys that "Creature" purge it.
#     traits = Item
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 292
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ef8b73a1-7655-4ab9-8da2-16db83836135
#     title = Sigil of Brotherhood
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_236_VWG6GMX929C6_en.png
#     text = Omni: Sacrifice Sigil of Brotherhood. For the remainder of the turn you may use friendly Sanctum "Creature"s.
#     traits = Power
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 236
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 42fcdd0d-9be6-4602-ae47-1e8ef088751b
#     title = Bulwark
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_238_4GJR4VPM7M26_en.png
#     text = Each of Bulwark’s neighbors gets +2 armor.
#     traits = Human • Knight
#     amber = 0
#     power = 4
#     armor = 2
#     rarity = "Common"
#     flavor = “Let me be thy shield.”
#     number = 238
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d792387f-8392-49b3-ad7c-ccaf7552256f
#     title = Hebe the Huge
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_36_73MRHJRCWXP4_en.png
#     text = Play: Deal 2<D> to each other undamaged "Creature".
#     traits = "Giant" • Knight
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Uncommon"
#     flavor = He’s much bigger in person. 
#     number = 36
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1ad71526-2782-4e56-a7b9-a0579fd63688
#     title = Loot the Bodies
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_10_48CVW9F66MJ8_en.png
#     text = Play: For the remainder of the turn gain 1<A> each time an enemy "Creature" is destroyed.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Loot the Bodies! Hit the Floor! Loot the Bodies! Hit the Floor!” –"Brobnar" War Chant
#     number = 10
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5a521238-f524-48e3-b121-40c16e1f7610
#     title = Doc Bookton
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_139_678M74P9FW66_en.png
#     text = Reap: Draw a card.
#     traits = Human • Scientist
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “Don’t worry Momo. We’ll have this quantum death ray installed in no time.”
#     number = 139
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b13b68ab-489c-47bc-803e-e87792edb931
#     title = Spectral Tunneler
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_133_FJGQFR6XJPHQ_en.png
#     text = "Action": Choose a "Creature". For the remainder of the turn that "Creature" is considered a flank "Creature" and gains “Reap: Draw a card.”
#     traits = Item
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 133
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = cc44ca9a-6994-4897-9308-ff332cc8de57
#     title = Phosphorus Stars
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_173_H5C875HQR3RC_en.png
#     text = Play: Stun each non-Mars "Creature". Gain 2 chains.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Martians love da smell of dis spice but it reminds me of Old Bruno’s feet.” - Dodger
#     number = 173
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 15f1a6f4-873f-4fa9-a080-7f01e72bbff1
#     title = Relentless Whispers
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_281_MPVFFW3882CJ_en.png
#     text = Play: Deal 2<D> to a "Creature". If this damage destroys that "Creature" steal 1<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 281
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1691e035-1eab-41de-ad18-26245265e64f
#     title = EMP Blast
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_163_HWF789XR9CMR_en.png
#     text = Play: Each Mars "Creature" and each Robot "Creature" is stunned. Each artifact is destroyed.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 163
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0cc7c1ea-5196-40ff-b408-f31997c8ab4d
#     title = Crystal Hive
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_182_QC7VW6G544RQ_en.png
#     text = "Action": For the remainder of the turn gain 1<A> each time a "Creature" reaps.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Behold the glory of Nova Hellas!
#     number = 182
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bbd788cd-1f8d-4950-a7c1-bc7fe5c0d49a
#     title = Oubliette
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_278_Q96GRFMV34CP_en.png
#     text = Play: Purge a "Creature" with power 3 or lower.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “I forgot we had this down here!”
#     number = 278
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = cda55db6-24e5-4e79-ac36-28482898dd4f
#     title = Grey Monk
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_244_4V54R77GCW9M_en.png
#     text = Each friendly "Creature" gets +1 armor. \u000bReap: Heal 2 damage from a "Creature".
#     traits = Human • Priest
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 244
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 551a951f-39cc-4f13-8070-c0758066769c
#     title = Subtle Maul
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_294_VJXHQQVX3C86_en.png
#     text = "Action": Your opponent discards a random card from their hand.
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 294
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f7104dfc-2f68-4ed5-aa4d-5d8d73960066
#     title = Hecatomb
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_63_4HRPQ25HC9QR_en.png
#     text = Play: Destroy each Dis "Creature". Each player gains 1<A> for each "Creature" they controlled that was destroyed this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 63
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9548d84e-2788-48d1-ba57-a54de15b289e
#     title = Armageddon Cloak
#     house = Sanctum
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_263_8WXW4FJ283XW_en.png
#     text = This "Creature" gains hazardous 2 and “Destroyed: Fully heal this "Creature" and destroy Armageddon Cloak instead.”
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 263
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = afa69425-4fe4-4e5b-a016-7c142ed0a849
#     title = Seeker Needle
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_290_PQP9MHRG7W4H_en.png
#     text = "Action": Deal 1<D> to a "Creature". If this damage destroys that "Creature" gain 1<A>.
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “What was that?”
#     number = 290
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 35bacc2e-48d6-4dac-a11c-5986e7416ddc
#     title = Key of Darkness
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_273_VHRR6QWG3C3_en.png
#     text = Play: Forge a key at +6<A> current cost. If your opponent has no <A> forge a key at +2<A> current cost instead.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 273
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3c5c1881-486c-4911-a3ce-497ef258e8ba
#     title = Batdrone
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_136_82MF23JH58M3_en.png
#     text = Skirmish. (When you use this "Creature" to fight it is dealt no damage in return.)\u000bFight: Steal 1<A>.
#     traits = Robot
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = The worst part is the singing.
#     number = 136
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b45eaa7a-22cd-4cd1-96bd-a240b63bea9f
#     title = Staunch Knight
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_259_F6VVWM6QHCRR_en.png
#     text = Staunch Knight gets +2 power while it is on a flank.
#     traits = Human • Knight
#     amber = 0
#     power = 4
#     armor = 2
#     rarity = "Common"
#     flavor = 0
#     number = 259
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d438faa9-7920-437a-8d1c-682fade5d350
#     title = Coward’s End
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_7_CFRV9R6JG7P7_en.png
#     text = Play: Destroy each undamaged "Creature". Gain 3 chains.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 7
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3cd0e141-6115-4719-a09e-8e0867fe567c
#     title = Murmook
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_361_WHJM9F6QF2MF_en.png
#     text = Your opponent’s keys cost +1<A>.
#     traits = Beast
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “Look out for the pincers and don’t make it crabby. “ –Dr. Escotera
#     number = 361
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9a319f7f-62ac-46d2-9f1b-c8846e02589f
#     title = Key Abduction
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_166_FC5W5F2668JC_en.png
#     text = Play: Return each Mars "Creature" to its owner's hand. Then you may forge a key at +9<A> current cost reduced by 1<A> for each card in your hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 166
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5fc44836-83fd-4a10-af61-9168db728cc0
#     title = Mindwarper
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_196_QG3353H2HJFM_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000b"Action": Choose an enemy "Creature". It captures 1<A> from its own side.
#     traits = Martian • Scientist
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 196
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = cdcef2b8-b0ca-4401-a386-dd3ae43d3f23
#     title = Creeping Oblivion
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_56_4RHHVXPC3X35_en.png
#     text = Play: Purge up to 2 cards from a discard pile.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “As far as oblivions go it’s in my bottom three.” –Dr. Escotera
#     number = 56
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f96b20b3-df0e-4d43-a737-e7fa56ff690b
#     title = Full Moon
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_323_CMWHFWX8HM52_en.png
#     text = Play: For the remainder of the turn gain 1<A> each time you play a "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = ”Mathematically a moon orbiting the Crucible is impossible.”\u000b”Then what is that?!”
#     number = 323
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = cc7b8381-1418-45e5-b328-7c538fa73407
#     title = Ritual of Balance
#     house = Untamed
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_342_CCCJH6Q4C2GR_en.png
#     text = "Action": If your opponent has 6<A> or more steal 1<A>.
#     traits = Power
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Is balance a means to an end or an end in itself? 
#     number = 342
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 34f85c32-4654-4177-9b9f-50825a58239e
#     title = Mimicry
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_328_7H4999VX47XJ_en.png
#     text = When you play this card treat it as a copy of an "Action" card in your opponent’s discard pile.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = It is said that if you travel far enough across the Crucible you will eventually meet yourself.
#     number = 328
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 296dca38-e6d1-4eb3-9bdb-966e48ebedbf
#     title = Lomir Flamefist
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_40_MH3839C78779_en.png
#     text = Play: If your opponent has 7<A> or more they lose 2<A>.
#     traits = "Giant"
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “I thought his name would turn out to be... metaphorical.” – Quixo the “Adventurer”
#     number = 40
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 22f59906-7f34-43e9-8285-836765e2c418
#     title = Way of the Wolf
#     house = Untamed
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_370_J935FXX4XCJW_en.png
#     text = This "Creature" gains skirmish.  (When you use this "Creature" to fight it is dealt no damage in return.)
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 370
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f05fadd1-0c4e-4242-9386-c5c6d112e124
#     title = Biomatrix Backup
#     house = Mars
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_208_77VHC8FXXP27_en.png
#     text = This "Creature" gains “Destroyed: You may put this "Creature" into its owner's archives.” 
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 208
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bdbb4933-b2f1-403b-986d-bbdec111b76b
#     title = Commpod
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_181_MXX6XH3QQRCV_en.png
#     text = "Action": Reveal any number of Mars cards from your hand. For each card revealed this way you may ready one Mars "Creature".
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 181
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 56252b23-94a4-46ac-a566-be6793ecbdfe
#     title = Blinding Light
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_213_P3Q4X37QMP7V_en.png
#     text = Play: Choose a house. Stun each "Creature" of that house.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 213
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 4a996715-f2c1-46e5-b80e-f285c1d36439
#     title = Bad Penny
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_296_QF774F23G6MR_en.png
#     text = Destroyed: Return Bad Penny to your hand.
#     traits = Human • Thief
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Common"
#     flavor = A Bad Penny saved is a Bad Penny earned.
#     number = 296
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 74422031-b763-4f04-9f90-3f580ad69d3f
#     title = Silvertooth
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_311_69G639M8F4F2_en.png
#     text = Silvertooth enters play ready.
#     traits = Elf • Thief
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = If you see teeth gleaming in the dark it’s already too late.
#     number = 311
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0e5e8a55-ab05-44be-8637-8362974dad8b
#     title = Grabber Jammer
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_193_PXQ9229CMHHP_en.png
#     text = Your opponent’s keys cost +1<A>.\u000bFight/Reap: Capture 1<A>.
#     traits = Robot
#     amber = 0
#     power = 4
#     armor = 1
#     rarity = "Common"
#     flavor = “Mine!”
#     number = 193
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9ba24b81-1887-46fd-9ec4-d8851af7e574
#     title = Pandemonium
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_68_52H2XVR2J45G_en.png
#     text = Play: Each undamaged "Creature" captures 1<A> from its opponent. 
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 68
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d4f666db-302f-43d0-b0af-bd03071f92ce
#     title = Ganger Chieftain
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_33_FGH2M9G9W45J_en.png
#     text = Play: You may ready and fight with a neighboring "Creature".
#     traits = "Giant"
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = It takes two to fight but more is better. 
#     number = 33
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 211c5213-7838-4292-b9c4-fb3a663898ee
#     title = Yxilx Dominator
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_205_GPCHG3XCV2MV_en.png
#     text = Taunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)\u000bYxilx Dominator enters play stunned. 
#     traits = Robot
#     amber = 0
#     power = 9
#     armor = 1
#     rarity = "Common"
#     flavor = Core power online. Stand by for domination. 
#     number = 205
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c5f7e033-f62e-442e-97a1-b23b47cde1e8
#     title = Lights Out
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_274_P4W2FF886X6V_en.png
#     text = Play: Return 2 enemy "Creature"s to their owner’s hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 274
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2ec5cbf6-3c41-41ef-9cb7-33a0601fd607
#     title = Quixo the “Adventurer”
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_144_7XJ66GGGX9P3_en.png
#     text = Skirmish. (When you use this "Creature" to fight it is dealt no damage in return.)\u000bFight: Draw a card.
#     traits = Human • Scientist
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “...I’ll leave this part out of the memoir.”
#     number = 144
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 817edf75-e91d-4b18-8c5a-d33e3759aeae
#     title = Shooler
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_96_4J8576237M3X_en.png
#     text = Play: If your opponent has 4<A> or more steal 1<A>.
#     traits = Demon
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “Demons only take never give.” - The Sanctified Scroll
#     number = 96
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f79ad4c9-4c3c-461c-b0e7-c949bb46d270
#     title = Blood of Titans
#     house = "Brobnar"
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_50_3GJFRPFVMF7M_en.png
#     text = This "Creature" gets +5 power.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Blood of "Giant"s? Why stop there?”  –Pingle Who Annoys
#     number = 50
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 02c7533e-98ac-48a0-94e4-621555443c8d
#     title = Whispering Reliquary
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_237_MMHF7CR6FMJ2_en.png
#     text = "Action": Return an artifact to its owner's hand.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 237
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = df4257dc-ac9c-40cf-ba1b-a77fffe960df
#     title = Duskrunner
#     house = Shadows
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_316_P6MMX3WR7MC6_en.png
#     text = This "Creature" gains “Reap: Steal 1<A>.” 
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Call me Night-Haunter and Duskrunner call me Who-Goes-There? and Just-The-Wind.” –‘The First Thief’ a Shadows children’s tale 
#     number = 316
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 98fca3bb-b74c-4563-876b-7c9e942e8254
#     title = Cooperative Hunting
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_319_75P9X98FJQHV_en.png
#     text = Play: Deal 1<D> for each friendly "Creature" in play. You may divide this damage among any number of "Creature"s.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “It sure beats uncooperative hunting!”
#     number = 319
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e1312fbf-c297-4d9f-b403-2d892271de62
#     title = Smaaash
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_46_MXF2PV92XQPW_en.png
#     text = Play: Stun a "Creature".
#     traits = "Giant"
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “I’m not sure he knows any other words.” 
#     number = 46
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 365b2432-0b7f-4f67-9fa6-e4b726de5c4e
#     title = Flame-Wreathed
#     house = Dis
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_106_4G49CMC5XCX4_en.png
#     text = This "Creature" gets +2 power and gains hazardous 2. (Before this "Creature" is attacked deal 2<D> to the attacking enemy.)
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 106
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0bd7cbf7-7d34-4a45-9049-217146229968
#     title = Orbital Bombardment
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_172_4CX23PH9H69J_en.png
#     text = Play: Reveal any number of Mars cards from your hand. For each card revealed this way deal 2<D> to a "Creature". (You may choose a different "Creature" each time.)
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 172
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 17e9dbd4-53cb-4c75-bdad-48e1550ff1e7
#     title = Key to Dis
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_74_RP2JCG669GWQ_en.png
#     text = Omni: Sacrifice Key to Dis. Destroy each "Creature".
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 74
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bc5df4f6-a9db-4b05-8a65-6c51c01b7b3e
#     title = Smiling Ruth
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_312_V2H6733WRV33_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: If you forged a key this turn take control of an enemy flank "Creature".
#     traits = Elf • Thief
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 312
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3a0c1861-3d38-4167-b0c1-afaa9cbe5e50
#     title = Noddy the Thief
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_306_6374XF5G5XMR_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000b"Action": Steal 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 306
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 4149fd67-12db-4ef6-9718-135c66ffefd3
#     title = Sound the Horns
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_15_8HXH9WQ5P4V4_en.png
#     text = Play: Discard cards from the top of your deck until you either discard a "Brobnar" "Creature" or run out of cards. If you discarded a "Brobnar" "Creature" this way put it into your hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 15
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 74d1da3a-9d90-43ea-8ead-f7968c4d562d
#     title = Regrowth
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_332_R2GQWP4RXCM4_en.png
#     text = Play: Return a "Creature" from your discard pile to your hand.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Deep in the heart of every bear one can find...another bear.” -Dr. Escotera
#     number = 332
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2a6e3e67-3c67-48c8-8ff3-b16896b14550
#     title = Silent Dagger
#     house = Shadows
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_318_CGCC5XW8VF69_en.png
#     text = This "Creature" gains “Reap: Deal 4<D> to a flank "Creature".”
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 318
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 1ef96099-4703-4883-9c55-9102e829797a
#     title = Shield of Justice
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_225_8WXGHPQGX9V_en.png
#     text = Play: For the remainder of the turn each friendly "Creature" cannot be dealt damage.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 225
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a0f1146a-6df3-4568-8fb1-d6845615d833
#     title = Follow the Leader
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_8_4CGG6P6JQ44W_en.png
#     text = Play: For the remainder of the turn each friendly "Creature" may fight.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 8
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = e9aefff3-acef-41e3-8258-182588f2b24c
#     title = Unguarded Camp
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_17_64F73PR27H7P_en.png
#     text = Play: For each "Creature" you have in excess of your opponent a friendly "Creature" captures 1<A>. Each "Creature" cannot capture more than 1<A> this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 17
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8754c688-6d87-4372-bbec-349e4e4bdded
#     title = Hidden Stash
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_271_3CCM38JM8932_en.png
#     text = Play: Archive a card.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Now where did you put that...”
#     number = 271
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3a3783ea-b5c4-407d-b3c7-0003c562a9aa
#     title = Hunting Witch
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_367_54RJ37XJPQ2_en.png
#     text = Each time you play another "Creature" gain 1<A>.
#     traits = Human • Witch
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = “What is it? Is it food?”
#     number = 367
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 86db8510-2854-440b-8ee5-559855bb7d2c
#     title = Gauntlet of Command
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_22_5F6F47CPQM7J_en.png
#     text = "Action": Ready and fight with a friendly "Creature".
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “I said ‘take me to your leader’ and got a fist to the face.”  –Captain Val Jericho
#     number = 22
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 91292e0d-e49e-485f-b19d-f066b1ff388a
#     title = Macis Asp
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_301_5G45CCCH6W5J_en.png
#     text = Skirmish. (When you use this "Creature" to fight it is dealt no damage in return.)\u000bPoison. (Any damage dealt by this "Creature"’s power during a fight destroys the damaged "Creature".)
#     traits = Beast
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 301
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5a1ee413-4b39-467f-a0bf-e5935f1edf9b
#     title = Dr. Escotera
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_140_GGR9WQGX52CC_en.png
#     text = Play: Gain 1<A> for each forged key your opponent has.
#     traits = Cyborg • Scientist
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Common"
#     flavor = “Interesting re"Action" but what does it mean?”
#     number = 140
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 050b35ae-461a-4630-a8df-a60b2652fc2b
#     title = Wardrummer
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_49_3J962PMQJRJ6_en.png
#     text = Play: Return each other friendly "Brobnar" "Creature" to your hand.
#     traits = Goblin
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 49
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d837b336-ae38-405b-b9d3-fc8583c770a0
#     title = Fogbank
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_322_9RH25FHMC26H_en.png
#     text = Play: Your opponent cannot use "Creature"s to fight on their next turn.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 322
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bec84d69-68f0-456c-a7bd-9f1e94d55a22
#     title = Experimental Therapy
#     house = Logos
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_157_4FCPWQMVGPC_en.png
#     text = This "Creature" belongs to all houses.\u000bPlay: Stun and exhaust this "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “This is for our research so be honest. How do you feel?”
#     number = 157
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9644c85a-12a7-44ff-a8bb-877dddb46995
#     title = Three Fates
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_71_5P29489P6443_en.png
#     text = Play: Destroy the 3 most powerful "Creature"s. 
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Destitution. Dereliction. Defenestration.”
#     number = 71
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f5cbdafd-487d-453b-96bb-a09378d1359f
#     title = Charge!
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_214_X3RQF994MG6R_en.png
#     text = Play: For the remainder of the turn each "Creature" you play gains “Play: Deal 2<D> to an enemy "Creature".”
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 214
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 23a96d73-4eb2-4c45-9550-8207145eb587
#     title = Lash of Broken Dreams
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_75_5WF77V8WRRPP_en.png
#     text = "Action": Keys cost +3<A> during your opponent’s next turn.
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “At first I thought that nothing could harm an Archon.”  –Captain Val Jericho
#     number = 75
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 6b113c63-c8e0-4c52-9973-b94263d2bf0d
#     title = Stealer of Souls
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_98_JJGJFX44Q6GF_en.png
#     text = After an enemy "Creature" is destroyed fighting Stealer of Souls purge that "Creature" and gain 1<A>.
#     traits = Demon
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 98
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 30df482b-4066-4d11-b357-75abc4ead329
#     title = Ammonia Clouds
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_160_VQMVCX37C6XQ_en.png
#     text = Play: Deal 3<D> to each "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Partly cloudy with a chance of acid rain.
#     number = 160
#     expansion = "CoA"
#     is_maverick = true
  
  
#     id = fc3d397a-3a51-4963-940c-6b43221b7667
#     title = Bumpsy
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_30_X82H79CQ6XH6_en.png
#     text = Play: Your opponent loses 1<A>.
#     traits = "Giant"
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = Whatever he doesn’t like he breaks. He doesn’t like anything.
#     number = 30
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 11663693-8a10-4783-9f89-47f43c49bfa3
#     title = Shadow Self
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_310_C33C4J4W6726_en.png
#     text = Shadow Self deals no damage when fighting.  \u000bDamage dealt to non-Specter neighbors is dealt to Shadow Self instead.
#     traits = Specter
#     amber = 0
#     power = 9
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 310
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8c763540-bb69-47aa-be43-4a8ace89864c
#     title = Bouncing Deathquark
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_107_X3G2GX9QW86R_en.png
#     text = Play: Destroy an enemy "Creature" and a friendly "Creature". You may repeat this effect as many times as you like as long as it is possible to repeat the entire effect.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 107
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = eec2bfbf-d019-4a7f-a0fa-2b8c8f16cd8d
#     title = Lord Golgotha
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_252_VXMWR7MR5CW9_en.png
#     text = Before Fight: Deal 3<D> to each neighbor of the "Creature" Lord Golgotha fights.
#     traits = Knight • Spirit
#     amber = 0
#     power = 5
#     armor = 2
#     rarity = "Rare"
#     flavor = “Enlightened” does not mean “peaceful.”
#     number = 252
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = dc0ba4ea-6f6e-475f-899c-88ad45ccae94
#     title = Niffle Ape
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_363_3RCHH4F7H4XF_en.png
#     text = While Niffle Ape is attacking ignore taunt and elusive.
#     traits = Beast • Niffle
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “Did it just say Niffle?” –Captain Val Jericho
#     number = 363
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 3b1f7db9-1c5a-4e15-a771-a4a45bd8fb0e
#     title = Mooncurser
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_304_3QMPPH48XHXJ_en.png
#     text = Skirmish. Poison.\u000bFight: Steal 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Uncommon"
#     flavor = Dark of night thieves’ delight.
#     number = 304
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 78f28f49-8edb-4333-bd22-308a229f200f
#     title = Imperial Traitor
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_272_9W52QM6RM94X_en.png
#     text = Play: Look at your opponent’s hand. You may choose and purge a Sanctum card in it.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 272
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 63f67670-16fb-4381-a859-c47920a847a6
#     title = The Warchest
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_27_5G98X8WW3V6G_en.png
#     text = "Action": Gain 1<A> for each enemy "Creature" that was destroyed in a fight this turn.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = It doesn’t matter what the treasure is only how it was won.
#     number = 27
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 03c4165e-a0bb-4fd5-b6a8-e3d9aec0551e
#     title = Urchin
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_315_7MCP67W84FWX_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bPlay: Steal 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 315
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 762973ae-27da-448f-93f4-2a9bc4ef5f35
#     title = Protectrix
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_254_W9QVJ9XWF94R_en.png
#     text = Reap: You may fully heal a "Creature". If you do that "Creature" cannot be dealt damage for the remainder of the turn.
#     traits = Knight • Spirit
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 254
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0c3231e1-1230-4e7d-890e-6d3149125de2
#     title = Headhunter
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_35_M3H9MVCF63W7_en.png
#     text = Fight: Gain 1<A>.
#     traits = "Giant"
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = “I mean I think it’s a head...”
#     number = 35
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f2c71c05-7a23-4465-8a89-82ab8e258a68
#     title = Rogue Ogre
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_45_HWPQ963W848R_en.png
#     text = At the end of your turn if you played exactly one card this turn Rogue Ogre heals 2 damage and captures 1<A>.
#     traits = "Giant" • Mutant
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Rare"
#     flavor = “I like to think of it as a Roguere.” –Dodger
#     number = 45
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9b079369-608a-430a-9b08-9f2d6b32435b
#     title = Ammonia Clouds
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_160_VQMVCX37C6XQ_en.png
#     text = Play: Deal 3<D> to each "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = Partly cloudy with a chance of acid rain.
#     number = 160
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a8e3dfc2-6cf2-42a2-97d3-99592ae7da9a
#     title = Honorable Claim
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_219_P9V3P7F8849M_en.png
#     text = Play: Each friendly Knight "Creature" captures 1<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “As your spirit is holy so æmber which is the spirit of the earth is holy.” - The Sanctified Scroll
#     number = 219
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2dc8f61d-c691-4204-b2b5-5115790d0ba8
#     title = Inka the Spider
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_356_QW7GHMXR5HJ8_en.png
#     text = Poison. (Any damage dealt by this "Creature"’s power during a fight destroys the damaged "Creature".)\u000bPlay/Reap: Stun a "Creature".
#     traits = Beast
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = “Let me weave you a tale.”
#     number = 356
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = eaae7cd5-62bd-4438-aedb-8309974535df
#     title = Ulyq Megamouth
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_200_CM3V8FW8C2PG_en.png
#     text = Fight/Reap: Use a friendly non-Mars "Creature".
#     traits = Martian • Scientist
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = “GLORY BE TO MARS!” 
#     number = 200
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 7c60d913-803f-4b84-8e84-cf931d70659c
#     title = Pocket Universe
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_131_Q67W5PMV8768_en.png
#     text = You may spend <A> on Pocket Universe when forging keys.\u000b"Action": Move 1<A> from your pool to Pocket Universe.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 131
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ff104cf4-f99d-4021-a570-dd949e559e97
#     title = Zyzzix the Many
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_207_C938GRH2C993_en.png
#     text = Fight/Reap: You may reveal a "Creature" from your hand. If you do archive it and Zyzzix the Many gets three +1 power counters.
#     traits = Martian • Soldier
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 207
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f51e8ec0-ab0e-46a8-a5f5-680039d6e664
#     title = Interdimensional Graft
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_112_VWRCJXGG9J99_en.png
#     text = Play: If an opponent forges a key on their next turn they must give you their remaining <A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 112
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 29eafbc7-7fc5-4239-b2a7-8bc90df1fc0f
#     title = Firespitter
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_32_PVV2WC6R6QWP_en.png
#     text = Before Fight: Deal 1<D> to each enemy "Creature".
#     traits = "Giant"
#     amber = 0
#     power = 5
#     armor = 1
#     rarity = "Common"
#     flavor = Guess how he got that name.
#     number = 32
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 750a9323-9c07-4ae7-be5e-79367b4a2a8d
#     title = Annihilation Ritual 
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_72_H2HJ8R9HF5C_en.png
#     text = When a "Creature" would enter a discard pile from play it is purged instead.
#     traits = Power
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 72
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 36b15919-4938-4e83-b57e-ae3a6b83cbbd
#     title = Raiding Knight
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_255_HX7GPH8C78C2_en.png
#     text = Play: Capture 1<A>.
#     traits = Human • Knight
#     amber = 0
#     power = 4
#     armor = 2
#     rarity = "Common"
#     flavor = “Sacred Æmber is not meant for hands such as thine.” 
#     number = 255
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f6d5781c-83a4-4070-bf98-085e81063c26
#     title = Miasma
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_275_5HGPVQG4QF5H_en.png
#     text = Play: Your opponent skips the “forge a key” step on their next turn.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 275
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = dc6344a9-0486-4926-a820-d99eb2151c7f
#     title = Ancient Bear
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_345_V9F9WCXJ5VHR_en.png
#     text = Assault 2.(Before this "Creature" attacks deal 2<D> to the attacked enemy.)
#     traits = Beast
#     amber = 0
#     power = 5
#     armor = 0
#     rarity = "Common"
#     flavor = ”And when I say ‘bear’ I mean it in the loosest of terms.” – Quixo the “Adventurer”
#     number = 345
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d988a134-ff29-40f7-bac7-3fd49fe525f8
#     title = Nexus
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_305_7QJVVWFQJPHJ_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: Use an opponent’s artifact as if it were yours.
#     traits = Cyborg • Thief
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 305
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a8a3578c-7a61-4e15-90ac-483daf2aff16
#     title = Vezyma Thinkdrone
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_202_99C5PXMWC2M7_en.png
#     text = Reap: You may archive a friendly "Creature" or artifact from play.
#     traits = Martian • Scientist
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Common"
#     flavor = Nothing helps me think like wanton destruction.
#     number = 202
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f97316b0-75a4-45a4-8735-15e72cc1568c
#     title = Dust Imp
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_83_9V7X379WFV8V_en.png
#     text = Destroyed: Gain 2<A>.
#     traits = Imp
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = When the demon’s away the imps will play.
#     number = 83
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 23508e89-0431-45d1-9692-192c6dffeb5a
#     title = Ghostly Hand
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_270_5MJXHHP7VWWG_en.png
#     text = Play: If your opponent has exactly 1<A> steal it.
#     traits = False
#     amber = 2
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “I felt a little bad stealing from the Microputians but only a little.” – Noddy the Thief
#     number = 270
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a2d750fc-aea3-48a6-ba18-5358fff7148e
#     title = Francus
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_243_PFW5PH796X2W_en.png
#     text = After an enemy "Creature" is destroyed fighting Francus Francus captures 1<A>.
#     traits = Knight • Spirit
#     amber = 0
#     power = 6
#     armor = 1
#     rarity = "Uncommon"
#     flavor = 0
#     number = 243
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ab58367b-51db-4ba0-926e-e4d562f7e4bd
#     title = Hayyel the Merchant
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_245_7MHFM8Q84QMX_en.png
#     text = Each time you play an artifact gain 1<A>.
#     traits = Human • Merchant
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = “The Enlightened are above haggling. Me on the other hand…”
#     number = 245
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 892c0a68-5213-48b2-8883-2ac3c97ac83c
#     title = Arise!
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_54_F9GHFCWJ233R_en.png
#     text = Play: Choose a house. Return each "Creature" of that house from your discard pile to your hand. Gain 1 chain.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 54
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 261b851a-84eb-44a7-828d-6b7599fecaaf
#     title = Sanctum Guardian
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_256_43Q78X6H273_en.png
#     text = Taunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)\u000bFight/Reap: Swap Sanctum Guardian with another friendly "Creature" in your battleline.
#     traits = Knight • Spirit
#     amber = 0
#     power = 6
#     armor = 1
#     rarity = "Rare"
#     flavor = 0
#     number = 256
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0186f94c-68df-4d5c-9338-9e918affe313
#     title = Bait and Switch
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_267_VHQ67J5MWQV5_en.png
#     text = Play: If your opponent has more <A> than you steal 1<A>. Repeat this card's effect if your opponent still has more <A> than you.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “Heckuva deal.” – Old Bruno
#     number = 267
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 71274e08-79b6-469b-9426-8af07d582704
#     title = Carlo Phantom
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_298_5PGPFVJF9292_en.png
#     text = Elusive. Skirmish.\u000bEach time you play an artifact steal 1<A>.
#     traits = Elf • Thief
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Give me half a chance an’ I’ll steal the whole of it.”
#     number = 298
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 68e2188c-4002-43d4-9fe1-0262df26c33f
#     title = Tremor
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_16_HQJ525M2CVG9_en.png
#     text = Play: Stun a "Creature" and each of its neighbors.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 16
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 96548d93-b318-40e3-9f5c-3297c8070ebd
#     title = Dominator Bauble
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_73_QRQ93X7RG4J9_en.png
#     text = "Action": Use a friendly "Creature".
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “I know I shouldn’t’a nicked it but ‘twere so…shiny. –Noddy the Thief
#     number = 73
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 728fcd16-1625-48f6-8633-567b9d4b7a2f
#     title = The Howling Pit
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_135_GVHX66578HV5_en.png
#     text = During their “draw cards” step each player refills their hand to 1 additional card.
#     traits = Location
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 135
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c578fa39-fe35-4a9f-844e-113fc47dc6f2
#     title = Ritual of the Hunt
#     house = Untamed
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_343_MWRP2VMRJ7R7_en.png
#     text = Omni: Sacrifice Ritual of the Hunt. For the remainder of the turn you may use friendly Untamed "Creature"s.
#     traits = Power
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 343
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0cdeb7ca-3071-472f-829c-6dc6ec0824b2
#     title = Perilous Wild
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_331_QF7G64HGJ35G_en.png
#     text = Play: Destroy each elusive "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = The Architects took great pains to make the Crucible inhabitable for "Creature"s from worlds across the galaxy. But they didn’t make it safe. 
#     number = 331
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 6378dc4a-fdb8-4580-a85f-1b6bcd158615
#     title = Iron Obelisk
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_23_G489GRF3RCV2_en.png
#     text = Your opponent’s keys cost +1<A> for each friendly damaged "Brobnar" "Creature".
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 23
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = eef21950-66f9-4535-b126-34d634fe524d
#     title = Scout
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_334_W8RW3VC8V333_en.png
#     text = Play: For the remainder of the turn up to 2 friendly "Creature"s gain skirmish. Then fight with those "Creature"s one at a time.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 334
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 98c0c7b0-59b4-48f2-8144-39d1d47bec7d
#     title = Sacrificial Altar
#     house = Dis
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_78_Q7JWX2HW28FX_en.png
#     text = "Action": Purge a friendly Human "Creature" from play. If you do play a "Creature" from your discard pile.
#     traits = Location
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 78
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 013def76-9edc-495c-bc35-af6210192f6b
#     title = Lupo the Scarred
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_359_RX86WM6596MC_en.png
#     text = Skirmish. (When you use this "Creature" to fight it is dealt no damage in return.) \u000bPlay: Deal 2<D> to an enemy "Creature".
#     traits = Beast
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Rare"
#     flavor = “Nothing that big should be able to move that silently.”  –Lost Lukas Lawrence
#     number = 359
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 315b5cb9-b5a6-42af-9f32-a89079ab42cc
#     title = Way of the Bear
#     house = Untamed
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_369_3822X74RGM8F_en.png
#     text = This "Creature" gains assault 2. (Before this "Creature" attacks deal 2<D> to the attacked enemy.)
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 369
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f5ec01ee-17d0-49fe-8d42-92fffcbe9a27
#     title = Chota Hazri
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_349_CGCR6RQRM629_en.png
#     text = Play: Lose 1<A>. If you do you may forge a key at current cost.
#     traits = Human • Witch
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Plenty of machines in the wild. Some of ‘em’s even alive.” 
#     number = 349
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 12acf848-7838-4668-a2df-620e67e6d916
#     title = Mighty Javelin
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_24_CG2485CM5HV4_en.png
#     text = Omni: Sacrifice Mighty Javelin. Deal 4<D> to a "Creature".
#     traits = Weapon
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 24
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c69a4a22-7d34-4719-9d64-a0a691d60164
#     title = Kindrith Longshot
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_357_CJVF7978M9W3_en.png
#     text = Elusive. Skirmish.\u000bReap: Deal 2<D> to a "Creature".
#     traits = Human • Ranger
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 357
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 040b3c05-428a-47c9-afc9-6fc65905462f
#     title = Duma the Martyr
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_242_8X9FFJ5RC99F_en.png
#     text = Destroyed: Fully heal each other friendly "Creature" and draw 2 cards.
#     traits = Human
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = “Remember me.”  - Squire Duma at the Battle for the Gate of Hope.
#     number = 242
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 746fd4a8-ae4d-4a28-8834-655923558721
#     title = Grommid
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_194_J7HVR74PWP6W_en.png
#     text = You cannot play "Creature"s.  \u000bAfter an enemy "Creature" is destroyed fighting Grommid your opponent loses 1<A>.
#     traits = Beast
#     amber = 0
#     power = 10
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 194
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a7621926-1f0f-4d56-b2aa-15efdded15a9
#     title = Fertility Chant
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_321_43VFXWMHFR7M_en.png
#     text = Play: Your opponent gains 2<A>.
#     traits = False
#     amber = 4
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 321
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a18f4950-87cd-4ebc-9096-9e82df8c6e88
#     title = Mighty Lance
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_221_GHP2MR29293_en.png
#     text = Play: Deal 3<D> to a "Creature" and 3<D> to a neighbor of that "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 221
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c29141ad-cc05-4d79-b3db-eb391808c29e
#     title = Restringuntus
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_94_F38PVXG83G8X_en.png
#     text = Play: Choose a house. Your opponent cannot choose that house as their active house until Restringuntus leaves play.
#     traits = Demon
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 94
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 439d9d6e-7abf-4a7a-83d5-77060b5668cc
#     title = Flaxia
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_352_JVPG4792RH9C_en.png
#     text = Play: Gain 2<A> if you control more "Creature"s than your opponent.
#     traits = Faerie
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 352
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 149e6b52-5d65-4fcb-9cc5-f57b4a16ba58
#     title = Vespilon Theorist
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_155_4XJVMF643M6C_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: Choose a house. Reveal the top card of your deck. If it is of that house archive it and gain 1<A>. Otherwise discard it.
#     traits = Cyborg • Scientist
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 155
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 63a22a26-ad71-4fa9-908d-4a13d6ab8359
#     title = A Fair Game
#     house = Dis
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_53_CJXQV688FHG_en.png
#     text = Play: Discard the top card of your opponent’s deck and reveal their hand. You gain 1<A> for each card of the discarded card’s house revealed this way. Your opponent repeats the preceding effect on you.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 53
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c68fa80b-08b2-4153-88c1-9e56aac487fe
#     title = Pile of Skulls
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_25_M6WXP2FVXH53_en.png
#     text = Each time an enemy "Creature" is destroyed during your turn a friendly "Creature" captures 1<A>.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 25
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2b5233c4-7da4-497a-b938-3eb72dabaaf1
#     title = Niffle Queen
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_364_F69VCQPX95RV_en.png
#     text = Each other friendly Beast "Creature" gets +1 power.\u000bEach other friendly Niffle "Creature" gets +1 power.
#     traits = Beast • Niffle
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 364
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0fba4ba8-317b-44c0-a51e-0a06bdb770d3
#     title = Swap Widget
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_189_Q8749GRQ2RRW_en.png
#     text = "Action": Return a ready friendly Mars "Creature" to your hand. If you do put a Mars "Creature" with a different name from your hand into play then ready it.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 189
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0077d73e-273c-4e89-adda-eb28dda8148e
#     title = Oath of Poverty
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_222_QR5CWH4G69H3_en.png
#     text = Play: Destroy each of your artifacts. Gain 2<A> for each artifact destroyed this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 222
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 93a7d1e6-b66e-4c6b-86e3-3ea230a4d768
#     title = Invasion Portal
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_185_6C5RX4PMJ5R2_en.png
#     text = "Action": Discard cards from the top of your deck until you discard a Mars "Creature" or run out of cards. If you discard a Mars "Creature" this way put it into your hand.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 185
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 57f8a873-414b-4c77-be9a-15561c76f719
#     title = Banner of Battle
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_20_3FQVR3V3CR7F_en.png
#     text = Each friendly "Creature" gets +1 power.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 20
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 4064612e-602e-46c1-b8eb-8adda1cfd0d0
#     title = Kelifi Dragon
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_37_PGMRV99HCWG7_en.png
#     text = Kelifi Dragon cannot be played unless you have 7<A> or more.\u000bFight/Reap: Gain 1<A>. Deal 5<D> to a "Creature".
#     traits = Dragon
#     amber = 0
#     power = 12
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 37
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8a045167-eccd-4026-9508-a73f5395cdad
#     title = Rock-Hurling "Giant"
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_44_HP3GQM2F73G5_en.png
#     text = During your turn each time you discard a "Brobnar" card from your hand you may deal 4<D> to a "Creature".
#     traits = "Giant"
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 44
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = bbb7c660-d282-4bd1-88f9-6d8213483c4a
#     title = Harland Mindlock
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_143_G7C9MP3P4VX2_en.png
#     text = Play: Take control of an enemy flank "Creature" until Harland Mindlock leaves play.
#     traits = Cyborg • Scientist
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 143
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = de5902d1-7462-497c-aa45-400f938772ef
#     title = Bulleteye
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_297_G45G2JGWP362_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: Destroy a flank "Creature".
#     traits = Elf • Thief
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 297
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c5e95ea2-fd32-4ab8-964a-720993f80d1b
#     title = Stampede
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_335_QV8XP6G2RJ4V_en.png
#     text = Play: If you used 3 or more "Creature"s this turn steal 2<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “Better to run with the herd than be trampled beneath it.” –Eldest Bear
#     number = 335
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 03980a75-13d7-4a47-8829-7a1c2ab996d9
#     title = Brain Stem Antenna
#     house = Mars
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_209_JHRJCP7RMVH2_en.png
#     text = This "Creature" gains “After you play a Mars "Creature" ready this "Creature" and for the remainder of the turn it belongs to house Mars.”
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 209
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 737b485f-fc98-4d01-9d07-b00c76e754ed
#     title = Veemos Lightbringer
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_262_VP65GQXWR45X_en.png
#     text = Play: Destroy each elusive "Creature".
#     traits = Angel • Spirit
#     amber = 0
#     power = 6
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 262
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = d46aafdf-13dd-45b0-be2e-d8e49be01d69
#     title = Master of 1
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_89_RF2PX33PJW8W_en.png
#     text = Reap: You may destroy a "Creature" with 1 power.
#     traits = Demon
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Rare"
#     flavor = The first sin is fear.
#     number = 89
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a6a864cf-ac90-4cd2-8d91-7de468c7f66c
#     title = Champion Tabris
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_240_C7P8FX9FVPXV_en.png
#     text = Fight: Capture 1<A>.
#     traits = Human • Knight
#     amber = 0
#     power = 6
#     armor = 2
#     rarity = "Uncommon"
#     flavor = “All my skill in battle brings me not one step closer to Enlightenment.”
#     number = 240
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f8f69f7c-ff0d-4ddb-b58a-41563b0c9a1c
#     title = Potion of Invulnerability
#     house = Sanctum
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_234_RJ99C8H7PWJH_en.png
#     text = Omni: Sacrifice Potion of Invulnerability. For the remainder of the turn each friendly "Creature" cannot be dealt damage.
#     traits = Item
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 234
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 026fa764-3bf2-40fc-9182-b34f0acfb760
#     title = Neutron Shark
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_146_92H2X974PG8Q_en.png
#     text = Play/Fight/Reap: Destroy an enemy "Creature" or artifact and a friendly "Creature" or artifact. Discard the top card of your deck. If that card is not a Logos card trigger this effect again.
#     traits = Beast • Mutant
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 146
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 54a95c9b-5b99-4a12-9e68-29adb3e8b49b
#     title = Deep Probe
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_162_J3M2V5CXFJ4W_en.png
#     text = Play: Choose a house. Reveal your opponent's hand. Discard each "Creature" of that house revealed this way.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 162
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 6806cdf1-81bb-49ce-909b-f98be2d82cb5
#     title = Numquid the Fair
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_253_3G85FMW7C6QH_en.png
#     text = Play: Destroy an enemy "Creature". Repeat this card’s effect if your opponent still controls more "Creature"s than you.
#     traits = Human
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 253
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2679977b-87f2-4afe-8c40-9e713569794f
#     title = Truebaru
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_104_VCQ8F8XMQJCH_en.png
#     text = You must lose 3<A> in order to play Truebaru.  \u000bTaunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)\u000bDestroyed: Gain 5<A>. 
#     traits = Demon
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 104
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 872b8871-93da-4b0d-a321-61f09e1824ea
#     title = Dysania
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_141_MMQJWC7Q6V3_en.png
#     text = Play: Your opponent discards each of their archived cards. You gain 1<A> for each card discarded this way.
#     traits = Mutant
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 141
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f4cc23bb-4e17-46e9-97ef-3d984b9a79fc
#     title = Bear Flute
#     house = Untamed
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_340_94548CJ4JMP9_en.png
#     text = "Action": Fully heal an Ancient Bear. If there are no Ancient Bears in play search your deck and discard pile and put each Ancient Bear from them into your hand. If you do shuffle your discard pile into your deck.
#     traits = Item
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 340
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 66f8ec97-15d0-4102-819a-7d912feca361
#     title = Piranha Monkeys
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_365_9WCFVMXQMVJG_en.png
#     text = Play/Reap: Deal 2<D> to each other "Creature".
#     traits = Beast
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = They can skeletonize a snufflegator in two minutes flat.
#     number = 365
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9a146bd4-7017-49ab-9e59-3ddbbb18d210
#     title = The Harder They Come
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_228_JQM953FW234C_en.png
#     text = Play: Purge a "Creature" with power 5 or higher.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 228
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = de9869e5-5750-4ce3-bec5-40f250a05a59
#     title = Incubation Chamber
#     house = Mars
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_186_PRG4HJPG6GX8_en.png
#     text = Omni: Reveal a Mars "Creature" from your hand. If you do archive it.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = Most Martians on the Crucible came out of one of these tanks.
#     number = 186
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2b3b461c-7f0b-4ebf-bcf7-f37a9509d7b5
#     title = Tolas
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_103_PMC43W3QPFW4_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bEach time a "Creature" is destroyed its opponent gains 1<A>.
#     traits = Imp
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 103
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f344ec2a-cbfb-4cd1-9f11-35b2a1a7e90c
#     title = Positron Bolt
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_118_9RQFX349V37W_en.png
#     text = Play: Deal 3<D> to a flank "Creature". Deal 2<D> to its neighbor. Deal 1<D> to the second "Creature"’s other neighbor.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = 0
#     number = 118
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a802b4cc-6c00-4559-bb29-677cc0d788e5
#     title = Crazy Killing Machine
#     house = Logos
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_128_8VF3XM5JM75C_en.png
#     text = "Action": Discard the top card of each player’s deck. For each of those cards destroy a "Creature" or artifact of that card’s house if able. If 2 cards are not destroyed as a result of this destroy Crazy Killing Machine.
#     traits = Weapon
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 128
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 2948a6fc-f7fa-45f2-b73d-fdf5f4216e46
#     title = Chuff Ape
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_191_MMMC6JPJ4H5P_en.png
#     text = Taunt. (This "Creature"’s neighbors cannot be attacked unless they have taunt.)\u000bChuff Ape enters play stunned.\u000bFight/Reap: You may sacrifice another friendly "Creature". If you do fully heal Chuff Ape.
#     traits = Beast
#     amber = 0
#     power = 11
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 191
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c25f3a5d-b757-4c30-9097-01a9ad692833
#     title = Selwyn the Fence
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_309_7GJ6RPFR59G2_en.png
#     text = Fight/Reap: Move 1<A> from one of your cards to your pool.
#     traits = Elf • Thief
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 309
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9c13665d-e4da-45b4-b04d-27abfafe5c23
#     title = Masterplan
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_288_8FJVHVWFWC4P_en.png
#     text = Play: Put a card from your hand facedown beneath Masterplan.\u000bOmni: Play the card beneath Masterplan. Sacrifice Masterplan.
#     traits = Item
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 288
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c5fad519-5703-497a-bafe-6eb5d8e0dfe6
#     title = Yo Mama Mastery
#     house = "Brobnar"
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_52_9664WG465QGC_en.png
#     text = This "Creature" gains taunt.\u000bPlay: Fully heal this "Creature".
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “Yo’ Mama is sooo tiny...”
#     number = 52
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5b0259f0-f15b-4530-b634-b6309b96be69
#     title = Mass Abduction
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_169_V74WF7V4MC37_en.png
#     text = Play: Put up to 3 damaged enemy "Creature"s into your archives. If any of these "Creature"s leave your archives they are put into their owner’s hand instead.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 169
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 4f438035-6597-4863-8bb1-35463034e0f2
#     title = Ember Imp
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_85_C72X25358RG2_en.png
#     text = Your opponent cannot play more than 2 cards each turn.
#     traits = Imp
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 85
#     expansion = "CoA"
#     is_maverick = true
  
  
#     id = 02feb5dd-81a0-4e06-8b5d-0ad7bdc9de08
#     title = Mushroom Man
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_362_HW3R4QRJGGMM_en.png
#     text = Mushroom Man gets +3 power for each unforged key you have.
#     traits = Fungus • Human
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “He’s a real fun guy if you get to know him.” –Eldest Bear
#     number = 362
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = b04d00f0-3ce2-49b7-8ab4-220a40db2865
#     title = Random Access Archives
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_119_5J4359XWQQ74_en.png
#     text = Play: Archive the top card of your deck.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “3.14159 Niffles Monosodium Glutamate...”
#     number = 119
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 67e81873-d126-4e97-a9b6-b0ad4368f1c3
#     title = Lava Ball
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_9_G7F5XC6J5QMG_en.png
#     text = Play: Deal 4<D> to a "Creature" with 2<D> splash.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “Here...Catch!”
#     number = 9
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c79475dc-0faf-4e89-9847-49a314e23236
#     title = The Sting
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_295_45HVFWG7RMPF_en.png
#     text = Skip your “forge a key” step.\u000bYou get all <A> spent by your opponent when forging keys.\u000b"Action": Sacrifice The Sting.
#     traits = Vehicle
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 295
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 94387722-ef2e-4591-8cbf-989feaf94656
#     title = Ring of Invisibility
#     house = Shadows
#     typ = Upgrade
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_317_F7RPHF6XHVWC_en.png
#     text = This "Creature" gains elusive and skirmish.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “I put it down for just a second...”
#     number = 317
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c9c045b1-061b-419e-aa1b-bc913b57e7f0
#     title = Mighty Tiger
#     house = Untamed
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_360_88VX5H673QQ4_en.png
#     text = Play: Deal 4<D> to an enemy "Creature".
#     traits = Beast
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 360
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = ff0d19c4-55e6-494e-b705-8b0c6b196468
#     title = Shaffles
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_95_563MPX64P3XC_en.png
#     text = At the end of your turn your opponent loses 1<A>.
#     traits = Imp
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Do you want imps? This is how you get imps.” 
#     number = 95
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c4b7c7e1-72b5-453b-9240-c9eb33710910
#     title = Phylyx the Disintegrator
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_197_C637CW23C7M7_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000b"Action": Your opponent loses 1<A> for each other friendly Mars "Creature".
#     traits = Martian • Soldier
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 197
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 7368fd79-70b8-4917-9d2c-dead816f624c
#     title = Pingle Who Annoys
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_43_PC7XR5283WJ_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bDeal 1<D> to each enemy "Creature" after it enters play.
#     traits = Goblin
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 43
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = c03f90e3-17a6-407e-8655-9884ed569108
#     title = Reverse Time
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_121_CXQ8C95R8C87_en.png
#     text = Play: Swap your deck and your discard pile. Then shuffle your deck.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = ...time back turn could I if
#     number = 121
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 21a5a8b1-4d19-43f2-8e8d-bd7a7531099d
#     title = Sneklifter
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_313_XW5J3RPG585M_en.png
#     text = Play: Take control of an enemy artifact. While under your control if it does not belong to one of your three houses it is considered to be of house Shadows.
#     traits = Elf • Thief
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 313
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 81bfdb14-81ac-4dba-9ef4-fcba524b354e
#     title = Eater of the Dead
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_84_5P9QW3X62X46_en.png
#     text = Fight/Reap: Purge a "Creature" from a discard pile. If you do put a +1 power counter on Eater of the Dead.
#     traits = Demon
#     amber = 0
#     power = 4
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 84
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f099e2ec-681b-4b47-878b-c091da3708d1
#     title = Deipno Spymaster
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_299_M3P2FVHP7MC_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bOmni: Choose a friendly "Creature". You may use that "Creature" this turn.
#     traits = Elf • Thief
#     amber = 0
#     power = 1
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 299
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 250a4cca-bd8e-4e2f-b420-18a3335371d2
#     title = Martian Hounds
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_167_3M79PQ4XJ4W2_en.png
#     text = Play: Choose a "Creature". For each damaged "Creature" give the chosen "Creature" two +1 power counters.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = Who let the... dogs?... out?
#     number = 167
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 13895422-dc36-49ae-bb7c-5e5d1f3f9df4
#     title = Timetraveller
#     house = Logos
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_153_X83CX7XJ5GRX_en.png
#     text = Play: Draw 2 cards. \u000b"Action": Shuffle Timetraveller into your deck.
#     traits = Human • Scientist
#     amber = 1
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 153
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a1766b1c-dc41-4e1c-975e-111f6b740a6d
#     title = The "Common" Cold
#     house = Untamed
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_336_6J5XR2JH8X5G_en.png
#     text = Play: Deal 1<D> to each "Creature". You may destroy all Mars "Creature"s.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “As it turns out it’s a weaker version of the uncommon cold.” –Dr. Escotera
#     number = 336
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 8f7f0b00-868d-4447-967b-e8c9d880c91a
#     title = World Tree
#     house = Untamed
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_344_JWRCR9MQX696_en.png
#     text = "Action": Return a "Creature" from your discard pile to the top of your deck.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 344
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 818f90a4-e896-4ba2-91ea-0d1232e94058
#     title = Radiant Truth
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_224_J975CJ57VPP9_en.png
#     text = Play: Stun each enemy "Creature" not on a flank.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = “Truly I say to you: pie is superior to cake.” - from the Ravings of the Prophet Gizelhart
#     number = 224
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = dddb201b-03d0-4fa9-b627-c69f51994c13
#     title = Faygin
#     house = Shadows
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_300_X7RWJQRG2MRV_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: Return an Urchin from play or from your discard pile to your hand.
#     traits = Human • Thief
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 300
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = a835a99c-67a5-4e2d-9720-85b41ef58468
#     title = Take that Smartypants
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_11_R2V4JJXQRVGH_en.png
#     text = Play: Steal 2<A> if your opponent has 3 or more Logos cards in play.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = “Them bots don’t wear pants. I carry spares.”
#     number = 11
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 90dc2b61-521a-40c1-bf0a-14e4d1457977
#     title = Safe Place
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_289_88GPJGFV248G_en.png
#     text = You may spend <A> on Safe Place when forging keys.\u000b"Action": Move 1<A> from your pool to Safe Place.
#     traits = Location
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 289
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 0ee63919-bff1-404f-b71b-b03e85cf692e
#     title = Inspiration
#     house = Mars
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_220_J4PRQX77RXV8_en.png
#     text = Play: Ready and use a friendly "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = “The Sanctum gives meaning to my life.” - Duma the Martyr
#     number = 220
#     expansion = "CoA"
#     is_maverick = true
  
  
#     id = 91a3ed7b-2940-4774-86f1-9ca02989adee
#     title = Finishing Blow
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_269_V557QC8HH5C9_en.png
#     text = Play: Destroy a damaged "Creature". If you do steal 1<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = You’ll never see it coming.
#     number = 269
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5b80c696-efe1-4be2-92c8-d31c260ba8ac
#     title = Doorstep to Heaven
#     house = Sanctum
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_217_RWHMP875732G_en.png
#     text = Play: Each player with 6<A> or more is reduced to 5<A>.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Uncommon"
#     flavor = The cities of the Sanctum are safe clean and vibrant like few others on the Crucible. But few are judged worthy to enter.
#     number = 217
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 74a9ed49-ed43-42ff-b531-b84f737581db
#     title = Qyxxlyx Plague Master
#     house = Mars
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_198_4QXQJ939VVQM_en.png
#     text = Fight/Reap: Deal 3<D> to each Human "Creature". This damage cannot be prevented by armor.
#     traits = Martian • Scientist
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 198
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = f4497a06-5ae3-4706-86b6-c0c141b8f788
#     title = Help from Future Self
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_111_5WMP36R2MHF_en.png
#     text = Play: Search your deck and discard pile for a Timetraveller reveal it and put it into your hand. Shuffle your discard pile into your deck.
#     traits = False
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = FIXED
#     flavor = 0
#     number = 111
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = fdf76fb4-708d-4950-bc31-c91bb25aeb40
#     title = Customs Office
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_285_C7MWV8WQ4QPG_en.png
#     text = Your opponent must pay you 1<A> in order to play an artifact.
#     traits = Location
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 285
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 85584ea2-11be-40d0-bfcd-82799b1547af
#     title = Champion’s Challenge
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_6_PJ6HFMR62X8F_en.png
#     text = Play: Destroy each enemy "Creature" except the most powerful enemy "Creature". Destroy each friendly "Creature" except the most powerful friendly "Creature". Ready and fight with your remaining "Creature".
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 6
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 99879b5b-70c1-4fb2-9700-87054eb750b9
#     title = Autocannon
#     house = "Brobnar"
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_19_XRFQ9GHJ98C3_en.png
#     text = Deal 1<D> to each "Creature" after it enters play.
#     traits = Weapon
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 19
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = aeddb1b9-1241-4476-ae67-bd07016f46a2
#     title = Arise!
#     house = "Brobnar"
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_54_F9GHFCWJ233R_en.png
#     text = Play: Choose a house. Return each "Creature" of that house from your discard pile to your hand. Gain 1 chain.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Common"
#     flavor = 0
#     number = 54
#     expansion = "CoA"
#     is_maverick = true
  
  
#     id = bc08aefc-363f-4ef3-b6a0-5c60fc4da8f3
#     title = Jehu the Bureaucrat
#     house = Sanctum
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_250_XMP7GGP9HP57_en.png
#     text = After you choose Sanctum as your active house gain 2<A>.
#     traits = Human
#     amber = 0
#     power = 3
#     armor = 0
#     rarity = "Rare"
#     flavor = “The knights protect the Sanctum. They are entitled to certain... benefits.” 
#     number = 250
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5c8c697c-ffcf-4116-b133-179198017c31
#     title = Looter Goblin
#     house = "Brobnar"
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_41_779WFQQ368X7_en.png
#     text = Elusive. (The first time this "Creature" is attacked each turn no damage is dealt.)\u000bReap: For the remainder of the turn gain 1<A> each time an enemy "Creature" is destroyed.
#     traits = Goblin
#     amber = 0
#     power = 2
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 41
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 5fc16338-955d-48ed-abb4-9f38b9506c12
#     title = Routine Job
#     house = Shadows
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_282_4F97HV2RJ9FC_en.png
#     text = Play: Steal 1<A>. Then steal 1<A> for each copy of Routine Job in your discard pile.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 282
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 9751d62a-ce61-41f1-a13a-0d7f8812abf8
#     title = Evasion Sigil
#     house = Shadows
#     typ = "Artifact"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_286_4686MGRJ87QX_en.png
#     text = Before a "Creature" fights discard the top card of its controller's deck. If the discarded card is of the active house exhaust that "Creature" with no effect.
#     traits = Power
#     amber = 1
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 286
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 4f1c5b07-d31a-4177-b3b2-d1890d41c3e4
#     title = Overlord Greking
#     house = Dis
#     typ = "Creature"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_87_JFFVJ73VP9VQ_en.png
#     text = After an enemy "Creature" is destroyed fighting Overlord Greking put that "Creature" into play under your control.
#     traits = Demon
#     amber = 0
#     power = 7
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 87
#     expansion = "CoA"
#     is_maverick = False
  
  
#     id = 7176b276-d696-4b53-8990-e78d94583d0b
#     title = Knowledge is Power
#     house = Logos
#     typ = "Action"
#     front_image = https://cdn.keyforgegame.com/media/card_front/en/"CoA"_113_9V5G7WCPW27X_en.png
#     text = Play: Choose one: Archive a card or for each archived card you have gain 1<A>.
#     traits = False
#     amber = 0
#     power = 0
#     armor = 0
#     rarity = "Rare"
#     flavor = 0
#     number = 113
#     expansion = "CoA"
#     is_maverick = False