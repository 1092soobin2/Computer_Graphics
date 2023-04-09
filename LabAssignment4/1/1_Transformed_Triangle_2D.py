import glfw
from OpenGL.GL import *
import numpy as np

pressedKey = []

# B
def render():
    global pressedKey

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    # draw cooridnates
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()

    glColor3ub(255, 255, 255)

    #########################
    # implement here
    for i in range(len(pressedKey) - 1, -1, -1):  
    # for i in range(0, len(pressedKey)):
        if pressedKey[i] == 'Q':
            glTranslatef(-1 * .1, 0., 0.)
        elif pressedKey[i] == 'E':
            glTranslatef(.1, .0, 0.)
        elif pressedKey[i] == 'A':
            glRotatef(10., 0., 0., 1.)
        elif pressedKey[i] == 'D':
            glRotatef(-10., 0., 0., 1.)
        elif pressedKey[i] == '1':
            glLoadIdentity()
    ###########################    

    drawTriangle()

def drawTriangle():
    glBegin(GL_TRIANGLES)
    glVertex2fv(np.array([0.,.5]))
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([.5,0.]))
    glEnd()

# C
def key_callback(window, key, scancode, action, mods):
    global pressedKey
    if key == glfw.KEY_Q:
        if action == glfw.PRESS or action == glfw.REPEAT:
            pressedKey.append('Q')
    elif key == glfw.KEY_E:
        if action == glfw.PRESS or action == glfw.REPEAT:
            pressedKey.append('E')
    elif key == glfw.KEY_A:
        if action == glfw.PRESS or action == glfw.REPEAT:
            pressedKey.append('A')
    elif key == glfw.KEY_D:
        if action == glfw.PRESS or action == glfw.REPEAT:
            pressedKey.append('D')
    elif key == glfw.KEY_1:
        if action == glfw.PRESS or action == glfw.REPEAT:
            pressedKey = []

def main():
    if not glfw.init():
        return
        # A
    window = glfw.create_window(480, 480, "2019011449", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    # C
    glfw.set_key_callback(window, key_callback)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        # C D 
        render()
        
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()