from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import math

# Window size
WIDTH = 1000
HEIGHT = 700

# Black hole position
black_hole_x = WIDTH // 2
black_hole_y = HEIGHT // 2

# Star particles
particles = []

# Gravity strength
gravity = 0.08


# =========================
# Particle Class
# =========================
class Particle:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)

        self.size = random.uniform(2, 5)

        self.r = random.random()
        self.g = random.random()
        self.b = 1.0

    def update(self):

        dx = black_hole_x - self.x
        dy = black_hole_y - self.y

        dist = math.sqrt(dx * dx + dy * dy)

        # Prevent division by zero
        if dist < 5:
            self.reset()
            return

        # Gravity force
        force = gravity / dist

        self.vx += dx * force
        self.vy += dy * force

        self.x += self.vx
        self.y += self.vy

    def draw(self):

        glPointSize(self.size)

        glBegin(GL_POINTS)

        glColor3f(self.r, self.g, self.b)

        glVertex2f(self.x, self.y)

        glEnd()

    def reset(self):

        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)

        self.vx = random.uniform(-1, 1)
        self.vy = random.uniform(-1, 1)


# =========================
# Initialize particles
# =========================
def init_particles():

    for i in range(400):

        particles.append(
            Particle(
                random.randint(0, WIDTH),
                random.randint(0, HEIGHT)
            )
        )


# =========================
# Draw black hole
# =========================
def draw_black_hole():

    # Glow effect
    for r in range(80, 0, -5):

        alpha = r / 80

        glColor4f(
            0.3,
            0.0,
            1.0,
            alpha * 0.08
        )

        glBegin(GL_POLYGON)

        for i in range(100):

            theta = 2 * math.pi * i / 100

            x = black_hole_x + r * math.cos(theta)
            y = black_hole_y + r * math.sin(theta)

            glVertex2f(x, y)

        glEnd()

    # Black center
    glColor3f(0, 0, 0)

    glBegin(GL_POLYGON)

    for i in range(100):

        theta = 2 * math.pi * i / 100

        x = black_hole_x + 30 * math.cos(theta)
        y = black_hole_y + 30 * math.sin(theta)

        glVertex2f(x, y)

    glEnd()


# =========================
# Draw text
# =========================
def draw_text(x, y, text):

    glColor3f(1, 1, 1)

    glRasterPos2f(x, y)

    for ch in text:

        glutBitmapCharacter(
            GLUT_BITMAP_HELVETICA_18,
            ord(ch)
        )


# =========================
# Display function
# =========================
def display():

    glClearColor(0.0, 0.0, 0.05, 1)

    glClear(GL_COLOR_BUFFER_BIT)

    # Draw black hole
    draw_black_hole()

    # Draw particles
    for p in particles:

        p.draw()

    # Instructions
    draw_text(
        10,
        HEIGHT - 30,
        "CLICK anywhere = Move Black Hole"
    )

    draw_text(
        10,
        HEIGHT - 60,
        "SPACE = Add More Stars"
    )

    draw_text(
        10,
        HEIGHT - 90,
        "ESC = Exit"
    )

    glutSwapBuffers()


# =========================
# Animation update
# =========================
def update(value):

    for p in particles:

        p.update()

    glutPostRedisplay()

    glutTimerFunc(16, update, 0)


# =========================
# Mouse interaction
# =========================
def mouse(button, state, x, y):

    global black_hole_x
    global black_hole_y

    if state == GLUT_DOWN:

        black_hole_x = x
        black_hole_y = HEIGHT - y


# =========================
# Keyboard controls
# =========================
def keyboard(key, x, y):

    key = key.decode("utf-8")

    # Add more particles
    if key == ' ':

        for i in range(100):

            particles.append(
                Particle(
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT)
                )
            )

    # Exit
    elif ord(key) == 27:

        exit()


# =========================
# OpenGL Initialization
# =========================
def init():

    glEnable(GL_BLEND)

    glBlendFunc(
        GL_SRC_ALPHA,
        GL_ONE_MINUS_SRC_ALPHA
    )

    glMatrixMode(GL_PROJECTION)

    glLoadIdentity()

    gluOrtho2D(0, WIDTH, 0, HEIGHT)

    glMatrixMode(GL_MODELVIEW)


# =========================
# Main function
# =========================
def main():

    glutInit()

    glutInitDisplayMode(
        GLUT_DOUBLE | GLUT_RGBA
    )

    glutInitWindowSize(
        WIDTH,
        HEIGHT
    )

    glutCreateWindow(
        b"Black Hole Gravity Simulation"
    )

    init()

    init_particles()

    glutDisplayFunc(display)

    glutMouseFunc(mouse)

    glutKeyboardFunc(keyboard)

    glutTimerFunc(16, update, 0)

    glutMainLoop()


main()