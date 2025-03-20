from single_deck import *

class MultiDeck(SingleDeck):
    def __init__(self, num=1):
        super().__init__()
        self.cards = [Card(suit, value) for _ in range(num) for suit in SUIT for value in VALUE]

    def shuffle(self):
        random.shuffle(self.cards)

    def display_table(self):
        ranks = [value.value for value in VALUE]
        suits = [suit.value for suit in SUIT]
        table = {suit: [0 for _ in ranks] for suit in suits}

        for card in self.cards:
            table[card.suit.value][ranks.index(card.value.value)] += 1

        df = pd.DataFrame(table, index=ranks)

        df["Total"] = df.sum(axis=1)

        df.loc["Total"] = df.sum(axis=0)
        df.at["Total", "Total"] = len(self.cards)

        print(df.to_string())

shoe = MultiDeck(num=3)
shoe.shuffle()
print(shoe.draw_card())
print(f"Remaining cards: {len(shoe.cards)}")
shoe.display_table()
shoe.show_top_cards(20)