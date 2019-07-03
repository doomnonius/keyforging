__package__ = 'cards'

import cardsAsClass

a = cardsAsClass.Krump("Bob")
b = cardsAsClass.Krump("Frank")
a.power += 2

MyBoard = [cardsAsClass.printdetails(a)]
OppBoard = [cardsAsClass.printdetails(b)]
MyArt = []
OppArt = []

cardsAsClass.Anger.played(cardsAsClass.Anger)


if __name__ == '__main__':
    print ('This statement will be executed only if this script is called directly')