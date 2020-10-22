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
ai_repeat = False
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
    white = True
    black = True
    for row in board:
        for piece in row:
            if piece == 1 or piece == 2:
                white = False
            elif piece == 3 or piece == 4:
                black = False

    if white:
        return 1
    if black:
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
    print("updating")
    for i in range(0, len(moves)):
        board = movement.move(board, moves[i][0], moves[i][1], moves[i][2], moves[i][3], moves[i][4], moves[i][5])
        king_check(board)

    return board

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
            ai_list = []
            for item in movelist:
                ai_list.append(item)
            start = movement.leaf(current_board, ai_list, '', 1, [3, 4])
            start.calculate_moves() # every move ai can do
            start.best_child = 0
            for leaf in start.child_list:
                leaf.calculate_moves() # every move the player can do
                for petal in leaf.child_list:
                    petal.calculate_moves() # every counter the ai can play
                    for twig in petal.child_list:
                        # draw_window(win, current_board)
                        # twig.score_self(update(movelist))
                        twig.score_self()
                        if twig.score > petal.child_list[petal.best_child].score:
                            petal.best_child = petal.child_list.index(twig)
                    if len(leaf.child_list[leaf.best_child].child_list) > 0:
                        if len(petal.child_list) > 0:
                            if petal.child_list[petal.best_child].score < leaf.child_list[leaf.best_child].child_list[leaf.child_list[leaf.best_child].best_child].score:
                                leaf.best_child = leaf.child_list.index(petal)
                if len(leaf.child_list) > 0:
                    if len(leaf.child_list[leaf.best_child].child_list) > 0:
                        if len(leaf.child_list[leaf.best_child].child_list[leaf.child_list[leaf.best_child].best_child].child_list) > 0:
                            if len(start.child_list) > 0:
                                if leaf.child_list[leaf.best_child].child_list[leaf.child_list[leaf.best_child].best_child].score > start.child_list[start.best_child].child_list[start.child_list[start.best_child].best_child].child_list[start.child_list[start.best_child].child_list[start.child_list[start.best_child].best_child].best_child].score:
                                    start.best_child = start.child_list.index(leaf)
            print("length", len(start.child_list))
            print(start.best_child)
            # this bit is not working at all
            # figure out which index of the move list is the correct one
            # possibly re-write the best move finding thing
            print("move_list", start.child_list[start.best_child].move_list)
            start_row, start_col, end_row, end_col, direction, side = start.child_list[start.best_child].move_list[len(movelist)]
            correct_turn = True
            progress = False



        # moves the piece
        repeat = False
        if correct_turn:
            print("HELLO")
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
                double = False
            # else don't change the turn
            else:
                print("Invalid move")

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
