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

screen = 2

ai = True
random_ai = True
ai_repeat = False
calculated = False
print("ai true")

work_row = None
work_col = None

start_row = 0

# texts = []


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

class text():
    def __init__(self, x, y, writing, size, is_bold):
        self.x = x
        self.y = y
        self.size = size
        self.is_bold = is_bold
        self.size_ratio = 1
        self.font = pygame.font.SysFont('cambria', self.size, self.is_bold)

    def update_size(self, old, new):
        self.size_ratio = new/old
        self.size *= self.size_ratio
        self.x *= self.size_ratio
        self.y *= self.size_ratio

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

def score_board(board):
    score = 0
    for row in board:
        for piece in row:
            if piece == 3:
                score += 1
            elif piece == 4:
                score += 2
            elif piece == 1:
                score -= 1
            elif piece == 2:
                score -= 2

    return score

def draw_window(win, board):
    # if screen == 1:
    #     for text in texts:
    #         current = font.render(text.writing, 1, (0, 0, 0))
    #         # add colour for texts
    #         # fix this
    #     win.fill((255, 255, 255))
    #     win.blit(title, (font_x * font_size_ratio, font_y * font_size_ratio))
    if screen == 2:
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

# texts.append(text(110, 110, 100, False))

run = True
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        # quits game
        if event.type == pygame.QUIT:
            run = False

        # Checks if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If a piece is already selected
            if screen == 2:
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
            # for text in texts:
            #     text.update_size(width, event.width)
            width, height = event.w, event.h
            surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

    if turn == 2 and ai:
        progress = True


    # Checks whether an attempt at a move should be made
    if progress:
        if turn == 1:
            # print("turn:", turn, "start row:", start_row, "start col:", start_col, "piece:", current_board[start_row][start_col])
            # print()
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
            weights = []
            start_row = 0
            if not ai_repeat:
                for start_row in range(0, 8):
                    for start_col in range(0, 8):
                        if current_board[start_row][start_col] in [3, 4]:
                            for end_row in range(0, 8):
                                for end_col in range(0, 8):
                                    move_check_info = movement.move_check(current_board, start_row, start_col, end_row, end_col)
                                    if move_check_info[0]:
                                        weight = 0
                                        legal_moves.append([start_row, start_col, end_row, end_col, move_check_info[2], move_check_info[3]])
                                        if end_row == 8 and current_board[start_row][start_col] == 3:
                                            weight += 100
                                        if move_check_info[1]:
                                            weight += 100
                                        weight += 0.1
                                        weights.append(weight)
            else:
                start_row, start_col = saved
                for end_row in range(0, 8):
                    for end_col in range(0, 8):
                        move_check_info = movement.move_check(current_board, start_row, start_col, end_row, end_col)
                        if move_check_info[0]:
                            weight = 0
                            legal_moves.append([start_row, start_col, end_row, end_col, move_check_info[2], move_check_info[3]])
                            if end_row == 8:
                                weight += 0.4
                            if move_check_info[1]:
                                weight += 0.4
                            weight += 0.1
                            weights.append(weight)

            try:
                time.sleep(0.4)
                selection = random.choices(legal_moves, weights)
                print(selection)
                correct_turn = True
                progress = False
                start_row, start_col, end_row, end_col, direction, side = selection[0]
                ai_repeat = False
                if movement.move_check(current_board, start_row, start_col, end_row, end_col)[4]:
                    ai_repeat = True
                    saved = [end_row, end_col]

            except:
                print("NO MOVES")
                correct_turn = False

        # moves the piece
        repeat = False
        if correct_turn:
            moving, double, direction, side, repeat = movement.move_check(current_board, start_row, start_col, end_row, end_col)
            # if the move was valid, change the turn
            if moving:
                movelist.append([start_row, start_col, end_row, end_col, direction, side])
                print(movelist)
                current_board = movement.move(current_board, start_row, start_col, end_row, end_col, direction, side)
                # if the move was a piece taking move, check if it can move again
                if double:
                    repeat, saved_col, saved_row, work_row, work_col = movement.double_move_check(current_board, end_row, end_col, direction, side)

                if not repeat:
                    turn = turn_change(turn)
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
