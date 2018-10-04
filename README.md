# solitaire
Command line version of klondike solitaire

# How to run
python3 drawer.py

# How to play
The game has standard Klonkide solitaire rules. The four commands are:
1. S : flip through stock
2. W C<col_name> | ex: W C1 | move from waste to table 1
3. W F<col_name> | ex: W F1 | move from waste to foundation 1
4. C<col_name> <card_num><suit> F<col_name> | ex: C7 10H F2 | move 10 of hearts
from column 7 of table to foundation's column 2

There are seven columns of table and four columns of foundation.
You win when the table and stock is empty.

The four suits are [H]earts, [S]pades, [D]iamonds, [C]lubs

# Design choices
Since this game is supposed to run in the terminal, I designed the UI to be
really simply without any complex graphics. The program is inspired by The
model-view-controller pattern. The game's state is stored as various arrays and
the drawer creates the view using the game's state and the controller takes the
user input to apply changes to the state.

# Dependencies
Python 3.7
