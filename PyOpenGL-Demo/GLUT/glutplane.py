import sys

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
from math import *
from random import random, choice, randint, getrandbits

"""                       
   Copyright (c) Mark J. Kilgard, 1994.   

   This program is freely distributable without licensing fees 
   and is provided without guarantee or warrantee expressed or 
   implied. This program is -not- in the public domain.  
"""
M_PI   = pi
M_PI_2 = pi / 2.0

moving = False
MAX_PLANES = 15

# define plane object
#
class plane(object):
    def __init__(self, speed, red, green, blue, theta, x, y, z, angle):
        self.speed = speed
        self.red   = red
        self.green = green
        self.blue  = blue
        self.theta = theta
        self.angle = angle
        self.x = x
        self.y = y
        self.z = z 

# create list of planes
#
planes = []        
for n in range(MAX_PLANES) :
    p = plane(0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    planes.append(p)


# define the GLUT display function
#
def draw():
    glClear(GL_DEPTH_BUFFER_BIT)
    # paint black to blue smooth shaded polygon for background 
    glDisable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glBegin(GL_POLYGON);
    glColor3f(0.0, 0.0, 0.0);
    glVertex3f(-20.0, 20.0, -19.0)
    glVertex3f( 20.0, 20.0, -19.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex3f( 20.0, -20.0, -19.0)
    glVertex3f(-20.0, -20.0, -19.0)
    glEnd()
    # paint planes 
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_FLAT)
    for n in range(MAX_PLANES) :
        if (planes[n].speed != 0.0) :
            glPushMatrix()
            glTranslatef(planes[n].x, planes[n].y, planes[n].z)
            glRotatef(290.0, 1.0, 0.0, 0.0)
            glRotatef(planes[n].angle, 0.0, 0.0, 1.0)
            glScalef(1.0 / 3.0, 1.0 / 4.0, 1.0 / 4.0)
            glTranslatef(0.0, -4.0, -1.5)
            glBegin(GL_TRIANGLE_STRIP)
            # left wing 
            glVertex3f(-7.0, 0.0, 2.0)
            glVertex3f(-1.0, 0.0, 3.0)
            red   = planes[n].red
            green = planes[n].green
            blue  = planes[n].blue
            glColor3f(red, green, blue)
            glVertex3f(-1.0, 7.0, 3.0)
            # left side 
            glColor3f(0.6 * red, 0.6 * green, 0.6 * blue)
            glVertex3f(0.0, 0.0, 0.0)
            glVertex3f(0.0, 8.0, 0.0)
            # right side
            glVertex3f(1.0, 0.0, 3.0)
            glVertex3f(1.0, 7.0, 3.0)
            # final tip of right wing */
            glColor3f(red, green, blue)
            glVertex3f(7.0, 0.0, 2.0)
            glEnd()
            glPopMatrix()
     
    glutSwapBuffers()
    return

# define the plane position and speed incrementor
#
def tick_per_plane(i):
    planes[i].theta += planes[i].speed
    theta = planes[i].theta
    planes[i].z = -10 + 4 * cos(theta)
    planes[i].x = 5 * sin(2 * theta)
    planes[i].y = sin(theta / 3.4) * 3
    planes[i].angle = ((atan(2.0) + M_PI_2) * sin(theta) - M_PI_2) * 180 / M_PI
    if (planes[i].speed < 0.0) :
        planes[i].angle += 180.0
    return

#define the list of rgb tuples for setting plane colours by random choice
#
rgblist = [(1.0, 0.0, 0.0),  # red 
           (1.0, 1.0, 1.0),  # white 
           (0.0, 1.0, 0.0),  # green
           (1.0, 0.0, 1.0),  # magenta
           (1.0, 1.0, 0.0),  # yellow
           (0.0, 1.0, 1.0)   # cyan
          ]

# define add planes to display of planes
# 
def add_plane():
    for i in range(MAX_PLANES) :
        if (planes[i].speed == 0.0) :
            planes[i].red, planes[i].green, planes[i].blue = choice(rgblist)
            planes[i].speed = (float(randint(0, 19)) * 0.001) + 0.02
            if (getrandbits(32) & 0x1) :
                planes[i].speed *= -1
            planes[i].theta = float(randint(0, 256)) * 0.1111
            tick_per_plane(i)
            if (not moving) :
                glutPostRedisplay()
            return
    return


# define remove a plane from display of planes
#
def remove_plane():
    for i in range(MAX_PLANES-1, -1, -1) :
      if (planes[i].speed != 0) :
          planes[i].speed = 0
          if (not moving) :
              glutPostRedisplay()
          return
    return

#define choice of planes to animate
#
def tick():
    for i in range(MAX_PLANES) :
        if (planes[i].speed != 0.0) :
            tick_per_plane(i)
    return

# define animator so that motion can be started
def animate():
    tick()
    glutPostRedisplay()
    return


def visible(state):
    if (state == GLUT_VISIBLE) :
        if (moving) :
            glutIdleFunc(animate)
    else :
        if (moving) :
            glutIdleFunc(None)
    return


# ARGSUSED1 

def keyboard( ch,  x,  y):
    if(ch == ' ') :
        if (not moving) :
            tick()
            glutPostRedisplay()
    elif (ch == chr(27)) :
        sys.exit(0)
    return 0

VOID, ADD_PLANE, REMOVE_PLANE, MOTION_ON, MOTION_OFF, QUIT = range(6)

def domotion_on(): 
    moving = GL_TRUE
    glutChangeToMenuEntry(3, "Motion off", MOTION_OFF)
    glutIdleFunc(animate)
    return

def domotion_off():
    moving = GL_FALSE
    glutChangeToMenuEntry(3, "Motion", MOTION_ON)
    glutIdleFunc(None)
    return

def doquit():
    sys.exit(0)
    return

menudict ={ADD_PLANE : add_plane, 
           REMOVE_PLANE : remove_plane, 
           MOTION_ON : domotion_on, 
           MOTION_OFF: domotion_off, 
           QUIT : doquit}

def dmenu(item):
    menudict[item]()
    return 0

if __name__ == "__main__":
	glutInit(['glutplane'])
	glutInitWindowPosition(112, 84)
	glutInitWindowSize(800, 600)
	# use multisampling if available 
	glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH | GLUT_MULTISAMPLE)
	wintitle = "glutplane  Copyright (c) Mark J. Kilgard, 1994. RIGHT-CLICK for menu"
	glutCreateWindow(wintitle)
	glutDisplayFunc(draw)
	glutKeyboardFunc(keyboard)
	glutVisibilityFunc(visible)
	#
	# This program fails if PyOpenGL-3.0.0b1-py2.5.egg\OpenGL\GLUT\special.py
	# is not corrected at line 158 to read :
	# callbackType = ctypes.CFUNCTYPE( None, ctypes.c_int )
	# instead of :
	# callbackType = ctypes.CFUNCTYPE( ctypes.c_int, ctypes.c_int )
	#
	# RIGHT-CLICK to display the menu
	#
	glutCreateMenu(dmenu)
	glutAddMenuEntry("Add plane", ADD_PLANE)
	glutAddMenuEntry("Remove plane", REMOVE_PLANE)
	glutAddMenuEntry("Motion", MOTION_ON)
	glutAddMenuEntry("Quit", QUIT)
	glutAttachMenu(GLUT_RIGHT_BUTTON)

	# setup OpenGL state 
	glClearDepth(1.0)
	glClearColor(0.0, 0.0, 0.0, 0.0)
	glMatrixMode(GL_PROJECTION)
	glFrustum(-1.0, 1.0, -1.0, 1.0, 1.0, 30)
	glMatrixMode(GL_MODELVIEW)
	# add three initial random planes 
	add_plane()
	add_plane()
	add_plane()
	# start event processing */
	print 'RIGHT-CLICK to display the menu.'
	glutMainLoop()

