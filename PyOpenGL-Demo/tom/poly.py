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
try:
	from numpy import *
except ImportError, err:
	try: 
		from Numeric import *
	except ImportError, err:
		print "This demo requires the numpy or Numeric extension, sorry"
		import sys
		sys.exit()

n=50
a=arange(0,n)
vertices = transpose(
	reshape(
		array(
			(
				cos(2*pi*a/float(n)), 
				sin(3*2*pi*a/float(n))
			)
		),
		(2, n)
	)
)

colors=ones((n, 3))
colors[0]=[1,0,0]
colors[25]=[1,1,0]
colors.shape = (n, 3)


def redraw(o):
	global n
	glClearColor(0.5, 0.5, 0.5, 0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glOrtho(-1,1,-1,1,-1,1)
	glDisable(GL_LIGHTING)
	glDrawArrays(GL_LINE_LOOP, 0, n)
	glEnable(GL_LIGHTING)

def main():
	global n, colors, vertices
	o = Opengl(width = 400, height = 400, double = 1)
	o.redraw = redraw
	o.autospin_allowed = 1

	glVertexPointerd(vertices)
	glColorPointerd(colors)
	glEnableClientState(GL_VERTEX_ARRAY)
	glEnableClientState(GL_COLOR_ARRAY)

	o.pack(side = 'top', expand = 1, fill = 'both')
	o.mainloop()

main()
