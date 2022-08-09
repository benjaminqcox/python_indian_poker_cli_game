import sys
import os
from random import randint
from typing import List

from card import Card
from player import Player
from bot import Bot
from deck import Deck

def change_player(i: int):
    return (i - 1) * -1


class Game:
    def __init__(self):
        self.banished = []
        self.centre = []
        self.deck = Deck()
        self.player = Player('You') # adding a better way of initializing players would be best
        self.bot = Bot('Bot', is_bot=True)

    def deal_game(self, players: List[Player]) -> None:  # Good
        rows = ['face_down', 'face_up', 'hand']
        for row in rows:
            for i in range(5):
                for each_player in players:
                    if self.deck.count() > 0:
                        each_player.cards[row].append(self.deck.deal())
        if self.deck.count() > 0:
            self.centre.append(self.deck.deal())
        if self.get_centre_value() == 10:
            self.ten_rule()


    def deal_to_five(self, current_player: Player) -> None:
        while self.deck.count() > 0 and len(current_player.cards['hand']) < 5:
            current_player.add_to_hand(self.deck.deal())

    def show_table(self) -> None:  # Good
        self.bot.show_cards()
        print(f'\n   Centre: {self.show_centre()}   Deck: {(self.deck.count() if self.deck.count() > 0 else "Empty")}\n')
        self.player.show_cards()

    def show_centre(self) -> str:  # Good
        centre = self.get_centre()
        return centre.show() if centre != 'Empty' else centre

    def get_centre(self) -> Card | str:  # Good
        return self.centre[-1] if len(self.centre) > 0 else 'Empty'

    def get_centre_value(self) -> int:  # Good
        centre = self.get_centre()
        if centre == 'Empty':
            return 0
        return centre.get_card_value()

    def move_centre_pile(self) -> List[Card]:  # Good
        temp_centre = self.centre
        self.centre = []
        return temp_centre


    def card_under_seven(self) -> Card:
        store_sevens = []
        while self.get_centre() != 'Empty' and self.get_centre().get_card_value() == 7:
            store_sevens.append(self.centre.pop())
        card_under_sevens = self.get_centre()
        self.centre.extend(store_sevens)
        return card_under_sevens

    def ten_rule(self) -> None:
        self.banished = self.centre
        self.centre = []

    def play_round(self, current_player: Player | Bot) -> None:
        centre_card = self.card_under_seven()
        row = current_player.get_playable_row()
        has_move = current_player.has_legal_move(centre_card)
        if not has_move and row == 'hand':
            current_player.add_to_hand(self.move_centre_pile())
        else:
            chosen_card_indexes = current_player.choose_card_indexes(row, centre_card)
            if row == 'face_down':
                chosen_card_indexes = [chosen_card_indexes[0]]
            else:
                while not current_player.has_chosen_multiple_matching_cards(row, chosen_card_indexes) or (not current_player.has_chosen_legal_card(current_player.cards[row][chosen_card_indexes[0]], centre_card) and has_move):
                    chosen_card_indexes = current_player.choose_card_indexes(row, centre_card)

            chosen_cards = current_player.play_cards(row, chosen_card_indexes)
            self.centre += chosen_cards
            if not current_player.has_chosen_legal_card(chosen_cards[0], centre_card):
                current_player.add_to_hand(self.move_centre_pile())

        self.deal_to_five(current_player)
        current_player.sort_cards('hand')

    def play_game(self) -> None: # Can be made more concise and easy to read
        # Game doesn't always end on the bots final card, they play theres then wait for me to play mine, then it says they win.
        # Not too much of an issue but it could mean if it's a close game, the wrong person wins
        # make players, deck, shuffle, deal cards, place card in centre then randomise who starts
        players = [self.player, self.bot]
        rows_to_sort = ['face_up', 'hand']
        self.deck.shuffle()
        self.deal_game(players)
        for row in rows_to_sort:
            for player in players:
                player.sort_cards(row)
        i = randint(0, 1)  # starting player
        next_player = i
        while players[i].has_cards_left():
            # Way to switch player by alternating i between index 0 and 1
            i = next_player
            print(f'It is {players[i].name}\'s go')
            self.show_table()
            self.play_round(players[i])
            if self.get_centre_value() == 10:
                self.ten_rule()
            else:
                next_player = change_player(i)
            os.system('cls||clear')

        os.system('cls||clear')
        self.show_table()
        print(f'#####################   {players[i].name} wins   #####################')
        sys.exit()
