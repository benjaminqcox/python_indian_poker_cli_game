import sys
import os
from random import randint
from typing import Tuple, List
from helper import get_multiple_input_between_range
from player import Player
from bot import Bot
from deck import Deck
from card import Card


def is_game_over(player):
    return not (player.get_playable_row() != 'Game over')



def is_same_value(cards: List[Card]):
    original_card = cards[0]
    original_card_value = original_card.get_card_value()
    for card in cards:
        if card.get_card_value() != original_card_value:
            return False
    return True


def change_player(i: int):
    return (i - 1) * -1


class Game:
    def __init__(self):
        self.banished = []
        self.centre = []
        self.deck = Deck()
        self.player = Player('You') # adding a better way of initializing players would be best
        self.bot = Bot('Bot', is_bot=True)

    def deal_game(self, players):
        rows = ['face_down', 'face_up', 'hand']
        for row in rows:
            for i in range(5):
                for each_player in players:
                    if self.deck.count() > 0:
                        each_player.cards[row].append(self.deck.deal())

    def show_table(self):
        self.bot.show_cards()
        print(f'\n   Centre: {self.show_centre()}   Deck: {(self.deck.count() if self.deck.count() > 0 else "Empty")}\n')
        self.player.show_cards()

    def show_centre(self):
        centre = self.get_centre()
        return centre.show() if centre != 'Empty' else centre

    def get_centre(self):
        return self.centre[-1] if len(self.centre) > 0 else 'Empty'

    def get_centre_value(self):
        centre = self.get_centre()
        if centre == 'Empty':
            return 0
        return centre.get_card_value()

    def pickup_centre(self):
        temp_centre = self.centre
        self.centre = []
        return temp_centre

    def pickup_to_five(self, player):
        while self.deck.count() > 0 and len(player.cards['hand']) < 5:
            player.add_to_hand(self.deck.deal())

    def first_legal_card(self, current_player, row):
        # This function is called after has legal move, so we can go off the basis that there is a legal card

        for card in current_player.cards[row]:
            if not card.is_magic() and self.is_legal_card(card):
                return card
        return current_player.cards[row][0]  # As the row is sorted, the first card is a magic card. If not, the return
        # will come from the for loop

    def all_indexes_matching_chosen_card(self, current_player, row, card):
        matching_card_indexes = []
        for card_index in range(len(current_player.cards[row])):
            current_card = current_player.cards[row][card_index]
            if current_card.get_card_value() == card.get_card_value():
                matching_card_indexes.append(card_index)
        return matching_card_indexes

    def choose_bot_card_indexes(self, current_player, row):
        return self.all_indexes_matching_chosen_card(current_player, row, self.first_legal_card(current_player, row))

    def choose_cards(self, current_player) -> Tuple[str, List[int]]:
        playable_row = current_player.get_playable_row()
        if current_player.is_bot:
            card_choices = self.choose_bot_card_indexes(current_player, playable_row)
        else:
            card_choices = [number - 1 for number in get_multiple_input_between_range(1, len(current_player.cards[playable_row]))]
        return playable_row, card_choices

    def is_legal_with_magic_rule(self, card, centre):
        if centre == 'Empty':
            return True
        centre_value = centre.get_card_value()
        if centre_value == 7:
            return self.is_legal_with_magic_rule(card, self.card_under_seven())
        elif centre_value == 8:
            return card.get_card_value() <= 8
        return card.get_card_value() >= centre_value

    def is_legal_card(self, card_chosen: Card):
        centre_card = self.get_centre()
        if centre_card == 'Empty' or card_chosen.is_magic():
            return True
        if centre_card.is_magic():
            return self.is_legal_with_magic_rule(card_chosen, centre_card)
        return card_chosen.get_card_value() >= centre_card.get_card_value()

    def has_legal_move(self, player):
        row = player.get_playable_row()
        if row == 'face_down':
            return True
        for card in player.cards[row]:
            if self.is_legal_card(card):
                return True
        return False

    def place_card_in_centre(self, card):
        self.centre.append(card)

    def card_under_seven(self):
        store_sevens = []
        while self.get_centre() != 'Empty' and self.get_centre().get_card_value() == 7:
            store_sevens.append(self.centre.pop())
        card_under_sevens = self.get_centre()
        self.centre.extend(store_sevens)
        return card_under_sevens

    def ten_rule(self):
        self.banished = self.centre
        self.centre = []

    def play_cards(self, current_player, row, card_indexes):
        if row == 'face_down':
            self.play_face_down(current_player, card_indexes)
        else:
            self.play_legal_cards(current_player, row, card_indexes)

    def play_legal_cards(self, current_player, row, card_indexes):
        try_again = False
        chosen_cards = [current_player.cards[row][card_index] for card_index in card_indexes]
        if not is_same_value(chosen_cards):
            print(f'To play multiple cards, you must match the values, you chose: {[card.show() for card in chosen_cards]} ')
            try_again = True
        elif not self.is_legal_card(chosen_cards[0]):
            print(f'{chosen_cards[0].show()} is not a legal move. Look at the middle and try again.')
            try_again = True
        if try_again:
            row, card_indexes = self.choose_cards(current_player)
            return self.play_legal_cards(current_player, row, card_indexes)
        # By sorting in reverse order (e.g. [5, 2]) I can remove each index without rearranging the row of cards
        card_indexes.sort(reverse=True)
        for index in card_indexes:
            self.place_card_in_centre(current_player.play_card(row, index))


    def play_face_down(self, current_player, card_indexes):
        # I don't like the repeating place_card_in_centre function, but I cannot think of a more concise way atm
        chosen_card = current_player.play_card('face_down', card_indexes[0])
        if not self.is_legal_card(chosen_card):
            self.place_card_in_centre(chosen_card)
            current_player.cards['hand'].extend(self.pickup_centre())
        else:
            self.place_card_in_centre(chosen_card)


    def play_face_up_then_pick_up(self, current_player, card_indexes):
        chosen_cards = [current_player.cards['face_up'][card_index] for card_index in card_indexes]
        if not is_same_value(chosen_cards):
            print(f'To play multiple cards, you must match the values, you chose: {[card.show() for card in chosen_cards]} ')
            row, card_indexes = self.choose_cards(current_player)
            self.play_face_up_then_pick_up(current_player, card_indexes)
        card_indexes.sort(reverse=True)  # By sorting in reverse order (e.g. [5, 2]) I can remove each index without rearranging the row of cards
        for index in card_indexes:
            self.place_card_in_centre(current_player.play_card('face_up', index))
        current_player.cards['hand'].extend(self.pickup_centre())

    def play_round(self, current_player):
        row = current_player.get_playable_row()
        if self.has_legal_move(current_player):
            # get player card choice
            row, card_indexes = self.choose_cards(current_player)
            self.play_cards(current_player, row, card_indexes)
            # if row is face_down, only play 1 card, the first card chosen
        else:
            if row == 'hand':
                current_player.cards['hand'].extend(self.pickup_centre())
            else:
                row, card_indexes = self.choose_cards(current_player)
                if row == 'face_up':
                    self.play_face_up_then_pick_up(current_player, card_indexes)
                elif row == 'face_down':
                    self.play_face_down(current_player, card_indexes)


    def play_game(self):
        # make players, deck, shuffle, deal cards, place card in centre then randomise who starts
        players = [self.player, self.bot]
        rows_to_sort = ['face_up', 'hand']
        self.deck.shuffle()
        self.deal_game(players)
        for row in rows_to_sort:
            for player in players:
                player.sort_cards(row)
        if self.deck.count() > 0:
            self.place_card_in_centre(self.deck.deal())
            if self.get_centre_value() == 10:
                self.ten_rule()

        i = randint(0, 1)  # starting player
        while not is_game_over(players[i]):
            # Way to switch player by alternating i between index 0 and 1
            print(f'It is {players[i].name}\'s go')
            self.show_table()
            self.play_round(players[i])
            self.pickup_to_five(players[i])
            players[i].sort_cards('hand')
            if self.get_centre_value() == 10:
                self.ten_rule()
                i = change_player(i)
            i = change_player(i)
            os.system('cls')

        os.system('cls')
        self.show_table()
        print(f'#####################   {players[i].name} wins   #####################')
        sys.exit()
