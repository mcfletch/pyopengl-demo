#!/usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception


import string
__version__ = string.split('$Revision: 1.1.1.1 $')[1]
__date__ = string.join(string.split('$Date: 2007/02/15 19:25:40 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'

import sys
try:
	from numpy import *
except ImportError, err:
	try: 
		from Numeric import *
	except ImportError, err:
		print "This demo requires the numpy or Numeric extension, sorry"
		import sys
		sys.exit()
from OpenGL.GL import *
from OpenGL.Tk import *

n, dt = 2000, 0.01
x, y, z = 0.01, 0.01, 0.01
frac = -1.0 * (8.0/3.0)
a = array((n,3), 'd')

def lorentz(o, x, y, z, n=2000, dt=0.01):
	"""Generate Lorentz attractor.  Put graphic in a graphical object"""
	o.grob = glGenLists(1);
	glNewList(o.grob, GL_COMPILE);
	try:
		glDisable(GL_LIGHTING)
		glBegin(GL_LINE_STRIP)
		try:
			glVertex3d(x, y, z)
			frac = -1.0 * (8.0/3.0)
			for i in range(0, n):
				xp = x + (-10.0 * x * dt + 10.0 * y * dt)
				yp = y + ( 28.0 * x * dt - y * dt - x * dt * z *dt)
				zp = z + ( frac * z * dt + x * dt * y * dt)
				x=xp
				y=yp
				z=zp
				glVertex3d(x, y, z)
		finally:
			glEnd()
		
		glEnable(GL_LIGHTING)
	finally:
		glEndList()

def redraw(o):
	"""The main scene redraw function."""
	
	# Clear the background and depth buffer.
	glClearColor(1., 0., 1., 0.)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glColor3f(1., 1., 1.)
	glCallList(o.grob)

#
# Demo starts here really.
if __name__ == "__main__":
	import Tkinter, sys
	
	# Create the opengl widget here.
	
	o = Opengl(None, width = 400, height = 400, double = 1)
	
	# Register the redraw procedure for the widget.
	
	o.redraw = redraw
	
	o.pack(side = 'top', expand = 1, fill = 'both')
	o.set_centerpoint(0., 0., 2000.)
	o.set_eyepoint(13000.)
	
	o.far = 600000.
	
	lorentz(o, 0.01, 0.01, 0.01)
	
	# Enter the tk mainloop.
	
	Tkinter.mainloop()
