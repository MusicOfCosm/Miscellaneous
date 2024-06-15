import ctypes
import glfw
from OpenGL.GL import *  #OpenGL.GL is just your typical OpenGL functions
from OpenGL.GLU import * #OpenGL.GLU is some of the more "fancy" OpenGL functions
import numpy as np
from OpenGL.GL.shaders import compileShader, compileProgram


def main():

    if not glfw.init():
        return -1

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 1)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL_TRUE)

    #Create a windowed mode window and its OpenGL context
    window = glfw.create_window(1280, 720, "Canvas", None, None)
    if not window:
        glfw.terminate()
        return -1

    #Make the window's context current
    glfw.make_context_current(window)

    info = [glGetString(GL_VENDOR), glGetString(GL_RENDERER), glGetString(GL_VERSION), glGetString(GL_SHADING_LANGUAGE_VERSION)]
    info = [string.decode("utf-8") for string in info]
    print("Vendor: %s" % info[0])
    print("Renderer: %s" % info[1])
    print("Version: %s" % info[2])
    print("Shading Language Version: %s\n\n" % info[3])


    triangle = (
        -0.75, -.75, 0.,
        0., .75, 0.,
        .75, -.75, 0.
    )

    triangle = np.array(triangle, dtype=np.float32)

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
    glEnableVertexAttribArray(0)

    with open("Py.vert", 'r') as f:
        vertCode = f.readlines()
        vertCode = ''.join(vertCode)
    # print(vertCode)
    with open("Py.frag", 'r') as f:
        fragCode = f.readlines()
        fragCode = ''.join(fragCode)

    shaderProgram = compileProgram(compileShader(vertCode, GL_VERTEX_SHADER), compileShader(fragCode, GL_FRAGMENT_SHADER))
    glUseProgram(shaderProgram)

    glfw.swap_interval(1)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    while not glfw.window_should_close(window) and glfw.get_key(window, glfw.KEY_ESCAPE) != glfw.PRESS:
        #Render here
        glClear(GL_COLOR_BUFFER_BIT)

        glDrawArrays(GL_TRIANGLES, 0, 3)

        #Swap front and back buffers
        glfw.swap_buffers(window)

        #Poll for and process events, can't interact or close the window without it
        glfw.poll_events()
    
    glDeleteVertexArrays(1, (VAO,))
    glDeleteBuffers(1, (VBO,))
    glfw.terminate()

if __name__ == '__main__':
    main()
