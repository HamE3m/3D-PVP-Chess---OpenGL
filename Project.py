from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

camera_pos = (0,500,800)
fovY = 120
grid_start = -800
white = (0.8, 0.8, 0.8)
black = (0.4, 0.4, 0.4)
pointer = [100, 100]
turn = True
selected_piece = None
game_over = False
top_down_view = False
white_wins = False
black_wins = False
captured_black = []
captured_white = []
black_capture_count = 0
white_capture_count = 0

white_time = 600
black_time = 600
last_time = time.time()

board_label = [
    (8,"A", 700, -700), (8,"B", 500, -700), (8,"C", 300, -700), (8,"D", 100, -700), (8,"E", -100, -700), (8,"F", -300, -700), (8,"G", -500, -700), (8,"H", -700, -700),
    (7,"A", 700, -500), (7,"B", 500, -500), (7,"C", 300, -500), (7,"D", 100, -500), (7,"E", -100, -500), (7,"F", -300, -500), (7,"G", -500, -500), (7,"H", -700, -500),
    (6,"A", 700, -300), (6,"B", 500, -300), (6,"C", 300, -300), (6,"D", 100, -300), (6,"E", -100, -300), (6,"F", -300, -300), (6,"G", -500, -300), (6,"H", -700, -300),
    (5,"A", 700, -100), (5,"B", 500, -100), (5,"C", 300, -100), (5,"D", 100, -100), (5,"E", -100, -100), (5,"F", -300, -100), (5,"G", -500, -100), (5,"H", -700, -100),
    (4,"A", 700, 100), (4,"B", 500, 100), (4,"C", 300, 100), (4,"D", 100, 100), (4,"E", -100, 100), (4,"F", -300, 100), (4,"G", -500, 100), (4,"H", -700, 100),
    (3,"A", 700, 300), (3,"B", 500, 300), (3,"C", 300, 300), (3,"D", 100, 300), (3,"E", -100, 300), (3,"F", -300, 300), (3,"G", -500, 300), (3,"H", -700, 300),
    (2,"A", 700, 500), (2,"B", 500, 500), (2,"C", 300, 500), (2,"D", 100, 500), (2,"E", -100, 500), (2,"F", -300, 500), (2,"G", -500, 500), (2,"H", -700, 500),
    (1,"A", 700, 700), (1,"B", 500, 700), (1,"C", 300, 700), (1,"D", 100, 700), (1,"E", -100, 700), (1,"F", -300, 700), (1,"G", -500, 700), (1,"H", -700, 700)]



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

class Chess_Piece:
    def __init__(self, name, position_x, position_y, color):
        self.name = name
        self.color = color
        self.x = position_x
        self.y = position_y
        self.initial_x = position_x
        self.initial_y = position_y

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def reset_position(self):
        self.x = self.initial_x
        self.y = self.initial_y


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

class King(Chess_Piece):
    def __init__(self, position_x, position_y, color):
        name = f"{'White' if color == white else 'Black'} King"
        super().__init__(name, position_x, position_y, color)

    def draw(self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
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



def cursor():
        global pointer, selected_piece
        glPushMatrix()
        glTranslatef(pointer[0], pointer[1],1)
        glColor3f(1, 1, 0)
        glScalef(1, 1, 0.1)
        glutSolidCube(200)
        glPopMatrix()

def highlight_selected_piece():
    global pointer, selected_piece
    if selected_piece:
        glPushMatrix()
        glTranslatef(selected_piece.x, selected_piece.y,2)
        glColor3f(0, 1, 0)
        glScalef(1, 1, 0.1)
        glutSolidCube(200)
        glPopMatrix()

#Call the blacks
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


# Call the whites
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


def format_time(second):
    minutes = int(second // 60)
    secs = int(second % 60)
    return f"{minutes:02d}:{secs:02d}"

def update_timer():
    global white_time, black_time, last_time, game_over, white_wins, black_wins
    if game_over:
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


def check_blacks(x, y):
    for piece in black_list:
        if piece not in captured_black:
                if x == piece.x and y == piece.y:
                    return piece

def delete_black(piece):
    global black_capture_count
    captured_black.append(piece)
    piece.move(-1000, 700 - black_capture_count * 100)
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
    white_list.remove(piece)



def reset_game():
    global turn, selected_piece, game_over, pointer, white_wins, black_wins, white_time, black_time, last_time
    global captured_black, captured_white, black_list, white_list, black_capture_count, white_capture_count
    turn = True
    selected_piece = None
    game_over = False
    white_wins = False
    black_wins = False
    pointer = [100, 100]
    white_time = 600
    black_time = 600
    last_time = time.time()
    black_list.extend(captured_black)
    white_list.extend(captured_white)
    captured_black.clear()
    captured_white.clear()
    black_capture_count = 0
    white_capture_count = 0

    for piece in black_list + white_list:
        piece.reset_position()

def keyboardListener(key, x, y):
    global queen_black, selected_piece, pointer, game_over, turn, board_label, white_wins, black_wins, last_time, captured_black, captured_white, white_capture_count, black_capture_count
    if not game_over:
        # Move Cursor Up (W key)
        if key == b'w':
            if pointer[1] > -700:
                pointer[1] -= 200

        # Move Cursor Down (S key)
        if key == b's':
            if pointer[1] < 700:
                pointer[1] += 200


        # Move Cursor Left (A key)
        if key == b'a':
            if pointer[0] < 700:
                pointer[0] += 200

        # Move Cursor Right (D key)
        if key == b'd':
            if pointer[0] > -700:
                pointer[0] -= 200

        # Select/Deselect Piece (Space key)
        if key == b' ':
            if turn:
                for piece in white_list:
                    if piece.x == pointer[0] and piece.y == pointer[1]:
                        if selected_piece:
                            selected_piece = None
                        else:
                            selected_piece = piece
                        return
                if selected_piece:
                    selected_piece.move(pointer[0], pointer[1])
                    black_piece = check_blacks(pointer[0], pointer[1])
                    if black_piece:
                        delete_black(black_piece)
                        black_capture_count += 1
                    selected_piece = None
                    turn = not turn
                    last_time = time.time()

            else:
                for piece in black_list:
                    if piece.x == pointer[0] and piece.y == pointer[1]:
                        if selected_piece:
                            selected_piece = None
                        else:
                            selected_piece = piece
                        return
                if selected_piece:
                    selected_piece.move(pointer[0], pointer[1])
                    white_piece = check_whites(pointer[0], pointer[1])
                    if white_piece:
                        delete_white(white_piece)
                        white_capture_count += 1

                    selected_piece = None
                    turn = not turn
                    last_time = time.time()

    # Reset the game if R key is pressed
    if key == b'r':
        reset_game()
    
    # Current Player Surrender
    if key == b'p':
        if turn:
            black_wins = True
        else:
            white_wins = True
        game_over = True

def specialKeyListener(key, x, y):
    global camera_pos
    x, y, z = camera_pos
    a = math.atan2(y, x) 
    r = math.sqrt(x**2 + y**2)

    # Move camera up (UP arrow key)
    if key == GLUT_KEY_UP :
        z += 5

    # # Move camera down (DOWN arrow key)
    if key == GLUT_KEY_DOWN and z > 5:
        z -= 5

    # moving camera left (LEFT arrow key)
    if key == GLUT_KEY_LEFT:
        a -= .05 

    # moving camera right (RIGHT arrow key)
    if key == GLUT_KEY_RIGHT:
        a += .05 
        
    x = r * math.cos(a)
    y = r * math.sin(a)
    camera_pos = (x, y, z)

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

def idle():
    update_timer()
    glutPostRedisplay()
    
def showScreen():
    global selected_piece, board_label
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glViewport(0, 0, 1000, 800)
    setupCamera()

    #Draw Chess Grid
    draw_grid()
    cursor()
    highlight_selected_piece()

    #Draw pieces
    for piece in black_list + white_list + captured_black + captured_white:
        piece.draw()

    # Text Display
    draw_text(20, 10, f"White Time: {format_time(white_time)}")
    draw_text(830, 10, f"Black Time: {format_time(black_time)}")

    if turn:
        draw_text(20, 770, f"Turn: White")
    else:
        draw_text(20, 770, f"Turn: Black")

    if selected_piece:
        for row, col, x, y in board_label:
            if (x, y) == (selected_piece.x, selected_piece.y):
                draw_text(20, 740, f"Selected Piece: {selected_piece.name} at {col}{row}")
                break
    else:
        draw_text(20, 740, f"Selected Piece: No Piece is Selected")

    draw_text(20, 710, f"Something EPIC")
    if white_wins:
        draw_text(435, 720, f"White Wins!", GLUT_BITMAP_TIMES_ROMAN_24)
    if black_wins:
        draw_text(435, 720, f"Black Wins!", GLUT_BITMAP_TIMES_ROMAN_24)
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    chess = glutCreateWindow(b"3D Chess")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
