import pygame, math, movement, time, random

# Initiates the pygame library
pygame.init()

# Sets up a window of size 800 x 800 pixels with the tag 'resizable'
win = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
# Sets the caption for the window as "Draughts"
pygame.display.set_caption("Draughts")
# allows pygame.time.Clock() to be accessed easily
clock = pygame.time.Clock()

# Initisalises variables
turn = 1
correct_turn = True

# Default window size
width = 800
height = 800

# sets whether there will be an ai opponent
# if input("Play against the computer? ") == "Yes":
#     ai = True
# else:
#     ai = False

ai = True
random_ai = False
calculated = False
print("ai true")


# Declares the 'current_board' array, a 2D array that consists of rows of numbers representing pieces or empty squares
current_board = [
    [0, 3, 0, 3, 0, 3, 0, 3],
    [3, 0, 3, 0, 3, 0, 3, 0],
    [0, 3, 0, 3, 0, 3, 0, 3],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0]
]

movelist = []

# current_board = [
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 2, 0, 0, 0, 3, 0],
#     [0, 0, 0, 3, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 3, 0],
#     [0, 0, 0, 3, 0, 0, 0, 1],
#     [0, 0, 1, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 1, 0],
#     [0, 0, 0, 0, 0, 4, 0, 0]
# ]

saved_board = []
for row in current_board:
    saved_board.append(row)

# Changes player turn
def turn_change(turn):
    turn += 1
    if turn > 2:
        turn = 1
    return turn


# Checks if a player is out of pieces
def win_check(board):
    red = True
    blue = True
    for row in board:
        for piece in row:
            if piece == 1 or piece == 2:
                red = False
            elif piece == 3 or piece == 4:
                blue = False

    if red:
        return 1
    if blue:
        return 2

    return 0


# checks whether a piece will be kinged
def king_check(board):
    num = 0
    for piece in board[0]:
        if piece == 1:
            board[0][num] = 2
        num += 1
    num = 0
    for piece in board[7]:
        if piece == 3:
            board[7][num] = 4
        num += 1

def update(moves):
    board = [
        [0, 3, 0, 3, 0, 3, 0, 3],
        [3, 0, 3, 0, 3, 0, 3, 0],
        [0, 3, 0, 3, 0, 3, 0, 3],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0]
    ]
    # print("updating")
    for i in range(0, len(moves)):
        board = movement.move(board, moves[i][0], moves[i][1], moves[i][2], moves[i][3], moves[i][4], moves[i][5])
        king_check(board)

    return board

def max(ai_board, depth, cap):
    ai_saved = []
    for row in ai_board:
        ai_saved.append(row)

    # the score of the best possiblity is initialised at -200, below the score given if the game is lost
    maxv = -200
    sx = None
    sy = None
    ex = None
    ey = None


    # if the ai has won with this board, it makes no move from here
    if win_check(ai_board) == 1:
        return (-100, 0, 0, 0, 0, depth)
    if win_check(ai_board) == 2:
        return (100, 0, 0, 0, 0, depth)

    # checks whether the ai should search down another layer of the tree
    if depth <= cap:
        # print("RUNNING")
        # si, sj = starting row and starting col
        for si in range(0, 8):
            for sj in range(0, 8):
                # if the piece is on the ai's team
                if ai_board[si][sj] == 3 or ai_board[si][sj] == 4:
                    # ei, ej = ending row and ending col
                    for ei in range(0, 8):
                        for ej in range(0, 8):
                            # if the move is legal
                            if movement.move_check(ai_board, si, sj, ei, ej)[0]:
                                depth += 1
                                direction, side = movement.move_check(ai_board, si, sj, ei, ej)[2], movement.move_check(ai_board, si, sj, ei, ej)[3]
                                # if the move is not a double-take move
                                if not movement.move_check(ai_board, si, sj, ei, ej)[4]:
                                    movement.move(ai_board, si, sj, ei, ej, direction, side)
                                # otherwise:
                                else:
                                    depth += 1
                                    forcedx, forcedy = movement.double_move_check(ai_board, si, sj, direction, side)[3], movement.double_move_check(ai_board, si, sj, direction, side)[4]
                                    movement.move(ai_board, si, sj, ei, ej, direction, side)
                                    movement.move(ai_board, si, sj, forcedx, forcedy, direction, side)

                                (m, min_si, min_sj, min_ei, min_ej, depth) = min(ai_board, depth, cap)

                                if m > maxv:
                                    maxv = m
                                    sx = si
                                    sy = sj
                                    ex = ei
                                    ey = ej

                                ai_board = []
                                for row in ai_saved:
                                    ai_board.append(row)
    else:
        # do the scoring of this board here, make up some m value for the score
        score = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if ai_board[x][y] == 1:
                    score -= 1
                if ai_board[x][y] == 2:
                    score -= 2
                if ai_board[x][y] == 3:
                    score += 1
                if ai_board[x][y] == 4:
                    score += 2

        m = score
        depth = 0

    return (m, sx, sy, ex, ey, depth)

def min(ai_board, depth, cap):
    ai_saved = []
    for row in ai_board:
        ai_saved.append(row)

    # the score of the best possiblity is initialised at 200, above the score given if the game is won
    minv = 200
    sx = None
    sy = None
    ex = None
    ey = None

    # if the ai has won with this board, it makes no move from here
    if win_check(ai_board) == 1:
        return (-100, 0, 0, 0, 0, depth)
    if win_check(ai_board) == 2:
        return (100, 0, 0, 0, 0, depth)

    # checks whether the ai should search down another layer of the tree
    if depth <= cap:
        # si, sj = starting row and starting col
        for si in range(0, 8):
            for sj in range(0, 8):
                # if the piece is on the ai's team
                if ai_board[si][sj] == 1 or ai_board[si][sj] == 2:
                    # ei, ej = ending row and ending col
                    for ei in range(0, 8):
                        for ej in range(0, 8):
                            # if the move is legal
                            if movement.move_check(ai_board, si, sj, ei, ej)[0]:
                                depth += 1
                                direction, side = movement.move_check(ai_board, si, sj, ei, ej)[2], movement.move_check(ai_board, si, sj, ei, ej)[3]
                                # if the move is not a double-take move
                                if not movement.move_check(ai_board, si, sj, ei, ej)[4]:
                                    movement.move(ai_board, si, sj, ei, ej, direction, side)
                                # otherwise:
                                else:
                                    depth += 1
                                    forcedx, forcedy = movement.double_move_check(ai_board, si, sj, direction, side)[3], movement.double_move_check(ai_board, si, sj, direction, side)[4]
                                    movement.move(ai_board, si, sj, ei, ej, direction, side)
                                    movement.move(ai_board, si, sj, forcedx, forcedy, direction, side)

                                (m, max_si, max_sj, max_ei, max_ej, depth) = max(ai_board, depth, cap)

                                if m < minv:
                                    minv = m
                                    sx = si
                                    sy = sj
                                    ex = ei
                                    ey = ej

                                ai_board = []
                                for row in ai_saved:
                                    ai_board.append(row)
    else:
        # do the scoring of this board here, make up some m value for the score
        score = 0
        for x in range(0, 8):
            for y in range(0, 8):
                if ai_board[x][y] == 1:
                    score -= 1
                if ai_board[x][y] == 2:
                    score -= 2
                if ai_board[x][y] == 3:
                    score += 1
                if ai_board[x][y] == 4:
                    score += 2

        m = score
        depth = 0

    return (m, sx, sy, ex, ey, depth)

def draw_window(win, board):
    colour = (255, 255, 255)
    x = 0
    y = 0

    # Drawing out board
    for row in board:
        for square in row:
            pygame.draw.rect(win, colour, (x, y, round(width / 8), round(height / 8)))
            # Swapping colour
            if colour == (255, 255, 255):
                colour = (100, 160, 100)
            else:
                colour = (255, 255, 255)
            x += round(width / 8)
        # Swapping colour again for next row
        if colour == (255, 255, 255):
            colour = (100, 160, 100)
        else:
            colour = (255, 255, 255)
        y += round(height / 8)
        x = 0

    # Drawing pieces onto screen
    x = round((width / 8) / 2)
    y = round((height / 8) / 2)
    for row in board:
        for piece in row:
            if piece == 1:
                pygame.draw.circle(win, (255, 0, 0), (x, y), round(width / 20))
            elif piece == 2:
                pygame.draw.circle(win, (255, 255, 0), (x, y), round(width / 20))
            elif piece == 3:
                pygame.draw.circle(win, (0, 0, 255), (x, y), round(width / 20))
            elif piece == 4:
                pygame.draw.circle(win, (0, 255, 255), (x, y), round(width / 20))
            x += round(width / 8)
        x = round((width / 8) / 2)
        y += round(height / 8)

    pygame.display.update()

selected = False
progress = False
saved_row, saved_col = 0, 0
repeat = False

run = True
while run:
    human = False
    clock.tick(60)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # quits game
        if event.type == pygame.QUIT:
            run = False

        # Checks if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If a piece is already selected
            if selected:
                mouse_x = math.floor((mouse_x / (width / 8)))
                mouse_y = math.floor((mouse_y / (height / 8)))
                if repeat:
                    # if it is consecutive move, ensure that the piece is taking another piece
                    if end_row == mouse_y + 2 or end_row == mouse_y - 2:
                        end_col, end_row = mouse_x, mouse_y
                else:
                    end_col, end_row = mouse_x, mouse_y
                progress = True
                human = True
            # If a piece has not been selected
            else:
                mouse_x = math.floor((mouse_x / (width / 8)))
                mouse_y = math.floor((mouse_y / (height / 8)))

                print(mouse_x, mouse_y)

                if current_board[mouse_y][mouse_x] != 0:
                    if repeat:
                        print("SAVED", saved_row, saved_col)
                        # if it is consecutive move, ensure that the same piece is moving
                        if mouse_x == saved_row and mouse_y == saved_col:
                            start_col, start_row = mouse_x, mouse_y
                    else:
                        start_col, start_row = mouse_x, mouse_y
                    selected = True
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if turn == 2 and ai:
        progress = True


    # Checks whether an attempt at a move should be made
    if progress:
        if turn == 1:
            print("turn:", turn, "start row:", start_row, "start col:", start_col, "piece:", current_board[start_row][start_col])
            print()
            # Checks whether it is moving the right piece for their turn
            if turn == 1:
                if current_board[start_row][start_col] != 1 and current_board[start_row][start_col] != 2:
                    correct_turn = False
                    print("Not piece in turn 1")
            elif turn == 2 and not ai:
                if current_board[start_row][start_col] != 3 and current_board[start_row][start_col] != 4:
                    correct_turn = False
                    print("Not piece in turn 2")

        elif random_ai:
            legal_moves = []
            start_row = 0
            for row in current_board:
                start_col = 0
                if ai_repeat:
                    start_row, start_col = saved
                for piece in row:
                    if piece in [3, 4]:
                        for end_row in range(0, 8):
                            for end_col in range(0, 8):
                                if movement.move_check(current_board, start_row, start_col, end_row, end_col)[0]:
                                    legal_moves.append([start_row, start_col, end_row, end_col, movement.move_check(current_board, start_row, start_col, end_row, end_col)[2], movement.move_check(current_board, start_row, start_col, end_row, end_col)[3]])
                    if not ai_repeat:
                        start_col += 1
                start_row += 1
            try:
                time.sleep(0.4)
                choice = random.randint(0, len(legal_moves) - 1)
                correct_turn = True
                progress = False
                start_row, start_col, end_row, end_col, direction, side = legal_moves[choice]
                ai_repeat = False
                if movement.move_check(current_board, start_row, start_col, end_row, end_col)[4]:
                    ai_repeat = True
                    saved = [start_row, start_col]

            except:
                print("NO MOVES")
                correct_turn = False

        elif ai:
            ai_board = []
            for row in current_board:
                ai_board.append(row)
            cap = 10
            (m, start_row, start_col, end_row, end_col, depth) = max(ai_board, 0, cap)
            print("BEST MOVE:")
            print(start_row, start_col)
            print(end_row, end_col)
            # print(current_board)
            # correct_turn = True
            ai = False

        # moves the piece
        repeat = False
        if correct_turn:
            moving, double, direction, side, repeat = movement.move_check(current_board, start_row, start_col, end_row, end_col)
            # if the move was valid, change the turn
            if moving:
                print("start row", start_row)
                movelist.append([start_row, start_col, end_row, end_col, direction, side])
                current_board = movement.move(current_board, start_row, start_col, end_row, end_col, direction, side)
                # if the move was a piece taking move, check if it can move again
                if double:
                    repeat, saved_col, saved_row, work_row, work_col = movement.double_move_check(current_board, end_row, end_col, direction, side)
                # somehow ai gets stuck when it repeats
                # keeps recalculating moves - not sure exactly what's wrong
                if not repeat:
                    turn = turn_change(turn)
                    ai = True
                double = False
            # else don't change the turn
            else:
                pass
                # print("Invalid move")

        # resets the progress with clicking on a piece
        progress = False
        selected = False
        correct_turn = True
        calculated = False
        current_board = update(movelist)

        # Checks if one player is out of pieces
        if win_check(current_board) == 1:
            print("White wins!")
            run = False
        elif win_check(current_board) == 2:
            print("Black wins!")
            run = False

        # Checks if a piece can be kinged
        king_check(current_board)
    draw_window(win, current_board)
pygame.quit()
