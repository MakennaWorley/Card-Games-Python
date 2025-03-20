from card_enums import *

class Card:
    def __init__(self, rank: RANK, suit: SUIT):
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        return self.rank.value

    def __str__(self):
        return f"{self.rank.name.capitalize()} of {self.suit.name.capitalize()}"

    def change_rank(self, new_rank: RANK):
        self.rank = new_rank

    def change_suit(self, new_suit: SUIT):
        self.suit = new_suit

    def change_card(self, new_rank: RANK, new_suit: SUIT):
        self.rank = new_rank
        self.suit = new_suit

card = Card(RANK.ACE, SUIT.HEARTS)
print(card)
card.change_rank(RANK.TWO)
print(card)
card.change_suit(SUIT.DIAMONDS)
print(card)
card.change_card(RANK.ACE, SUIT.CLUBS)
print(card)