import cardsAsClass
import fight
import play

a = cardsAsClass.Krump("Bob")
b = cardsAsClass.Krump("Frank")
a.power += 2

MyBoard = [cardsAsClass.printdetails(a)]
OppBoard = [cardsAsClass.printdetails(b)]

cardsAsClass.Anger.played(cardsAsClass.Anger)