from enum import Enum

class SUIT(Enum):
    HEARTS = "♥ Hearts"
    DIAMONDS = "♦ Diamonds"
    CLUBS = "♣ Clubs"
    SPADES = "♠ Spades"

class VALUE(Enum):
    ACE = "Ace"
    TWO = "2"
    THREE = "3"
    FOUR = "4"
    FIVE = "5"
    SIX = "6"
    SEVEN = "7"
    EIGHT = "8"
    NINE = "9"
    TEN = "10"
    JACK = "Jack"
    QUEEN = "Queen"
    KING = "King"

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
