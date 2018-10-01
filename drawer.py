import sys,os
import curses
import state
import logging
import controller
import time
from curses.textpad import Textbox, rectangle

EMPTY_CARD_LINES = 5
EMPTY_CARD_COLS = 9
CARD_LINES = 4
CARD_COLS = 8
CLOSED_CARD_INNER_LINES = 2
CLOSED_CARD_INNER_COLS = 4
STACK_LINE = 6

def drawEmptyCard(stdscr, x, y):
    emptyCard = stdscr.subwin(EMPTY_CARD_LINES, EMPTY_CARD_COLS, x, y)
    emptyCard.box()
    stdscr.addstr(x+2, y+2, 'EMPTY')

def drawClosedCard(stdscr, x, y):
    box1 = stdscr.subwin(CARD_LINES, CARD_COLS, x, y)
    box1.box()
    box2 = stdscr.subwin(CLOSED_CARD_INNER_LINES, CLOSED_CARD_INNER_COLS, x+1, y+2)
    box2.box()

def drawOpenCard(stdscr, x, y, card):
    box3 = stdscr.subwin(CARD_LINES-1, CARD_COLS, x, y)
    box3.box()
    face = card.face
    suit = card.suit
    color = card.color
    cardStr = ''
    if face.value <= 10:
        cardStr += str(face.value)
    elif face.value == 11:
        cardStr += 'J'
    elif face.value == 12:
        cardStr += 'Q'
    elif face.value == 13:
        cardStr += 'K'
    else:
        raise Exception('unknown value: ' + str(face.value))

    cardStr += ' '
    if suit == state.Suit.SPADE:
        cardStr += '\u2660' if color == state.Color.BLACK else '\u2664'
    elif suit == state.Suit.HEART:
        cardStr += '\u2665' if color == state.Color.BLACK else '\u2661'
    elif suit == state.Suit.DIAMOND:
        cardStr += '\u2666' if color == state.Color.BLACK else '\u2662'
    elif suit == state.Suit.CLUB:
        cardStr += '\u2663' if color == state.Color.BLACK else '\u2667'
    else:
        raise Exception('unknown suit')

    stdscr.addstr(x+1, y+2, cardStr)

def drawStack(stdscr, stack, x, y, logging):
    showInd = stack.showIndex
    #showInd = 0
    cards = stack.cardStack

    for i in range(0, showInd):
        stdscr.hline(x + i + 1, y + 1, '_', STACK_LINE)
    for j in range(showInd, len(cards)):
        #logging.warning(''+ str( x + showInd + 1+(j-showInd)*CARD_LINES)+' '+str(y)
        drawOpenCard(stdscr, x + showInd + 1+(j-showInd)*(CARD_LINES-2), y , cards[j])


def draw_state(stdscr, gameState, logging):
    # draw the stock
    #gameState.stock = []
    if gameState.waste == len(gameState.stock)-1:
        drawEmptyCard(stdscr, 0, 0)
    else:
        drawClosedCard(stdscr, 1, 1)

    stdscr.addstr(5, 1, '[S]tock')

    # draw the waste
    if gameState.waste == -1:
        drawEmptyCard(stdscr, 0, 11)
    else:
        drawOpenCard(stdscr, 1, 11,gameState.stock[gameState.waste])

    stdscr.addstr(5, 12, '[W]aste')

    # draw col numbers
    for i in range(len(gameState.table)):
        stdscr.addstr(7, 3+i*CARD_COLS, 'C'+str(i+1))

    # draw table
    #drawOpenCard(stdscr, 10, 30, gameState.stock[0])
    #drawOpenCard(stdscr, 15, 0, gameState.stock[1])
    for i in range(len(gameState.table)):
        if gameState.table[i].length() == 0:
            drawEmptyCard(stdscr, 8, i*CARD_COLS)
        else:
            drawStack(stdscr, gameState.table[i], 8, i*CARD_COLS, logging)

    # draw foundation
    for i in range(len(gameState.foundation)):
        if gameState.foundation[i].face == state.Face.NONE: # empty
            drawEmptyCard(stdscr, 0, 22+i*(CARD_COLS+1))
        else:
            drawOpenCard(stdscr, 0, 22+i*CARD_COLS, gameState.foundation[i])
    # draw foundation text
    for i in range(len(gameState.foundation)):
        stdscr.addstr(5, 27+i*CARD_COLS, 'F'+str(i+1))




def draw(stdscr, logging):
    k = 0
    cursor_x = 0
    cursor_y = 0

    curses.noecho ()
    curses.curs_set (0)
    curses.raw ()
    stdscr.keypad (0)

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    stdscr.nodelay (True)
    y, x = stdscr.getmaxyx ()

    stdscr.setscrreg (1, y-1)
    stdscr.scrollok (True)



    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    gameState = state.State(logging)
    statusbarstr = 'Enter Command: '
    gameController = controller.Controller(logging)
    # Loop where k is the last character pressed
    error = ''
    win = False
    while True:

        # Initialization
        stdscr.erase()
        height, width = stdscr.getmaxyx()

        if win:
            stdscr.addstr(height//2, width//2, 'You Won')
            stdscr.refresh()
            time.sleep(5)
            break

        draw_state(stdscr, gameState, logging)

        if error:
            stdscr.attron(curses.color_pair(2))
            stdscr.addstr(height-2, 0, error)
            stdscr.attroff(curses.color_pair(2))

        # Render status bar
        stdscr.attron(curses.color_pair(3))
        stdscr.addstr(height-1, 0, statusbarstr)
        #stdscr.addstr(height-1, len(statusbarstr), " " * (width - len(statusbarstr) - 1))

        sub2 = stdscr.subwin(1, 8, height-1,  len(statusbarstr))
        tb = curses.textpad.Textbox(sub2)
        stdscr.refresh()
        tb.edit()
        message = tb.gather()
        if message and message[0] == 'q':
            break
        error, gameState = gameController.applyMove(message, gameState)
        win = gameController.checkWinState(gameState)

        stdscr.attroff(curses.color_pair(3))
        # Refresh the screen
        stdscr.refresh()


def main():
    logging.basicConfig(format='%(asctime)-6s: %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG,
            filename="log.txt")
    curses.wrapper(draw, logging)

if __name__ == "__main__":
    main()
