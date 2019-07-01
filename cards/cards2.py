import json

data = ['{ \
    "id": "469dd68d-cdd6-40e0-8fc9-a167c45a9aea", \
    "card_title": "Grasping Vines", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_324_VH9R4P26824V_en.png", \
    "card_text": "Play: Return up to 3 artifacts to their owners hands.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "324", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1a84631d-7fcb-4c9a-a50c-9539dcb84928", \
    "card_title": "Yxilo Bolter", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_204_H9HQ5F59FJQX_en.png", \
    "card_text": "Fight/Reap: Deal 2<D> to a creature. If this damage destroys that creature, purge it.", \
    "traits": "Martian  Soldier", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "204", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b8343462-b5d7-48b0-9e3b-f020c5e73c55", \
    "card_title": "Tocsin", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_102_CG7PMM7PJ3G6_en.png", \
    "card_text": "Reap: Your opponent discards a random card from their hand.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "102", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c08c91f0-043a-4a8a-8761-6080e9f46183", \
    "card_title": "Titan Mechanic", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_154_M7WH2HV6J2FX_en.png", \
    "card_text": "While Titan Mechanic is on a flank, each key costs –1<A>.", \
    "traits": "Cyborg  Scientist", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "If they come, they will build it. ", \
    "card_number": "154", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ce051448-1745-4606-95a0-e44e70401ba1", \
    "card_title": "Foggify", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_110_4W42XPXRVP7V_en.png", \
    "card_text": "Play: Your opponent cannot use creatures to fight on their next turn.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "110", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "622f072b-bdab-412b-9da4-f59116940a95", \
    "card_title": "Troop Call", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_337_WP75XF628MRC_en.png", \
    "card_text": "Play: Return each friendly Niffle creature from your discard pile and from play to your hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "337", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "aabeebf7-1da5-4149-afab-e7e221b47d93", \
    "card_title": "Uxlyx the Zookeeper", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_201_69W23Q88QWW4_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: Put an enemy creature into your archives. If that creature leaves your archives, it is put into its owner’s hand instead.", \
    "traits": "Martian  Scientist", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "201", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "699f06e3-e47b-4910-90b9-c67fac157d6e", \
    "card_title": "Dance of Doom", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_57_QR3X35J5GWCR_en.png", \
    "card_text": "Play: Choose a number. Destroy each creature with power equal to that number.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "57", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5fbcee22-232c-46ba-84e0-3baad3946220", \
    "card_title": "Blood Money", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_3_XX937XGH258R_en.png", \
    "card_text": "Play: Place 2<A> from the common supply on an enemy creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“You! Æmber lover. You’re next.”", \
    "card_number": "3", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c7f70ade-d2e2-4032-a843-0fca6076d243", \
    "card_title": "Grenade Snib", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_34_WJXC3F32R7CP_en.png", \
    "card_text": "Destroyed: Your opponent loses 2<A>.", \
    "traits": "Goblin", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "34", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "6bf5d9fa-1fbb-4609-8671-986a4709d3aa", \
    "card_title": "Lifeward", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_77_46M5PVW2VRX9_en.png", \
    "card_text": "Omni: Sacrifice Lifeward. Your opponent cannot play creatures on their next turn.", \
    "traits": "Power", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "77", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5aba3999-2489-4073-92be-cc0ec93ee65f", \
    "card_title": "Lady Maxena", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_251_P4MXH8G4VPX4_en.png", \
    "card_text": "Play: Stun a creature. Action: Return Lady Maxena to its owner’s hand.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "5", \
    "armor": "2", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "251", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "afe27535-5cb7-43a1-8eab-ff9a6a472edb", \
    "card_title": "Vigor", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_338_CR6PV8PPC85R_en.png", \
    "card_text": "Play: Heal up to 3 damage from a creature. If you healed 3 damage, gain 1<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "338", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c39567bb-4695-4518-8b8d-8ac882894d1e", \
    "card_title": "Round Table", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_235_MJMGJPH3545P_en.png", \
    "card_text": "Each friendly Knight creature gets +1 power and gains taunt.", \
    "traits": "Location", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Come my friends, let us ready for battle.” –King Godfrey Greywind", \
    "card_number": "235", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2f9f20aa-b110-4df8-8f4e-560a11f0ae49", \
    "card_title": "Novu Archaeologist", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_147_X27M5CQW494F_en.png", \
    "card_text": "Action: Archive a card from your discard pile.", \
    "traits": "Cyborg  Scientist", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“One civilization’s trash is... nope, still trash.”", \
    "card_number": "147", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9095c1fe-1783-4b09-9d90-6164234a73aa", \
    "card_title": "Shoulder Armor", \
    "house": "Sanctum", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_266_F6GMMXCFJ9PC_en.png", \
    "card_text": "While this creature is on a flank, it gets +2 armor and +2 power.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“I can’t see anything. Do I look cool?” ", \
    "card_number": "266", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a8b24d43-1940-4852-afcb-d034d99da55d", \
    "card_title": "Protect the Weak", \
    "house": "Sanctum", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_265_36392V5F286G_en.png", \
    "card_text": "This creature gets +1 armor and gains taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "265", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5607fecd-b90e-4e12-84bc-cb36d079117c", \
    "card_title": "Hysteria", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_65_HX7W9345R87F_en.png", \
    "card_text": "Play: Return each creature to its owner’s hand.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Help! I can’t stop this feeling!”", \
    "card_number": "65", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3056e60c-8f7c-40da-951c-6e0e9cfb9d46", \
    "card_title": "Inspiration", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_220_J4PRQX77RXV8_en.png", \
    "card_text": "Play: Ready and use a friendly creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“The Sanctum gives meaning to my life.” - Duma the Martyr", \
    "card_number": "220", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "459a6725-dcc0-4967-8cd4-a9bbb1548eda", \
    "card_title": "Lost in the Woods", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_327_W6VV383R4X8P_en.png", \
    "card_text": "Play: Choose 2 friendly creatures and 2 enemy creatures. Shuffle each chosen creature into its owner’s deck.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "327", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f0c4cb0f-8e5f-454c-a6ad-35f35ac3c98a", \
    "card_title": "Dew Faerie", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_350_6X8HWG4MJPCC_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: Gain 1<A>.", \
    "traits": "Faerie", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "350", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "aa9b8dfe-3817-4f9d-b4c8-95c5c303c513", \
    "card_title": "Effervescent Principle", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_109_9382CVHW3F7H_en.png", \
    "card_text": "Play: Each player loses half their <A> (rounding down the loss). Gain 1 chain.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "109", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "19b74b4e-bec8-4fbb-bd35-cb635f500249", \
    "card_title": "Soft Landing", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_177_F3R3FCFQQQG8_en.png", \
    "card_text": "Play: The next creature or artifact you play this turn enters play ready.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Any landing you walk away from…", \
    "card_number": "177", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a2ad028a-8447-4568-aa8e-520227640aca", \
    "card_title": "Brothers in Battle", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_4_75MHQJM77RGH_en.png", \
    "card_text": "Play: Choose a house. For the remainder of the turn, each friendly creature of that house may fight.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "4", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b97236a0-5a0e-437b-b3be-d13834c0dc2d", \
    "card_title": "Tireless Crocag", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_47_QHVVFWHGJM8R_en.png", \
    "card_text": "Tireless Crocag cannot reap.You may use Tireless Crocag as if it belonged to the active house.If your opponent has no creatures in play, destroy Tireless Crocag.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "47", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d42dd1d0-3462-410f-b683-dd0768b84188", \
    "card_title": "Hand of Dis", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_62_8WF3JF84X9VM_en.png", \
    "card_text": "Play: Destroy a creature that is not on a flank.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Let me give you a hand...”", \
    "card_number": "62", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8717beaa-79ff-44ba-b4e1-700235535844", \
    "card_title": "Soul Snatcher", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_80_79QFRXPXVQ33_en.png", \
    "card_text": "Each time a creature is destroyed, its owner gains 1<A>.", \
    "traits": "Vehicle", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "No one goes in, no one comes out. And yet the fires burn.", \
    "card_number": "80", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f75dda7d-680c-4bd5-8813-d04646857753", \
    "card_title": "Red Planet Ray Gun", \
    "house": "Mars", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_211_PQFJWQ3VVVGJ_en.png", \
    "card_text": "This creature gains, “Reap: Choose a creature. Deal 1<D> to that creature for each Mars creature in play.”", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "211", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "64f0e039-dd33-49f0-8e9c-42ec38aba8a1", \
    "card_title": "Skeleton Key", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_291_7FCVJGVJQF96_en.png", \
    "card_text": "Action: A friendly creature captures 1<A>.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Skeleton sold separately.", \
    "card_number": "291", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "57bccc52-b6a1-4d11-b9d9-6356d8ac279c", \
    "card_title": "Mother", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_145_65HF32HQGF2G_en.png", \
    "card_text": "During your “draw cards” step, refill your hand to 1 additional card.", \
    "traits": "Robot  Scientist", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Of course she’s necessary, she’s the mother of all invention!”", \
    "card_number": "145", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "59cb3ad9-cc98-4fe5-8589-a8967d32af00", \
    "card_title": "Library of Babble", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_129_WR7JW9MF9F2R_en.png", \
    "card_text": "Action: Draw a card.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "When you make an archive of all knowledge in the galaxy, don’t be surprised when you understand almost none of it. ", \
    "card_number": "129", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1d17903e-5c7a-4882-833f-707ce03d1228", \
    "card_title": "Curiosity", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_320_Q6Q7VG34P9GF_en.png", \
    "card_text": "Play: Destroy each Scientist creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“It started with Schrödinger’s cat and just kept going from there.” – Quixo the “Adventurer”", \
    "card_number": 320, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "05fa104f-3719-41d0-9189-57ff3ec5edc1", \
    "card_title": "Witch of the Eye", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_368_MC5PG9FQ3766_en.png", \
    "card_text": "Reap: Return a card from your discard pile to your hand.", \
    "traits": "Human  Witch", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Waste not, want not.”", \
    "card_number": "368", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "aeed12e9-7b9d-43f4-8bf7-04f076c3ea79", \
    "card_title": "Psychic Network", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_174_Q59H8QWGHQCR_en.png", \
    "card_text": "Play: Steal 1<A> for each friendly ready Mars creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "174", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "16168a85-bbfa-4e54-8c84-5ea02e2a7da1", \
    "card_title": "Mating Season", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_170_6C5MPJVJ5G9R_en.png", \
    "card_text": "Play: Shuffle each Mars creature into its owner’s deck. Each player gains 1<A> for each creature shuffled into their deck this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "170", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e5746977-89c3-4300-8125-c8fd776a020f", \
    "card_title": "Sniffer", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_188_JXXCR37F52MR_en.png", \
    "card_text": "Action: For the remainder of the turn, each creature loses elusive.", \
    "traits": "Ally", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "Even the Martians’ pets have a bone to pick with the other lifeforms on the Crucible.", \
    "card_number": "188", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "20c810de-ad56-49ad-a57c-7fe7262b3cda", \
    "card_title": "Nepenthe Seed", \
    "house": "Untamed", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_341_M3P5Q4RWG42_en.png", \
    "card_text": "Omni: Sacrifice Nepenthe Seed. Return a card from your discard pile to your hand.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "341", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bda929e2-962a-438c-a210-47f21228dfbc", \
    "card_title": "Mothergun", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_187_886VP3RR6C5F_en.png", \
    "card_text": "Action: Reveal any number of Mars cards from your hand. Deal damage to a creature equal to the number of Mars cards revealed this way.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "187", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c9625085-6eb2-4555-87cd-cda180af9f71", \
    "card_title": "Pitlord", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_93_95PVMCCHQ7P2_en.png", \
    "card_text": "Taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)While Pitlord is in play you must choose Dis as your active house.", \
    "traits": "Demon", \
    "amber": "2", \
    "power": "9", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "93", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ff5917ee-ddb9-42d1-8a2a-ecc8c1a6ab84", \
    "card_title": "Dimension Door", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_108_XHW22F7FH9FM_en.png", \
    "card_text": "Play: For the remainder of the turn, any <A> you would gain from reaping is stolen from your opponent instead.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "108", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "87ebd58d-d08f-41f7-a3fd-67b476d13673", \
    "card_title": "Mothership Support", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_171_C9HXR9JCPGP9_en.png", \
    "card_text": "Play: For each friendly ready Mars creature, deal 2<D> to a creature. (You may choose a different creature each time.)", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "171", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e40df662-6506-4a35-816d-efe29a0e4a6f", \
    "card_title": "Sequis", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_257_WC74XH7M2MJW_en.png", \
    "card_text": "Reap: Capture 1<A>.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "4", \
    "armor": "2", \
    "rarity": "Common", \
    "flavor_text": "“I follow the Æmber light of the Sanctum, the light of truth and hope. What is it you follow?”", \
    "card_number": "257", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9779c7a8-419a-4c99-9460-a48ddf33b963", \
    "card_title": "Champion Anaphiel", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_239_FR9V84W6X65C_en.png", \
    "card_text": "Taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "6", \
    "armor": "1", \
    "rarity": "Common", \
    "flavor_text": "“Steel thyself, Knave. To harm them you must first defeat me.”", \
    "card_number": "239", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a8c4f41a-0d6b-4f0b-ac8f-27b2db518dce", \
    "card_title": "Punch", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_12_8QF6VM4C23R9_en.png", \
    "card_text": "Play: Deal 3<D> to a creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Three for flinching.", \
    "card_number": "12", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f04a582c-c50b-453e-afc8-9d459c46cc22", \
    "card_title": "Nocturnal Maneuver", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_330_R4Q6P7M74J89_en.png", \
    "card_text": "Play: Exhaust up to 3 creatures.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Every world has its fearsome creatures that thrive in the darkness, and the Crucible has them all. ", \
    "card_number": "330", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c8ed04c1-d938-4d96-a284-6e0f6a2b116e", \
    "card_title": "Teliga", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_366_F2PF3262P9XJ_en.png", \
    "card_text": "Each time your opponent plays a creature, gain 1<A>.", \
    "traits": "Human  Witch", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Don’t try to change the Crucible to suit your needs. Let it change you.”", \
    "card_number": "366", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ff290bf3-dd57-48b3-add3-c6baf605967c", \
    "card_title": "Magda the Rat", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_303_JJPCRGJ7CFPW_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Play: Steal 2<A>.Leaves Play: Your opponent steals 2<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "303", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "27a6e4f0-4770-4ce0-89ff-8b2fd5a99f4a", \
    "card_title": "Relentless Assault", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_13_967HJV9Q3J5P_en.png", \
    "card_text": "Play: Ready and fight with up to 3 different friendly creatures, one at a time.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "13", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0b20bfe2-5664-4c1a-9e1a-22aa108d3786", \
    "card_title": "Cleansing Wave", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_215_RFRWH2MX953_en.png", \
    "card_text": "Play: Heal 1 damage from each creature. Gain 1<A> for each creature healed this way.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "215", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "22c50a42-0b6e-4681-9632-3d315a76e849", \
    "card_title": "Save the Pack", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_333_4J9WMP4Q2F2G_en.png", \
    "card_text": "Play: Destroy each damaged creature. Gain 1 chain.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "333", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d6aae364-d547-49ec-83dd-be3ffbcb80c6", \
    "card_title": "Ganymede Archivist", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_142_9RC9J993WM9F_en.png", \
    "card_text": "Reap: Archive a card.", \
    "traits": "Human  Scientist", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“They offered to let my crew stay with them. I politely declined.” –Captain Val Jericho", \
    "card_number": "142", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b361d7e2-6873-4890-8f87-702d9c89c5ad", \
    "card_title": "Anger", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_1_7C854VPW72RH_en.png", \
    "card_text": "Play: Ready and fight with a friendly creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Don’t make them angry you say? Heh. The Brobnar are born angry.” –Old Bruno", \
    "card_number": "1", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3e4d74e3-8080-402f-9444-b069ce4e56d7", \
    "card_title": "Glorious Few", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_218_63PVJ7PJP3GP_en.png", \
    "card_text": "Play: For each creature your opponent controls in excess of you, gain 1<A>.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "218", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "45bc71b4-3465-4917-a67f-f4928d22d795", \
    "card_title": "Tendrils of Pain", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_64_WCMG558RP6QV_en.png", \
    "card_text": "Play: Deal 1<D> to each creature. Deal an additional 3<D> to each creature if your opponent forged a key on their previous turn.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "64", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2cb1f58c-5979-4d3a-ae86-9dadc6000288", \
    "card_title": "Phase Shift", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_117_HP2M3PV8GPJ7_en.png", \
    "card_text": "Play: You may play one non-Logos card this turn.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "117", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "dc18cfc1-9dd9-440d-93be-50c2c114b3c8", \
    "card_title": "Spangler Box", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_132_XQ93M42M9FR5_en.png", \
    "card_text": "Action: Purge a creature in play. If you do, your opponent gains control of Spangler Box. If Spangler Box leaves play, return to play all cards purged by Spangler Box.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "132", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "67ac26ce-b816-4ae1-9bea-9f38059f3b46", \
    "card_title": "Longfused Mines", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_287_H6CGFG593XMM_en.png", \
    "card_text": "Omni: Sacrifice Longfused Mines. Deal 3<D> to each enemy creature not on a flank.", \
    "traits": "Weapon", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "287", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a429a71c-e558-4ee6-af48-6326df3d4b0f", \
    "card_title": "Library Access", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_115_4J2C745JC5V2_en.png", \
    "card_text": "Play: For the remainder of the turn, each time you play another card, draw a card.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "115", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1838fbaa-a062-4593-acbe-53ecfadfb5cc", \
    "card_title": "Labwork", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_114_X6V5QX33Q589_en.png", \
    "card_text": "Play: Archive a card.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Attention to detail is the key to all progress.", \
    "card_number": "114", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f74c96d8-ccec-4201-af7c-755df49d0025", \
    "card_title": "Jammer Pack", \
    "house": "Mars", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_210_HCXQ277C22FW_en.png", \
    "card_text": "This creature gains, '"Your opponents keys cost +2<A>."'", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“The humans make it. It’s called ‘moo-zak.’”", \
    "card_number": "210", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3515de43-9c9a-4ec8-bced-d2d21ff24824", \
    "card_title": "Remote Access", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_120_V59VPJJ255WQ_en.png", \
    "card_text": "Play: Use an opponents artifact as if it were yours.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "120", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8023cf81-ac80-499e-b8bb-3bfa2511fd63", \
    "card_title": "Red-Hot Armor", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_70_QXV6993G25X7_en.png", \
    "card_text": "Play: Each enemy creature with armor loses all of its armor until the end of the turn and is dealt 1<D> for each point of armor it lost this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": 70, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "06ab14e9-ec4f-4f2d-908e-20940241590c", \
    "card_title": "Krump", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_39_Q64CQC29J542_en.png", \
    "card_text": "After an enemy creature is destroyed fighting Krump, its controller loses 1<A>.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "39", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a936b45d-5de6-4b43-889b-9c58f0ab4c35", \
    "card_title": "Nerve Blast", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_276_833RV7MVFCH8_en.png", \
    "card_text": "Play: Steal 1<A>. If you do, deal 2<D> to a creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Don’t look so shocked to see me!”", \
    "card_number": "276", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "aa73a693-e1e6-4097-8010-ddc820cc6d96", \
    "card_title": "Gongoozle", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_60_8J78GV8GV57Q_en.png", \
    "card_text": "Play: Deal 3<D> to a creature. If it is not destroyed, its owner discards a random card from their hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Just trying to understand these...’things’ gives me a headache.”", \
    "card_number": "60", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f5019c91-eea0-4883-9946-297bbf1c6822", \
    "card_title": "Anomaly Exploiter", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_126_F66C7VF2HR8Q_en.png", \
    "card_text": "Action: Destroy a damaged creature.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "126", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "6ae428ad-1ac3-4419-be83-7c7790b8fd96", \
    "card_title": "Too Much to Protect", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_283_J93HJ73F4PMQ_en.png", \
    "card_text": "Play: Steal all but 6 of your opponent’s <A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Not taking it would be the real crime.", \
    "card_number": "283", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5ad003a2-8572-4fbd-b9fb-a2e94e4bdc7c", \
    "card_title": "Poltergeist", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_69_P2P8M5XWMHCW_en.png", \
    "card_text": "Play: Use an artifact controlled by any player as if it were yours. Destroy that artifact.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "69", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "179f877a-9b59-46d6-a43e-15b4524af3c6", \
    "card_title": "Ether Spider", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_192_P52JHFXR9X8X_en.png", \
    "card_text": "Ether Spider deals no damage when fighting.Each <A> that would be added to your opponent’s pool is captured by Ether Spider instead.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "192", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c5ed37f7-0d05-48bc-a595-4f25c0ec1e6d", \
    "card_title": "Charette", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_81_GM7WM322M4_en.png", \
    "card_text": "Play: Capture 3<A>.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "It doesn’t like to share.", \
    "card_number": "81", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "53f7d3ec-a65f-4b05-8c82-74f44a7bdc44", \
    "card_title": "Research Smoko", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_151_XC9823CQ2V92_en.png", \
    "card_text": "Destroyed: Archive the top card of your deck.", \
    "traits": "Mutant", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "151", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "916f271b-9928-437c-bfc4-d60d32af8c7c", \
    "card_title": "Ember Imp", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_85_C72X25358RG2_en.png", \
    "card_text": "Your opponent cannot play more than 2 cards each turn.", \
    "traits": "Imp", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "85", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d71c36b7-c4be-427a-8038-2033ba9bf07e", \
    "card_title": "Commander Remiel", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_241_C472V3C68C9_en.png", \
    "card_text": "Reap: Use a friendly non-Sanctum creature.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I was not always a knight. Perhaps, someday, you will stand where I stand and see what I see.” ", \
    "card_number": "241", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3f0f006a-10bc-4f1a-a90a-a64abb14d5a0", \
    "card_title": "Lifeweb", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_326_X574G5FJP676_en.png", \
    "card_text": "Play: If your opponent played 3 or more creatures on their previous turn, steal 2<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "326", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9c75188a-8cb2-4201-9f10-d13f6cd00255", \
    "card_title": "Pawn Sacrifice", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_279_RJJJ2R3P5FHC_en.png", \
    "card_text": "Play: Sacrifice a friendly creature. If you do, deal 3<D> each to 2 creatures.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Pawn to Queen’s Bishop four.", \
    "card_number": "279", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "79be4a3f-0f51-4cf7-a199-819244879eac", \
    "card_title": "Custom Virus", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_183_3G89HPF6R2GX_en.png", \
    "card_text": "Omni: Sacrifice Custom Virus. Purge a creature from your hand. Destroy each creature that shares a trait with the purged creature.", \
    "traits": "Weapon", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "183", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "21d11426-7870-44ec-a16f-bf3724271d21", \
    "card_title": "Begone!", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_212_W36G9HXF9RQ7_en.png", \
    "card_text": "Play: Choose one: destroy each Dis creature, or gain 1<A>.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "212", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3d650fe4-817a-4922-ba0f-297c1ebf816d", \
    "card_title": "Screechbomb", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_26_WGX3X54PQCMP_en.png", \
    "card_text": "Omni: Sacrifice Screechbomb. Your opponent loses 2<A>.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“I think that thing made me deaf!”“What? I can’t hear you! I think that thing made me deaf!” ", \
    "card_number": "26", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ba8d348b-5c05-44d1-88f1-3945f9a485d8", \
    "card_title": "Old Bruno", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_307_7M48G5WCGGX9_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Play: Capture 3<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“I raise.”", \
    "card_number": "307", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f8f497ca-3216-446a-805a-0d00ff1b7702", \
    "card_title": "Barehanded", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_2_53CXMQCJ46PP_en.png", \
    "card_text": "Play: Put each artifact on top of its owner’s deck.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "2", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d2edea65-7c2f-487f-a6f4-f44a077c4a65", \
    "card_title": "Control the Weak", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_55_7CJ4H2WMJWQ2_en.png", \
    "card_text": "Play: Choose a house on your opponent’s identity card. Your opponent must choose that house as their active house on their next turn.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "55", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "448c1335-d45b-473e-b222-d71f31ba0292", \
    "card_title": "Sloppy Labwork", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_123_R3C97J8JMPRV_en.png", \
    "card_text": "Play: Archive a card. Discard a card.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Don’t fret the details. Progress happens when you least expect it.", \
    "card_number": "123", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1da26e11-d319-4980-a2c3-931054ff008c", \
    "card_title": "Epic Quest", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_231_9CW6R752CCQG_en.png", \
    "card_text": "Play: Archive each friendly Knight creature in play.Omni: If you have played 7 or more Sanctum cards this turn, sacrifice Epic Quest and forge a key at no cost.", \
    "traits": "Quest", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "231", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "87197e65-0d83-42a8-bec9-9e0e1fb75f34", \
    "card_title": "Gatekeeper", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_260_MJV7XGGFVMQC_en.png", \
    "card_text": "Play: If your opponent has 7 or more <A>, capture all but 5 of it.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "5", \
    "armor": "1", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "260", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e8276e78-a5f3-42c0-b030-a08e25137dc0", \
    "card_title": "Fuzzy Gruen", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_353_5P9MP78G2R8Q_en.png", \
    "card_text": "Play: Your opponent gains 1<A>.", \
    "traits": "Beast", \
    "amber": "2", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "353", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "52e685bc-df93-42b5-b8e6-bad9357c48da", \
    "card_title": "Hypnotic Command", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_164_QCCQ9VXCQH7X_en.png", \
    "card_text": "Play: For each friendly Mars creature, choose an enemy creature to capture 1<A> from their own side.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "164", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "68fbba20-4516-4e8a-8d3d-47e2cb401032", \
    "card_title": "Key Charge", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_325_66XVRV5PWMVG_en.png", \
    "card_text": "Play: Lose 1<A>. If you do, you may forge a key at current cost.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“You might call it madness, but for all we know madness is a key ingredient.” –Inka the Spider", \
    "card_number": "325", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "df6e4b5b-9f0a-4bd5-808a-6ccd46d973c4", \
    "card_title": "Chaos Portal", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_127_R2424CG64G8M_en.png", \
    "card_text": "Action: Choose a house. Reveal the top card of your deck. If it is of that house, play it.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "127", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ea2a390e-e121-4cbd-96c5-2430cc600e81", \
    "card_title": "Mind Barb", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_67_GJXV3PCXVPMW_en.png", \
    "card_text": "Play: Your opponent discards a random card from their hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "67", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ac8fb9f6-ee8e-4434-85e8-d084a66c50db", \
    "card_title": "Zorg", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_206_4XXWX9CP9XGJ_en.png", \
    "card_text": "Zorg enters play stunned. Before Fight: Stun the creature Zorg fights and each of that creature’s neighbors.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "206", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "22fdfc0f-5ea1-42bd-984a-8c9edd8b16b7", \
    "card_title": "Hallowed Blaster", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_233_V3CVPF24W8MR_en.png", \
    "card_text": "Action: Heal 3 damage from a creature.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Swords into plowshares is thinking too small.", \
    "card_number": "233", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "6f6b30f0-c2b5-4824-b836-b5f45ca5fb6d", \
    "card_title": "Blypyp", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_190_8XHXRR6J7CH2_en.png", \
    "card_text": "Reap: The next Mars creature you play this turn enters play ready.", \
    "traits": "Martian  Scientist", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Soooon…”", \
    "card_number": "190", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f26caba2-7ab6-477c-8a53-45e5fb666a90", \
    "card_title": "Screaming Cave", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_79_WQCG263H8RWW_en.png", \
    "card_text": "Action: Shuffle your hand and discard pile into your deck.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "”Was that you, or the cave?” - Captain<nonbreak>Val<nonbreak>Jericho", \
    "card_number": "79", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "4e9e09ba-66b9-4fc8-a61d-ca2dad320a5c", \
    "card_title": "Clear Mind", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_216_4CVXQJV2QG3P_en.png", \
    "card_text": "Play: Unstun each friendly creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "Thy body is an illusion. Only thy spirit is eternal.", \
    "card_number": "216", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "37a73724-a6e5-457f-8fde-fa792efa18ab", \
    "card_title": "Ozmo, Martianologist", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_148_R25C9WHJ9V29_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Fight/Reap: Heal 3 damage from a Mars creature or stun a Mars creature. ", \
    "traits": "Human  Scientist", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "148", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3680b506-9a5c-4afb-956d-15b08d1e9ecc", \
    "card_title": "Dust Pixie", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_351_PFJXP2G7VWVP_en.png", \
    "card_text": "(Vanilla)", \
    "traits": "Faerie", \
    "amber": "2", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "The faeries are believed to be created by the Architects to tend to the plants and animals of the Crucible. In the eons since their creation, some have become…quirky.  ", \
    "card_number": "351", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ceecd78b-f0bb-4de9-a3c6-dff6686be13d", \
    "card_title": "Combat Pheromones", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_180_HQXG9V9X249X_en.png", \
    "card_text": "Omni: Sacrifice Combat Pheromones. You may use up to 2 other Mars cards this turn.", \
    "traits": "Item", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Don’t worry, this will only sting a lot.”", \
    "card_number": "180", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "49183ec5-6dad-48fb-9d86-253db31d72cf", \
    "card_title": "“John Smyth”", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_195_8VX38X5J32VV_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Fight/Reap: Ready a non-Agent Mars creature.", \
    "traits": "Agent  Martian", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "195", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "466deee8-d9c0-4e08-af87-da5cbf80ce69", \
    "card_title": "Brain Eater", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_137_F8PFV5JC764_en.png", \
    "card_text": "After a creature is destroyed fighting Brain Eater, draw a card.", \
    "traits": "Cyborg  Beast", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "137", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e5a1f190-6964-4b2e-bcb3-696d3f6f2713", \
    "card_title": "Gabos Longarms", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_86_33RP646XMQ93_en.png", \
    "card_text": "Before Fight: Choose a creature. Gabos Longarms deals damage to that creature rather than the one it is fighting.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "86", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "22476b3c-d05c-4274-ad8f-ec1efabad116", \
    "card_title": "Cannon", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_21_CRMGW6QVC5HC_en.png", \
    "card_text": "Action: Deal 2<D> to a creature.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "21", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "575d4804-78ff-4afa-8d44-2507126af6da", \
    "card_title": "Tunk", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_199_FW92QH6WPGCW_en.png", \
    "card_text": "After you play another Mars creature, fully heal Tunk.", \
    "traits": "Robot", \
    "amber": "0", \
    "power": "6", \
    "armor": "1", \
    "rarity": "Common", \
    "flavor_text": "“Who’s driving?” “I thought you were.”“Let’s…not tell the Elders.” ", \
    "card_number": "199", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ddd62eb0-4699-4fb0-9b63-43769186b509", \
    "card_title": "Snufflegator", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_358_C2FM8V788JM5_en.png", \
    "card_text": "Skirmish. (When you use this creature to fight, it is dealt no damage in return.)", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Well, it’s a snufflegator, ain’t it?” –Dodger", \
    "card_number": "358", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "652c4e38-c4fa-4e30-8f8d-036e95249529", \
    "card_title": "Valdr", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_29_97VGG57XM738_en.png", \
    "card_text": "Valdr deals +2<D> while attacking an enemy creature on the flank.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Gather that Æmber! And you’re welcome.”", \
    "card_number": "29", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bb0dc3dc-b591-447d-a181-1dc4907e3eaa", \
    "card_title": "Troll", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_48_CPX86RFXW765_en.png", \
    "card_text": "Reap: Troll heals 3 damage.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "8", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Don’t feed it, it’ll go away.", \
    "card_number": "48", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9ed7d241-1ca3-4a2a-b067-bb44776f7d4b", \
    "card_title": "The Terror", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_101_9W755VJWMG92_en.png", \
    "card_text": "Play: If your opponent has no <A>, gain 2<A>.", \
    "traits": "Demon  Knight", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I once thought that these creatures could be redeemed. Now I know better.” –Champion Anaphiel", \
    "card_number": "101", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2d5666d0-5a93-4f75-b5f4-5085e4ee9b0f", \
    "card_title": "Squawker", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_178_7J9MG8W9F6GM_en.png", \
    "card_text": "Play: Ready a Mars creature or stun a non-Mars creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "178", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f6202f7a-e204-482c-91d6-e8d1f5117d28", \
    "card_title": "Yxili Marauder", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_203_8JJ739HGPCPC_en.png", \
    "card_text": "Yxili Marauder gets +1 power for each <A> on it.Play: Capture 1<A> for each friendly ready Mars creature.", \
    "traits": "Martian  Soldier", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "203", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0ef760a3-68b9-42a9-93fa-419ea171917b", \
    "card_title": "Smith", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_14_CV3QCM67C9GM_en.png", \
    "card_text": "Play: Gain 2<A> if you control more creatures than your opponent.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "14", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "45cf7fd4-6f40-4ee7-89ff-6f11ed80377a", \
    "card_title": "The Vaultkeeper", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_261_GRHXCM2HH6W2_en.png", \
    "card_text": "Your <A> cannot be stolen.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "4", \
    "armor": "1", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "261", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8604d465-8154-4354-9b77-9d4ad7eb3a02", \
    "card_title": "King of the Crag", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_38_VH6FGMM4HCH4_en.png", \
    "card_text": "Each enemy Brobnar creature gets –2 power.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "Overthrowing this king is an uphill battle. ", \
    "card_number": "38", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ccfd5033-ffd1-4d9a-b4be-2f9dc90095c8", \
    "card_title": "Treasure Map", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_284_Q7HHRF75F97J_en.png", \
    "card_text": "Play: If you have not played any other cards this turn, gain 3<A>. For the remainder of the turn, you cannot play cards.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "284", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c1494f7b-eb87-4c64-9405-871579af1f80", \
    "card_title": "Guilty Hearts", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_61_HM8RPQWR5X46_en.png", \
    "card_text": "Play: Destroy each creature with any <A> on it.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "C’mon, take it. You know you want to.", \
    "card_number": "61", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "116f4590-792e-4d5f-ab06-94dbf7ba85d3", \
    "card_title": "Sergeant Zakiel", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_258_96FR2MX3FJWF_en.png", \
    "card_text": "Play: You may ready and fight with a neighboring creature.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "4", \
    "armor": "1", \
    "rarity": "Common", \
    "flavor_text": "“Together!” ", \
    "card_number": "258", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ce019a46-29ac-4e54-a12e-ec9ad8e0d200", \
    "card_title": "Gorm of Omm", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_232_9XQ8F9638GX2_en.png", \
    "card_text": "Omni: Sacrifice Gorm of Omm. Destroy an artifact.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“An object, no matter how sacred, is just a thing.”", \
    "card_number": "232", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a8f25ae7-75f4-4768-94f0-87d62036516c", \
    "card_title": "Umbra", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_314_VHG44C64WFXQ_en.png", \
    "card_text": "Skirmish. (When you use this creature to fight, it is dealt no damage in return.)Fight: Steal 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“When the fightin’s done, the real work begins.” ", \
    "card_number": "314", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "740e0810-14e8-4278-bb44-e2e5c98184f9", \
    "card_title": "Halacor", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_355_XCPG4GRFR6PR_en.png", \
    "card_text": "Each friendly flank creature gains skirmish. (When you use a creature with skirmish to fight, it is dealt no damage in return.)", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Forget the others, have you seen the teeth on that one?!”", \
    "card_number": "355", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "37f09612-6ebb-4374-b598-ad0614f2d729", \
    "card_title": "Take Hostages", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_226_VMCJ79WHJVR2_en.png", \
    "card_text": "Play: For the remainder of the turn, each time a friendly creature fights, it captures 1<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "226", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "45d564a2-fcc9-4baa-8dc8-8e1a0fe2a37a", \
    "card_title": "Dextre", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_138_WVWFRR3PMG3H_en.png", \
    "card_text": "Play: Capture 1<A>.Destroyed: Put Dextre on top of your deck.", \
    "traits": "Human  Scientist", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "138", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9c613507-63b6-447b-9df5-a72a5d62fdf3", \
    "card_title": "Warsong", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_18_Q84XVC2GVCPR_en.png", \
    "card_text": "Play: For the remainder of the turn, gain 1<A> each time a friendly creature fights.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "18", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "35983b27-9674-448e-b066-63b0c6067668", \
    "card_title": "One Last Job", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_277_HGVF3P4J7PVJ_en.png", \
    "card_text": "Play: Purge each friendly Shadows creature. Steal 1<A> for each creature purged this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "277", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "be492d70-5c87-441e-8223-79fb2bce85c9", \
    "card_title": "Gateway to Dis", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_59_WW6PQP2CGM8H_en.png", \
    "card_text": "Play: Destroy each creature. Gain 3 chains.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "59", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3d6a02d0-b5c8-49be-93e4-dfdd5c1200eb", \
    "card_title": "Guardian Demon", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_88_W95JX5C22HW7_en.png", \
    "card_text": "Play/Fight/Reap: Heal up to 2 damage from a creature. Deal that amount of damage to another creature.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "88", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ba26515f-1705-45ba-ae42-dcb65685a0ec", \
    "card_title": "Tentacus", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_100_WQWQX27FH7M2_en.png", \
    "card_text": "Your opponent must pay you 1<A> in order to use an artifact.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "100", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "09101020-58c5-4d9f-b93b-7fb25d684ff0", \
    "card_title": "Burn the Stockpile", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_5_7WCGR88265CM_en.png", \
    "card_text": "Play: If your opponent has 7<A> or more, they lose 4<A>.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“If you can’t protect it, you don’t deserve it.” –Bilgum Avalanche", \
    "card_number": "5", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8e3d6aaf-e740-4924-86aa-57689c7cbdab", \
    "card_title": "Rocket Boots", \
    "house": "Logos", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_158_WMW7JV5QGXW6_en.png", \
    "card_text": "This creature gains, “Fight/Reap: If this is the first time this creature was used this turn, ready it.”", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "”Wheeeee!”", \
    "card_number": "158", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "89b647b4-74b1-4e74-9812-1581e088f32e", \
    "card_title": "Terms of Redress", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_227_VC53Q7XQ4C33_en.png", \
    "card_text": "Play: Choose a friendly creature to capture 2<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Thou shalt wear pants.”", \
    "card_number": "227", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "60f095d7-1816-4f14-88ec-04412ebde43b", \
    "card_title": "Veylan Analyst", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_156_4F6VP56RFQQ5_en.png", \
    "card_text": "Each time you use an artifact, gain 1<A>.", \
    "traits": "Cyborg  Scientist", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Logos are divided into two camps: Theorists and Mechanists. Each believes themselves to be superior to the other. ", \
    "card_number": "156", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "eb91efae-9fbe-46e2-a6f4-f93d290703a9", \
    "card_title": "Speed Sigil", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_293_6Q53JFFFWX8F_en.png", \
    "card_text": "The first creature played each turn enters play ready.", \
    "traits": "Power", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "293", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3c4513a3-260e-441f-8abf-b27c1c4e23ef", \
    "card_title": "Succubus", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_99_C63GPXC7XM83_en.png", \
    "card_text": "During their “draw cards” step, your opponent refills their hand to 1 less card.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "99", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "cd83ebe7-f961-4e5e-a00e-046d1be5e5d3", \
    "card_title": "Psychic Bug", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_149_GW4755VJMRRP_en.png", \
    "card_text": "Play/Reap: Look at your opponent’s hand.", \
    "traits": "Cyborg  Insect", \
    "amber": "1", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“I’d make more, but I discovered lesser minds aren’t worth reading.” – Biologician Moreau", \
    "card_number": "149", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "05193f38-c59c-4cf1-92e9-87e69b3bb76e", \
    "card_title": "Earthshaker", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_31_C7RGGJ9WG7XW_en.png", \
    "card_text": "Play: Destroy each creature with power 3 or lower.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Did you feel that?”", \
    "card_number": "31", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1983bc1e-a6e5-4fd4-b620-5e3d691c6851", \
    "card_title": "The Spirit’s Way", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_229_J233WVWH3WPR_en.png", \
    "card_text": "Play: Destroy each creature with power 3 or higher.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“The spirit is eternal. The flesh is weak. Let go the flesh, for your earthly strength is the greatest prison.” - The Last Book", \
    "card_number": "229", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1ca5f524-5a24-4a58-aacf-8204bdb46a32", \
    "card_title": "Neuro Syphon", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_116_CW34G484FFRV_en.png", \
    "card_text": "Play: If your opponent has more <A> than you, steal 1<A> and draw a card.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "116", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "40587911-1857-4947-87e7-867cfd7fbab4", \
    "card_title": "Shadow Self", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_310_C33C4J4W6726_en.png", \
    "card_text": "Shadow Self deals no damage when fighting.  Damage dealt to non-Specter neighbors is dealt to Shadow Self instead.", \
    "traits": "Specter", \
    "amber": "0", \
    "power": "9", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "310", \
    "expansion": "341", \
    "is_maverick": "True" \
  }',
  '{ \
    "id": "d5aabe84-2155-4e26-96bc-67e1cbaa1b9d", \
    "card_title": "Witch of the Wilds", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_347_44X322787G78_en.png", \
    "card_text": "During each turn in which Untamed is not your active house, you may play one Untamed card.", \
    "traits": "Beast  Witch", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "347", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3d3f65df-f6f5-44e3-979c-c9b3fda94ddd", \
    "card_title": "Booby Trap", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_268_6P3M73RFGR8W_en.png", \
    "card_text": "Play: Deal 4<D> to a creature that is not on a flank with 2<D> splash.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "268", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "253588cf-4fd5-4022-9c5c-a2b3693e21f0", \
    "card_title": "Poison Wave", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_280_3W4H8F78V4FG_en.png", \
    "card_text": "Play: Deal 2<D> to each creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Totally Tubular!” – Quixo the “Adventurer”", \
    "card_number": "280", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f65fea34-6c03-4d02-8434-02192dba72be", \
    "card_title": "Briar Grubbling", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_348_X9R7J6J64H38_en.png", \
    "card_text": "Hazardous 5. (Before this creature is attacked, deal 5<D> to the attacking enemy.)", \
    "traits": "Beast  Insect", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "Nature says “do not touch” in so many creative ways. ", \
    "card_number": "348", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f14abd8e-6732-4afe-8679-c1059fc31edf", \
    "card_title": "Twin Bolt Emission", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_124_636R5683G3F_en.png", \
    "card_text": "Play: Deal 2<D> to a creature and deal 2<D> to a different creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "124", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "23099339-dbe2-4b35-b26b-9dfb4c0fb35a", \
    "card_title": "Mack the Knife", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_302_RP49F4QFW3FM_en.png", \
    "card_text": "Elusive.You may use Mack the Knife as if it belonged to the active house.Action: Deal 1<D> to a creature. If this damage destroys that creature, gain 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "302", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c0ab6f27-619e-4b17-a623-c70f4cd84026", \
    "card_title": "Nature’s Call", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_329_387QVR6XM2M3_en.png", \
    "card_text": "Play: Return up to 3 creatures to their owners’ hands.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Gotta go, gotta go, gotta go...”", \
    "card_number": "329", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "429e5d71-40bc-4ff4-ae81-4d5c0c10d15e", \
    "card_title": "Dodger", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_308_4VWXF7969J9H_en.png", \
    "card_text": "Fight: Steal 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“What did you do, Tiny?” –Valdr", \
    "card_number": "308", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ac834ffc-01d5-4f35-8efe-982a746bdf3d", \
    "card_title": "Total Recall", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_179_69V9P82V8QCF_en.png", \
    "card_text": "Play: For each friendly ready creature, gain 1<A>. Return each friendly creature to your hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "179", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "78f1a306-5e1d-4155-90d4-a4f0646c5c4c", \
    "card_title": "Bigtwig", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_346_GFJP96HGWG24_en.png", \
    "card_text": "Bigtwig can only fight stunned creatures. Reap: Stun and exhaust a creature.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "346", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b68e10b3-275e-46b8-8227-fe02984ff525", \
    "card_title": "Replicator", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_150_8QGJM4R2RQQW_en.png", \
    "card_text": "Reap: Trigger the reap effect of another creature in play as if you controlled that creature. (That creature does not exhaust.)", \
    "traits": "Mutant", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "150", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "10715fd2-031a-47ca-9119-9b7b2ec1d2c0", \
    "card_title": "Fear", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_58_7RV7CX53R83P_en.png", \
    "card_text": "Play: Return an enemy creature to its owner’s hand.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "58", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2d0d0224-b954-47df-9bed-9161a7742815", \
    "card_title": "Library of the Damned", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_76_QR2M3J84P2GX_en.png", \
    "card_text": "Action: Archive a card.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "”This place takes the idea of losing yourself in a book to a whole new level.” – Doc Bookton", \
    "card_number": "76", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "62c1aa96-491a-4dbe-a5a3-6895d55e2311", \
    "card_title": "Key Hammer", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_66_RR9GCHVXP44C_en.png", \
    "card_text": "Play: If your opponent forged a key on their previous turn, unforge it. Your opponent gains 6<A>. ", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "What time is it?", \
    "card_number": "66", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "39f255c4-2ca4-4e7e-ba44-88ac0fcaeb1b", \
    "card_title": "Pit Demon", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_92_CRW34FMH3JF2_en.png", \
    "card_text": "Action: Steal 1<A>.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“They come from another world, they are pure evil made flesh and steel, and they lurk in the darkest corners of the land. Yes, I’m comfortable calling them ‘demons.’” –Science Officer Wu", \
    "card_number": "92", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8bd62dbc-77ac-400d-a31a-ca2e9c57728e", \
    "card_title": "Sample Collection", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_175_6FF5HPJG5FFV_en.png", \
    "card_text": "Play: Put an enemy creature into your archives for each key your opponent has forged. If any of these creatures leave your archives, they are put into their owner’s hand instead.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "175", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e52d5652-7365-4644-8b7f-e929035ca2c5", \
    "card_title": "Giant Sloth", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_354_9QP6FJMQC6W8_en.png", \
    "card_text": "You cannot use this card unless you have discarded an Untamed card from your hand this turn.Action: Gain 3<A>.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "354", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "953bbe23-df2b-4459-a3f6-beca7cd49a34", \
    "card_title": "Wild Wormhole", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_125_H2RWQ5VF7V7_en.png", \
    "card_text": "Play: Play the top card of your deck.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“But if we ever do recover the dataprobe, think of what we will learn!” ", \
    "card_number": "125", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "7402a14d-d397-4a4c-9415-b84e231e0aa6", \
    "card_title": "One Stood Against Many", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_223_PHQJHJ4P73J2_en.png", \
    "card_text": "Play: Ready and fight with a friendly creature 3 times, each time against a different enemy creature. Resolve these fights one at a time.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "223", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bc22a9d4-8d8d-4c56-a879-262b68d6704a", \
    "card_title": "Skippy Timehog", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_152_3PXCFH529CPG_en.png", \
    "card_text": "Play: Your opponent cannot use any cards next turn. (Cards can still be played and discarded.)", \
    "traits": "Mutant", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "152", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c225caa0-5e29-4b7d-8b89-aa7cbf3f4b14", \
    "card_title": "Drumble", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_82_HVV8PJ352J78_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Play: If your opponent has 7<A> or more, capture all of it.", \
    "traits": "Imp", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "82", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "753bfb51-4ba7-4c0a-b141-a5b6388498c0", \
    "card_title": "Battle Fleet", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_161_FPHCPHPMX8W8_en.png", \
    "card_text": "Play: Reveal any number of Mars cards from your hand. For each card revealed this way, draw 1 card.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "161", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c88c632e-743e-4f81-a9de-f61cddcbcaf5", \
    "card_title": "Virtuous Works", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_230_848RC8PR567J_en.png", \
    "card_text": "(Vanilla)", \
    "traits": "0", \
    "amber": "3", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "On the Crucible, there is no sanctimony. There is only Sanctumony.", \
    "card_number": "230", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9300339c-18a0-43f2-93cc-1937cfafb17b", \
    "card_title": "Irradiated Æmber", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_165_V5XGG2973F82_en.png", \
    "card_text": "Play: If your opponent has 6<A> or more, deal 3<D> to each enemy creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“They poisoned Mars. We must not let them do the same here.” –Eldest Bear", \
    "card_number": "165", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1283215c-3ea2-4d2b-9af4-452d7c0d57d9", \
    "card_title": "Scrambler Storm", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_122_HRQG3433R5R4_en.png", \
    "card_text": "Play: Your opponent cannot play action cards on their next turn.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "122", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9152cbad-d83f-4ee4-9846-87cc60d185f1", \
    "card_title": "Snudge", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_97_RM5XHC9QXGC5_en.png", \
    "card_text": "Fight/Reap: Return an artifact or flank creature to its owner’s hand.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "It’s only sensible to fear the dark. ", \
    "card_number": "97", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "189c881e-f5bc-4d2d-b97e-3166980aa1c9", \
    "card_title": "Special Delivery", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_292_C98PWPG7H4FC_en.png", \
    "card_text": "Omni: Sacrifice Special Delivery. Deal 3<D> to a flank creature. If this damage destroys that creature, purge it.", \
    "traits": "Item", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "292", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ef8b73a1-7655-4ab9-8da2-16db83836135", \
    "card_title": "Sigil of Brotherhood", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_236_VWG6GMX929C6_en.png", \
    "card_text": "Omni: Sacrifice Sigil of Brotherhood. For the remainder of the turn, you may use friendly Sanctum creatures.", \
    "traits": "Power", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "236", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "42fcdd0d-9be6-4602-ae47-1e8ef088751b", \
    "card_title": "Bulwark", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_238_4GJR4VPM7M26_en.png", \
    "card_text": "Each of Bulwark’s neighbors gets +2 armor.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "4", \
    "armor": "2", \
    "rarity": "Common", \
    "flavor_text": "“Let me be thy shield.”", \
    "card_number": "238", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d792387f-8392-49b3-ad7c-ccaf7552256f", \
    "card_title": "Hebe the Huge", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_36_73MRHJRCWXP4_en.png", \
    "card_text": "Play: Deal 2<D> to each other undamaged creature.", \
    "traits": "Giant  Knight", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "He’s much bigger in person. ", \
    "card_number": "36", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1ad71526-2782-4e56-a7b9-a0579fd63688", \
    "card_title": "Loot the Bodies", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_10_48CVW9F66MJ8_en.png", \
    "card_text": "Play: For the remainder of the turn, gain 1<A> each time an enemy creature is destroyed.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Loot the Bodies! Hit the Floor! Loot the Bodies! Hit the Floor!” –Brobnar War Chant", \
    "card_number": "10", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5a521238-f524-48e3-b121-40c16e1f7610", \
    "card_title": "Doc Bookton", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_139_678M74P9FW66_en.png", \
    "card_text": "Reap: Draw a card.", \
    "traits": "Human  Scientist", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Don’t worry, Momo. We’ll have this quantum death ray installed in no time.”", \
    "card_number": "139", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b13b68ab-489c-47bc-803e-e87792edb931", \
    "card_title": "Spectral Tunneler", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_133_FJGQFR6XJPHQ_en.png", \
    "card_text": "Action: Choose a creature. For the remainder of the turn, that creature is considered a flank creature and gains, “Reap: Draw a card.”", \
    "traits": "Item", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "133", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "cc44ca9a-6994-4897-9308-ff332cc8de57", \
    "card_title": "Phosphorus Stars", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_173_H5C875HQR3RC_en.png", \
    "card_text": "Play: Stun each non-Mars creature. Gain 2 chains.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Martians love da smell of dis spice, but it reminds me of Old Bruno’s feet.” - Dodger", \
    "card_number": "173", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "15f1a6f4-873f-4fa9-a080-7f01e72bbff1", \
    "card_title": "Relentless Whispers", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_281_MPVFFW3882CJ_en.png", \
    "card_text": "Play: Deal 2<D> to a creature. If this damage destroys that creature, steal 1<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "281", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1691e035-1eab-41de-ad18-26245265e64f", \
    "card_title": "EMP Blast", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_163_HWF789XR9CMR_en.png", \
    "card_text": "Play: Each Mars creature and each Robot creature is stunned. Each artifact is destroyed.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "163", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0cc7c1ea-5196-40ff-b408-f31997c8ab4d", \
    "card_title": "Crystal Hive", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_182_QC7VW6G544RQ_en.png", \
    "card_text": "Action: For the remainder of the turn, gain 1<A> each time a creature reaps.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Behold the glory of Nova Hellas!", \
    "card_number": "182", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bbd788cd-1f8d-4950-a7c1-bc7fe5c0d49a", \
    "card_title": "Oubliette", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_278_Q96GRFMV34CP_en.png", \
    "card_text": "Play: Purge a creature with power 3 or lower.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“I forgot we had this down here!”", \
    "card_number": "278", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "cda55db6-24e5-4e79-ac36-28482898dd4f", \
    "card_title": "Grey Monk", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_244_4V54R77GCW9M_en.png", \
    "card_text": "Each friendly creature gets +1 armor. Reap: Heal 2 damage from a creature.", \
    "traits": "Human  Priest", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "244", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "551a951f-39cc-4f13-8070-c0758066769c", \
    "card_title": "Subtle Maul", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_294_VJXHQQVX3C86_en.png", \
    "card_text": "Action: Your opponent discards a random card from their hand.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "294", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f7104dfc-2f68-4ed5-aa4d-5d8d73960066", \
    "card_title": "Hecatomb", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_63_4HRPQ25HC9QR_en.png", \
    "card_text": "Play: Destroy each Dis creature. Each player gains 1<A> for each creature they controlled that was destroyed this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "63", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9548d84e-2788-48d1-ba57-a54de15b289e", \
    "card_title": "Armageddon Cloak", \
    "house": "Sanctum", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_263_8WXW4FJ283XW_en.png", \
    "card_text": "This creature gains hazardous 2 and, “Destroyed: Fully heal this creature and destroy Armageddon Cloak instead.”", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "263", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "afa69425-4fe4-4e5b-a016-7c142ed0a849", \
    "card_title": "Seeker Needle", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_290_PQP9MHRG7W4H_en.png", \
    "card_text": "Action: Deal 1<D> to a creature. If this damage destroys that creature, gain 1<A>.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“What was that?”", \
    "card_number": "290", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "35bacc2e-48d6-4dac-a11c-5986e7416ddc", \
    "card_title": "Key of Darkness", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_273_VHRR6QWG3C3_en.png", \
    "card_text": "Play: Forge a key at +6<A> current cost. If your opponent has no <A>, forge a key at +2<A> current cost instead.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "273", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3c5c1881-486c-4911-a3ce-497ef258e8ba", \
    "card_title": "Batdrone", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_136_82MF23JH58M3_en.png", \
    "card_text": "Skirmish. (When you use this creature to fight, it is dealt no damage in return.)Fight: Steal 1<A>.", \
    "traits": "Robot", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "The worst part is the singing.", \
    "card_number": "136", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b45eaa7a-22cd-4cd1-96bd-a240b63bea9f", \
    "card_title": "Staunch Knight", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_259_F6VVWM6QHCRR_en.png", \
    "card_text": "Staunch Knight gets +2 power while it is on a flank.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "4", \
    "armor": "2", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "259", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d438faa9-7920-437a-8d1c-682fade5d350", \
    "card_title": "Coward’s End", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_7_CFRV9R6JG7P7_en.png", \
    "card_text": "Play: Destroy each undamaged creature. Gain 3 chains.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "7", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3cd0e141-6115-4719-a09e-8e0867fe567c", \
    "card_title": "Murmook", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_361_WHJM9F6QF2MF_en.png", \
    "card_text": "Your opponent’s keys cost +1<A>.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Look out for the pincers and don’t make it crabby. “ –Dr. Escotera", \
    "card_number": "361", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9a319f7f-62ac-46d2-9f1b-c8846e02589f", \
    "card_title": "Key Abduction", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_166_FC5W5F2668JC_en.png", \
    "card_text": "Play: Return each Mars creature to its owners hand. Then, you may forge a key at +9<A> current cost, reduced by 1<A> for each card in your hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "166", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5fc44836-83fd-4a10-af61-9168db728cc0", \
    "card_title": "Mindwarper", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_196_QG3353H2HJFM_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Action: Choose an enemy creature. It captures 1<A> from its own side.", \
    "traits": "Martian  Scientist", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "196", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "cdcef2b8-b0ca-4401-a386-dd3ae43d3f23", \
    "card_title": "Creeping Oblivion", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_56_4RHHVXPC3X35_en.png", \
    "card_text": "Play: Purge up to 2 cards from a discard pile.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“As far as oblivions go, it’s in my bottom three.” –Dr. Escotera", \
    "card_number": "56", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f96b20b3-df0e-4d43-a737-e7fa56ff690b", \
    "card_title": "Full Moon", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_323_CMWHFWX8HM52_en.png", \
    "card_text": "Play: For the remainder of the turn, gain 1<A> each time you play a creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "”Mathematically, a moon orbiting the Crucible is impossible.””Then what is that?!”", \
    "card_number": "323", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "cc7b8381-1418-45e5-b328-7c538fa73407", \
    "card_title": "Ritual of Balance", \
    "house": "Untamed", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_342_CCCJH6Q4C2GR_en.png", \
    "card_text": "Action: If your opponent has 6<A> or more, steal 1<A>.", \
    "traits": "Power", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Is balance a means to an end, or an end in itself? ", \
    "card_number": "342", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "34f85c32-4654-4177-9b9f-50825a58239e", \
    "card_title": "Mimicry", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_328_7H4999VX47XJ_en.png", \
    "card_text": "When you play this card, treat it as a copy of an action card in your opponent’s discard pile.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "It is said that if you travel far enough across the Crucible, you will eventually meet yourself.", \
    "card_number": "328", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "296dca38-e6d1-4eb3-9bdb-966e48ebedbf", \
    "card_title": "Lomir Flamefist", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_40_MH3839C78779_en.png", \
    "card_text": "Play: If your opponent has 7<A> or more, they lose 2<A>.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“I thought his name would turn out to be... metaphorical.” – Quixo the “Adventurer”", \
    "card_number": "40", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "22f59906-7f34-43e9-8285-836765e2c418", \
    "card_title": "Way of the Wolf", \
    "house": "Untamed", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_370_J935FXX4XCJW_en.png", \
    "card_text": "This creature gains skirmish.  (When you use this creature to fight, it is dealt no damage in return.)", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "370", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f05fadd1-0c4e-4242-9386-c5c6d112e124", \
    "card_title": "Biomatrix Backup", \
    "house": "Mars", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_208_77VHC8FXXP27_en.png", \
    "card_text": "This creature gains, “Destroyed: You may put this creature into its owners archives.” ", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "208", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bdbb4933-b2f1-403b-986d-bbdec111b76b", \
    "card_title": "Commpod", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_181_MXX6XH3QQRCV_en.png", \
    "card_text": "Action: Reveal any number of Mars cards from your hand. For each card revealed this way, you may ready one Mars creature.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "181", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "56252b23-94a4-46ac-a566-be6793ecbdfe", \
    "card_title": "Blinding Light", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_213_P3Q4X37QMP7V_en.png", \
    "card_text": "Play: Choose a house. Stun each creature of that house.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "213", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "4a996715-f2c1-46e5-b80e-f285c1d36439", \
    "card_title": "Bad Penny", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_296_QF774F23G6MR_en.png", \
    "card_text": "Destroyed: Return Bad Penny to your hand.", \
    "traits": "Human  Thief", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "A Bad Penny saved is a Bad Penny earned.", \
    "card_number": "296", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "74422031-b763-4f04-9f90-3f580ad69d3f", \
    "card_title": "Silvertooth", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_311_69G639M8F4F2_en.png", \
    "card_text": "Silvertooth enters play ready.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "If you see teeth gleaming in the dark, it’s already too late.", \
    "card_number": "311", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0e5e8a55-ab05-44be-8637-8362974dad8b", \
    "card_title": "Grabber Jammer", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_193_PXQ9229CMHHP_en.png", \
    "card_text": "Your opponent’s keys cost +1<A>.Fight/Reap: Capture 1<A>.", \
    "traits": "Robot", \
    "amber": "0", \
    "power": "4", \
    "armor": "1", \
    "rarity": "Common", \
    "flavor_text": "“Mine!”", \
    "card_number": "193", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3bdfeeec-0424-469b-b169-8e5ad6821e95", \
    "card_title": "Bilgum Avalanche", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_28_VP32QGRWMRW3_en.png", \
    "card_text": "After you forge a key, deal 2<D> to each enemy creature.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Some call her ‘warleader.’ Some call her ‘demon.’ I just call her ‘Avalanche.’” –Dodger", \
    "card_number": "28", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9ba24b81-1887-46fd-9ec4-d8851af7e574", \
    "card_title": "Pandemonium", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_68_52H2XVR2J45G_en.png", \
    "card_text": "Play: Each undamaged creature captures 1<A> from its opponent. ", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "68", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d4f666db-302f-43d0-b0af-bd03071f92ce", \
    "card_title": "Ganger Chieftain", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_33_FGH2M9G9W45J_en.png", \
    "card_text": "Play: You may ready and fight with a neighboring creature.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "It takes two to fight, but more is better. ", \
    "card_number": "33", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "211c5213-7838-4292-b9c4-fb3a663898ee", \
    "card_title": "Yxilx Dominator", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_205_GPCHG3XCV2MV_en.png", \
    "card_text": "Taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)Yxilx Dominator enters play stunned. ", \
    "traits": "Robot", \
    "amber": "0", \
    "power": "9", \
    "armor": "1", \
    "rarity": "Common", \
    "flavor_text": "Core power online. Stand by for domination. ", \
    "card_number": "205", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c5f7e033-f62e-442e-97a1-b23b47cde1e8", \
    "card_title": "Lights Out", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_274_P4W2FF886X6V_en.png", \
    "card_text": "Play: Return 2 enemy creatures to their owner’s hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "274", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2ec5cbf6-3c41-41ef-9cb7-33a0601fd607", \
    "card_title": "Quixo the “Adventurer”", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_144_7XJ66GGGX9P3_en.png", \
    "card_text": "Skirmish. (When you use this creature to fight, it is dealt no damage in return.)Fight: Draw a card.", \
    "traits": "Human  Scientist", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“...I’ll leave this part out of the memoir.”", \
    "card_number": "144", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "817edf75-e91d-4b18-8c5a-d33e3759aeae", \
    "card_title": "Shooler", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_96_4J8576237M3X_en.png", \
    "card_text": "Play: If your opponent has 4<A> or more, steal 1<A>.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Demons only take, never give.” - The Sanctified Scroll", \
    "card_number": "96", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f79ad4c9-4c3c-461c-b0e7-c949bb46d270", \
    "card_title": "Blood of Titans", \
    "house": "Brobnar", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_50_3GJFRPFVMF7M_en.png", \
    "card_text": "This creature gets +5 power.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Blood of Giants? Why stop there?”  –Pingle Who Annoys", \
    "card_number": "50", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "02c7533e-98ac-48a0-94e4-621555443c8d", \
    "card_title": "Whispering Reliquary", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_237_MMHF7CR6FMJ2_en.png", \
    "card_text": "Action: Return an artifact to its owners hand.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "237", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "df4257dc-ac9c-40cf-ba1b-a77fffe960df", \
    "card_title": "Duskrunner", \
    "house": "Shadows", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_316_P6MMX3WR7MC6_en.png", \
    "card_text": "This creature gains, “Reap: Steal 1<A>.” ", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Call me Night-Haunter and Duskrunner, call me Who-Goes-There? and Just-The-Wind.” –‘The First Thief’, a Shadows children’s tale ", \
    "card_number": "316", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "98fca3bb-b74c-4563-876b-7c9e942e8254", \
    "card_title": "Cooperative Hunting", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_319_75P9X98FJQHV_en.png", \
    "card_text": "Play: Deal 1<D> for each friendly creature in play. You may divide this damage among any number of creatures.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“It sure beats uncooperative hunting!”", \
    "card_number": "319", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e1312fbf-c297-4d9f-b403-2d892271de62", \
    "card_title": "Smaaash", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_46_MXF2PV92XQPW_en.png", \
    "card_text": "Play: Stun a creature.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I’m not sure he knows any other words.” ", \
    "card_number": "46", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "365b2432-0b7f-4f67-9fa6-e4b726de5c4e", \
    "card_title": "Flame-Wreathed", \
    "house": "Dis", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_106_4G49CMC5XCX4_en.png", \
    "card_text": "This creature gets +2 power and gains hazardous 2. (Before this creature is attacked, deal 2<D> to the attacking enemy.)", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "106", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0bd7cbf7-7d34-4a45-9049-217146229968", \
    "card_title": "Orbital Bombardment", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_172_4CX23PH9H69J_en.png", \
    "card_text": "Play: Reveal any number of Mars cards from your hand. For each card revealed this way, deal 2<D> to a creature. (You may choose a different creature each time.)", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "172", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "17e9dbd4-53cb-4c75-bdad-48e1550ff1e7", \
    "card_title": "Key to Dis", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_74_RP2JCG669GWQ_en.png", \
    "card_text": "Omni: Sacrifice Key to Dis. Destroy each creature.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "74", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bc5df4f6-a9db-4b05-8a65-6c51c01b7b3e", \
    "card_title": "Smiling Ruth", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_312_V2H6733WRV33_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: If you forged a key this turn, take control of an enemy flank creature.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "312", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3a0c1861-3d38-4167-b0c1-afaa9cbe5e50", \
    "card_title": "Noddy the Thief", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_306_6374XF5G5XMR_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Action: Steal 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "306", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "4149fd67-12db-4ef6-9718-135c66ffefd3", \
    "card_title": "Sound the Horns", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_15_8HXH9WQ5P4V4_en.png", \
    "card_text": "Play: Discard cards from the top of your deck until you either discard a Brobnar creature or run out of cards. If you discarded a Brobnar creature this way, put it into your hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "15", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "74d1da3a-9d90-43ea-8ead-f7968c4d562d", \
    "card_title": "Regrowth", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_332_R2GQWP4RXCM4_en.png", \
    "card_text": "Play: Return a creature from your discard pile to your hand.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Deep in the heart of every bear, one can find...another bear.” -Dr. Escotera", \
    "card_number": "332", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2a6e3e67-3c67-48c8-8ff3-b16896b14550", \
    "card_title": "Silent Dagger", \
    "house": "Shadows", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_318_CGCC5XW8VF69_en.png", \
    "card_text": "This creature gains, “Reap: Deal 4<D> to a flank creature.”", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "318", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "1ef96099-4703-4883-9c55-9102e829797a", \
    "card_title": "Shield of Justice", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_225_8WXGHPQGX9V_en.png", \
    "card_text": "Play: For the remainder of the turn, each friendly creature cannot be dealt damage.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "225", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a0f1146a-6df3-4568-8fb1-d6845615d833", \
    "card_title": "Follow the Leader", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_8_4CGG6P6JQ44W_en.png", \
    "card_text": "Play: For the remainder of the turn, each friendly creature may fight.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "8", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "e9aefff3-acef-41e3-8258-182588f2b24c", \
    "card_title": "Unguarded Camp", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_17_64F73PR27H7P_en.png", \
    "card_text": "Play: For each creature you have in excess of your opponent, a friendly creature captures 1<A>. Each creature cannot capture more than 1<A> this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "17", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8754c688-6d87-4372-bbec-349e4e4bdded", \
    "card_title": "Hidden Stash", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_271_3CCM38JM8932_en.png", \
    "card_text": "Play: Archive a card.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Now where did you put that...”", \
    "card_number": "271", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3a3783ea-b5c4-407d-b3c7-0003c562a9aa", \
    "card_title": "Hunting Witch", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_367_54RJ37XJPQ2_en.png", \
    "card_text": "Each time you play another creature, gain 1<A>.", \
    "traits": "Human  Witch", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“What is it? Is it food?”", \
    "card_number": "367", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "86db8510-2854-440b-8ee5-559855bb7d2c", \
    "card_title": "Gauntlet of Command", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_22_5F6F47CPQM7J_en.png", \
    "card_text": "Action: Ready and fight with a friendly creature.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I said ‘take me to your leader’ and got a fist to the face.”  –Captain Val Jericho", \
    "card_number": "22", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "91292e0d-e49e-485f-b19d-f066b1ff388a", \
    "card_title": "Macis Asp", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_301_5G45CCCH6W5J_en.png", \
    "card_text": "Skirmish. (When you use this creature to fight, it is dealt no damage in return.)Poison. (Any damage dealt by this creature’s power during a fight destroys the damaged creature.)", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "301", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5a1ee413-4b39-467f-a0bf-e5935f1edf9b", \
    "card_title": "Dr. Escotera", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_140_GGR9WQGX52CC_en.png", \
    "card_text": "Play: Gain 1<A> for each forged key your opponent has.", \
    "traits": "Cyborg  Scientist", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Interesting reaction, but what does it mean?”", \
    "card_number": "140", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "050b35ae-461a-4630-a8df-a60b2652fc2b", \
    "card_title": "Wardrummer", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_49_3J962PMQJRJ6_en.png", \
    "card_text": "Play: Return each other friendly Brobnar creature to your hand.", \
    "traits": "Goblin", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "49", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d837b336-ae38-405b-b9d3-fc8583c770a0", \
    "card_title": "Fogbank", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_322_9RH25FHMC26H_en.png", \
    "card_text": "Play: Your opponent cannot use creatures to fight on their next turn.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "322", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bec84d69-68f0-456c-a7bd-9f1e94d55a22", \
    "card_title": "Experimental Therapy", \
    "house": "Logos", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_157_4FCPWQMVGPC_en.png", \
    "card_text": "This creature belongs to all houses.Play: Stun and exhaust this creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“This is for our research, so be honest. How do you feel?”", \
    "card_number": "157", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9644c85a-12a7-44ff-a8bb-877dddb46995", \
    "card_title": "Three Fates", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_71_5P29489P6443_en.png", \
    "card_text": "Play: Destroy the 3 most powerful creatures. ", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Destitution. Dereliction. Defenestration.”", \
    "card_number": 71, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f5cbdafd-487d-453b-96bb-a09378d1359f", \
    "card_title": "Charge!", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_214_X3RQF994MG6R_en.png", \
    "card_text": "Play: For the remainder of the turn, each creature you play gains, “Play: Deal 2<D> to an enemy creature.”", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "214", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "23a96d73-4eb2-4c45-9550-8207145eb587", \
    "card_title": "Lash of Broken Dreams", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_75_5WF77V8WRRPP_en.png", \
    "card_text": "Action: Keys cost +3<A> during your opponent’s next turn.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“At first, I thought that nothing could harm an Archon.”  –Captain Val Jericho", \
    "card_number": "75", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "6b113c63-c8e0-4c52-9973-b94263d2bf0d", \
    "card_title": "Stealer of Souls", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_98_JJGJFX44Q6GF_en.png", \
    "card_text": "After an enemy creature is destroyed fighting Stealer of Souls, purge that creature and gain 1<A>.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "98", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "30df482b-4066-4d11-b357-75abc4ead329", \
    "card_title": "Ammonia Clouds", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_160_VQMVCX37C6XQ_en.png", \
    "card_text": "Play: Deal 3<D> to each creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Partly cloudy with a chance of acid rain.", \
    "card_number": "160", \
    "expansion": "341", \
    "is_maverick": "True" \
  }',
  '{ \
    "id": "fc3d397a-3a51-4963-940c-6b43221b7667", \
    "card_title": "Bumpsy", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_30_X82H79CQ6XH6_en.png", \
    "card_text": "Play: Your opponent loses 1<A>.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Whatever he doesn’t like, he breaks. He doesn’t like anything.", \
    "card_number": "30", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "11663693-8a10-4783-9f89-47f43c49bfa3", \
    "card_title": "Shadow Self", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_310_C33C4J4W6726_en.png", \
    "card_text": "Shadow Self deals no damage when fighting.  Damage dealt to non-Specter neighbors is dealt to Shadow Self instead.", \
    "traits": "Specter", \
    "amber": "0", \
    "power": "9", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": 310, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8c763540-bb69-47aa-be43-4a8ace89864c", \
    "card_title": "Bouncing Deathquark", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_107_X3G2GX9QW86R_en.png", \
    "card_text": "Play: Destroy an enemy creature and a friendly creature. You may repeat this effect as many times as you like, as long as it is possible to repeat the entire effect.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "107", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "eec2bfbf-d019-4a7f-a0fa-2b8c8f16cd8d", \
    "card_title": "Lord Golgotha", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_252_VXMWR7MR5CW9_en.png", \
    "card_text": "Before Fight: Deal 3<D> to each neighbor of the creature Lord Golgotha fights.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "5", \
    "armor": "2", \
    "rarity": "Rare", \
    "flavor_text": "“Enlightened” does not mean “peaceful.”", \
    "card_number": "252", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "dc0ba4ea-6f6e-475f-899c-88ad45ccae94", \
    "card_title": "Niffle Ape", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_363_3RCHH4F7H4XF_en.png", \
    "card_text": "While Niffle Ape is attacking, ignore taunt and elusive.", \
    "traits": "Beast  Niffle", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Did it just say Niffle?” –Captain Val Jericho", \
    "card_number": "363", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "3b1f7db9-1c5a-4e15-a771-a4a45bd8fb0e", \
    "card_title": "Mooncurser", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_304_3QMPPH48XHXJ_en.png", \
    "card_text": "Skirmish. Poison.Fight: Steal 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "Dark of night, thieves’ delight.", \
    "card_number": "304", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "78f28f49-8edb-4333-bd22-308a229f200f", \
    "card_title": "Imperial Traitor", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_272_9W52QM6RM94X_en.png", \
    "card_text": "Play: Look at your opponent’s hand. You may choose and purge a Sanctum card in it.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "272", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "63f67670-16fb-4381-a859-c47920a847a6", \
    "card_title": "The Warchest", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_27_5G98X8WW3V6G_en.png", \
    "card_text": "Action: Gain 1<A> for each enemy creature that was destroyed in a fight this turn.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "It doesn’t matter what the treasure is, only how it was won.", \
    "card_number": "27", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "03c4165e-a0bb-4fd5-b6a8-e3d9aec0551e", \
    "card_title": "Urchin", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_315_7MCP67W84FWX_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Play: Steal 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "315", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "762973ae-27da-448f-93f4-2a9bc4ef5f35", \
    "card_title": "Protectrix", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_254_W9QVJ9XWF94R_en.png", \
    "card_text": "Reap: You may fully heal a creature. If you do, that creature cannot be dealt damage for the remainder of the turn.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "254", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0c3231e1-1230-4e7d-890e-6d3149125de2", \
    "card_title": "Headhunter", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_35_M3H9MVCF63W7_en.png", \
    "card_text": "Fight: Gain 1<A>.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I mean, I think it’s a head...”", \
    "card_number": "35", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f2c71c05-7a23-4465-8a89-82ab8e258a68", \
    "card_title": "Rogue Ogre", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_45_HWPQ963W848R_en.png", \
    "card_text": "At the end of your turn, if you played exactly one card this turn, Rogue Ogre heals 2 damage and captures 1<A>.", \
    "traits": "Giant  Mutant", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“I like to think of it as a Roguere.” –Dodger", \
    "card_number": "45", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9b079369-608a-430a-9b08-9f2d6b32435b", \
    "card_title": "Ammonia Clouds", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_160_VQMVCX37C6XQ_en.png", \
    "card_text": "Play: Deal 3<D> to each creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Partly cloudy with a chance of acid rain.", \
    "card_number": 160, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a8e3dfc2-6cf2-42a2-97d3-99592ae7da9a", \
    "card_title": "Honorable Claim", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_219_P9V3P7F8849M_en.png", \
    "card_text": "Play: Each friendly Knight creature captures 1<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“As your spirit is holy, so æmber, which is the spirit of the earth, is holy.” - The Sanctified Scroll", \
    "card_number": "219", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2dc8f61d-c691-4204-b2b5-5115790d0ba8", \
    "card_title": "Inka the Spider", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_356_QW7GHMXR5HJ8_en.png", \
    "card_text": "Poison. (Any damage dealt by this creature’s power during a fight destroys the damaged creature.)Play/Reap: Stun a creature.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Let me weave you a tale.”", \
    "card_number": "356", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "eaae7cd5-62bd-4438-aedb-8309974535df", \
    "card_title": "Ulyq Megamouth", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_200_CM3V8FW8C2PG_en.png", \
    "card_text": "Fight/Reap: Use a friendly non-Mars creature.", \
    "traits": "Martian  Scientist", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“GLORY BE TO MARS!” ", \
    "card_number": "200", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "7c60d913-803f-4b84-8e84-cf931d70659c", \
    "card_title": "Pocket Universe", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_131_Q67W5PMV8768_en.png", \
    "card_text": "You may spend <A> on Pocket Universe when forging keys.Action: Move 1<A> from your pool to Pocket Universe.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "131", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ff104cf4-f99d-4021-a570-dd949e559e97", \
    "card_title": "Zyzzix the Many", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_207_C938GRH2C993_en.png", \
    "card_text": "Fight/Reap: You may reveal a creature from your hand. If you do, archive it and Zyzzix the Many gets three +1 power counters.", \
    "traits": "Martian  Soldier", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "207", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f51e8ec0-ab0e-46a8-a5f5-680039d6e664", \
    "card_title": "Interdimensional Graft", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_112_VWRCJXGG9J99_en.png", \
    "card_text": "Play: If an opponent forges a key on their next turn, they must give you their remaining <A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "112", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "29eafbc7-7fc5-4239-b2a7-8bc90df1fc0f", \
    "card_title": "Firespitter", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_32_PVV2WC6R6QWP_en.png", \
    "card_text": "Before Fight: Deal 1<D> to each enemy creature.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "5", \
    "armor": "1", \
    "rarity": "Common", \
    "flavor_text": "Guess how he got that name.", \
    "card_number": "32", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "750a9323-9c07-4ae7-be5e-79367b4a2a8d", \
    "card_title": "Annihilation Ritual ", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_72_H2HJ8R9HF5C_en.png", \
    "card_text": "When a creature would enter a discard pile from play, it is purged instead.", \
    "traits": "Power", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "72", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "36b15919-4938-4e83-b57e-ae3a6b83cbbd", \
    "card_title": "Raiding Knight", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_255_HX7GPH8C78C2_en.png", \
    "card_text": "Play: Capture 1<A>.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "4", \
    "armor": "2", \
    "rarity": "Common", \
    "flavor_text": "“Sacred Æmber is not meant for hands such as thine.” ", \
    "card_number": "255", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f6d5781c-83a4-4070-bf98-085e81063c26", \
    "card_title": "Miasma", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_275_5HGPVQG4QF5H_en.png", \
    "card_text": "Play: Your opponent skips the “forge a key” step on their next turn.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "275", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "dc6344a9-0486-4926-a820-d99eb2151c7f", \
    "card_title": "Ancient Bear", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_345_V9F9WCXJ5VHR_en.png", \
    "card_text": "Assault 2.(Before this creature attacks, deal 2<D> to the attacked enemy.)", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "5", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "”And when I say ‘bear,’ I mean it in the loosest of terms.” – Quixo the “Adventurer”", \
    "card_number": "345", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d988a134-ff29-40f7-bac7-3fd49fe525f8", \
    "card_title": "Nexus", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_305_7QJVVWFQJPHJ_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: Use an opponent’s artifact as if it were yours.", \
    "traits": "Cyborg  Thief", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "305", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a8a3578c-7a61-4e15-90ac-483daf2aff16", \
    "card_title": "Vezyma Thinkdrone", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_202_99C5PXMWC2M7_en.png", \
    "card_text": "Reap: You may archive a friendly creature or artifact from play.", \
    "traits": "Martian  Scientist", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "Nothing helps me think like wanton destruction.", \
    "card_number": "202", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f97316b0-75a4-45a4-8735-15e72cc1568c", \
    "card_title": "Dust Imp", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_83_9V7X379WFV8V_en.png", \
    "card_text": "Destroyed: Gain 2<A>.", \
    "traits": "Imp", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "When the demon’s away, the imps will play.", \
    "card_number": "83", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "23508e89-0431-45d1-9692-192c6dffeb5a", \
    "card_title": "Ghostly Hand", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_270_5MJXHHP7VWWG_en.png", \
    "card_text": "Play: If your opponent has exactly 1<A>, steal it.", \
    "traits": "0", \
    "amber": "2", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I felt a little bad stealing from the Microputians, but only a little.” – Noddy the Thief", \
    "card_number": "270", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a2d750fc-aea3-48a6-ba18-5358fff7148e", \
    "card_title": "Francus", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_243_PFW5PH796X2W_en.png", \
    "card_text": "After an enemy creature is destroyed fighting Francus, Francus captures 1<A>.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "6", \
    "armor": "1", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "243", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ab58367b-51db-4ba0-926e-e4d562f7e4bd", \
    "card_title": "Hayyel the Merchant", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_245_7MHFM8Q84QMX_en.png", \
    "card_text": "Each time you play an artifact, gain 1<A>.", \
    "traits": "Human  Merchant", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“The Enlightened are above haggling. Me, on the other hand…”", \
    "card_number": "245", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "892c0a68-5213-48b2-8883-2ac3c97ac83c", \
    "card_title": "Arise!", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_54_F9GHFCWJ233R_en.png", \
    "card_text": "Play: Choose a house. Return each creature of that house from your discard pile to your hand. Gain 1 chain.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": 54, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "261b851a-84eb-44a7-828d-6b7599fecaaf", \
    "card_title": "Sanctum Guardian", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_256_43Q78X6H273_en.png", \
    "card_text": "Taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)Fight/Reap: Swap Sanctum Guardian with another friendly creature in your battleline.", \
    "traits": "Knight  Spirit", \
    "amber": "0", \
    "power": "6", \
    "armor": "1", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "256", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0186f94c-68df-4d5c-9338-9e918affe313", \
    "card_title": "Bait and Switch", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_267_VHQ67J5MWQV5_en.png", \
    "card_text": "Play: If your opponent has more <A> than you, steal 1<A>. Repeat this cards effect if your opponent still has more <A> than you.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“Heckuva deal.” – Old Bruno", \
    "card_number": "267", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "71274e08-79b6-469b-9426-8af07d582704", \
    "card_title": "Carlo Phantom", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_298_5PGPFVJF9292_en.png", \
    "card_text": "Elusive. Skirmish.Each time you play an artifact, steal 1<A>.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Give me half a chance an’ I’ll steal the whole of it.”", \
    "card_number": "298", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "68e2188c-4002-43d4-9fe1-0262df26c33f", \
    "card_title": "Tremor", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_16_HQJ525M2CVG9_en.png", \
    "card_text": "Play: Stun a creature and each of its neighbors.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "16", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "96548d93-b318-40e3-9f5c-3297c8070ebd", \
    "card_title": "Dominator Bauble", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_73_QRQ93X7RG4J9_en.png", \
    "card_text": "Action: Use a friendly creature.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“I know I shouldn’t’a nicked it, but ‘twere so…shiny. –Noddy the Thief", \
    "card_number": "73", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "728fcd16-1625-48f6-8633-567b9d4b7a2f", \
    "card_title": "The Howling Pit", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_135_GVHX66578HV5_en.png", \
    "card_text": "During their “draw cards” step, each player refills their hand to 1 additional card.", \
    "traits": "Location", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": 135, \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c578fa39-fe35-4a9f-844e-113fc47dc6f2", \
    "card_title": "Ritual of the Hunt", \
    "house": "Untamed", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_343_MWRP2VMRJ7R7_en.png", \
    "card_text": "Omni: Sacrifice Ritual of the Hunt. For the remainder of the turn, you may use friendly Untamed creatures.", \
    "traits": "Power", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "343", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0cdeb7ca-3071-472f-829c-6dc6ec0824b2", \
    "card_title": "Perilous Wild", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_331_QF7G64HGJ35G_en.png", \
    "card_text": "Play: Destroy each elusive creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "The Architects took great pains to make the Crucible inhabitable for creatures from worlds across the galaxy. But they didn’t make it safe. ", \
    "card_number": "331", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "6378dc4a-fdb8-4580-a85f-1b6bcd158615", \
    "card_title": "Iron Obelisk", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_23_G489GRF3RCV2_en.png", \
    "card_text": "Your opponent’s keys cost +1<A> for each friendly damaged Brobnar creature.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "23", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "eef21950-66f9-4535-b126-34d634fe524d", \
    "card_title": "Scout", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_334_W8RW3VC8V333_en.png", \
    "card_text": "Play: For the remainder of the turn, up to 2 friendly creatures gain skirmish. Then, fight with those creatures one at a time.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "334", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "98c0c7b0-59b4-48f2-8144-39d1d47bec7d", \
    "card_title": "Sacrificial Altar", \
    "house": "Dis", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_78_Q7JWX2HW28FX_en.png", \
    "card_text": "Action: Purge a friendly Human creature from play. If you do, play a creature from your discard pile.", \
    "traits": "Location", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "78", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "013def76-9edc-495c-bc35-af6210192f6b", \
    "card_title": "Lupo the Scarred", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_359_RX86WM6596MC_en.png", \
    "card_text": "Skirmish. (When you use this creature to fight, it is dealt no damage in return.) Play: Deal 2<D> to an enemy creature.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Nothing that big should be able to move that silently.”  –Lost Lukas Lawrence", \
    "card_number": "359", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "315b5cb9-b5a6-42af-9f32-a89079ab42cc", \
    "card_title": "Way of the Bear", \
    "house": "Untamed", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_369_3822X74RGM8F_en.png", \
    "card_text": "This creature gains assault 2. (Before this creature attacks, deal 2<D> to the attacked enemy.)", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "369", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f5ec01ee-17d0-49fe-8d42-92fffcbe9a27", \
    "card_title": "Chota Hazri", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_349_CGCR6RQRM629_en.png", \
    "card_text": "Play: Lose 1<A>. If you do, you may forge a key at current cost.", \
    "traits": "Human  Witch", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Plenty of machines in the wild. Some of ‘em’s even alive.” ", \
    "card_number": "349", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "12acf848-7838-4668-a2df-620e67e6d916", \
    "card_title": "Mighty Javelin", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_24_CG2485CM5HV4_en.png", \
    "card_text": "Omni: Sacrifice Mighty Javelin. Deal 4<D> to a creature.", \
    "traits": "Weapon", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "24", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c69a4a22-7d34-4719-9d64-a0a691d60164", \
    "card_title": "Kindrith Longshot", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_357_CJVF7978M9W3_en.png", \
    "card_text": "Elusive. Skirmish.Reap: Deal 2<D> to a creature.", \
    "traits": "Human  Ranger", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "357", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "040b3c05-428a-47c9-afc9-6fc65905462f", \
    "card_title": "Duma the Martyr", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_242_8X9FFJ5RC99F_en.png", \
    "card_text": "Destroyed: Fully heal each other friendly creature and draw 2 cards.", \
    "traits": "Human", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Remember me.”  - Squire Duma, at the Battle for the Gate of Hope.", \
    "card_number": "242", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "746fd4a8-ae4d-4a28-8834-655923558721", \
    "card_title": "Grommid", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_194_J7HVR74PWP6W_en.png", \
    "card_text": "You cannot play creatures.  After an enemy creature is destroyed fighting Grommid, your opponent loses 1<A>.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "10", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "194", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a7621926-1f0f-4d56-b2aa-15efdded15a9", \
    "card_title": "Fertility Chant", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_321_43VFXWMHFR7M_en.png", \
    "card_text": "Play: Your opponent gains 2<A>.", \
    "traits": "0", \
    "amber": "4", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "321", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a18f4950-87cd-4ebc-9096-9e82df8c6e88", \
    "card_title": "Mighty Lance", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_221_GHP2MR29293_en.png", \
    "card_text": "Play: Deal 3<D> to a creature and 3<D> to a neighbor of that creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "221", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c29141ad-cc05-4d79-b3db-eb391808c29e", \
    "card_title": "Restringuntus", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_94_F38PVXG83G8X_en.png", \
    "card_text": "Play: Choose a house. Your opponent cannot choose that house as their active house until Restringuntus leaves play.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "94", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "439d9d6e-7abf-4a7a-83d5-77060b5668cc", \
    "card_title": "Flaxia", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_352_JVPG4792RH9C_en.png", \
    "card_text": "Play: Gain 2<A> if you control more creatures than your opponent.", \
    "traits": "Faerie", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "352", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "149e6b52-5d65-4fcb-9cc5-f57b4a16ba58", \
    "card_title": "Vespilon Theorist", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_155_4XJVMF643M6C_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: Choose a house. Reveal the top card of your deck. If it is of that house, archive it and gain 1<A>. Otherwise, discard it.", \
    "traits": "Cyborg  Scientist", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "155", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "63a22a26-ad71-4fa9-908d-4a13d6ab8359", \
    "card_title": "A Fair Game", \
    "house": "Dis", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_53_CJXQV688FHG_en.png", \
    "card_text": "Play: Discard the top card of your opponent’s deck and reveal their hand. You gain 1<A> for each card of the discarded card’s house revealed this way. Your opponent repeats the preceding effect on you.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "53", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c68fa80b-08b2-4153-88c1-9e56aac487fe", \
    "card_title": "Pile of Skulls", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_25_M6WXP2FVXH53_en.png", \
    "card_text": "Each time an enemy creature is destroyed during your turn, a friendly creature captures 1<A>.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "25", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2b5233c4-7da4-497a-b938-3eb72dabaaf1", \
    "card_title": "Niffle Queen", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_364_F69VCQPX95RV_en.png", \
    "card_text": "Each other friendly Beast creature gets +1 power.Each other friendly Niffle creature gets +1 power.", \
    "traits": "Beast  Niffle", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "364", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0fba4ba8-317b-44c0-a51e-0a06bdb770d3", \
    "card_title": "Swap Widget", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_189_Q8749GRQ2RRW_en.png", \
    "card_text": "Action: Return a ready friendly Mars creature to your hand. If you do, put a Mars creature with a different name from your hand into play, then ready it.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "189", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0077d73e-273c-4e89-adda-eb28dda8148e", \
    "card_title": "Oath of Poverty", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_222_QR5CWH4G69H3_en.png", \
    "card_text": "Play: Destroy each of your artifacts. Gain 2<A> for each artifact destroyed this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "222", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "93a7d1e6-b66e-4c6b-86e3-3ea230a4d768", \
    "card_title": "Invasion Portal", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_185_6C5RX4PMJ5R2_en.png", \
    "card_text": "Action: Discard cards from the top of your deck until you discard a Mars creature or run out of cards. If you discard a Mars creature this way, put it into your hand.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "185", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "57f8a873-414b-4c77-be9a-15561c76f719", \
    "card_title": "Banner of Battle", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_20_3FQVR3V3CR7F_en.png", \
    "card_text": "Each friendly creature gets +1 power.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "20", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "4064612e-602e-46c1-b8eb-8adda1cfd0d0", \
    "card_title": "Kelifi Dragon", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_37_PGMRV99HCWG7_en.png", \
    "card_text": "Kelifi Dragon cannot be played unless you have 7<A> or more.Fight/Reap: Gain 1<A>. Deal 5<D> to a creature.", \
    "traits": "Dragon", \
    "amber": "0", \
    "power": "12", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "37", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8a045167-eccd-4026-9508-a73f5395cdad", \
    "card_title": "Rock-Hurling Giant", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_44_HP3GQM2F73G5_en.png", \
    "card_text": "During your turn, each time you discard a Brobnar card from your hand, you may deal 4<D> to a creature.", \
    "traits": "Giant", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "44", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "bbb7c660-d282-4bd1-88f9-6d8213483c4a", \
    "card_title": "Harland Mindlock", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_143_G7C9MP3P4VX2_en.png", \
    "card_text": "Play: Take control of an enemy flank creature until Harland Mindlock leaves play.", \
    "traits": "Cyborg  Scientist", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "143", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "de5902d1-7462-497c-aa45-400f938772ef", \
    "card_title": "Bulleteye", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_297_G45G2JGWP362_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: Destroy a flank creature.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "297", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c5e95ea2-fd32-4ab8-964a-720993f80d1b", \
    "card_title": "Stampede", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_335_QV8XP6G2RJ4V_en.png", \
    "card_text": "Play: If you used 3 or more creatures this turn, steal 2<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Better to run with the herd than be trampled beneath it.” –Eldest Bear", \
    "card_number": "335", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "03980a75-13d7-4a47-8829-7a1c2ab996d9", \
    "card_title": "Brain Stem Antenna", \
    "house": "Mars", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_209_JHRJCP7RMVH2_en.png", \
    "card_text": "This creature gains, “After you play a Mars creature, ready this creature and for the remainder of the turn it belongs to house Mars.”", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "209", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "737b485f-fc98-4d01-9d07-b00c76e754ed", \
    "card_title": "Veemos Lightbringer", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_262_VP65GQXWR45X_en.png", \
    "card_text": "Play: Destroy each elusive creature.", \
    "traits": "Angel  Spirit", \
    "amber": "0", \
    "power": "6", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "262", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "d46aafdf-13dd-45b0-be2e-d8e49be01d69", \
    "card_title": "Master of 1", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_89_RF2PX33PJW8W_en.png", \
    "card_text": "Reap: You may destroy a creature with 1 power.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "The first sin is fear.", \
    "card_number": "89", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a6a864cf-ac90-4cd2-8d91-7de468c7f66c", \
    "card_title": "Champion Tabris", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_240_C7P8FX9FVPXV_en.png", \
    "card_text": "Fight: Capture 1<A>.", \
    "traits": "Human  Knight", \
    "amber": "0", \
    "power": "6", \
    "armor": "2", \
    "rarity": "Uncommon", \
    "flavor_text": "“All my skill in battle brings me not one step closer to Enlightenment.”", \
    "card_number": "240", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f8f69f7c-ff0d-4ddb-b58a-41563b0c9a1c", \
    "card_title": "Potion of Invulnerability", \
    "house": "Sanctum", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_234_RJ99C8H7PWJH_en.png", \
    "card_text": "Omni: Sacrifice Potion of Invulnerability. For the remainder of the turn, each friendly creature cannot be dealt damage.", \
    "traits": "Item", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "234", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "026fa764-3bf2-40fc-9182-b34f0acfb760", \
    "card_title": "Neutron Shark", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_146_92H2X974PG8Q_en.png", \
    "card_text": "Play/Fight/Reap: Destroy an enemy creature or artifact and a friendly creature or artifact. Discard the top card of your deck. If that card is not a Logos card, trigger this effect again.", \
    "traits": "Beast  Mutant", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "146", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "54a95c9b-5b99-4a12-9e68-29adb3e8b49b", \
    "card_title": "Deep Probe", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_162_J3M2V5CXFJ4W_en.png", \
    "card_text": "Play: Choose a house. Reveal your opponents hand. Discard each creature of that house revealed this way.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "162", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "6806cdf1-81bb-49ce-909b-f98be2d82cb5", \
    "card_title": "Numquid the Fair", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_253_3G85FMW7C6QH_en.png", \
    "card_text": "Play: Destroy an enemy creature. Repeat this card’s effect if your opponent still controls more creatures than you.", \
    "traits": "Human", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "253", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2679977b-87f2-4afe-8c40-9e713569794f", \
    "card_title": "Truebaru", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_104_VCQ8F8XMQJCH_en.png", \
    "card_text": "You must lose 3<A> in order to play Truebaru.  Taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)Destroyed: Gain 5<A>. ", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "104", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "872b8871-93da-4b0d-a321-61f09e1824ea", \
    "card_title": "Dysania", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_141_MMQJWC7Q6V3_en.png", \
    "card_text": "Play: Your opponent discards each of their archived cards. You gain 1<A> for each card discarded this way.", \
    "traits": "Mutant", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "141", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f4cc23bb-4e17-46e9-97ef-3d984b9a79fc", \
    "card_title": "Bear Flute", \
    "house": "Untamed", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_340_94548CJ4JMP9_en.png", \
    "card_text": "Action: Fully heal an Ancient Bear. If there are no Ancient Bears in play, search your deck and discard pile and put each Ancient Bear from them into your hand. If you do, shuffle your discard pile into your deck.", \
    "traits": "Item", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "340", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "66f8ec97-15d0-4102-819a-7d912feca361", \
    "card_title": "Piranha Monkeys", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_365_9WCFVMXQMVJG_en.png", \
    "card_text": "Play/Reap: Deal 2<D> to each other creature.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "They can skeletonize a snufflegator in two minutes flat.", \
    "card_number": "365", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9a146bd4-7017-49ab-9e59-3ddbbb18d210", \
    "card_title": "The Harder They Come", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_228_JQM953FW234C_en.png", \
    "card_text": "Play: Purge a creature with power 5 or higher.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "228", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "de9869e5-5750-4ce3-bec5-40f250a05a59", \
    "card_title": "Incubation Chamber", \
    "house": "Mars", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_186_PRG4HJPG6GX8_en.png", \
    "card_text": "Omni: Reveal a Mars creature from your hand. If you do, archive it.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "Most Martians on the Crucible came out of one of these tanks.", \
    "card_number": "186", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2b3b461c-7f0b-4ebf-bcf7-f37a9509d7b5", \
    "card_title": "Tolas", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_103_PMC43W3QPFW4_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Each time a creature is destroyed, its opponent gains 1<A>.", \
    "traits": "Imp", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "103", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f344ec2a-cbfb-4cd1-9f11-35b2a1a7e90c", \
    "card_title": "Positron Bolt", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_118_9RQFX349V37W_en.png", \
    "card_text": "Play: Deal 3<D> to a flank creature. Deal 2<D> to its neighbor. Deal 1<D> to the second creature’s other neighbor.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "0", \
    "card_number": "118", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a802b4cc-6c00-4559-bb29-677cc0d788e5", \
    "card_title": "Crazy Killing Machine", \
    "house": "Logos", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_128_8VF3XM5JM75C_en.png", \
    "card_text": "Action: Discard the top card of each player’s deck. For each of those cards, destroy a creature or artifact of that card’s house, if able. If 2 cards are not destroyed as a result of this, destroy Crazy Killing Machine.", \
    "traits": "Weapon", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "128", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "2948a6fc-f7fa-45f2-b73d-fdf5f4216e46", \
    "card_title": "Chuff Ape", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_191_MMMC6JPJ4H5P_en.png", \
    "card_text": "Taunt. (This creature’s neighbors cannot be attacked unless they have taunt.)Chuff Ape enters play stunned.Fight/Reap: You may sacrifice another friendly creature. If you do, fully heal Chuff Ape.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "11", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "191", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c25f3a5d-b757-4c30-9097-01a9ad692833", \
    "card_title": "Selwyn the Fence", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_309_7GJ6RPFR59G2_en.png", \
    "card_text": "Fight/Reap: Move 1<A> from one of your cards to your pool.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "309", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9c13665d-e4da-45b4-b04d-27abfafe5c23", \
    "card_title": "Masterplan", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_288_8FJVHVWFWC4P_en.png", \
    "card_text": "Play: Put a card from your hand facedown beneath Masterplan.Omni: Play the card beneath Masterplan. Sacrifice Masterplan.", \
    "traits": "Item", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "288", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c5fad519-5703-497a-bafe-6eb5d8e0dfe6", \
    "card_title": "Yo Mama Mastery", \
    "house": "Brobnar", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_52_9664WG465QGC_en.png", \
    "card_text": "This creature gains taunt.Play: Fully heal this creature.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Yo’ Mama is sooo tiny...”", \
    "card_number": "52", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5b0259f0-f15b-4530-b634-b6309b96be69", \
    "card_title": "Mass Abduction", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_169_V74WF7V4MC37_en.png", \
    "card_text": "Play: Put up to 3 damaged enemy creatures into your archives. If any of these creatures leave your archives, they are put into their owner’s hand instead.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "169", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "4f438035-6597-4863-8bb1-35463034e0f2", \
    "card_title": "Ember Imp", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_85_C72X25358RG2_en.png", \
    "card_text": "Your opponent cannot play more than 2 cards each turn.", \
    "traits": "Imp", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": 85, \
    "expansion": "341", \
    "is_maverick": "True" \
  }',
  '{ \
    "id": "02feb5dd-81a0-4e06-8b5d-0ad7bdc9de08", \
    "card_title": "Mushroom Man", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_362_HW3R4QRJGGMM_en.png", \
    "card_text": "Mushroom Man gets +3 power for each unforged key you have.", \
    "traits": "Fungus  Human", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“He’s a real fun guy if you get to know him.” –Eldest Bear", \
    "card_number": "362", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "b04d00f0-3ce2-49b7-8ab4-220a40db2865", \
    "card_title": "Random Access Archives", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_119_5J4359XWQQ74_en.png", \
    "card_text": "Play: Archive the top card of your deck.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "3.14159, Niffles, Monosodium Glutamate...", \
    "card_number": "119", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "67e81873-d126-4e97-a9b6-b0ad4368f1c3", \
    "card_title": "Lava Ball", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_9_G7F5XC6J5QMG_en.png", \
    "card_text": "Play: Deal 4<D> to a creature with 2<D> splash.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Here...Catch!”", \
    "card_number": "9", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c79475dc-0faf-4e89-9847-49a314e23236", \
    "card_title": "The Sting", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_295_45HVFWG7RMPF_en.png", \
    "card_text": "Skip your “forge a key” step.You get all <A> spent by your opponent when forging keys.Action: Sacrifice The Sting.", \
    "traits": "Vehicle", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "295", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "94387722-ef2e-4591-8cbf-989feaf94656", \
    "card_title": "Ring of Invisibility", \
    "house": "Shadows", \
    "card_type": "Upgrade", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_317_F7RPHF6XHVWC_en.png", \
    "card_text": "This creature gains elusive and skirmish.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“I put it down for just a second...”", \
    "card_number": "317", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c9c045b1-061b-419e-aa1b-bc913b57e7f0", \
    "card_title": "Mighty Tiger", \
    "house": "Untamed", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_360_88VX5H673QQ4_en.png", \
    "card_text": "Play: Deal 4<D> to an enemy creature.", \
    "traits": "Beast", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "360", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "ff0d19c4-55e6-494e-b705-8b0c6b196468", \
    "card_title": "Shaffles", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_95_563MPX64P3XC_en.png", \
    "card_text": "At the end of your turn, your opponent loses 1<A>.", \
    "traits": "Imp", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Do you want imps? This is how you get imps.” ", \
    "card_number": "95", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c4b7c7e1-72b5-453b-9240-c9eb33710910", \
    "card_title": "Phylyx the Disintegrator", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_197_C637CW23C7M7_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Action: Your opponent loses 1<A> for each other friendly Mars creature.", \
    "traits": "Martian  Soldier", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "197", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "7368fd79-70b8-4917-9d2c-dead816f624c", \
    "card_title": "Pingle Who Annoys", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_43_PC7XR5283WJ_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Deal 1<D> to each enemy creature after it enters play.", \
    "traits": "Goblin", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "43", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "c03f90e3-17a6-407e-8655-9884ed569108", \
    "card_title": "Reverse Time", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_121_CXQ8C95R8C87_en.png", \
    "card_text": "Play: Swap your deck and your discard pile. Then, shuffle your deck.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "...time back turn could I if", \
    "card_number": "121", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "21a5a8b1-4d19-43f2-8e8d-bd7a7531099d", \
    "card_title": "Sneklifter", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_313_XW5J3RPG585M_en.png", \
    "card_text": "Play: Take control of an enemy artifact. While under your control, if it does not belong to one of your three houses, it is considered to be of house Shadows.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "313", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "81bfdb14-81ac-4dba-9ef4-fcba524b354e", \
    "card_title": "Eater of the Dead", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_84_5P9QW3X62X46_en.png", \
    "card_text": "Fight/Reap: Purge a creature from a discard pile. If you do, put a +1 power counter on Eater of the Dead.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "4", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "84", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f099e2ec-681b-4b47-878b-c091da3708d1", \
    "card_title": "Deipno Spymaster", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_299_M3P2FVHP7MC_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Omni: Choose a friendly creature. You may use that creature this turn.", \
    "traits": "Elf  Thief", \
    "amber": "0", \
    "power": "1", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "299", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "250a4cca-bd8e-4e2f-b420-18a3335371d2", \
    "card_title": "Martian Hounds", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_167_3M79PQ4XJ4W2_en.png", \
    "card_text": "Play: Choose a creature. For each damaged creature, give the chosen creature two +1 power counters.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "Who let the... dogs?... out?", \
    "card_number": "167", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "13895422-dc36-49ae-bb7c-5e5d1f3f9df4", \
    "card_title": "Timetraveller", \
    "house": "Logos", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_153_X83CX7XJ5GRX_en.png", \
    "card_text": "Play: Draw 2 cards. Action: Shuffle Timetraveller into your deck.", \
    "traits": "Human  Scientist", \
    "amber": "1", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "153", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a1766b1c-dc41-4e1c-975e-111f6b740a6d", \
    "card_title": "The Common Cold", \
    "house": "Untamed", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_336_6J5XR2JH8X5G_en.png", \
    "card_text": "Play: Deal 1<D> to each creature. You may destroy all Mars creatures.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“As it turns out, it’s a weaker version of the uncommon cold.” –Dr. Escotera", \
    "card_number": "336", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "8f7f0b00-868d-4447-967b-e8c9d880c91a", \
    "card_title": "World Tree", \
    "house": "Untamed", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_344_JWRCR9MQX696_en.png", \
    "card_text": "Action: Return a creature from your discard pile to the top of your deck.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "344", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "818f90a4-e896-4ba2-91ea-0d1232e94058", \
    "card_title": "Radiant Truth", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_224_J975CJ57VPP9_en.png", \
    "card_text": "Play: Stun each enemy creature not on a flank.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "“Truly I say to you: pie is superior to cake.” - from the Ravings of the Prophet Gizelhart", \
    "card_number": "224", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "dddb201b-03d0-4fa9-b627-c69f51994c13", \
    "card_title": "Faygin", \
    "house": "Shadows", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_300_X7RWJQRG2MRV_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: Return an Urchin from play or from your discard pile to your hand.", \
    "traits": "Human  Thief", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "300", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "a835a99c-67a5-4e2d-9720-85b41ef58468", \
    "card_title": "Take that, Smartypants", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_11_R2V4JJXQRVGH_en.png", \
    "card_text": "Play: Steal 2<A> if your opponent has 3 or more Logos cards in play.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“Them bots don’t wear pants. I carry spares.”", \
    "card_number": "11", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "90dc2b61-521a-40c1-bf0a-14e4d1457977", \
    "card_title": "Safe Place", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_289_88GPJGFV248G_en.png", \
    "card_text": "You may spend <A> on Safe Place when forging keys.Action: Move 1<A> from your pool to Safe Place.", \
    "traits": "Location", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "289", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "0ee63919-bff1-404f-b71b-b03e85cf692e", \
    "card_title": "Inspiration", \
    "house": "Mars", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_220_J4PRQX77RXV8_en.png", \
    "card_text": "Play: Ready and use a friendly creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "“The Sanctum gives meaning to my life.” - Duma the Martyr", \
    "card_number": "220", \
    "expansion": "341", \
    "is_maverick": "True" \
  }',
  '{ \
    "id": "91a3ed7b-2940-4774-86f1-9ca02989adee", \
    "card_title": "Finishing Blow", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_269_V557QC8HH5C9_en.png", \
    "card_text": "Play: Destroy a damaged creature. If you do, steal 1<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "You’ll never see it coming.", \
    "card_number": "269", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5b80c696-efe1-4be2-92c8-d31c260ba8ac", \
    "card_title": "Doorstep to Heaven", \
    "house": "Sanctum", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_217_RWHMP875732G_en.png", \
    "card_text": "Play: Each player with 6<A> or more is reduced to 5<A>.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Uncommon", \
    "flavor_text": "The cities of the Sanctum are safe, clean, and vibrant like few others on the Crucible. But few are judged worthy to enter.", \
    "card_number": "217", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "74a9ed49-ed43-42ff-b531-b84f737581db", \
    "card_title": "Qyxxlyx Plague Master", \
    "house": "Mars", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_198_4QXQJ939VVQM_en.png", \
    "card_text": "Fight/Reap: Deal 3<D> to each Human creature. This damage cannot be prevented by armor.", \
    "traits": "Martian  Scientist", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "198", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "f4497a06-5ae3-4706-86b6-c0c141b8f788", \
    "card_title": "Help from Future Self", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_111_5WMP36R2MHF_en.png", \
    "card_text": "Play: Search your deck and discard pile for a Timetraveller, reveal it, and put it into your hand. Shuffle your discard pile into your deck.", \
    "traits": "0", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "FIXED", \
    "flavor_text": "0", \
    "card_number": "111", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "fdf76fb4-708d-4950-bc31-c91bb25aeb40", \
    "card_title": "Customs Office", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_285_C7MWV8WQ4QPG_en.png", \
    "card_text": "Your opponent must pay you 1<A> in order to play an artifact.", \
    "traits": "Location", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "285", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "85584ea2-11be-40d0-bfcd-82799b1547af", \
    "card_title": "Champion’s Challenge", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_6_PJ6HFMR62X8F_en.png", \
    "card_text": "Play: Destroy each enemy creature except the most powerful enemy creature. Destroy each friendly creature except the most powerful friendly creature. Ready and fight with your remaining creature.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "6", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "99879b5b-70c1-4fb2-9700-87054eb750b9", \
    "card_title": "Autocannon", \
    "house": "Brobnar", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_19_XRFQ9GHJ98C3_en.png", \
    "card_text": "Deal 1<D> to each creature after it enters play.", \
    "traits": "Weapon", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "19", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "aeddb1b9-1241-4476-ae67-bd07016f46a2", \
    "card_title": "Arise!", \
    "house": "Brobnar", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_54_F9GHFCWJ233R_en.png", \
    "card_text": "Play: Choose a house. Return each creature of that house from your discard pile to your hand. Gain 1 chain.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Common", \
    "flavor_text": "0", \
    "card_number": "54", \
    "expansion": "341", \
    "is_maverick": "True" \
  }',
  '{ \
    "id": "bc08aefc-363f-4ef3-b6a0-5c60fc4da8f3", \
    "card_title": "Jehu the Bureaucrat", \
    "house": "Sanctum", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_250_XMP7GGP9HP57_en.png", \
    "card_text": "After you choose Sanctum as your active house, gain 2<A>.", \
    "traits": "Human", \
    "amber": "0", \
    "power": "3", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "“The knights protect the Sanctum. They are entitled to certain... benefits.” ", \
    "card_number": "250", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5c8c697c-ffcf-4116-b133-179198017c31", \
    "card_title": "Looter Goblin", \
    "house": "Brobnar", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_41_779WFQQ368X7_en.png", \
    "card_text": "Elusive. (The first time this creature is attacked each turn, no damage is dealt.)Reap: For the remainder of the turn, gain 1<A> each time an enemy creature is destroyed.", \
    "traits": "Goblin", \
    "amber": "0", \
    "power": "2", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "41", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "5fc16338-955d-48ed-abb4-9f38b9506c12", \
    "card_title": "Routine Job", \
    "house": "Shadows", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_282_4F97HV2RJ9FC_en.png", \
    "card_text": "Play: Steal 1<A>. Then, steal 1<A> for each copy of Routine Job in your discard pile.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "282", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "9751d62a-ce61-41f1-a13a-0d7f8812abf8", \
    "card_title": "Evasion Sigil", \
    "house": "Shadows", \
    "card_type": "Artifact", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_286_4686MGRJ87QX_en.png", \
    "card_text": "Before a creature fights, discard the top card of its controllers deck. If the discarded card is of the active house, exhaust that creature with no effect.", \
    "traits": "Power", \
    "amber": "1", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "286", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "4f1c5b07-d31a-4177-b3b2-d1890d41c3e4", \
    "card_title": "Overlord Greking", \
    "house": "Dis", \
    "card_type": "Creature", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_87_JFFVJ73VP9VQ_en.png", \
    "card_text": "After an enemy creature is destroyed fighting Overlord Greking, put that creature into play under your control.", \
    "traits": "Demon", \
    "amber": "0", \
    "power": "7", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "87", \
    "expansion": "341", \
    "is_maverick": "False" \
  }',
  '{ \
    "id": "7176b276-d696-4b53-8990-e78d94583d0b", \
    "card_title": "Knowledge is Power", \
    "house": "Logos", \
    "card_type": "Action", \
    "front_image": "https://cdn.keyforgegame.com/media/card_front/en/341_113_9V5G7WCPW27X_en.png", \
    "card_text": "Play: Choose one: Archive a card, or, for each archived card you have, gain 1<A>.", \
    "traits": "0", \
    "amber": "0", \
    "power": "0", \
    "armor": "0", \
    "rarity": "Rare", \
    "flavor_text": "0", \
    "card_number": "113", \
    "expansion": "341", \
    "is_maverick": "False" \
  }']

def removeUseless(S):
  """Removes spaces from a string.
  """
  if len(S) == 0:
    return ''
  if S[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
    return S[0] + removeUseless(S[1:])
  else:
    return '' + removeUseless(S[1:])

def parse(n = 0):
  """Sorts the cards by card number into a list.
  """
  #base case
  if n == len(data):
    return []
  else:
    y = json.loads(data[n])
    x = [y["card_title"], int(y["amber"]), y["house"], y["card_type"], int(y["power"]), int(y["armor"]), 0, y["traits"], y["card_text"], y["flavor_text"], y["rarity"], y["expansion"], int(y["card_number"]), y["id"], y["is_maverick"], y["front_image"]]
    # print(removeUseless(x[0]), "=", x)
    return [x] + parse(n + 1)

# Next steps: turned all into lists, now need to figure out how to automate class creation
z = parse()
z.sort(key = lambda z: z[12])

def printList(z, n = 0):
  """Prints out the items in the inputed list of lists
  """
  if n == len(z):
    return
  else:
    print(removeUseless(z[n][0]), "=", z[n])
    printList(z, n + 1)

def printClass(z, n = 0):
	"""Prints out the items from the list of lists as a Class.
	"""
	if n == len(z):
		return
	else:
		print("class " + removeUseless(z[n][0]) + "(Card):")
		print("    title = '" + str(z[n][0]) + "'")
		print("    house = '" + str(z[n][2]) + "'")
		print("    amber = " + str(z[n][1]))
		print("    typ = '" + str(z[n][3]) + "'")
		print("    text = '" + str(z[n][8]) + "'")
		print("    traits = '" + str(z[n][7]) + "'")
		print("    power = " + str(z[n][4]))
		print("    armor = " + str(z[n][5]))
		print("    damage = " + str(z[n][6]))
		print("    rarity = '" + str(z[n][10]) + "'")
		print("    flavor = '" + str(z[n][9]) + "'")
		print("    exp = 'CoA'")
		print("    number = " + str(z[n][12]))
		print("    id = '" + str(z[n][13]) + "'")
		print("    mav = " + str(z[n][14]))
		print("    image = '" + str(z[n][15]) + "'")
		printClass(z, n + 1)

printClass(z)