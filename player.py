from card import Card
class Player:
    def __init__(self, name):
        self.name = name
        self.cards = {'hand': [], 'face_up': [], 'face_down': []}

    def show_cards(self):
        print(f'Player: {self.name}')
        for row, cards in self.cards.items():
            print(f'{row}:', end=' ')
            i = 0
            for card in cards:
                i+=1
                display_card = card.show()
                if row == 'face_down':
                    display_card = 'X'
                print(f'[{i}]: {display_card} ', end=' ')
            print()

    def get_playable_row(self):
        if len(self.cards['hand']) > 0:
            return 'hand'
        elif len(self.cards['face_up']) > 0:
            return 'face_up'
        elif len(self.cards['face_down']) > 0:
            return 'face_down'
        else:
            return 'Game over'

    def show_cards_in_row(self, row):
        for card in self.cards[row]:
            print(card, end='   ')
        print()

    def play_card(self, row, choice):
        return self.cards[row].pop(choice)

    def add_to_hand(self, card):
        self.cards['hand'].append(card)

    def sort_cards(self, row):
        magic_cards = []
        regular_cards = []
        for card in self.cards[row]:
            if card.is_magic():
                magic_cards.append(card)
            else:
                regular_cards.append(card)
        magic_cards.sort(key=lambda x: x.get_card_value())
        regular_cards.sort(key=lambda x: x.get_card_value())
        self.cards[row] = magic_cards + regular_cards


