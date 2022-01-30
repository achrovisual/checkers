from copy import deepcopy
from math import inf


# This class represents a state. It
class State(object):
    # This is a constructor. It initializes object variables.
    def __init__(self, table, turn = True):
        self.table = table
        self.next_moves = None
        self.game_over = False
        self.turn = turn
        self.evaluation = 0

    # This overloads the greater than operator for comparing State objects.
    def __gt__(self, other):
        return self.evaluation > other.get_evaluation()

    # This overloads the greater than or equal to operator for comparing State objects.
    def __ge__(self, other):
        return self.evaluation >= other.get_evaluation()

    # This overloads the less than operator for comparing State objects.
    def __lt__(self, other):
        return self.evaluation < other.get_evaluation()

    # This overloads the less than or equal to operator for comparing State objects.
    def __le__(self, other):
        return self.evaluation <= other.get_evaluation()

    # This overloads the equal operator for comparing State objects.
    def __eq__(self, other):
        return self.evaluation == other.get_evaluation()

    # This overloads the hash function for State objects.
    def __hash__(self):
        return id(self)

    # This returns the game over flag.
    def get_game_end(self):
        return self.game_over

    # This updates the turn boolean flag.
    def set_turn(self, value):
        self.turn = value

    # This returns the turn boolean flag.
    def get_turn(self):
        return self.turn

    # This updates the state evaluation to the given parameter.
    def set_evaluation(self, value):
        self.evaluation = value

    # This returns the state evaluation.
    def get_evaluation(self):
        return self.evaluation

    # This returns the state's next moves.
    def get_next_moves(self):
        if self.next_moves is None:
            self.generate_next_moves()
        return self.next_moves

    # This returns the table.
    def get_table(self):
        return self.table

    # This counts the pieces of each player on the board.
    def count_pieces(self):
        # Initialize variables.
        p1_counter = 0
        p2_counter = 0

        # Iterate through the board and count the pieces.
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if self.table[i][j] == 'x':
                    p1_counter += 1
                if self.table[i][j] == 'X':
                    p1_counter += 1
                if self.table[i][j] == 'o':
                    p2_counter += 1
                if self.table[i][j] == 'O':
                    p2_counter += 1

        # Return the counters.
        return p1_counter, p2_counter

    # This function finds the move that was done.
    def find_move_played(self, previous):
        # Initialize variable.
        move = []

        # Iterate through the board and append the move done to the list.
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if self.table[i][j] != previous[i][j]:
                    move.append((i, j))

        # Return move list.
        return move

    # This function finds capturing moves.
    def find_capturing_moves(self):
        # Initialize variable.
        moves = []

        # Iterate through the board and find moves that can capture opponent's pieces.
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                if self.turn and (self.table[i][j] == 'x' or self.table[i][j] == 'X'):
                    move = self.find_valid_moves_for_piece((i, j))
                    for temp in move:
                        if i - temp[0] == 2 or i - temp[0] == -2:
                            moves.append((i, j))
                            break
                if not self.turn and (self.table[i][j] == 'o' or self.table[i][j] == 'O'):
                    move = self.find_valid_moves_for_piece((i, j))
                    for temp in move:
                        if i - temp[0] == 2 or i - temp[0] == -2:
                            moves.append((i, j))
                            break

        # Return move list.
        return moves

    # This function evaluates the state. Essentially, this is the utility function.
    # It implements the Control the Center Strategy, where AI will favor center positions.
    # Reference used, https://hobbylark.com/board-games/Checkers-Strategy-Tactics-How-To-Win.
    def evaluate_state(self):
        # Initialize variables.
        p1_score = 0
        p2_score = 0
        p1_counter = 0
        p2_counter = 0

        # Iterate through the board and update the scores.
        for i in range(len(self.table)):
            for j in range(len(self.table[i])):
                # Increment score if pawn.
                if self.table[i][j] == 'x':
                    # Increment piece counter.
                    p1_counter += 1

                    # Increment scores. Favor center positions more.
                    if 2 < i < 5 and 1 < j < 6:
                        p1_score += 50
                    elif i < 4:
                        p1_score += 45
                    else:
                        p1_score += 40

                # Increment score if king.
                if self.table[i][j] == 'X':
                    # Increment piece counter.
                    p1_counter += 1
                    # Increment score.
                    p1_score += 60

                # Increment score if pawn.
                if self.table[i][j] == 'o':
                    # Increment piece counter.
                    p2_counter += 1

                    # Increment scores. Favor center positions more.
                    if 2 < i < 5 and 1 < j < 6:
                        p2_score += 50
                    elif i > 3:
                        p2_score += 45
                    else:
                        p2_score += 40

                # Increment score if king.
                if self.table[i][j] == 'O':
                    # Increment piece counter.
                    p2_counter += 1
                    # Increment score.
                    p2_score += 60

        # Get the difference of the two scores.
        self.evaluation = p2_score - p1_score

        # If counter has no more pieces, game is over.
        if p1_counter == 0:
            self.evaluation = inf
            self.game_over = True

        # If counter has no more pieces, game is over.
        if p2_counter == 0:
            self.evaluation = -inf
            self.game_over = True

        # Return heuristic value.
        return self.evaluation

    # This function generates possible moves.
    def generate_next_moves(self):
            # initialize variables.
            self.next_moves = []
            captures = []
            all_moves = []

            # Iterate through the board and look for valid moves.
            for i in range(len(self.table)):
                for j in range(len(self.table[i])):
                    if self.turn:
                        # If valid piece, look for valid moves.
                        if self.table[i][j] == "x" or self.table[i][j] == "X":
                            valid_moves = self.find_valid_moves_for_piece((i, j))
                            for move in valid_moves:
                                # Append capturing move to list.
                                if move[0] - i == 2 or move[0] - i == -2:
                                    new_table = self.generate_new_state((i, j), move)
                                    position = State(new_table, not self.turn)
                                    captures.append(position)
                                # Append non-capturing move to list.
                                else:
                                    new_table = self.generate_new_state((i, j), move)
                                    position = State(new_table, not self.turn)
                                    all_moves.append(position)

                    else:
                        # If valid piece, look for valid moves.
                        if self.table[i][j] == "o" or self.table[i][j] == "O":
                            valid_moves = self.find_valid_moves_for_piece((i, j))
                            for move in valid_moves:
                                # Append capturing move to list.
                                if move[0] - i == 2 or move[0] - i == -2:
                                    new_table = self.generate_new_state((i, j), move)
                                    position = State(new_table, not self.turn)
                                    captures.append(position)
                                else:
                                # Append non-capturing move to list.
                                    new_table = self.generate_new_state((i, j), move)
                                    position = State(new_table, not self.turn)
                                    all_moves.append(position)

            # Set next moves to captures if it's not empty. Otherwise, set next moves to non-capturing moves.
            if len(captures) > 0:
                self.next_moves = captures
            else:
                self.next_moves = captures + all_moves

    # This function generates a new state with the piece to move.
    def generate_new_state(self, piece, move):
        # Initialize variables.
        table_copy = deepcopy(self.table)
        piece_type = table_copy[piece[0]][piece[1]]

        # This moves the piece. It promotes the piece to king.
        if piece_type == "x" or piece_type == "X":
            if move[0] == 0:
                table_copy[piece[0]][piece[1]] = "X"
            if piece[0] - move[0] == 2 or piece[0] - move[0] == -2:
                row = piece[0] + (move[0] - piece[0]) // 2
                column = piece[1] + (move[1] - piece[1]) // 2
                table_copy[row][column] = "-"

        # This moves the piece. It promotes the piece to king.
        if piece_type == "o" or piece_type == "O":
            if move[0] == 7:
                table_copy[piece[0]][piece[1]] = "O"
            if piece[0] - move[0] == 2 or piece[0] - move[0] == -2:
                row = piece[0] + (move[0] - piece[0]) // 2
                column = piece[1] + (move[1] - piece[1]) // 2
                table_copy[row][column] = "-"

        table_copy[piece[0]][piece[1]], table_copy[move[0]][move[1]] = table_copy[move[0]][move[1]], \
            table_copy[piece[0]][piece[1]]

        # Return state.
        return table_copy

    # This function performs the move.
    def play_move(self, piece, move):
        # Initialize variables.
        table = self.generate_new_state(piece, move)
        position = None

        # Iterate through valid states and find same table within the states.
        for state in self.get_next_moves():
            if table == state.get_table():
                position = state
                break

        # Return the move.
        return position

    # This function looks for valid moves.
    def find_valid_moves_for_piece(self, coordinates):
        # Initialize variables.
        captures = []
        valid_moves = []
        piece = self.table[coordinates[0]][coordinates[1]]

        # Look for player moves.
        if piece != "x":
            if 0 <= coordinates[0] < 7:
                # Search left side of the piece.
                if (coordinates[1] - 1) >= 0:
                    # Search for non-capturing moves.
                    if self.table[coordinates[0] + 1][coordinates[1] - 1] == '-':
                        valid_moves.append((coordinates[0] + 1, coordinates[1] - 1))
                    # Search for capture moves.
                    elif coordinates[0] + 2 < 8 and coordinates[1] - 2 >= 0:
                        if self.table[coordinates[0] + 2][coordinates[1] - 2] == '-':
                            if piece.lower() != self.table[coordinates[0] + 1][coordinates[1] - 1].lower():
                                captures.append((coordinates[0] + 2, coordinates[1] - 2))

                # Search right side of the piece.
                if (coordinates[1] + 1) < 8:
                    # Search for non-capturing moves.
                    if self.table[coordinates[0] + 1][coordinates[1] + 1] == '-':
                        valid_moves.append((coordinates[0] + 1, coordinates[1] + 1))
                    # Search for capture moves.
                    elif coordinates[0] + 2 < 8 and coordinates[1] + 2 < 8:
                        if self.table[coordinates[0] + 2][coordinates[1] + 2] == '-':
                            if piece.lower() != self.table[coordinates[0] + 1][coordinates[1] + 1].lower():
                                captures.append((coordinates[0] + 2, coordinates[1] + 2))
        # Look for AI moves.
        if piece != "o":
            if 0 < coordinates[0] < 8:
                # Search left side of the piece.
                if (coordinates[1] - 1) >= 0:
                    # Search for non-capturing moves.
                    if self.table[coordinates[0] - 1][coordinates[1] - 1] == '-':
                        valid_moves.append((coordinates[0] - 1, coordinates[1] - 1))
                    # Search for capture moves.
                    elif coordinates[0] - 2 >= 0 and coordinates[1] - 2 >= 0:
                        if self.table[coordinates[0] - 2][coordinates[1] - 2] == '-':
                            if piece.lower() != self.table[coordinates[0] - 1][coordinates[1] - 1].lower():
                                captures.append((coordinates[0] - 2, coordinates[1] - 2))

                # Search right side of the piece.
                if (coordinates[1] + 1) < 8:
                    # Search for non-capturing moves.
                    if self.table[coordinates[0] - 1][coordinates[1] + 1] == '-':
                        valid_moves.append((coordinates[0] - 1, coordinates[1] + 1))
                    # Search for capture moves.
                    elif coordinates[0] - 2 >= 0 and coordinates[1] + 2 < 8:
                        if self.table[coordinates[0] - 2][coordinates[1] + 2] == '-':
                            if piece.lower() != self.table[coordinates[0] - 1][coordinates[1] + 1].lower():
                                captures.append((coordinates[0] - 2, coordinates[1] + 2))

        # Capturing moves list is not empty, return the list.
        if len(captures) != 0:
            return captures

        # Otherwise, return all moves.
        return captures + valid_moves
