"""
Tic Tac Toe Player. 
This contains all of the logic for playing the game and for
making optimal moves.
"""

import math

# variables that represent the posible values of the board
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board. The board is represented as a list of 3
    lists, where each internal list contains 3 values (either X, O, or EMPTY).
    In the initial state all the values are EMPTY.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    INPUT:   - board: list of lists representing the state of the board
    RETURNS: - X/O: the player who has the next turn
    """
    if board == terminal(board):
        return "The game is over"
    
    if board == initial_state():
        return X
        # the first player will always be X
    else:
        # For knowing who is the next player we need to count the number of X and O in the board
        x_count = sum([row.count(X) for row in board])
        o_count = sum([row.count(O) for row in board])
        if x_count > o_count:
            return O
        else:
            return X
    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    i corresponds to the row of the move (0, 1, 2) and j corresponds to the cell in the row (0, 1, 2)
    INPUT:   - board: list of lists representing the state of the board
    RETURNS: - set of tuples: set of all possible actions (i, j) available on the board. 
                              Available actions are the cells that are empty
    """
    if board == terminal(board):
        return "The game is over"
    
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions
   

def result(board, action):
    """
    Returns a new board state that results from making move (i, j) on the board without modifing the
    original board.
    INPUT:   - board: list of lists representing the state of the board
             - action: tuple representing the move (i, j) to be made
    RETURNS: - new_board: the board that results from making move (i, j) on the board
    """
    if action not in actions(board):
        raise Exception("The action is not valid")
    else:
        new_board = [row.copy() for row in board]
        new_board[action[0]][action[1]] = player(board)
        return new_board
   
def winner(board):
    """
    Returns the winner of the game, if there is one. One can win the game by having a row, column or diagonal
    filled with the same value (X or O). There will be one or no winner.
    INPUT:   - board: list of lists representing the state of the board
    RETURNS: - X/O/None: the winner of the game, if there is one. If there is no winner, it returns None
    """
    # Check rows
    for row in board:
        if row.count(X) == 3:
            return X
        elif row.count(O) == 3:
            return O
    
    # Check columns
    for j in range(3):
        if board[0][j] == board[1][j] == board[2][j] == X:
            return X
        elif board[0][j] == board[1][j] == board[2][j] == O:
            return O
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] == X:
        return X
    elif board[0][0] == board[1][1] == board[2][2] == O:
        return O
    elif board[0][2] == board[1][1] == board[2][0] == X:
        return X
    elif board[0][2] == board[1][1] == board[2][0] == O:
        return O
    
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise. The game is over when all the cells are filled or there
    is a winner.
    INPUT:   - board: list of lists representing the state of the board
    RETURNS: - True/False: True if game is over, False otherwise
    """
    if winner(board) is not None:
        return True
    elif all([cell != EMPTY for row in board for cell in row]):
        return True
    else:
        return False


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    INPUT:   - board: list of lists representing the state of the board
    RETURNS: - 1/-1/0: the utility of the board
    """
    if terminal(board) == True:
        if winner(board) == X:
            return 1
        elif winner(board) == O:
            return -1
        else:
            return 0
    

def minimax(board):
    """
    Returns the optimal action for the current player on the board. If many actions have the same value, any
    of them can be returned. If the game is over, it returns None.

    The player X will try to maximize the value of the board, while the player O will try to minimize it.

    INPUT:   - board: list of lists representing the state of the board
    RETURNS: - tuple: the optimal action for the current player on the board
             - None: if the game is over
    """
    def max_val(board):
        value = float("-inf") # we start with the minimun value possible because we want to maximize it
        if terminal(board):
            return utility(board)
        for action in actions(board):
            value = max(value, min_val(result(board,action)))
        return value
    
    def min_val(board):
        value = float("inf")
        if terminal(board):
            return utility(board)
        for action in actions(board):
            value = min(value, max_val(result(board,action)))
        return value
    
    #the maximazing player picks an action that produces the highest value of Min-Value
    if player(board) == X:
        value = float("-inf")
        for action in actions(board):
            new_value = min_val(result(board, action))
            if new_value > value:
                value = new_value
                optimal_action = action
        return optimal_action
    #the minimizing player picks an action that produces the lowest value of Max-Value
    else:
        value = float("inf")
        for action in actions(board):
            new_value = max_val(result(board, action))
            if new_value < value:
                value = new_value
                optimal_action = action
        return optimal_action
    