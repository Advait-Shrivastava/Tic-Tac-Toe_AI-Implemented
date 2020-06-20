"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count_X = 0
    count_O = 0

    for i in board:
        for j in i:
            if j == "X":
                count_X+=1
            elif j == "O":
                count_O+=1    
    if count_X>count_O:
        return O

    elif terminal(board) == False and count_X == count_O:
        return X

    else:
        return None        


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    result = set()

    for i in range(3):
        for j in range(3):
            if(board[i][j] == EMPTY):
                result.add((i,j))

    return result            


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    if terminal(board):
        raise ValueError("Game Over")

    
    elif action not in actions(board):
        raise ValueError("Invalid Action")

    else:
        p = player(board)
        result_board = copy.deepcopy(board)
        (i,j) = action
        result_board[i][j] = p

    return result_board    

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != None:
            if board[i][0] == X:
                return X
            else:
                return O

    for i in range(3):          
        if board[0][i] == board[1][i] == board[2][i] != None:
            if board[0][i] == X:
                return X
            else:
                return O

    if board[0][0] == board[1][1] == board[2][2] != None:
        if board[0][0] == X:
            return X
        else:
            return O

    elif board[0][2] == board[1][1] == board[2][0] != None:
        if board[0][2] == X:
            return X
        else:
            return O

    else:
        return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board) != None:
        return True
        
    for i in board:
        for j in i:
            if j == EMPTY:
                return False

    return True            


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """

    who_won = winner(board)

    if who_won == X:
        return 1

    elif who_won == O:
        return -1

    else:
        return 0



def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    
    p = player(board)

    if board == [[EMPTY]*3]*3:
        return(0,0)


    if p == X:
        least_val = float("-inf")

        chosen_action = None

        for action in actions(board):
            min_val_result = minVal(result(board,action))

            if min_val_result > least_val:
                least_val = min_val_result 
                chosen_action = action


    if p == O:
        max_val = float("inf")

        chosen_action = None

        for action in actions(board):
            max_val_result = maxVal(result(board,action))

            if max_val_result < max_val:
                max_val = max_val_result 
                chosen_action = action


    return chosen_action            


def maxVal(board):
    if terminal(board):
        return utility(board)

    least_val = float("-inf")

    for action in actions(board):
        least_val = max(least_val,minVal(result(board,action)))


    return least_val


def minVal(board):
    if terminal(board):
        return utility(board)

    max_val = float("inf")

    for action in actions(board):
        max_val = min(max_val,maxVal(result(board,action)))


    return max_val
