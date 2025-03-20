import random
from card import Card
from card_enums import SUIT, VALUE
from multi_deck import MultiDeck
from single_deck import SingleDeck

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

    def reset_deck(self):
        self.deck = SingleDeck()
        self.deck.shuffle()
        self.community_cards = []
