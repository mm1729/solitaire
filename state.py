from enum import Enum
import random
import logging

# constants
DECK_SIZE = 52
TABLE_COLS = 7

# Enums of properties of cards
class Face(Enum):
    ACE = 1
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
    NONE = 14

class Suit(Enum):
    SPADE = 1
    HEART = 2
    DIAMOND = 3
    CLUB = 4
    NONE = 5

class Color(Enum):
    BLACK = 1
    WHITE = 2
    NONE = 3

class Card:
    def __init__(self, face=Face.NONE, suit=Suit.NONE, color=Color.NONE):
        self.face = face
        self.suit = suit
        self.color = color

class TableStack:
    def __init__(self):
        self.cardStack = []
        self.showIndex = -1 # index [i, end] to display card faces

    def addCard(self, card):
        self.cardStack.append(card)

    def popCard(self):
        if self.showIndex > 0 and self.showIndex == len(self.cardStack) - 1:
            self.showIndex -= 1
        if self.cardStack:
            return self.cardStack.pop()
        return None

    def peekCard(self):
        if self.cardStack:
            return self.cardStack[-1]
        return None

    def length(self):
        return len(self.cardStack)




class State:
    def __init__(self, logging):
        self._logging = logging
        # initialize deck
        colors = [Color.BLACK, Color.BLACK, Color.WHITE, Color.WHITE]
        random.shuffle(colors)

        deck = []
        colorInd = 0
        for suit in range(1, len(Suit)):
            color = colors[colorInd]
            for face in range(1, len(Face)):
                deck.append(Card(Face(face), Suit(suit), color))
            colorInd+=1

        # shuffle deck
        random.shuffle(deck)

        # create table and initialize table
        self.table = [TableStack() for i in range(TABLE_COLS)]

        """for i in range(TABLE_COLS):
            for j in range(i, TABLE_COLS):
                self.table[j].addCard(deck.pop())
                self.table[j].showIndex+=1"""

        self.stock = deck
        self.waste = -1
        self.foundation = [Card() for i in range(4)]
