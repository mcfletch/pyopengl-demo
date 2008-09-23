#! /usr/bin/env python
# -*- coding: utf8 -*-
"""Port of NeHe Lesson 12 by Ivan Izuver <izuver@users.sourceforge.net>"""
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import sys
import numpy

ESCAPE = '\033'

# Number of the glut window.
window = 0
xloop=yloop=0
xrot=yrot=0

boxcol=numpy.zeros((5, 3), 'f')
boxcol[0]=1.0,0.0,0.0
boxcol[1]=1.0,0.5,0.0
boxcol[2]=1.0,1.0,0.0
boxcol[3]=0.0,1.0,0.0
boxcol[4]=0.0,1.0,1.0

topcol=numpy.zeros((5, 3), 'f')
topcol[0]=0.5,0.0,0.0
topcol[1]=0.5,0.25,0.0
topcol[2]=0.5,0.5,0.0
topcol[3]=0.0,0.5,0.0
topcol[4]=0.0,0.5,0.5

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
	glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
	glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LEQUAL)                # The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
	glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
	
	glEnable(GL_LIGHT0)
	glEnable(GL_LIGHTING)
	glEnable(GL_COLOR_MATERIAL)
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()                    # Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
	if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1

	glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	
	box=glGenLists(2)
	
	# create list maned box (with quad)
	glNewList(box,GL_COMPILE)
	
	glBegin(GL_QUADS);
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, 1.0)
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
	
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, 1.0)
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, 1.0)
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0, 1.0, 1.0)
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
	
	glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)        
	glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 1.0, -1.0)        
	glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, 1.0, -1.0)        
	glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)        
 
	glTexCoord2f(1.0 , 0.0 ); glVertex3f( 1.0 , -1.0 , -1.0 )        
	glTexCoord2f(1.0 , 1.0 ); glVertex3f( 1.0 , 1.0 , -1.0 )
	glTexCoord2f(0.0 , 1.0 ); glVertex3f( 1.0 , 1.0 , 1.0 )
	glTexCoord2f(0.0 , 0.0 ); glVertex3f( 1.0 , -1.0 , 1.0 )
							
	glTexCoord2f(0.0 , 0.0 ); glVertex3f(-1.0 , -1.0 , -1.0 )        
	glTexCoord2f(1.0 , 0.0 ); glVertex3f(-1.0 , -1.0 , 1.0 )
	glTexCoord2f(1.0 , 1.0 ); glVertex3f(-1.0 , 1.0 , 1.0 )
	glTexCoord2f(0.0 , 1.0 ); glVertex3f(-1.0 , 1.0 , -1.0 )      
	glEnd();                        
	glEndList(); 
	
	top=box+1
	# create new list named top ( with head of quad)
	glNewList(top,GL_COMPILE)
	
	glBegin(GL_QUADS)
	glTexCoord2f(0.0, 1.0); glVertex3f(-1.0, 1.0, -1.0);
	glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, 1.0, 1.0);
	glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, 1.0, 1.0);
	glTexCoord2f(1.0, 1.0); glVertex3f( 1.0, 1.0, -1.0);
	glEnd()
	glEndList()   

	for yloop in range(6):
		for xloop in range(5):
			glLoadIdentity()                         # Reset The View
			glTranslatef(1.4+(float(xloop)*2.8)-(float(yloop)*1.4),((6.0-float(yloop))*2.4)-7.0,-20.0)
			glRotatef(45.0-(2.0*yloop)+xrot,1.0,0.0,0.0);      
			glRotatef(45.0+yrot,0.0,1.0,0.0);                  
			
			glColor3fv(boxcol[yloop-1]);             
			glCallList(box);                        # call list named box
			
			glColor3fv(topcol[yloop-1]);            
			glCallList(top);                        # call list named top

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
	global window
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		sys.exit()

def main():
	global window
	# pass arguments to init
	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(640, 480)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("glLists by RISC")

	   # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.    
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	#glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine    
	glutMainLoop()

# Print message to console, and kick off the main to get it rolling.
if __name__ == "__main__":
	print "Hit ESC key to quit."
	main()
			
