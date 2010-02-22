#! /usr/bin/env python
# -*- coding: utf8 -*-
"""Port of NeHe Lesson 19 by Ivan Izuver <izuver@users.sourceforge.net>

port NeHe tutorials from C\C++ to Python  
"""
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Image import *
import sys,random

ESCAPE = '\033'

# global particles settings
MAX_PARTICLES=1000 # Number of particles create.
SPEED_PARTICLES=2.0 # particles speed
XSPEED=0.0 # speed OX
YSPEED=0.0 # speed OY
ZOOM=-30.0# zoom
LOOP=0 # loop particles
DELAY=0 # delay

# particle struct
class particle:
    def __init__(self):
        
        self.ACTIVE=1 # dead or live
        self.LIFE=0.0 # len of life
        self.FADE=0.0 # step of fade
    
        self.R=0.0 # red
        self.G=0.0 # green
        self.B=0.0 # blue
        
        self.X=0.0 # X position
        self.Y=0.0 # Y position
        self.Z=0.0 # Z position
        
        self.Xi=0.0 # X direction
        self.Yi=0.0 # Y direction
        self.Zi=0.0 # Z direction
        
        self.Xj=0.0 # X gravity
        self.Yj=0.0 # Y gravity
        self.Zj=0.0 # Z gravity

#        self.particle=[i for i in xrange(MAX_PARTICLES)]
        
prts=[]

for i in xrange(MAX_PARTICLES):
    particl=particle() 
    prts.append(particl)
    
colors= [[(1.0,0.5,0.5),(1.0,0.75,0.5),(1.0,1.0,0.5),(0.75,1.0,0.5)],
         [(0.5,1.0,0.5),(0.5,1.0,0.75),(0.5,1.0,1.0),(0.5,0.75,1.0)],
         [(0.5,0.5,1.0),(0.75,0.5,1.0),(1.0,0.5,1.0),(1.0,0.5,0.75)]]

window = 0 # Number of the glut window.

def LoadTextures():
    #global texture
    image = open("myfire.jpg")
    
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
    LoadTextures()
    global LOOP
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glDisable(GL_DEPTH_TEST)                # Enables Depth Testing
    glEnable(GL_BLEND)         
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    
    glBlendFunc(GL_SRC_ALPHA,GL_ONE)          
    glHint(GL_PERSPECTIVE_CORRECTION_HINT,GL_NICEST);
    glHint(GL_POINT_SMOOTH_HINT,GL_NICEST);   
    glEnable(GL_TEXTURE_2D);                  
    
    for i in xrange(MAX_PARTICLES):
        prts[i]
        
        prts[i].LIFE=1.0
        prts[i].FADE=float(random.randrange(0,100))/1000.0+0.003
        
        prts[i].R=colors[i*(12/1000)][0]
        prts[i].G=colors[i*(12/1000)][1]
        prts[i].B=colors[i*(12/1000)][2]
        
        prts[i].Xi=(float(random.randrange(0,100)%50)-26.0)*10.0
        prts[i].Yi=(float(random.randrange(0,100)%50)-25.0)*10.0
        prts[i].Zi=(float(random.randrange(0,100)%50)-25.0)*10.0
        
        prts[i].Xj=0.0
        prts[i].Yj=-0.8
        prts[i].Zj=0.0
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 200.0)

    glMatrixMode(GL_MODELVIEW)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 200.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
    
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                         # Reset The View
    
    for i in xrange(MAX_PARTICLES):
        if prts[i].ACTIVE==1:
            x=float(prts[i].X)
            y=float(prts[i].Y)
            z=float(prts[i].Z+ZOOM)
            
            glColor4f(prts[i].R==i,prts[i].G==i,prts[i].B==i,prts[i].LIFE)
            
            glBegin(GL_TRIANGLE_STRIP)
            glTexCoord2d(1,1); glVertex3f(x+0.5,y+0.5,z); # upper right
            glTexCoord2d(0,1); glVertex3f(x-0.5,y+0.5,z); # upper left
            glTexCoord2d(1,0); glVertex3f(x+0.5,y-0.5,z); # bottom right 
            glTexCoord2d(0,0); glVertex3f(x-0.5,y-0.5,z); # bottom left
            glEnd()

            prts[i].X+=prts[i].Xi/(SPEED_PARTICLES*1000)
            prts[i].Y+=prts[i].Yi/(SPEED_PARTICLES*1000)
            prts[i].Z+=prts[i].Zi/(SPEED_PARTICLES*1000)
            
            prts[i].Xi+=prts[i].Xj
            prts[i].Yi+=prts[i].Yj
            prts[i].Zi+=prts[i].Zj
            
            prts[i].LIFE-=prts[i].FADE
            if prts[i].LIFE<0.0:
                prts[i].LIFE=1.0
                prts[i].FADE=float(random.randrange(0,100)%100)/1000.0+0.003
                
                prts[i].X=0.0
                prts[i].Y=0.0
                prts[i].Z=0.0
                
                prts[i].Xi=XSPEED+float((random.randrange(0,100)%60)-32.0)
                prts[i].Yi=XSPEED+float((random.randrange(0,100)%60)-30.0)
                prts[i].Zi=float((random.randrange(0,100)%60)-32.0)
                
        else:
            prts[i].ACTIVE=1
            prts[i].FADE=float(random.randrange(0,100))/1000.0+0.003;
            
            prts[i].X=0.0
            prts[i].Y=0.0
            prts[i].Z=0.0
            
    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(key, x, y):
    global window,ZOOM
    # If escape is pressed, kill everything.
    key = string.upper(key)
    prt=particle()
    
    if key == ESCAPE:
        sys.exit()
    elif key == 'W':
        for i in xrange(MAX_PARTICLES):
            if prts[i].Yj<1.5:
                prts[i].Yj+=0.1
    elif key == 'S':
        for i in xrange(MAX_PARTICLES):
            if prts[i].Yj>-1.5:
                prts[i].Yj-=0.1
    elif key == 'A':
        for i in xrange(MAX_PARTICLES):
            if prts[i].Xj>-1.5:
                prts[i].Xj-=0.1
    elif key == 'D':
        for i in xrange(MAX_PARTICLES):
            if prts[i].Xj<1.5:
                prts[i].Xj+=0.1
    elif key == 'F':
        for i in xrange(MAX_PARTICLES):    
            prts[i].X=0.0
            prts[i].Y=0.0
            prts[i].Z=0.0
            
            prts[i].Xi=float((random.randrange(0,100)%50)-26.0)*10.0
            prts[i].Yi=float((random.randrange(0,100)%50)-25.0)*10.0
            prts[i].Yi=float((random.randrange(0,100)%50)-25.0)*10.0
    elif key == 'Z':
        ZOOM+=1.0
    elif key == 'X':
        ZOOM-=1.0   
     
def main():
    global window
    # pass arguments to init
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
    window = glutCreateWindow("Particles by RISC")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.    
    glutDisplayFunc(DrawGLScene)
    
    # Uncomment this line to get full screen.
    #glutFullScreen()

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
    print 'other commands: WASD (direction) ZX (zoom)'
    main()
