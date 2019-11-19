#! /usr/bin/env python
from __future__ import absolute_import
from OpenGL.GL import *
from OpenGL.Tk import *

def redraw(o):
	glClearColor(0, 0, 1, 0)
	glClear(GL_COLOR_BUFFER_BIT)

def main():
    o = Opengl(width = 200, height = 200, double = 1)
    o.redraw = redraw
    o.pack(side = 'top', expand = 1, fill = 'both')
    o.mainloop()

if __name__ == "__main__":
    main()
