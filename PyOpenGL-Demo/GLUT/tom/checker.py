"""GLUT replacement for the original checker.py demonstration code

Note:
	Has no navigation code ATM.
"""

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

__version__='$Revision: 1.1.1.1 $'[11:-2]
__date__ = '$Date: 2007/02/15 19:25:11 $'[6:-2]

import OpenGL 
OpenGL.ERROR_ON_COPY = True 

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time, sys
try:
	from numpy import *
except ImportError, err:
	try: 
		from Numeric import *
	except ImportError, err:
		print "This demo requires the numpy or Numeric extension, sorry"
		import sys
		sys.exit()

def drawCheckerBoard( N=5, white=GLfloat_3(1,1,1), black=GLfloat_3(0,0,0) ):
	"""Draw an 2N*2N checkerboard with given colours"""
	glDisable(GL_LIGHTING)
	try:
		for x in range(-N, N):
			for y in range(-N, N):
				if (x + y) % 2 == 0:
					glColor3fv(white)
				else:
					glColor3fv(black)	
				glRectf(x, y, x + 1, y + 1)
	finally:
		glEnable(GL_LIGHTING)
def drawSphere( center=(0,0,1), radius=1.0, sides=20 ):
	glPushMatrix()
	try:
		glTranslatef(*center)
		glutSolidSphere(radius, sides, sides)
	finally:
		glPopMatrix()

def display( swap=1, clear=1):
	"""Callback function for displaying the scene

	This defines a unit-square environment in which to draw,
	i.e. width is one drawing unit, as is height
	"""
	if clear:
		glClearColor(0.5, 0.5, 0.5, 0)
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

	# establish the projection matrix (perspective)
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	x,y,width,height = glGetDoublev(GL_VIEWPORT)
	gluPerspective(
		45, # field of view in degrees
		width/float(height or 1), # aspect ratio
		.25, # near clipping plane
		200, # far clipping plane
	)

	# and then the model view matrix
	glMatrixMode(GL_MODELVIEW)
	glLoadIdentity()
	gluLookAt(
		0,1,20, # eyepoint
		0,0,0, # center-of-view
		0,1,0, # up-vector
	)
	glLightfv( GL_LIGHT0, GL_DIFFUSE, GLfloat_3(.8,.8,.3) )
	glLightfv( GL_LIGHT0, GL_POSITION, GLfloat_4(1,1,3,0) )
	glEnable( GL_LIGHT0)
	
	rotation()
	drawCheckerBoard()
	drawSphere()
	if swap:
		glutSwapBuffers()

def idle( ):
	glutPostRedisplay()

starttime = time.time()

def rotation( period = 10):
	"""Do rotation of the scene at given rate"""
	angle = (((time.time()-starttime)%period)/period)* 360
	glRotate( angle, 0,1,0)
	return angle
def key_pressed(*args):
	# If escape is pressed, kill everything.
	if args[0] == '\033':
		sys.exit()

if __name__ == "__main__":
	print """You should see a sphere+checker-board rotating about the origin."""
	import sys
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutCreateWindow('Rotating Checkerboard')
	glutDisplayFunc(display)
	glutKeyboardFunc(key_pressed)
	glutIdleFunc(display)
	# note need to do this to properly render faceted geometry
	glEnable( GL_DEPTH_TEST )
	glutMainLoop()
