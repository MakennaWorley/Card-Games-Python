from itertools import combinations
from collections import Counter
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
    def card_value(card):
        return list(VALUE).index(card.value)

    @staticmethod
    def is_four_of_a_kind(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        return 4 in counts.values()

    @staticmethod
    def get_four_of_a_kind_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        four_rank = max(rank for rank, count in counts.items() if count == 4)
        kicker = max(rank for rank, count in counts.items() if rank != four_rank)
        return (four_rank, kicker)

    @staticmethod
    def is_full_house(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        return sorted(counts.values()) == [2, 3]

    @staticmethod
    def get_full_house_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        trip_rank = max(rank for rank, count in counts.items() if count >= 3)
        pair_rank = max(rank for rank, count in counts.items() if rank != trip_rank and count >= 2)
        return (trip_rank, pair_rank)

    @staticmethod
    def is_flush(cards):
        suits = [c.suit for c in cards]
        return len(set(suits)) == 1

    @staticmethod
    def get_flush_cards(cards):
        return sorted(cards, key=Evaluator.card_value, reverse=True)

    @staticmethod
    def is_straight(cards):
        values = sorted(set(Evaluator.card_value(c) for c in cards), reverse=True)
        if len(values) < 5:
            return False
        for i in range(len(values) - 4):
            if values[i] - values[i + 4] == 4:
                return True
        if 12 in values and all(x in values for x in [0, 1, 2, 3]):
            return True
        return False

    @staticmethod
    def get_highest_straight_card(cards):
        values = sorted(set(Evaluator.card_value(c) for c in cards), reverse=True)
        for i in range(len(values) - 4):
            if values[i] - values[i + 4] == 4:
                return values[i]
        if 12 in values and all(x in values for x in [0, 1, 2, 3]):
            return 3
        return None

    @staticmethod
    def is_three_of_a_kind(cards):
        counts = Counter(Evaluator.card_value(c) for c in cards)
        return sorted(counts.values()) == [1, 1, 3]

    @staticmethod
    def get_three_of_a_kind_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        trip_rank = max(rank for rank, count in counts.items() if count == 3)
        kickers = sorted((rank for rank, count in counts.items() if count == 1), reverse=True)
        return (trip_rank, kickers)

    @staticmethod
    def is_two_pair(cards):
        counts = Counter(Evaluator.card_value(c) for c in cards)
        pairs = [rank for rank, count in counts.items() if count == 2]
        return len(pairs) == 2

    @staticmethod
    def get_two_pair_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        pairs = sorted([rank for rank, count in counts.items() if count == 2], reverse=True)
        kicker = max(rank for rank, count in counts.items() if count == 1)
        return (pairs[0], pairs[1], kicker)

    @staticmethod
    def is_one_pair(cards):
        counts = Counter(Evaluator.card_value(c) for c in cards)
        pairs = [rank for rank, count in counts.items() if count == 2]
        return len(pairs) == 1 and max(counts.values()) == 2

    @staticmethod
    def get_one_pair_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        pair_rank = max(rank for rank, count in counts.items() if count == 2)
        kickers = sorted([rank for rank, count in counts.items() if count == 1], reverse=True)
        return (pair_rank, kickers)

    @staticmethod
    def evaluate_hand(player, community_cards):
        all_cards = player.hand + community_cards
        best_hand = (-1, ())
        for combo in combinations(all_cards, 5):
            rank, tiebreaker = Evaluator.get_hand_rank(combo)
            if (rank, tiebreaker) > best_hand:
                best_hand = (rank, tiebreaker)
        return best_hand

    @staticmethod
    def get_hand_rank(cards):
        values = sorted([list(VALUE).index(card.value) for card in cards], reverse=True)
        suits = [card.suit for card in cards]

        is_flush = len(set(suits)) == 1
        is_straight = all(values[i] - 1 == values[i + 1] for i in range(4))

        is_royal = is_flush and values == [12, 11, 10, 9, 0]

        if is_royal:
            return (Evaluator.HAND_RANKS["Royal Flush"], tuple(values))
        elif is_flush and is_straight:
            return (Evaluator.HAND_RANKS["Straight Flush"], (Evaluator.get_highest_straight_card(cards),))
        elif Evaluator.is_four_of_a_kind(cards):
            four_rank, kicker = Evaluator.get_four_of_a_kind_info(cards)
            return (Evaluator.HAND_RANKS["Four of a Kind"], (four_rank, kicker))
        elif Evaluator.is_full_house(cards):
            trip_rank, pair_rank = Evaluator.get_full_house_info(cards)
            return (Evaluator.HAND_RANKS["Full House"], (trip_rank, pair_rank))
        elif Evaluator.is_flush(cards):
            flush_cards = Evaluator.get_flush_cards(cards)
            return (Evaluator.HAND_RANKS["Flush"], tuple(sorted([Evaluator.card_value(c) for c in flush_cards], reverse=True)))
        elif Evaluator.is_straight(cards):
            return (Evaluator.HAND_RANKS["Straight"], (Evaluator.get_highest_straight_card(cards),))
        elif Evaluator.is_three_of_a_kind(cards):
            trip_rank, kickers = Evaluator.get_three_of_a_kind_info(cards)
            return (Evaluator.HAND_RANKS["Three of a Kind"], (trip_rank,) + tuple(sorted(kickers, reverse=True)))
        elif Evaluator.is_two_pair(cards):
            high_pair, low_pair, kicker = Evaluator.get_two_pair_info(cards)
            return (Evaluator.HAND_RANKS["Two Pair"], (high_pair, low_pair, kicker))
        elif Evaluator.is_one_pair(cards):
            pair_rank, kickers = Evaluator.get_one_pair_info(cards)
            return (Evaluator.HAND_RANKS["One Pair"], (pair_rank,) + tuple(sorted(kickers, reverse=True)))
        else:
            high_cards = sorted([Evaluator.card_value(c) for c in cards], reverse=True)[:5]
            return (Evaluator.HAND_RANKS["High Card"], tuple(high_cards))

    @staticmethod
    def determine_winner(players, community_cards):
        best_hand = (-1, ())
        winner = None
        for player in players:
            if not player.folded:
                hand = Evaluator.evaluate_hand(player, community_cards)
                if hand > best_hand:
                    best_hand = hand
                    winner = player
        return winner
