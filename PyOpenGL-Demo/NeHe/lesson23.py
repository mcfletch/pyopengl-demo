#! /usr/bin/env python
# -*- coding: utf8 -*-
"""Port of NeHe Lesson 16 by Ivan Izuver <izuver@users.sourceforge.net>"""
import string

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Image import *

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'

# Number of the glut window.
window = 0

# Rotations for cube. 
xrot=yrot=zrot=0.0
xspeed=yspeed=zspeed=0.0

texture = 0

object=0

def LoadTextures():
    #global texture
    image = open("mirrow2.bmp")
    
    ix = image.size[0]
    iy = image.size[1]
    image = image.tostring("raw", "RGBX", 0, -1)
    
    # Create Texture    
    glBindTexture(GL_TEXTURE_2D, glGenTextures(1))   # 2d texture (x and y size)
    
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    global quadratic
    LoadTextures()
    
    quadratic = gluNewQuadric()
    gluQuadricNormals(quadratic, GLU_SMOOTH)        # Create Smooth Normals (NEW) 
    gluQuadricTexture(quadratic, GL_TRUE)            # Create Texture Coords (NEW)
     
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading

##    glPolygonMode(GL_FRONT, GL_LINE)
##    glPolygonMode(GL_BACK, GL_LINE)
    
    glTexGeni(GL_S, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    glTexGeni(GL_T, GL_TEXTURE_GEN_MODE, GL_SPHERE_MAP)
    
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

def DrawCube():
   # Note there does not seem to be support for this call.
    #glBindTexture(GL_TEXTURE_2D,texture)    # Rotate The Pyramid On It's Y Axis

    glBegin(GL_QUADS)                # Start Drawing The Cube
    
    # Front Face (note that the texture's corners have to match the quad's corners)
    glNormal3f( 0.0, 0.0, 0.5)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad
    
    # Back Face
    glNormal3f( 0.0, 0.0, -0.5)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    # Bottom Left Of The Texture and Quad
    
    # Top Face
    glNormal3f( 0.0, 0.5, 0.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
    
    # Bottom Face
    glNormal3f( 0.0, -0.5, 0.0)       
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
    
    # Right face
    glNormal3f( 0.5, 0.0, 0.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)    # Top Left Of The Texture and Quad
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)    # Bottom Left Of The Texture and Quad
    
    # Left Face
    glNormal3f( -0.5, 0.0, 0.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)    # Bottom Left Of The Texture and Quad
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)    # Bottom Right Of The Texture and Quad
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)    # Top Right Of The Texture and Quad
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)    # Top Left Of The Texture and Quad
    
    glEnd();                # Done Drawing The Cube
    
# The main drawing function. 
def DrawGLScene():
    global xrot, yrot, zrot, texture,quadratic

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    # Clear The Screen And The Depth Buffer
    glLoadIdentity()                    # Reset The View
    glTranslatef(0.0,0.0,-5.0)            # Move Into The Screen
    
    glPushMatrix()
    
    glRotatef(xrot,1.0,0.0,0.0)            # Rotate The Cube On It's X Axis
    glRotatef(yrot,0.0,1.0,0.0)            # Rotate The Cube On It's Y Axis
    glRotatef(zrot,0.0,0.0,1.0)            # Rotate The Cube On It's Z Axis
    
    glEnable(GL_TEXTURE_GEN_S)
    glEnable(GL_TEXTURE_GEN_T)
    
    if object == 0:
        DrawCube()
    elif object == 1:
        glTranslatef(0.0,0.0,-1.5)            # Center The Cylinder 
        gluCylinder(quadratic,1.0,1.0,3.0,32,32)    # A Cylinder With A Radius Of 0.5 And A Height Of 2 
    elif object == 2:
        gluDisk(quadratic,0.5,1.5,32,32)
        # Draw A Disc (CD Shape) With An 
        # Inner Radius Of 0.5, And An 
        # Outer Radius Of 2.  Plus A Lot Of Segments  
    elif object == 3:
        gluSphere(quadratic,1.3,32,32) # Draw A Sphere With A Radius Of 1 And 16 Longitude And 16 Latitude Segments 
    elif object == 4:
        glTranslatef(0.0,0.0,-1.5)            # Center The Cone
        # A Cone With A Bottom Radius Of .5 And A Height Of 2 
        gluCylinder(quadratic,1.0,0.0,3.0,32,32)    
    elif object == 5:
        gluPartialDisk(quadratic,0.5,1.5,32,32,0,300)    # A Disk Like The One Before 
    elif object == 6:
        glutSolidTeapot(1.0)
    
    glPopMatrix()
    glDisable(GL_TEXTURE_GEN_S)
    glDisable(GL_TEXTURE_GEN_T)
    
    glPushMatrix()
    glTranslatef(0.0, 0.0, -24.0)
    
    glBegin(GL_QUADS)
    
    glNormal3f( 0.0, 0.0, 1.0)

    glTexCoord2f(0.0, 0.0)
    glVertex3f(-13.3, -10.0, 10.0)
    
    glTexCoord2f(1.0, 0.0)
    glVertex3f( 13.3, -10.0, 10.0)
    
    glTexCoord2f(1.0, 1.0)
    glVertex3f( 13.3, 10.0, 10.0)
    
    glTexCoord2f(0.0, 1.0)
    glVertex3f(-13.3, 10.0, 10.0)

    glEnd()
    glPopMatrix()

    xrot  = xrot + 0.6                # X rotation
    yrot = yrot + 0.6                 # Y rotation
    zrot = zrot + 0.6                 # Z rotation

    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(key,x,y):
    global object
    # If escape is pressed, kill everything.
    key = string.upper(key)
    if key == ESCAPE:
        sys.exit()
    elif key == 'L':
        light = not light
    elif key == 'T': #  switch the texture
        texture_num = (texture_num + 1) % 3
    elif key == 'O': #  switch the object
        object = (object + 1) % 7

def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    # get a 640 x 480 window 
    glutInitWindowSize(800, 600)
    
    # the window starts at the upper left corner of the screen 
    glutInitWindowPosition(100, 100)
    
    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Spheric by RISC")

       # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(DrawGLScene)
    
    # Uncomment this line to get full screen.
    # glutFullScreen()

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
        
