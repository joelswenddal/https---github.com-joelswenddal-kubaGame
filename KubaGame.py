# Author: Joel Swenddal
# Date: 06/01/2021
# Course: CS 162
# Semester: Spring 2021
# Description: Project 9 - Portfolio Project - KubaGame
#   Program implements game play, turn taking, movement, and game state updating
#   for the game Kuba. Kuba takes place on a 7x7 grid using Black, White and Red marbles.
#   Two players, assigned Black or White marbles, take turns pushing their marbles one
#   space in any orthagonal direction, as long as the direction they 'push away' from is
#   an empty spot (the empty space provides 'access' to the marble). Any marbles in the
#   direction they are pushing in are moved down by their push (row or column).
#   Wins happen when a player pushes 7 red marbles off the board, the other player's
#   marbles (Black or White) are all pushed off the board, or the other player is not
#   able to make any moves.
#   Full Kuba rules: https://sites.google.com/site/boardandpieces/list-of-games/kuba


class WrongParameterTypeError (Exception):
    """Defines exception: WrongParameterTypeError"""
    pass


class KubaGame:
    """
    Implements the core functionality of the Kuba game. Responsibilities including:
        - initializing the game including related classes: Board and Player
        - executing moves
        - conducting move validation according to game rules
        - allotting turn-taking
        - tracking game state (including win declaration)

    KubaGame class communicates with Board class in order to:
        - update values assigned to positions on the 7 x 7 board grid

    KubaGame class communicates with Player class in order to:
        - access names and game piece (marble) colors associated with each player
        - access  and adjust number of marbles 'captured' by a player
            (related to win declaration)

    """

    def __init__(self, playerTuple1=None, playerTuple2=None):
        """
        Takes as parameters two tuples, each containing player name
        and color of the marble that the player is playing (ex: ('PlayerA', 'B'),
        ('PlayerB','W')) and it intializes the board. Players can choose to be
        either 'B' or 'W'. On the board R, B, W are used to represent Red, Black
        and White marbles. X represents an empty spot (cell) on the board.
        """

        if playerTuple1 is None:
            playerTuple1 = ('PlayerA', 'B')

        if playerTuple2 is None:
            playerTuple2 = ('PlayerB', 'W')

        self._board = Board()

        # initialize players
        self._playerA = Player(playerTuple1[0], playerTuple1[1])
        self._playerB = Player(playerTuple2[0], playerTuple2[1])

        # initalize player list
        self._player_list = [self._playerA, self._playerB]
        self._current_turn = None
        self._off_turn = None
        self._winner = None
        # _ko_move format is tuple: (coordinate, direction)
        self._ko_move = (None, None)
        self._marble_count = (8, 8, 13)

    def get_current_turn(self):
        """
        Returns the player name whose turn it is to play the next move. Returns
        None if called when no player has made the first move yet, since any player
        can start the game.
        """
        if self._current_turn == None:
            return None

        return self._current_turn.get_player_name()

    def set_current_turn(self, player_name):
        """
        Takes a player_name (string), and if the player is already initialized
        then it marks them as having the next turn. It also sets the other player
        as being in the "off-turn" player. This is used in managing
        turn-taking.

        """
        for player in self._player_list:

            if player_name == player.get_player_name():

                self._current_turn = player

            if player_name != player.get_player_name():

                self._off_turn = player

    def print_board(self):
        """
        Prints a rough visual of the board updated with its current state.
        """
        self._board.print_board()

    def validate_move(self, player_name, coordinate, direction):
        """
        Takes a player name (string), coordinate (tuple), and direction (string),
        which indicate an intended move. Validates the move according to
        game rules. Returns False if the move is invalid and True if the move
        is allowed to proceed. Used within the make_move method.
        """

        cur_row = coordinate[0]
        cur_col = coordinate[1]

        # check that key (coordinate tuple) is on the board (in dictionary)
        # will cause KeyError if not
        try:
            self._board.get_marble(coordinate)

        # Raises a KeyError (the current cell (key) can't be located in the dict - cell is not on the board)
        except KeyError:

            # print("Invalid move: Space that is not on the board.")  # For testing
            return False

        current_val = self._board.get_marble(coordinate)

        # check if the game is still in play (winner not yet declared)

        if self._winner != None:
            # For testing
            # print("Invalid move: A winner has already been declared.")
            return False

        if self.get_current_turn() == None:
            # if current turn is not assigned yet, assign it to first player
            # who makes a move
            self.set_current_turn(player_name)

        if self.get_current_turn() != player_name:
            # Check that it is player's turn or not yet assigned (None)
            # print("Invalid move: It is not your turn.")  # For testing
            return False

        # Check that there is a marble at the current location and it is not red
        if current_val in ('X', 'R'):
            # For testing
            # print("Invalid move: You are attempting to move an incorrect value.")
            return False

        # Reject attempt to move a marble different than assigned color ("B", "W")
        if current_val != self._current_turn.get_player_color():
            # For testing
            #print("Invalid move: You are attempting to move an incorrect value.")
            return False

        # Reject incorrect direction entry - invalid move
        if direction not in ("B", "F", "L", "R"):
            # For testing
            #print("Invalid move: This is not a recognized direction.")
            return False

        # Reject attempt to reverse the prior move position (Ko rule)
        if self._ko_move[0] == coordinate and self._ko_move[1] == direction:

            #print("Invalid move: Blocked because of Ko rule")
            return False

        # Below - Check that the cell is moveable (must have 'X' space in the opposite
        # direction) from the move direction

        # validate Backward (down) direction move (there must be an empty spot 'above' the cell)
        if direction == 'B':
            if self.get_marble((cur_row-1, cur_col)) != 'X':
                # For testing
                #print("Invalid move: Cannot start a move between two marbles.")
                return False

        # validate Forward (up) direction move (must be an empty spot 'below' the cell)
        elif direction == "F":
            if self.get_marble((cur_row+1, cur_col)) != 'X':
                # For testing
                #print("Invalid move: Cannot start a move between two marbles.")
                return False

        # validate Right direction move (must be an empty spot 'left' of the cell)
        elif direction == "R":
            if self.get_marble((cur_row, cur_col-1)) != 'X':
                # For testing
                #print("Invalid move: Cannot start a move between two marbles.")
                return False

        # validate Left direction move (must be an empty spot 'right' of the cell)
        elif direction == "L":
            if self.get_marble((cur_row, cur_col+1)) != 'X':
                # For testing
                #print("Invalid move: Cannot start a move between two marbles.")
                return False

        # check that the player will not push their own marble type off the board
        check_list = []

        if direction == 'B':

            for num in range(cur_row, 7):
                check_list.append(self.get_marble((num, cur_col)))

            if 'X' not in check_list:

                if self.get_marble((6, cur_col)) == self._current_turn.get_player_color():

                    #print("Invalid move: Cannot push your own marble off board.")

                    return False

        if direction == 'F':

            for num in range(0, cur_row + 1):
                check_list.append(self.get_marble((num, cur_col)))

            if 'X' not in check_list:

                if self.get_marble((0, cur_col)) == self._current_turn.get_player_color():

                    #print("Invalid move: Cannot push your own marble off board.")

                    return False

        if direction == 'R':

            for num in range(cur_col, 7):
                check_list.append(self.get_marble((cur_row, num)))

            if 'X' not in check_list:

                if self.get_marble((cur_row, 6)) == self._current_turn.get_player_color():

                    #print("Invalid move: Cannot push your own marble off board.")

                    return False

        if direction == 'L':

            for num in range(0, cur_col+1):
                check_list.append(self.get_marble((cur_row, num)))

            if 'X' not in check_list:

                if self.get_marble((cur_row, 0)) == self._current_turn.get_player_color():

                    #print("Invalid move: Cannot push your own marble off board.")

                    return False

        return True

    def make_move(self, player_name, coordinate, direction):
        """
        Implements a Kuba move. Takes three parameters: playername, coordinates i.e. a
        tuple containing the location of marble that is being moved, and the direction
        in which the player wants to push the marble. Valid directions are L(Left), R(Right),
        F(Forward) and B(Backward). Returns True if move is successful, False otherwise.
        Note that this method uses a recursive strategy to implement a move and includes
        an inner function (rec_move) to do so.
        """

        if self.validate_move(player_name, coordinate, direction) != True:
            return False

        def rec_move(current_cell, direction):
            """
            Takes a cell address (coordinates tuple) and direction (string) and 'moves' the
            marble value in the cell in the direction specified. If the next cell
            is not marked 'X', then it will 'push' the next marble value forward
            as well (until 'X' or border is reached). This uses a recursive
            strategy to simulate movement of a row n marbles where n >= 1. Note
            that this approach will 'move' any values in the cell. Validation of which
            values are allowed to move is handled separately.
            """
            cur_row = current_cell[0]
            cur_col = current_cell[1]

            # define direction adjustments (initialize next cell)
            if direction == 'L':
                next = (cur_row, cur_col-1)

            elif direction == 'R':
                next = (cur_row, cur_col + 1)

            elif direction == 'B':
                next = (cur_row + 1, cur_col)

            elif direction == 'F':
                next = (cur_row - 1, cur_col)

            # base case - successful move opportunity identified
            if self.get_marble(next) == 'X':

                if next[0] < 0 or next[0] > 6 or next[1] < 0 or next[1] > 6:

                    if self.get_marble(current_cell) == 'R':
                        self._current_turn.increment_red_marbles()

                    self._board.set_marble(current_cell, 'X')

                    self._ko_move = self.ko_rule(next, direction)
                    self.update_game_state()
                    return True

                self._board.set_marble(next, self.get_marble(current_cell))
                self._ko_move = self.ko_rule(next, direction)
                self._board.set_marble(current_cell, 'X')
                self.update_game_state()
                return True

            else:

                rec_move(next, direction)
                self._board.set_marble(next, self.get_marble(current_cell))
                self._board.set_marble(current_cell, 'X')
                return True

        return rec_move(coordinate, direction)

    def ko_rule(self, current_cell, direction):
        """
        Takes a current cell tuple (board space) and direction and
        returns a tuple that indicates a move that is off-limits
        in the next turn. Format of output tuple is:
        (coordinates tuple, direction), e.g. ((2,3), "L"). This method
        is used in move validation.
        """
        opposite = None

        if direction == "F":
            opposite = "B"

        elif direction == "B":
            opposite = "F"

        elif direction == "R":
            opposite = "L"

        elif direction == "L":
            opposite = "R"

        else:
            opposite = "X"

        return (current_cell, opposite)

    def other_player_move_check(self):
        """
        Check the other player's move options. If at least one
        move is available, returns True. If no move
        options are available on the board, then return
        False. Used as part of post-move check to identify a
        winner while updating game state.
        """
        marble_list = []
        # a list of coordinates where a player has a marble

        directions = ("F", "B", "R", "L")

        player_color = self._off_turn.get_player_color()
        next = None

        for key, value in self._board.get_board().items():
            if value == player_color:
                marble_list.append(key)

            for coord in marble_list:
                # for each coordinate where the player has a marble

                for direction in directions:
                    # check one square in each direction for an empty cell
                    # to push from

                    if direction == 'L':
                        next = (coord[0], coord[1]-1)

                    elif direction == 'R':
                        next = (coord[0], coord[1] + 1)

                    elif direction == 'B':
                        next = (coord[0] + 1, coord[1])

                    elif direction == 'F':
                        next = (coord[0] - 1, coord[1])

                    if self.get_marble(next) == 'X':
                        # if a move is available (an empty spot to 'push from')
                        # check the last spot opposite direction in the column or row
                        # if it is not the player's color,then a move is available
                        # if it is the player's color, then check all the marbles between
                        # the current marble and the end of row or column; if any 'X's, move
                        # is still available

                        if direction == 'L':

                            if self.get_marble((coord[0], 6)) != player_color:

                                return True

                            for col in range(coord[1], 7):
                                if self.get_marble((coord[0], col)) == 'X':

                                    return True

                        elif direction == 'R':

                            if self.get_marble((coord[0], 0)) != player_color:

                                return True

                            for col in range(0, coord[1]+1):

                                if self.get_marble((coord[0], col)) == 'X':
                                    available_move = True
                                    return True

                        elif direction == 'F':

                            if self.get_marble((6, coord[1])) != player_color:

                                return True

                            for row in range(coord[0], 7):
                                if self.get_marble((row, coord[1])) == 'X':

                                    return True

                        elif direction == 'B':

                            if self.get_marble((0, coord[1])) != player_color:

                                return True

                            for row in range(0, coord[0]+1):
                                if self.get_marble((row, coord[1])) == 'X':

                                    return True

        return False

    def update_game_state(self):
        """
        Checks for a win, updates the winner, and
        designates next turn as appropriate
        """
        # update the marble count attributes
        white = 0
        black = 0
        red = 0

        for value in self._board.get_board().values():

            if value == "W":
                white += 1

            elif value == "B":
                black += 1

            elif value == "R":
                red += 1

        self._marble_count = (white, black, red)

        if white == 0 or black == 0:
            # Win State 1: if either are 0, then whoever made
            # current move caused this -> they win
            self._winner = self.get_current_turn()
            # print("The winner is:", self._winner)  # For testing
            #print("The other player has no marbles remaining.")

        elif self._current_turn.get_red_marbles() >= 7:
            # Win State 2: current player has 7 red marbles -> they win
            self._winner = self.get_current_turn()
            # print("The winner is:", self._winner)  # For testing
            #print(self._winner, " has won 7 red marbles!")

        elif self.other_player_move_check() == False:
            # Win State 3: other player cannot make any moves
            # so current player wins
            self._winner = self.get_current_turn()
            # print("The winner is:", self._winner)  # For testing
            #print("Other player cannot make any moves!")

        # change player turn for the next move
        if self.get_current_turn() == self._playerA.get_player_name():
            self.set_current_turn(self._playerB.get_player_name())

        elif self.get_current_turn() == self._playerB.get_player_name():
            self.set_current_turn(self._playerA.get_player_name())

    def get_winner(self):
        """
        Returns the name of the winning player. If no player has won yet,
        it returns None. Note that this does not return the color that
        the player chose
        """
        return self._winner

    def get_captured(self, player_name):
        """
        Takes a player's name and returns the number of Red marbles
        captured by the player. This returns 0 if no marble is captured.
        """
        for player in self._player_list:

            if player_name == player.get_player_name():

                return player.get_red_marbles()

    def get_marble(self, coordinate):
        """
        Takes the coordinates of a cell as a tuple and returns the marble
        that is present at the location. If no marble is present at the
        coordinate location return 'X'
        """
        row = coordinate[0]
        col = coordinate[1]

        if row < 0 or row > 6 or col < 0 or col > 6:
            # sets up the outside of the board to be recognized as
            # moveable (empty space) because you can only move a marble
            # if there is an empty space in the opposite direction from
            # which you are trying to move
            return 'X'

        # returns the value at the location ("R", "W", "B" or "X")
        return self._board.get_marble(coordinate)

    def get_marble_count(self):
        """
        Returns the numer of White marbles, Black marbles
        and Red marbles as tuple in the order (W,B,R).
        """
        return self._marble_count


class Player:
    """
    Player class interacts with KubaGame class in order to provide
    identifying details needed to track game state. These elements are the player
    name (a string), the color of the player's marbles (either "W" or "B"), and
    the number of red marbles ("R") that the player has 'captured' in the
    course of the game. KubaGame updates these attributes in initialization of the
    game, and in the case of the red marbles, during play.

    """

    def __init__(self, player_name, marble_color):
        """
        Takes a player name (string) and marble_color ("W" or "B"), and intitiates
        the Player object.
        """

        self._name = player_name
        self._color = marble_color
        self._red_marbles = 0

    def get_player_name(self):
        """
        Returns player name
        """
        return self._name

    def get_player_color(self):
        """
        Returns player's marble color
        """

        return self._color

    def get_red_marbles(self):
        """
        Returns the count of red marbles that the
        player has captured.
        """

        return self._red_marbles

    def increment_red_marbles(self):
        """
        Adds a red marble to the player's count of red
        marbles that have been won
        """
        self._red_marbles += 1


class Board:
    """
    Implements the board object which is the basis for the Kuba game. The board
    is a 6 x 6 grid which can be populated by one of 4 values: "W" (representing
    white marble), "B" (black marble), "R" (red marble), and "X" (an empty space).

    Board class interacts with the KubaGame class to allow access and adjustment to
    the current state of the board. Board is implemented as a dictionary with key
    lookup by grid-cell tuples: first element is row, second element is column (range
    is (0,0) through (6,6))
    """

    def __init__(self):
        """
        Initiates the game board
        """

        self._board = {
            (0, 0): 'W', (0, 1): 'W', (0, 2): 'X', (0, 3): 'X', (0, 4): 'X', (0, 5): 'B', (0, 6): 'B',
            (1, 0): 'W', (1, 1): 'W', (1, 2): 'X', (1, 3): 'R', (1, 4): 'X', (1, 5): 'B', (1, 6): 'B',
            (2, 0): 'X', (2, 1): 'X', (2, 2): 'R', (2, 3): 'R', (2, 4): 'R', (2, 5): 'X', (2, 6): 'X',
            (3, 0): 'X', (3, 1): 'R', (3, 2): 'R', (3, 3): 'R', (3, 4): 'R', (3, 5): 'R', (3, 6): 'X',
            (4, 0): 'X', (4, 1): 'X', (4, 2): 'R', (4, 3): 'R', (4, 4): 'R', (4, 5): 'X', (4, 6): 'X',
            (5, 0): 'B', (5, 1): 'B', (5, 2): 'X', (5, 3): 'R', (5, 4): 'X', (5, 5): 'W', (5, 6): 'W',
            (6, 0): 'B', (6, 1): 'B', (6, 2): 'X', (6, 3): 'X', (6, 4): 'X', (6, 5): 'W', (6, 6): 'W'
        }

    def get_board(self):
        """
        Returns the game board
        """

        return self._board

    def set_marble(self, coordinate, value):
        """
        Takes a cell coordinate (tuple) and a value (string) and sets the cell (key) to that value
        in the board dictionary
        """
        self._board[coordinate] = value

    def get_marble(self, coordinate):
        """
        Takes a board coordinate tuple (row number, column number) and returns
        the value assigned to that spot on the board ("W", "B", "R" or "X")
        """
        return self._board[coordinate]

    def print_board(self):
        """
        Prints a rough visual of the board updated with its current state.
        """

        # print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(0, 0)], self._board[(0, 1)], self._board[(0, 2)],
               self._board[(0, 3)], self._board[(0, 4)], self._board[(0, 5)],
               self._board[(0, 6)]))
        print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(1, 0)], self._board[(1, 1)], self._board[(1, 2)],
               self._board[(1, 3)], self._board[(1, 4)], self._board[(1, 5)],
               self._board[(1, 6)]))
        print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(2, 0)], self._board[(2, 1)], self._board[(2, 2)],
               self._board[(2, 3)], self._board[(2, 4)], self._board[(2, 5)],
               self._board[(2, 6)]))
        print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(3, 0)], self._board[(3, 1)], self._board[(3, 2)],
               self._board[(3, 3)], self._board[(3, 4)], self._board[(3, 5)],
               self._board[(3, 6)]))
        print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(4, 0)], self._board[(4, 1)], self._board[(4, 2)],
               self._board[(4, 3)], self._board[(4, 4)], self._board[(4, 5)],
               self._board[(4, 6)]))
        print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(5, 0)], self._board[(5, 1)], self._board[(5, 2)],
               self._board[(5, 3)], self._board[(5, 4)], self._board[(5, 5)],
               self._board[(5, 6)]))
        print('-------------------------------------------')
        print('   %s  |  %s  |  %s  |  %s  |  %s  |  %s  |  %s  ' %
              (self._board[(6, 0)], self._board[(6, 1)], self._board[(6, 2)],
               self._board[(6, 3)], self._board[(6, 4)], self._board[(6, 5)],
               self._board[(6, 6)]))
        # print('-------------------------------------------')

        return


if __name__ == "__main__":
    """
    For testing purposes
    """

    game = KubaGame(('PlayerA', 'B'), ('PlayerB', 'W'))
    game.print_board()
    print()

    # Test game
    print(game.make_move('PlayerA', (6, 1), 'F'))
    print(game.make_move('PlayerB', (0, 1), 'B'))
    print(game.make_move('PlayerA', (5, 1), 'F'))
    print(game.make_move('PlayerB', (1, 0), 'R'))
    print(game.make_move('PlayerA', (4, 1), 'F'))
    print(game.make_move('PlayerB', (6, 6), 'F'))
    print(game.make_move('PlayerA', (3, 1), 'R'))
    print(game.make_move('PlayerB', (5, 6), 'F'))
    print(game.make_move('PlayerA', (3, 2), 'R'))
    print(game.make_move('PlayerB', (4, 6), 'F'))
    print(game.make_move('PlayerA', (3, 3), 'R'))
    print(game.make_move('PlayerB', (6, 5), 'F'))
    print(game.make_move('PlayerA', (3, 4), 'R'))
    print(game.make_move('PlayerB', (5, 5), 'F'))
    print(game.make_move('PlayerA', (2, 1), 'R'))
    print(game.make_move('PlayerB', (0, 1), 'B'))
    print(game.make_move('PlayerA', (2, 6), 'L'))
    print(game.make_move('PlayerB', (0, 0), 'B'))
    print(game.make_move('PlayerA', (2, 5), 'L'))
    print(game.make_move('PlayerB', (1, 0), 'B'))
    print(game.make_move('PlayerA', (2, 4), 'L'))
    print(game.make_move('PlayerB', (1, 1), 'B'))
    print(game.make_move('PlayerA', (2, 3), 'L'))
    print(game.make_move('PlayerB', (3, 5), 'R'))
    print(game.make_move('PlayerA', (2, 2), 'L'))
    print(game.make_move('PlayerB', (3, 6), 'B'))
    print(game.make_move('PlayerA', (6, 0), 'F'))
    print(game.make_move('PlayerB', (1, 2), 'R'))
    print(game.make_move('PlayerA', (2, 1), 'B'))
    print(game.make_move('PlayerB', (1, 3), 'R'))
    print(game.make_move('PlayerA', (4, 0), 'R'))
    print(game.make_move('PlayerB', (1, 4), 'R'))
    print(game.make_move('PlayerA', (4, 1), 'R'))
    print(game.make_move('PlayerB', (1, 5), 'R'))
    print(game.make_move('PlayerA', (0, 5), 'B'))
    print(game.make_move('PlayerB', (1, 6), 'L'))
    print(game.make_move('PlayerA', (3, 1), 'F'))
    print(game.make_move('PlayerB', (1, 5), 'F'))
    print(game.make_move('PlayerA', (2, 1), 'L'))
    print(game.make_move('PlayerB', (0, 5), 'R'))
    print(game.make_move('PlayerA', (1, 4), 'R'))
    print(game.make_move('PlayerB', (0, 6), 'L'))
    print(game.make_move('PlayerA', (1, 5), 'F'))

    game.print_board()
    print()
    print(game.get_marble_count())
    print(game.get_current_turn())
    print(game.get_winner())
    print(game._current_turn.get_red_marbles())
    print(game.get_captured("PlayerB"))
    print(game.get_marble((6, 6)))
