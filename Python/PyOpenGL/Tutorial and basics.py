import pygame
from pygame.locals import * #So that you can type function_name() instead of saying pygame.locals.function_name() for certain functions
from OpenGL.GL import *  #OpenGL.GL is just your typical OpenGL functions
from OpenGL.GLU import * #OpenGL.GLU is some of the more "fancy" OpenGL functions

#vextex (sing)/vertices (plur) = sommets
vertices= (
    (-1, -1, -1), #vertex 0: left,  bottom, back
    (1, -1, -1),  #vertex 1: right, bottom, back
    (-1, 1, -1),  #vertex 2: left,  top,    back
    (1, 1, -1),   #vertex 3: right, top,    back
    (-1, -1, 1),  #vertex 4: left,  bottom, front
    (1, -1, 1),   #vertex 5: right, bottom, front
    (-1, 1, 1),   #vertex 6: left,  top,    front
    (1, 1, 1)     #vertex 7: right, top,    front
    )
#Each tuple define the xyz coordinate of a vertex: left or right, bottom or top, back or in front

edges = (
    (0, 1), #Connecting the three nearest vertices (same x, then y, then z) to the one on the back bottom left 
    (0, 2),
    (0, 4),
    (3, 1), #Same for the one on the back top right
    (3, 2),
    (3, 7),
    (5, 4), #And then the one on the front top left
    (5, 7),
    (5, 1),
    (6, 7), #And finally on the front bottom right
    (6, 4),
    (6, 2)
    )
#Each tuple defines from what vertices to draw a line between

surfaces = ( #The order matters. Remember the basics in school!
    (0, 1, 3, 2), #Back
    (4, 5, 7, 6), #Front
    (0, 2, 6, 4), #Left
    (1, 3, 7, 5), #Right
    (0, 1, 5, 4), #Bottom
    (2, 3, 7, 6)  #Top
    )

colors = ( #rgb values, but going from 0 to 1 insteaf of 0 to 255
    (1, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 0, 1) 
    )

ground_vertices = (
    (-50, -1, -50),
    (50, -1, -50),
    (-50, -1, 50),
    (50, -1, 50)
    )

glBegin(GL_LINES)


def Cube():
    #The quadrilaterals must be drawn first, otherwise they would erase the vertices
    glBegin(GL_QUADS) #Tells OpenGL that the following code will be used to draw surfaces (quadrilaterals)
    x = -1
    for surface in surfaces:
        x+=1
        for vertex in surface:
            glColor3fv(colors[x])
            glVertex3fv(vertices[vertex])
    glEnd()

    glBegin(GL_LINES) #Tells OpenGL that the following code will be used to draw lines
    for edge in edges:
        for vertex in edge: #vertex is a number 0 to 7
            glVertex3fv(vertices[vertex]) 
            #This function specifies a vertex. Here it's vertices[vertex], so a tuple containing vertices coordinates (xyz)
    glEnd()


def main():
    pygame.init()
    display = (960, 540)
    pygame.display.set_mode(display, OPENGL | DOUBLEBUF | RESIZABLE) #OPENGL creates an OpenGL-renderable display
    #The purpose of a buffer is to hold data right before it is used.
    #There are two buffers - one currently shown and one you draw on. The buffers cannot be swapped at any time because that would cause screen tearing.
    #Double buffering is using a separate block of memory to apply all the draw routines and then copying that block (buffer) to video memory as a single operation.

    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)
    #(fov in degrees, aspect ratio (width/height), znear (near cliping plane), zfar (far cliping plane))
    #A clipping plane is the distance at which the object appear/disappear relative to your perspective.

    glTranslatef(0.0, 0.0, -50)
    #Coordinates of the entire object, this gives the illusion that the perspective is a bit away from it

    x_move = 0
    y_move = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()


            if event.type == pygame.KEYDOWN: #If you press these keys, they will move the object
                #The values are flipped to give the illusion that the camera is moving
                if event.key == pygame.K_LEFT:
                    x_move = 0.1
                if event.key == pygame.K_RIGHT:
                    x_move = -0.1

                if event.key == pygame.K_UP:
                    y_move = -0.1
                if event.key == pygame.K_DOWN:
                    y_move = 0.1

            if event.type == pygame.KEYUP: #If you don't press these keys, the object stops
                #The values are flipped to give the illusion that the camera is moving
                if event.key == pygame.K_LEFT:
                    x_move = 0
                if event.key == pygame.K_RIGHT:
                    x_move = -0

                if event.key == pygame.K_UP:
                    y_move = -0
                if event.key == pygame.K_DOWN:
                    y_move = 0

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4: #mousewheel foward
                    glTranslatef(0, 0, 1.0)

                if event.button == 5: #mousewheel back
                    glTranslatef(0, 0, -1.0)

        #glRotatef(1, 1, 1, 1)
        #Produces a rotation of angle degrees around a 3d vector x y z. Therefore, the angle sets the speed, the rest set the direction.
        
        glTranslatef(x_move, y_move, 0.1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT) #Clears the two buffers off the display
        Cube()
        pygame.display.flip()
        pygame.time.wait(10) #Sets the speed in miliseconds, if no speed is specified, it will run as fast as it can


main()