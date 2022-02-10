"""
Minimax Tic-Tac-Toe Player
(Play Tic-Tac-Toe against the computer)

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import poc_ttt_gui
import poc_ttt_provided as provided
#import user47_JKOUZKANWx_15 as test_suite

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    winner = board.check_win()
    if winner != None:
        return SCORES[winner], (-1, -1)

    best_move = (-SCORES[player], (-1, -1))
    for square in board.get_empty_squares():
        child_board = board.clone()
        child_board.move(square[0], square[1], player)
        if child_board.check_win() == player:
            return (SCORES[player], square)

        response_move = mm_move(child_board, provided.switch_player(player))
        if response_move[0] * SCORES[player] >= best_move[0] * SCORES[player]:
            best_move = (response_move[0], square)

    return best_move
        

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]


# Test game with the console or the GUI;
# uncomment whichever you prefer.

#provided.play_game(move_wrapper, 1, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)


# TESTING#####################################################
#test_suite.run_suite_mm_move(mm_move)

