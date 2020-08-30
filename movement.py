
def direction_check(board, start_row, start_col, end_row):

    # if it is a normal piece, checks it is moving forward only
    if board[start_row][start_col] == 1:
        if end_row > start_row:
            print("Wrong Direction for Piece Type")
            return False
    if board[start_row][start_col] == 3:
        if end_row < start_row:
            print("Wrong Direction for Piece Type")
            return False

    return True

def double_move_check(board, start_row, end_row, start_col, end_col, direction, side):
    board = move(board, start_row, end_row, start_col, end_col, direction, side)[0]
    try:
        if move_check(board, end_row, end_col, end_row - 2, end_col + 2)[0]:
            return True
    except:
        print("Tested Out of Bounds Move")
    try:
        if move_check(board, end_row, end_col, end_row - 2, end_col - 2)[0]:
            return True
    except:
        print("Tested Out of Bounds Move")
    return False

def move_check(board, start_row, start_col, end_row, end_col):
    moving = False
    double = False

    if direction_check(board, start_row, start_col, end_row):

        # checks side piece is trying to move in
        if end_col > start_col:
            side = 1
        else:
            side = -1

        # checks direction piece is trying to move in
        if end_row > start_row:
            direction = 1
        else:
            direction = -1

        #Sets up coordinates for idexing

        print("start row:", start_row, "end row:", end_row, "start col:", start_col, "end col:", end_col, "direction:", direction, "side:", side)

        # Checks that piece being taken is not on own team
        print(board[start_row + direction][start_col + side], board[start_row][start_col])
        if board[start_row + direction][start_col + side] != board[start_row][start_col]:
            # checks that piece is not on own team

            #If piece is normal, is it moving over a king?
            if board[start_row][start_col] != 2 and board[start_row][start_col] != 4:
                if board[start_row + direction][start_col + side] != board[start_row][start_col] + 1:
                    moving = True
                    if double_move_check(board, start_row, start_col, end_row, end_col, direction, side):
                        double = True
            #If a piece is a king, is it moving over a normal piece?
            else:
                if board[start_row + direction][start_col + side] != board[start_row][start_col] - 1:
                    moving = True
                    if double_move_check(board, start_row, start_col, end_row, end_col, direction, side):
                        double = True
        else:
            print("Trying to jump over same piece")

    return moving, double, direction, side


def move(board, start_row, start_col, end_row, end_col, direction, side):
    board[start_row + direction][start_col + side] = 0
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = 0
    print("Moved.")

    return board
