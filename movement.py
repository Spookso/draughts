
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


def move(board, start_row, start_col, end_row, end_col):
    moved = False
    moving = False

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
            #If a piece is a king, is it moving over a normal piece?
            else:
                if board[start_row + direction][start_col + side] != board[start_row][start_col] - 1:
                    moving = True
        else:
            print("Trying to jump over same piece")

        # moves the piece one space
        if moving:
            if end_row == start_row + direction and end_col == start_col + side:
                print("Moved one space")
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row][start_col] = 0
                moved = True

        # jumps piece over another

            # if the piece being jumped over is not on the other's own team, jump over it
            elif end_row == start_row + (direction * 2) and end_col == start_col + (side * 2):
                print("Moved over another piece")
                board[end_row][end_col] = board[start_row][start_col]
                board[start_row + direction][start_col + side] = 0
                board[start_row][start_col] = 0
                moved = True
            else:
                print("Cannot move there")

    return board, moved
