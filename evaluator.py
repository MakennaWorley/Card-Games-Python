from itertools import combinations
from collections import Counter
from card_enums import *

class Evaluator:
    HAND_RANKS = {
        "Royal Flush": 9,
        "Straight Flush": 8,
        "Four of a Kind": 7,
        "Full House": 6,
        "Flush": 5,
        "Straight": 4,
        "Three of a Kind": 3,
        "Two Pair": 2,
        "One Pair": 1,
        "High Card": 0
    }

    @staticmethod
    def card_value(card):
        # Define the correct ranking order: TWO is lowest, ACE is highest.
        order = [
            VALUE.TWO, VALUE.THREE, VALUE.FOUR, VALUE.FIVE, VALUE.SIX,
            VALUE.SEVEN, VALUE.EIGHT, VALUE.NINE, VALUE.TEN, VALUE.JACK,
            VALUE.QUEEN, VALUE.KING, VALUE.ACE
        ]
        # Return the index so that TWO=0, ACE=12.
        return order.index(card.value)

    # FOUR OF A KIND
    @staticmethod
    def is_four_of_a_kind(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        # Accept any group of 4 or more as four-of-a-kind.
        return any(count >= 4 for count in counts.values())

    @staticmethod
    def get_four_of_a_kind_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        # Get the rank that appears at least 4 times.
        four_rank = max(rank for rank, count in counts.items() if count >= 4)
        # Find the highest kicker that is not part of the four-of-a-kind.
        kicker_candidates = [rank for rank, count in counts.items() if rank != four_rank]
        kicker = max(kicker_candidates) if kicker_candidates else 0  # Default to lowest if none found
        return (four_rank, kicker)

    # FULL HOUSE
    @staticmethod
    def is_full_house(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        # Full house: one rank appears at least 3 times and another (can be the same if 4 or 5 of a kind) appears at least 2 times.
        has_three = any(count >= 3 for count in counts.values())
        # For the pair part, we want a rank different from the triple.
        pairs = [rank for rank, count in counts.items() if count >= 2]
        return has_three and len(pairs) >= 2

    @staticmethod
    def get_full_house_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        # Choose the highest rank with count>=3 as the triplet.
        trip_rank = max(rank for rank, count in counts.items() if count >= 3)
        # For the pair, choose the highest rank (other than trip_rank) with count>=2.
        pair_candidates = [rank for rank, count in counts.items() if rank != trip_rank and count >= 2]
        pair_rank = max(pair_candidates) if pair_candidates else 0
        return (trip_rank, pair_rank)

    # FLUSH
    @staticmethod
    def is_flush(cards):
        suits = [c.suit for c in cards]
        return len(set(suits)) == 1

    @staticmethod
    def get_flush_cards(cards):
        # Returns the cards sorted descending by their value.
        return sorted(cards, key=Evaluator.card_value, reverse=True)

    # STRAIGHT
    @staticmethod
    def is_straight(cards):
        # Get unique card values sorted in descending order.
        values = sorted(set(Evaluator.card_value(c) for c in cards), reverse=True)
        if len(values) < 5:
            return False
        for i in range(len(values) - 4):
            if values[i] - values[i + 4] == 4:
                return True
        # Ace-low straight: Ace, 2, 3, 4, 5 (Assumes ACE index is highest, TWO is index 0)
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
            return 3  # In Ace-low straight, highest card is 5 (index 3)
        return None

    # THREE OF A KIND (excluding full house)
    @staticmethod
    def is_three_of_a_kind(cards):
        counts = Counter(Evaluator.card_value(c) for c in cards)
        # We want exactly one triplet in a 5-card combination (which wouldn't form a full house)
        return any(count == 3 for count in counts.values())

    @staticmethod
    def get_three_of_a_kind_info(cards):
        values = [Evaluator.card_value(c) for c in cards]
        counts = Counter(values)
        trip_rank = max(rank for rank, count in counts.items() if count == 3)
        kickers = sorted((rank for rank, count in counts.items() if count == 1), reverse=True)
        return (trip_rank, kickers)

    # TWO PAIR
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

    # ONE PAIR (excluding higher multiplicities)
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
        best_hand = (-1, ())  # (rank, tiebreakers)
        for combo in combinations(all_cards, 5):
            rank, tiebreaker = Evaluator.get_hand_rank(combo)
            if (rank, tiebreaker) > best_hand:
                best_hand = (rank, tiebreaker)
        return best_hand

    @staticmethod
    def get_hand_rank(cards):
        # Convert card values to indices.
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
        best_primary = -1
        best_kicker = None
        winner = None
        for player in players:
            if not player.folded:
                primary, kicker = Evaluator.evaluate_hand(player, community_cards)
                if primary > best_primary:
                    best_primary = primary
                    best_kicker = kicker
                    winner = player
                elif primary == best_primary:
                    # Only use the kicker to decide if the primary ranks are equal.
                    if kicker > best_kicker:
                        best_kicker = kicker
                        winner = player
        return winner
