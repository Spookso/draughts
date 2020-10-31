# Checks that the piece is moving the right way for its type
def direction_check(board, start_row, start_col, end_row):

    # if it is a normal piece, checks it is moving forward only
    if board[start_row][start_col] == 1:
        if end_row > start_row:
            # print("Wrong Direction for Piece Type")
            return False
    if board[start_row][start_col] == 3:
        if end_row < start_row:
            # print("Wrong Direction for Piece Type")
            return False

    return True


# Checks if move is legal
def move_check(board, start_row, start_col, end_row, end_col):
    # Initialises local variables
    moving = False
    double = False
    repeat = False
    legal = False
    direction = 0
    side = 0

    # In case direction_check fails so there is no error in the returning

    if direction_check(board, start_row, start_col, end_row):

        # checks side (left or right) piece is trying to move in
        if end_col > start_col:
            side = 1
        else:
            side = -1

        # checks direction (up or down) piece is trying to move in
        if end_row > start_row:
            direction = 1
        else:
            direction = -1

        # print("start row:", start_row, "end row:", end_row, "start col:", start_col, "end col:", end_col, "direction:", direction, "side:", side)

        # if the piece is trying to move to a square on the board
        if -1 < end_row < 8 and -1 < end_col < 8:

            # checks if it is a double move
            if start_row + direction * 2 == end_row and start_col + side * 2 == end_col:
                if board[start_row + direction][start_col + side] != 0:
                    if board[start_row + direction][start_col + side] != board[start_row][start_col]:
                        if board[start_row][start_col] == 1 or board[start_row][start_col] == 3:
                            if board[start_row + direction][start_col + side] != board[start_row][start_col] + 1:
                                double = True
                                legal = True
                        elif board[start_row + direction][start_col + side] != board[start_row][start_col] - 1:
                            double = True
                            legal = True

            # Otherwise, is it a single move?
            if start_row + direction == end_row and start_col + side == end_col:
                legal = True

            # If the place it is moving to is empty and the move is legal, it can move
            if board[end_row][end_col] == 0 and legal:
                moving = True

    return moving, double, direction, side, repeat


def move(board, start_row, start_col, end_row, end_col, direction, side):
    board[start_row + direction][start_col + side] = 0
    board[end_row][end_col] = board[start_row][start_col]
    board[start_row][start_col] = 0
    # print("Moved.")

    return board

def double_move_check(board, row, col, direction, side):
    repeat = False
    new_row = row + (2 * direction)
    new_col = col + 2
    work_row = 0
    work_col = 0
    if board[row][col] == 2 or board[row][col] == 4:
        for i in range(0, 2):
            for attempt in range(0, 2):
                print("ROW:", row, "NEW_ROW:", new_row, "COL:", col,  "NEW_COL", new_col, "DIRECTION", direction, "SIDE", side)
                if move_check(board, row, col, new_row, new_col)[0]:
                    repeat = True
                    work_row = new_row
                    work_col = new_col
                print("REPEAT:", repeat)
                new_col = col - 2

            new_row = row - (2 * direction)
            new_col = col + 2
    else:
        for attempt in range(0, 2):
            print("ROW:", row, "NEW_ROW:", new_row, "COL:", col,  "NEW_COL", new_col, "DIRECTION", direction, "SIDE", side)
            if move_check(board, row, col, new_row, new_col)[0]:
                repeat = True
                work_row = new_row
                work_col = new_col
            print("REPEAT:", repeat)
            new_col = col - 2

    return repeat, row, col, work_row, work_col
