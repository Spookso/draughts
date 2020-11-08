# checks that the piece is moving the correct way for it type (non-kinged pieces can only move forward)
def direction_check(board, start_row, start_col, end_row):

    # if it is a normal piece, checks it is moving forward only
    if board[start_row][start_col] == 1: # normal piece on team one
        if end_row > start_row:
            return False
    if board[start_row][start_col] == 3: # normal piece on team two
        if end_row < start_row:
            return False

    return True


# this functions checks if a move is legal
def move_check(board, start_row, start_col, end_row, end_col):
    # initialising local variables
    moving = False # whether the piece can move
    double = False # whether the move captures a piece
    legal = False # whether the movement of the piece is correct
    direction = 0
    side = 0

    # if the pieces are moving in the correct direction
    if direction_check(board, start_row, start_col, end_row):

        # finds the side (left or right) that piece is trying to move in
        if end_col > start_col:
            side = 1
        else:
            side = -1

        # finds the direction (up or down) that the piece is trying to move in
        if end_row > start_row:
            direction = 1
        else:
            direction = -1

        if -1 < end_row < 8 and -1 < end_col < 8: # if the end coordinates are not out of bounds

            # this block of code checks if the move captures a piece, thus moving two squares
            if start_row + direction * 2 == end_row and start_col + side * 2 == end_col: # if the piece is moving two spaces in the 'direction' and 'side' it is going in
                if board[start_row + direction][start_col + side] != 0: # if it is moving over a square that contains a piece
                    if board[start_row + direction][start_col + side] != board[start_row][start_col]: # if the piece it is jumping over is not the same type as itself
                        if board[start_row][start_col] == 1 or board[start_row][start_col] == 3: # if the piece performing the move is the normal type / this is important because if it is a normal piece, then I can simply add one to its value and check if it is jumping over a piece with this new value, and as such a kinged piece on its team. Otherwise I can subtract 1 from its number, and check if the piece being jumped over is a normal piece on the same team as the moving piece
                            if board[start_row + direction][start_col + side] != board[start_row][start_col] + 1: # checks that the piece that it is jumping over is not, a kinged piece, but on the same team
                                double = True # the move is a 'double' move, or in other words captures a piece
                                legal = True # the move is also legal
                        # otherwise if the piece that is moving is a kinged piece
                        elif board[start_row + direction][start_col + side] != board[start_row][start_col] - 1: # checks that the piece that it is jumping over is not, not a kinged piece, but on the same team
                            double = True  # the move is a 'double' move, or in other words captures a piece
                            legal = True  # the move is also legal

            # otherwise, is it a single move?
            if start_row + direction == end_row and start_col + side == end_col: # if the piece is moving just one square
                legal = True


            if board[end_row][end_col] == 0 and legal: # if the square the piece is moving to is empty and the move is legal, it can move
                moving = True

    return moving, double, direction, side

# this function modifies the board array, performing a move
def move(board, start_row, start_col, end_row, end_col, direction, side):
    # these three lines work regardless of whether the piece is moving one square or two squares, capturing a piece
    board[start_row + direction][start_col + side] = 0 # the space one square diagonnally that the piece is moving in is set to be empty
    board[end_row][end_col] = board[start_row][start_col] # the piece is moved to its ending square
    board[start_row][start_col] = 0 # the starting square of the piece is set to be empty

    return board # the board here is the 2D array containing rows of squares

# this functions checks if a second, consecutive move is possible
def double_move_check(board, row, col, direction, side): # the board, as well as the current coordinates of the piece are taken in as arguments
    repeat = False # whether the consecutive move is possible; this will be set to True if it is
    new_row = row + (2 * direction) # new ending row coordinate two squares in the direction that the piece can travel (direction is either -1 or 1 depending on if the piece can go up or down)
    new_col = col + 2 # new ending colunm coordinate two squares to the right

    if board[row][col] == 2 or board[row][col] == 4: # if the piece is a king, and as such able to move both up and down
        for i in range(0, 2): # for every direction that the piece can move in (up and down)
            for attempt in range(0, 2): # for every column that the piece can move in to (left and right)
                if move_check(board, row, col, new_row, new_col)[0]: # if the move is legal
                    repeat = True # the piece can do a second, consecutive move
                new_col = col - 2 # the ending column coordinate is changed to be two squares to the left

            new_row = row - (2 * direction) # the ending row coordinate is changed (if it was going up, it is now going down and vica versa)
            new_col = col + 2 # the ending column coordinate is reset
    else: # otherwise if the piece is a non-king piece, and as such only able to move in one direction vertically
        for attempt in range(0, 2): # for every column that the piece can move in to (left and right)
            if move_check(board, row, col, new_row, new_col)[0]: # if the move is legal
                repeat = True  # the piece can do a second, consecutive move
            new_col = col - 2  # the ending column coordinate is changed to be two squares to the left

    return repeat, row, col
