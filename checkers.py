from os import system
from math import inf
from time import time, sleep
from copy import deepcopy

import shared_variables
from helper import *
from ai import *
from state import State


# This function evaluates the current state and checks if it reached the game over state.
# The game over condition is where one of the players has no more pieces to move.
def game_over(position):
    moves = position.get_next_moves()
    piece_counter = position.count_pieces()

    # If player pieces is zero, AI has won.
    if piece_counter[0] == 0:
        print("AI won!")
        return True

    # If AI pieces is zero, player has won.
    if piece_counter[1] == 0:
        print("You won!")
        return True

    # If current player has no more moves, the game is over.
    if not moves:
        print("There are no possible moves left! Game over!")
        return True

    return False


# This function creates an 8x8 board with the checkers pieces placed. o is the AI, and x is the player.
# O and X are promoted pieces.
def initialize_board():
    board = []
    for row in range(8):
        board.append([])
        for column in range(8):
            if column % 2 == ((row + 1) % 2):
                if row < 3:
                    board[row].append('o')
                elif row > 4:
                    board[row].append('x')
                else:
                    board[row].append('-')
            else:
                board[row].append('-')
    return board


# This function starts the game. It begins with the player's turn, followed by the AI.
def main():
    # Initialize variables.
    board = initialize_board()
    position = State(board, True)
    time_previous_move = 0

    # Acquire parameters from shared_variables.
    depth = shared_variables.DEPTH
    move_ordering = shared_variables.HEURISTIC

    # Start game.
    # Loops until game over condition is met.
    while True:
        # Check if game is over.
        if game_over(position):
            break

        # Get pieces that can capture.
        available_pieces = position.find_capturing_moves()

        # Print board.
        print_table(position.get_table(), available_pieces)

        # Choose a piece to move.
        piece = choose_piece(position, available_pieces)

        # Get the valid moves of the chosen piece.
        valid_moves = position.find_valid_moves_for_piece(piece)

        # Print board with valid moves of chosen piece.
        print_table(position.get_table(), piece, valid_moves)

        # Choose which position to go to.
        new_position = choose_field(valid_moves)

        # Copy current state (before player move) for printing.
        previous_table = deepcopy(position.get_table())

        # Perform move.
        position = position.play_move(piece, new_position)

        # Print board with player move.
        differences = position.find_move_played(previous_table)
        print_table(position.get_table(), differences)
        print("User played the move displayed on the table above.")
        sleep(1.5)

        # Check if game is over after player move.
        if game_over(position):
            break

        # Copy current state (before AI move) for printing.
        previous_table = deepcopy(position.get_table())

        # Get start time (right before AI move).
        start_time = time()

        # Perform AI algorithm.
        alpha_beta(position, depth, -inf, inf, True, move_ordering)

        # Perform move.
        position = max(position.get_next_moves())

        # Get end time (right after AI move).
        end_time = time()

        # Compute AI search and move time.
        time_elapsed = end_time - start_time

        # Add search time to shared_variables time variable.
        shared_variables.TIME += time_elapsed

        # Print board with AI move.
        differences = position.find_move_played(previous_table)
        print_table(position.get_table(), differences)
        print("Computer played a move displayed on the table above.")
        sleep(1.5)

# This is the main function.
# It will run the main program and will terminate when Control + C is pressed.
if __name__ == '__main__':
    try:
        # Start main program.
        main()
    except KeyboardInterrupt:
        # Print parameters and metrics.
        system('clear')
        print("Move ordering: " + shared_variables.HEURISTIC)
        print("Depth: " + str(shared_variables.DEPTH))
        print("Nodes: " + str(shared_variables.NODE_COUNTER))
        print("Cutoffs: " + str(shared_variables.CUTOFF_COUNTER))
        print("Search time: " + str(shared_variables.TIME))

        # Terminate program.
        exit()
