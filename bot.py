from random import randint
from typing import List

from card import Card
from player import Player

class Bot(Player):
    def choose_card_indexes(self, row: str, centre_card: Card) -> List[int]:
        if row == 'face_down':
            return [randint(0, len(self.cards[row])-1)]
        bot_selection = self.bot_card_selection(row, centre_card)
        return self.all_indexes_matching_chosen_card(row, bot_selection)

    def bot_card_selection(self, row, centre_card):
        has_magic = self.cards[row][0].is_magic()
        for card_index in range(len(self.cards[row])):
            if not self.cards[row][card_index].is_magic() and self.has_chosen_legal_card(self.cards[row][card_index], centre_card):
                return card_index
        return randint(0, len(self.cards[row])-1) if not has_magic else 0
