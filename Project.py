from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time


# Global Variables-----------------------------------------------------------------------------------------------------------------------------

camera_pos = (0,500,800)
fovY = 120
grid_start = -800
white = (0.8, 0.8, 0.8)
black = (0.4, 0.4, 0.4)
pointer = [100, 100]
menu = True
turn = True
selected_piece = None
game_over = False
white_draw = False
black_draw = False
draw_flag = False
resign_flag = False
top_down_view = False
white_wins = False
black_wins = False
captured_black = []
captured_white = []
black_capture_count = 0
white_capture_count = 0
white_time = 60
black_time = 60
last_time = time.time()
king_in_check = False
checkmate = False
last_move_message = "Last Move: No moves yet"

board_label = [
    (8,"A", 700, -700), (8,"B", 500, -700), (8,"C", 300, -700), (8,"D", 100, -700), (8,"E", -100, -700), (8,"F", -300, -700), (8,"G", -500, -700), (8,"H", -700, -700),
    (7,"A", 700, -500), (7,"B", 500, -500), (7,"C", 300, -500), (7,"D", 100, -500), (7,"E", -100, -500), (7,"F", -300, -500), (7,"G", -500, -500), (7,"H", -700, -500),
    (6,"A", 700, -300), (6,"B", 500, -300), (6,"C", 300, -300), (6,"D", 100, -300), (6,"E", -100, -300), (6,"F", -300, -300), (6,"G", -500, -300), (6,"H", -700, -300),
    (5,"A", 700, -100), (5,"B", 500, -100), (5,"C", 300, -100), (5,"D", 100, -100), (5,"E", -100, -100), (5,"F", -300, -100), (5,"G", -500, -100), (5,"H", -700, -100),
    (4,"A", 700, 100), (4,"B", 500, 100), (4,"C", 300, 100), (4,"D", 100, 100), (4,"E", -100, 100), (4,"F", -300, 100), (4,"G", -500, 100), (4,"H", -700, 100),
    (3,"A", 700, 300), (3,"B", 500, 300), (3,"C", 300, 300), (3,"D", 100, 300), (3,"E", -100, 300), (3,"F", -300, 300), (3,"G", -500, 300), (3,"H", -700, 300),
    (2,"A", 700, 500), (2,"B", 500, 500), (2,"C", 300, 500), (2,"D", 100, 500), (2,"E", -100, 500), (2,"F", -300, 500), (2,"G", -500, 500), (2,"H", -700, 500),
    (1,"A", 700, 700), (1,"B", 500, 700), (1,"C", 300, 700), (1,"D", 100, 700), (1,"E", -100, 700), (1,"F", -300, 700), (1,"G", -500, 700), (1,"H", -700, 700)]



# Classes for Chess Pieces-------------------------------------------------------------------------------------------------------------------

class Chess_Piece:
    def __init__(self, name, position_x, position_y, color):
        self.name = name
        self.color = color
        self.x = position_x
        self.y = position_y
        self.initial_x = position_x
        self.initial_y = position_y

    def move(self, new_x, new_y):
        global last_move_message
        self.x = new_x
        self.y = new_y
        for row, col, x, y in board_label:
            if (x, y) == (self.x, self.y):
                print(f"{self.name} moved to {col}{row}")
                last_move_message = f"Last Move: {self.name} moved to {col}{row}"
                break

    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y

    def is_valid_move(self, new_x, new_y):
        return False

    def is_path_clear(self, new_x, new_y):
        dx = 0 if new_x == self.x else (1 if new_x > self.x else -1)
        dy = 0 if new_y == self.y else (1 if new_y > self.y else -1)
        current_x, current_y = self.x + dx * 200, self.y + dy * 200
        while current_x != new_x or current_y != new_y:
            if get_piece_at(current_x, current_y):
                return False
            current_x += dx * 200
            current_y += dy * 200
        return True

    def draw(self):
        pass


class Pawn(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} Pawn"
        super().__init__(name, position_x, position_y, color)

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 50)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glTranslatef(0, 0, -50)
        gluCylinder(gluNewQuadric(), 40, 10, 50, 10, 10)
        glPopMatrix()

    def is_valid_move(self, new_x, new_y):
        dx = new_x - self.x
        dy = new_y - self.y
        direction = -200 if self.color == white else 200
        # Forward Movement
        if dx == 0:
            # One Step
            if dy == direction:
                return not get_piece_at(new_x, new_y)
            # Two Steps at Start
            elif dy == 2 * direction and ((self.color == white and self.y == 500) or (self.color == black and self.y == -500)):
                return not get_piece_at(new_x, new_y) and not get_piece_at(new_x, self.y + direction)
        # Diagonal Capture
        elif abs(dx) == 200 and dy == direction:
            target_piece = get_piece_at(new_x, new_y)
            return target_piece and target_piece.color != self.color
        return False


class Bishop(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} Bishop"
        super().__init__(name, position_x, position_y, color)

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        gluCylinder(gluNewQuadric(), 40, 10, 100, 10, 10)
        glTranslatef(0, 0, 100)
        gluCylinder(gluNewQuadric(), 20, 0, 40, 10, 10)
        glPopMatrix()

    def is_valid_move(self, new_x, new_y):
        # Diagonal Movement
        dx = abs(new_x - self.x)
        dy = abs(new_y - self.y)
        if dx == dy and dx > 0:
            return self.is_path_clear(new_x, new_y)
        return False


class Rook(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} Rook"
        super().__init__(name, position_x, position_y, color)

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        gluCylinder(gluNewQuadric(), 40, 20, 20, 10, 10)
        glTranslatef(0, 0, 20)
        gluCylinder(gluNewQuadric(), 20, 20, 50, 10, 10)
        glTranslatef(0, 0, 50)    
        gluCylinder(gluNewQuadric(), 30, 30, 20, 10, 10)
        glPopMatrix()

    def is_valid_move(self, new_x, new_y):
        # Horizontal or Vertical Movement
        if self.x == new_x or self.y == new_y:
            return self.is_path_clear(new_x, new_y)
        return False


class Queen(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} Queen"
        super().__init__(name, position_x, position_y, color)

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        gluCylinder(gluNewQuadric(), 40, 20, 20, 10, 10)
        glTranslatef(0, 0, 20)
        gluCylinder(gluNewQuadric(), 20, 20, 70, 10, 10)
        glTranslatef(0, 0, 70)
        gluCylinder(gluNewQuadric(), 20, 30, 20, 10, 10)
        glTranslatef(0, 0, 20)
        gluCylinder(gluNewQuadric(), 20, 0, 10, 10, 10)
        glTranslatef(0, 0, 10)
        gluSphere(gluNewQuadric(), 5, 10, 10)
        glPopMatrix()

    def is_valid_move(self, new_x, new_y):
        dx = abs(new_x - self.x)
        dy = abs(new_y - self.y)
        # All Direction Movement
        if self.x == new_x or self.y == new_y or dx == dy:
            return self.is_path_clear(new_x, new_y)
        return False


class King(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} King"
        super().__init__(name, position_x, position_y, color)
        self.is_rotated = False

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        if self.is_rotated:
            glRotatef(90, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 40, 10, 100, 10, 10)
        glTranslatef(0, 0, 100)
        gluCylinder(gluNewQuadric(), 10, 20, 20, 10, 10)
        glTranslatef(0, 0, 20)
        gluCylinder(gluNewQuadric(), 20, 0, 20, 10, 10)
        glTranslatef(0, 0, 20)
        glScalef(0.3, 0.3, 1)
        glutSolidCube(10)
        glScalef(1/0.3, 1/0.3, 1)
        glScalef(1, 0.3, 0.3)
        glutSolidCube(10)
        glPopMatrix()

    def is_valid_move(self, new_x, new_y):
        # All Direction One Step Movement
        dx = abs(new_x - self.x)
        dy = abs(new_y - self.y)
        return dx <= 200 and dy <= 200 and (dx > 0 or dy > 0)
    
    def rotate(self):    
        self.is_rotated = True

class Knight(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} Knight"
        super().__init__(name, position_x, position_y, color)

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        gluCylinder(gluNewQuadric(), 40, 10, 100, 10, 10)
        glTranslatef(0, 0, 100)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        if self.color == black:
            glRotatef(180, 0, 0, 1)
        glTranslatef(0, -20, 0)
        glScalef(1, 2, 1)
        glRotatef(110, 1, 0, 0)
        glutSolidCube(20)
        glPopMatrix()


    def is_valid_move(self, new_x, new_y):
        # L Movement
        dx = abs(new_x - self.x)
        dy = abs(new_y - self.y)
        return (dx == 400 and dy == 200) or (dx == 200 and dy == 400)

# Initialize Chess Pieces---------------------------------------------------------------------------------------------------------------

# Black Pieces
queen_black = Queen(100, -700, black)
king_black = King(-100, -700, black)
rook1_black = Rook(700, -700, black)
rook2_black = Rook(-700, -700, black)
bishop1_black = Bishop(300, -700, black)
bishop2_black = Bishop(-300, -700, black)
knight1_black = Knight(500, -700, black)
knight2_black = Knight(-500, -700, black)
pawn1_black = Pawn(700, -500, black)
pawn2_black = Pawn(500, -500, black)
pawn3_black = Pawn(300, -500, black)
pawn4_black = Pawn(100, -500, black)
pawn5_black = Pawn(-100, -500, black)
pawn6_black = Pawn(-300, -500, black)
pawn7_black = Pawn(-500, -500, black)
pawn8_black = Pawn(-700, -500, black)

black_list = [queen_black, king_black, rook1_black, rook2_black, bishop1_black, 
              bishop2_black, knight1_black, knight2_black, pawn1_black, pawn2_black, 
              pawn3_black, pawn4_black, pawn5_black, pawn6_black, pawn7_black, pawn8_black]

# White Pieces
queen_white = Queen(100, 700, white)
king_white = King(-100, 700, white)
rook1_white = Rook(700, 700, white)
rook2_white = Rook(-700, 700, white)
bishop1_white = Bishop(300, 700, white)
bishop2_white = Bishop(-300, 700, white)
knight1_white = Knight(500, 700, white)
knight2_white = Knight(-500, 700, white)
pawn1_white = Pawn(700, 500, white)
pawn2_white = Pawn(500, 500, white)
pawn3_white = Pawn(300, 500, white)
pawn4_white = Pawn(100, 500, white)
pawn5_white = Pawn(-100, 500, white)
pawn6_white = Pawn(-300, 500, white)
pawn7_white = Pawn(-500, 500, white)
pawn8_white = Pawn(-700, 500, white)

white_list = [queen_white, king_white, rook1_white, rook2_white, bishop1_white,
               bishop2_white, knight1_white, knight2_white, pawn1_white, pawn2_white,
                 pawn3_white, pawn4_white, pawn5_white, pawn6_white, pawn7_white, pawn8_white]

# Draw Menu and Game Mode Selection---------------------------------------------------------------------------------------------

def draw_menu():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    draw_text(350, 600, "Welcome to PVP 3D Chess!", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 500, "Select Game Mode:", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 450, "1. Rapid (10 minutes per player)", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 400, "2. Blitz (5 minutes per player)", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 350, "3. Exit game", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 250, "Press 1 or 2 to select game mode.", GLUT_BITMAP_TIMES_ROMAN_24)
    draw_text(350, 200, "Press 3 to exit game.", GLUT_BITMAP_TIMES_ROMAN_24)
    glutSwapBuffers()

def menuScreen():
    if menu:
        draw_menu()
    else:
        showScreen()

def menuKeyboardListener(key, x, y):
    global menu, game_mode, white_time, black_time
    if menu:
        if key == b'1':
            game_mode = "Rapid"
            white_time = 600
            black_time = 600
            menu = False
            glutDisplayFunc(showScreen)
            glutKeyboardFunc(keyboardListener)  
            glutSpecialFunc(specialKeyListener)
            glutMouseFunc(mouseListener)
        elif key == b'2':
            game_mode = "Blitz"
            white_time = 300
            black_time = 300
            menu = False
            glutDisplayFunc(showScreen)
            glutKeyboardFunc(keyboardListener)
            glutSpecialFunc(specialKeyListener)
            glutMouseFunc(mouseListener)
        elif key == b'3':
            glutLeaveMainLoop()

# Draw Chess Grid---------------------------------------------------------------------------------------------------------------

def draw_grid():
    glBegin(GL_QUADS)
    for i in range(8):
        for j in range(8):
            if i % 2 == 0:
                if j % 2 == 0:
                    glColor3f(1, 1, 1)
                else:
                    glColor3f(0.2, 0.2, 0.2)
            else:
                if j % 2 == 0:
                    glColor3f(0.2, 0.2, 0.2)
                else:
                    glColor3f(1, 1, 1)
            glVertex3f(grid_start + (200*j), grid_start + (200*i), 0)
            glVertex3f(grid_start + (200*j), grid_start + 200 + (200*i), 0)
            glVertex3f(grid_start + 200 + (200*j), grid_start + 200 + (200*i), 0)
            glVertex3f(grid_start + 200 + (200*j), grid_start + (200*i), 0)              
    glEnd()

#Movement Mechanics and Game Logic--------------------------------------------------------------------------------------------------------------

def get_piece_at(x, y):
    for piece in black_list + white_list:
        if piece.x == x and piece.y == y:
            return piece
    return None

def can_move_to_position(piece, new_x, new_y):
    if not (-700 <= new_x <= 700 and -700 <= new_y <= 700):
        return False
    # Check Valid Move
    if not piece.is_valid_move(new_x, new_y):
        return False
    # Check For Friendly Piece
    target_piece = get_piece_at(new_x, new_y)
    if target_piece and target_piece.color == piece.color:
        return False
    return True

def get_valid_moves(piece):
    valid_moves = []
    for x in range(-700, 800, 200):
        for y in range(-700, 800, 200):
            if is_legal_move(piece, x, y):
                valid_moves.append((x, y))
    return valid_moves

def highlight_valid_moves():
    if selected_piece:
        valid_moves = get_valid_moves(selected_piece)
        for x, y in valid_moves:
            glPushMatrix()
            glTranslatef(x, y, 1.5)
            glColor3f(0.38, 0.70, 0.55)
            glScalef(1, 1, 0.1)
            glutSolidCube(100)
            glPopMatrix()

def highlight_selected_piece():
    global pointer, selected_piece
    if selected_piece:
        glPushMatrix()
        glTranslatef(selected_piece.x, selected_piece.y, 2)
        glColor3f(0.4, 0.7, 1)
        glScalef(1, 1, 0.1)
        glutSolidCube(200)
        glPopMatrix()

def draw_game():
    global white_draw, black_draw, draw
    if white_draw and black_draw:
        draw_flag = True

def resign():
    global white_wins, black_wins, game_over, turn, resign_flag
    resign_flag = True
    if turn:
        king_white.rotate()
    else:
        king_black.rotate()

def cursor():
        global pointer, selected_piece
        glPushMatrix()
        glTranslatef(pointer[0], pointer[1],1)
        glColor3f(1, 1, 0)
        glScalef(1, 1, 0.1)
        glutSolidCube(200)
        glPopMatrix()

# Capture Mechanics -----------------------------------------------------------------------------------------------------------------------------

def check_blacks(x, y):
    for piece in black_list:
        if piece not in captured_black:
                if x == piece.x and y == piece.y:
                    return piece

def delete_black(piece):
    global black_capture_count
    captured_black.append(piece)
    piece.move(-1000, 700 - black_capture_count * 100)
    black_capture_count += 1
    black_list.remove(piece)

def check_whites(x, y):
    for piece in white_list:
        if piece not in captured_white:
            if x == piece.x and y == piece.y:
                return piece

def delete_white(piece):
    global white_capture_count
    captured_white.append(piece)
    piece.move(1000, -700 + white_capture_count * 100)
    white_capture_count += 1
    white_list.remove(piece)

# King Check(Mate) Mechanics ----------------------------------------------------------------------
    
def is_king_in_check(king_color):
    # Find King
    king = None
    friendly_pieces = white_list if king_color == white else black_list
    for piece in friendly_pieces:
        if isinstance(piece, King):
            king = piece
            break
    if not king:
        return False
    # Check Enemy Valid Moves to King's Position
    enemy_pieces = black_list if king_color == white else white_list
    for piece in enemy_pieces:
        if can_move_to_position(piece, king.x, king.y):
            return True
    return False

def if_piece_moves_king_in_check(piece, new_x, new_y):
    # Temporary move
    old_x, old_y = piece.x, piece.y
    captured_piece = get_piece_at(new_x, new_y)
    # Temporary Remove Captured Piece
    if captured_piece:
        if captured_piece in white_list:
            white_list.remove(captured_piece)
        elif captured_piece in black_list:
            black_list.remove(captured_piece)
    piece.x = new_x
    piece.y = new_y
    king_in_check_after = is_king_in_check(piece.color)
    piece.x = old_x
    piece.y = old_y
    # Restore Temporary Captured Piece
    if captured_piece:
        if captured_piece.color == white:
            white_list.append(captured_piece)
        elif captured_piece.color == black:
            black_list.append(captured_piece)
    return king_in_check_after

def is_legal_move(piece, new_x, new_y):
    if not can_move_to_position(piece, new_x, new_y):
        return False
    return not if_piece_moves_king_in_check(piece, new_x, new_y)

def is_checkmate(king_color):
    if not is_king_in_check(king_color):
        return False
    # Check for Legal Moves
    friendly_pieces = white_list if king_color == white else black_list
    for piece in friendly_pieces[:]:  # slice to avoid list modification
        for x in range(-700, 800, 200):
            for y in range(-700, 800, 200):
                if is_legal_move(piece, x, y):
                    return False
    return True

def highlight_king_in_check():
    if king_in_check:
        current_color = white if turn else black
        king = None
        for piece in (white_list if current_color == white else black_list):
            if isinstance(piece, King):
                king = piece
                break
        if king:
            glPushMatrix()
            glTranslatef(king.x, king.y, 3)
            glColor3f(1, 0, 0)
            glScalef(1, 1, 0.1)
            glutSolidCube(200)
            glPopMatrix()

# Reset Game -----------------------------------------------------------------------------------------------------------------------------

def reset_game():
    global turn, selected_piece, white_draw, black_draw, draw_flag, pointer, resign_flag, white_time, black_time, last_time, last_move_message
    global captured_black, captured_white, black_list, white_list, black_capture_count, white_capture_count, game_over, white_wins, black_wins
    global king_in_check, checkmate, king_black, king_white
    turn = True
    selected_piece = None
    game_over = False
    draw_flag = False
    resign_flag = False
    white_draw = False
    black_draw = False
    white_wins = False
    black_wins = False
    pointer = [100, 100]
    white_time = 600
    black_time = 600
    last_time = time.time()
    last_move_message = "Last Move: No moves yet"
    king_in_check = False
    checkmate = False
    black_list.extend(captured_black)
    white_list.extend(captured_white)
    captured_black.clear()
    captured_white.clear()
    black_capture_count = 0
    white_capture_count = 0

    king_white.is_rotated = False
    king_black.is_rotated = False

    for piece in black_list + white_list:
        piece.reset_position()

# Cursor Movement, Piece Selection and Game Mechanics -------------------------------------------------------------------------------------------------------------

def keyboardListener(key, x, y):
    global queen_black, selected_piece, pointer, white_draw, black_draw, draw_flag, turn, board_label, white_wins, black_wins, last_time
    global captured_black, captured_white, white_capture_count, black_capture_count, checkmate, king_in_check, game_over

    if not game_over and not( white_draw or black_draw):
        # Cursor Movement (WASD keys)
        if key == b'w':
            if pointer[1] > -700:
                pointer[1] -= 200
        if key == b's':
            if pointer[1] < 700:
                pointer[1] += 200
        if key == b'a':
            if pointer[0] < 700:
                pointer[0] += 200
        if key == b'd':
            if pointer[0] > -700:
                pointer[0] -= 200

        # Select/Deselect Piece (Space key)
        if key == b' ':
            # White's Turn
            if turn:  
                white_piece = None
                for piece in white_list:
                    if piece.x == pointer[0] and piece.y == pointer[1]:
                        white_piece = piece
                        break
                if white_piece:
                    if selected_piece:
                        selected_piece = None
                    else:
                        selected_piece = white_piece
                elif selected_piece:
                    # Move Selected Piece (only if it's a legal move)
                    if is_legal_move(selected_piece, pointer[0], pointer[1]):
                        # Capture Black Pieces in Selected Position
                        selected_piece.move(pointer[0], pointer[1])
                        black_piece = check_blacks(pointer[0], pointer[1])
                        if black_piece:
                            delete_black(black_piece)
                        selected_piece = None
                        turn = not turn
                        last_time = time.time()
                        
                        # Check for check and checkmate
                        if is_king_in_check(black):
                            if is_checkmate(black):
                                white_wins = True
                                game_over = True
                                checkmate = True

            # Black's Turn
            else:  
                black_piece = None
                for piece in black_list:
                    if piece.x == pointer[0] and piece.y == pointer[1]:
                        black_piece = piece
                        break
                if black_piece:
                    if selected_piece:
                        selected_piece = None
                    else:
                        selected_piece = black_piece
                elif selected_piece:
                    # Move Selected Piece (only if it's a legal move)
                    if is_legal_move(selected_piece, pointer[0], pointer[1]):
                        # Capture White Pieces in Selected Position
                        selected_piece.move(pointer[0], pointer[1])
                        white_piece = check_whites(pointer[0], pointer[1])
                        if white_piece:
                            delete_white(white_piece)
                        selected_piece = None
                        turn = not turn
                        last_time = time.time()
                        
                        # Check for check and checkmate
                        if is_king_in_check(white):
                            if is_checkmate(white):
                                black_wins = True
                                game_over = True
                                checkmate = True

    # Initiate Draw
    if key == b't':
        if turn:
            white_draw = True
            draw_game()
            turn = not turn 
        else:
            black_draw = True
            draw_game()
            turn = not turn

    # Accept Draw
    if key == b'y':
        if turn and black_draw:
            white_draw = True
            print("Opponent has accpeted a draw")
            draw_game()
        elif not turn and white_draw:
            black_draw = True
            print("Opponent has accpeted a draw")
            draw_text(300, 760, f"Opponent has accpeted a draw", GLUT_BITMAP_TIMES_ROMAN_24)
            draw_game()
        else:
            print("No draw was intiated")

    # Reject Draw
    if key == b'n':
        if white_draw or black_draw:
            white_draw, black_draw = False, False
            print("Opponent has rejected a draw")
            turn = not turn
        else:
            print("No draw was intiated")

    # Reset Game
    if key == b'r':
        reset_game()
    
    # Current Player Resigns
    if key == b'p':
        resign()

# Camera Movement -----------------------------------------------------------------------------------------------------------------------------

#3D Camera Movement (Arrow Keys)
def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    a = math.atan2(y, x) 
    r = math.sqrt(x**2 + y**2)
    if key == GLUT_KEY_UP :
        z += 5
    if key == GLUT_KEY_DOWN and z > 5:
        z -= 5
    if key == GLUT_KEY_LEFT:
        a -= .05 
    if key == GLUT_KEY_RIGHT:
        a += .05 
    x = r * math.cos(a)
    y = r * math.sin(a)
    camera_pos = (x, y, z)

# Top Down View/3D View Toggle (Right Mouse Button)
def mouseListener(button, state, x, y):
    global game_over, top_down_view
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        top_down_view = not top_down_view

def setupCamera():
    global top_down_view, player_x, player_y, player_direction
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(fovY, 1.25, 0.1, 1500)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    if top_down_view:
        gluLookAt(0, 1, 700, 0, 0, 0, 0, 0, 1)
    else:
        x, y, z = camera_pos
        gluLookAt(x, y, z, 0, 0, 0, 0, 0, 1)

# Timer -----------------------------------------------------------------------------------------------------------------------------

def format_time(second):
    minutes = int(second // 60)
    secs = int(second % 60)
    return f"{minutes:02d}:{secs:02d}"

def update_timer():
    global white_time, black_time, last_time, game_over, draw_flag, resign_flag, white_wins, black_wins
    if game_over or draw_flag or resign_flag:
        return
    current_time = time.time()
    time_elapsed = current_time - last_time
    last_time = current_time
    if turn:
        white_time -= time_elapsed
        if white_time <= 0:
            white_time = 0
            black_wins = True
            game_over = True
    else:
        black_time -= time_elapsed
        if black_time <= 0:
            black_time = 0
            white_wins = True
            game_over = True

def idle():
    update_timer()
    glutPostRedisplay()

# Text Display ------------------------------------------------------------------------------------------------------------------------

def draw_text(x, y, text, font=GLUT_BITMAP_9_BY_15):
    glColor3f(1,1,1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()
    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))
    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)

def showScreen():
    global selected_piece, board_label, white_time, black_time, king_in_check
    global turn, last_move_message, checkmate, white_wins, black_wins
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()
    
    # Check for check at the beginning of each frame
    current_color = white if turn else black
    king_in_check = is_king_in_check(current_color)
    
    # Draw Grid, Cursor and Highlights
    draw_grid()
    cursor()
    highlight_valid_moves()
    highlight_selected_piece()
    highlight_king_in_check()

    #Draw pieces
    for piece in black_list + white_list + captured_black + captured_white:
        piece.draw()

    # Display Time
    draw_text(20, 10, f"White Time: {format_time(white_time)}")
    draw_text(830, 10, f"Black Time: {format_time(black_time)}")

    # Turns
    if turn:
        if king_in_check and not game_over:
            draw_text(20, 770, f"Turn: White (IN CHECK!)")
        else:
            draw_text(20, 770, f"Turn: White")
    else:
        if king_in_check and not game_over:
            draw_text(20, 770, f"Turn: Black (IN CHECK!)")
        else:        
            draw_text(20, 770, f"Turn: Black")

    # Board Labels
    if selected_piece:
        for row, col, x, y in board_label:
            if (x, y) == (selected_piece.x, selected_piece.y):
                draw_text(20, 740, f"Selected Piece: {selected_piece.name} at {col}{row}")
                break
        valid_moves = get_valid_moves(selected_piece)
        draw_text(20, 680, f"Valid Moves: {len(valid_moves)}")
    else:
        draw_text(20, 740, f"Selected Piece: No Piece is Selected")
    draw_text(20, 710, last_move_message)

    # Draw Call Texts
    if white_draw or black_draw:
        draw_text(20, 680, f"Opponent has called for a Draw. Do you agree? Y/N")

    # Win or Draw Texts
    if (white_time * black_time) <= 0:
        draw_text(437, 760, f"Time's Up!", GLUT_BITMAP_TIMES_ROMAN_24)
    if checkmate:
        draw_text(435, 760, f"Checkmate!", GLUT_BITMAP_TIMES_ROMAN_24)
    if white_wins:
        draw_text(435, 720, f"White Wins!", GLUT_BITMAP_TIMES_ROMAN_24)
    if black_wins:
        draw_text(435, 720, f"Black Wins!", GLUT_BITMAP_TIMES_ROMAN_24)
    if draw_flag:
        draw_text(435, 720, f"The Game Ended in a Draw!", GLUT_BITMAP_TIMES_ROMAN_24)
    if resign_flag:
        if turn:
            draw_text(435, 720, f"Black Wins by Resignation!", GLUT_BITMAP_TIMES_ROMAN_24)
        else:
            draw_text(435, 720, f"White Wins by Resignation!", GLUT_BITMAP_TIMES_ROMAN_24)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    chess = glutCreateWindow(b"PVP 3D Chess")
    glutDisplayFunc(menuScreen)
    glutKeyboardFunc(menuKeyboardListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()