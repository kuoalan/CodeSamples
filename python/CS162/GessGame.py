# Name: Alan Kuo
# Date: 5/18/2020
# Description: Implementation of the board game Gess


class Selection:
    """Represents a 3x3 Selection"""

    def __init__(self, center):
        """Initializes selection. Converts alpha-num center coordinate to num-num and calculates footprint.
        Used for getting the footprint of a selection and checking if it is a valid in-bounds selection."""
        self._center = center
        self._footprint = [[self._center[0] + num1, self._center[1] + num2] for num1 in range(-1, 2) for num2 in
                           range(-1, 2)]

    def footprint(self):
        """Returns footprint coordinates"""
        return self._footprint

    def check_valid_selection(self):
        """Function for checking if selection is valid"""
        # checking that center of piece is within bounds
        if not (0 < self._center[0] < 19 and 0 < self._center[1] < 19):
            return False
        else:
            return True


class Piece(Selection):
    """Represents a 3x3 Game Piece. Inherits from Selection. Includes method for determining which movement
    directions are allowed, based on the stones contained in the Piece."""

    def __init__(self, center, curr_player_stones):
        super().__init__(center)
        """Initializes Game Piece"""
        self._dirs = ["DL", "L", "UL", "D", "C", "U", "DR", "R", "UR"]
        self._dir_coords = {self._dirs[i]: self._footprint[i] for i in range(len(self._dirs))}
        self._contained_stones = [stone for stone in curr_player_stones if stone in self.footprint()]
        #self._contained_stones = contained_stones

    def contained_stones(self):
        return self._contained_stones

    def move_dirs(self):
        move_dirs = [key for key, value in self._dir_coords.items() for coord in self._contained_stones if coord == value]
        return move_dirs


class GessGame:
    """Represents a game of Gess. Stores game board and game state. Includes method for making moves. Includes
    other helper methods to implement game functionality."""

    # Initializes game board and stone locations
    def __init__(self):
        """Initializes Game Board"""

        # Board will be saved as a list of lists. Each nested list represents a row.
        # Coordinate system for board will be a numerical [col, row]. For example, "a3" will be [0,2]
        self._board = [["-"] * 20 for _ in range(20)]
        self._game_state = "UNFINISHED"
        self._curr_player = "BLACK"
        self._opp_player = "WHITE"
        self._black_starting = ["b3", "c2", "c3", "c4", "c7", "d3", "e2", "e4", "f3", "f7", "g2", "g4", "h2", "h3", "h4",
                                "i2", "i3", "i4", "i7", "j2", "j3", "j4", "k2", "k3", "k4", "l2", "l4", "l7", "m2", "m3",
                                "m4", "n2", "n4", "o3", "o7", "p2", "p4", "q3", "r2", "r3", "r4", "r7", "s3"]

        # Converting coordinates for black stones and placing on board
        self._black_stones = [coord_converter(stone) for stone in self._black_starting]
        for stone in self._black_stones:
            self._board[stone[1]][stone[0]] = "B"

        # Placing white stones on board
        self._white_stones = [[stone[0], stone[1]+15] if stone[1] != 6 else [stone[0], 13]for stone in self._black_stones]
        for stone in self._white_stones:
            self._board[stone[1]][stone[0]] = "W"


    def print_board(self):
        for i in range(19, -1, -1):
            print(self._board[i])

    def print_black_stones(self):
        print(self._black_stones)

    def place_stone(self, coord, stone_list, symbol):
        """Places stone on board and appends to each player's list of stones. Due to list structure of board,
        stone is placed on board as [col][row]"""
        self._board[coord[1]][coord[0]] = symbol
        stone_list.append(coord)

    def remove_stone(self, coord, stone_list):
        """Removes stone from board and removes from each player's list of stones. Due to list structure of board,
        stone coordinates are [col][row]"""
        self._board[coord[1]][coord[0]] = "-"
        stone_list.remove(coord)

    def player_stone_selector(self):
        if self._curr_player == "BLACK":
            curr_player_stones = self._black_stones
            opp_player_stones = self._white_stones
        elif self._curr_player == "WHITE":
            curr_player_stones = self._white_stones
            opp_player_stones = self._black_stones
        return curr_player_stones, opp_player_stones

    def make_move(self, center_1, center_2):
        if self._game_state != "UNFINISHED":
            print("The game is already over!")
            return False
        center_1 = coord_converter(center_1)
        center_2 = coord_converter(center_2)
        return self.stone_handler(center_1, center_2)


    def stone_handler(self, center_1, center_2):
        """Handles checking if move goal and direction are valid. Handles stone capture/removal and placement of stones
        after successful move"""

        # setting current player stones, symbol, and start/end selections for proposed move.
        curr_player_stones, opp_player_stones = self.player_stone_selector()
        curr_player_sym = self._curr_player[0]
        start_sel = Selection(center_1)
        end_sel = Selection(center_2)

        # Checking if starting and ending locations are valid with check_valid_selection method.
        if not start_sel.check_valid_selection() == end_sel.check_valid_selection() == True:
            print("bad selection or bad target!")
            return False

        # Checking starting footprint for any of opponent's stones
        start_footprint = start_sel.footprint()
        opp_stones_in_sel = any(stone in opp_player_stones for stone in start_footprint)
        if opp_stones_in_sel:
            print("Hey! you gotta pick something with only your stones!")
            return False

        # Initializing Piece object that will be moving
        moving_piece = Piece(center_1, curr_player_stones)

        # Getting stones contained in Piece and checking if move is allowed
        contained_stones = moving_piece.contained_stones()
        if not self.check_dir_range(center_1, center_2, contained_stones):
            print("Range or direction incorrect")
            return False

        # Gets list of current player's stones that aren't moving, and runs collision checking method.
        curr_stationary_stones = [stone for stone in curr_player_stones if stone not in contained_stones]
        stationary_stones = opp_player_stones + curr_stationary_stones
        if not self.collision_checker(center_1, center_2, stationary_stones):
            return False

        # Setting backup lists for restoring board if necessary.
        backup_black = self._black_stones[:]
        backup_white = self._white_stones[:]

        # Removing current player's stones from starting location.
        for stone in contained_stones:
            self.remove_stone(stone, curr_player_stones)

        # Removing both player's stones from ending location
        for stone in end_sel.footprint():
            if stone in curr_stationary_stones:
                self.remove_stone(stone, curr_player_stones)
            elif stone in opp_player_stones:
                self.remove_stone(stone, opp_player_stones)

        # Uses stone_mover method to place stones at new location in proper places.
        self.stone_mover(center_2, moving_piece.move_dirs(), curr_player_stones, curr_player_sym)

        # If move results in current player losing their last O, restores board to state from before attempted move.
        if not self.o_checker(curr_player_stones):
            print("Your move leaves you without an O!")
            self.restore_board(backup_black, backup_white)
            return False

        # If move results in opponent losing their last O, changes game state
        if not self.o_checker(opp_player_stones):
            print("Your opponent lost!")
            self._game_state = self._curr_player + "_WON"
            return True

        # Move is successful. Switches players for next move and returns True.
        self._curr_player, self._opp_player = self._opp_player, self._curr_player
        for i in range(19, -1, -1):
            print(self._board[i])
        return True



    def restore_board(self, black_list, white_list):
        """Restores game board from backup lists of pieces"""
        self._board = self._board = [["-"] * 20 for _ in range(20)]
        self._black_stones = []
        self._white_stones = []
        for stone in black_list:
            self.place_stone(stone, self._black_stones, "B")
        for stone in white_list:
            self.place_stone(stone, self._white_stones, "W")


    def stone_mover(self, center, directions, player_list, symbol):
        """Function for moving stones to new location during a move."""
        offsets = {"DL": (-1, -1), "L": (-1, 0), "UL": (-1, 1), "D": (0, -1), "U": (0, 1), "DR": (1, -1), "R": (1, 0),
                   "UR": (1, 1), "C": (0,0)}

        for direction in directions:
            new_col = center[0] + offsets[direction][0]
            new_row = center[1] + offsets[direction][1]
            if 0 < new_col < 19 and 0 < new_row < 19:
                self.place_stone([new_col, new_row], player_list, symbol)


    def o_checker(self, stone_list):
        """Function for checking if player has a valid O."""
        offsets = {(0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (2,2)}
        for stone in stone_list:
            other_o_stones = [[stone[0] + offset[0], stone[1] + offset[1]] for offset in offsets]
            if all(stone in stone_list for stone in other_o_stones) is True and [stone[0] + 1, stone[1] + 1] not in stone_list:
                return True
        return False

    def collision_checker(self, center_1, center_2, stationary_stones):
        # Collision checking
        move_dir, move_range = self.find_dir_range(center_1, center_2)
        offsets = self.dir_offsets(move_dir)
        for i in range(1, move_range):
            new_center = [center_1[0] + i * offsets[0], center_1[1] + i * offsets[1]]
            test_footprint = Selection(new_center).footprint()
            overlapping_stones = any(stone in stationary_stones for stone in test_footprint)
            if overlapping_stones:
                print("Your move collided!")
                return False
        return True



    def dir_offsets(self, move_dir):
        """Helper function that returns x and y offsets for a 1 unit move in any direction. Used for collision checking"""
        offsets = {"DL": (-1,-1), "L": (-1,0), "UL": (-1, 1), "D": (0, -1), "U": (0, 1), "DR": (1, -1), "R": (1, 0), "UR": (1,1)}
        try:
            return offsets[move_dir]

        except KeyError:
            return "OOPS!"

        return x, y

    def check_dir_range(self, center_1, center_2, contained_stones):
        """Function for checking if direction and range of move are allowed."""
        # Initializing piece to check
        valid_piece = Piece(center_1, contained_stones)

        # Getting valid move directions based on contained stones with the move_dirs method.
        valid_dirs = valid_piece.move_dirs()

        # if only center stone is present, piece cannot move
        if valid_dirs == ["C"]:
            print("no possible directions!")
            return False

        # setting range for move, range is unlimited if center space is filled, otherwise range is 3 squares
        elif "C" in valid_dirs:
            move_range = 99
        else:
            move_range = 3

        # Finding the direction and range of the attempted move with the find_dir_range method
        test_dir_range = self.find_dir_range(center_1, center_2)
        if test_dir_range[0] in valid_dirs and test_dir_range[1] <= move_range:
            return True
        else:
            return False


    def find_dir_range(self, center_1, center_2):
        """Function for finding the direction and range of a move, given an initial and final center space."""

        # Finding the change in x and y values
        x_delta = center_2[0] - center_1[0]
        y_delta = center_2[1] - center_1[1]

        # Returns direction and range of move as a tuple
        if x_delta == y_delta != 0:
            if x_delta > 0:
                return "UR", x_delta
            else:
                return "DL", abs(x_delta)

        elif x_delta == - y_delta != 0:
            if x_delta > 0:
                return "DR", x_delta
            else:
                return "UL", abs(x_delta)

        elif x_delta == 0:
            if y_delta > 0:
                return "U", y_delta
            elif y_delta < 0:
                return "D", abs(y_delta)
            else:
                return "Not valid"

        elif y_delta == 0:
            if x_delta > 0:
                return "R", x_delta
            elif x_delta < 0:
                return "L", x_delta
            else:
                return "Not valid"

        # Move is not in an allowed direction
        else:
            return "Not valid"

    def resign_game(self):
        """Function for current player to resign the game and give the opposing player the win"""
        game_state = self._game_state = self._opp_player + "_WON"


def coord_converter(coordinate):
    """Converts letter-number coordinate to number-number coordinate system used in program"""

    # If coordinate is in alphanumeric form
    try:
        if coordinate[0].isalpha():
            return [(ord(coordinate[0]) - 97), int(coordinate[1:]) - 1]

    # If coordinate is in numerical form
    except AttributeError:
        return [chr(coordinate[0]+97), coordinate[1]+1]



GG = GessGame()
GG.print_board()
print("test")
#print(GG.make_move("c14", "c16"))
print(GG.make_move("r3", "s3"))
print(GG.make_move("d18", "c17"))
#print(GG.make_move("k3", "k4"))
#print(GG.make_move("c3", "c4"))
#print(GG.make_move("c2", "c5"))
print(GG.make_move("c18", "c17"))
#print(GG.make_move("c5", "d4"))
#print(GG.make_move("r15", "r14"))
print(GG.make_move("l5", "m5"))

#GG.resign_game()
#print(GG.make_move("e3", "d4"))
#print(GG.make_move("c3", "c4"))
#GG.place_stone([2, 12], GG._black_stones, "B")
#print(GG.make_move("c12", "c15"))
#GG.print_board()
#GG.remove_stone([10,2], GG._black_stones)
#GG.remove_stone([7,1], GG._black_stones)
#GG.print_board()
#print(GG.o_checker(GG._black_stones))
#print(GG.o_checker(GG._white_stones))