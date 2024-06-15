# PyOpenGL

This folder was originally just named OpenGL before being moved here.
It presents the little things that I've done in [OpenGL](https://opengl.org/) using Python. Honestly, if you really want to use OpenGL, it's better to do so in a compiled language like C, C++, or Rust, as you're usually making games or simulations which need to be fast on both the CPU and GPU.


## Tutorials and basics

This is from a [tutorial](https://pythonprogramming.net/opengl-rotating-cube-example-pyopengl-tutorial/) by sentdex. It uses Pygame to create a window that holds the context. I suppose this tutorial was good to introduce the basics of the basics of graphics programming, but as an OpenGL tutorial? It's utterly useless because it uses *legacy* OpenGL.

I made a copy of the file almost exactly a year later. I barely changed anything, so I didn't bother giving the file an actual name.


## Modern.py

Having learned enough OpenGL to be able to actually do stuff with it, I wanted to test out Python's ability to use modern versions of it. I just made a barebones script that renders a white triangle. I specified version 4.1, otherwise it wouldn't work on MacOS.