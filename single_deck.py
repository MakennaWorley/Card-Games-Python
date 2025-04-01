import random
import pandas as pd

from card import Card
from card_enums import RANK, SUIT

class SingleDeck:
    def __init__(self):
        self.cards = [Card(rank, suit) for suit in SUIT for rank in RANK]

    def __str__(self):
        return "\n".join(str(card) for card in self.cards)

    def add_card(self, card: Card):
        self.cards.append(card)

    def remove_card(self, card: Card):
        self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def show_top_cards(self, num):
        for i, card in enumerate(self.cards[:num], start=1):
            print(f"{i}: {card}")

    def draw_card(self):
        return self.cards.pop(0) if self.cards else None

    def display_table(self):
        ranks = [rank.name for rank in RANK]
        suits = [suit.name for suit in SUIT]

        table = {suit: [0 for _ in ranks] for suit in suits}

        for card in self.cards:
            table[card.suit.name][ranks.index(card.rank.name)] += 1

        df = pd.DataFrame(table, index=ranks)

        df["Total"] = df.sum(axis=1)

        df.loc["Total"] = df.sum(axis=0)
        df.at["Total", "Total"] = len(self.cards)

        print(df.to_string())

if __name__ == '__main__':
    deck = SingleDeck()
    deck.show_top_cards(5)
    print("-" * 30)

    deck.shuffle()
    deck.show_top_cards(5)
    print("-" * 30)

    print(deck.draw_card())
    print("-" * 30)

    deck.show_top_cards(5)
    print("-" * 30)

    new_card = Card(RANK.ACE, SUIT.HEARTS)
    deck.add_card(new_card)
    deck.display_table()
    print("-" * 30)

    deck.remove_card(new_card)
    deck.show_top_cards(5)
    print("-" * 30)

    deck.display_table()
