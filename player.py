from card import *
from card_enums import *
from single_deck import SingleDeck

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

if __name__ == '__main__':
    deck = SingleDeck()
    deck.shuffle()
    deck.show_top_cards(5)
    print("-" * 30)

    player = Player("Alice", chips=500, position=BUTTON.DEALER)

    dealt_cards = [deck.draw_card(), deck.draw_card()]
    player.receive_cards(dealt_cards)

    for card in player.hand:
        print(card)
    print("-" * 30)

    try:
        bet_amount = 100
        player.place_bet(bet_amount)
        print(
            f"Player placed a bet of {bet_amount}. Remaining chips: {player.chips}, Current bet: {player.current_bet}")
    except ValueError as e:
        print("Error placing bet:", e)
    print("-" * 30)

    try:
        bet_amount = 500
        player.place_bet(bet_amount)
        print(
            f"Player placed a bet of {bet_amount}. Remaining chips: {player.chips}, Current bet: {player.current_bet}")
    except ValueError as e:
        print("Error placing bet:", e)
    print("-" * 30)

    print(player.folded)
    player.fold()
    print(player.folded)
    print("-" * 30)

    player.reset_hand()

    dealt_cards = [deck.draw_card(), deck.draw_card()]
    player.receive_cards(dealt_cards)

    for card in player.hand:
        print(card)

    print(player.current_bet, player.folded)
    print("-" * 30)

    deck.show_top_cards(5)
