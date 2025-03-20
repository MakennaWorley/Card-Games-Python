from enum import Enum

class SUIT(Enum):
    HEARTS = "♥ Hearts"
    DIAMONDS = "♦ Diamonds"
    CLUBS = "♣ Clubs"
    SPADES = "♠ Spades"

class RANK(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

class BUTTON(Enum):
    DEALER = "Dealer"
    SB = "Small Blind"
    BB = "Big Blind"
    PLAYER = "Player"

class PHASE(Enum):
    PF = "Pre-Flop"
    FLOP = "Flop"
    TURN = "Turn"
    RIVER = "River"
