import random
import pandas as pd

from card import *
from card_enums import *

class SingleDeck:
    def __init__(self):
        self.cards = [Card(suit, value) for suit in SUIT for value in VALUE]

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
        return self.cards.pop() if self.cards else None

    def display_table(self):
        ranks = [value.value for value in VALUE]
        suits = [suit.value for suit in SUIT]
        table = {suit: [" " for _ in ranks] for suit in suits}

        for card in self.cards:
            table[card.suit.value][ranks.index(card.value)] = "X"

        df = pd.DataFrame(table, index=ranks)

        df["Total"] = df.apply(lambda row: sum(1 for x in row if x == "X"), axis=1)

        total_counts = df.map(lambda x: 1 if x == "X" else 0).sum()
        df.loc["Total"] = total_counts
        df.at["Total", "Total"] = len(self.cards)

        print(df.to_string())


deck = SingleDeck()
deck.shuffle()
print(deck.draw_card())
print(f"Remaining cards: {len(deck.cards)}")
deck.display_table()
