import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
from OpenGL.arrays import vbo
import ctypes

gCamAng = 0.
gCamHeight = 1.

def createVertexAndIndexArrayIndexed():
    varr = np.array([
            ( -0.5773502691896258 , 0.5773502691896258 ,  0.5773502691896258 ),
            ( -1 ,  1 ,  1 ), # v0
            ( 0.8164965809277261 , 0.4082482904638631 ,  0.4082482904638631 ),
            (  1 ,  1 ,  1 ), # v1
            ( 0.4082482904638631 , -0.4082482904638631 ,  0.8164965809277261 ),
            (  1 , -1 ,  1 ), # v2
            ( -0.4082482904638631 , -0.8164965809277261 ,  0.4082482904638631 ),
            ( -1 , -1 ,  1 ), # v3
            ( -0.4082482904638631 , 0.4082482904638631 , -0.8164965809277261 ),
            ( -1 ,  1 , -1 ), # v4
            ( 0.4082482904638631 , 0.8164965809277261 , -0.4082482904638631 ),
            (  1 ,  1 , -1 ), # v5
            ( 0.5773502691896258 , -0.5773502691896258 , -0.5773502691896258 ),
            (  1 , -1 , -1 ), # v6
            ( -0.8164965809277261 , -0.4082482904638631 , -0.4082482904638631 ),
            ( -1 , -1 , -1 ), # v7
            ], 'float32')
    iarr = np.array([
            (0,2,1),
            (0,3,2),
            (4,5,6),
            (4,6,7),
            (0,1,5),
            (0,5,4),
            (3,6,2),
            (3,7,6),
            (1,2,6),
            (1,6,5),
            (0,7,3),
            (0,4,7),
            ])
    return varr, iarr

def drawCube_glDrawElements():
    global gVertexArrayIndexed, gIndexArray
    varr = gVertexArrayIndexed
    iarr = gIndexArray
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawElements(GL_TRIANGLES, iarr.size, GL_UNSIGNED_INT, iarr)

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([3.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,3.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,3.]))
    glEnd()

# slerp
def l2norm(v):
    return np.sqrt(np.dot(v, v))
def normalized(v):
    l = l2norm(v)
    return 1/l * np.array(v)
def lerp(v1, v2, t):
    return (1-t)*v1 + t*v2

def exp(rv):
    t = l2norm(rv)
    rv = normalized(rv)
    R = np.array([[np.cos(t)+(rv[0]**2)*(1-np.cos(t)), rv[0]*rv[1]*(1-np.cos(t))-rv[2]*np.sin(t), rv[0]*rv[2]*(1-np.cos(t))+rv[1]*np.sin(t)],
                [rv[1]*rv[0]*(1-np.cos(t))+rv[2]*np.sin(t), np.cos(t)+(rv[1]**2)*(1-np.cos(t)), rv[1]*rv[2]*(1-np.cos(t))-rv[0]*np.sin(t)],
                [rv[2]*rv[0]*(1-np.cos(t))-rv[1]*np.sin(t), rv[2]*rv[1]*(1-np.cos(t))+rv[0]*np.sin(t), np.cos(t)+(rv[2]**2)*(1-np.cos(t))]])
    return R

def log(R):
    rv = np.zeros(3)
    th = np.arccos((R[0][0]+R[1][1]+R[2][2]-1)/2)
    rv[0] = (R[2][1]-R[1][2])/(2*np.sin(th))
    rv[1] = (R[0][2]-R[2][0])/(2*np.sin(th))
    rv[2] = (R[1][0]-R[0][1])/(2*np.sin(th))
    return th*rv

def slerp(R1,R2,t):
    return R1 @ exp (t * log(R1.T @ R2))
'''
def exp(rv):
    th = l2norm(rv)
    if th == 0:
        u = np.array([0, 0, 0])
    else:
        u = normalized(rv)

    cos = np.cos(th)
    sin = np.sin(th)
    ux = u[0]
    uy = u[1]
    uz = u[2]
    print('in exp uxuyuz:', ux, uy, uz, '\n')

    R = [[cos + ux*ux*(1-cos),      ux*uy*(1-cos) - uz*sin, ux*uz*(1-cos) + uy*sin],
         [uy*ux*(1-cos) + uz*sin,   cos + uy*uy*(1-cos),    uy*uz*(1-cos) - ux*sin],
         [uz*ux*(1-cos) - uy*sin,   uz*uy*(1-cos) + ux*sin, cos + uz*uz*(1-cos)]]
    
    return np.array(R)
def log(R):
    v = [0, 0, 0]

    th = np.arccos((R[0, 0] + R[1, 1] + R[2, 2] - 1) / 2) 
    
    v[0] = (R[2, 1] - R[1, 2]) / (2 * np.sin(th))
    v[1] = (R[0, 2] - R[2, 0]) / (2 * np.sin(th))
    v[2] = (R[1, 0] - R[0, 1]) / (2 * np.sin(th))

    # tr = R[0, 0] + R[1, 1] + R[2, 2]
    
    # if tr == 3:                         # th = arccos(1) = 0
    #     pass
    # elif tr == -1:                      # th = arccos(-1) = 180
    #     if R[0, 0] == 1:
    #         v = np.array([1, 0, 0])
    #     elif R[1, 1] == 1:
    #         v = np.array([0, 1, 0])
    #     elif R[2, 2] == 1:
    #         v = np.array([0, 0, 1])
    # else:                               # th = arccos(x)
    #     th = np.arccos((tr - 1) / 2) 
    #     v[0] = (R[2, 1] - R[1, 2]) / (2 * np.sin(th))
    #     v[1] = (R[0, 2] - R[2 ,0]) / (2 * np.sin(th))
    #     v[2] = (R[1, 0] - R[0, 1]) / (2 * np.sin(th))

    return np.array(v) * th
'''

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

# def get_frame_number(time):
#     return int((time % 1) * 61)

R1 = [np.identity(4), np.identity(4), np.identity(4), np.identity(4)]
T1 = [np.identity(4), np.identity(4), np.identity(4), np.identity(4)]
R2 = [np.identity(4), np.identity(4), np.identity(4), np.identity(4)]
def createR1T1R2():
    # frame 0
    Rx = rotateX(20)
    Ry = rotateY(30)
    Rz = rotateZ(30)
    R1[0][:3, :3] = Rx @ Ry @ Rz

    T1[0][0][3] = 1.
    Rx = rotateX(15)
    Ry = rotateY(30)
    Rz = rotateZ(25)
    R2[0][:3, :3] = Rx @ Ry @ Rz

    # frame 20
    Rx = rotateX(45)
    Ry = rotateY(60)
    Rz = rotateZ(40)
    R1[1][:3, :3] = Rx @ Ry @ Rz

    T1[1][0][3] = 1.
    Rx = rotateX(25)
    Ry = rotateY(40)
    Rz = rotateZ(40)
    R2[1][:3, :3] = Rx @ Ry @ Rz

    # frmae 40
    Rx = rotateX(60)
    Ry = rotateY(70)
    Rz = rotateZ(50)
    R1[2][:3, :3] = Rx @ Ry @ Rz
    
    T1[2][0][3] = 1.
    Rx = rotateX(40)
    Ry = rotateY(60)
    Rz = rotateZ(50)
    R2[2][:3, :3] = Rx @ Ry @ Rz
    # frame 60

    Rx = rotateX(80)
    Ry = rotateY(85)
    Rz = rotateZ(70)
    R1[3][:3, :3] = Rx @ Ry @ Rz
    
    T1[3][0][3] = 1.
    Rx = rotateX(55)
    Ry = rotateY(80)
    Rz = rotateZ(65)
    R2[3][:3, :3] = Rx @ Ry @ Rz

def drawUnitCube_glDrawArray():
    global gVertexArraySeparate
    varr = gVertexArraySeparate
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glNormalPointer(GL_FLOAT, 6*varr.itemsize, varr)
    glVertexPointer(3, GL_FLOAT, 6*varr.itemsize, ctypes.c_void_p(varr.ctypes.data + 3*varr.itemsize))
    glDrawArrays(GL_TRIANGLES, 0, int(varr.size/6))

def drawFrame():
    glBegin(GL_LINES)
    glColor3ub(255, 0, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([1.,0.,0.]))
    glColor3ub(0, 255, 0)
    glVertex3fv(np.array([0.,0.,0.]))
    glVertex3fv(np.array([0.,1.,0.]))
    glColor3ub(0, 0, 255)
    glVertex3fv(np.array([0.,0.,0]))
    glVertex3fv(np.array([0.,0.,1.]))
    glEnd()

def render(frame_number):
    global gCamAng, gCamHeight

    # Enable depth test
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glEnable(GL_DEPTH_TEST)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, 1, 1,10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(5*np.sin(gCamAng),gCamHeight,5*np.cos(gCamAng), 0,0,0, 0,1,0)

    # draw global frame
    drawFrame()

    ############################################################
    # Lighting
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)

    glEnable(GL_RESCALE_NORMAL)

    lightPos = (3.,4.,5.,1.)
    glLightfv(GL_LIGHT0, GL_POSITION, lightPos)

    lightColor = (1.,1.,1.,1.)
    ambientLightColor = (.1,.1,.1,1.)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightColor)
    glLightfv(GL_LIGHT0, GL_SPECULAR, lightColor)
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambientLightColor)
    
    ############################################################
    # Draw each frame
    global R1, T1, R2
    # frame_number = get_frame_number(t)

    ############################################################
    # frame 0
    objectColor = (1.,0.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    # joint J1
    J1 = R1[0]
    # link
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5, 0, 0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    # joint J2
    J2 = R1[0] @ T1[0] @ R2[0]
    # link
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    ############################################################
    # frame 20
    objectColor = (1.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    # joint J1
    J1 = R1[1]
    # link
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    # joint J2
    J2 = R1[1] @ T1[1] @ R2[1]
    #link
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    ############################################################
    # frame 40
    objectColor = (0.,1.,0.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    # joint J1
    J1 = R1[2]
    # link
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    # joint J2
    J2 = R1[2] @ T1[2] @ R2[2]
    #link
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    ############################################################
    # frame 60
    objectColor = (0.,0.,1.,1.)
    specularObjectColor = (1.,1.,1.,1.)
    glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
    glMaterialfv(GL_FRONT, GL_SHININESS, 10)
    glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

    # joint J1
    J1 = R1[3]
    # link
    glPushMatrix()
    glMultMatrixf(J1.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    # joint J2
    J2 = R1[3] @ T1[3] @ R2[3]
    #link
    glPushMatrix()
    glMultMatrixf(J2.T)
    glPushMatrix()
    glTranslatef(0.5,0,0)
    glScalef(0.5, 0.05, 0.05)
    drawCube_glDrawElements()
    glPopMatrix()
    glPopMatrix()

    ############################################################
    # inner frame
    if (frame_number not in [0, 20, 40, 60]) :
        prev_index = (int(frame_number / 20))
        next_index = (prev_index + 1) 
        scaling = (frame_number % 20) / 20

        ############################################################    
        objectColor = (1.,1.,1.,1.)
        specularObjectColor = (1.,1.,1.,1.)
        glMaterialfv(GL_FRONT, GL_AMBIENT_AND_DIFFUSE, objectColor)
        glMaterialfv(GL_FRONT, GL_SHININESS, 10)
        glMaterialfv(GL_FRONT, GL_SPECULAR, specularObjectColor)

        # joint J1
        inner_R1 = np.identity(4)
        inner_R1[:3, :3] = slerp(R1[prev_index][:3, :3], R1[next_index][:3, :3], scaling)
        J1 =  inner_R1
        # link
        glPushMatrix()
        glMultMatrixf(J1.T)
        glPushMatrix()
        glTranslatef(0.5, 0, 0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

        # joint J2
        inner_T1 = np.identity(4)
        inner_T1[:3, 3] = lerp(T1[prev_index][:3, 3], T1[next_index][:3, 3], scaling)
        inner_R2 = np.identity(4)
        inner_R2[:3, :3] = slerp(R2[prev_index][:3, :3], R2[next_index][:3, :3], scaling)
        J2 = inner_R1 @ inner_T1 @ inner_R2
        # link
        glPushMatrix()
        glMultMatrixf(J2.T)
        glPushMatrix()
        glTranslatef(0.5, 0, 0)
        glScalef(0.5, 0.05, 0.05)
        drawCube_glDrawElements()
        glPopMatrix()
        glPopMatrix()

    glDisable(GL_LIGHTING)

def key_callback(window, key, scancode, action, mods):
    global gCamAng, gCamHeight
    # rotate the camera when 1 or 3 key is pressed or repeated
    if action==glfw.PRESS or action==glfw.REPEAT:
        if key==glfw.KEY_1:
            gCamAng += np.radians(-10)
        elif key==glfw.KEY_3:
            gCamAng += np.radians(10)
        elif key==glfw.KEY_2:
            gCamHeight += .1
        elif key==glfw.KEY_W:
            gCamHeight += -.1

gVertexArrayIndexed = None
gIndexArray = None

def main():
    global gVertexArrayIndexed, gIndexArray

    if not glfw.init():
        return

    window = glfw.create_window(640,640,'2019011449', None,None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.swap_interval(1)

    gVertexArrayIndexed, gIndexArray = createVertexAndIndexArrayIndexed()
    createR1T1R2()

    frame_number = 0
    while not glfw.window_should_close(window):
        glfw.poll_events()

        frame_number = frame_number % 61
        render(frame_number)
        frame_number += 1

        glfw.swap_buffers(window)

    glfw.terminate()

if __name__ == "__main__":
    main()

 