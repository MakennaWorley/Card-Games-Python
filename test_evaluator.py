import unittest
from card_enums import *
from evaluator import *

class TestEvaluator(unittest.TestCase):
    class MockCard:
        """Mock class to simulate a card object using RANK and SUIT enums."""
        def __init__(self, rank, suit):
            self.rank = RANK[rank]
            self.value = self.rank.value
            self.suit = SUIT[suit]

        def __repr__(self):
            return f"{self.rank.name} of {self.suit.name}"

    class MockPlayer:
        """Mock class to simulate a player object with a hand and folded status."""
        def __init__(self, hand, folded=False):
            self.hand = hand
            self.folded = folded

        def __repr__(self):
            return f"Player({self.hand}, folded={self.folded})"

    def create_cards(self, values, suits):
        """Helper function to create a list of MockCard objects using enums."""
        return [self.MockCard(value, suit) for value, suit in zip(values, suits)]

    def test_hand_rankings(self):
        """Test that each hand is assigned the correct ranking value."""
        test_cases = [
            # (Hand Type, Player Hand Values, Player Hand Suits, Community Cards Values, Community Cards Suits)
            ("Royal Flush", ["ACE", "KING"], ["HEARTS", "HEARTS"],
             ["QUEEN", "JACK", "TEN", "FIVE", "TWO"],
             ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"]),
            ("Straight Flush", ["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"],
             ["SEVEN", "SIX", "FIVE", "TWO", "THREE"],
             ["DIAMONDS", "DIAMONDS", "DIAMONDS", "SPADES", "HEARTS"]),
            ("Four of a Kind", ["QUEEN", "QUEEN"], ["CLUBS", "DIAMONDS"],
             ["QUEEN", "QUEEN", "NINE", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Full House", ["KING", "KING"], ["HEARTS", "DIAMONDS"],
             ["KING", "NINE", "NINE", "FOUR", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Flush", ["JACK", "FIVE"], ["CLUBS", "CLUBS"],
             ["NINE", "SIX", "THREE", "KING", "TWO"],
             ["CLUBS", "CLUBS", "CLUBS", "CLUBS", "DIAMONDS"]),
            ("Straight", ["JACK", "TEN"], ["HEARTS", "DIAMONDS"],
             ["NINE", "EIGHT", "SEVEN", "FIVE", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Three of a Kind", ["SEVEN", "SEVEN"], ["CLUBS", "DIAMONDS"],
             ["SEVEN", "KING", "JACK", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Two Pair", ["FOUR", "FOUR"], ["HEARTS", "DIAMONDS"],
             ["NINE", "NINE", "FIVE", "THREE", "TWO"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("One Pair", ["ACE", "ACE"], ["SPADES", "DIAMONDS"],
             ["EIGHT", "SIX", "FIVE", "THREE", "TWO"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
            ("High Card", ["ACE", "JACK"], ["SPADES", "DIAMONDS"],
             ["NINE", "SIX", "FIVE", "FOUR", "THREE"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
        ]

        for hand_name, player_values, player_suits, comm_values, comm_suits in test_cases:
            with self.subTest(hand=hand_name):
                player = self.MockPlayer(self.create_cards(player_values, player_suits))
                community_cards = self.create_cards(comm_values, comm_suits)
                rank, _ = Evaluator.evaluate_hand(player, community_cards)
                expected_rank = Evaluator.HAND_RANKS[hand_name]
                self.assertEqual(rank, expected_rank,
                                 f"Expected {hand_name} to have rank {expected_rank} but got {rank}")

    def test_rankings(self):
        """Test head-to-head comparisons with various edge cases for tie-breakers."""
        test_cases = [
            ("Royal Flush", ["ACE", "KING"], ["HEARTS", "HEARTS"],
             ["QUEEN", "JACK", "TEN", "FIVE", "TWO"],
             ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"]),
            ("Straight Flush", ["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"],
             ["SEVEN", "SIX", "FIVE", "TWO", "THREE"],
             ["DIAMONDS", "DIAMONDS", "DIAMONDS", "SPADES", "HEARTS"]),
            ("Four of a Kind", ["QUEEN", "QUEEN"], ["CLUBS", "DIAMONDS"],
             ["QUEEN", "QUEEN", "NINE", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Full House", ["KING", "KING"], ["HEARTS", "DIAMONDS"],
             ["KING", "NINE", "NINE", "FOUR", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Flush", ["JACK", "FIVE"], ["CLUBS", "CLUBS"],
             ["NINE", "SIX", "THREE", "KING", "TWO"],
             ["CLUBS", "CLUBS", "CLUBS", "CLUBS", "DIAMONDS"]),
            ("Straight", ["JACK", "TEN"], ["HEARTS", "DIAMONDS"],
             ["NINE", "EIGHT", "SEVEN", "FIVE", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Three of a Kind", ["SEVEN", "SEVEN"], ["CLUBS", "DIAMONDS"],
             ["SEVEN", "KING", "JACK", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Two Pair", ["FOUR", "FOUR"], ["HEARTS", "DIAMONDS"],
             ["NINE", "NINE", "FIVE", "THREE", "TWO"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("One Pair", ["ACE", "ACE"], ["SPADES", "DIAMONDS"],
             ["EIGHT", "SIX", "FIVE", "THREE", "TWO"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
            ("High Card", ["ACE", "JACK"], ["SPADES", "DIAMONDS"],
             ["NINE", "SIX", "FIVE", "FOUR", "THREE"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
        ]

        # For each test case, ensure that a higher-ranked hand wins head-to-head.
        for i, (name1, p1_values, p1_suits, comm_values, comm_suits) in enumerate(test_cases):
            player1 = self.MockPlayer(self.create_cards(p1_values, p1_suits))
            community_cards = self.create_cards(comm_values, comm_suits)
            for name2, p2_values, p2_suits, _, _ in test_cases[i + 1:]:
                player2 = self.MockPlayer(self.create_cards(p2_values, p2_suits))
                with self.subTest(hand1=name1, hand2=name2):
                    winner = Evaluator.determine_winner([player1, player2], community_cards)
                    self.assertEqual(winner, [player1],
                                     f"{name1} should beat {name2}")

        # Additional edge cases for tie-breakers:

        # Board Dominance: Board nearly forms a flush.
        board = self.create_cards(["ACE", "KING", "FOUR", "FIVE", "SIX"],
                                  ["CLUBS", "CLUBS", "CLUBS", "DIAMONDS", "HEARTS"])
        player1 = self.MockPlayer(self.create_cards(["TWO", "THREE"], ["CLUBS", "CLUBS"]))  # Completes flush
        player2 = self.MockPlayer(self.create_cards(["FOUR", "FIVE"], ["CLUBS", "DIAMONDS"]))  # Does not complete flush
        winner = Evaluator.determine_winner([player1, player2], board)
        self.assertEqual(winner, [player1], "Board Dominance: player1 wins with flush kicker")

        # Minimal Improvement: Same board gives a pair; one player's hole cards improve it to two pair.
        board = self.create_cards(["ACE", "ACE", "KING", "QUEEN", "JACK"],
                                  ["DIAMONDS", "DIAMONDS", "SPADES", "CLUBS", "HEARTS"])
        player1 = self.MockPlayer(self.create_cards(["ACE", "FOUR"], ["SPADES", "HEARTS"]))  # Upgrades pair to two pair
        player2 = self.MockPlayer(self.create_cards(["KING", "QUEEN"], ["CLUBS", "SPADES"]))  # Remains with one pair
        winner = Evaluator.determine_winner([player1, player2], board)
        self.assertEqual(winner, [player1], "Minimal Improvement: player1 wins with upgraded two pair")

        # Kicker Dispute: Both players have the same primary pair; the kicker decides.
        board = self.create_cards(["ACE", "KING", "QUEEN", "JACK", "NINE"],
                                  ["CLUBS", "SPADES", "DIAMONDS", "CLUBS", "HEARTS"])
        player1 = self.MockPlayer(self.create_cards(["ACE", "TEN"], ["HEARTS", "DIAMONDS"]))  # Kicker 10
        player2 = self.MockPlayer(self.create_cards(["ACE", "EIGHT"], ["CLUBS", "SPADES"]))  # Kicker 8
        winner = Evaluator.determine_winner([player1, player2], board)
        self.assertEqual(winner, [player1], "Kicker Dispute: player1 wins with higher kicker")

        # Full House Tie: Two players with full houses, but one has a higher triplet.
        board = self.create_cards(["KING", "KING", "QUEEN", "JACK", "TEN"],
                                  ["DIAMONDS", "HEARTS", "CLUBS", "SPADES", "DIAMONDS"])
        player1 = self.MockPlayer(
            self.create_cards(["KING", "TWO"], ["CLUBS", "HEARTS"]))  # Full house with triple Kings
        player2 = self.MockPlayer(self.create_cards(["QUEEN", "THREE"], ["SPADES",
                                                                         "DIAMONDS"]))  # Full house with triple Kings but lower pair
        winner = Evaluator.determine_winner([player1, player2], board)
        self.assertEqual(winner, [player1], "Full House Tie: player1 wins with better kickers")

    def test_ties_all_hand_types(self):
        test_cases = [
            # Straight Flush (Note: no royal flush)
            ("Straight Flush",
             ["KING", "QUEEN"], ["HEARTS", "HEARTS"],
             ["JACK", "TEN", "NINE", "EIGHT", "SEVEN"],
             ["HEARTS", "HEARTS", "HEARTS", "HEARTS", "HEARTS"]),
            ("Straight Flush",
             ["QUEEN", "JACK"], ["DIAMONDS", "DIAMONDS"],
             ["TEN", "NINE", "EIGHT", "SEVEN", "SIX"],
             ["DIAMONDS", "DIAMONDS", "DIAMONDS", "DIAMONDS", "DIAMONDS"]),
            ("Straight Flush",
             ["JACK", "TEN"], ["CLUBS", "CLUBS"],
             ["NINE", "EIGHT", "SEVEN", "SIX", "FIVE"],
             ["CLUBS", "CLUBS", "CLUBS", "CLUBS", "CLUBS"]),

            # Four of a Kind
            ("Four of a Kind",
             ["ACE", "ACE"], ["HEARTS", "DIAMONDS"],
             ["ACE", "ACE", "ACE", "KING", "QUEEN"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Four of a Kind",
             ["KING", "KING"], ["CLUBS", "DIAMONDS"],
             ["KING", "KING", "KING", "QUEEN", "JACK"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Four of a Kind",
             ["QUEEN", "QUEEN"], ["SPADES", "CLUBS"],
             ["QUEEN", "QUEEN", "QUEEN", "JACK", "TEN"],
             ["DIAMONDS", "HEARTS", "SPADES", "CLUBS", "DIAMONDS"]),

            # Full House
            ("Full House",
             ["KING", "KING"], ["HEARTS", "CLUBS"],
             ["KING", "KING", "QUEEN", "QUEEN", "JACK"],
             ["SPADES", "DIAMONDS", "HEARTS", "DIAMONDS", "CLUBS"]),
            ("Full House",
             ["QUEEN", "QUEEN"], ["DIAMONDS", "HEARTS"],
             ["QUEEN", "QUEEN", "JACK", "JACK", "TEN"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Full House",
             ["JACK", "JACK"], ["SPADES", "DIAMONDS"],
             ["JACK", "JACK", "TEN", "TEN", "NINE"],
             ["HEARTS", "CLUBS", "DIAMONDS", "HEARTS", "CLUBS"]),

            # Flush (ensure non-sequential to avoid straight flush)
            ("Flush",
             ["ACE", "QUEEN"], ["SPADES", "SPADES"],
             ["JACK", "NINE", "EIGHT", "FIVE", "TWO"],
             ["SPADES", "SPADES", "SPADES", "SPADES", "SPADES"]),
            ("Flush",
             ["KING", "JACK"], ["HEARTS", "HEARTS"],
             ["TEN", "EIGHT", "SEVEN", "FOUR", "TWO"],
             ["HEARTS", "HEARTS", "HEARTS", "HEARTS", "HEARTS"]),
            ("Flush",
             ["QUEEN", "TEN"], ["CLUBS", "CLUBS"],
             ["NINE", "EIGHT", "SIX", "THREE", "TWO"],
             ["CLUBS", "CLUBS", "CLUBS", "CLUBS", "CLUBS"]),

            # Straight (non-flush)
            ("Straight",
             ["KING", "QUEEN"], ["HEARTS", "DIAMONDS"],
             ["JACK", "TEN", "NINE", "TWO", "THREE"],
             ["SPADES", "SPADES", "HEARTS", "DIAMONDS", "CLUBS"]),
            ("Straight",
             ["QUEEN", "JACK"], ["CLUBS", "DIAMONDS"],
             ["TEN", "NINE", "EIGHT", "FOUR", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "HEARTS"]),
            # Edge case: the "wheel" A-2-3-4-5 straight
            ("Straight",
             ["ACE", "TWO"], ["HEARTS", "DIAMONDS"],
             ["THREE", "FOUR", "FIVE", "NINE", "KING"],
             ["SPADES", "CLUBS", "DIAMONDS", "HEARTS", "SPADES"]),

            # Three of a Kind
            ("Three of a Kind",
             ["ACE", "ACE"], ["DIAMONDS", "HEARTS"],
             ["ACE", "KING", "QUEEN", "TEN", "NINE"],
             ["CLUBS", "SPADES", "DIAMONDS", "HEARTS", "CLUBS"]),
            ("Three of a Kind",
             ["KING", "KING"], ["CLUBS", "DIAMONDS"],
             ["KING", "QUEEN", "JACK", "TEN", "EIGHT"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Three of a Kind",
             ["QUEEN", "QUEEN"], ["SPADES", "CLUBS"],
             ["QUEEN", "JACK", "TEN", "NINE", "EIGHT"],
             ["DIAMONDS", "HEARTS", "SPADES", "CLUBS", "DIAMONDS"]),

            # Two Pair
            ("Two Pair",
             ["ACE", "KING"], ["HEARTS", "DIAMONDS"],
             ["ACE", "KING", "QUEEN", "JACK", "TEN"],
             ["CLUBS", "SPADES", "DIAMONDS", "HEARTS", "CLUBS"]),
            ("Two Pair",
             ["QUEEN", "JACK"], ["CLUBS", "SPADES"],
             ["QUEEN", "JACK", "TEN", "NINE", "EIGHT"],
             ["HEARTS", "DIAMONDS", "CLUBS", "SPADES", "HEARTS"]),
            ("Two Pair",
             ["TEN", "NINE"], ["DIAMONDS", "HEARTS"],
             ["TEN", "NINE", "EIGHT", "SEVEN", "SIX"],
             ["CLUBS", "SPADES", "DIAMONDS", "HEARTS", "CLUBS"]),

            # One Pair
            ("One Pair",
             ["ACE", "ACE"], ["SPADES", "HEARTS"],
             ["KING", "QUEEN", "JACK", "TEN", "NINE"],
             ["DIAMONDS", "CLUBS", "HEARTS", "SPADES", "DIAMONDS"]),
            ("One Pair",
             ["KING", "KING"], ["CLUBS", "DIAMONDS"],
             ["QUEEN", "JACK", "TEN", "NINE", "EIGHT"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("One Pair",
             ["QUEEN", "QUEEN"], ["DIAMONDS", "CLUBS"],
             ["JACK", "TEN", "NINE", "EIGHT", "SEVEN"],
             ["SPADES", "HEARTS", "DIAMONDS", "CLUBS", "SPADES"]),

            # High Card
            ("High Card",
             ["ACE", "KING"], ["HEARTS", "DIAMONDS"],
             ["QUEEN", "JACK", "NINE", "FOUR", "TWO"],
             ["CLUBS", "SPADES", "DIAMONDS", "HEARTS", "CLUBS"]),
            ("High Card",
             ["QUEEN", "JACK"], ["CLUBS", "SPADES"],
             ["TEN", "EIGHT", "SEVEN", "THREE", "TWO"],
             ["DIAMONDS", "HEARTS", "SPADES", "CLUBS", "DIAMONDS"]),
            # Edge case: lowest possible high card (using low-value cards, ensuring no pair, flush, or straight)
            ("High Card",
             ["TWO", "THREE"], ["CLUBS", "DIAMONDS"],
             ["FOUR", "FIVE", "SEVEN", "NINE", "JACK"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "HEARTS"]),
        ]

        for i, (hand_type, p1_values, p1_suits, comm_values, comm_suits) in enumerate(test_cases):
            player1 = self.MockPlayer(self.create_cards(p1_values, p1_suits))
            community_cards = self.create_cards(comm_values, comm_suits)
            for hand_type2, p2_values, p2_suits, _, _ in test_cases[i + 1:]:
                player2 = self.MockPlayer(self.create_cards(p2_values, p2_suits))
                with self.subTest(hand1=hand_type, hand2=hand_type2):
                    winner = Evaluator.determine_winner([player1, player2], community_cards)
                    self.assertEqual(winner, [player1], f"{hand_type} should beat {hand_type2}")

    def test_determine_winner(self):
        """Test if the correct winner is determined among multiple players."""
        # Player1: Royal Flush, Player2: Straight Flush, Player3: Four of a Kind
        player1 = self.MockPlayer(self.create_cards(["ACE", "KING"], ["HEARTS", "HEARTS"]))  # Royal Flush
        player2 = self.MockPlayer(self.create_cards(["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"]))  # Straight Flush
        player3 = self.MockPlayer(self.create_cards(["QUEEN", "QUEEN"], ["CLUBS", "DIAMONDS"]))  # Four of a Kind

        community_cards = self.create_cards(
            ["QUEEN", "JACK", "TEN", "FIVE", "TWO"],
            ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"]
        )

        winner = Evaluator.determine_winner([player1, player2, player3], community_cards)
        self.assertEqual(winner, [player1], "Player with Royal Flush should win")

    def test_folded_player_ignored(self):
        """Test that folded players are ignored when determining the winner."""
        player1 = self.MockPlayer(self.create_cards(["ACE", "KING"], ["HEARTS", "HEARTS"]),
                                  folded=True)  # Folded Royal Flush
        player2 = self.MockPlayer(self.create_cards(["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"]))  # Straight Flush

        community_cards = self.create_cards(
            ["QUEEN", "JACK", "TEN", "FIVE", "TWO"],
            ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"]
        )

        winner = Evaluator.determine_winner([player1, player2], community_cards)
        self.assertEqual(winner, [player2], "Folded player should be ignored; player2 wins")

if __name__ == "__main__":
    unittest.main()
