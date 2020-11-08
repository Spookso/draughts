# various python libraries are imported, as well as another python file, movement.py, which contains functions allowing pieces to move
import pygame, math, movement, time, random

# the pygame library in initiated
pygame.init()

# Sets up a window of size 800 x 800 pixels with the tag 'resizable', allowing for it to be scaled
win = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
# Sets the caption for the window as "Draughts"
pygame.display.set_caption("Draughts")

# Default window size of 800 x 800 is set to these variables controlling the width and height respectively
width = 800
height = 800

# The default winner is set to team one
winner = 1

# arrays containing all text and button objects respectively are declared
texts = []
buttons = []

# the pygame music player is initiated, and the volume is set to 50%
pygame.mixer.init()
pygame.mixer.music.set_volume(0.5)

# a class for text is declared
class Text():
    def __init__(self, x, y, writing, colour, size, is_bold, screen):
        # x and y coordinates on the screen
        self.x = x
        self.y = y
        # these are stored so that they can be scaled when the size of the interface is changed
        self.start_x = x
        self.start_y = y
        # the colour of the text, stored as a tuple made up of three values which can go from 0 to 255, representing the intensity of either red, green or blue
        self.colour = colour
        # the actual script that the text contains
        self.writing = writing
        # the font size of the text
        self.size = size
        # this is stored for the same reason as the inital x and y coordinates
        self.start_size = size
        # whether the text is bolded
        self.is_bold = is_bold
        # the screen (main menu or on the board) that the text should be displayed on
        self.screen = screen

        # the update size function is run for the first time
        self.update_size(800, 800)

    # this function updates the size of the text and its position when the window is rescaled
    def update_size(self, width, height): # the new width and height of the screen are taken as arguments
        # the size and x and y coordinates of the text are multiplied by the current width of the screen / 800, the original width
        # This allows the text to change position and size relative to the change in the window size
        self.size = round(self.start_size * (width / 800))
        self.x = round(self.start_x * (width / 800))
        self.y = round(self.start_y * (height / 800))

        # a pygame 'font' is created, or in other words a template for a piece of text containing the font, size and whether it is bolded
        self.font = pygame.font.SysFont('cambria', self.size, self.is_bold)

    # this function draws the text into the screen
    def draw(self, win):
        # the text is 'rendered' with the actual writing, whether it is anti-aliased, and its colour, and then drawn onto the screen
        win.blit(self.font.render(self.writing, True, self.colour), (self.x, self.y))

# a class for buttons is declared
class Button():
    def __init__(self, x, y, width, height, text='', outline_colour=False): # by default, the text is set to be a blank string, and the outline colour is simply set to false
        # the x,y coordinates, width and height of the button itself
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        # these values are saved so that they can be scaled when the size of the interface is changed
        self.start_x = x
        self.start_y = y
        self.start_width = width
        self.start_height = height

        # the writing of the text
        self.text = text
        # the font size of the text is set to be 1/8th of the width of the button
        self.text_size = round(width / 8)
        # the colour is set to this rgb code
        self.colour = (255, 253, 208)
        self.outline_colour = outline_colour

        # the button begins having not been clicked
        self.clicked = False
        # a small delay is used so that the button can briefly darken when clicked
        self.click_delay = 0

    # this function checks whether the mouse is over the button
    def is_over(self, pos): # 'pos' contains both the x and y coordinates of the mouse on the screen
        if pos[0] > self.x and pos[0] < self.x + self.width: # if the x coordinate is between the start and end of the button
            if pos[1] > self.y and pos[1] < self.y + self.height:# if the y coordinate is between the top and bottom of the button
                return True # if the mouse is over the button, the function returns True

        return False # otherwise, it returns False

    # this function checks if the button should be darkened, and if so does so
    def highlight_check(self, mouse_pos): # the mouse position, containing an x and y coordinate is given as an argument
        if self.click_delay <= 0: # if the button has not been clicked very recently
            if self.is_over(mouse_pos): # if the mouse is over the button
                self.colour = (229, 203, 144) # the colour of the button is changed to a darker value
                return True
            else:
                self.colour = (255, 253, 208) # the colour is set back to the original value
        else:
            self.click_delay -= 1 # the click delay is reduced by one
        return False

    # this function simply darkens the button when it is clicked on
    def click_darken(self):
        self.colour = (165, 144, 121) # the colour of the button is set to an even darker value
        self.click_delay = 0
        self.clicked = True # .clicked is set to True, as the button has been clicked on

    # this function updates the size of the button and its position when the window is rescaled
    def update_size(self, width, height):
        # all of this is the same with the text, so see the comments within the text class's update_size function for an explanation of how it works
        self.width = round(self.start_width * (width / 800))
        self.height = round(self.start_height * (height / 800))
        self.x = round(self.start_x * (width / 800))
        self.y = round(self.start_y * (height / 800))
        self.text_size = round(self.width / 8)

    # this function draws the button onto the screen
    def draw(self, win):
        if self.outline_colour != False: # if the button should have an outline
            # a pygame rect object is draw onto the screen, containing the outline_colour. It is made slightly wider than the button, and its 'width' value is set to zero, making filled in. This means that the button can be drawn over the top, creating an outline of it.
            pygame.draw.rect(win, self.outline_colour, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        # the button itself is draw, with its own colour, and its x, y coordinates, and with its width and height. It is filled in fully
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text != '': # if the button should have text
            # the text is set up and drawn onto the middle of the button by taking half of the width of the text and subtracting it from the middle point of the button. The same is done with the height.
            font = pygame.font.SysFont('cambria', self.text_size)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

# This function re-initialises all of the variables once the game should restart
def set_up():
    # the screen is set back to 1, the main menu
    screen = 1
    # by defult the ai is turned off
    ai = False
    first_move = True
    double_ai = False

    # these values stored whether a piece hass been selected to move
    selected = False
    progress = False
    saved_row, saved_col = 0, 0
    repeat = False

    # the turn is set to 1, the first player
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

    # all of these values are returned back
    return screen, ai, selected, progress, saved_row, saved_col, repeat, turn, correct_turn, current_board, double_ai, first_move

# this function loads and plays the sound effects
def play_sound_effect(type):
    if type == 1: # if a piece is being clicked on
        pygame.mixer.music.load("click_one.wav") # the sound effect, located in the same directory as the code files is loaded
    else: # otherwise if a move is being made
        pygame.mixer.music.load("click_two.wav") # the sound effect, located in the same directory as the code files is loaded
    pygame.mixer.music.play() # the sound effect is played once, and not looped


# this function simply changes which turn it is after a move has been played
def turn_change(turn):
    turn += 1
    if turn > 2:
        turn = 1
    return turn


# this function checks if a player is out of pieces
def win_check(board):
    # by default both teams are set to have no pieces
    red = True
    blue = True
    for row in board: # for every 'row' array in the 2D board array
        for piece in row: # for every piece in the row, this can be either a 0, 1, 2, 3 or 4
            if piece == 1 or piece == 2: # if the piece is a 1 or 2, being a piece on team red
                red = False
            elif piece == 3 or piece == 4: # if the piece is a 3 or 4, being a piece on team blue
                blue = False

    # if either teams are out of pieces, a number, either 1 or 2 is returned
    if red:
        return 1
    if blue:
        return 2
    # otherwise 0 is returned
    return 0


# this function checks whether a piece can be kinged. This can happen when a piece gets to the opposite end of the board
def king_check(board):
    column = 0
    for piece in board[0]: # this is the first row, at the top of the board
        if piece == 1: # if the piece is a non-kinged piece on the red team
            board[0][column] = 2 # it becomes a kinged piece
        column += 1
    column = 0
    for piece in board[7]: # this is the last row, at the bottom of the board
        if piece == 3: # if the piece is a non-kinged piece on the blue team
            board[7][column] = 4 # it becomes a kinged piece
        column += 1

# this function draws everything onto the graphical screen
def draw_window(win, board, width, height):
    # if the user is on the main menu
    if screen == 1:
        # the window is filled with the colour white
        win.fill((255, 255, 255))

        # every text's draw function is run
        for text in texts:
            if text.screen == 1: # if the text should be drawn onto the main menu
                text.draw(win)

        # a number of circles, resembling game pieces are drawn onto the screen
        # this is purely asthetic to make the menu screen look a bit nicer
        # Some are blue (0, 0, 255), and some are red (255, 0, 0), and they are all the same size, and drawn 80 pixels apart. They also alternate going up and down in height
        pygame.draw.circle(win, (255, 0, 0), (round(160 * width / 800), round(300 * height / 800)), round(width / 18))
        pygame.draw.circle(win, (0, 0, 255), (round(240 * width / 800), round(250 * height / 800)), round(width / 18))
        pygame.draw.circle(win, (255, 0, 0), (round(320 * width / 800), round(300 * height / 800)), round(width / 18))
        pygame.draw.circle(win, (0, 0, 255), (round(400 * width / 800), round(250 * height / 800)), round(width / 18))
        pygame.draw.circle(win, (255, 0, 0), (round(480 * width / 800), round(300 * height / 800)), round(width / 18))
        pygame.draw.circle(win, (0, 0, 255), (round(560 * width / 800), round(250 * height / 800)), round(width / 18))
        pygame.draw.circle(win, (255, 0, 0), (round(620 * width / 800), round(300 * height / 800)), round(width / 18))

        # every button is drawn onto the screen
        for button in buttons:
            button.draw(win)

    # if the user is on the second screen, which is the game board
    elif screen == 2:
        # the colour for the squares of the board is set to white
        colour = (255, 255, 255)
        # the x and y values of each square is set initally to 0 for the first square
        # in pygame, 0 for both the x and y is the top left corner, with the y value increasing downwards, and the x value increasing rightwards
        x = 0
        y = 0

        # the board is drawn out
        for row in board:
            for square in row:
                pygame.draw.rect(win, colour, (x, y, round(width / 8), round(height / 8))) # a square is drawn onto the screen. It is an eighth of the total screen height and width, so that a perfect 8 x 8 grid can be made
                # the colours of the squares alternate between white and pale green
                if colour == (255, 255, 255):
                    colour = (100, 160, 100) # the green colour
                else:
                    colour = (255, 255, 255) # the white colour
                x += round(width / 8) # the x value is increased

            # the colours a swapped one more time when moving to the next rrow
            if colour == (255, 255, 255):
                colour = (100, 160, 100)
            else:
                colour = (255, 255, 255)
            # the x value is set back to zero for the next row, while the y value increases
            y += round(height / 8)
            x = 0

        # Here the actual pieces are drawn onto the board

        # the first piece is placed right in the centre of the first square, which is one eigth the size of the whole screen
        # it is put in the centre because the pygame.draw.circle function draws the circles outwards from the x and y coordinate given
        x = round((width / 8) / 2)
        y = round((height / 8) / 2)
        for row in board:
            for piece in row:
                if piece == 1:
                    pygame.draw.circle(win, (255, 0, 0), (x, y), round(width / 20)) # a red piece
                elif piece == 2:
                    pygame.draw.circle(win, (255, 255, 0), (x, y), round(width / 20)) # yellow, kinged piece (still on the red team)
                elif piece == 3:
                    pygame.draw.circle(win, (0, 0, 255), (x, y), round(width / 20)) # a dark blue piece
                elif piece == 4:
                    pygame.draw.circle(win, (0, 255, 255), (x, y), round(width / 20)) # a lighter, kinged blue piece (also on the blue team)
                x += round(width / 8)
            x = round((width / 8) / 2)
            y += round(height / 8)

            # if there are more than one text objects, the latest one is drawn
            # when one team wins, an extra text object is created announcing the winner. Only in this case should text be drawn onto the board screen
            if len(texts) > 1:
                texts[-1].draw(win)

    # the actual display is now updated with all of the changes made above
    pygame.display.update()

# all of the variables are initialised for the first time as shown above
screen, ai, selected, progress, saved_row, saved_col, repeat, turn, correct_turn, current_board, double_ai, first_move = set_up()

# a title text is created
texts.append(Text(82, 80, "English Draughts", (0, 0, 0), 80, False, 1))
# this button allows the player to choose the player vs player mode
p_button = Button(40, 500, 300, 80, "Player VS Player", (0, 0, 0))
# this button allows the player to choose the player vs ai mode
ai_button = Button(460, 500, 300, 80, "Player VS AI", (0, 0, 0))
# this button allows the player to choose the ai vs ai mode
dai_button = Button(250, 650, 300, 80, "AI VS AI", (0, 0, 0))

# all of the buttons are appended to the list of button objects
buttons.append(p_button)
buttons.append(ai_button)
buttons.append(dai_button)

# this is the main game loop which continuously runs
# once run is set to false, the game stops
run = True
while run:
    # the loop is set to repeat exactly 60 times a second, which ensures that the game does not run too fast
    pygame.time.Clock().tick(60)

    # this contains information on whether any key on the keyboard is being pressed
    keys = pygame.key.get_pressed()

    if screen == 2: # if the user is on the board screen
        if keys[pygame.K_ESCAPE]: # if the escape key is pressed
            if len(texts) > 1: # if there is a text object announcing the winner
                texts.remove(texts[-1]) # it is removed
            # all of the variables are reset, including the screen, taking the user back to the main menu
            screen, ai, selected, progress, saved_row, saved_col, repeat, turn, correct_turn, current_board, double_ai, first_move = set_up()

    # the current x and y coordinates of the mouse are obtained
    mouse_x, mouse_y = pygame.mouse.get_pos()

    if screen == 1: # on the menu screen

        # all of the buttons check if they should darken
        for button in buttons:
            button.highlight_check((mouse_x, mouse_y))

        # if any of the buttons are clicked, the screen is set to 2 and they are set to no longer be clicked
        if p_button.clicked:
            screen = 2
            p_button.clicked = False
        elif ai_button.clicked:
            ai = True # the ai variable is also set to true, as the user chose the player vs ai mode
            screen = 2
            ai_button.clicked = False
        elif dai_button.clicked:
            screen = 2
            ai = True
            double_ai = True # the double_ai variable is also set to true, as the user chose the ai vs ai mode
            dai_button.clicked = False

    # this checks for various 'events' that pygame can detect, including the mouse being clicked, game window being resized, 'x' button to close the game beiojng clicked, etc
    for event in pygame.event.get():

        if event.type == pygame.QUIT: # if the 'x' button is clicked to close the game window
            run = False # run is set to false, meaning the game loop with no longer repeat

        if event.type == pygame.MOUSEBUTTONDOWN: # if the mouse is clicked down (this can be a left click or right click)
            if screen == 1: # if on the menu
                for button in buttons: # all of the button objects run checks to see if the mouse is also over them
                    if button.highlight_check((mouse_x, mouse_y)):
                        button.click_darken() # if the mouse is over a button and it was just clicked, then the button must have been clicked, and so this function is run


            elif screen == 2: # otherwise if on the board screen
                if selected: # if a piece has already been selected by the user to be moved
                    # the mouse x and y values are divided by the size of each square of the board, and then rounded down using the math.floor function
                    # this effectively makes these values into an index value between 0 and 7 of the row and column that the user has clicked on
                    mouse_x = math.floor((mouse_x / (width / 8)))
                    mouse_y = math.floor((mouse_y / (height / 8)))
                    if repeat: # if it is consecutive move, it is ensured that the piece is capturing another piece
                        if start_row == mouse_y + 2 or start_row == mouse_y - 2: # the piece is moving two squares in some direction
                            end_col, end_row = mouse_x, mouse_y # the ending coordinates (between 0 and 7 for the row and column) of the pieces are assigned as the new rounded mouse coordinates
                    else:
                        end_col, end_row = mouse_x, mouse_y # the ending coordinates (between 0 and 7 for the row and column) of the pieces are assigned as the new rounded mouse coordinates
                    progress = True # progress is set to true, meaning that both start coordinates and end coordinates for the piece have been made, and allowing the movement of the piece to progress to the next step

                else: # otherwise if a piece has not yet been selected
                    # the same thing is done as explained above
                    mouse_x = math.floor((mouse_x / (width / 8)))
                    mouse_y = math.floor((mouse_y / (height / 8)))

                    if current_board[mouse_y][mouse_x] != 0: # if the user has clicked on a square with a piece (0 means that the square is empty)
                        if repeat: # if it is a consecutive move, it must be the same piece which is moving
                            if mouse_y == saved_row and mouse_x == saved_col: # if the piece selected is in the ending location of the last move
                                start_col, start_row = mouse_x, mouse_y # the start coordinates (between 0 and 7 for the row and column) of the pieces are assigned as the new rounded mouse coordinates
                        else:
                            start_col, start_row = mouse_x, mouse_y # the start coordinates (between 0 and 7 for the row and column) of the pieces are assigned as the new rounded mouse coordinates
                        selected = True # as a piece has been selected, the process can move to the next step; note that this also happens if no piece is selected and the board is simply clicked on, however that is addressed later
                        play_sound_effect(1) # the sound effect playing function is called, with the type set to one, meaning that the first sound effect is played

        if event.type == pygame.VIDEORESIZE: # if the window is being resized
            width, height = event.w, event.h # the width and height are set to the new width and height after the window is resized

            # all text and button objects update their sizes and positions relative to the new width and height of the window
            for text in texts:
                text.update_size(width, height)
            for button in buttons:
                button.update_size(width, height)

    # if it is the ai's turn, the code requiring a piece to be clicked on is skipped
    if turn == 2 and ai:
        progress = True
    # if the user chose the ai vs ai mode, then regardless of the turn, the code requiring a piece to be clicked on is skipped
    if screen == 2 and double_ai:
        progress = True

    if progress: # if the starting and ending coordinates for the piece have all been chosen

        # this code checks that the user has selected one of their own pieces and not one of their opponents
        if turn == 1 and not double_ai: # this is skipped if the ai controls player one
            if current_board[start_row][start_col] != 1 and current_board[start_row][start_col] != 2:
                correct_turn = False
        elif turn == 2 and not ai: # this is skipped if the ai controls player two
            if current_board[start_row][start_col] != 3 and current_board[start_row][start_col] != 4:
                correct_turn = False

        # all of this code allows the ai to calculate a move
        elif ai:
            if turn == 1: # if it is the first players turn
                moveables = [1, 2] # the 'moveables' array is set to contain the piece types that the first player can move
                king_row = 0 # the 'kingrow' variable is set to the row that the first player has to move a piece to to king it
            else: # if it is the second player's turn
                moveables = [3, 4] # the 'moveables' array is set to contain the piece types that the second player can move
                king_row = 7 # the 'kingrow' variable is set to the row that the second player has to move a piece to to king it
            legal_moves = [] # an array that will contain all of the information about legal moves that the ai can make is declared
            weights = [] # a parrell array to the legal moves is also declared, which contains the probability weightings that will select a move from
            # for every piece on the board
            if not repeat:  # if the ai is not doing a second consecutive move
                for start_row in range(0, 8):
                    for start_col in range(0, 8):
                        if current_board[start_row][start_col] in moveables: # if the ai is allowed to move it
                            # for every square on the board
                            for end_row in range(0, 8):
                                for end_col in range(0, 8):
                                    # all of the information about the move is stored
                                    move_check_info = movement.move_check(current_board, start_row, start_col, end_row, end_col)
                                    if move_check_info[0]: # if the 'moving' variable is true, or in other words the function has determined that the move is legal
                                        weight = 0 # the weighting of the move is set to zero
                                        # information about the move, including the starting coordinates, ending coordinates, and the direction, both vertically and horizontally that the piece is moving in is all together stored as an array inside the array containing the legal moves
                                        legal_moves.append([start_row, start_col, end_row, end_col, move_check_info[2], move_check_info[3]])

                                        # if either an unkinged piece is moving into the final row, or the move captures an opponents piece, the weighting of that move is increased significantly
                                        # this effectively means that the ai will always choose to take a piece or king a piece if it can
                                        if end_row == king_row and current_board[start_row][start_col] == moveables[0]:
                                            weight += 100
                                        if move_check_info[1]:
                                            weight += 100
                                        weight += 0.1 # the weighting is increased for all moves
                                        weights.append(weight) # the weighting is appended to the array of weights

            else: # if the ai is doing a second consecutive move
                # all of the code here is that same as above, except that the saved ending coordinates from the last move are used as new starting coordinates, as the same piece must move
                # these are saved after a move is made where a consecutive move can be performed
                for end_row in range(0, 8):
                    for end_col in range(0, 8):
                        move_check_info = movement.move_check(current_board, saved_row, saved_col, end_row, end_col)
                        if move_check_info[0]:
                            weight = 0
                            legal_moves.append([saved_row, saved_col, end_row, end_col, move_check_info[2], move_check_info[3]])

                            if end_row == king_row and current_board[saved_row][saved_col] == moveables[0]:
                                weight += 100
                            if move_check_info[1]:
                                weight += 100
                            weight += 0.1
                            weights.append(weight)

            try: # attempts to perform a move
                # this code prevents the ai from making a move as soon as the new board is loaded once the user clicks the ai vs ai button
                if double_ai:
                    if first_move and screen == 2: # if it is the ai's very first move
                        draw_window(win, current_board, width, height) # the screen is refreshed early so that the board can be seen before the first move is made
                        first_move = False

                time.sleep(0.6) # the program pauses for .6 seconds to prevent the moves from happening too fast
                selection = random.choices(legal_moves, weights) # a random, albeit weighted choice is made from the selection of legal moves that were found earlier
                correct_turn = True # the program is now able to continue with the move
                start_row, start_col, end_row, end_col, direction, side = selection[0] # the coordinates of the movements and other bits of information and set to the choice made

            except: # if this fails, then there are no legal moves, and so it is a draw
                if len(texts) < 2: # if text has not already been added
                    texts.append(Text(200, 110, "Draw!", (0, 0, 0), 100, True, 1)) # text is added declaring that it is a draw
                correct_turn = False

        if correct_turn: # if all of the information for the move has been found, and the piece that was selected is on the right team
            play_sound_effect(2) # the sound effect playing function is called, with the type set to two, meaning that the second sound effect is played
            moving, double, direction, side = movement.move_check(current_board, start_row, start_col, end_row, end_col) # meta information about the move is calculated, including whether it is legal and if it captures a piece

            if moving: # if the move is legal
                current_board = movement.move(current_board, start_row, start_col, end_row, end_col, direction, side) # the current board is updated, with the new move being performed on it

                if double: # if the move captured a piece, a check is performed to see if it can move again
                    repeat, saved_row, saved_col = movement.double_move_check(current_board, end_row, end_col, direction, side) # here the ending coordinates of the piece that just moved are also saved

                if not repeat: # if the piece cannot move again
                    turn = turn_change(turn) # the turn is changed, meaning that it is the next player's go\

        # all of these values are reset, regardless of whether a move was performed or not
        # in the case of the latter, the player can then reselect a new piece and choose a new square for it to move to
        progress = False
        selected = False
        correct_turn = True

        # Checks if one player is out of pieces
        if len(texts) < 2: # if some decision about the conclusion of the game, signified by a text object being created, has not already happened
            if win_check(current_board) == 1: # if red team has no more pieces left
                texts.append(Text(150, 110, "Blue Wins!", (0, 0, 0), 100, True, 1)) # text is added declaring that the blue team won
            elif win_check(current_board) == 2: # if blue team has no more pieces left
                texts.append(Text(150, 110, "Red Wins!", (0, 0, 0), 100, True, 1)) # text is added declaring that the red team won

        print(repeat)

        king_check(current_board) # checks if any pieces can be kinged
    draw_window(win, current_board, width, height) # the game window is updated

# this is only reachable once the main loop has stopped running
pygame.quit() # the pygame library is shut down
