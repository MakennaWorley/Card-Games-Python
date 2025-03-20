import random
from evaluator import *
from player import *
from dealer import *
from table import *

class TexasHoldemGame:
    def __init__(self, player_names):
        self.players = [Player(name) for name in player_names]
        self.dealer = Dealer()
        self.table = Table(self.players)
        self.active_player_index = 0
        self.phase = PHASE.PF

    def play_round(self):
        self.dealer.reset_deck()
        for player in self.players:
            player.reset_hand()

        self.players[0].position = BUTTON.DEALER
        self.players[1].position = BUTTON.SB
        self.players[2].position = BUTTON.BB

        self.dealer.deal_hole_cards(self.players)

        self.phase = PHASE.PF
        self.betting_round()

        self.phase = PHASE.FLOP
        self.dealer.deal_community_cards(3)
        self.betting_round()

        self.phase = PHASE.TURN
        self.dealer.deal_community_cards(1)
        self.betting_round()

        self.phase = PHASE.RIVER
        self.dealer.deal_community_cards(1)
        self.betting_round()

        winner = Evaluator.determine_winner(self.players, self.dealer.community_cards)
        if isinstance(winner, list):
            winner_names = ", ".join([w.name for w in winner])
            print(f"Winners: {winner_names}")
        else:
            print(f"Winner: {winner.name}")

        self.table.distribute_pot(winner)

    def betting_round(self):
        for player in self.players:
            if not player.folded:
                bet = min(100, player.chips)  # Placeholder bet logic
                player.place_bet(bet)
        self.table.collect_bets()

if __name__ == "__main__":
    player_names = ["Alice", "Bob", "Charlie"]
    for _ in range(10):
        game = TexasHoldemGame(player_names)
        game.play_round()
