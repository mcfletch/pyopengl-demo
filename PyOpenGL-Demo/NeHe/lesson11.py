#! /usr/bin/env python
# -*- coding: utf8 -*-
# Conversion contributed by: Ivan Izuver <izuver@users.sourceforge.net>
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from math import sin
 
import sys
import numpy # or Numeric


ESCAPE = '\033'

w_count=0
hold = 0.0

# Number of the glut window.
window = 0

# 3D array
points = numpy.zeros((46, 46, 3), 'f')

# rotation
xrot = yrot = zrot = 0.0
		
# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                 # We call this right after our OpenGL window is created.
  
	glClearColor(0.0, 0.0, 0.0, 0.0)       # This Will Clear The Background Color To Black
	glClearDepth(1.0)                      # Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)                   # The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
	glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
	
	glPolygonMode(GL_BACK,GL_FILL)
	glPolygonMode(GL_FRONT,GL_LINE)
	
	# walk on plane X
	for x in xrange(45):
		# walk on plane Y
		for y in xrange(45):
			# apply wave to grid
			points[x][y][0]=float((x/5.0)-4.5)
			points[x][y][1]=float((y/5.0)-4.5)
			points[x][y][2]=float(sin((((x/5.0)*40.0)/360.0)*3.141592654*2.0))

		
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
	global xrot,yrot,zrot,w_count
	
	float_x=float_y=float_xb=float_yb=0.0 # for division our flag on small quads
	
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()                         # Reset The View
	
	glTranslatef(0.0,0.0,-12.0)
	
	glRotatef(xrot,1.0,0.0,0.0)     # rotate by x
	glRotatef(yrot,0.0,1.0,0.0)     # rotate by y
	glRotatef(zrot,0.0,0.0,1.0)     # rotate by z
	
	# build the wave
	glBegin(GL_QUADS)
	for x in xrange(45):
		for y in xrange(45):
			float_x = float(x)/44.0
			float_y = float(y)/44.0
			float_xb = float(x+1)/44.0
			float_yb = float(y+1)/44.0
			
			# bottom left
			glTexCoord2f(float_x, float_y)
			glColor3f(0.0,0.0,0.0)
			glVertex3f(points[x][y][0],points[x][y][1],points[x][y][2])
			
			# upper left
			glTexCoord2f( float_x, float_yb )
			glColor3f(0.0,0.5,0.0) # set grid color
			glVertex3f( points[x][y+1][0], points[x][y+1][1], points[x][y+1][2])
			
			# upper right
			glTexCoord2f( float_xb, float_yb )
			glVertex3f( points[x+1][y+1][0], points[x+1][y+1][1], points[x+1][y+1][2])
			
			# bottom right
			glTexCoord2f( float_xb, float_y )
			glVertex3f( points[x+1][y][0], points[x+1][y][1], points[x+1][y][2])
			
	glEnd()
	
	if w_count==2: # for slowing the wave
		for y in xrange(45): # walk on plane Y
			hold=points[0][y][2] # save the current value of left side one point 
			for x in xrange(45): # walk on plane Y
				points[x][y][2] = points[x+1][y][2]  
			points[44][y][2]=hold 
		w_count = 1
	w_count+=1
				
	# uncomment if need
	#xrot+=0.6
	#yrot+=0.5
	#zrot+=0.8
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
	glutInitWindowSize(800, 600)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(200, 200)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("Wave by RISC")

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
