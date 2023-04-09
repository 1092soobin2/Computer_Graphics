import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

gAzimuth = np.radians(45)
gElevation = np.radians(45)
gDistance = 1
gPanning = [0, 0]
gPrev_pos = [0, 0]
gCur_pos = [0, 0]
gToggle = True

def render():
    global gAzimuth, gElevation, gDistance

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)
    glLoadIdentity()

    # Orthographic
    if gToggle == False:
        glOrtho(-10, 10, -10, 10, 1, 100)
    # Perspective
    elif gToggle == True:
        glFrustum(-1, 1, -1, 1, 1, 100)

    # Orbit, Panning, Zooming
    # myLookAt(np.array([(1. * np.cos(gAzimuth)) * gDistance, (1. * np.sin(gElevation))* gDistance, (1. * np.sin(gAzimuth)) * gDistance]),
    #          np.array([0 * gDistance, 0 * gDistance, 0 * gDistance]),
    #          np.array([0, 1, 0]))

    myLookAt(np.array([1, 1, 1]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawRectangularGrid()

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([-100.,0.,0.]))
    glVertex3fv(np.array([100.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,-100.]))
    glVertex3fv(np.array([0.,0.,100.]))
    glEnd()
def drawRectangularGrid():
    glBegin(GL_LINES)
    for i in range(-100, 0):
        # glVertex3f(-100., 0, i)
        # glVertex3f(100., 0, i)
        # glVertex3f(i, 0, -100.)
        # glVertex3f(i, 0, 100.)
        glVertex3fv(np.array([-100., 0, i]))
        glVertex3fv(np.array([100., 0, i]))
        glVertex3fv(np.array([i, 0, -100.]))
        glVertex3fv(np.array([i, 0, 100.]))
    for i in range(1, 101):
        # glVertex3f(-100., 0, i)
        # glVertex3f(100., 0, i)
        # glVertex3f(i, 0, -100.)
        # glVertex3f(i, 0, 100.)
        glVertex3fv(np.array([-100., 0, i]))
        glVertex3fv(np.array([100., 0, i]))
        glVertex3fv(np.array([i, 0, -100.]))
        glVertex3fv(np.array([i, 0, 100.]))
    glEnd()

# A. Orbit: Click mouse left button & drag
# B. Panning: Click mouse right button & drag
# C. Zooming: Rotate mouse wheel
def button_callback(window, button, action, mod):
    global gPrev_pos
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:    
        gPrev_pos = glfw.get_cursor_pos(window)
    elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        gPrev_pos = glfw.get_cursor_pos(window)

def cursor_callback(window, xpos, ypos):
    global gPrev_pos, gCur_pos
    left_state = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT)
    right_state = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT)
    if left_state == True:
        gCur_pos = [xpos, ypos]
        orbit(gPrev_pos, gCur_pos)
        gPrev_pos = gCur_pos
    elif right_state == True:
        gCur_pos = [xpos, ypos]
        panning(gPrev_pos, gCur_pos)
        gPrev_pos = gCur_pos

def scroll_callback(window, xoffset, yoffset):
    zooming(xoffset, yoffset)

def key_callback(window, key, scancode, action, mods):
    global gToggle
    if key == glfw.KEY_V and action == glfw.PRESS:
        print('v pressed')
        gToggle = not(gToggle)

def myLookAt(eye, at, up):
    global gAzimuth, gElevation, gDistance, gPanning

    distance = 5
    eye[0] = at[0] + distance * np.cos(gAzimuth)
    eye[1] = at[1] + distance * np.sin(gElevation)
    eye[2] = at[2] + distance * np.sin(gAzimuth)
    
    w = (eye - at) / np.sqrt(np.dot(eye - at, eye - at))
    u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
    v = np.cross(w, u)
    
    Mv = np.array([[u[0], u[1], u[2], -np.dot(u, eye) + gPanning[0]],
                   [v[0], v[1], v[2], -np.dot(v, eye) + gPanning[1]],
                   [w[0], w[1], w[2], (-np.dot(w, eye)) * gDistance],
                   [0, 0, 0, 1]])
    
    glMultMatrixf(Mv.T)

def orbit(prev_pos, cur_pos):
    global gAzimuth, gElevation
    # print('orbit')
    gAzimuth += .1 * np.radians(cur_pos[0] - prev_pos[0])
    gElevation += .1 * np.radians(cur_pos[1] - prev_pos[1])

def panning(prev_pos, cur_pos):
    global gPanning
    # print('panning')
    gPanning[0] += .01 * (cur_pos[0] - prev_pos[0])
    gPanning[1] += .01 * -(cur_pos[1] - prev_pos[1])

def zooming(xoffset, yoffset):
    global gDistance
    # print('zooming')
    gDistance += .01 * yoffset
    
def main():
    if not glfw.init():
        return
    
    # 1
    window = glfw.create_window(640,640,'ClassAssignmnet1', None,None)
    
    if not window:
        glfw.terminate()
        return

    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
