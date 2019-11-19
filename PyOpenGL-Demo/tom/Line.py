#! /usr/bin/env python
from __future__ import absolute_import
from OpenGL.GL import *
from OpenGL.Tk import *

def redraw(o):
	glClearColor(0.5, 0.5, 0.5, 0)
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glOrtho(0,1,0,1,0,1)
	glDisable(GL_LIGHTING)
	glBegin(GL_LINES)
	glColor3f(1,1,0)
	glVertex2f(0,0)
	glColor3f(1,0,1)
	glVertex2f(1,1)
	glColor3f(1,0,0)
	glVertex2f(1,0)
	glColor3f(0,0,1)
	glVertex2f(0,1)
	glEnd()
	glEnable(GL_LIGHTING)

o = Opengl(width = 400, height = 400, double = 1)
o.redraw = redraw
o.pack(side = 'top', expand = 1, fill = 'both')
o.mainloop()
