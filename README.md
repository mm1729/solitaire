# solitaire
Command line version of klondike solitaire

# How to run
python3 drawer.py

# Design choices
Since this game is supposed to run in the terminal, I designed the UI to be
really simply without any complex graphics. The program is inspired by The
model-view-controller pattern. The game's state is stored as various arrays and
the drawer creates the view using the game's state and the controller takes the
user input to apply changes to the state.

# Dependencies
Python 3.7
