#!/usr/bin/python

# This is statement is required by the build system to query build info
if __name__ == '__build__':
	raise Exception


import string
__version__ = string.split('$Revision: 1.1.1.1 $')[1]
__date__ = string.join(string.split('$Date: 2007/02/15 19:25:40 $')[1:3], ' ')
__author__ = 'Tarn Weisner Burton <twburton@users.sourceforge.net>'

from OpenGL.GL import *
from OpenGL.Tk import *

from logo import define_logo

def redraw(o):
	if o.grob == -1:
		o.grob = glGenLists(1);
		glNewList(o.grob, GL_COMPILE_AND_EXECUTE);
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [1., 1., 0., 0.])
		define_logo()
		glEndList()

		o.autospin = 1

		o.xspin = 1
		o.yspin = 2

		o.update()

		o.after(10, o.do_AutoSpin)

	else:

		glCallList(o.grob)

#
# Demo starts here really.
if __name__ == "__main__":
	import Tkinter, sys
	
	o = Opengl(None, width = 400, height = 200, double = 1, depth = 1)
	o.pack(expand = 1, fill = 'both')
	
	o.redraw = redraw
	o.set_centerpoint(30., 2., 0.)
	o.set_eyepoint(80.)
	
	o.grob = -1
	
	o.autospin_allowed = 1
	
	# Enter the tk mainloop.
	
	Tkinter.mainloop()
	
