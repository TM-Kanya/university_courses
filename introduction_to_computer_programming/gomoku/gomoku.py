"""
Gomoku- with  incomplete functions completed by Tanvi Manku

Authors: Michael Guerzhoy (starter code), Siavash Kazemian (testing), Tanvi Manku (completed functions).

Hello, world!
"""

def is_empty(board):
    """
    Purpose:
    - Check if the game board is empty (i.e., no stones have been placed on it)

    Parameters:
    - board -- the game board

    Returns:
    - Boolean
    - True if the board is empty, False if it is not

    Assumes:
    - Only black and white pieces can be placed on the board
    """

    for row in board:
        if "b" in row or "w" in row:
            return False

    return True

def check_edge(board, edge_y, edge_x):
    """
    Purpose:
    - Check if a pair of coordinates is "out-of-bounds" (i.e., is an invalid pair of coordinates for the board) or is occupied by a stone

    Parameters:
    - board -- the game board
    - edge_y -- the y-coordinate of the pair of coordinates to be checked
    - edge_x -- the x-coordinate of the pair of coordinates to be checked

    Returns:
    - Integer
    - 0 if the square is out-of-bounds or occupied, 1 if the square is empty

    Assumes:
    - The board is an 8 by 8 board
    """

    if edge_y < 0 or edge_y > 7 or edge_x < 0 or edge_x > 7:
        return 0
    elif board[edge_y][edge_x] != " ":
        return 0
    else:
        return 1

def is_bounded(board, y_end, x_end, length, d_y, d_x):
    """
    Purpose:
    - Check if a sequence is open, semiopen, or closed

    Parameters:
    - board -- the game board
    - y_end -- the y-coordinate of the last square in the sequence to be checked
    - x_end -- the x-coordinate of the last square in the sequence to be checked
    - d_y -- the y-direction of the sequence to be checked
    - d_x -- the x-direction of the sequence to be checked

    Returns:
    - String
    - "CLOSED" if the sequence is closed, "SEMIOPEN" if the sequence is semiopen, "OPEN" if the sequence is open

    Assumes:
    - The given sequence is a complete sequence (not a subsequence)
    - The sequence lies in the board
    - The given sequence only contains stones of one color
    """

    # Finding the two "edges" of the sequence (i.e., the squares right before and right after the sequence
    edge1 = (y_end + d_y, x_end + d_x)
    edge2 = (y_end - length * d_y, x_end - length * d_x)

    # Using check_edge() to see if the sequence is closed, semiopen, or open
    check_state = check_edge(board, edge1[0], edge1[1]) + check_edge(board, edge2[0], edge2[1])

    if check_state == 0:
        return "CLOSED"
    elif check_state == 2:
        return "OPEN"
    else:
        return "SEMIOPEN"

def get_all_states(board, col, y_start, x_start, length, d_y, d_x):
    """
    Purpose:
    - Find the total number of open, semiopen, and closed sequences of a specific color, length, and direction in a row

    Parameters:
    - board -- the game board
    - col -- the color of the sequences to be checked
    - y_start -- the y-coordinate of the start of the row to be checked
    - x_start -- the x-coordinate of the start of the row to be checked
    - length -- the length of the sequences to be checked
    - d_y -- the y-direction of the row to be checked
    - d_x -- the x-direction of the row to be checked

    Returns:
    - Tuple of integers
    - (number of open sequences, number of semiopen sequences, number of closed sequences)

    Assumes:
    - The starting coordinates are at the edge of the board
    - Length is an integer greater than or equal to 2
    - The row lies in the board
    - Only complete sequences count (i.e., a row with _ _ b b b _ _ _ contains only one row of 3 blacks, not any other sequences)
    """

    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    running = True

    sequence = []

    pos_x = x_start
    pos_y = y_start

    while running == True:
        chip = board[pos_y][pos_x]

        if chip == col:
            sequence.append((pos_y, pos_x))

        elif chip != col:
            if len(sequence) == length:

                bound_state = is_bounded(board, sequence[-1][0], sequence[-1][1], length, d_y, d_x)

                if bound_state == "SEMIOPEN":
                    semi_open_seq_count += 1
                elif bound_state == "OPEN":
                    open_seq_count += 1
                elif bound_state == "CLOSED":
                    closed_seq_count += 1

            sequence = []

        pos_y += d_y
        pos_x += d_x

        if pos_y > 7 or pos_x > 7 or pos_y < 0 or pos_x < 0:
            if len(sequence) == length:
                bound_state = is_bounded(board, sequence[-1][0], sequence[-1][1], length, d_y, d_x)
                if bound_state == "SEMIOPEN":
                    semi_open_seq_count += 1
                elif bound_state == "OPEN":
                    open_seq_count += 1
                elif bound_state == "CLOSED":
                    closed_seq_count += 1

            running = False

    res = (open_seq_count, semi_open_seq_count, closed_seq_count)

    return res

def board_get_all_states(board, col, length):
    """
    Purpose:
    - Find the total number of open, semiopen, and closed sequences of a specific color and length in the entire board

    Parameters:
    - board -- the game board
    - col -- the color of the sequences to be checked
    - length -- the length of the sequences to be checked

    Returns:
    - Tuple of integers
    - (number of open sequences, number of semiopen sequences, number of closed sequences)

    Assumes:
    - Length is an integer greater than or equal to 2
    - Only complete sequences count (i.e., a row with _ _ b b b _ _ _ contains only one row of 3 blacks, not any other sequences)
    """

    open_seq_count = 0
    semi_open_seq_count = 0
    closed_seq_count = 0

    # Go through different starting positions to detect sequences
    # This will go through all starting positions for directions (0, 1) and (1, 0) and half of the starting positions for directions (1, 1) and (1, -1)
    for i in range(0, 8):
        add_vert = get_all_states(board, col, 0, i, length, 1, 0)
        open_seq_count += add_vert[0]
        semi_open_seq_count += add_vert[1]
        closed_seq_count += add_vert[2]

        add_hori = get_all_states(board, col, i, 0, length, 0, 1)
        open_seq_count += add_hori[0]
        semi_open_seq_count += add_hori[1]
        closed_seq_count += add_hori[2]

        add_dia_1_1 = get_all_states(board, col, 0, i, length, 1, 1)
        open_seq_count += add_dia_1_1[0]
        semi_open_seq_count += add_dia_1_1[1]
        closed_seq_count += add_dia_1_1[2]

        add_dia_2_1 = get_all_states(board, col, 0, i, length, 1, -1)
        open_seq_count += add_dia_2_1[0]
        semi_open_seq_count += add_dia_2_1[1]
        closed_seq_count += add_dia_2_1[2]


    # Go through the remaining starting positions for directions (1, 1) and (1, -1)
    for j in range(1, 8):
        add_dia_1_2 = get_all_states(board, col, j, 0, length, 1, 1)
        open_seq_count += add_dia_1_2[0]
        semi_open_seq_count += add_dia_1_2[1]
        closed_seq_count += add_dia_1_2[2]

        add_dia_2_2 = get_all_states(board, col, j, 7, length, 1, -1)
        open_seq_count += add_dia_2_2[0]
        semi_open_seq_count += add_dia_2_2[1]
        closed_seq_count += add_dia_2_2[2]

    res = (open_seq_count, semi_open_seq_count, closed_seq_count)

    return res

def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    """
    Purpose:
    - Find the total number of open and semiopen sequences of a specific color, length, and direction in a row

    Parameters:
    - board -- the game board
    - col -- the color of the sequences to be checked
    - y_start -- the y-coordinate of the start of the row to be checked
    - x_start -- the x-coordinate of the start of the row to be checked
    - length -- the length of the sequences to be checked
    - d_y -- the y-direction of the row to be checked
    - d_x -- the x-direction of the row to be checked

    Returns:
    - Tuple of integers
    - (number of open sequences, number of semiopen sequences)

    Assumes:
    - The starting coordinates are at the edge of the board
    - Length is an integer greater than or equal to 2
    - The row lies in the board
    - Only complete sequences count (i.e., a row with _ _ b b b _ _ _ contains only one row of 3 blacks, not any other sequences)
    """

    # Use get_all_states() to find all relevant open, semiopen, and closed sequences
    res = get_all_states(board, col, y_start, x_start, length, d_y, d_x)

    # Save only the number of open and semiopen sequences
    res = (res[0], res[1])

    return res

def detect_rows(board, col, length):
    """
    Purpose:
    - Find the total number of open and semiopen sequences of a specific color and length in the entire board

    Parameters:
    - board -- the game board
    - col -- the color of the sequences to be checked
    - length -- the length of the sequences to be checked

    Returns:
    - Tuple of integers
    - (number of open sequences, number of semiopen sequences, number of closed sequences)

    Assumes:
    - Length is an integer greater than or equal to 2
    - Only complete sequences count (i.e., a row with _ _ b b b _ _ _ contains only one row of 3 blacks, not any other sequences)
    """

    # Use board_get_all_states() to find all relevant open, semiopen, and closed sequences
    totals = board_get_all_states(board, col, length)

    # Save only the number of open and semiopen sequences
    open_seq_count = totals[0]
    semi_open_seq_count = totals[1]

    res = (open_seq_count, semi_open_seq_count)

    return res

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def search_max(board):
    """
    Purpose:
    - Find the optimal square for black to maximize the score of the board

    Parameters:
    - board -- the game board

    Returns:
    - Tuple of integers
    - Square of optimal coordinates: (y-coordinate, x-coordinate)

    Assumes:
    - The board is an 8 by 8 board
    """

    max_score = score(board)
    move_y = 0
    move_x = 0

    for y_pos in range(0, 8):
        for x_pos in range(0, 8):

            if board[y_pos][x_pos] == " ":
                board[y_pos][x_pos] = "b"

                cur_score = score(board)

                if cur_score >= max_score:
                    max_score = cur_score

                    move_y = y_pos
                    move_x = x_pos

                # Reverting the board back to its original state
                board[y_pos][x_pos] = " "

    res = (move_y, move_x)

    return res

def is_win(board):
    """
    Purpose:
    - Determines the current state of the game

    Parameters:
    - board -- the game board

    Returns:
    - String
    - "White won" if white wins, "Black won" if black wins, "Draw" if the board is full without a winner, "Continue playing" if there is no winner and the game is not full

    Assumes:
    - If there is a winner, there is only one winner
    """

    # Checking if the board has any empty squares
    has_empty = 0

    for row in board:
        if " " in row:
            has_empty += 1

    if board_get_all_states(board, "b", 5) != (0, 0, 0):
        return "Black won"
    elif board_get_all_states(board, "w", 5) != (0, 0, 0):
        return "White won"
    elif has_empty == 0:
        return "Draw"
    else:
        return "Continue playing"


def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res





        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x


def test_is_empty():
    board  = make_empty_board(8)
    if is_empty(board):
        print("TEST CASE for is_empty PASSED")
    else:
        print("TEST CASE for is_empty FAILED")

def test_is_bounded():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)

    y_end = 3
    x_end = 5

    if is_bounded(board, y_end, x_end, length, d_y, d_x) == 'OPEN':
        print("TEST CASE for is_bounded PASSED")
    else:
        print("TEST CASE for is_bounded FAILED")


def test_detect_row():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_row(board, "w", 0,x,length,d_y,d_x) == (1,0):
        print("TEST CASE for detect_row PASSED")
    else:
        print("TEST CASE for detect_row FAILED")

def test_detect_rows():
    board = make_empty_board(8)
    x = 5; y = 1; d_x = 0; d_y = 1; length = 3; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    if detect_rows(board, col,length) == (1,0):
        print("TEST CASE for detect_rows PASSED")
    else:
        print("TEST CASE for detect_rows FAILED")

def test_search_max():
    board = make_empty_board(8)
    x = 5; y = 0; d_x = 0; d_y = 1; length = 4; col = 'w'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    x = 6; y = 0; d_x = 0; d_y = 1; length = 4; col = 'b'
    put_seq_on_board(board, y, x, d_y, d_x, length, col)
    print_board(board)
    if search_max(board) == (4,6):
        print("TEST CASE for search_max PASSED")
    else:
        print("TEST CASE for search_max FAILED")

def easy_testset_for_main_functions():
    test_is_empty()
    test_is_bounded()
    test_detect_row()
    test_detect_rows()
    test_search_max()

def some_tests():
    board = make_empty_board(8)

    board[0][5] = "w"
    board[0][6] = "b"
    y = 5; x = 2; d_x = 0; d_y = 1; length = 3
    put_seq_on_board(board, y, x, d_y, d_x, length, "w")
    print_board(board)
    analysis(board)

    # Expected output:
    #       *0|1|2|3|4|5|6|7*
    #       0 | | | | |w|b| *
    #       1 | | | | | | | *
    #       2 | | | | | | | *
    #       3 | | | | | | | *
    #       4 | | | | | | | *
    #       5 | |w| | | | | *
    #       6 | |w| | | | | *
    #       7 | |w| | | | | *
    #       *****************
    #       Black stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 0
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0
    #       White stones:
    #       Open rows of length 2: 0
    #       Semi-open rows of length 2: 0
    #       Open rows of length 3: 0
    #       Semi-open rows of length 3: 1
    #       Open rows of length 4: 0
    #       Semi-open rows of length 4: 0
    #       Open rows of length 5: 0
    #       Semi-open rows of length 5: 0

    y = 3; x = 5; d_x = -1; d_y = 1; length = 2

    put_seq_on_board(board, y, x, d_y, d_x, length, "b")
    print_board(board)
    analysis(board)

    # Expected output:
    #        *0|1|2|3|4|5|6|7*
    #        0 | | | | |w|b| *
    #        1 | | | | | | | *
    #        2 | | | | | | | *
    #        3 | | | | |b| | *
    #        4 | | | |b| | | *
    #        5 | |w| | | | | *
    #        6 | |w| | | | | *
    #        7 | |w| | | | | *
    #        *****************
    #
    #         Black stones:
    #         Open rows of length 2: 1
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 0
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #         White stones:
    #         Open rows of length 2: 0
    #         Semi-open rows of length 2: 0
    #         Open rows of length 3: 0
    #         Semi-open rows of length 3: 1
    #         Open rows of length 4: 0
    #         Semi-open rows of length 4: 0
    #         Open rows of length 5: 0
    #         Semi-open rows of length 5: 0
    #

    y = 5; x = 3; d_x = -1; d_y = 1; length = 1
    put_seq_on_board(board, y, x, d_y, d_x, length, "b");
    print_board(board);
    analysis(board);

    #        Expected output:
    #           *0|1|2|3|4|5|6|7*
    #           0 | | | | |w|b| *
    #           1 | | | | | | | *
    #           2 | | | | | | | *
    #           3 | | | | |b| | *
    #           4 | | | |b| | | *
    #           5 | |w|b| | | | *
    #           6 | |w| | | | | *
    #           7 | |w| | | | | *
    #           *****************
    #
    #
    #        Black stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0
    #        White stones:
    #        Open rows of length 2: 0
    #        Semi-open rows of length 2: 0
    #        Open rows of length 3: 0
    #        Semi-open rows of length 3: 1
    #        Open rows of length 4: 0
    #        Semi-open rows of length 4: 0
    #        Open rows of length 5: 0
    #        Semi-open rows of length 5: 0

def my_tests():
    passed = 0
    failed = 0

    print("RUNNING TANVI'S TEST CASES")

    ## is_empty
    print("Testing is_empty")
    board = make_empty_board(8)

    print_board(board)
    # Case 1
    if is_empty(board) == True:
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 2
    board[0][1] = "b"

    print_board(board)

    if is_empty(board) == False:
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    print("\n")

    ## is_bounded
    print("Testing is_bounded")
    # Case 1
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 5, 1, 0, 4, "w")
    print_board(board)
    if is_bounded(board, 3, 5, 4, 1, 0) == "SEMIOPEN":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 2
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 5, 1, -1, 6, "w")
    print_board(board)
    if is_bounded(board, 5, 0, 6, 1, -1) == "CLOSED":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 3
    board = make_empty_board(8)
    put_seq_on_board(board, 4, 3, 0, 1, 4, "w")
    print_board(board)
    if is_bounded(board, 4, 6, 4, 0, 1) == "OPEN":
        print(True)
        passed += 1
    else:
        failed += 1

    # Case 4
    board = make_empty_board(8)
    put_seq_on_board(board, 2, 3, 1, 1, 3, "w")
    put_seq_on_board(board, 1, 2, 1, 1, 1, "b")
    put_seq_on_board(board, 5, 6, 1, 1, 1, "b")

    print_board(board)
    if is_bounded(board, 4, 5, 3, 1, 1) == "CLOSED":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 5
    board = make_empty_board(8)
    put_seq_on_board(board, 2, 3, 1, 1, 3, "w")
    put_seq_on_board(board, 1, 2, 1, 1, 1, "b")
    print_board(board)
    if is_bounded(board, 4, 5, 3, 1, 1) == "SEMIOPEN":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 6
    board = make_empty_board(8)
    put_seq_on_board(board, 4, 3, 1, -1, 3, "w")
    print_board(board)
    if is_bounded(board, 6, 1, 3, 1, -1) == "OPEN":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    print("\n")

    ## detect_row
    print("Testing detect_row")
    # Case 1
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 5, 1, 0, 4, "w")
    print_board(board)

    if detect_row(board, "w", 0, 5, 4, 1, 0) == (0, 1):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 2
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 5, 1, 0, 4, "w")
    print_board(board)

    if detect_row(board, "w", 1, 5, 4, 1, 0) == (1, 0):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 3
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 5, 1, 0, 3, "w")
    put_seq_on_board(board, 4, 5, 1, 0, 3, "w")
    print_board(board)

    if detect_row(board, "w", 0, 5, 3, 1, 0) == (1, 1):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 4
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 7, 1, -1, 3, "w")
    put_seq_on_board(board, 4, 3, 1, -1, 3, "w")
    print_board(board)

    if detect_row(board, "w", 0, 7, 3, 1, -1) == (1, 1):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 5
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 3, 0, 1, 3, "w")
    print_board(board)

    if detect_row(board, "w", 0, 3, 2, 0, 1) == (0, 0):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 6
    board = make_empty_board(8)
    put_seq_on_board(board, 1, 1, 1, 1, 2, "w")
    put_seq_on_board(board, 4, 4, 1, 1, 2, "w")
    put_seq_on_board(board, 3, 3, 1, 1, 1, "b")
    print_board(board)

    if detect_row(board, "w", 1, 1, 2, 1, 1) == (0, 2):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 7
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 1, 1, 8, "w")
    print_board(board)

    if detect_row(board, "w", 1, 1, 4, 1, 1) == (0, 0):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    print("\n")

    ## detect_rows
    print("Testing detect_rows")
    # Case 1
    board = make_empty_board(8)
    put_seq_on_board(board, 3, 7, 1, -1, 3, "w")
    put_seq_on_board(board, 1, 4, 0, 1, 3, "b")
    put_seq_on_board(board, 0, 0, 1, 0, 4, "b")
    put_seq_on_board(board, 5, 1, 1, 1, 2, "b")
    put_seq_on_board(board, 5, 6, 1, -1, 3, "b")
    print_board(board)

    if detect_rows(board, "b", 3) == (1, 1):
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    print("\n")

    ## is_win
    print("Testing is_win")
    # Case 1
    board = make_empty_board(8)
    for row in board:
        for col in range (0, 8, 2):
            row[col] = "w"
        for col in range (1, 8, 2):
            row[col] = "b"

    print_board(board)

    if is_win(board) == "Draw":
        print(True)
        passed += 1
    else:
        print(False)
        print(is_win(board))
        failed += 1

    # Case 2
    board = make_empty_board(8)
    put_seq_on_board(board, 3, 7, 1, -1, 5, "w")
    put_seq_on_board(board, 1, 4, 0, 1, 3, "b")
    print_board(board)

    if is_win(board) == "White won":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 3
    board = make_empty_board(8)
    put_seq_on_board(board, 3, 7, 1, -1, 5, "b")
    put_seq_on_board(board, 1, 4, 0, 1, 3, "w")
    print_board(board)

    if is_win(board) == "Black won":
        print(True)
        passed += 1
    else:
        print(False)
        failed += 1

    # Case 4
    board = make_empty_board(8)
    put_seq_on_board(board, 0, 0, 0, 1, 8, "w")
    put_seq_on_board(board, 1, 0, 0, 1, 8, "b")
    put_seq_on_board(board, 2, 0, 0, 1, 8, "w")
    put_seq_on_board(board, 3, 0, 0, 1, 8, "b")
    put_seq_on_board(board, 4, 0, 0, 1, 8, "w")
    put_seq_on_board(board, 5, 0, 0, 1, 8, "b")
    put_seq_on_board(board, 6, 0, 0, 1, 8, "w")
    put_seq_on_board(board, 7, 0, 0, 1, 8, "b")
    print_board(board)

    if is_win(board) == "Draw":
        print(True)
        passed += 1
    else:
        print(False)
        print(is_win(board))
        failed += 1

    # Case 5
    board = make_empty_board(8)
    put_seq_on_board(board, 3, 7, 1, -1, 4, "b")
    put_seq_on_board(board, 1, 4, 0, 1, 3, "w")
    print_board(board)

    if is_win(board) == "Continue playing":
        print(True)
        passed += 1
    else:
        print(False)
        print(is_win(board))
        failed += 1

    print("\n")

    print("\nDONE RUNNING TANVI'S TEST CASES")
    print(f"PROGRAM PERFORMANCE\nTests Passed: {passed}\nTests Failed: {failed}")


if __name__ == '__main__':

    #play_gomoku(8)

    #easy_testset_for_main_functions()

    #some_tests()

    my_tests()

    # Additional testing conducted using tests provided by Samson
