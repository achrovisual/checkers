from math import inf

import shared_variables


# Create global history table dictionary
HISTORY_TABLE = {}


# This function updates move history key with score. Creates new key if not yet present.
def update_history(move, depth):
    # Get the hash of the utility object.
    key = hash(move)

    # Get the score of the key. It uses 0 if key is not present.
    score = HISTORY_TABLE.get(key, 0)

    # Add the square of the depth to the current score.
    # Reference used, https://www.chessprogramming.org/History_Heuristic.
    HISTORY_TABLE[key] = score + 2 ** depth


# This function sorts the move list using the scores.
def sort_by_history_heuristic(moves):
    # Initialize variables.
    global HISTORY_TABLE
    scores = []

    # Iterate through the move list and get the score from HISTORY_TABLE. If not found, use 0.
    for move in moves:
        key = hash(move)
        if key in HISTORY_TABLE:
            scores.append(HISTORY_TABLE[key])
        else:
            scores.append(0)

    # Sort the move list using the score list and return it.
    return [x for _, x in sorted(zip(scores, moves))]


# This function is the implementation of Minimax with Alpha-Beta Pruning.
# If heuristic variable is set to "HISTORY", it will perform move ordering using History Heuristics.
# Otherwise, it will not perform move ordering.
def alpha_beta(position, depth, alpha, beta, max_player, heuristic):
    # Initialize variables.
    global HISTORY_TABLE
    shared_variables.NODE_COUNTER += 1

    # Check if at depth 0 or if current state is game over.
    if depth == 0 or position.get_game_end():
        return position.evaluate_state()

    # Get possible moves.
    moves = position.get_next_moves()
    best_move = None

    # Perform Minimax with Alpha-Beta Pruning and Move Ordering via History Heuristics.
    if heuristic == 'HISTORY':
        # Sort the move list.
        moves = sort_by_history_heuristic(moves)

        # Initialize variable.
        max_evaluation = -inf

        # Iterate through the move list.
        for child in moves:
            # Increment node counter.
            shared_variables.NODE_COUNTER += 1

            # If move hasn't been done, append to cache.
            if hash(child) not in shared_variables.CACHE:
                shared_variables.CACHE.append(hash(child))

            # Recursive call.
            evaluation = alpha_beta(child, depth - 1, -alpha, -beta, None, heuristic)
            max_evaluation = max(max_evaluation, evaluation)

            # Get max value between max_evaluation and evaluation. Update best move afterwards.
            if max_evaluation < evaluation:
                max_evaluation = evaluation
                best_move = child

            # Remove move object from cache if alpha is less than max_evaluation.
            if max_evaluation > alpha:
                shared_variables.CACHE.remove(hash(child))

            # This is the Alpha-Beta cutoff. Increment counter cutoff counter.
            if beta <= alpha:
                shared_variables.CUTOFF_COUNTER += 1
                break

        # Update move evaluation.
        position.set_evaluation(max_evaluation)

        # Update history table.
        update_history(best_move, depth)

        # Return the evaluation of the move.
        return max_evaluation

    # Perform Minimax with Alpha-Beta Pruning.
    else:
        if max_player:
            # Initialize variable.
            max_evaluation = -inf

            for child in moves:
                # Increment node counter.
                shared_variables.NODE_COUNTER += 1

                # If move hasn't been done, append to cache.
                if hash(child) not in shared_variables.CACHE:
                    shared_variables.CACHE.append(hash(child))

                # Recursive call.
                evaluation = alpha_beta(child, depth - 1, alpha, beta, False, heuristic)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)

                # This is the Alpha-Beta cutoff. Increment counter cutoff counter.
                if beta <= alpha:
                    shared_variables.CUTOFF_COUNTER += 1
                    break

            # Update move evaluation.
            position.set_evaluation(max_evaluation)

            # Return the evaluation of the move.
            return max_evaluation
        else:
            # Initialize variable.
            min_evaluation = inf

            for child in moves:
                # Increment node counter.
                shared_variables.NODE_COUNTER += 1

                # If move hasn't been done, append to cache.
                if hash(child) not in shared_variables.CACHE:
                    shared_variables.CACHE.append(hash(child))

                # Recursive call.
                evaluation = alpha_beta(child, depth - 1, alpha, beta, True, heuristic)
                min_evaluation = min(min_evaluation, evaluation)
                beta = min(beta, evaluation)

                # This is the Alpha-Beta cutoff. Increment counter cutoff counter.
                if beta <= alpha:
                    shared_variables.CUTOFF_COUNTER += 1
                    break

            # Update move evaluation.
            position.set_evaluation(min_evaluation)

            # Return the evaluation of the move.
            return min_evaluation
