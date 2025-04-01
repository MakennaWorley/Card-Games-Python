from multi_deck import MultiDeck
from single_deck import SingleDeck
from card_enums import BUTTON
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

    def deal_community_cards(self, count, players):
        self.deck.draw_card()  # Burn a card
        new_cards = [self.deck.draw_card() for _ in range(count)]
        self.community_cards.extend(new_cards)
        # Update each player's community cards if a players list is provided.
        if players is not None:
            for player in players:
                # Make a copy to avoid unintended modifications.
                player.community_cards = self.community_cards.copy()

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
        print(f"{player.name}'s hand: {player.hand_str()} and community cards: {player.community_cards_str()}")
        print("-" * 30)

    # Pass the players list so that their community_cards get updated.
    dealer.deal_community_cards(3, players)
    print("Community Cards on the Table:")
    for card in dealer.community_cards:
        print(f"  {card}")
    print("-" * 30)

    # Confirm that each player now has the community cards updated.
    for player in players:
        print(f"{player.name}'s hand: {player.hand_str()} and community cards: {player.community_cards_str()}")
        print("-" * 30)

    dealer.deck.display_table()
    dealer.reset_deck(2)
    print("-" * 30)
    dealer.deck.display_table()
