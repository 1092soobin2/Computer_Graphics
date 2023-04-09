import glfw
from OpenGL.GL import *
import numpy as np

pressedKey = 0

# B C D
def render():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glBegin(GL_LINE_LOOP)
    for i in np.linspace(0, 11, 12):
        glVertex2f(np.cos(i * np.pi / 6), np.sin(i * np.pi / 6))
    glEnd()
    glBegin(GL_LINES)
    glVertex2f(0.0, 0.0)
    glVertex2f(np.cos(np.pi / 2  - pressedKey * np.pi / 6), np.sin(np.pi / 2  - pressedKey * np.pi / 6))
    glEnd()

# F
def key_callback(window, key, scancode, action, mods):
    global pressedKey
    if key in [glfw.KEY_1, glfw.KEY_2, glfw.KEY_3, glfw.KEY_4, glfw.KEY_5, glfw.KEY_6, glfw.KEY_7, glfw.KEY_8, glfw.KEY_9]:
        if action == glfw.PRESS:
            pressedKey = key - 48
    elif key == glfw.KEY_0:
        if action == glfw.PRESS:  
            pressedKey = 10
    elif key == glfw.KEY_Q:
        if action ==  glfw.PRESS:
            pressedKey = 11
    elif key == glfw.KEY_W:
        if action == glfw.PRESS:
            pressedKey = 12


def main():

    if not glfw.init():
        return
    
    # A
    window = glfw.create_window(480, 480, '2019011449', None, None)
    if not window:
        glfw.terminate()
        return
    
    glfw.set_key_callback(window, key_callback)
    
    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
         glfw.poll_events()
         
         render()
         
         glfw.swap_buffers(window)
    
    glfw.terminate()
    
if __name__ == "__main__":
            main()

