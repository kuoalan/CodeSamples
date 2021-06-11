## FBoard.py
Text based implementation of a two-player board game in Python 3.

## Instructions for CS 161 Portfolio Project

Write a class named FBoard for playing a game, where player x is trying to get her piece to corner square (7,7) and player o is trying to make it so player x doesn't have any legal moves.  It should have the following private data members:

* An 8x8 list of lists for tracking what's on each square of the board.
* A data member for tracking the game state, that holds one of the following string values: "X_WON", "O_WON", or "UNFINISHED".
* Data members to keep track of where the x piece is.

**The data members should all be private.**
* An init method (constructor) that initializes the list of lists to represent an empty 8x8 board (you can use whatever character you want to represent empty).  It should put four o pieces at the following (row, column) coordinates: (5,7), (6,6), (7,5), and (7,7).  It should put an x piece at (0,0).  It should also initialize the other data members.
* A method called get_game_state, that returns the current value of game_state.
* A method called move_x that takes as parameters the row and column of the square to move to.  If the desired move is not allowed, or if the game has already been won, it should just return False.  Otherwise it should make the move and return True.  A piece belonging to x can move 1 square diagonally in any direction.  A piece is not allowed to move off the board or to an occupied square.  If x's move gets her piece to square (7,7), game_state should be set to "X_WON".
* A method called move_o that takes as parameters the row and column to move from, and the row and column to move to.  If the first pair of coordinates doesn't hold o's piece, or if the desired move is not allowed, or if the game has already been won, it should just return False.  Othewise it should make the move and return True.  A piece belonging to o can move 1 square diagonally, **but the row and column cannot both increase**, so any o piece has at most three available moves.  For example, if player o has a piece at (5, 1), it could move to (4, 0), (4, 2), or (6,0), but not to (6, 2).  It is not allowed to move off the board or to an occupied square.  If o's move leaves no legal move for x, game_state should be set to "O_WON".

You do not need to track whose turn it is.  Either move method can be called multiple times in a row.

It doesn't matter which index of the list of lists you consider the row and which you consider the column as long as you're consistent.

Feel free to add helper functions if you want.  You may also find it useful to add a print function to help with debugging.

Here's a very simple example of how the class could be used:
```
   fb = FBoard();
   fb.move_x(1,1);
   fb.move_x(2,0);
   fb.move_o(6,6,5,5);
   print(fb.get_game_state());
```
The file must be named: **FBoard.py**
