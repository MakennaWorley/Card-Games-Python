from multi_deck import MultiDeck
from single_deck import SingleDeck
from card_enums import *
from player import Player

class Dealer:
    def __init__(self, num_decks=1):
        if num_decks < 1:
            raise ValueError("Number of decks must be greater than 0")
        elif num_decks < 2:
            self.deck = SingleDeck()
        else:
            self.deck = MultiDeck(num_decks)

        self.deck.shuffle()
        self.community_cards = []

    def deal_hole_cards(self, players):
        for _ in range(2):
            for player in players:
                player.receive_cards([self.deck.draw_card()])

    def deal_community_cards(self, count):
        self.deck.draw_card()  # Burn a card
        self.community_cards.extend([self.deck.draw_card() for _ in range(count)])

    def reset_deck(self, num_decks=1):
        if num_decks < 1:
            raise ValueError("Number of decks must be greater than 0")
        elif num_decks < 2:
            self.deck = SingleDeck()
        else:
            self.deck = MultiDeck(num_decks)
        self.deck.shuffle()
        self.community_cards = []


if __name__ == '__main__':
    players = [
        Player("Alice", chips=1000, position=BUTTON.DEALER),
        Player("Bob", chips=1000, position=BUTTON.SB),
        Player("Charlie", chips=1000, position=BUTTON.BB)
    ]

    dealer = Dealer(num_decks=2)
    dealer.deck.display_table()

    dealer.deal_hole_cards(players)
    for player in players:
        print(f"{player.name}'s hand:")
        for card in player.hand:
            print(f"  {card}")
        print("-" * 30)

    dealer.deal_community_cards(3)
    for card in dealer.community_cards:
        print(f"  {card}")
    print("-" * 30)

    dealer.deck.display_table()
    dealer.reset_deck(2)
    print("-" * 30)
    dealer.deck.display_table()
