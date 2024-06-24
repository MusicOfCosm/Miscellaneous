# WebGL

The sole purpose of this project was to use OpenGL but on the Web (WebGL), meaning that people on other platforms (even a phone) could run it, including relatives that I want to make a gift for. To test if I could 

[Andrew Adamson's tutorials](https://www.youtube.com/playlist?list=PLPbmjY2NVO_X1U1JzLxLDdRn4NmtxyQQo) were an extremely great ressource to learn WebGL (or even the regular OpenGL). I followed them still, in case of differences between JavaScript and C/C++ important enough to cause problems.

I attempted to make Conway's Game of Life, but it didn't go well the first time due to my lack of knowledge in JavaScript and asynchronous programming. I gave up and did it in regular OpenGL. A little more than six months later, I came back to it and realized that I only needed to replace the `while` loop  a function that used `RequestAnimationFrame()` instead.
