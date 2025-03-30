from enum import Enum

class SUIT(Enum):
    HEARTS = "♥ Hearts"
    DIAMONDS = "♦ Diamonds"
    CLUBS = "♣ Clubs"
    SPADES = "♠ Spades"

class RANK(Enum):
    ACE = 0
    TWO = 1
    THREE = 2
    FOUR = 3
    FIVE = 4
    SIX = 5
    SEVEN = 6
    EIGHT = 7
    NINE = 8
    TEN = 9
    JACK = 10
    QUEEN = 11
    KING = 12

class BUTTON(Enum):
    DEALER = "Dealer"
    SB = "Small Blind"
    BB = "Big Blind"
    PLAYER = "Player"
    NONE = "None"

class PHASE(Enum):
    PF = "Pre-Flop"
    FLOP = "Flop"
    TURN = "Turn"
    RIVER = "River"
