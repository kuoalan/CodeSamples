# Name: Alan Kuo
# Date: 5/18/2020
# Description: Text-based implementation of the board game Gess.


class Selection:
    """Represents a 3x3 Selection. Includes methods for finding the footprint of a selection, and checking if
    a selection is valid (center is in-bounds). Class interacts with the GessGame class during each attempted move."""

    def __init__(self, center):
        """Initializes Selection by setting center of selection and calculating footprint of selection."""
        self._center = center
        self._footprint = [[self._center[0] + num1, self._center[1] + num2] for num1 in range(-1, 2) for num2 in
                           range(-1, 2)]

    def footprint(self):
        """Returns coordinates of spaces in footprint. Takes no parameters."""
        return self._footprint

    def check_valid_selection(self):
        """Method for checking if a selection is valid. Returns False if selection is out of bounds, otherwise True.
         Takes no parameters."""
        # Checking if center of Selection is within bounds
        if not (0 < self._center[0] < 19 and 0 < self._center[1] < 19):
            return False
        else:
            return True


class Piece(Selection):
    """Represents a 3x3 Game Piece. Inherits from Selection. Includes methods for finding coordinates of stones
    that are within the footprint of the Piece, and the allowed move directions based on the included stones.
    Class interacts with the GessGame class during each attempted move."""

    def __init__(self, center, curr_player_stones):
        """Initializes Piece. Takes center coordinate and a list of the current player's stones as parameters.
        Creates dictionary that corresponds each cardinal direction to a space in the footprint. Calculates which
        of the current player's stones are in the Piece's footprint."""

        super().__init__(center)
        self._dirs = ["DL", "L", "UL", "D", "C", "U", "DR", "R", "UR"]
        self._dir_coords = {self._dirs[i]: self._footprint[i] for i in range(len(self._dirs))}
        self._contained_stones = [stone for stone in curr_player_stones if stone in self.footprint()]

    def contained_stones(self):
        """Returns the stones contained in the Piece. Takes no parameters."""
        return self._contained_stones

    def move_dirs(self):
        """Returns the allowed move directions based on contained stones. Takes no parameters"""
        move_dirs = [key for key, value in self._dir_coords.items() for stone in self._contained_stones if
                     stone == value]
        return move_dirs


class GessGame:
    """Represents a game of Gess. Stores game board and game state. Includes method for making moves. Includes
    other helper methods to implement move and game functionality. Instantiates Selection and Piece classes during
    move functionality."""

    # Initializes game board and stone locations
    def __init__(self):
        """Initializes Game Board. Sets up game status, current player status, and places game pieces for both sides
        on the board. Takes no parameters"""

        # Board will be saved as a list of lists. Each nested list represents a row.
        # Coordinate system for board will be a numerical [col, row]. For example, "a3" will be [0,2]
        self._board = [["-"] * 20 for _ in range(20)]
        self._game_state = "UNFINISHED"
        self._curr_player = "BLACK"
        self._opp_player = "WHITE"
        self._black_starting = ["b3", "c2", "c3", "c4", "c7", "d3", "e2", "e4", "f3", "f7", "g2", "g4", "h2", "h3",
                                "h4", "i2", "i3", "i4", "i7", "j2", "j3", "j4", "k2", "k3", "k4", "l2", "l4", "l7",
                                "m2", "m3", "m4", "n2", "n4", "o3", "o7", "p2", "p4", "q3", "r2", "r3", "r4", "r7",
                                "s3"]

        # Converts coordinates for black stones, saves coordinate to list, and places on board
        self._black_stones = [self.coord_converter(stone) for stone in self._black_starting]
        for stone in self._black_stones:
            self._board[stone[1]][stone[0]] = "B"

        # Saves coordinates of white stones to list and places on board
        self._white_stones = [[stone[0], stone[1]+15] if stone[1] != 6 else [stone[0], 13] for stone in
                              self._black_stones]
        for stone in self._white_stones:
            self._board[stone[1]][stone[0]] = "W"

    def get_game_state(self):
        """Returns current game state. Takes no parameters"""
        return self._game_state

    def coord_converter(self, coordinate):
        """Converts letter-number coordinate to number-number coordinate system used in program. Takes the coordinate
        to convert as parameter and returns the converted coordinate."""
        return [(ord(coordinate[0]) - 97), int(coordinate[1:]) - 1]

    def print_board(self):
        """Function for printing game board. Used for debugging. Takes no parameters. Prints board."""
        for i in range(19, -1, -1):
            print(self._board[i])
        print("")

    def make_move(self, start_center, end_center):
        """Function for making a move. Uses helper functions for checking if move is valid. If move is valid, updates
        game state and switches current/opposing players (if necessary). Takes starting and ending coordinates of move
        as parameters. Returns True if move is successful or False if move is invalid."""

        # Checks if game is already over.
        if self._game_state != "UNFINISHED":
            return False

        # Converts alphanumeric coordinate to [column, row] coordinate as numbers with coord_converter method.
        start_center, end_center = self.coord_converter(start_center), self.coord_converter(end_center)

        # Sets current player stones, symbol, and initializes start/end Selection objects for proposed move.
        curr_player_stones, opp_player_stones = self.player_stone_selector()
        curr_player_sym = self._curr_player[0]
        start_sel, end_sel = Selection(start_center), Selection(end_center)

        # Checks if starting and ending locations are valid with check_valid_selection method.
        if not start_sel.check_valid_selection() or not end_sel.check_valid_selection():
            return False

        # Checking starting footprint for any of opponent's stones. Also will prevent moving out of turn.
        start_footprint = start_sel.footprint()
        opp_stones_in_sel = any(stone in opp_player_stones for stone in start_footprint)
        if opp_stones_in_sel:
            return False

        # Initializing Piece object that will be moving.
        moving_piece = Piece(start_center, curr_player_stones)

        # Getting stones contained in Piece and checking if move is allowed based on direction and range.
        contained_stones = moving_piece.contained_stones()
        move_dir_range = self.check_dir_range(start_center, end_center, moving_piece)
        if not move_dir_range:
            return False
        else:
            move_dir, move_range = move_dir_range

        # Gets list of current player's stones that aren't moving, and runs collision checking method.
        curr_stationary_stones = [stone for stone in curr_player_stones if stone not in contained_stones]
        stationary_stones = opp_player_stones + curr_stationary_stones
        if not self.collision_checker(start_center, move_dir, move_range, stationary_stones):
            return False

        # Setting backup lists for restoring board if necessary.
        backup_black, backup_white = self._black_stones[:], self._white_stones[:]

        # Removing current player's stones from starting footprint.
        for stone in contained_stones:
            self.remove_stone(stone, curr_player_stones)

        # Removing both player's stones from ending footprint.
        for stone in end_sel.footprint():
            if stone in curr_stationary_stones:
                self.remove_stone(stone, curr_player_stones)
            elif stone in opp_player_stones:
                self.remove_stone(stone, opp_player_stones)

        # Uses stone_mover method to place stones at new location in proper place.
        self.stone_mover(end_center, moving_piece.move_dirs(), curr_player_stones, curr_player_sym)

        # If move results in current player losing their last ring, restores board to state from before attempted move.
        if not self.ring_checker(curr_player_stones):
            self.restore_board(backup_black, backup_white)
            return False

        # If move results in opponent losing their last ring, changes game state to reflect win, switches players, and
        # returns True.
        if not self.ring_checker(opp_player_stones):
            self._game_state = self._curr_player + "_WON"
            self._curr_player, self._opp_player = self._opp_player, self._curr_player
            return True

        # Move is successful. Switches players for next move and returns True.
        self._curr_player, self._opp_player = self._opp_player, self._curr_player
        return True

    def player_stone_selector(self):
        """Helper function for assigning the correct list of stones to the current and opposing player. Takes no
        parameters and returns lists of stones for the current player and opposing player as a tuple."""
        if self._curr_player == "BLACK":
            return self._black_stones, self._white_stones
        else:
            return self._white_stones, self._black_stones

    def check_dir_range(self, start_center, end_center, piece):
        """Function for checking if direction and range of move are allowed based on the stones contained in the Piece.
         Takes starting and ending coordinates of move and Piece object as parameters. Returns False if move is invalid,
         otherwise returns the direction and range of move as a tuple."""

        # Getting valid move directions based on contained stones with the move_dirs method.
        valid_dirs = piece.move_dirs()

        # if only center stone is present, piece cannot move
        if valid_dirs == ["C"]:
            return False

        # setting range for move, range is unlimited if center space is filled, otherwise range is 3 squares
        elif "C" in valid_dirs:
            move_range = 99
        else:
            move_range = 3

        # Finding the direction and range of the attempted move with the find_dir_range method.
        move_dir_range = self.find_dir_range(start_center, end_center)
        if not move_dir_range:
            return False
        elif move_dir_range[0] in valid_dirs and move_dir_range[1] <= move_range:
            return move_dir_range[0], move_dir_range[1]
        else:
            return False

    def find_dir_range(self, start_center, end_center):
        """Helper function for finding the direction and range of a move. Used by check_dir_range method. Takes the
        starting and ending coordinates of move as parameters. If move direction corresponds to one of the allowed
        directions, returns the move direction and distance as a tuple. Otherwise, returns False"""

        # Finding the change in x and y values
        x_delta, y_delta = end_center[0] - start_center[0], end_center[1] - start_center[1]

        # Returns direction and distance of move as a tuple
        if x_delta == y_delta != 0:
            if x_delta > 0:
                return "UR", x_delta
            elif x_delta < 0:
                return "DL", abs(x_delta)

        elif x_delta == - y_delta != 0:
            if x_delta > 0:
                return "DR", x_delta
            elif x_delta < 0:
                return "UL", abs(x_delta)

        elif x_delta == 0:
            if y_delta > 0:
                return "U", y_delta
            elif y_delta < 0:
                return "D", abs(y_delta)

        elif y_delta == 0:
            if x_delta > 0:
                return "R", x_delta
            elif x_delta < 0:
                return "L", abs(x_delta)

        # Returns False if move is not in an allowed direction or if position has not changed.
        else:
            return False

    def collision_checker(self, start_center, move_dir, move_range, stationary_stones):
        """Function for checking if premature collision occurs during attempted move. Takes the start location for move,
        move direction, move range, and list of stones not involved in move as parameters. Returns False if move results
        in a premature collision, otherwise returns True."""

        # Gets corresponding offset for given move direction from dir_offsets method
        offsets = self.dir_offsets(move_dir)

        # Iterates through intermediate moves to check for collisions
        for i in range(1, move_range):
            new_center = [start_center[0] + i * offsets[0], start_center[1] + i * offsets[1]]
            test_footprint = Selection(new_center).footprint()
            if any(stone in stationary_stones for stone in test_footprint):
                return False
        return True

    def dir_offsets(self, move_dir):
        """Helper function that returns x and y offsets for a 1 unit move in any direction. Used during collision
        checking. Takes the desired move direction as a parameter and returns the correct x,y offset as a tuple."""

        offsets = {"DL": (-1, -1), "L": (-1, 0), "UL": (-1, 1), "D": (0, -1), "U": (0, 1), "DR": (1, -1), "R": (1, 0),
                   "UR": (1, 1)}
        return offsets[move_dir]

    def stone_mover(self, center, directions, player_list, symbol):
        """Function for moving stones to new location during a move. Takes the center of new location, a list of
         directional positions of the stones to be moved, the current player's list of stones, and correct symbol
         for the stones."""

        # Dictionary containing x,y offsets for each directional position
        offsets = {"DL": (-1, -1), "L": (-1, 0), "UL": (-1, 1), "D": (0, -1), "U": (0, 1), "DR": (1, -1), "R": (1, 0),
                   "UR": (1, 1), "C": (0, 0)}

        # Calculates new x,y coordinate for each stone based on their directional position.
        for direction in directions:
            new_col, new_row = center[0] + offsets[direction][0], center[1] + offsets[direction][1]
            if 0 < new_col < 19 and 0 < new_row < 19:
                self.place_stone([new_col, new_row], player_list, symbol)

    def place_stone(self, coord, stone_list, symbol):
        """Places stone on board and appends to each player's list of stones. Due to nested list structure of board,
        stone is placed on board as [col][row]. Takes coordinate of new stone to be placed, the list where the
        coordinate of the new stone is to be placed, and the specific symbol ('B' or 'W') to be placed on the
        board as parameters."""

        self._board[coord[1]][coord[0]] = symbol
        stone_list.append(coord)

    def remove_stone(self, coord, stone_list):
        """Removes stone from board and removes from each player's list of stones. Due to list structure of board,
        stone coordinates are [col][row]. Takes coordinate of stone to be removed and the list where the coordinate of
        the stone is to be removed from as parameters."""

        self._board[coord[1]][coord[0]] = "-"
        stone_list.remove(coord)

    def ring_checker(self, stone_list):
        """Function for checking if player has a valid ring by iterating through a list of stones and checking if the
        other stones in the ring are present. Each stone will be checked as if it was the lower left stone in the ring.
        Takes list of stones to check as a parameter. Returns True if ring is present, otherwise False."""

        # Offsets for other coordinates in the ring compared to the lower left stone in ring
        offsets = {(0, 1), (0, 2), (1, 0), (1, 2), (2, 0), (2, 1), (2, 2)}

        # Iterates through each stone in the list and checks that all other stones required for ring are in the list.
        for stone in stone_list:
            other_o_stones = [[stone[0] + offset[0], stone[1] + offset[1]] for offset in offsets]
            if all(stone in stone_list for stone in other_o_stones) and [stone[0] + 1, stone[1] + 1] not in stone_list:
                return True
        return False

    def restore_board(self, black_list, white_list):
        """Restores game board from backup lists of stone locations. Used by make_move method and takes lists of stones
         for the two players as parameters."""
        self._board = [["-"] * 20 for _ in range(20)]
        self._black_stones, self._white_stones = [], []
        for stone in black_list:
            self.place_stone(stone, self._black_stones, "B")
        for stone in white_list:
            self.place_stone(stone, self._white_stones, "W")

    def resign_game(self):
        """Function for current player to resign the game and give the opposing player the win. Takes no parameters."""
        self._game_state = self._opp_player + "_WON"
