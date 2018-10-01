import state

class Controller:
    def __init__(self, logging):
        self._logging = logging
        return

    def isValidCard(self,cardString):
        cardString = cardString.strip()
        try:
            face = int(cardString)
            if face >= 1 and face <= 10:
                return True
        except ValueError:
            if cardString == 'J' or cardString == 'Q' or cardString == 'K':
                return True
            return False

    def getCardFace(self,cardString):
        cardString = cardString.strip()
        try:
            return int(cardString)
        except ValueError:
            if cardString == 'J':
                return 11
            elif cardString == 'Q':
                return 12
            elif cardString == 'K':
                return 13

    def isValidLocation(self,string):
        self._logging.warning('>> ' + string)
        if len(string) == 1:
            return True if string == 'W' or string == 'S' else False
        elif len(string) == 2:
            letter = string[0]
            number = -1
            try:
                number = int(string[1])
            except ValueError:
                self._logging.warning('not a number')
                return False
            return True if (string[0] == 'C' and number >= 1 and number <= 7)\
             or (string[0] == 'F' and number >= 1 and number <= 4)\
             else False

    def getLocationAndNumber(self,string):
        return string[0], int(string[1]) - 1

    def applyMove(self, move, gameState):
        self.gameState = gameState
        move = move.strip().upper()
        self._logging.warning('> ' + str(move))
        if len(move) == 1 and move[0] == 'S': # move type 1
            return self.openStock(), self.gameState
        elif len(move) == 4 and move[0] == 'W' and move[1] == ' ' and \
        self.isValidLocation(move[2:]): # move type 2
            self._logging.warning('>>>')
            location, number = self.getLocationAndNumber(move[2:])
            self._logging.warning('>>>>')
            return self.moveFromWaste(location, number), self.gameState
        elif (len(move) == 7 or len(move) == 8) and move[0] == 'C' and \
        self.isValidLocation(move[0:2]) and (move[-2] == 'F' or move[-2] == 'C') and \
        self.isValidLocation(move[-2:]) and self.isValidCard(move[2:-2]): # move type 3
            loc1, num1 = self.getLocationAndNumber(move[0:2])
            loc2, num2 = self.getLocationAndNumber(move[-2:])
            cardFace = self.getCardFace(move[2:-2])
            return self.moveFromTable(num1, loc2, num2, cardFace), self.gameState
        else:
            self._logging.warning('in else')
            return "Illegal move", self.gameState

    def openStock(self):
        self.gameState.waste+=1
        if self.gameState.waste >= len(self.gameState.stock):
            self.gameState.waste = -1

        return None

    # move card1 onto card2
    def canMoveToFoundation(self,card1, card2):
        if card2.face == state.Face.NONE and card1.face == state.Face.ACE:
            return True
        if card1.face == state.Face.NONE:
            return False
        if card1.suit == card2.suit and card1.face.value - card2.face.value == 1:
            return True
        else:
            return False

    def canMoveToTable(self,card1, card2):
        if card2.face == state.Face.NONE and card1.face == state.Face.KING:
            return True
        if card1.face == state.Face.NONE:
            return False
        if card1.color != card2.color and card2.face.value - card1.face.value == 1:
            return True
        else:
            return False

    def moveFromWaste(self, location, number):
        waste = self.gameState.waste
        if waste == -1:
            return 'Waste is empty'

        cardToMove = self.gameState.stock[waste]

        if location == 'F':
            cardBelow = self.gameState.foundation[number]
            if self.canMoveToFoundation(cardToMove, cardBelow):
                del self.gameState.stock[waste]
                self.gameState.waste -= 1
                self.gameState.foundation[number] = cardToMove
                return None
            else:
                return 'Cannot move to foundation'
        elif location == 'C':
            cardBelow = self.gameState.table[number].peekCard()
            if cardBelow == None:
                cardBelow = state.Card()
            if self.canMoveToTable(cardToMove, cardBelow):
                del self.gameState.stock[waste]
                self.gameState.waste -= 1
                self.gameState.table[number].addCard(cardToMove)
                return None
            else:
                return 'Illegal Move'
        else:
            return 'Illegal Location'

    def moveFromTable(self, numTable, loc2, num2, cardFace):
        cardStack = self.gameState.table[numTable].cardStack
        showIndex = self.gameState.table[numTable].showIndex
        cardInd = -1
        for i in range(len(cardStack)-1,showIndex-1, -1):
            if cardStack[i].face.value == cardFace:
                cardInd = i
                break

        if cardInd == -1:
            return "No such card is at col " + str(numTable)

        cardToMove = cardStack[cardInd]

        if loc2 == 'F':
            if cardInd != len(cardStack)-1:
                return "Cannot move card"
            cardBelow = self.gameState.foundation[num2]
            if self.canMoveToFoundation(cardToMove, cardBelow):
                self.gameState.table[numTable].popCard()
                self.gameState.foundation[num2] = cardToMove
                return None
            return "Illegal Move"
        elif loc2 == 'C':
            cardBelow = self.gameState.table[num2].peekCard()
            if cardBelow == None:
                cardBelow = state.Card()
            if self.canMoveToTable(cardToMove, cardBelow):
                for i in range(cardInd, len(cardStack), 1):
                    self.gameState.table[num2].addCard(cardStack[i])
                for i in range(len(cardStack)-1, cardInd-1, -1):
                    self.gameState.table[numTable].popCard()
                return None
            else:
                return 'Illegal Move'
        else:
            return 'Illegal Location'

    def checkWinState(self, gameState):
        if len(gameState.stock) != 0:
            return False
        for table in gameState.table:
            if length(table) != 0:
                return False
        return True
