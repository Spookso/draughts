import pygame, math, movement

pygame.init()

win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Draughts")
clock = pygame.time.Clock()

turn = 1
correct_turn = True

# board = [
#     [0, 3, 0, 3, 0, 3, 0, 3],
#     [3, 0, 3, 0, 3, 0, 3, 0],
#     [0, 3, 0, 3, 0, 3, 0, 3],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0],
#     [1, 0, 1, 0, 1, 0, 1, 0],
#     [0, 1, 0, 1, 0, 1, 0, 1],
#     [1, 0, 1, 0, 1, 0, 1, 0],
# ]

board = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],

]


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
    for row in board:
        for piece in row:
            if piece == 1 or piece == 2:
                white = True
            if piece == 3 or piece == 4:
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
            pygame.draw.rect(win, colour, (x, y, 100, 100))
            # Swapping colour
            if colour == (255, 255, 255):
                colour = (100, 160, 100)
            else:
                colour = (255, 255, 255)
            x += 100
        # Swapping colour again for next row
        if colour == (255, 255, 255):
            colour = (100, 160, 100)
        else:
            colour = (255, 255, 255)
        y += 100
        x = 0

    # Drawing pieces onto screen
    x = 50
    y = 50
    for row in board:
        for piece in row:
            if piece == 1:
                pygame.draw.circle(win, (255, 0, 0), (x, y), (40))
            elif piece == 2:
                pygame.draw.circle(win, (255, 255, 0), (x, y), (40))
            elif piece == 3:
                pygame.draw.circle(win, (0, 0, 255), (x, y), (40))
            elif piece == 4:
                pygame.draw.circle(win, (0, 255, 255), (x, y), (40))
            x += 100
        x = 50
        y += 100

    pygame.display.update()


# Prints the board
def print_board():
    print("   0", " 1", " 2", " 3", " 4", " 5", " 6", " 7")
    count = 0
    for row in board:
        print(count, row)
        count += 1
    print()


print_board()

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
                mouse_x = math.floor(mouse_x / 100)
                mouse_y = math.floor(mouse_y / 100)
                end_col, end_row = mouse_x, mouse_y

                progress = True
            # If a piece has not been selected
            else:
                mouse_x = math.floor(mouse_x / 100)
                mouse_y = math.floor(mouse_y / 100)

                if board[mouse_y][mouse_x] != 0:
                    start_col, start_row = mouse_x, mouse_y
                    selected = True

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
            moving, double, direction, side = movement.move_check(board, start_row, start_col, end_row, end_col)
            # if the move was valid, change the turn
            if moving:
                board = movement.move(board, start_row, start_col, end_row, end_col, direction, side)[0]
                if not double:
                    turn = turn_change(turn)
                double = False
            # else don't change the turn
            else:
                print("Invalid move")

            print_board()

        # resets the progress with clicking on a piece
        progress = False
        selected = False
        correct_turn = True

        # Checks if one player is out of pieces
        if win_check() == 1:
            print("Black wins!")
            run = False
        elif win_check() == 2:
            print("White wins!")
            run = False

        # Checks if a piece can be kinged
        king_check()

pygame.quit()
