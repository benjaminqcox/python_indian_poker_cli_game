from typing import List
from helper import get_multiple_input_between_range
from card import Card



class Player:
    def __init__(self, name, is_bot=False):
        self.name = name
        self.cards = {'hand': [], 'face_up': [], 'face_down': []}
        self.is_bot = is_bot

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

    def get_playable_row(self) -> str:
        if len(self.cards['hand']) > 0:
            return 'hand'
        elif len(self.cards['face_up']) > 0:
            return 'face_up'
        elif len(self.cards['face_down']) > 0:
            return 'face_down'
        else:
            return 'Game over'

    def show_cards_in_row(self, row: str) -> None:
        for card in self.cards[row]:
            print(card, end='   ')
        print()

    def play_cards(self, row: str, card_indexes: List[int] | int) -> List[Card]:
        if not isinstance(card_indexes, list):
            return [self.cards[row].pop(card_indexes)]
        card_indexes.sort(reverse=True)
        return [self.cards[row].pop(card_index) for card_index in card_indexes]

    def add_to_hand(self, cards_to_add: Card | List[Card]) -> None:
        if not isinstance(cards_to_add, List):
            cards_to_add = [cards_to_add]
        self.cards['hand'] += cards_to_add

    def sort_cards(self, row: str) -> None:
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



    def all_indexes_matching_chosen_card(self, row: str, card_index: int) -> List[int]:
        matching_card_indexes = []
        chosen_card_value = self.cards[row][card_index].get_card_value()
        for card_index in range(len(self.cards[row])):
            current_card = self.cards[row][card_index]
            if current_card.get_card_value() == chosen_card_value:
                matching_card_indexes.append(card_index)
        return matching_card_indexes

    def choose_card_indexes(self, row: str, centre_card: Card) -> List[int]: # Want to find a method that works for both bot and player
        card_indexes = [number - 1 for number in get_multiple_input_between_range(1, len(self.cards[row]))]
        if row == 'face_down':
            return [card_indexes[0]]
        return card_indexes

    def has_chosen_multiple_matching_cards(self, row: str, card_indexes: List[int]) -> bool:
        chosen_cards = [self.cards[row][card_index] for card_index in card_indexes]
        chosen_card_value = chosen_cards[0].get_card_value()
        for each_card in chosen_cards:
            if each_card.get_card_value() != chosen_card_value:
                return False
        return True

    def has_chosen_legal_card(self, chosen_card, centre_card: Card | str) -> bool:
        # If the card in the centre is a 7, then the card below that is parsed here
        if centre_card == "Empty" or chosen_card.is_magic():
            return True
        centre_card_value = centre_card.get_card_value()
        card_chosen_value = chosen_card.get_card_value()
        if centre_card_value == 8:
            return card_chosen_value <= 8
        return card_chosen_value >= centre_card_value

    def has_legal_move(self, centre_card: Card | str) -> bool:
        row = self.get_playable_row()
        if row == 'face_down':
            return True
        for current_card in self.cards[row]:
            if self.has_chosen_legal_card(current_card, centre_card):
                return True
        return False

    def has_cards_left(self) -> bool:
        return self.get_playable_row() != 'Game over'