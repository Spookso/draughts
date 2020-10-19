import time
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



class leaf():
    def __init__(self, board, move_list, forced, depth, team):
        self.board = board
        self.move_list = move_list
        self.forced = forced
        self.child_list = []
        self.depth = depth + 1
        self.best_child = 0
        self.team = team

    def team_change(self):
        if self.team == [3, 4]:
            return [1, 2]
        return [3, 4]

    def find_board(self):
        self.board = [
            [0, 3, 0, 3, 0, 3, 0, 3],
            [3, 0, 3, 0, 3, 0, 3, 0],
            [0, 3, 0, 3, 0, 3, 0, 3],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 1, 0, 1, 0, 1, 0],
            [0, 1, 0, 1, 0, 1, 0, 1],
            [1, 0, 1, 0, 1, 0, 1, 0]
        ]
        for i in range(0, len(self.move_list)):
            self.board = move(self.board, self.move_list[i][0], self.move_list[i][1], self.move_list[i][2], self.move_list[i][3], self.move_list[i][4], self.move_list[i][5])
            self.king_check()

        return self.board

    def king_check(self):
        num = 0
        for piece in self.board[0]:
            if piece == 1:
                self.board[0][num] = 2
            num += 1
        num = 0
        for piece in self.board[7]:
            if piece == 3:
                self.board[7][num] = 4
            num += 1

    def calculate_moves(self):
        self.board = self.find_board()
        if self.forced == '':
            start_row = 0
            for row in self.board:
                start_col = 0
                for piece in row:
                    if piece in self.team:
                        for end_row in range(0, 8):
                            for end_col in range(0, 8):
                                if move_check(self.board, start_row, start_col, end_row, end_col)[0]:
                                    self.clone(start_row, start_col, end_row, end_col)
                    start_col += 1
                start_row += 1
        else:
            start_row, start_col = self.forced
            if double_move_check(self.board, start_row, start_col, 1, 1)[0]:
                time.sleep(2)
                print("DOUBLE FOUND")
                end_row = double_move_check(self.board, start_row, start_col, 1, 1)[3]
                end_col = double_move_check(self.board, start_row, start_col, 1, 1)[4]
                if move_check(self.board, start_row, start_col, end_row, end_col)[0]:
                    self.clone(start_row, start_col, end_row, end_col)

    def clone(self, start_row, start_col, end_row, end_col):
        moves = self.move_list
        moves.append([start_row, start_col, end_row, end_col, move_check(self.board, start_row, start_col, end_row, end_col)[2], move_check(self.board, start_row, start_col, end_row, end_col)[3]])
        # bit confused about here; shouldn't it be moves[0], moves[1], etc instead of own_move
        # as you are performing the new moves
        #---------------------------------------------------
        # something is fundamentally broken here
        # board is not being updated correctly; the boards that the twigs have are not 4 moves ahead,
        # they are the current board but with each twig losing a piece
        # THIS WHOLE THING needs to be like completely re-wrtten
        # If no solution to the board loss is found ai might all need to be scrapped
        # good luck
        self.board = self.find_board()
        if move_check(self.board, start_row, start_col, end_row, end_col)[4]:
            force = [start_row, start_col]
        else:
            force = ''
        new_board = move(self.board, self.move_list[-1][0], self.move_list[-1][1], self.move_list[-1][2], self.move_list[-1][3], self.move_list[-1][4], self.move_list[-1][5])
        if self.depth != 4:
            self.child_list.append(leaf(new_board, moves, force, self.depth, self.team_change()))
        else:
            self.child_list.append(twig(new_board, moves, force, self.depth, self.team_change()))

class twig(leaf):
    # issue here is that the board is deleted when things happen
    # so each twig has less board
    # and can't just use the update function because this is the board three moves in advance
    # don't know how to fix this without a major rework, or firguring out why the board keeps changing itself
    # when it shouldn't
    def score_self(self):
        self.board = self.find_board()
        print(self.board)
        score = 0
        empty = True
        for row in self.board:
            for piece in row:
                if piece == 3:
                    score += 1
                    empty = False
                elif piece == 4:
                    score += 2
                    empty = False
                elif piece == 1:
                    score -= 3
                elif piece == 2:
                    score -= 4
        if empty:
            score = -10000000000
        self.score = score
