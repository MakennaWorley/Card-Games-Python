class Table:
    def __init__(self, players):
        self.players = players
        self.pot = 0
        self.current_bet = 0

    def collect_bets(self):
        for player in self.players:
            if not player.folded:
                self.pot += player.current_bet
                player.current_bet = 0

    def reset_betting_round(self):
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0

    def distribute_pot(self, winner):
        winner.chips += self.pot
        self.pot = 0
