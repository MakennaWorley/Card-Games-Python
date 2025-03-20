import unittest
from unittest.mock import MagicMock
from card_enums import VALUE, SUIT  # Use enums from the provided file
from evaluator import Evaluator  # Import Evaluator

class TestEvaluator(unittest.TestCase):

    class MockCard:
        """Mock class to simulate a card object with VALUE and SUIT enums."""
        def __init__(self, value, suit):
            self.value = VALUE[value]  # No need to uppercase; match `VALUE` exactly
            self.suit = SUIT[suit]  # Match `SUIT` exactly

    class MockPlayer:
        """Mock class to simulate a player object with a hand and folded status."""
        def __init__(self, hand, folded=False):
            self.hand = hand
            self.folded = folded

    def create_cards(self, values, suits):
        """Helper function to create a list of MockCard objects using enums."""
        return [self.MockCard(value, suit) for value, suit in zip(values, suits)]

    def test_hand_rankings(self):
        test_cases = [
            # (Hand Type, Player Hand, Suits, Community Cards, Suits)
            ("Royal Flush", ["ACE", "KING"], ["HEARTS", "HEARTS"], ["QUEEN", "JACK", "TEN", "FIVE", "TWO"],
             ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"]),
            ("Straight Flush", ["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"], ["SEVEN", "SIX", "FIVE", "TWO", "THREE"],
             ["DIAMONDS", "DIAMONDS", "DIAMONDS", "SPADES", "HEARTS"]),
            ("Four of a Kind", ["QUEEN", "QUEEN"], ["CLUBS", "DIAMONDS"], ["QUEEN", "QUEEN", "NINE", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Full House", ["KING", "KING"], ["HEARTS", "DIAMONDS"], ["KING", "NINE", "NINE", "FOUR", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Flush", ["JACK", "FIVE"], ["CLUBS", "CLUBS"], ["NINE", "SIX", "THREE", "KING", "TWO"],
             ["CLUBS", "CLUBS", "CLUBS", "CLUBS", "DIAMONDS"]),
            ("Straight", ["JACK", "TEN"], ["HEARTS", "DIAMONDS"], ["NINE", "EIGHT", "SEVEN", "FIVE", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Three of a Kind", ["SEVEN", "SEVEN"], ["CLUBS", "DIAMONDS"], ["SEVEN", "KING", "JACK", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Two Pair", ["FOUR", "FOUR"], ["HEARTS", "DIAMONDS"], ["NINE", "NINE", "FIVE", "THREE", "TWO"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("One Pair", ["ACE", "ACE"], ["SPADES", "DIAMONDS"], ["EIGHT", "SIX", "FIVE", "THREE", "TWO"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
            ("High Card", ["ACE", "JACK"], ["SPADES", "DIAMONDS"], ["NINE", "SIX", "FIVE", "FOUR", "THREE"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
        ]

        for hand_name, player_values, player_suits, comm_values, comm_suits in test_cases:
            with self.subTest(hand=hand_name):
                player = self.MockPlayer(self.create_cards(player_values, player_suits))
                community_cards = self.create_cards(comm_values, comm_suits)
                rank, _ = Evaluator.evaluate_hand(player, community_cards)
                expected_rank = Evaluator.HAND_RANKS[hand_name]
                self.assertEqual(rank, expected_rank)

    def test_rankings(self):
        test_cases = [
            ("Royal Flush", ["ACE", "KING"], ["HEARTS", "HEARTS"], ["QUEEN", "JACK", "TEN", "FIVE", "TWO"],
             ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"]),
            ("Straight Flush", ["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"], ["SEVEN", "SIX", "FIVE", "TWO", "THREE"],
             ["DIAMONDS", "DIAMONDS", "DIAMONDS", "SPADES", "HEARTS"]),
            ("Four of a Kind", ["QUEEN", "QUEEN"], ["CLUBS", "DIAMONDS"], ["QUEEN", "QUEEN", "NINE", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Full House", ["KING", "KING"], ["HEARTS", "DIAMONDS"], ["KING", "NINE", "NINE", "FOUR", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Flush", ["JACK", "FIVE"], ["CLUBS", "CLUBS"], ["NINE", "SIX", "THREE", "KING", "TWO"],
             ["CLUBS", "CLUBS", "CLUBS", "CLUBS", "DIAMONDS"]),
            ("Straight", ["JACK", "TEN"], ["HEARTS", "DIAMONDS"], ["NINE", "EIGHT", "SEVEN", "FIVE", "THREE"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("Three of a Kind", ["SEVEN", "SEVEN"], ["CLUBS", "DIAMONDS"], ["SEVEN", "KING", "JACK", "FIVE", "TWO"],
             ["HEARTS", "SPADES", "DIAMONDS", "CLUBS", "SPADES"]),
            ("Two Pair", ["FOUR", "FOUR"], ["HEARTS", "DIAMONDS"], ["NINE", "NINE", "FIVE", "THREE", "TWO"],
             ["CLUBS", "SPADES", "HEARTS", "DIAMONDS", "SPADES"]),
            ("One Pair", ["ACE", "ACE"], ["SPADES", "DIAMONDS"], ["EIGHT", "SIX", "FIVE", "THREE", "TWO"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
            ("High Card", ["ACE", "JACK"], ["SPADES", "DIAMONDS"], ["NINE", "SIX", "FIVE", "FOUR", "THREE"],
             ["CLUBS", "HEARTS", "SPADES", "DIAMONDS", "CLUBS"]),
        ]

        for i, (name1, p1_values, p1_suits, comm_values, comm_suits) in enumerate(test_cases):
            player1 = self.MockPlayer(self.create_cards(p1_values, p1_suits))
            community_cards = self.create_cards(comm_values, comm_suits)

            for name2, p2_values, p2_suits, _, _ in test_cases[i + 1:]:
                player2 = self.MockPlayer(self.create_cards(p2_values, p2_suits))

                with self.subTest(hand1=name1, hand2=name2):
                    winner = Evaluator.determine_winner([player1, player2], community_cards)
                    self.assertEqual(winner, player1, f"{name1} should beat {name2}")

    def test_determine_winner(self):
        """Test if the correct winner is determined."""
        player1 = self.MockPlayer(self.create_cards(["ACE", "KING"], ["HEARTS", "HEARTS"]))  # Royal Flush
        player2 = self.MockPlayer(self.create_cards(["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"]))  # Straight Flush
        player3 = self.MockPlayer(self.create_cards(["QUEEN", "QUEEN"], ["CLUBS", "DIAMONDS"]))  # Four of a Kind

        community_cards = self.create_cards(["QUEEN", "JACK", "TEN", "FIVE", "TWO"], ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"])

        winner = Evaluator.determine_winner([player1, player2, player3], community_cards)
        print(winner)
        self.assertEqual(winner, player1)  # Player with Royal Flush should win

    def test_folded_player_ignored(self):
        """Test that folded players are ignored when determining the winner."""
        player1 = self.MockPlayer(self.create_cards(["ACE", "KING"], ["HEARTS", "HEARTS"]), folded=True)  # Folded Royal Flush
        player2 = self.MockPlayer(self.create_cards(["NINE", "EIGHT"], ["DIAMONDS", "DIAMONDS"]))  # Straight Flush

        community_cards = self.create_cards(["QUEEN", "JACK", "TEN", "FIVE", "TWO"], ["HEARTS", "HEARTS", "HEARTS", "DIAMONDS", "CLUBS"])

        winner = Evaluator.determine_winner([player1, player2], community_cards)
        print(winner)
        self.assertEqual(winner, player2)  # Player2 wins since Player1 is folded

if __name__ == "__main__":
    unittest.main()
