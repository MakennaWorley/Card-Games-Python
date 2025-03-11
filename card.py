from card_enums import *

class Card:
    def __init__(self, suit: SUIT, value: VALUE):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f'{self.value.value} of {self.suit.value}'

    def change_value(self, new_value: VALUE):
        self.value = new_value

    def change_suit(self, new_suit: SUIT):
        self.suit = new_suit

    def change_card(self, new_suit: SUIT, new_value: VALUE):
        self.suit = new_suit
        self.value = new_value