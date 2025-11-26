X = "X"
O = "O"
EMPTY = None 

def initial_state():
    """
    Returns starting board: 3x3 grid filled with EMPTY.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]

def player(board):
    """
    Returns player who has the next turn.
    X goes first, then alternate turns.
    """
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count <= o_count else O

def actions(board):
    """
    Returns a set of all possible moves (i, j) on the board.
    """
    moves = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                moves.add((i, j))
    return moves

def result(board, action):
    """
    Returns the board that results from making move (i, j).
    Does not mutate original board. Raises Exception for invalid move.
    """
    if action not in actions(board):
        raise Exception("Invalid move")
    
    new_board = [row.copy() for row in board]
    i, j = action
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game: X, O, or None.
    Checks rows, columns, and diagonals.
    """
    # Rows
    for row in board:
        if row[0] is not None and row[0] == row[1] == row[2]:
            return row[0]
    # Columns
    for j in range(3):
        if board[0][j] is not None and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]
    # Diagonals
    if board[0][0] is not None and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] is not None and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None

def terminal(board):
    """
    Returns True if the game is over (winner or tie), False otherwise.
    """
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def utility(board):
    """
    Returns 1 if X won, -1 if O won, 0 if tie.
    Assumes board is terminal.
    """
    win = winner(board)
    if win == X:
        return 1
    elif win == O:
        return -1
    else:
        return 0

def minimax(board):
    """
    Returns optimal action (i, j) for current player.
    If board is terminal, returns None.
    Uses Minimax algorithm.
    """
    if terminal(board):
        return None

    current_player = player(board)

    def max_value(b):
        if terminal(b):
            return utility(b)
        v = float('-inf')
        for action in actions(b):
            v = max(v, min_value(result(b, action)))
        return v

    def min_value(b):
        if terminal(b):
            return utility(b)
        v = float('inf')
        for action in actions(b):
            v = min(v, max_value(result(b, action)))
        return v

    best_action = None
    if current_player == X:
        best_val = float('-inf')
        for action in actions(board):
            val = min_value(result(board, action))
            if val > best_val:
                best_val = val
                best_action = action
    else:
        best_val = float('inf')
        for action in actions(board):
            val = max_value(result(board, action))
            if val < best_val:
                best_val = val
                best_action = action

    return best_action
