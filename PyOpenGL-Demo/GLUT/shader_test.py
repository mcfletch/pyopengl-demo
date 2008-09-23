#! /usr/bin/env python
'''Tests rendering using the ARB shader objects extension...
'''
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from OpenGL.GL.ARB.shader_objects import *
from OpenGL.GL.ARB.vertex_shader import *
from OpenGL.GL.ARB.fragment_shader import *

import time, sys

program = None

def compileShader( source, shaderType ):
    """Compile shader source of given type"""
    shader = glCreateShaderObjectARB(shaderType)
    print "glShaderSourceARB:", bool(glShaderSourceARB)
    glShaderSourceARB( shader, source )
    glCompileShaderARB( shader )
    return shader


def compileProgram(vertexSource=None, fragmentSource=None):
    ##return
    program = glCreateProgramObjectARB()

    if vertexSource:
        vertexShader = compileShader(vertexSource, GL_VERTEX_SHADER_ARB)
        glAttachObjectARB(program, vertexShader)
    if fragmentSource:
        fragmentShader = compileShader(fragmentSource, GL_FRAGMENT_SHADER_ARB)
        glAttachObjectARB(program, fragmentShader)

    glValidateProgramARB( program )
    glLinkProgramARB(program)

    if vertexShader:
        glDeleteObjectARB(vertexShader)
    if fragmentShader:
        glDeleteObjectARB(fragmentShader)

    return program

# A general OpenGL initialization function.  Sets all of the initial parameters. 
def InitGL(Width, Height):                # We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)    # This Will Clear The Background Color To Black
    glClearDepth(1.0)                    # Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)                # The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)                # Enables Depth Testing
    glShadeModel(GL_SMOOTH)                # Enables Smooth Color Shading
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()                    # Reset The Projection Matrix
                                        # Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)
 
    if not glInitShaderObjectsARB():
        print 'Missing Shader Objects!'
        sys.exit(1)
    if not glInitVertexShaderARB():
        print 'Missing Vertex Shader!'
        sys.exit(1)
    if not glInitFragmentShaderARB():
        print 'Missing Fragment Shader!'
        sys.exit(1)
    
    global program
    program = compileProgram(
[
    '''
    varying vec3 normal;
    void main() {
        normal = gl_NormalMatrix * gl_Normal;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    ''',
], 
[
    '''
    varying vec3 normal;
    void main() {
        float intensity;
        vec4 color;
        vec3 n = normalize(normal);
        vec3 l = normalize(gl_LightSource[0].position).xyz;
    
        // quantize to 5 steps (0, .25, .5, .75 and 1)
        intensity = (floor(dot(l, n) * 4.0) + 1.0)/4.0;
        color = vec4(intensity*1.0, intensity*0.5, intensity*0.5,
            intensity*1.0);
    
        gl_FragColor = color;
    }
    ''',
]
)

# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:                        # Prevent A Divide By Zero If The Window Is Too Small 
        Height = 1

    glViewport(0, 0, Width, Height)        # Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# The main drawing function. 
def DrawGLScene():
    # Clear The Screen And The Depth Buffer
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()                    # Reset The View 

    # Move Left 1.5 units and into the screen 6.0 units.
    glTranslatef(-1.5, 0.0, -6.0)

    if program:
        glUseProgramObjectARB(program)
    glutSolidSphere(1.0,32,32)
    glTranslate( 1,0,2 )
    glutSolidCube( 1.0 )

    #  since this is double buffered, swap the buffers to display what just got drawn. 
    glutSwapBuffers()

# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)  
def keyPressed(*args):
    # If escape is pressed, kill everything.
    if args[0] == '\x1b':
        sys.exit()

def main():
    global window
    # For now we just pass glutInit one empty argument. I wasn't sure what should or could be passed in (tuple, list, ...)
    # Once I find out the right stuff based on reading the PyOpenGL source, I'll address this.
    glutInit(sys.argv)

    # Select type of Display mode:   
    #  Double buffer 
    #  RGBA color
    # Alpha components supported 
    # Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    
    # get a 640 x 480 window 
    glutInitWindowSize(640, 480)
    
    # the window starts at the upper left corner of the screen 
    glutInitWindowPosition(0, 0)
    
    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("Jeff Molofee's GL Code Tutorial ... NeHe '99")

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
    main()

