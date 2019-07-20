import cards.cardsAsClass as card
from cards.cardsAsList import listt
import random
import requests
import json
import re
from decks.deckList import deckDict

# idea: use composition, these five classes will go under the deck class. Not sure if this makes more sense then having them all as an individual list.

# class Discard:

# class Draw:

# class Archive:

# class Hand:

# class Purged:

# class Deck:

url1 = "https://www.keyforgegame.com/api/decks/?page=1&page_size=1&links=cards&search="
url2 = "https://www.keyforgegame.com/deck-details/"

def convertToHtml(string):
    """Converts a string to html to be used in a search.
    """
    if string == '':
        return ''
    elif string[0] in 'abcdefghijklmnopqrstuvwxyz."-':
        return string[0] + convertToHtml(string[1:])
    elif string[0] == ' ':
        return '%20' + convertToHtml(string[1:])
    elif string[0] == ',':
        return '%2C' + convertToHtml(string[1:])
    elif string[0] == '\'':
        return '%27' + convertToHtml(string[1:])

def importDeck():
    """Imports a deck for the user. How it works: converts the deck name to html, appends that to the url to get the json of a dekc from the keyforge api. This data doesn't have the cards ids I need, so I regex the deck id from the json (and also check the deck is from the right expansion, that there is only one deck, and log which houses are in the deck), then add that to a second url, from which I scrape the html and use regex to find all the card ids and add them to the list.
    """
    def sortName(val):
        """Used to sort deckDict by the 'name' key.
        """
        return val['card_number']

    newDeck = []
    deckname = input("Enter your deck's exact full name: ")
    # why not let them import a bunch of decks at once? because links=cards doesn't work, so I'd need to do another json call. Not willing to implement that yet
    newUrl = url1 + convertToHtml(deckname.lower())
    page = requests.get(newUrl).json()
    # print(newUrl)
    with open('decks/newdeck.json', 'w') as f:
        json.dump(page, f, ensure_ascii=False)
    with open('decks/newdeck.json') as f:
        data = json.load(f)
        if data['data'] == []:
            print("That input returned no results.")
            return
        deckid = data['data'][0]['id']
        deckName = data['data'][0]['name']
        deckExp = data['data'][0]['expansion']
        if deckExp != 341:
            print("This version of the game can only handle CotA decks.")
            return
        with open('decks/deckList.json', 'r') as f:
            data2 = json.load(f)
            for x in data2:
                if x['name'] == deckName:
                    print("This deck has already been added.")
                    return
            original = data2[0:]
            print(original)
        houses = (data['data'][0]['_links']['houses'][0:3])
        # print(len(data['_linked']['cards']))
        cards = data['_linked']['cards']
        cards.sort(key = sortName)
        cardids = data['data'][0]['_links']['cards']
        for card in cards:
            for x in cardids:
                if x == card['id']:
                    newDeck.append(card)
        # print(newDeck, len(newDeck))
        addDeck = {}
        addDeck['houses'] = houses
        addDeck['id'] = deckid
        addDeck['name'] = deckName
        addDeck['deck'] = newDeck
        # Do something to append this data to a json file - the attempt at a solution below is not working
    with open('decks/deckList.json', 'a') as f:
        new = original + addDeck
        json.dump(new, f, ensure_ascii=False)


    # ^ this works to print a dict with the houses, id, name, and deck (as a list of dicts), and can account for multiple instances of a card

"""When drawing and adding cards, use pop() and append() to work from the end of the list as it is faster
"""

allCards = [card.AFairGame, card.AmmoniaClouds, card.AncientBear, card.Anger, card.AnnihilationRitual, card.AnomalyExploiter, card.Arise, card.ArmageddonCloak, card.Autocannon, card.BadPenny, card.BaitandSwitch, card.BannerofBattle, card.Barehanded, card.Batdrone, card.BattleFleet, card.BearFlute, card.Begone, card.Bigtwig, card.BilgumAvalanche, card.BiomatrixBackup, card.BlindingLight, card.BloodMoney, card.BloodofTitans, card.Blypyp, card.BoobyTrap, card.BouncingDeathquark, card.BrainEater, card.BrainStemAntenna, card.BriarGrubbling, card.BrothersinBattle, card.Bulleteye, card.Bulwark, card.Bumpsy, card.BurntheStockpile, card.Cannon, card.Card, card.CarloPhantom, card.ChampionAnaphiel, card.ChampionTabris, card.ChampionsChallenge, card.ChaosPortal, card.Charette, card.Charge, card.ChotaHazri, card.ChuffApe, card.CleansingWave, card.ClearMind, card.CollarOfSubordination, card.CombatPheromones, card.CommanderRemiel, card.Commpod, card.ControltheWeak, card.CooperativeHunting, card.CowardsEnd, card.CrazyKillingMachine, card.CreepingOblivion, card.CrystalHive, card.Curiosity, card.CustomVirus, card.CustomsOffice, card.DanceofDoom, card.DeepProbe, card.DeipnoSpymaster, card.DewFaerie, card.Dextre, card.DimensionDoor, card.DocBookton, card.Dodger, card.DominatorBauble, card.DoorsteptoHeaven, card.DrEscotera, card.Drumble, card.DumatheMartyr, card.Duskrunner, card.DustImp, card.DustPixie, card.Dysania, card.EMPBlast, card.Earthshaker, card.EateroftheDead, card.EffervescentPrinciple, card.EmberImp, card.EpicQuest, card.EtherSpider, card.EvasionSigil, card.ExperimentalTherapy, card.Faygin, card.Fear, card.FeedingPit, card.FertilityChant, card.FinishingBlow, card.Firespitter, card.FlameWreathed, card.Flaxia, card.Fogbank, card.Foggify, card.FollowtheLeader, card.Francus, card.FullMoon, card.FuzzyGruen, card.GabosLongarms, card.GangerChieftain, card.GanymedeArchivist, card.Gatekeeper, card.GatewaytoDis, card.GauntletofCommand, card.GhostlyHand, card.GiantSloth, card.GloriousFew, card.Gongoozle, card.GormofOmm, card.GrabberJammer, card.GraspingVines, card.GrenadeSnib, card.GreyMonk, card.Grommid, card.GuardianDemon, card.GuiltyHearts, card.Halacor, card.HallowedBlaster, card.HandofDis, card.HarlandMindlock, card.HayyeltheMerchant, card.Headhunter, card.HebetheHuge, card.Hecatomb, card.HelpfromFutureSelf, card.HiddenStash, card.HonorableClaim, card.HorsemanOfDeath, card.HorsemanOfFamine, card.HorsemanOfPestilence, card.HorsemanOfWar, card.HuntingWitch, card.HypnoticCommand, card.Hysteria, card.ImperialTraitor, card.IncubationChamber, card.InkatheSpider, card.Inspiration, card.InterdimensionalGraft, card.InvasionPortal, card.IronObelisk, card.Irradiatedmber, card.JammerPack, card.JehutheBureaucrat, card.JohnSmyth, card.KelifiDragon, card.KeyAbduction, card.KeyCharge, card.KeyHammer, card.KeyofDarkness, card.KeytoDis, card.KindrithLongshot, card.KingoftheCrag, card.KnowledgeisPower, card.Krump, card.Labwork, card.LadyMaxena, card.LashofBrokenDreams, card.LavaBall, card.LibraryAccess, card.LibraryofBabble, card.LibraryoftheDamned, card.Lifeward, card.Lifeweb, card.LightsOut, card.LomirFlamefist, card.LongfusedMines, card.LooterGoblin, card.LoottheBodies, card.LordGolgotha, card.LostintheWoods, card.LupotheScarred, card.MacisAsp, card.MacktheKnife, card.MagdatheRat, card.MantleoftheZealot, card.MartianHounds, card.MartiansMakeBadAllies, card.MassAbduction, card.Masterof1, card.Masterof2, card.Masterof3, card.Masterplan, card.MatingSeason, card.Miasma, card.MightyJavelin, card.MightyLance, card.MightyTiger, card.Mimicry, card.MindBarb, card.Mindwarper, card.MobiusScroll, card.Mooncurser, card.Mother, card.Mothergun, card.MothershipSupport, card.Mugwump, card.Murmook, card.MushroomMan, card.NaturesCall, card.NepentheSeed, card.NerveBlast, card.NeuroSyphon, card.NeutronShark, card.Nexus, card.NiffleApe, card.NiffleQueen, card.NocturnalManeuver, card.NoddytheThief, card.NovuArchaeologist, card.NumquidtheFair, card.OathofPoverty, card.OldBruno, card.OneLastJob, card.OneStoodAgainstMany, card.OrbitalBombardment, card.Oubliette, card.OverlordGreking, card.OzmoMartianologist, card.Pandemonium, card.PawnSacrifice, card.PerilousWild, card.PhaseShift, card.PhoenixHeart, card.PhosphorusStars, card.PhylyxtheDisintegrator, card.PileofSkulls, card.PingleWhoAnnoys, card.PiranhaMonkeys, card.PitDemon, card.Pitlord, card.PocketUniverse, card.PoisonWave, card.Poltergeist, card.PositronBolt, card.PotionofInvulnerability, card.Protectrix, card.ProtecttheWeak, card.PsychicBug, card.PsychicNetwork, card.Punch, card.QuixotheAdventurer, card.QyxxlyxPlagueMaster, card.RadiantTruth, card.RaidingKnight, card.RandomAccessArchives, card.RedHotArmor, card.RedPlanetRayGun, card.Regrowth, card.RelentlessAssault, card.RelentlessWhispers, card.RemoteAccess, card.Replicator, card.ResearchSmoko, card.Restringuntus, card.ReverseTime, card.RingofInvisibility, card.RitualofBalance, card.RitualoftheHunt, card.RockHurlingGiant, card.RocketBoots, card.RogueOgre, card.RoundTable, card.RoutineJob, card.SacrificialAltar, card.SafePlace, card.SampleCollection, card.SanctumGuardian, card.SavethePack, card.Scout, card.ScramblerStorm, card.ScreamingCave, card.Screechbomb, card.SeekerNeedle, card.SelwyntheFence, card.Sequis, card.SergeantZakiel, card.ShadowSelf, card.Shaffles, card.ShatterStorm, card.ShieldofJustice, card.Shooler, card.ShoulderArmor, card.SigilofBrotherhood, card.SilentDagger, card.Silvertooth, card.SkeletonKey, card.SkippyTimehog, card.SloppyLabwork, card.Smaaash, card.SmilingRuth, card.Smith, card.Sneklifter, card.Sniffer, card.Snudge, card.Snufflegator, card.SoftLanding, card.SoulSnatcher, card.SoundtheHorns, card.SpanglerBox, card.SpecialDelivery, card.SpectralTunneler, card.SpeedSigil, card.Squawker, card.Stampede, card.StaunchKnight, card.StealerofSouls, card.StrangeGizmo, card.SubtleMaul, card.Succubus, card.SwapWidget, card.TakeHostages, card.TakethatSmartypants, card.Teliga, card.TendrilsofPain, card.Tentacus, card.TermsofRedress, card.TheCommonCold, card.TheHarderTheyCome, card.TheHowlingPit, card.TheSpiritsWay, card.TheSting, card.TheTerror, card.TheVaultkeeper, card.TheWarchest, card.ThreeFates, card.Timetraveller, card.TirelessCrocag, card.TitanMechanic, card.Tocsin, card.Tolas, card.TooMuchtoProtect, card.TotalRecall, card.TranspositionSandals, card.TreasureMap, card.Tremor, card.Troll, card.TroopCall, card.Truebaru, card.Tunk, card.TwinBoltEmission, card.UlyqMegamouth, card.Umbra, card.UnguardedCamp, card.Urchin, card.UxlyxtheZookeeper, card.Valdr, card.VeemosLightbringer, card.VespilonTheorist, card.VeylanAnalyst, card.VezymaThinkdrone, card.Vigor, card.VirtuousWorks, card.Wardrummer, card.Warsong, card.WayoftheBear, card.WayoftheWolf, card.WhisperingReliquary, card.WildWormhole, card.WitchoftheEye, card.WitchoftheWilds, card.WordOfReturning, card.WorldTree, card.YoMamaMastery, card.YxiliMarauder, card.YxiloBolter, card.YxilxDominator, card.Zorg, card.ZyzzixtheMany]

brobnar = [card.Anger, card.Autocannon, card.BannerofBattle, card.Barehanded, card.BilgumAvalanche, card.BloodMoney, card.BloodofTitans, card.BrothersinBattle, card.Bumpsy, card.BurntheStockpile, card.Cannon, card.ChampionsChallenge, card.CowardsEnd, card.Earthshaker, card.Firespitter, card.FollowtheLeader, card.GangerChieftain, card.GauntletofCommand, card.GrenadeSnib, card.Headhunter, card.HebetheHuge, card.IronObelisk, card.KelifiDragon, card.KingoftheCrag, card.Krump, card.LavaBall, card.LomirFlamefist, card.LooterGoblin, card.LoottheBodies, card.MightyJavelin, card.Mugwump, card.PhoenixHeart, card.PileofSkulls, card.PingleWhoAnnoys, card.Punch, card.RelentlessAssault, card.RockHurlingGiant, card.RogueOgre, card.Screechbomb, card.Smaaash, card.Smith, card.SoundtheHorns, card.TakethatSmartypants, card.TheWarchest, card.TirelessCrocag, card.Tremor, card.Troll, card.UnguardedCamp, card.Valdr, card.Wardrummer, card.Warsong, card.YoMamaMastery]
shadows = [card.BadPenny, card.BaitandSwitch, card.BoobyTrap, card.Bulleteye, card.CarloPhantom, card.CustomsOffice, card.DeipnoSpymaster, card.Dodger, card.Duskrunner, card.EvasionSigil, card.Faygin, card.FinishingBlow, card.GhostlyHand, card.HiddenStash, card.ImperialTraitor, card.KeyofDarkness, card.LightsOut, card.LongfusedMines, card.MacisAsp, card.MacktheKnife, card.MagdatheRat, card.Masterplan, card.Miasma, card.Mooncurser, card.NerveBlast, card.Nexus, card.NoddytheThief, card.OldBruno, card.OneLastJob, card.Oubliette, card.PawnSacrifice, card.PoisonWave, card.RelentlessWhispers, card.RingofInvisibility, card.RoutineJob, card.SafePlace, card.SeekerNeedle, card.SelwyntheFence, card.ShadowSelf, card.SilentDagger, card.Silvertooth, card.SkeletonKey, card.SmilingRuth, card.Sneklifter, card.SpecialDelivery, card.SpeedSigil, card.SubtleMaul, card.TheSting, card.TooMuchtoProtect, card.TreasureMap, card.Umbra, card.Urchin]
mars = [card.AmmoniaClouds, card.BattleFleet, card.BiomatrixBackup, card.Blypyp, card.BrainStemAntenna, card.ChuffApe, card.CombatPheromones, card.Commpod, card.CrystalHive, card.CustomVirus, card.DeepProbe, card.EMPBlast, card.EtherSpider, card.FeedingPit, card.GrabberJammer, card.Grommid, card.HypnoticCommand, card.IncubationChamber, card.InvasionPortal, card.Irradiatedmber, card.JammerPack, card.JohnSmyth, card.KeyAbduction, card.MartianHounds, card.MartiansMakeBadAllies, card.MassAbduction, card.MatingSeason, card.Mindwarper, card.Mothergun, card.MothershipSupport, card.OrbitalBombardment, card.PhosphorusStars, card.PhylyxtheDisintegrator, card.PsychicNetwork, card.QyxxlyxPlagueMaster, card.RedPlanetRayGun, card.SampleCollection, card.ShatterStorm, card.Sniffer, card.SoftLanding, card.Squawker, card.SwapWidget, card.TotalRecall, card.Tunk, card.UlyqMegamouth, card.UxlyxtheZookeeper, card.VezymaThinkdrone, card.YxiliMarauder, card.YxiloBolter, card.YxilxDominator, card.Zorg, card.ZyzzixtheMany]
sanctum = [card.ArmageddonCloak, card.Begone, card.BlindingLight, card.Bulwark, card.ChampionAnaphiel, card.ChampionTabris, card.Charge, card.CleansingWave, card.ClearMind, card.CommanderRemiel, card.DoorsteptoHeaven, card.DumatheMartyr, card.EpicQuest, card.Francus, card.Gatekeeper, card.GloriousFew, card.GormofOmm, card.GreyMonk, card.HallowedBlaster, card.HayyeltheMerchant, card.HonorableClaim, card.HorsemanOfDeath, card.HorsemanOfFamine, card.HorsemanOfPestilence, card.HorsemanOfWar, card.Inspiration, card.JehutheBureaucrat, card.LadyMaxena, card.LordGolgotha, card.MantleoftheZealot, card.MightyLance, card.NumquidtheFair, card.OathofPoverty, card.OneStoodAgainstMany, card.PotionofInvulnerability, card.Protectrix, card.ProtecttheWeak, card.RadiantTruth, card.RaidingKnight, card.RoundTable, card.SanctumGuardian, card.Sequis, card.SergeantZakiel, card.ShieldofJustice, card.ShoulderArmor, card.SigilofBrotherhood, card.StaunchKnight, card.TakeHostages, card.TermsofRedress, card.TheHarderTheyCome, card.TheSpiritsWay, card.TheVaultkeeper, card.VeemosLightbringer, card.VirtuousWorks, card.WhisperingReliquary]
untamed = [card.AncientBear, card.BearFlute, card.Bigtwig, card.BriarGrubbling, card.ChotaHazri, card.CooperativeHunting, card.Curiosity, card.DewFaerie, card.DustPixie, card.FertilityChant, card.Flaxia, card.Fogbank, card.FullMoon, card.FuzzyGruen, card.GiantSloth, card.GraspingVines, card.Halacor, card.HuntingWitch, card.InkatheSpider, card.KeyCharge, card.KindrithLongshot, card.Lifeweb, card.LostintheWoods, card.LupotheScarred, card.MightyTiger, card.Mimicry, card.Murmook, card.MushroomMan, card.NaturesCall, card.NepentheSeed, card.NiffleApe, card.NiffleQueen, card.NocturnalManeuver, card.PerilousWild, card.PiranhaMonkeys, card.Regrowth, card.RitualofBalance, card.RitualoftheHunt, card.SavethePack, card.Scout, card.Snufflegator, card.Stampede, card.Teliga, card.TheCommonCold, card.TroopCall, card.Vigor, card.WayoftheBear, card.WayoftheWolf, card.WitchoftheEye, card.WitchoftheWilds, card.WordOfReturning, card.WorldTree]
logos = [card.AnomalyExploiter, card.Batdrone, card.BouncingDeathquark, card.BrainEater, card.ChaosPortal, card.CrazyKillingMachine, card.Dextre, card.DimensionDoor, card.DocBookton, card.DrEscotera, card.Dysania, card.EffervescentPrinciple, card.ExperimentalTherapy, card.Foggify, card.GanymedeArchivist, card.HarlandMindlock, card.HelpfromFutureSelf, card.InterdimensionalGraft, card.KnowledgeisPower, card.Labwork, card.LibraryAccess, card.LibraryofBabble, card.MobiusScroll, card.Mother, card.NeuroSyphon, card.NeutronShark, card.NovuArchaeologist, card.OzmoMartianologist, card.PhaseShift, card.PocketUniverse, card.PositronBolt, card.PsychicBug, card.QuixotheAdventurer, card.RandomAccessArchives, card.RemoteAccess, card.Replicator, card.ResearchSmoko, card.ReverseTime, card.RocketBoots, card.ScramblerStorm, card.SkippyTimehog, card.SloppyLabwork, card.SpanglerBox, card.SpectralTunneler, card.StrangeGizmo, card.TheHowlingPit, card.Timetraveller, card.TitanMechanic, card.TranspositionSandals, card.TwinBoltEmission, card.VespilonTheorist, card.VeylanAnalyst, card.WildWormhole]
dis = [card.AFairGame, card.AnnihilationRitual, card.Arise, card.Charette, card.CollarOfSubordination, card.ControltheWeak, card.CreepingOblivion, card.DanceofDoom, card.DominatorBauble, card.Drumble, card.DustImp, card.EateroftheDead, card.EmberImp, card.Fear, card.FlameWreathed, card.GabosLongarms, card.GatewaytoDis, card.Gongoozle, card.GuardianDemon, card.GuiltyHearts, card.HandofDis, card.Hecatomb, card.Hysteria, card.KeyHammer, card.KeytoDis, card.LashofBrokenDreams, card.LibraryoftheDamned, card.Lifeward, card.Masterof1, card.Masterof2, card.Masterof3, card.MindBarb, card.OverlordGreking, card.Pandemonium, card.PitDemon, card.Pitlord, card.Poltergeist, card.RedHotArmor, card.Restringuntus, card.SacrificialAltar, card.ScreamingCave, card.Shaffles, card.Shooler, card.Snudge, card.SoulSnatcher, card.StealerofSouls, card.Succubus, card.TendrilsofPain, card.Tentacus, card.TheTerror, card.ThreeFates, card.Tocsin, card.Tolas, card.Truebaru]

MyDeck = []
OppDeck = []
MyHand = [6]
OppHand = [6]

def buildDeck(L, L2 = [], n = 1):
    """Takes a list of card numbers and builds a deck to L2. What this should do (and doesn't at this point), is to create a whole bunch of variables that are tied to instantiations of the appropriate classes.
    """
    # print("Calling build deck: " + str(n))
    def search(n, L):
        """A helper function that finds the card in cardsAsList that has card.number == n.
        """
        # print("Calling search: " + str(n))
        if L[0].number == n:
            return L[0]
        else:
            return search(n, L[1:])
    # optimization: split cards into houses
    # base case: empty list
    if len(L) == 3:
        print(len(L2))
        return L2
    elif L[0] == "Brobnar":
        if len(L) == 27:
            L[0] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, brobnar)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[0] == "Dis":
        if len(L) == 27:
            L[0] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, dis)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[0] == "Logos":
        if len(L) == 27:
            L[0] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, logos)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[0] == "Mars":
        if len(L) == 27:
            L[0] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, mars)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[0] == "Sanctum":
        if len(L) == 27:
            L[0] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, sanctum)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[1] == "Dis":
        if len(L) == 15:
            L[1] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, dis)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[1] == "Logos":
        if len(L) == 15:
            L[1] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, logos)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[1] == "Mars":
        if len(L) == 15:
            L[1] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, mars)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[1] == "Sanctum":
        if len(L) == 15:
            L[1] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, sanctum)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[1] == "Shadows":
        if len(L) == 15:
            L[1] = "done"
            buildDeck(L, L2, n)
        elif L[3] == n:
            L2.append(card.listdetails(search(n, shadows)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[2] == "Logos":
        if L[3] == n:
            L2.append(card.listdetails(search(n, logos)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[2] == "Mars":
        if L[3] == n:
            L2.append(card.listdetails(search(n, mars)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[2] == "Sanctum":
        if L[3] == n:
            L2.append(card.listdetails(search(n, sanctum)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[2] == "Shadows":
        if L[3] == n:
            L2.append(card.listdetails(search(n, shadows)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    elif L[2] == "Untamed":
        if L[3] == n:
            L2.append(card.listdetails(search(n, untamed)))
            buildDeck(L[0:3] + L[4:], L2, n)
        else:
            buildDeck(L, L2, n + 1)
    else:
        buildDeck(L, L2, n + 1)

def nameList(L):
    """Takes the listdetails() function output and returns only card names.
    """
    # Since L[0] of MyHand is an int and not another list, we need to ignore the first item of those lists.
    if L == []:
        return
    elif type(L[0]) == int:
        L = L[1:]
    # The first three indexes of MyDeck will be the houses.
    while type(L[0]) == str:
        L = L[1:]
    return [x[0] for x in L]

def drawEOT(hand, n = 0):
    """Draws until hand is full. Index 0 of each hand is the number of cards a hand should have. Also does all other end of turn actions.
    """
    while (len(hand) - 1) < hand[0]:
        x = MyDeck.pop()
        print(x)
        hand.append(x)
     #Going to need to add end of turn stuff

