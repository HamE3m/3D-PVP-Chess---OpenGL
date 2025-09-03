from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

camera_pos = (0,200,500)
fovY = 120
grid_start = -800
white = (0.8, 0.8, 0.8)
black = (0.4, 0.4, 0.4)
highlight = [100, 100]
game_score = 0
turn = 'Black'

board_label = [
    (8,"A", 700, -700), (8,"B", 500, -700), (8,"C", 300, -700), (8,"D", 100, -700), (8,"E", -100, -700), (8,"F", -300, -700), (8,"G", -500, -700), (8,"H", -700, -700),
    (7,"A", 700, -500), (7,"B", 500, -500), (7,"C", 300, -500), (7,"D", 100, -500), (7,"E", -100, -500), (7,"F", -300, -500), (7,"G", -500, -500), (7,"H", -700, -500),
    (6,"A", 700, -300), (6,"B", 500, -300), (6,"C", 300, -300), (6,"D", 100, -300), (6,"E", -100, -300), (6,"F", -300, -300), (6,"G", -500, -300), (6,"H", -700, -300),
    (5,"A", 700, -100), (5,"B", 500, -100), (5,"C", 300, -100), (5,"D", 100, -100), (5,"E", -100, -100), (5,"F", -300, -100), (5,"G", -500, -100), (5,"H", -700, -100),
    (4,"A", 700, 100), (4,"B", 500, 100), (4,"C", 300, 100), (4,"D", 100, 100), (4,"E", -100, 100), (4,"F", -300, 100), (4,"G", -500, 100), (4,"H", -700, 100),
    (3,"A", 700, 300), (3,"B", 500, 300), (3,"C", 300, 300), (3,"D", 100, 300), (3,"E", -100, 300), (3,"F", -300, 300), (3,"G", -500, 300), (3,"H", -700, 300),
    (2,"A", 700, 500), (2,"B", 500, 500), (2,"C", 300, 500), (2,"D", 100, 500), (2,"E", -100, 500), (2,"F", -300, 500), (2,"G", -500, 500), (2,"H", -700, 500),
    (1,"A", 700, 700), (1,"B", 500, 700), (1,"C", 300, 700), (1,"D", 100, 700), (1,"E", -100, 700), (1,"F", -300, 700), (1,"G", -500, 700), (1,"H", -700, 700)
]

selected_piece = None
game_over = False
top_down_view = False

def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
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

    def move(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

    def draw_pawn (self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 50)
        gluSphere(gluNewQuadric(), 20, 10, 10)
        glTranslatef(0, 0, -50)
        gluCylinder(gluNewQuadric(), 40, 10, 50, 10, 10)
        glPopMatrix()

    def draw_bishop (self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        gluCylinder(gluNewQuadric(), 40, 10, 100, 10, 10)
        glTranslatef(0, 0, 100)
        gluCylinder(gluNewQuadric(), 20, 0, 40, 10, 10)
        glPopMatrix()

    def draw_rook (self):
        glPushMatrix()
        glColor3f(*self.color)
        glTranslatef(self.x, self.y, 0)
        gluCylinder(gluNewQuadric(), 40, 20, 20, 10, 10)
        glTranslatef(0, 0, 20)
        gluCylinder(gluNewQuadric(), 20, 20, 50, 10, 10)
        glTranslatef(0, 0, 50)    
        gluCylinder(gluNewQuadric(), 30, 30, 20, 10, 10)
        glPopMatrix()

    def draw_queen (self):
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

    def draw_king (self):
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

    def draw_knight (self):
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
        global highlight, selected_piece
        glPushMatrix()
        glTranslatef(highlight[0], highlight[1],1)
        glColor3f(1, 1, 0)
        glScalef(1, 1, 0.1)
        glutSolidCube(200)
        glPopMatrix()

def highlight_selected_piece():
    global highlight, selected_piece
    if selected_piece:
        glPushMatrix()
        glTranslatef(selected_piece.x, selected_piece.y,2)
        glColor3f(0, 1, 0)
        glScalef(1, 1, 0.1)
        glutSolidCube(200)
        glPopMatrix()

#Call the blacks
queen_black = Chess_Piece('Black Queen', 100, -700, black)
king_black = Chess_Piece('Black King', -100, -700, black)
rook1_black = Chess_Piece('Black Rook', 700, -700, black)
rook2_black = Chess_Piece('Black Rook', -700, -700, black)
bishop1_black = Chess_Piece('Black Bishop', 300, -700, black)
bishop2_black = Chess_Piece('Black Bishop', -300, -700, black)
knight1_black = Chess_Piece('Black Knight', 500, -700, black)
knight2_black = Chess_Piece('Black Knight', -500, -700, black)
pawn1_black = Chess_Piece('Black Pawn', 700, -500, black)
pawn2_black = Chess_Piece('Black Pawn', 500, -500, black)
pawn3_black = Chess_Piece('Black Pawn', 300, -500, black)
pawn4_black = Chess_Piece('Black Pawn', 100, -500, black)
pawn5_black = Chess_Piece('Black Pawn', -100, -500, black)
pawn6_black = Chess_Piece('Black Pawn', -300, -500, black)
pawn7_black = Chess_Piece('Black Pawn', -500, -500, black)
pawn8_black = Chess_Piece('Black Pawn', -700, -500, black)

black_list = [queen_black, king_black, rook1_black, rook2_black, bishop1_black, 
              bishop2_black, knight1_black, knight2_black, pawn1_black, pawn2_black, 
              pawn3_black, pawn4_black, pawn5_black, pawn6_black, pawn7_black, pawn8_black]


# Call the whites
queen_white = Chess_Piece('White Queen', 100, 700, white)
king_white = Chess_Piece('White King', -100, 700, white)
rook1_white = Chess_Piece('White Rook', 700, 700, white)
rook2_white = Chess_Piece('White Rook', -700, 700, white)
bishop1_white = Chess_Piece('White Bishop', 300, 700, white)
bishop2_white = Chess_Piece('White Bishop', -300, 700, white)
knight1_white = Chess_Piece('White Knight', 500, 700, white)
knight2_white = Chess_Piece('White Knight', -500, 700, white)
pawn1_white = Chess_Piece('White Pawn', 700, 500, white)
pawn2_white = Chess_Piece('White Pawn', 500, 500, white)
pawn3_white = Chess_Piece('White Pawn', 300, 500, white)
pawn4_white = Chess_Piece('White Pawn', 100, 500, white)
pawn5_white = Chess_Piece('White Pawn', -100, 500, white)
pawn6_white = Chess_Piece('White Pawn', -300, 500, white)
pawn7_white = Chess_Piece('White Pawn', -500, 500, white)
pawn8_white = Chess_Piece('White Pawn', -700, 500, white)

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

def keyboardListener(key, x, y):
    global queen_black, selected_piece, highlight, game_over, turn, board_label
    if not game_over:
        # Move Cursor Up (W key)
        if key == b'w':
            if highlight[1] > -700:
                highlight[1] -= 200

        # Move Cursor Down (S key)
        if key == b's':
            if highlight[1] < 700:
                highlight[1] += 200


        # Move Cursor Left (A key)
        if key == b'a':
            if highlight[0] < 700:
                highlight[0] += 200

        # Move Cursor Right (D key)
        if key == b'd':
            if highlight[0] > -700:
                highlight[0] -= 200

        # Select/Deselect Piece (Space key)
        if key == b' ':
            if turn == 'White':
                for piece in white_list:
                    if piece.x == highlight[0] and piece.y == highlight[1]:
                        if selected_piece:
                            selected_piece = None
                        else:
                            selected_piece = piece
                    elif selected_piece:
                        selected_piece.move(highlight[0], highlight[1])
            else:
                for piece in black_list:
                    if piece.x == highlight[0] and piece.y == highlight[1]:
                        if selected_piece:
                            selected_piece = None
                        else:
                            selected_piece = piece
                    elif selected_piece:
                        selected_piece.move(highlight[0], highlight[1])

        # Toggle cheat vision (V key)
        if key == b'v':
            pass

    # Reset the game if R key is pressed
    if key == b'r':
        pass

    if key == b'u':
        selected_piece = queen_black
    if key == b'q':
        selected_piece.move(random.randint(-700, 700), random.randint(-700, 700))

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
    #Draw blacks
    queen_black.draw_queen()
    king_black.draw_king()
    rook1_black.draw_rook()
    rook2_black.draw_rook()
    bishop1_black.draw_bishop()
    bishop2_black.draw_bishop()
    knight1_black.draw_knight()
    knight2_black.draw_knight()
    pawn1_black.draw_pawn()
    pawn2_black.draw_pawn()
    pawn3_black.draw_pawn()
    pawn4_black.draw_pawn()
    pawn5_black.draw_pawn()
    pawn6_black.draw_pawn()
    pawn7_black.draw_pawn()
    pawn8_black.draw_pawn()

    # Draw whites
    queen_white.draw_queen()
    king_white.draw_king()
    rook1_white.draw_rook()
    rook2_white.draw_rook()
    bishop1_white.draw_bishop()
    bishop2_white.draw_bishop()
    knight1_white.draw_knight()
    knight2_white.draw_knight()
    pawn1_white.draw_pawn()
    pawn2_white.draw_pawn()
    pawn3_white.draw_pawn()
    pawn4_white.draw_pawn()
    pawn5_white.draw_pawn()
    pawn6_white.draw_pawn()
    pawn7_white.draw_pawn()
    pawn8_white.draw_pawn()

    # Text Display
    draw_text(10, 770, f"Current Player: {turn}")

    if selected_piece:
        for row, col, x, y in board_label:
            if (x, y) == (selected_piece.x, selected_piece.y):
                draw_text(10, 740, f"Selected Piece: {selected_piece.name} at {col}{row}")
                break
    else:
        draw_text(10, 740, f"Selected Piece: No Piece is Selected")

    draw_text(10, 710, f"Something EPIC")
    glutSwapBuffers()

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(1000, 800)
    glutInitWindowPosition(0, 0)
    wind = glutCreateWindow(b"Lab 3")
    glutDisplayFunc(showScreen)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
