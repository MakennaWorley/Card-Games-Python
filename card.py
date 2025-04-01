from card_enums import RANK, SUIT

class Card:
    def __init__(self, rank: RANK, suit: SUIT):
        self.rank = rank
        self.suit = suit

    @property
    def value(self):
        return self.rank.value

    def __str__(self):
        return f"{self.rank.name.capitalize()} of {self.suit.value}"

    def change_rank(self, new_rank: RANK):
        self.rank = new_rank

    def change_suit(self, new_suit: SUIT):
        self.suit = new_suit

    def change_card(self, new_rank: RANK, new_suit: SUIT):
        self.rank = new_rank
        self.suit = new_suit

if __name__ == "__main__":
    card = Card(RANK.ACE, SUIT.HEARTS)
    print(card)
    print("-" * 30)

    card.change_rank(RANK.TWO)
    print(card)
    print("-" * 30)

    card.change_suit(SUIT.DIAMONDS)
    print(card)
    print("-" * 30)

    card.change_card(RANK.ACE, SUIT.CLUBS)
    print(card)
