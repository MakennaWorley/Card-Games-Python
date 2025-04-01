from itertools import combinations
from collections import Counter

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
        rank_index = card.value
        if rank_index == 0:
            return 14
        else:
            return rank_index + 1

    # FOUR OF A KIND
    @staticmethod
    def is_four_of_a_kind(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        return any(count >= 4 for count in counts.values())

    @staticmethod
    def get_four_of_a_kind_info(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        four_rank = max(rank for rank, count in counts.items() if count >= 4)
        kicker_candidates = [r for r, cnt in counts.items() if r != four_rank]
        kicker = max(kicker_candidates) if kicker_candidates else 0
        return (four_rank, kicker)

    # FULL HOUSE
    @staticmethod
    def is_full_house(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        has_three = any(count >= 3 for count in counts.values())
        pairs = [rank for rank, cnt in counts.items() if cnt >= 2]
        return has_three and len(pairs) >= 2

    @staticmethod
    def get_full_house_info(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        three_rank = max(r for r, cnt in counts.items() if cnt >= 3)
        pair_candidates = [r for r, cnt in counts.items() if r != three_rank and cnt >= 2]
        pair_rank = max(pair_candidates) if pair_candidates else 0
        return (three_rank, pair_rank)

    # FLUSH
    @staticmethod
    def is_flush(cards):
        suits = [c.suit for c in cards]
        return len(set(suits)) == 1

    @staticmethod
    def get_flush_cards(cards):
        return sorted(cards, key=lambda c: Evaluator.card_value(c), reverse=True)

    # STRAIGHT
    @staticmethod
    def is_straight(cards):
        values = sorted({Evaluator.card_value(c) for c in cards})
        if len(values) < 5:
            return False
        for i in range(len(values) - 4):
            if values[i + 4] - values[i] == 4:
                return True
        if {14, 2, 3, 4, 5}.issubset(values):
            return True
        return False

    @staticmethod
    def get_highest_straight_card(cards):
        values = sorted({Evaluator.card_value(c) for c in cards})
        for i in range(len(values) - 4):
            if values[i + 4] - values[i] == 4:
                return values[i+4]
        if {14, 2, 3, 4, 5}.issubset(values):
            return 5  # In Ace-low straight, highest card is 5 (index 3)
        return None

    # THREE OF A KIND (excluding full house)
    @staticmethod
    def is_three_of_a_kind(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        has_three = any(count == 3 for count in counts.values())
        if not has_three:
            return False
        return not Evaluator.is_full_house(cards)

    @staticmethod
    def get_three_of_a_kind_info(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        three_rank = max(r for r, cnt in counts.items() if cnt == 3)
        kickers = sorted((r for r, cnt in counts.items() if r != three_rank), reverse=True)
        return (three_rank, kickers)

    # TWO PAIR
    @staticmethod
    def is_two_pair(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        pairs = [r for r, cnt in counts.items() if cnt == 2]
        return len(pairs) == 2

    @staticmethod
    def get_two_pair_info(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        pairs = sorted([r for r, cnt in counts.items() if cnt == 2], reverse=True)
        kicker = max(r for r, cnt in counts.items() if cnt == 1)
        return (pairs[0], pairs[1], kicker)

    # ONE PAIR (excluding higher multiplicities)
    @staticmethod
    def is_one_pair(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        pairs = [cnt for cnt in counts.values() if cnt == 2]
        return len(pairs) == 1 and max(counts.values()) == 2

    @staticmethod
    def get_one_pair_info(cards):
        vals = [Evaluator.card_value(c) for c in cards]
        counts = Counter(vals)
        pair_rank = max(r for r, cnt in counts.items() if cnt == 2)
        kickers = sorted([r for r, cnt in counts.items() if cnt == 1], reverse=True)
        return (pair_rank, kickers)

    @staticmethod
    def evaluate_hand(player, community_cards):
        all_cards = player.hand + community_cards
        best = (-1, ())
        for combo in combinations(all_cards, 5):
            rank_info = Evaluator.get_hand_rank(combo)
            if rank_info > best:
                best = rank_info
        return best

    @staticmethod
    def get_hand_rank(cards):
        values = sorted([Evaluator.card_value(c) for c in cards], reverse=True)

        # Check for flush and straight conditions.
        flush = Evaluator.is_flush(cards)
        straight = Evaluator.is_straight(cards)
        straight_high = Evaluator.get_highest_straight_card(cards)

        # Check for Royal Flush (Ace-high flush with the specific values).
        if flush and straight and straight_high == 14:
            return (Evaluator.HAND_RANKS["Royal Flush"], tuple(values))
        # Straight Flush.
        if flush and straight:
            return (Evaluator.HAND_RANKS["Straight Flush"], (straight_high,))
        # Four of a Kind.
        if Evaluator.is_four_of_a_kind(cards):
            four_rank, kicker = Evaluator.get_four_of_a_kind_info(cards)
            return (Evaluator.HAND_RANKS["Four of a Kind"], (four_rank, kicker))
        # Full House.
        if Evaluator.is_full_house(cards):
            trip_rank, pair_rank = Evaluator.get_full_house_info(cards)
            return (Evaluator.HAND_RANKS["Full House"], (trip_rank, pair_rank))
        # Flush.
        if flush:
            flush_cards_sorted = Evaluator.get_flush_cards(cards)
            ranks_desc = sorted(
                [Evaluator.card_value(c) for c in flush_cards_sorted],
                reverse=True
            )
            return Evaluator.HAND_RANKS["Flush"], tuple(ranks_desc)
        # Straight.
        if straight:
            return (Evaluator.HAND_RANKS["Straight"], (straight_high,))
        # Three of a Kind.
        if Evaluator.is_three_of_a_kind(cards):
            trip_rank, kicker_list = Evaluator.get_three_of_a_kind_info(cards)
            return (Evaluator.HAND_RANKS["Three of a Kind"],
                    (trip_rank,) + tuple(kicker_list))
        # Two Pair.
        if Evaluator.is_two_pair(cards):
            high_pair, low_pair, kicker = Evaluator.get_two_pair_info(cards)
            return (Evaluator.HAND_RANKS["Two Pair"], (high_pair, low_pair, kicker))
        # One Pair.
        if Evaluator.is_one_pair(cards):
            pair_rank, kicker_list = Evaluator.get_one_pair_info(cards)
            return (Evaluator.HAND_RANKS["One Pair"],
                    (pair_rank,) + tuple(kicker_list))
        # High Card.
        return (Evaluator.HAND_RANKS["High Card"], tuple(values))

class EvaluatorTable(Evaluator):
    @staticmethod
    def determine_winner(players, community_cards):
        player_ranks = {}
        for p in players:
            if not getattr(p, "folded", False):
                player_ranks[p] = EvaluatorTable.evaluate_hand(p, community_cards)
        sorted_by_best = sorted(player_ranks.items(), key=lambda x: x[1], reverse=True)
        if not sorted_by_best:
            return []
        top_score = sorted_by_best[0][1]
        winners = [sorted_by_best[0][0]]
        for i in range(1, len(sorted_by_best)):
            if sorted_by_best[i][1] == top_score:
                winners.append(sorted_by_best[i][0])
            else:
                break
        return winners
