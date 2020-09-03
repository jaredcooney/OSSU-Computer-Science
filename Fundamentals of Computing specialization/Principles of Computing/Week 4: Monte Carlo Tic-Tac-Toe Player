"""
Monte Carlo Tic-Tac-Toe Player

Student: Jared Cooney
jaredcooney2@gmail.com

Runs in CodeSkulptor (Python 2)
codeskulptor.org
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided
#import user47_lk3kavkuTy_13 as test_suite

# Constants for Monte Carlo simulator (**do not change their names)
NTRIALS = 1000         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
DIM = 3

def mc_trial(board, player):
    """Randomly plays out the rest of a Tic-Tac-Toe game given an initial board"""
    current_player = player
    while board.check_win() == None:
        rand_square = random.choice(board.get_empty_squares())
        board.move(rand_square[0], rand_square[1], current_player)
        current_player = provided.switch_player(current_player)

def mc_update_scores(scores, board, player):
    """Updates scores list given results of a Tic-Tac-Toe trial game"""
    flip = 0
    winner = board.check_win()
    if winner == player:
        flip = 1
    elif winner == provided.switch_player(player):
        flip = -1
        
    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == player:
                scores[row][col] += SCORE_CURRENT * flip
            elif board.square(row, col) == provided.switch_player(player):
                scores[row][col] -= SCORE_OTHER * flip
    
def get_best_move(board, scores):
    """Returns optimal Tic-Tac-Toe move as tuple given predetermined scores for each square"""
    max_score = -NTRIALS * max(SCORE_CURRENT, SCORE_OTHER)
    best_list = board.get_empty_squares()
    if len(best_list) == 0:
        print "Error: no open squares"
        return
    for square in best_list:
        if scores[square[0]][square[1]] > max_score:
            max_score = scores[square[0]][square[1]]
    for square in list(best_list):
        if scores[square[0]][square[1]] < max_score:
            best_list.remove(square)
    return random.choice(best_list)

def mc_move(board, player, trials):
    """Runs Monte Carlo trials and returns the optimal Tic-Tac-Toe move as a tuple"""
    scores = [[0 for dummy_i in range(board.get_dim())] for dummy_j in range(board.get_dim())]
    for dummy_var in range(trials):
        trial_board = board.clone()
        mc_trial(trial_board, player)
        mc_update_scores(scores, trial_board, player)
    return get_best_move(board, scores)



# Test game with the console or the GUI;
# uncomment whichever you prefer.

#provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(DIM, provided.PLAYERX, mc_move, NTRIALS, False)


# TESTING BELOW ###################################################
#provided.EMPTY = 1
#provided.PLAYERX = 2
#provided.PLAYERO = 3 
#provided.DRAW = 4

#test_suite.run_suite_mc_trial(mc_trial)
#test_suite.run_suite_mc_update_scores(mc_update_scores)
#test_suite.run_suite_get_best_move(get_best_move)
#test_suite.run_suite_mc_move(mc_move)
