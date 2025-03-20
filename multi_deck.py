from single_deck import *

class MultiDeck(SingleDeck):
    def __init__(self, num=1):
        super().__init__()
        self.cards = [Card(rank, suit) for _ in range(num) for suit in SUIT for rank in RANK]

if __name__ == '__main__':
    deck = MultiDeck(num=3)
    deck.show_top_cards(5)
    print(f"Remaining cards: {len(deck.cards)}")
    print("-" * 30)

    deck.shuffle()
    deck.show_top_cards(5)
    print(f"Remaining cards: {len(deck.cards)}")
    print("-" * 30)

    deck.show_top_cards(12)
    print("-" * 30)

    for i in range(10):
        print(deck.draw_card())
    print("-" * 30)
    deck.show_top_cards(2)
    print("-" * 30)

    new_card = Card(RANK.ACE, SUIT.HEARTS)
    for i in range(10):
        deck.add_card(new_card)
    deck.display_table()
    print("-" * 30)

    deck.remove_card(new_card)
    deck.display_table()
