"""GLUT replacement for the original checker.py demonstration code

Note:
	Has no navigation code ATM.
"""

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception

__version__='$Revision: 1.2 $'[11:-2]
__date__ = '$Date: 2008/09/05 20:20:57 $'[6:-2]
import OpenGL 
OpenGL.ERROR_ON_COPY = True 

import cone

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import time, sys, os

def click( button, state, x, y ):
	"""Handler for click on the screen"""
	if state == GLUT_UP:
		saveBuffer( )

def saveBuffer( filename="test.jpg", format="JPEG" ):
	"""Save current buffer to filename in format"""
	import Image # get PIL's functionality...
	x,y,width,height = glGetDoublev(GL_VIEWPORT)
	width,height = int(width),int(height)
	glPixelStorei(GL_PACK_ALIGNMENT, 1)
	data = glReadPixels(x, y, width, height, GL_RGB, GL_UNSIGNED_BYTE)
	image = Image.fromstring( "RGB", (width, height), data )
	image = image.transpose( Image.FLIP_TOP_BOTTOM)
	image.save( filename, format )
	print 'Saved image to %s'% (os.path.abspath( filename))
	return image
def key_pressed(*args):
	# If escape is pressed, kill everything.
	if args[0] == '\033':
		sys.exit()

def main():
	print """You should see a cone rotating slowly, click to save to test.jpg"""
	import sys
	glutInit(sys.argv)
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	glutCreateWindow('Image Saving Demo')
	glutDisplayFunc(cone.display)
	glutIdleFunc(cone.display)
	glutKeyboardFunc(key_pressed)
	glutMouseFunc( click )
	# note need to do this to properly render faceted geometry
	glutMainLoop()

if __name__ == "__main__":
    main()
