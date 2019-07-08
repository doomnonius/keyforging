import cards.cardsAsClass as card
from cards.cardsAsList import listt
import random

# For starters, I'll take two of my decks and manually enter them.

"""When drawing and adding cards, use pop() and append() to work from the end of the list as it is faster
"""

"""I want to write a function so that I can enter only a list of the card numbers and it will be converted into a list of the cards.
"""
deckIn = [7, 7, 16, 18, 22, 27, 29, 32, 33, 48, 49, 51, 267, 276, 276, 276, 281, 290, 292, 301, 311, 315, 315, 318, 325, 332, 349, 351, 351, 361, 362, 362, 363, 363, 363, 365]

allCards = [card.AFairGame, card.AmmoniaClouds, card.AncientBear, card.Anger, card.AnnihilationRitual, card.AnomalyExploiter, card.Arise, card.ArmageddonCloak, card.Autocannon, card.BadPenny, card.BaitandSwitch, card.BannerofBattle, card.Barehanded, card.Batdrone, card.BattleFleet, card.BearFlute, card.Begone, card.Bigtwig, card.BilgumAvalanche, card.BiomatrixBackup, card.BlindingLight, card.BloodMoney, card.BloodofTitans, card.Blypyp, card.BoobyTrap, card.BouncingDeathquark, card.BrainEater, card.BrainStemAntenna, card.BriarGrubbling, card.BrothersinBattle, card.Bulleteye, card.Bulwark, card.Bumpsy, card.BurntheStockpile, card.Cannon, card.Card, card.CarloPhantom, card.ChampionAnaphiel, card.ChampionTabris, card.ChampionsChallenge, card.ChaosPortal, card.Charette, card.Charge, card.ChotaHazri, card.ChuffApe, card.CleansingWave, card.ClearMind, card.CollarOfSubordination, card.CombatPheromones, card.CommanderRemiel, card.Commpod, card.ControltheWeak, card.CooperativeHunting, card.CowardsEnd, card.CrazyKillingMachine, card.CreepingOblivion, card.CrystalHive, card.Curiosity, card.CustomVirus, card.CustomsOffice, card.DanceofDoom, card.DeepProbe, card.DeipnoSpymaster, card.DewFaerie, card.Dextre, card.DimensionDoor, card.DocBookton, card.Dodger, card.DominatorBauble, card.DoorsteptoHeaven, card.DrEscotera, card.Drumble, card.DumatheMartyr, card.Duskrunner, card.DustImp, card.DustPixie, card.Dysania, card.EMPBlast, card.Earthshaker, card.EateroftheDead, card.EffervescentPrinciple, card.EmberImp, card.EpicQuest, card.EtherSpider, card.EvasionSigil, card.ExperimentalTherapy, card.Faygin, card.Fear, card.FeedingPit, card.FertilityChant, card.FinishingBlow, card.Firespitter, card.FlameWreathed, card.Flaxia, card.Fogbank, card.Foggify, card.FollowtheLeader, card.Francus, card.FullMoon, card.FuzzyGruen, card.GabosLongarms, card.GangerChieftain, card.GanymedeArchivist, card.Gatekeeper, card.GatewaytoDis, card.GauntletofCommand, card.GhostlyHand, card.GiantSloth, card.GloriousFew, card.Gongoozle, card.GormofOmm, card.GrabberJammer, card.GraspingVines, card.GrenadeSnib, card.GreyMonk, card.Grommid, card.GuardianDemon, card.GuiltyHearts, card.Halacor, card.HallowedBlaster, card.HandofDis, card.HarlandMindlock, card.HayyeltheMerchant, card.Headhunter, card.HebetheHuge, card.Hecatomb, card.HelpfromFutureSelf, card.HiddenStash, card.HonorableClaim, card.HorsemanOfDeath, card.HorsemanOfFamine, card.HorsemanOfPestilence, card.HorsemanOfWar, card.HuntingWitch, card.HypnoticCommand, card.Hysteria, card.ImperialTraitor, card.IncubationChamber, card.InkatheSpider, card.Inspiration, card.InterdimensionalGraft, card.InvasionPortal, card.IronObelisk, card.Irradiatedmber, card.JammerPack, card.JehutheBureaucrat, card.JohnSmyth, card.KelifiDragon, card.KeyAbduction, card.KeyCharge, card.KeyHammer, card.KeyofDarkness, card.KeytoDis, card.KindrithLongshot, card.KingoftheCrag, card.KnowledgeisPower, card.Krump, card.Labwork, card.LadyMaxena, card.LashofBrokenDreams, card.LavaBall, card.LibraryAccess, card.LibraryofBabble, card.LibraryoftheDamned, card.Lifeward, card.Lifeweb, card.LightsOut, card.LomirFlamefist, card.LongfusedMines, card.LooterGoblin, card.LoottheBodies, card.LordGolgotha, card.LostintheWoods, card.LupotheScarred, card.MacisAsp, card.MacktheKnife, card.MagdatheRat, card.MantleoftheZealot, card.MartianHounds, card.MartiansMakeBadAllies, card.MassAbduction, card.Masterof1, card.Masterof2, card.Masterof3, card.Masterplan, card.MatingSeason, card.Miasma, card.MightyJavelin, card.MightyLance, card.MightyTiger, card.Mimicry, card.MindBarb, card.Mindwarper, card.MobiusScroll, card.Mooncurser, card.Mother, card.Mothergun, card.MothershipSupport, card.Mugwump, card.Murmook, card.MushroomMan, card.NaturesCall, card.NepentheSeed, card.NerveBlast, card.NeuroSyphon, card.NeutronShark, card.Nexus, card.NiffleApe, card.NiffleQueen, card.NocturnalManeuver, card.NoddytheThief, card.NovuArchaeologist, card.NumquidtheFair, card.OathofPoverty, card.OldBruno, card.OneLastJob, card.OneStoodAgainstMany, card.OrbitalBombardment, card.Oubliette, card.OverlordGreking, card.OzmoMartianologist, card.Pandemonium, card.PawnSacrifice, card.PerilousWild, card.PhaseShift, card.PhoenixHeart, card.PhosphorusStars, card.PhylyxtheDisintegrator, card.PileofSkulls, card.PingleWhoAnnoys, card.PiranhaMonkeys, card.PitDemon, card.Pitlord, card.PocketUniverse, card.PoisonWave, card.Poltergeist, card.PositronBolt, card.PotionofInvulnerability, card.Protectrix, card.ProtecttheWeak, card.PsychicBug, card.PsychicNetwork, card.Punch, card.QuixotheAdventurer, card.QyxxlyxPlagueMaster, card.RadiantTruth, card.RaidingKnight, card.RandomAccessArchives, card.RedHotArmor, card.RedPlanetRayGun, card.Regrowth, card.RelentlessAssault, card.RelentlessWhispers, card.RemoteAccess, card.Replicator, card.ResearchSmoko, card.Restringuntus, card.ReverseTime, card.RingofInvisibility, card.RitualofBalance, card.RitualoftheHunt, card.RockHurlingGiant, card.RocketBoots, card.RogueOgre, card.RoundTable, card.RoutineJob, card.SacrificialAltar, card.SafePlace, card.SampleCollection, card.SanctumGuardian, card.SavethePack, card.Scout, card.ScramblerStorm, card.ScreamingCave, card.Screechbomb, card.SeekerNeedle, card.SelwyntheFence, card.Sequis, card.SergeantZakiel, card.ShadowSelf, card.Shaffles, card.ShatterStorm, card.ShieldofJustice, card.Shooler, card.ShoulderArmor, card.SigilofBrotherhood, card.SilentDagger, card.Silvertooth, card.SkeletonKey, card.SkippyTimehog, card.SloppyLabwork, card.Smaaash, card.SmilingRuth, card.Smith, card.Sneklifter, card.Sniffer, card.Snudge, card.Snufflegator, card.SoftLanding, card.SoulSnatcher, card.SoundtheHorns, card.SpanglerBox, card.SpecialDelivery, card.SpectralTunneler, card.SpeedSigil, card.Squawker, card.Stampede, card.StaunchKnight, card.StealerofSouls, card.StrangeGizmo, card.SubtleMaul, card.Succubus, card.SwapWidget, card.TakeHostages, card.TakethatSmartypants, card.Teliga, card.TendrilsofPain, card.Tentacus, card.TermsofRedress, card.TheCommonCold, card.TheHarderTheyCome, card.TheHowlingPit, card.TheSpiritsWay, card.TheSting, card.TheTerror, card.TheVaultkeeper, card.TheWarchest, card.ThreeFates, card.Timetraveller, card.TirelessCrocag, card.TitanMechanic, card.Tocsin, card.Tolas, card.TooMuchtoProtect, card.TotalRecall, card.TranspositionSandals, card.TreasureMap, card.Tremor, card.Troll, card.TroopCall, card.Truebaru, card.Tunk, card.TwinBoltEmission, card.UlyqMegamouth, card.Umbra, card.UnguardedCamp, card.Urchin, card.UxlyxtheZookeeper, card.Valdr, card.VeemosLightbringer, card.VespilonTheorist, card.VeylanAnalyst, card.VezymaThinkdrone, card.Vigor, card.VirtuousWorks, card.Wardrummer, card.Warsong, card.WayoftheBear, card.WayoftheWolf, card.WhisperingReliquary, card.WildWormhole, card.WitchoftheEye, card.WitchoftheWilds, card.WordOfReturning, card.WorldTree, card.YoMamaMastery, card.YxiliMarauder, card.YxiloBolter, card.YxilxDominator, card.Zorg, card.ZyzzixtheMany]

MyDeck = []
OppDeck = []
MyHand = [6]
OppHand = [6]

def buildDeck(L, n = 1):
    """Takes a list of card numbers and builds a deck.
    """
    print("Calling build deck: " + str(n))
    def search(n, L):
        """A helper function that finds the card in cardsAsList that has card.number == n.
        """
        print("Calling search: " + str(n))
        if L[0].number == n:          #ISSUES HERE
            return L[0]
        else:
            return search(n, L[1:])
    # optimization?: split cards into houses
    # base case: empty list
    if L == []:
        return
    elif L[0] == n:
        print("elif")
        MyDeck.append(card.listdetails(search(n, allCards))) # need to find the card that has .number == n
        buildDeck(L[1:], n)
    else:
        buildDeck(L, n + 1)

def nameList(L):
    """Takes the listdetails() function output and returns only card names.
    """
    if type(L[0]) == int:
        L = L[1:]
    return [x[0] for x in L]

buildDeck(deckIn)
random.shuffle(MyDeck)
print(nameList(MyDeck))

def drawEOT(hand, n = 0):
    """Draws until hand is full. Index 0 of each hand is the number of cards a hand should have.
    """
    # Base case is full hand
    while (len(hand) - 1) < hand[0]:
        x = MyDeck.pop()
        print(x)
        hand.append(x)
     #Going to need to add end of turn stuff or a call to end of turn stuff

drawEOT(MyHand)