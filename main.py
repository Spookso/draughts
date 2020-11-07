import pygame, math, movement, time, random

# Initiates the pygame library
pygame.init()

# Sets up a window of size 800 x 800 pixels with the tag 'resizable'
win = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
# Sets the caption for the window as "Draughts"
pygame.display.set_caption("Draughts")
# allows pygame.time.Clock() to be accessed easily
clock = pygame.time.Clock()

# Default window size
width = 800
height = 800

winner = 1

texts = []
buttons = []

pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

class Text():
    def __init__(self, x, y, writing, colour, size, is_bold, screen):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.colour = colour
        self.writing = writing
        self.size = size
        self.start_size = size
        self.is_bold = is_bold
        self.screen = screen
        self.update_size(800, 800)

    def update_size(self, width, height):
        self.size = round(self.start_size * (width / 800))
        self.x = round(self.start_x * (width / 800))
        self.y = round(self.start_y * (height / 800))
        self.font = pygame.font.SysFont('cambria', self.size, self.is_bold)

    def draw(self, win):
        current = self.font.render(self.writing, True, self.colour)
        win.blit(current, (self.x, self.y))


class Button():
    def __init__(self, x, y, width, height, text='', outline_colour=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.start_x = x
        self.start_y = y
        self.start_width = width
        self.start_height = height

        self.text = text
        self.text_size = round(width / 6)
        self.colour = (255, 253, 208)
        self.outline_colour = outline_colour

        self.clicked = False
        self.click_delay = 0

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False

    def highlight_check(self, mouse_pos):
        if self.click_delay <= 0:
            if self.is_over(mouse_pos):
                self.colour = (229, 203, 144)
                return True
            else:
                self.colour = (255, 253, 208)
        else:
            self.click_delay -= 1
        return False

    def click_darken(self):
        self.colour = (165, 144, 121)
        self.click_delay = 0
        self.clicked = True

    def update_size(self, width, height):
        self.width = round(self.start_width * (width / 800))
        self.height = round(self.start_height * (height / 800))
        self.x = round(self.start_x * (width / 800))
        self.y = round(self.start_y * (height / 800))
        self.text_size = round(self.width / 6)

    def draw(self, win):
        if self.outline_colour != False:
            pygame.draw.rect(win, self.outline_colour, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('cambria', self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))


def set_up():
    screen = 1
    ai = False
    ai_repeat = False
    double_ai = False
    work_row = None
    work_col = None

    selected = False
    progress = False
    saved_row, saved_col = 0, 0
    repeat = False

    turn = 1
    correct_turn = True

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

    return screen, ai, ai_repeat, work_col, work_row, selected, progress, saved_row, saved_col, repeat, turn, correct_turn, current_board, double_ai

def play_sound_effect(type):
    if type == 1:
        pygame.mixer.music.load("click_one.wav")
    else:
        pygame.mixer.music.load("click_two.wav")
    pygame.mixer.music.play()


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

def draw_window(win, board, width, height):
    if screen == 1:
        win.fill((255, 255, 255))
        for text in texts:
            if text.screen == 1:
                text.draw(win)
        pygame.draw.circle(win, (255, 0, 0), (160 * width / 800, 300 * height / 800), round(width / 18))
        pygame.draw.circle(win, (0, 0, 255), (240 * width / 800, 250 * height / 800), round(width / 18))
        pygame.draw.circle(win, (255, 0, 0), (320 * width / 800, 300 * height / 800), round(width / 18))
        pygame.draw.circle(win, (0, 0, 255), (400 * width / 800, 250 * height / 800), round(width / 18))
        pygame.draw.circle(win, (255, 0, 0), (480 * width / 800, 300 * height / 800), round(width / 18))
        pygame.draw.circle(win, (0, 0, 255), (560 * width / 800, 250 * height / 800), round(width / 18))
        pygame.draw.circle(win, (255, 0, 0), (640 * width / 800, 300 * height / 800), round(width / 18))

        for button in buttons:
            button.draw(win)
    elif screen == 2:
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

            if len(texts) > 1:
                texts[-1].draw(win)
    elif screen == 3:
        pass

    pygame.display.update()

screen, ai, ai_repeat, work_col, work_row, selected, progress, saved_row, saved_col, repeat, turn, correct_turn, current_board, double_ai = set_up()

texts.append(Text(110, 110, "English Draughts", (0, 0, 0), 100, False, 1))
p_button = Button(40, 500, 300, 80, "Player VS Player", (0, 0, 0))
ai_button = Button(460, 500, 300, 80, "Player VS AI", (0, 0, 0))
dai_button = Button(250, 650, 300, 80, "AI VS AI", (0, 0, 0))
buttons.append(p_button)
buttons.append(ai_button)
buttons.append(dai_button)

run = True
while run:
    clock.tick(60)
    keys = pygame.key.get_pressed()

    if screen == 2:
        if keys[pygame.K_ESCAPE]:
            if len(texts) > 1:
                texts.remove(texts[-1])
            screen, ai, ai_repeat, work_col, work_row, selected, progress, saved_row, saved_col, repeat, turn, correct_turn, current_board, double_ai = set_up()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    if screen == 1:
        for button in buttons:
            button.highlight_check((mouse_x, mouse_y))

        if p_button.clicked:
            screen = 2
            p_button.clicked = False
        elif ai_button.clicked:
            ai = True
            screen = 2
            ai_button.clicked = False
        elif dai_button.clicked:
            screen = 2
            ai = True
            double_ai = True
            dai_button.clicked = False

    for event in pygame.event.get():
        # quits game
        if event.type == pygame.QUIT:
            run = False

        # Checks if mouse is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if screen == 1:
                for button in buttons:
                    if button.highlight_check((mouse_x, mouse_y)):
                        button.click_darken()
            # If a piece is already selected
            elif screen == 2:
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
                        play_sound_effect(1)
        elif event.type == pygame.VIDEORESIZE:
            width, height = event.w, event.h
            surface = pygame.display.set_mode((width, height), pygame.RESIZABLE)

            for text in texts:
                text.update_size(width, height)
            for button in buttons:
                button.update_size(width, height)


    if turn == 2 and ai:
        progress = True
    if screen == 2 and double_ai:
        progress = True


    # Checks whether an attempt at a move should be made
    if progress:
        if turn == 1 and not double_ai:
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

        elif ai:
            if turn == 1:
                moveables = [1, 2]
            else:
                moveables = [3, 4]
            # problem with ai doing different double moves when moving multiple times
            # fix by cross checking again the work row and col that were saved already
            legal_moves = []
            weights = []
            start_row = 0
            if not ai_repeat:
                for start_row in range(0, 8):
                    for start_col in range(0, 8):
                        if current_board[start_row][start_col] in moveables:
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
                if len(texts) < 2:
                    texts.append(Text(200, 110, "Draw!", (0, 0, 0), 100, True, 1))
                correct_turn = False

        # moves the piece
        repeat = False
        if correct_turn:
            play_sound_effect(2)
            moving, double, direction, side, repeat = movement.move_check(current_board, start_row, start_col, end_row, end_col)
            # if the move was valid, change the turn
            if moving:
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

        # Checks if one player is out of pieces
        if len(texts) < 2:
            if win_check(current_board) == 1:
                texts.append(Text(200, 110, "Blue Wins!", (0, 0, 0), 100, True, 1))
            elif win_check(current_board) == 2:
                texts.append(Text(200, 110, "Red Wins!", (0, 0, 0), 100, True, 1))

        # Checks if a piece can be kinged
        king_check(current_board)
    draw_window(win, current_board, width, height)
pygame.quit()
