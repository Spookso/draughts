import pygame, math
pygame.init()

win = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Draughts")
clock = pygame.time.Clock()

turn = 1

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
    [0, 3, 0, 3, 0, 3, 0, 3],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0],
]

def move(row, col, direction, side):

    #If it is a normal piece, sets direction to forward
    if board[row][col] == 1:
        direction = -1
    if board[row][col] == 3:
        direction = 1

    #checks to see that the piece is not trying to move out of bounds
    if error_check(row, direction):
        return False
    if error_check(col, side):
        return False

    #moves the piece one space
    if board[row + direction][col + side] == 0:
        board[row + direction][col + side] = board[row][col]
        board[row][col] = 0

    #tries to jumps piece over another piece
    elif board[row + direction][col + side] != board[row][col]:
        #checks that the piece it is jumping over is on the other team
        if board[row][col] - 1 == 0 or board[row][col] - 1 == 2:
            if board[row + direction][col + side] == board[row][col] + 1:
                return False
        else:
            if board[row + direction][col + side] == board[row][col] - 1:
                return False

        #checks to see that the piece is not trying to move out of bounds
        if error_check(row, direction + direction):
            return False
        elif error_check(col, side + side):
            return False

        #actually jumps piece
        else:
            if board[row + direction + direction][col + side + side] == 0:
                board[row + direction][col + side] = 0
                board[row + direction + direction][col + side + side] = board[row][col]
                board[row][col] = 0

    return True


def error_check(pos, increase):
    if pos + increase < 0 or pos + increase > 7:
        return True

#Changes player turn
def turn_change():
    global turn
    turn += 1
    if turn > 2:
        turn = 1

#Checks if a player is out of pieces
def win_check():
    white = False
    black = False
    for row in board:
        for piece in row:
            if piece == 1 or piece == 2:
                white = True
            if piece == 3 or piece == 4:
                black = True

    if white == False:
        return 1
    if black == False:
        return 2

    return 0

def king_check():
    num = 0
    for piece in board[0]:
        if piece == 1:
            board[0][num] = 2
        num += 1
    num = 0
    for piece in board[7]:
        if piece == 3:
            board[0][num] = 4
        num += 1

def draw_window(win):
    colour = (255, 255, 255)
    x = 0
    y = 0

    #Drawing out board
    for row in board:
        for square in row:
            pygame.draw.rect(win, colour, (x, y, 100, 100))
            #Swapping colour
            if colour == (255, 255, 255):
                colour = (100, 160, 100)
            else:
                colour = (255, 255, 255)
            x += 100
        #Swapping colour again for next row
        if colour == (255, 255, 255):
            colour = (100, 160, 100)
        else:
            colour = (255, 255, 255)
        y += 100
        x = 0

    #Drawing pieces onto screen
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

#Prints the board
print("   1", " 2", " 3", " 4", " 5", " 6", " 7", " 8")
count = 1
for row in board:
    print(count, row)
    count += 1

print()

selected = False
progress = False
run = True

while run:
    clock.tick(60)
    draw_window(win)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    for event in pygame.event.get():
        #quits game
        if event.type == pygame.QUIT:
            run = False
        #Checks if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            #If a piece is already selected
            if selected:
                print(row)
                print(math.floor(mouse_y / 100)8)
                if math.floor(mouse_x / 100) > col:
                    side = 1
                else:
                    side = -1

                if math.floor(mouse_y / 100) > row:
                    direction = -1
                else:
                    direction = 1

                progress = True
            #If a piece has not been selected
            else:
                mouse_x = math.floor(mouse_x / 100)
                mouse_y = math.floor(mouse_y / 100)

                if board[mouse_y][mouse_x] != 0:
                    col, row = mouse_x, mouse_y
                    selected = True

    #Checks whether an attempt at a move has been made
    if progress:
        #Checks whether it is moving the right piece for their turn
        if turn != board[row][col] and turn + 1 != board[row][col]:
            print("Error not your turn")
        else:
            #Moves the piece
            if move(row, col, direction, side):
                turn_change()
            else:
                print("Invalid move")

        #Checks if one player is out of pieces
        if win_check() == 1:
            print("Black wins!")
            run = False
        elif win_check() == 2:
            print("White wins!")
            run = False

        # Prints the new board
        # print("   1", " 2", " 3", " 4", " 5", " 6", " 7", " 8")
        # count = 1
        # for row in board:
        #     print(count, row)
        #     count += 1
        # print()

        progress = False
        selected = False

        #Checks if a piece can be kinged
        king_check()

pygame.quit()
