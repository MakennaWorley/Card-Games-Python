from card_enums import BUTTON, RANK, SUIT
from card import Card
from single_deck import SingleDeck
import random

class Player:
    def __init__(self, name, chips=1000, community_cards=[], position=BUTTON.PLAYER, verbose=False):
        self.name = name
        self.chips = chips
        self.hand = []
        self.community_cards = community_cards
        self.current_bet = 0
        self.folded = False
        self.position = position
        self.verbose = verbose

    def place_bet(self, amount):
        if amount > self.chips:
            raise ValueError("Not enough chips!")
        self.chips -= amount
        self.current_bet += amount

    def fold(self):
        self.folded = True

    def receive_cards(self, cards):
        self.hand.extend(cards)

    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False

    def hand_str(self):
        return ", ".join(str(card) for card in self.hand)

    def community_cards_str(self):
        return ", ".join(str(card) for card in self.community_cards)


class RandomPlayer(Player):
    def make_decision(self, highest_bet, call_amount):
        """
        A more refined random decision process:
          - If call_amount == 0, then no one has bet/raised yet.
            * We can either check or make a small bet or bigger bet.
          - If call_amount > 0, we can fold, call, or raise by a random amount.
          - If we don't have enough chips to call, we might fold or go all-in.
        """
        if self.folded or self.chips <= 0:
            return

        if call_amount >= self.chips:
            if random.random() < 0.5:
                self.fold()
                if self.verbose:
                    print(f"{self.name} folds (cannot afford call).")
            else:
                bet = self.chips
                self.place_bet(bet)
                if self.verbose:
                    print(f"{self.name} goes all-in with {bet}.")
            return

        action = random.choices(
            population=["fold", "call", "raise"],
            weights=[0.1, 0.6, 0.3],
            k=1
        )[0]

        if action == "fold":
            self.fold()
            if self.verbose:
                print(f"{self.name} folds.")
        elif action == "call":
            self.place_bet(call_amount)
            if self.verbose:
                print(f"{self.name} calls {call_amount}.")
        else:
            min_raise = 5
            max_raise = min(self.chips - call_amount, 3 * call_amount)
            if max_raise < min_raise:
                if self.chips > call_amount:
                    bet = call_amount
                    self.place_bet(bet)
                    if self.verbose:
                        print(f"{self.name} wanted to raise but can only call {bet}.")
                else:
                    bet = self.chips
                    self.place_bet(bet)
                    if self.verbose:
                        print(f"{self.name} goes all-in with {bet}.")
            else:
                raise_amount = random.randint(min_raise, max_raise)
                total_bet = call_amount + raise_amount
                if total_bet > self.chips:
                    total_bet = self.chips
                self.place_bet(total_bet)
                if self.verbose:
                    if total_bet == self.chips:
                        print(f"{self.name} goes all-in with {total_bet}.")
                    else:
                        print(f"{self.name} raises by {raise_amount} (total {total_bet}).")


class HumanPlayer(Player):
    def make_decision(self, highest_bet, call_amount):
        """
        Prompt a human user for a fold/call/check/raise decision, ensuring
        the bet is within the player's chip range.

        Arguments:
          highest_bet: the current highest bet in this street
          call_amount: how many chips we must place to call
                       (i.e. highest_bet - self.current_bet)
        """

        if self.folded or self.chips <= 0:
            return

        print(f"\n{self.name}, it's your turn!")
        print(f"Your current chips: {self.chips}")
        print(f"Your current bet (this street): {self.current_bet}")
        print(f"Highest bet so far: {highest_bet}")
        print(f"Call amount needed: {call_amount}")

        print("Your hand:", ", ".join(str(c) for c in self.hand))

        if call_amount >= self.chips:
            while True:
                action = input("You can only fold or go all-in. (f/a): ").strip().lower()
                if action == "f":
                    self.fold()
                    print(f"{self.name} folds.")
                    return
                elif action == "a":
                    # all-in
                    bet = self.chips
                    self.place_bet(bet)
                    print(f"{self.name} goes all-in for {bet} chips.")
                    return
                else:
                    print("Invalid input. Type 'f' to fold or 'a' to go all-in.")
            return

        while True:
            if call_amount == 0:
                # No bet to call => fold/check/bet/raise
                action = input("Do you want to fold (f), check (c), or raise (r)? ").strip().lower()
            else:
                action = input("Do you want to fold (f), call (c), or raise (r)? ").strip().lower()

            if action == "f":
                self.fold()
                print(f"{self.name} folds.")
                return

            elif action == "c":
                if call_amount > 0:
                    self.place_bet(call_amount)
                    print(f"{self.name} calls {call_amount}.")
                else:
                    # check
                    print(f"{self.name} checks (no additional bet).")
                return

            elif action == "r":
                min_raise = 5
                print(f"You must bet at least {call_amount + min_raise}, up to {self.chips}.")

                while True:
                    try:
                        raise_amount = int(input("Enter raise amount above the call: "))

                        total_needed = call_amount + raise_amount
                        if raise_amount < min_raise:
                            print(f"Raise too small! Must be at least {min_raise} over the call.")
                            continue
                        if total_needed > self.chips:
                            print(
                                f"You only have {self.chips} chips! Must be <= {self.chips - call_amount} over the call.")
                            continue

                        self.place_bet(total_needed)
                        print(f"{self.name} raises by {raise_amount}, total bet {total_needed}.")
                        return
                    except ValueError:
                        print("Invalid number. Try again.")
            else:
                print("Invalid input. Please type 'f', 'c', or 'r'.")


if __name__ == '__main__':
    deck = SingleDeck()
    deck.shuffle()
    deck.show_top_cards(5)
    print("-" * 30)

    cc = Card(RANK.ACE, SUIT.HEARTS)

    player = Player("Alice", chips=500, position=BUTTON.DEALER, community_cards=[cc])

    dealt_cards = [deck.draw_card(), deck.draw_card()]
    player.receive_cards(dealt_cards)
    print(f"{player.name}'s hand: {player.hand_str()} and community cards: {player.community_cards_str()}")
