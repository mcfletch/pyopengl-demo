#! /usr/bin/env python
# -*- coding: utf8 -*-
"""Port of NeHe Lesson 26 by Ivan Izuver <izuver@users.sourceforge.net>"""
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Image import *
import sys,gc


ESCAPE = '\033'

# Number of the glut window.
window = 0

LightAmb=(0.7,0.7,0.7)  #Окружающий свет
LightDif=(1.0,1.0,0.0)  #Рассеянный свет
LightPos=(4.0,4.0,6.0,1.0) #Позиция источника освещения
#q=GLUquadricObj()
xrot=yrot=0.0 #Вращение по Х Y

xrotspeed=yrotspeed=0.0 #Скорость вращения по X Y
zoom=-3.0 #Глубина сцены в экране
height=0.5 #Высота мяча над полом
textures = {}

def LoadTextures(fname):
	if textures.get( fname ) is not None:
		return textures.get( fname )
	texture = textures[fname] = glGenTextures(1)
	image = open(fname)
	
	ix = image.size[0]
	iy = image.size[1]
	image = image.tostring("raw", "RGBX", 0, -1)
	
	# Create Texture    
	glBindTexture(GL_TEXTURE_2D, texture)   # 2d texture (x and y size)
	
	glPixelStorei(GL_UNPACK_ALIGNMENT,1)
	glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
	glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
	return texture

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
	glClearColor(0.2, 0.5, 1.0, 1.0)    # This Will Clear The Background Color To Black
	glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
	glClearStencil(0)
	glDepthFunc(GL_LEQUAL)                # The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
	glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
	
	glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
	glEnable(GL_TEXTURE_2D)
	
	glLightfv(GL_LIGHT0, GL_AMBIENT, LightAmb)
	glLightfv(GL_LIGHT0, GL_DIFFUSE, LightDif)
	glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
	glEnable(GL_LIGHT0)           
	glEnable(GL_LIGHTING)
	
   

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

def DrawObject():
	glColor3f(1.0, 1.0, 1.0);
	glBindTexture( GL_TEXTURE_2D, LoadTextures('NeHe.bmp') )
	
	Q=gluNewQuadric()
	gluQuadricNormals(Q, GL_SMOOTH)
	gluQuadricTexture(Q, GL_TRUE)
	glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
	
	gluSphere(Q, 0.35, 32, 16)

	glColor4f(1.0, 1.0, 1.0, 0.4)
	glEnable(GL_BLEND)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE)
	glEnable(GL_TEXTURE_GEN_S)
	glEnable(GL_TEXTURE_GEN_T)
	gluSphere(Q, 0.35, 32, 16)
	
	glDisable(GL_TEXTURE_GEN_S)
	glDisable(GL_TEXTURE_GEN_T)
	glDisable(GL_BLEND)
	gluDeleteQuadric( Q )

def DrawFloor():
	glBindTexture( GL_TEXTURE_2D, LoadTextures('NeHe2.bmp') )
	
	glBegin(GL_QUADS)           # Begin draw

	glNormal3f(0.0, 1.0, 0.0) # Upper normal
	glTexCoord2f(0.0, 1.0)  # bottom left side of texture

	glVertex3f(-2.0, 0.0, 2.0) # bottom left angle of floor
	glTexCoord2f(0.0, 0.0)  # upper left side of texture

	glVertex3f(-2.0, 0.0,-2.0)# upper left angle of floor
	glTexCoord2f(1.0, 0.0)  #upper right side of texture

	glVertex3f( 2.0, 0.0,-2.0) # upper right angle of floor
	glTexCoord2f(1.0, 1.0)  # bottom right side of texture

	glVertex3f( 2.0, 0.0, 2.0)# bottom right angle of floor

	glEnd()                     # finish draw


# The main drawing function. 
def DrawGLScene():
	pass
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT|GL_STENCIL_BUFFER_BIT)
	eqr=(0.0,-1.0, 0.0, 0.0)
	
	glLoadIdentity()                         # Reset The View
	
	glTranslatef(0.0, -0.6, zoom)
	
	glColorMask(0,0,0,0)
	
	glEnable(GL_STENCIL_TEST)
	
	glStencilFunc(GL_ALWAYS, 1, 1)
	glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
	glDisable(GL_DEPTH_TEST)
	
	DrawFloor()

	glEnable(GL_DEPTH_TEST)
	glColorMask(1,1,1,1)
	glStencilFunc(GL_EQUAL, 1, 1)
	glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)
	
	glEnable(GL_CLIP_PLANE0)
	glClipPlane(GL_CLIP_PLANE0, eqr)
	glPushMatrix()
	glScalef(1.0, -1.0, 1.0)

	glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
	glTranslatef(0.0, height, 0.0)
	glRotatef(xrot, 1.0, 0.0, 0.0)
	glRotatef(yrot, 0.0, 1.0, 0.0)
	
	DrawObject()
	
	glPopMatrix()
	glDisable(GL_CLIP_PLANE0)
	glDisable(GL_STENCIL_TEST)
	
	glLightfv(GL_LIGHT0, GL_POSITION, LightPos)
	glEnable(GL_BLEND)
	glDisable(GL_LIGHTING)
	glColor4f(1.0, 1.0, 1.0, 0.8)
	glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
	
	DrawFloor()
	
	glEnable(GL_LIGHTING)
	glDisable(GL_BLEND)
	glTranslatef(0.0, height, 0.0)
	glRotatef(xrot, 1.0, 0.0, 0.0)
	glRotatef(yrot, 0.0, 1.0, 0.0)
	DrawObject()
	
	glFlush()

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
	window = glutCreateWindow("Realistic Reflection by RISC")

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
		
