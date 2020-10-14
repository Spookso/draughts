# Checks that the piece is moving the right way for its type
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

        print("start row:", start_row, "end row:", end_row, "start col:", start_col, "end col:", end_col, "direction:", direction, "side:", side)

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
    print("Moved.")

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
    def __init__(self, own_board, own_move, own_score, parent, team, forced):
        self.own_board = own_board
        self.own_move = own_move
        self.own_score = own_score
        self.parent = parent
        self.team = team
        self.forced = forced
        self.child_list = []
        self.best_child = -10000

    def team_swap(self):
        if self.team == 1:
            return 3
        return 1

    def calculate_moves(self):
        if self.forced == '':
            start_row = 0
            for row in self.own_board:
                start_col = 0
                for piece in row:
                    if piece == self.team or piece == self.team + 1:
                        for end_row in range(0, 8):
                            for end_col in range(0, 8):
                                self.clone(start_row, start_col, end_row, end_col)
                    start_col += 1
                start_row += 1
        else:
            start_row, start_col = self.forced
            if double_move_check(self.own_board, start_row, start_col, 1, 1)[0]:
                end_row = double_move_check(self.own_board, start_row, start_col, 1, 1)[3]
                end_col = double_move_check(self.own_board, start_row, start_col, 1, 1)[4]
                self.clone(start_row, start_col, end_row, end_col)

    def clone(self, start_row, start_col, end_row, end_col):
        moves = [start_row, start_col, end_row, end_col, move_check(self.own_board, start_row, start_col, end_row, end_col)[2], move_check(self.own_board, start_row, start_col, end_row, end_col)[3]]
        new_board = move(self.own_board, self.own_move[0], self.own_move[1], self.own_move[2], self.own_move[3], self.own_move[4], self.own_move[5])
        score = 0
        if move_check(self.own_board, start_row, start_col, end_row, end_col)[4]:
            force = [start_row, start_col]
        else:
            force = ''
        for row in new_board:
            for piece in row:
                if piece != self.team and piece != self.team + 1:
                    score -= 3
                elif piece == self.team + 1:
                    score += 2
                elif piece == self.team:
                    score += 1
        self.child_list.append(leaf(new_board, moves, score, self, self.team_swap(), force))


class petal(leaf):
    def score(self):
        pass
