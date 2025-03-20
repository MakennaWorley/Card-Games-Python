from card_enums import *

class Player:
    def __init__(self, name, chips=1000, position=BUTTON.PLAYER):
        self.name = name
        self.chips = chips
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.position = position

    def place_bet(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips!")
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.folded = True

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False
