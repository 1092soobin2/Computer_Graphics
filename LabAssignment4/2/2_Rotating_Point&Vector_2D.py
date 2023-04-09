import glfw
from OpenGL.GL import *
import numpy as np



def render(th):
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    # draw cooridnate
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([1.,0.]))
    glColor3ub(0, 255, 0)
    glVertex2fv(np.array([0.,0.]))
    glVertex2fv(np.array([0.,1.]))
    glEnd()
    glColor3ub(255, 255, 255)

    # calculate matrix M1, M2 using th
    # your implementation
    # D
    t = glfw.get_time()
    th = t
    M1 = np.identity(3) # for p1, v1
    M2 = np.identity(3) # for p2, v2
    M1[:2, 2] = [.5 * np.cos(th), .5 * np.sin(th)]
    M2[:2, 2] = [.5 * np.cos(np.pi / 2 + th), .5 * np.sin(np.pi / 2 + th)]
    M1[:2, :2] = [[np.cos(th), -np.sin(th)],[np.sin(th), np.cos(th)]]
    M2[:2, :2] = [[np.cos(th), -np.sin(th)],[np.sin(th), np.cos(th)]]

    # # draw point p
    glBegin(GL_POINTS)
    glVertex2fv((M1 @ np.array([.5, 0., 1.]))[:-1])
    glVertex2fv((M2 @ np.array([0., .5, 1.]))[:-1])
    glEnd()

    # draw vector v
    glBegin(GL_LINES)
    glVertex2fv((M1 @ np.array([0., 0., 0.]))[:-1])
    glVertex2fv((M1 @ np.array([.5, 0., 0.]))[:-1])
    glVertex2fv((M2 @ np.array([0., 0., 0.]))[:-1])
    glVertex2fv((M2 @ np.array([0., .5, 0.]))[:-1])
    glEnd()

def main():
    if not glfw.init():
        return
    
    # A
    window = glfw.create_window(480, 480, "2019011449", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        
        # C D E
        t = glfw.get_time()
        th = t 
        M = np.array([[np.cos(th), -np.sin(th), 0.5 * np.cos(th),],
                        [np.sin(th), np.cos(th), 0.5 * np.sin(th)],
                        [0., 0., 1.]])
        render(M)
        
        glfw.swap_buffers(window)
    
    glfw.terminate()

if __name__ == "__main__":
    main()