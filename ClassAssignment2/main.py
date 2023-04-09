import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

g_azimuth = np.radians(45)
g_elevation = np.radians(45)
g_distance = 1
g_panning = [0, 0]
g_prev_pos = [0, 0]
g_cur_pos = [0, 0]

g_toggle_frustum_ortho = True       # v
g_toggle_wireframe_solid = True     # z
g_toggle_single_hierarchy = True    # h
g_toggle_normal_smooth = True       # s

g_light0 = True                     # 0
g_light1 = True                     # 1
g_light2 = True                     # 2

######################################################################
######################## ClassAssignment1 ############################
######################################################################
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
    for i in range(-200, 0):
        # glVertex3f(-100., 0, i)
        # glVertex3f(100., 0, i)
        # glVertex3f(i, 0, -100.)
        # glVertex3f(i, 0, 100.)
        glVertex3fv(np.array([-100., 0, i / 2.]))
        glVertex3fv(np.array([100., 0, i / 2.]))
        glVertex3fv(np.array([i / 2., 0, -100.]))
        glVertex3fv(np.array([i / 2., 0, 100.]))
    for i in range(1, 201):
        # glVertex3f(-100., 0, i)
        # glVertex3f(100., 0, i)
        # glVertex3f(i, 0, -100.)
        # glVertex3f(i, 0, 100.)
        glVertex3fv(np.array([-100., 0, i / 2.]))
        glVertex3fv(np.array([100., 0, i / 2.]))
        glVertex3fv(np.array([i / 2., 0, -100.]))
        glVertex3fv(np.array([i / 2., 0, 100.]))
    glEnd()

# A. Orbit: Click mouse left button & drag
# B. Panning: Click mouse right button & drag
# C. Zooming: Rotate mouse wheel
def button_callback(window, button, action, mod):
    global g_prev_pos
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:    
        g_prev_pos = glfw.get_cursor_pos(window)
    elif button == glfw.MOUSE_BUTTON_RIGHT and action == glfw.PRESS:
        g_prev_pos = glfw.get_cursor_pos(window)
def cursor_callback(window, xpos, ypos):
    global g_prev_pos, g_cur_pos
    left_state = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_LEFT)
    right_state = glfw.get_mouse_button(window, glfw.MOUSE_BUTTON_RIGHT)
    if left_state == True:
        g_cur_pos = [xpos, ypos]
        orbit(g_prev_pos, g_cur_pos)
        g_prev_pos = g_cur_pos
    elif right_state == True:
        g_cur_pos = [xpos, ypos]
        panning(g_prev_pos, g_cur_pos)
        g_prev_pos = g_cur_pos
def scroll_callback(window, xoffset, yoffset):
    zooming(xoffset, yoffset)
def key_callback(window, key, scancode, action, mods):
    global g_toggle_frustum_ortho, g_toggle_wireframe_solid, g_toggle_single_hierarchy, g_toggle_normal_smooth
    global g_light0, g_light1, g_light2
    
    if key == glfw.KEY_V and action == glfw.PRESS:
        g_toggle_frustum_ortho = not(g_toggle_frustum_ortho)
    elif key == glfw.KEY_Z and action == glfw.PRESS:
        g_toggle_wireframe_solid = not(g_toggle_wireframe_solid)
    elif key == glfw.KEY_H and action == glfw.PRESS:
        g_toggle_single_hierarchy = not(g_toggle_single_hierarchy)
    elif key == glfw.KEY_S and action == glfw.PRESS:
        g_toggle_normal_smooth = not(g_toggle_normal_smooth)
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_0:
            g_light0 = not g_light0
        elif key == glfw.KEY_1:
            g_light1 = not g_light1
        elif key == glfw.KEY_2:
            g_light2 = not g_light2

def orbit(prev_pos, cur_pos):
    global g_azimuth, g_elevation
    # print('orbit')
    g_azimuth += .2 * np.radians(cur_pos[0] - prev_pos[0])
    g_elevation += .2 * np.radians(cur_pos[1] - prev_pos[1])
def panning(prev_pos, cur_pos):
    global g_panning
    # print('panning')
    g_panning[0] += .02 * (cur_pos[0] - prev_pos[0])
    g_panning[1] += .02 * -(cur_pos[1] - prev_pos[1])
def zooming(xoffset, yoffset):
    global g_distance
    # print('zooming')
    g_distance += .015 * yoffset
      
def myLookAt(eye, at, up):
    global g_azimuth, g_elevation, g_distance, g_panning

    distance = 5
    eye[0] = at[0] + distance * np.cos(g_azimuth)
    eye[1] = at[1] + distance * np.sin(g_elevation)
    eye[2] = at[2] + distance * np.sin(g_azimuth)
    
    w = (eye - at) / np.sqrt(np.dot(eye - at, eye - at))
    u = np.cross(up, w) / np.sqrt(np.dot(np.cross(up, w), np.cross(up, w)))
    v = np.cross(w, u)
    
    Mv = np.array([[u[0], u[1], u[2], -np.dot(u, eye) + g_panning[0]],
                   [v[0], v[1], v[2], -np.dot(v, eye) + g_panning[1]],
                   [w[0], w[1], w[2], (-np.dot(w, eye)) * g_distance],
                   [0, 0, 0, 1]])
    
    glMultMatrixf(Mv.T)

######################################################################
######################## ClassAssignment2 ############################
######################################################################

# single_mesh_rendering
g_vertex_array_seperate = np.array([], 'float32')       # for normal shading
g_vertex_array_indexed = np.array([], 'float32')        # for smooth shading (1 vn per vertex)
g_index_array = np.array([])                            # for smooth shading (1 vn per vertex)
# hierarchical_modeling
g_h_varr = np.array([], 'float32')
g_h_ivarr = np.array([], 'float32')
g_h_iarr = np.array([])

def drop_callback(window, paths):
    if g_toggle_single_hierarchy == True:
        handle_obj_file(paths[0], True)

def handle_obj_file(path, is_drop):
    global g_toggle_single_hierarchy

    global g_vertex_array_seperate
    global g_vertex_array_indexed, g_index_array

    global g_h_varr
    global g_h_ivarr, g_h_iarr


    # Info of the obj file
    file_name = path
    num_of_faces = 0
    num_of_faces_3v = 0
    num_of_faces_4v = 0
    num_of_faces_morev = 0

    # Open file
    fd = open(path, 'r')
    file_txt = fd.read()
    fd.close()

    # vertex parsing
    vertices = (file_txt.split('v '))[1:]                       # '1.0 1.0 1.0 ....'

    for i in range(len(vertices)):
        vertices[i] = ((vertices[i].split('\n'))[0]).split()    # ['1.0', '1.0', '1.0']
        for j in range(len(vertices[i])):
            vertices[i][j] = float(vertices[i][j])              # [1.0, 1.0, 1.0]
        vertices[i] = tuple(vertices[i])                        # (1.0, 1.0, 1.0)
    
    # vertex normal parsing
    vertex_normals = (file_txt.split('vn '))[1:]

    for i in range(len(vertex_normals)):
        vertex_normals[i] = ((vertex_normals[i].split('\n'))[0]).split()
        for j in range(len(vertex_normals[i])):
            vertex_normals[i][j] = float(vertex_normals[i][j])
        vertex_normals[i] = tuple(vertex_normals[i])

    # face parsing + Info of the obj file
    faces = (file_txt.split('f '))[1:]                          # '1 1 1'(faces[i]) '1//1 1//1 1//1' (v//vn)

    for i in range(len(faces)):
        faces[i] = ((faces[i].split('\n'))[0]).split()          # ['1', '1', '1']   ['1//1', '1//1', '1//1'] 

        # Info of the obj file
        num_of_vertex_in_face = len(faces[i])
        if num_of_vertex_in_face < 3:
            sys.exit("face with 2 vertices in obj file")
        elif num_of_vertex_in_face == 3:
            num_of_faces_3v += 1
        elif num_of_vertex_in_face == 4:
            num_of_faces_4v += 1
        else:
            num_of_faces_morev += 1
        
        # face parsing
        for j in range(len(faces[i])):
            faces[i][j] = (faces[i][j]).split('/')              # [['1'], ['1'], ['1']] [['1', '', '1'], ..., ...]
            for k in range(len(faces[i][j])):
                if faces[i][j][k] == '':
                    faces[i][j][k] = None
                else:
                    faces[i][j][k] = int(faces[i][j][k])        # [[1], [1], [1]]       [[1, None, 1], ..., ...]
    
    # Create g_vertex_array_seperate
    varr = []
    
    for i in range(len(faces)):
        # i: index of face, j: index of v//vn included in the faces[i]

        num_of_vertex_in_face = len(faces[i])
        # Append 3 vertices per 1 repeat
        for j in range(num_of_vertex_in_face - 1):
            # 123   123
            # 1234  123,134
            # 12345 123,134,145
            if len(faces[i][j]) == 1:
                # 1, 1, 1
                varr.append(vertices[faces[i][0][0] - 1])
                # 2, 3, 4
                varr.append(vertices[faces[i][j][0] - 1])
                # 3, 4, 5
                varr.append(vertices[faces[i][j + 1][0] - 1])
            else:
                varr.append(vertex_normals[faces[i][0][2] - 1])
                varr.append(vertices[faces[i][0][0] - 1])
                varr.append(vertex_normals[faces[i][j][2] - 1])
                varr.append(vertices[faces[i][j][0] - 1])
                varr.append(vertex_normals[faces[i][j + 1][2] - 1])
                varr.append(vertices[faces[i][j + 1][0] - 1])

    # spaghetti,,,,
    if g_toggle_single_hierarchy == True:
        g_vertex_array_seperate = np.array(varr, 'float32')
    else:
        g_h_varr = np.array(varr, 'float32')

    # Create g_vertex_array_indexed & g_index_array
    iarr = []

    ivarr = []                                  # ivarr = [[], vertex, [], v, [], v, ...] 
    num_of_vertex = len(vertices)
    for i in range(num_of_vertex):
        ivarr.append([])                                                  
        ivarr.append(vertices[i])

    normals_sum = []
    normals_num = []
    for i in range(num_of_vertex):
        normals_sum.append([0, 0, 0])
        normals_num.append(0)
    
    for i in range(len(faces)):
        # i: index of face, j: index of v//vn included in the faces[i]
        
        num_of_vertex_in_face = len(faces[i])
        # iarr; append 3 vertices in iarr per 1 repeat
        for j in range(num_of_vertex_in_face - 1):
            if (len(faces[i][j]) == 1):
                sys.exit("There is no vertex normal.")
            else:
                iarr.append(faces[i][0][0] - 1)
                iarr.append(faces[i][j][0] - 1)
                iarr.append(faces[i][j + 1][0] - 1)
        
        # normals sum & num
        for j in range(num_of_vertex_in_face):
            v_index = faces[i][j][0] - 1
            vn_index = faces[i][j][2] - 1

            # num of vertex normals
            normals_num[v_index] += 1
            # sum of vertex normals
            normals_sum[v_index][0] += vertex_normals[vn_index][0]
            normals_sum[v_index][1] += vertex_normals[vn_index][1]
            normals_sum[v_index][2] += vertex_normals[vn_index][2]

    for i in range(num_of_vertex):
        ivarr[2 * i] = (normals_sum[i][0] / normals_num[i], normals_sum[i][1] / normals_num[i], normals_sum[i][2] / normals_num[i])
    
    if g_toggle_single_hierarchy == True:
        g_vertex_array_indexed = np.array(ivarr, 'float32')
        g_index_array = np.array(iarr)
    else:
        g_h_ivarr = np.array(ivarr, 'float32')
        g_h_iarr = np.array(iarr)

    # Pinrt file info. in console
    if is_drop == True:
        print("====================\nFILE INFO (stdout in console)\n--------------------")
        print("File name:", file_name)
        print("Total number of faces:", num_of_faces)
        print("Number of faces with 3 vertices:", num_of_faces_3v)
        print("Number of faces with 4 vertices:", num_of_faces_4v)
        print("Number of faces with more than 4 vertices:", num_of_faces_morev)
        print("====================\n")

def drawObj_glDrawArray(varr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))

    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def drawObj_glDrawElement(varr, iarr):
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)

    glNormalPointer(GL_FLOAT, 6 * varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6 * varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3 * varr.itemsize))

    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

######################################################################
######################################################################
######################################################################
def render():
    global g_azimuth, g_elevation, g_distance
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    # Toggle orthogonal / perspective projection
    if g_toggle_frustum_ortho == False:
        glOrtho(-10, 10, -10, 10, 1, 100)
    else:
        glFrustum(-1, 1, -1, 1, 1, 100)

    myLookAt(np.array([1, 1, 1]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawRectangularGrid()

    ######################################################################
    ######################## ClassAssignment2 ############################
    ######################################################################

    ######################################################################
    # Toggle wireframe / solid mode
    ######################################################################
    global g_toggle_wireframe_solid
    if g_toggle_wireframe_solid == True:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    ######################################################################
    # Lignting Configuration
    ######################################################################
    global g_light0, g_light1, g_light2

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # 3 light sources
    glEnable(GL_LIGHTING)

    if g_light0 == True:
        glEnable(GL_LIGHT0)
    else:
        glDisable(GL_LIGHT0)
    if g_light1 == True:
        glEnable(GL_LIGHT1)
    else:
        glDisable(GL_LIGHT1)
    if g_light2 == True:
        glEnable(GL_LIGHT2)
    else:
        glDisable(GL_LIGHT2)
    
    glEnable(GL_RESCALE_NORMAL)
    glEnable(GL_NORMALIZE)

    # light position
    glPushMatrix()

    light_pos0 = (2., 7., 2., 1.)
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos0)
    light_pos1 = (2., -7., 2., 1.)
    glLightfv(GL_LIGHT1, GL_POSITION, light_pos1)
    light_pos2 = (4., 4., 4., 0.)
    glLightfv(GL_LIGHT2, GL_POSITION, light_pos2)

    glPopMatrix()

    # light intensity
    light_color0 = (.2, 0., .8, 1.)
    ambient_light_color = (.1, .0, .1, 1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_color0)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_color0)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light_color)
    light_color1 = (.8, 0., .2, 1.)
    ambient_light_color = (.1, .0, .1, 1.)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light_color1)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light_color1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, ambient_light_color)
    light_color2 = (0., .5, .5, 1.)
    ambient_light_color = (.0, .1, .1, 1.)
    glLightfv(GL_LIGHT2, GL_DIFFUSE, light_color2)
    glLightfv(GL_LIGHT2, GL_SPECULAR, light_color2)
    glLightfv(GL_LIGHT2, GL_AMBIENT, ambient_light_color)

    # material reflectance
    object_color = (1., 1., 1., 1.)
    specular_object_color = (1., 1., 1., 1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, object_color)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specular_object_color)

    ######################################################################
    # Toggle single_mesh_rendering / hierarchical_modeling
    ######################################################################
    global g_toggle_single_hierarchy
    
    if g_toggle_single_hierarchy == True:
        render_single_mesh()
    else:
        render_hierarchical_model()
    
    glDisable(GL_LIGHTING)

def render_single_mesh():
    global g_vertex_array_seperate
    global g_vertex_array_indexed, g_index_array

    # draw an object
    global g_toggle_normal_smooth

    glPushMatrix()

    glColor3ub(255,255,255)
    if g_toggle_normal_smooth == True:
        drawObj_glDrawArray(g_vertex_array_seperate)
    else:
        drawObj_glDrawElement(g_vertex_array_indexed, g_index_array)

    glPopMatrix()
    
def render_hierarchical_model():
    global g_h_varr, g_h_ivarr, g_h_varr
    global g_toggle_normal_smooth

    t = 2 * glfw.get_time()

    ######################################################################
    # desk movement
    glPushMatrix()
    glTranslatef(3 * np.sin(t / np.pi), 0, 0)

    # draw desk
    glPushMatrix()

    handle_obj_file('./' + 'desk.obj', False)

    glColor3ub(255,255,255)
    glTranslatef(0., -7.3, 0.)
    glRotatef(-90, 1, 0, 0)
    glScalef(.01, .01, .01)

    if g_toggle_normal_smooth == True:
        drawObj_glDrawArray(g_h_varr)
    else:
        drawObj_glDrawElement(g_h_ivarr, g_h_iarr)

    glPopMatrix()
    # ######################################################################

    # ######################################################################
    # cup movement
    glPushMatrix()
    glTranslatef(0, 0, 2 * np.sin(t / np.pi))

    # draw cup
    glPushMatrix()

    handle_obj_file('./' + 'cup.obj', False)

    glColor3ub(255, 255, 255)
    glScalef(.2, .2, .2)

    if g_toggle_normal_smooth == True:
        drawObj_glDrawArray(g_h_varr)
    else:
        drawObj_glDrawElement(g_h_ivarr, g_h_iarr)

    glPopMatrix()
    ######################################################################

    ######################################################################
    # Spoon movement
    glPushMatrix()
    glTranslatef(0.2 * np.sin(t), 0, 0.2 * np.cos(t))
    glRotatef(10, np.sin(t), 0, np.cos(t))
    
    # draw spoon
    glPushMatrix()
    
    handle_obj_file('./' + 'spoon.obj', False)

    glColor3ub(255, 255, 255)
    glScalef(.08, .08, .08)
    glTranslatef(.0, 7.5, .0)
    glRotatef(90, 0, 0, 1)

    if g_toggle_normal_smooth == True:
        drawObj_glDrawArray(g_h_varr)
    else:
        drawObj_glDrawElement(g_h_ivarr, g_h_iarr)

    glPopMatrix()
    ######################################################################

    # spoon, cup, desk
    glPopMatrix()
    glPopMatrix()
    glPopMatrix()


def main():
    if not glfw.init():
        return
    
    # 1
    window = glfw.create_window(720,720,'ClassAssignment2', None,None)
    
    if not window:
        glfw.terminate()
        return

    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.make_context_current(window)

    while not glfw.window_should_close(window):
        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()
