import pygame, math, movement

pygame.init()

win = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
pygame.display.set_caption("Draughts")
clock = pygame.time.Clock()

turn = 1
correct_turn = True

# Default window size
width = 800
height = 800


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

# board = [[1001, 12030, "hello", "BUGRER", 32, 3, 3, 3],
#          [1001, 12030, "hello", 23, 3, "e"],
#          [1001, 12030, "hello", 23, 3],
#          [1001, 12030, "hello", "BUGRER", 32, 3, 3, 3],
#          [1001, 12030, "hello"],
#          [1001, 12030, "hello", "BUGRER", 32, 3, 3, 3, 2, 56, "he", True, 3],
#          [1001, 12030, "hello", 23, 3, True],
#          [True, False, 12.2, False, True, False]]

# board = [
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 1],
#     [0, 0, 0, 3, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 3, 0, 0, 0, 0],
#     [0, 0, 0, 0, 1, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0]
#
# ]


# Changes player turn
def turn_change(turn):
    turn += 1
    if turn > 2:
        turn = 1
    return turn


# Checks if a player is out of pieces
def win_check():
    white = False
    black = False
    print("ROW BELOW")
    for row in board:
        for piece in row:
            if board[row][col - 1] == 1 or board[row][col - 1] == 2:
                white = True
            if board[row][col - 1] == 3 or board[row][col - 1] == 4:
                black = True

    if not white:
        return 1
    if not black:
        return 2

    return 0


# checks whether a piece will be kinged
def king_check():
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


def draw_window(win):
    colour = (255, 255, 255)
    x = 0
    y = 0

    # Drawing out board
    for row in board:
        for square in row:
            pygame.draw.rect(win, colour, (x, y, width / 8, height / 8))
            # Swapping colour
            if colour == (255, 255, 255):
                colour = (100, 160, 100)
            else:
                colour = (255, 255, 255)
            x += width / 8
        # Swapping colour again for next row
        if colour == (255, 255, 255):
            colour = (100, 160, 100)
        else:
            colour = (255, 255, 255)
        y += height / 8
        x = 0

    # Drawing pieces onto screen
    x = (width / 8) / 2
    y = (height / 8) / 2
    for row in board:
        for piece in row:
            if piece == 1:
                pygame.draw.circle(win, (255, 0, 0), (x, y), width / 20)
            elif piece == 2:
                pygame.draw.circle(win, (255, 255, 0), (x, y), width / 20)
            elif piece == 3:
                pygame.draw.circle(win, (0, 0, 255), (x, y), width / 20)
            elif piece == 4:
                pygame.draw.circle(win, (0, 255, 255), (x, y), width / 20)
            x += width / 8
        x = (width / 8) / 2
        y += height / 8

    pygame.display.update()


# Prints the board
def print_board():
    print("   0", " 1", " 2", " 3", " 4", " 5", " 6", " 7")
    count = 0
    for row in board:
        print(count, row)
        count += 1
    print()


#print_board()

selected = False
progress = False
run = True

while run:
    clock.tick(60)
    draw_window(win)

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
                end_col, end_row = mouse_x, mouse_y
                print(end_col, end_row)

                progress = True
            # If a piece has not been selected
            else:
                mouse_x = math.floor((mouse_x / (width / 8)))
                mouse_y = math.floor((mouse_y / (height / 8)))

                print(mouse_x, mouse_y)

                if board[mouse_y][mouse_x] != 0:
                    start_col, start_row = mouse_x, mouse_y
                    selected = True
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    # Checks whether an attempt at a move should be made
    if progress:
        print("turn:", turn, "start row:", start_row, "start col:", start_col, "piece:", board[start_row][start_col])
        print()
        # Checks whether it is moving the right piece for their turn
        if turn == 1:
            if board[start_row][start_col] != 1 and board[start_row][start_col] != 2:
                correct_turn = False
                print("Not piece in turn 1")
        else:
            if board[start_row][start_col] != 3 and board[start_row][start_col] != 4:
                correct_turn = False
                print("Not piece in turn 2")

        # Moves the piece
        if correct_turn:
            moving, double, direction, side, repeat = movement.move_check(board, start_row, start_col, end_row, end_col)
            # if the move was valid, change the turn
            if moving:
                board = movement.move(board, start_row, start_col, end_row, end_col, direction, side)
                if not double:
                    if not repeat:
                        turn = turn_change(turn)
                double = False
            # else don't change the turn
            else:
                print("Invalid move")

            #print_board()

        # resets the progress with clicking on a piece
        progress = False
        selected = False
        correct_turn = True

        # Checks if one player is out of pieces
        # if win_check() == 1:
        #     print("Black wins!")
        #     run = False
        # elif win_check() == 2:
        #     print("White wins!")
        #     run = False

        # Checks if a piece can be kinged
        king_check()

pygame.quit()
