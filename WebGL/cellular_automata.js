"use strict";

// Having everything in one file is annoying, but that's the way to go when not using a server

var vertex = `#version 300 es

layout(location = 0) in vec2 aPosition;
layout(location = 1) in vec2 aTexCoords;

out vec2 TexCoords;

void main()
{
    TexCoords = aTexCoords;
    gl_Position = vec4(aPosition, 0.0, 1.0);
}
`;

var fragment = `#version 300 es

precision highp float;

out vec4 outColor;

in vec2 TexCoords;

uniform sampler2D screenTexture;

uniform float  rand;
uniform float WIDTH;
uniform float HEIGHT;

float random(vec2 st) {
    return fract(sin(dot(st.xy, vec2(12.9898,78.233))*rand) * 43758.5453123);
}


uniform bool first;

float rule(vec2[9] offsets) {
    int neighbor = 0;
    bool alive = false;
    for (int i = 0; i < 9; i++)
    {
        if (i == 4 && vec3(texture(screenTexture, TexCoords.st + offsets[i])).x == 1.0)
            alive = true;
       
        else if (vec3(texture(screenTexture, TexCoords.st + offsets[i])).x == 1.0)
            neighbor += 1;
    }

    // Any live cell with two or three live neighbours survives.
    // Any dead cell with three live neighbours becomes a live cell.
    // All other live cells die in the next generation. Similarly, all other dead cells stay dead.
    if (alive && neighbor == 2 || alive && neighbor == 3) {
        return 1.0;
    }
    else if (!alive && neighbor == 3) {
        return 1.0;
    }
    else 
        return 0.0;
}

void main()
{
    float xoffset = 1.0 / WIDTH;
    float yoffset = 1.0 / HEIGHT;

    vec2 offsets[9] = vec2[](
        vec2(-xoffset,  yoffset), // top-left
        vec2( 0.0f,    yoffset), // top-center
        vec2( xoffset,  yoffset), // top-right
        vec2(-xoffset,  0.0f),   // center-left
        vec2( 0.0f,    0.0f),   // center-center
        vec2( xoffset,  0.0f),   // center-right
        vec2(-xoffset, -yoffset), // bottom-left
        vec2( 0.0f,   -yoffset), // bottom-center
        vec2( xoffset, -yoffset)  // bottom-right    
    );

    float bw = random(TexCoords.st);
    if (first) {
        if (bw >= 0.5)
            outColor = vec4(1.0);
        else
            outColor = vec4(vec3(0.0), 1.0);
    }
    else {
        outColor = vec4(vec3(rule(offsets)), 1.0);
    }
}
`;

const canvas = document.querySelector("#canvas");
const gl = canvas.getContext("webgl2");

function compileShaders(program, vertex, fragment) {
    const vertexShader = gl.createShader(gl.VERTEX_SHADER);
    gl.shaderSource(vertexShader, vertex);
    gl.compileShader(vertexShader);
    gl.attachShader(program, vertexShader);

    const fragmentShader = gl.createShader(gl.FRAGMENT_SHADER);
    gl.shaderSource(fragmentShader, fragment);
    gl.compileShader(fragmentShader);
    gl.attachShader(program, fragmentShader);

    gl.linkProgram(program);
    if (!gl.getProgramParameter(program, gl.LINK_STATUS)) {
        console.log(gl.getShaderInfoLog(vertexShader));
        console.log(gl.getShaderInfoLog(fragmentShader));
    }

    gl.deleteShader(vertexShader);
    gl.deleteShader(fragmentShader);

    gl.useProgram(program);
}

function SET1I(program, varName, value) { gl.uniform1i(gl.getUniformLocation(program, varName), value); }
function SET1F(program, varName, value) { gl.uniform1f(gl.getUniformLocation(program, varName), value); }

var WIDTH = canvas.width;
var HEIGHT = canvas.height;

console.log("GPU Information:\n");
console.log("Vendor: %s\n", gl.getParameter(gl.VENDOR));
console.log("Renderer: %s\n", gl.getParameter(gl.RENDERER));
console.log("Version: %s\n", gl.getParameter(gl.VERSION));
console.log("Shading Language Version: %s\n\n\n", gl.getParameter(gl.SHADING_LANGUAGE_VERSION));

// Only continue if WebGL is available and working
if (gl === null) {
    alert(`Unable to initialize WebGL2.\nYour browser or machine may not support it.`);
}

const vertices = new Float32Array([
    -1, -1,  0, 0,
     1,  1,  1, 1,
    -1,  1,  0, 1,
    
    -1, -1,  0, 0,
     1,  1,  1, 1,
     1, -1,  1, 0
]);

const VBO = gl.createBuffer();
gl.bindBuffer(gl.ARRAY_BUFFER, VBO);
gl.bufferData(gl.ARRAY_BUFFER, vertices, gl.STATIC_DRAW);

gl.enableVertexAttribArray(0);
gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 4*4, 0);
gl.enableVertexAttribArray(1);
gl.vertexAttribPointer(1, 2, gl.FLOAT, false, 4*4, 2*4);


const program = gl.createProgram();
compileShaders(program, vertex, fragment);


const FBO = gl.createFramebuffer();
gl.bindFramebuffer(gl.FRAMEBUFFER, FBO);

//creating a color attachement texture
const fbo_tex = gl.createTexture();
gl.bindTexture(gl.TEXTURE_2D, fbo_tex);
gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, WIDTH, HEIGHT, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.NEAREST); //if render target is the size of the texture, can use gl.NEAREST
gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.NEAREST);
gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, fbo_tex, 0);

if (gl.checkFramebufferStatus(gl.FRAMEBUFFER) != gl.FRAMEBUFFER_COMPLETE)
    console.log("Framebuffer Error - Status: 0x%x\n", gl.checkFramebufferStatus(gl.FRAMEBUFFER));


SET1F(program, "rand", Math.random());

var deltaTime = 0.0;
var lastFrame = 0.0;
function mainloop(time) {
    time *= 0.001; //from miliseconds to seconds
    if (lastFrame == 0.0)
        SET1I(program, "first", 1);
    else
        SET1I(program, "first", 0);
    deltaTime = time - lastFrame;
	lastFrame = time;

    gl.canvas.width = window.innerWidth;
    gl.canvas.height = window.innerHeight;
    
    SET1F(program, "WIDTH", WIDTH);
    SET1F(program, "HEIGHT", HEIGHT);

    gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, null);

    gl.drawArrays(gl.TRIANGLES, 0, 6);

    gl.bindFramebuffer(gl.READ_FRAMEBUFFER, null);
    gl.bindFramebuffer(gl.DRAW_FRAMEBUFFER, FBO);
    gl.blitFramebuffer(0, 0, WIDTH, HEIGHT, 0, 0, WIDTH, HEIGHT, gl.COLOR_BUFFER_BIT, gl.LINEAR);

    requestAnimationFrame(mainloop);
}

requestAnimationFrame(mainloop);
