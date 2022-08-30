#! /usr/bin/env python
## This isn't really a PyOpenGL demo, but it's a nice
## example of how Numeric, Tkinter, and PIL can be used
## together to create all sorts of images.
## In this case, it's the Mandelbrot set.
## i used the Numerical python text example, but modified it to
## work with PIL

from __future__ import absolute_import
from __future__ import print_function
from six.moves import range
import sys
try:
	import numpy as np
except ImportError as err:
	print("This demo requires the numpy extension")
	import sys
	sys.exit()

import six.moves.tkinter
from PIL import Image
try:
	from PIL import ImageTk
except ImportError:
	print("This demo requires the ImageTk module, `python3-pil.imagetk` on debian systems")
	import sys
	sys.exit()

w = 256
h = 256

class Test:
	def draw(self,LowX, HighX, LowY, HighY, maxiter=30):
		xx=np.arange(LowX,HighX,(HighX-LowX)/w*2)
		yy=np.arange(HighY,LowY,(LowY-HighY)/h*2)*1j
		c=np.ravel(xx+yy[:,np.newaxis])
		z=np.zeros(c.shape,np.complex)
		output=np.resize(np.array(0,),c.shape)

		for iter in range(maxiter):
			print("iter",iter)
			z=z*z+c
			finished=np.greater(abs(z),2.0)
			c=np.where(finished,0+0j,c)
			z=np.where(finished,0+0j,z)
			output=np.where(finished,iter,output)

		## scale output a bit to make it brighter
##      output * output * 1000
		output = (output + (256*output) + (256**2)*output)*8
		self.mandel = output.tobytes()#"raw", "RGBX", 0, -1)
		print(len(self.mandel))

	def createImage(self):
		self.im = Image.new("RGB", (w//2,h//2))
		self.draw(-2.1, 0.7, -1.2, 1.2)
		print(len(self.im.tobytes("raw", "RGBX", 0, -1)))
		self.im.frombytes(self.mandel, "raw", "RGBX", 0, -1)

	def createLabel(self):
		self.image = ImageTk.PhotoImage(self.im)
		self.label = six.moves.tkinter.Label(self.root, image=self.image)
		self.label.pack()


	def __init__(self):
		self.root = six.moves.tkinter.Tk()
		self.i = 0
		self.createImage()
		self.createLabel()
		self.root.mainloop()

demo = Test

if __name__ == '__main__':
	demo()

