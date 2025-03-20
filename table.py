from card_enums import *
from player import Player

class Table:
    def __init__(self, players):
        self.players = players
        self.pot = 0
        self.current_bet = 0

    def process_bet(self, player, amount):
        if amount < self.current_bet:
            raise ValueError("Bet must be at least the current bet amount.")
        elif amount < player.current_bet:
            raise ValueError("Bet cannot be lower than what you've already put in.")
        additional_bet = amount - player.current_bet
        if additional_bet > player.chips:
            raise ValueError("Not enough chips to call or raise that amount.")
        player.place_bet(additional_bet)
        if amount > self.current_bet:
            self.current_bet = amount

    def player_action(self, player, action, amount=0):
        if player.folded:
            print(f"{player.name} has already folded.")
            return
        if action == "call":
            # Calculate call amount
            call_amount = self.current_bet - player.current_bet
            self.process_bet(player, player.current_bet + call_amount)
        elif action == "raise":
            # Raise must be at least greater than current bet
            self.process_bet(player, player.current_bet + amount)
        elif action == "fold":
            player.fold()
        else:
            raise ValueError("Invalid action.")

    def collect_bets(self):
        for player in self.players:
            if not player.folded:
                self.pot += player.current_bet
                player.current_bet = 0

    def reset_betting_round(self):
        self.current_bet = 0
        for player in self.players:
            player.current_bet = 0

    def distribute_pot(self, winners):
        if not winners:
            raise ValueError("There must be at least one winner to distribute the pot.")

        share = self.pot // len(winners)
        for winner in winners:
            winner.chips += share
        self.pot = 0

if __name__ == '__main__':
    players = [
        Player("Alice", chips=1000, position=BUTTON.DEALER),
        Player("Bob", chips=1000, position=BUTTON.SB),
        Player("Charlie", chips=1000, position=BUTTON.BB)
    ]

    table = Table(players)

    for p in players:
        print(f"{p.name}: Chips={p.chips}, Current Bet={p.current_bet}, Folded={p.folded}")
    print("-" * 30)

    print("First Betting Round:")
    table.player_action(players[0], action="raise", amount=100)
    table.player_action(players[1], action="call")
    table.player_action(players[2], action="fold")

    for p in players:
        print(f"{p.name}: Chips={p.chips}, Current Bet={p.current_bet}, Folded={p.folded}")
    print(f"Table Current Bet: {table.current_bet}")
    print("-" * 30)

    table.collect_bets()
    print(f"Table Pot: {table.pot}")
    for p in players:
        print(f"{p.name}: Current Bet={p.current_bet}")
    print("-" * 30)

    table.reset_betting_round()
    print("Betting round reset.")
    for p in players:
        print(f"{p.name}: Current Bet={p.current_bet}")
    print("-" * 30)

    print("Second Betting Round:")
    table.player_action(players[1], action="raise", amount=150)
    table.player_action(players[0], action="call")

    for p in players:
        print(f"{p.name}: Chips={p.chips}, Current Bet={p.current_bet}, Folded={p.folded}")
    print(f"Table Current Bet: {table.current_bet}")
    print("-" * 30)

    table.collect_bets()
    print(f"Table Pot: {table.pot}")
    for p in players:
        print(f"{p.name}: Chips={p.chips}")
    print("-" * 30)

    table.distribute_pot([players[1]])
    for p in players:
        print(f"{p.name}: Chips={p.chips}")
    print(f"Table Pot: {table.pot}")
