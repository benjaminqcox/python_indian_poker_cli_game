class Card:
    card_values = {'A': 14, 'K': 13, 'Q': 12, 'J': 11}
    magic_numbers = [2, 7, 8, 10]

    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def show(self):
        return f'{self.value}{self.suit}'

    def get_card_value(self):
        if self.value in self.card_values:
            return self.card_values[self.value]
        return int(self.value)

    def is_magic(self):
        if self.get_card_value() in self.magic_numbers:
            return True
        return False
