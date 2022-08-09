from card import Card
from random import shuffle

SUITS = ['C', 'H', 'S', 'D']
VALUE = ['A', '2', 'K']


class Deck:
    def __init__(self):
        self.cards = []
        self.build()

    def build(self):
        for suit in SUITS:
            for value in VALUE:
                self.cards.append(Card(value, suit))

    def shuffle(self):
        shuffle(self.cards)

    def show(self):
        i = 0
        for card in self.cards:
            i += 1
            print(f'{i}: {card.show()}')

    def deal(self):
        return self.cards.pop()

    def count(self):
        return len(self.cards)
