from evaluator import *
from player import *
from dealer import *
from table import *
from card_enums import PHASE, BUTTON

class TexasHoldemGame:
    def __init__(self, player_names, starting_chips=1000, verbose=False):
        self.players = [RandomPlayer(name, chips=starting_chips) for name in player_names]
        self.dealer = Dealer()
        self.table = Table(self.players)
        self.verbose = verbose
        self.button_position = 0

    def play_round(self):
        """
        Plays one full round (hand) of Texas Hold'em:
         1) shuffle/reset
         2) rotate dealer button (positions)
         3) post blinds
         4) deal hole cards (already done in round setup)
         5) preflop betting
         6) flop & betting
         7) turn & betting
         8) river & betting
         9) showdown & pot distribution
        """
        # 1) Round Setup (shuffle, reset pot, reset players, deal holes)
        self._round_setup()

        # 2) Assign positions (Dealer, SB, BB) for this round
        self._assign_positions()

        # 3) Post blinds
        self._calculate_dynamic_blinds()
        self._post_blinds()

        # 4) Preflop betting
        self._betting_round(PHASE.PF)
        if self._check_for_default_winner():
            self._rotate_button()
            return

        # 5) Flop
        self.dealer.deal_community_cards(3)
        self._log_community_cards(PHASE.FLOP)
        self._betting_round(PHASE.FLOP)
        if self._check_for_default_winner():
            self._rotate_button()
            return

        # 6) Turn
        self.dealer.deal_community_cards(1)
        self._log_community_cards(PHASE.TURN)
        self._betting_round(PHASE.TURN)
        if self._check_for_default_winner():
            self._rotate_button()
            return

        # 7) River
        self.dealer.deal_community_cards(1)
        self._log_community_cards(PHASE.RIVER)
        self._betting_round(PHASE.RIVER)
        if self._check_for_default_winner():
            self._rotate_button()
            return

        # 8) Showdown
        self._showdown()

        # 9) Rotate button
        self._rotate_button()

    def _round_setup(self):
        """
        Reset deck, pot, players' hands/bets, then deal hole cards.
        """
        # Shuffle/Reset deck and clear community cards
        self.dealer.reset_deck()

        # Reset the table pot
        self.table.reset_pot()

        # Reset each player's state for a new hand
        for player in self.players:
            player.reset_hand()

        # Deal two hole cards to each player
        self.dealer.deal_hole_cards(self.players)

        if self.verbose:
            for p in self.players:
                print(f"{p.name}'s hand: {p.hand_str()}")

    def _assign_positions(self):
        """
        Assign dealer, SB, BB based on current button_position index.
        """
        n = len(self.players)

        # Clear old positions
        for p in self.players:
            p.position = BUTTON.NONE

        # Dealer
        dealer_p = self.players[self.button_position]
        dealer_p.position = BUTTON.DEALER

        # SB
        sb_index = (self.button_position + 1) % n
        sb_p = self.players[sb_index]
        sb_p.position = BUTTON.SB

        # BB
        bb_index = (self.button_position + 2) % n
        bb_p = self.players[bb_index]
        bb_p.position = BUTTON.BB

        if self.verbose:
            print("\nPositions:")
            print(f"  Dealer: {dealer_p.name}")
            print(f"  Small Blind: {sb_p.name}")
            print(f"  Big Blind: {bb_p.name}")

    def _calculate_dynamic_blinds(self):
        """
        Determine the blinds based on the smallest stack among active players.
        E.g., small blind = 10% of lowest stack (floored to at least 1),
        big blind = 2x small blind.
        """
        # Find the lowest chip count among players who haven't busted
        lowest_chips = min(p.chips for p in self.players if p.chips > 0)

        # Compute small blind as 10% of that, ensure at least 1 chip
        calculated_small_blind = max(1, int(lowest_chips * 0.1))
        calculated_big_blind = calculated_small_blind * 2

        # Store these as attributes for usage in _post_blinds
        self.current_small_blind = calculated_small_blind
        self.current_big_blind = calculated_big_blind

        if self.verbose:
            print(f"\nLowest stack: {lowest_chips} chips")
            print(f"Small Blind set to {self.current_small_blind}")
            print(f"Big Blind set to {self.current_big_blind}")

    def _post_blinds(self):
        """
        SB and BB place the computed blinds into the pot.
        """
        sb_player = next((p for p in self.players if p.position == BUTTON.SB), None)
        bb_player = next((p for p in self.players if p.position == BUTTON.BB), None)

        if sb_player and sb_player.chips > 0:
            sb_amount = min(self.current_small_blind, sb_player.chips)
            sb_player.place_bet(sb_amount)
            if self.verbose:
                print(f"{sb_player.name} posts small blind of {sb_amount}.")

        if bb_player and bb_player.chips > 0:
            bb_amount = min(self.current_big_blind, bb_player.chips)
            bb_player.place_bet(bb_amount)
            if self.verbose:
                print(f"{bb_player.name} posts big blind of {bb_amount}.")

        self.table.collect_bets()

    def _betting_round(self, phase):
        """
        Conduct a betting round that continues until all non-folded players
        have matched the highest bet or folded. (Simplified version.)
        """
        if self.verbose:
            print(f"\n--- {phase.name} Betting Round ---")

        # We'll do multiple cycles around the table until stable
        def active_players():
            return [p for p in self.players if not p.folded and p.chips > 0]

        highest_bet = 0
        start_index = self._first_to_act(phase)

        while True:
            action_happened = False

            for i in range(len(self.players)):
                idx = (start_index + i) % len(self.players)
                player = self.players[idx]

                if player.folded or player.chips <= 0:
                    continue

                # If all active players' bets match highest_bet, no need to continue
                if self._all_bets_matched(highest_bet, active_players()):
                    break

                call_amount = highest_bet - player.current_bet
                old_bet = player.current_bet

                # Use your player's "decision" method (RandomPlayer, etc.)
                player.make_decision(highest_bet, call_amount)

                new_bet = player.current_bet

                # If they raised more than just call_amount, update highest_bet
                if not player.folded and (new_bet > old_bet + call_amount):
                    highest_bet = new_bet

                if new_bet != old_bet:
                    action_happened = True

            # End conditions
            if self._all_bets_matched(highest_bet, active_players()):
                break
            if not action_happened:
                # No change in a full cycle, avoid infinite loop
                break
            if len(active_players()) <= 1:
                # Only one left? They get the pot
                break

        # After all betting is done, move the bets to the pot
        self.table.collect_bets()

    def _all_bets_matched(self, highest_bet, active_players):
        """
        Returns True if all active players have bet at least 'highest_bet'
        or are all-in (chips == 0).
        """
        for p in active_players:
            if p.current_bet < highest_bet and p.chips > 0:
                return False
        return True

    def _first_to_act(self, phase):
        """
        Determine the index of the player who acts first this street.
        - Preflop: to the left of the BB
        - Postflop: to the left of the Dealer
        """
        n = len(self.players)
        if phase == PHASE.PF:
            # Preflop acts left of BB
            bb_index = next((i for i, p in enumerate(self.players) if p.position == BUTTON.BB), 0)
            return (bb_index + 1) % n
        else:
            # Postflop acts left of the Dealer
            return (self.button_position + 1) % n

    def _check_for_default_winner(self):
        """
        If there's only one active (non-folded) player left,
        that player immediately wins the pot.
        """
        active_players = [p for p in self.players if not p.folded]
        if len(active_players) == 1:
            winner = active_players[0]
            if self.verbose:
                print(f"Winner by default (everyone else folded): {winner.name}")
            self.table.distribute_pot(winner)
            return True
        if len(active_players) == 0:
            # Everyone folded? Very rare scenario
            if self.verbose:
                print("All players folded. No winner.")
            return True
        return False

    def _showdown(self):
        """
        Evaluate the remaining players' hole cards + community
        and determine a winner (or tie).
        """
        winners = Evaluator.determine_winner(self.players, self.dealer.community_cards)
        # If tie returns a list, else single Player
        if isinstance(winners, list):
            # multiple winners or single in a list
            if len(winners) == 1:
                # it's still a list but just has one winner
                if self.verbose:
                    print("Winner:", winners[0].name)
            else:
                # true tie with multiple winners
                if self.verbose:
                    print("Tie between:", ", ".join(w.name for w in winners))
        else:
            # 'winners' is a single Player
            winners = [winners]  # <--- wrap the single winner in a list
            if self.verbose:
                print("Winner:", winners[0].name)

        self.table.distribute_pot(winners)

    def _log_community_cards(self, phase):
        """
        Print community cards to the console if verbose is True.
        """
        if self.verbose:
            print(f"\n--- {phase.name} ---")
            comm_str = ", ".join(str(c) for c in self.dealer.community_cards)
            print("Community Cards:", comm_str)

    def _rotate_button(self):
        """
        Move the dealer button to the next player for next round.
        """
        self.button_position = (self.button_position + 1) % len(self.players)

if __name__ == "__main__":
    player_names = ["Alice", "Bob", "Charlie"]
    game = TexasHoldemGame(player_names, verbose=True)
    for i in range(3):
        print(f"\n===== ROUND {i+1} =====")
        game.play_round()
        # Show chip counts
        for p in game.players:
            print(f"{p.name}: {p.chips} chips")
        print("---------------")
