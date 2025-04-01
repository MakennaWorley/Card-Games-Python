import math
from player import Player
from evaluator import Evaluator

class MinimaxPlayer(Player):
    def make_decision(self, highest_bet, call_amount):
        """
        Naive minimax-based decision for a single betting round
        with limited possible actions.
        """
        if self.folded or self.chips <= 0:
            return

        if call_amount >= self.chips:
            expected_fold_value = self.evaluate_fold()
            expected_allin_value = self.evaluate_allin()
            if expected_allin_value >= expected_fold_value:
                self.place_bet(self.chips)
                if self.verbose:
                    print(f"{self.name} goes all-in (minimax).")
            else:
                self.fold()
                if self.verbose:
                    print(f"{self.name} folds (minimax).")
            return

        possible_actions = ["fold", "call", "raise"]
        best_action = None
        best_value = -math.inf

        for action in possible_actions:
            action_value = self.minimax_value_of_action(action, highest_bet, call_amount)

            if action_value > best_value:
                best_value = action_value
                best_action = action

        if best_action == "fold":
            self.fold()
            if self.verbose:
                print(f"{self.name} folds (minimax).")
        elif best_action == "call":
            self.place_bet(call_amount)
            if self.verbose:
                print(f"{self.name} calls {call_amount} (minimax).")
        else:
            raise_amount = min(self.chips - call_amount, max(5, call_amount))
            total_bet = call_amount + raise_amount
            self.place_bet(total_bet)
            if self.verbose:
                print(f"{self.name} raises to {total_bet} (minimax).")

    def minimax_value_of_action(self, action, highest_bet, call_amount):
        """
        Evaluate the EV of a single action by recursively simulating
        the opponent's response, choosing their best (or worst for us) action.
        This is extremely naive for demonstration only.
        """
        if action == "fold":
            return self.evaluate_fold()

        elif action == "call":
            return self.evaluate_post_call()

        else:
            fold_ev = self.evaluate_opponent_fold()
            call_ev = self.evaluate_opponent_call()
            raise_ev = self.evaluate_opponent_reraise()
            return min(fold_ev, call_ev, raise_ev)

    def evaluate_fold(self):
        return 0

    def evaluate_allin(self):
        strength = self.estimate_strength()
        return 300 * (strength - 0.5)

    def evaluate_post_call(self):
        strength = self.estimate_strength()
        return 200 * (strength - 0.5)

    def evaluate_opponent_fold(self):
        strength = self.estimate_strength()
        return 150 + 150 * (strength - 0.5)

    def evaluate_opponent_call(self):
        strength = self.estimate_strength()
        return 200 * (strength - 0.5)

    def evaluate_opponent_reraise(self):
        strength = self.estimate_strength()
        return (200 * (strength - 0.5)) - 50

    def estimate_strength(self):
        cards = self.hand + self.community_cards
        return Evaluator.get_hand_rank(cards)

#===================================================================================================================================

class AlphaBetaPlayer(Player):
    def make_decision(self, highest_bet, call_amount):
        if self.folded or self.chips <= 0:
            return

        if call_amount >= self.chips:
            fold_ev = self.evaluate_fold()
            allin_ev = self.evaluate_allin()
            if allin_ev >= fold_ev:
                self.place_bet(self.chips)
                if self.verbose:
                    print(f"{self.name} goes all-in (alpha-beta).")
            else:
                self.fold()
                if self.verbose:
                    print(f"{self.name} folds (alpha-beta).")
            return

        actions = ["fold", "call", "raise"]
        best_action = None
        alpha = -math.inf
        beta = math.inf
        best_value = -math.inf

        for action in actions:
            value = self.alphabeta_value_of_action(action, highest_bet, call_amount, alpha, beta, maximizing=True)
            if value > best_value:
                best_value = value
                best_action = action

            alpha = max(alpha, value)
            if alpha >= beta:
                break

        if best_action == "fold":
            self.fold()
            if self.verbose:
                print(f"{self.name} folds (alpha-beta).")
        elif best_action == "call":
            self.place_bet(call_amount)
            if self.verbose:
                print(f"{self.name} calls {call_amount} (alpha-beta).")
        else:
            raise_amount = min(self.chips - call_amount, max(5, call_amount))
            total_bet = call_amount + raise_amount
            self.place_bet(total_bet)
            if self.verbose:
                print(f"{self.name} raises to {total_bet} (alpha-beta).")

    def alphabeta_value_of_action(self, action, highest_bet, call_amount, alpha, beta, maximizing=True):
        if action == "fold":
            return self.evaluate_fold()
        elif action == "call":
            return self.evaluate_post_call()
        else:
            fold_ev = self.evaluate_opponent_fold()
            call_ev = self.evaluate_opponent_call()
            raise_ev = self.evaluate_opponent_reraise()

            return min(fold_ev, call_ev, raise_ev)

    def evaluate_fold(self):
        return 0

    def evaluate_allin(self):
        strength = self.estimate_strength()
        return 300 * (strength - 0.5)

    def evaluate_post_call(self):
        strength = self.estimate_strength()
        return 200 * (strength - 0.5)

    def evaluate_opponent_fold(self):
        strength = self.estimate_strength()
        return 150 + 150 * (strength - 0.5)

    def evaluate_opponent_call(self):
        strength = self.estimate_strength()
        return 200 * (strength - 0.5)

    def evaluate_opponent_reraise(self):
        strength = self.estimate_strength()
        return (200 * (strength - 0.5)) - 50

    def estimate_strength(self):
        cards = self.hand + self.community_cards
        return Evaluator.get_hand_rank(cards)
