#! /usr/bin/env python
from __future__ import absolute_import
from __future__ import print_function
from OpenGL.GL import *
from OpenGL.Tk import *
from OpenGL.GLUT import *
from six.moves.tkinter import *
import sys

class MyApp(Frame):

	def init(self):
		glutInit([])
		glMaterialfv(GL_FRONT, GL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
		glMaterialfv(GL_FRONT, GL_DIFFUSE, [0.8, 0.8, 0.8, 1.0])
		glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 0.0, 1.0, 1.0])
		glMaterialfv(GL_FRONT, GL_SHININESS, 50.0)
		glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 1.0, 0.0, 1.0])
		glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
		glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
		glLightfv(GL_LIGHT0, GL_POSITION, [1.0, 1.0, 1.0, 0.0]);
		glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.2, 0.2, 0.2, 1.0])
		glEnable(GL_LIGHTING)
		glEnable(GL_LIGHT0)


	def redraw(self, o):
		glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
		glPushMatrix()
		glTranslatef(0, -1, 0)
		glRotatef(250, 1, 0, 0)
		glutSolidCone(1, 2, 50, 10)
		glPopMatrix()

	def save( self, filename='test.jpg', format="JPEG" ):
		from PIL import Image # get PIL's functionality...
		width, height = 400,400
		glPixelStorei(GL_PACK_ALIGNMENT, 1)
		data = glReadPixelsub(0, 0, width, height, GL_RGB)
		if hasattr(data,'shape'):
			assert data.shape == (width,height,3), """Got back array of shape %r, expected %r"""%(
				data.shape,
				(width,height,3),
			)
			image = Image.frombytes( "RGB", (width, height), data.tostring() )
		else:
			image = Image.frombytes("RGB",(width,height), data)
		image = image.transpose( Image.FLIP_TOP_BOTTOM)
		image.save( filename, format )
		print('Saved image to %s'% (os.path.abspath( filename)))
		return image

	def __init__(self):
		self.f = Frame()
		self.f.pack()

		self.gl = Opengl(width = 400, height = 400, double = 1, depth = 1)
		self.gl.redraw = self.redraw
		self.gl.autospin_allowed = 1
		self.gl.pack(side = TOP, expand = YES, fill = BOTH)
		self.gl.set_background(255,255,255)
		self.init()

		self.b = Button(self.f, text="Save", command=self.save)
		self.b.pack(side='top')
		self.quit = Button(self.f, text = 'Quit', command = sys.exit)
		self.quit.pack(side = 'top')
		self.gl.mainloop()

app = MyApp()
