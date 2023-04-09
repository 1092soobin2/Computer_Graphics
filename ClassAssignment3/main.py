import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

######################################################################
######################## ClassAssignment1 ############################
######################################################################

g_azimuth = np.radians(45)
g_elevation = np.radians(45)
g_distance = 1
g_panning = [0, 0]
g_prev_pos = [0, 0]
g_cur_pos = [0, 0]

g_toggle_frustum_ortho = True       # v
g_toggle_wireframe_solid = True     # z

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
######################## ClassAssignment3 ############################
######################################################################

# Make rotation matrix
def rotateX(angle):
    th = np.radians(angle)
    R = np.array([[1,   0,          0],
                  [0,   np.cos(th), -np.sin(th)],
                  [0,   np.sin(th), np.cos(th)]])
    return R
def rotateY(angle):
    th = np.radians(angle)
    R = np.array([[np.cos(th),   0,  np.sin(th)],
                  [0,            1,  0        ],
                  [-np.sin(th),  0,  np.cos(th)]])
    return R
def rotateZ(angle):
    th = np.radians(angle)
    R = np.array([[np.cos(th),  -np.sin(th),    0],
                   [np.sin(th), np.cos(th),    0],
                   [0,          0,              1]])
    return R

class joint:
    def __init__(self, name, parent):
        self.name = name
        self.offset = []
        self.channels = []
        self.parent = parent
        self.children = []
        self.affine_mat = np.identity(4)

class bvh:
    def __init__(self):
        self.joint_list = None
        self.motion_list = None
        self.number_of_frames = 0
        self.frame_time = 0
        self.num_of_root_channel = 0

g_bvh = bvh()

g_toggle_animate = False
def key_callback(window, key, scancode, action, mods):
    global g_toggle_animate, g_toggle_line

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_SPACE:
            g_toggle_animate = not(g_toggle_animate)

def drop_callback(window, paths):
    handle_bvh_file(paths[0])
def handle_bvh_file(path):
    global g_bvh
    global g_toggle_animate

    # B. ii. draw T_pose
    g_toggle_animate = False
    # Info of the bvh file (stdout in console)
    file_name = (path.split('/'))[-1]
    num_of_frames = 0
    frame_per_second = 0
    num_of_joints = 0   # including Root
    list_of_joint_names = []

    # return value
    joint_list = []                     # root joint ... joint end

    # Open file
    fd = open(path, "r")
    file_txt = fd.read()
    fd.close()

    # HIERARCHY Section
    hierarcy_section = ((file_txt.split("MOTION"))[0]).split()
    parent = joint(None, None)         # dummy joint
    now = None

    i = 1
    l = len(hierarcy_section)
    while i < l:
        i += 1
        # name
        # if hierarcy_section[i - 1] in ["ROOT", "JOINT", "END"]:
        if hierarcy_section[i - 1] in ["ROOT", "JOINT", "End"]:
            # parsing
            name = ""
            while hierarcy_section[i + 1] != "{":
                name += hierarcy_section[i] + " "
                i += 1
            name += hierarcy_section[i]
            i += 1         # {

            list_of_joint_names.append(name)

        # {
        if hierarcy_section[i - 1] == "{":
            # new joint
            now = joint(name, parent)
            (parent.children).append(now)
            joint_list.append(now)

            parent = now
            # i += 1

        # offset
        if hierarcy_section[i - 1] == "OFFSET":
            # parsing
            now.offset = hierarcy_section[i : i+3]
            i += 3

        # channels
        if hierarcy_section[i - 1] == "CHANNELS":
            # parsing
            num_of_channel = int(hierarcy_section[i])
            if (g_bvh.num_of_root_channel == 0):
                g_bvh.num_of_root_channel = num_of_channel
            i += 1
            for j in range(num_of_channel):
                channel = hierarcy_section[i][0]
                channel2 = hierarcy_section[i][1]
                if (channel == 'x' or channel == 'X'):
                    if (channel2 == 'p' or channel2 == 'P'):
                        (now.channels).append(0)
                    elif (channel2 == 'r' or channel2 == 'R'):
                        (now.channels).append(3)
                elif (channel == 'y' or channel == 'Y'):
                    if (channel2 == 'p' or channel2 == 'P'):
                        (now.channels).append(1)
                    elif (channel2 == 'r' or channel2 == 'R'):
                        (now.channels).append(4)
                elif (channel == 'z' or channel == 'Z'):
                    if (channel2 == 'p' or channel2 == 'P'):
                        (now.channels).append(2)
                    elif (channel2 == 'r' or channel2 == 'R'):
                        (now.channels).append(5)
                i += 1

        # }
        if hierarcy_section[i - 1] == "}":
            # parent = now.parent
            parent = parent.parent
            # i += 1

    num_of_joints = len(list_of_joint_names)
    g_bvh.joint_list = joint_list
  

    # MOTION section
    motion_section = ((file_txt.split("MOTION"))[1]).split('\n')

    g_bvh.number_of_frames = int((motion_section[1].split())[1])
    g_bvh.frame_time = float(((motion_section[2]).split())[2])

    num_of_frames = g_bvh.number_of_frames
    frame_per_second = int(1 / g_bvh.frame_time)

    tmp_motion_section_str = []
    tmp_motion_section_float = []
    for i in range(0, num_of_frames):
        # split
        tmp_motion_section_str.append(motion_section[i + 3].split())
        # make str to float
        tmp_one_line = []
        for j in range(len(tmp_motion_section_str[i])):
            tmp_one_line.append(float(tmp_motion_section_str[i][j]))
        tmp_motion_section_float.append(tmp_one_line)
    g_bvh.motion_section = tmp_motion_section_float

    # stdout in console
    print("\n>>>>    FILE INFO    <<<<")
    print("File name:", file_name)
    print("Number of frames:", num_of_frames)
    print("FPS:", frame_per_second)
    print("Number of joints:", num_of_joints)
    print("List of all joint names:", list_of_joint_names)
    print(">>>>>>>>>>>>><<<<<<<<<<<<<\n")

def print_joint_list(joint):
    if (joint.name == "Hips"):
        print("joint:", joint.name)
    else:
        print("Parent:", joint.parent.name, "Joint:", joint.name)
    for i in range(len(joint.children)):
        print_joint_list(joint.children[i])

######################################################################
######################################################################
######################################################################
def render():
    global g_toggle_animate

    # Enable depth test
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    ######################################################################
    ######################## ClassAssignment1 ############################
    ######################################################################

    # Toggle orthogonal / perspective projection
    if g_toggle_frustum_ortho == False:
        glOrtho(-10, 10, -10, 10, 1, 100)
    else:
        glFrustum(-1, 1, -1, 1, 1, 1000)

    myLookAt(np.array([1, 1, 1]), np.array([0, 0, 0]), np.array([0, 1, 0]))
    
    drawFrame()
    glColor3ub(255, 255, 255)
    drawRectangularGrid()

    ######################################################################
    ######################## ClassAssignment3 ############################
    ######################################################################
    global g_bvh
    if (g_bvh.joint_list != None):
        if g_toggle_animate == False:
            draw_T_pose()
        else:
            draw_all_frame()

def draw_T_pose():
    global g_bvh
    root = g_bvh.joint_list[0]
    draw_a_joint(root)
def draw_a_joint(joint_obj):
    # draw a line(offset)
    glBegin(GL_LINES)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array(joint_obj.offset))    
    glEnd()
    
    # hierarchy(transl offset)
    glPushMatrix()
    tmp_affine_mat = np.identity(4)
    tmp_affine_mat[:3, 3] = joint_obj.offset
    glMultMatrixf(tmp_affine_mat.T)

    # draw children
    for i in range(len(joint_obj.children)):
        draw_a_joint(joint_obj.children[i])

    glPopMatrix()

g_start_time = -1
def draw_all_frame():
    global g_bvh, g_start_time
    t = glfw.get_time()
    
    if (g_start_time < 0):
        g_start_time = t
    
    lapse_time = (t - g_start_time)
    frame_number = int(lapse_time / g_bvh.frame_time) % g_bvh.number_of_frames    
    draw_one_frame(frame_number) 

def draw_one_frame(frame_number):
    global g_bvh

    num_of_joints = len(g_bvh.joint_list)
    motion = g_bvh.motion_section[frame_number]

    # motion capture
    # ROOT
    index_of_joint_list = 0
    # translate and rotate by motion capture data
    tmp_rot_mat = np.identity(3)
    for index_of_motion in range(g_bvh.num_of_root_channel):
        channel = g_bvh.joint_list[index_of_joint_list].channels[index_of_motion]
        if (channel == 0):          # XPos
            (g_bvh.joint_list[index_of_joint_list].affine_mat)[0, 3] = motion[index_of_motion]
        elif (channel == 1):        # YPos
            (g_bvh.joint_list[index_of_joint_list].affine_mat)[1, 3] = motion[index_of_motion]
        elif (channel == 2):        # ZPos
            (g_bvh.joint_list[index_of_joint_list].affine_mat)[2, 3] = motion[index_of_motion]
        elif (channel == 3):        # XRot
            tmp_rot_mat = tmp_rot_mat @ rotateX(motion[index_of_motion])
        elif (channel == 4):        # YRot
            tmp_rot_mat = tmp_rot_mat @ rotateY(motion[index_of_motion])
        elif (channel == 5):        # ZRot
            tmp_rot_mat = tmp_rot_mat @ rotateZ(motion[index_of_motion])
    (g_bvh.joint_list[index_of_joint_list].affine_mat)[:3, :3] = tmp_rot_mat

    # JOINT, END
    num_of_End = 0
    for index_of_joint_list in range(1, len(g_bvh.joint_list)):
        if (g_bvh.joint_list[index_of_joint_list].channels == []):
            num_of_End += 1
            continue
        # translate as offset
        (g_bvh.joint_list[index_of_joint_list].affine_mat)[:3, 3] = g_bvh.joint_list[index_of_joint_list].offset
        # rotate by motion capture data
        tmp_rot_mat = np.identity(3)
        start = g_bvh.num_of_root_channel + (index_of_joint_list - 1 - num_of_End) * 3
        for index_of_motion in range(start, start + 3):
            channel = g_bvh.joint_list[index_of_joint_list].channels[index_of_motion - start]   # channel: 0, 1, 2
            if (channel == 3):        # XRot
                tmp_rot_mat = tmp_rot_mat @ rotateX(motion[index_of_motion])
            elif (channel == 4):        # YRot
                tmp_rot_mat = tmp_rot_mat @ rotateY(motion[index_of_motion])
            elif (channel == 5):        # ZRot
                tmp_rot_mat = tmp_rot_mat @ rotateZ(motion[index_of_motion])
        (g_bvh.joint_list[index_of_joint_list].affine_mat)[:3, :3] = tmp_rot_mat
    # draw a character
    root = g_bvh.joint_list[0]
    draw_a_joint2(root)

def draw_a_joint2(joint_obj):
    # draw a line(offset)
    glBegin(GL_LINES)
    glVertex3fv(np.array([0., 0., 0.]))
    glVertex3fv(np.array(joint_obj.offset))    
    glEnd()

    # hierarchy
    glPushMatrix()
    glMultMatrixf((joint_obj.affine_mat).T)

    # draw children 
    for i in range(len(joint_obj.children)):
        draw_a_joint2(joint_obj.children[i])
    
    glPopMatrix()

def main():
    if not glfw.init():
        return
    
    # 1
    window = glfw.create_window(720,720,'ClassAssignment3', None,None)
    
    if not window:
        glfw.terminate()
        return

    glfw.set_mouse_button_callback(window, button_callback)
    glfw.set_cursor_pos_callback(window, cursor_callback)
    glfw.set_scroll_callback(window, scroll_callback)
    glfw.set_key_callback(window, key_callback)
    glfw.set_drop_callback(window, drop_callback)

    glfw.make_context_current(window)
    
    glfw.swap_interval(1)

    while not glfw.window_should_close(window):

        glfw.poll_events()
        render()
        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()