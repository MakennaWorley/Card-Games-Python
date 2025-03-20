from itertools import combinations
from card_enums import *

class Evaluator:
    HAND_RANKS = {
        "Royal Flush": 10,
        "Straight Flush": 9,
        "Four of a Kind": 8,
        "Full House": 7,
        "Flush": 6,
        "Straight": 5,
        "Three of a Kind": 4,
        "Two Pair": 3,
        "One Pair": 2,
        "High Card": 1
    }

    @staticmethod
    def evaluate_hand(player, community_cards):
        all_cards = player.hand + community_cards
        best_hand = (1, [])
        best_rank = 1 # 2

        for combo in combinations(all_cards, 5):
            rank, tiebreaker = Evaluator.get_hand_rank(combo)
            if rank > best_rank or (rank == best_rank and tiebreaker > best_hand[1]):
                best_rank = rank
                best_hand = (rank, tiebreaker)

        return best_rank, best_hand

    @staticmethod
    def get_hand_rank(cards):
        values = sorted([list(VALUE).index(card.value) for card in cards], reverse=True)
        suits = [card.suit for card in cards]

        is_flush = len(set(suits)) == 1
        is_straight = all(values[i] - 1 == values[i + 1] for i in range(4))

        # Correct detection for Royal Flush
        is_royal = is_flush and values[:5] == [12, 11, 10, 9, 0]

        value_counts = {v: values.count(v) for v in values}
        sorted_counts = sorted(value_counts.items(), key=lambda x: (-x[1], -x[0]))

        if is_royal:
            return Evaluator.HAND_RANKS["Royal Flush"], values
        if is_flush and is_straight:
            return Evaluator.HAND_RANKS["Straight Flush"], values
        if 4 in value_counts.values():
            return Evaluator.HAND_RANKS["Four of a Kind"], [sorted_counts[0][0], sorted_counts[1][0]]
        if sorted(value_counts.values()) == [2, 3]:
            return Evaluator.HAND_RANKS["Full House"], [sorted_counts[0][0], sorted_counts[1][0]]
        if is_flush:
            return Evaluator.HAND_RANKS["Flush"], values
        if is_straight:
            return Evaluator.HAND_RANKS["Straight"], values
        if 3 in value_counts.values():
            return Evaluator.HAND_RANKS["Three of a Kind"], [sorted_counts[0][0]] + [c[0] for c in sorted_counts[1:]]
        if list(value_counts.values()).count(2) == 2:
            return Evaluator.HAND_RANKS["Two Pair"], [sorted_counts[0][0], sorted_counts[1][0], sorted_counts[2][0]]
        if 2 in value_counts.values():
            return Evaluator.HAND_RANKS["One Pair"], [sorted_counts[0][0]] + [c[0] for c in sorted_counts[1:]]

        return Evaluator.HAND_RANKS["High Card"], values

    @staticmethod
    def determine_winner(players, community_cards):
        best_hand = (-1, [])
        winner = None
        for player in players:
            if not player.folded:
                hand_strength, tiebreaker = Evaluator.evaluate_hand(player, community_cards)
                if (hand_strength > best_hand[0]) or (hand_strength == best_hand[0] and tiebreaker > best_hand[1]):
                    best_hand = (hand_strength, tiebreaker)
                    winner = player
        return winner