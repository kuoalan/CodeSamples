class FBoard:
    """Class for playing a game. Player x is trying to move their piece to coordinate [7,7]
    and player o is trying to stop player x by surrounding her"""
    def __init__(self):
        """Initializes game state, empty game board, and places pieces"""
        # initializing game state and empty game board
        # game coordinate system is [row, col] or [row][col] to access element on game board
        # coordinate [0,0] is bottom left of board (x starting position)
        # coordinate [7,7] is top right of board (victory position for x)
        self._game_state = "UNFINISHED"
        self._game_board = [["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""],
                            ["", "", "", "", "", "", "", ""]]
        # setting coordinates for x and o pieces at start of game
        self._x_location = [0, 0]
        self._o_locations = [[5, 7], [6, 6], [7, 5], [7, 7]]
        # placing pieces on board
        self._game_board[0][0] = "x"
        for coord in self._o_locations:
            self._game_board[coord[0]][coord[1]] = "o"

    def get_game_state(self):
        """Returns current game state"""
        return self._game_state

    def check_valid_move(self, player, row_from, col_from, row_to, col_to):
        """Checks whether move is valid"""
        # Checking if move is within game bounds, game state is unfinished, and move is diagonal and to an empty sqace
        if (0 <= row_to <= 7 and 0 <= col_to <= 7 and self._game_state == "UNFINISHED" and
                abs(row_to - row_from) == 1 and abs(col_to - col_from) == 1 and self._game_board[row_to][col_to] == ""):
            if player == "x":
                return True
            # Need to run two further checks for o, must move existing piece and row and col cannot both increase
            elif player == "o":
                if [row_from, col_from] in self._o_locations and not (row_to - row_from == 1 and col_to - col_from == 1):
                    return True
                # illegal o move diagonally upwards
                else:
                    return False
        # Invalid move
        else:
            return False

    def check_win(self):
        """Checks for changes in game state from either x or o winning. Returns the current game state"""
        # initializes variables for row and col of x piece for easier use in calculations
        x_row = self._x_location[0]
        x_col = self._x_location[1]

        # Checking if x is on winning space
        if x_row == x_col == 7:
            return "X_WON"

        # Checking if there are any valid moves for x, move checking function will handle any edge cases
        elif (self.check_valid_move("x", x_row, x_col, x_row + 1, x_col + 1) or
              self.check_valid_move("x", x_row, x_col, x_row + 1, x_col - 1) or
              self.check_valid_move("x", x_row, x_col, x_row - 1, x_col + 1) or
              self.check_valid_move("x", x_row, x_col, x_row - 1, x_col - 1)):
            return "UNFINISHED"

        # if there are no valid moves for x, o wins
        else:
            return "O_WON"

    def move_x(self,row_to, col_to):
        """Function for moving x piece, uses move checking and win checking functions and changes game state"""
        if self.check_valid_move("x", self._x_location[0], self._x_location[1], row_to, col_to):
            # setting previous space as empty
            self._game_board[self._x_location[0]][self._x_location[1]] = ""
            # setting new x location and placing x piece on new location on game board
            self._x_location = [row_to, col_to]
            self._game_board[row_to][col_to] = "x"
            # changes game state with win checking function
            self._game_state = self.check_win()
            return True
        else:
            return False

    def move_o(self, row_from, col_from, row_to, col_to):
        """Function for moving o piece, uses move checking and win checking functions and changes game state"""
        # checking if move is valid
        if self.check_valid_move("o", row_from, col_from, row_to, col_to):
            # clearing current location of piece of be moved and placing piece at new location
            self._game_board[row_from][col_from] = ""
            self._game_board[row_to][col_to] = "o"
            # for loop iterating through index of "o" piece locations to change location of piece to be moved
            for num in range(4):
                if self._o_locations[num] == [row_from, col_from]:
                    self._o_locations[num] = [row_to, col_to]
            # changes game state with win checking function
            self._game_state = self.check_win()
            return True
        # invalid move
        else:
            return False

