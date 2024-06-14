'''This is too slow'''

#!/usr/bin/env python
import time    #for error handling information
start_time = time.time()
import pygame
import random      #for movement
import numpy as np #for interaction between objects
import logging #for logging and error handling
import sys     #for error handling information
from math import cos, sin, pi


#https://www.youtube.com/watch?v=AY9MnQ4x3zk
import sys
import pygame
pygame.init()

NUMBER = 1000#((HEIGHT*WIDTH)//100)*random.randint(5, 10)
SPEED = 2#random.uniform(1, 3)
SENSOR_RANGE = 11#random.randint(6, 12)
SENSOR_SIZE = 2
BOUNDARY = False#random.choice((True, False))
START = 'random'#random.choice(('centre', 'random'))
# print(f'Dimensions {HEIGHT}x{WIDTH}\nNumber: {NUMBER}\nSpeed: {SPEED}\nSensor range: {SENSOR_RANGE}\nSensor size: {SENSOR_SIZE}\nBoundaries: {BOUNDARY}')

color = []
color_bool = True
if color_bool is True:
    for _ in range(3):
        i = random.randint(round(255/3), 255)
        color.append(i)
    color = tuple(color)
else: color = (255, 255, 255)

del color_bool
# surface.set_at((x, y), color)

WIDTH = 1280
HEIGHT = 660
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE) #Opens a PyGame window with (Width, Height) under the variable "screen". (1280, 648) is the max for my computer.
pygame.display.set_caption('Canvas') #Names the PyGale window
clock = pygame.time.Clock()

# test_surface = pygame.Surface((1, 2)) #Creates a surface under the variable "test_surface" with a width of 100px and a height of 200px
# test_surface.fill('Red') #Colors "test_surface" red

# image_surface = pygame.image.load(r"C:\Users\macky\OneDrive\Pictures\Cadeau_Bee (Terminé).png").convert_alpha() #.convert() for easier pygame use, .convert_alpha to remove alpha values

# test_font = pygame.font.SysFont('Verdana', 30) #Font and size, .Font(None, size) uses the default pygame font, for anything else, import sys and use .SysFont
# text_surface = test_font.render('A string of words', True, 'Black') #Words, make the edges blocky or smooth, and color (can be rgb, so (0, 0, 0) instead of 'Black')

# animated_surface = pygame.Surface((100, 40))
# animated_surface.fill('Blue')
# animated_x_pos = 300

screen.fill('Black') #If the dispaly isn't colored here, animated_surface will be stretched

print(screen.get_at((50, 50)))

def sense(self, sensorAngleOffset):
    sensorAngle = self.orientation + sensorAngleOffset
    sensorDir = (cos(sensorAngle), sin(sensorAngle))
    sensorCentre = (self.x + sensorDir[0] * SENSOR_RANGE, self.y + sensorDir[1] * SENSOR_RANGE)
    somme = 0
    offsetX = -SENSOR_SIZE
    offsetY = -SENSOR_SIZE

    for offsetX in range(-SENSOR_SIZE, SENSOR_SIZE+1):
        for offsetY in range(-SENSOR_SIZE, SENSOR_SIZE+1):
            posX = sensorCentre[0] + offsetX
            posY = sensorCentre[1] + offsetY
            posX, posY = boundary(posX, posY, self.WIDTH, self.HEIGHT)

            color_vals = (screen.get_at((round(posX), round(posY)))[0],
                          screen.get_at((round(posX), round(posY)))[1],
                          screen.get_at((round(posX), round(posY)))[2])
            color_vals = (color_vals[0] + color_vals[1] + color_vals[2])/3
            
            if BOUNDARY is True:
                if posX >= 0 and posX < self.WIDTH and posY >= 0 and posY < self.HEIGHT:
                    somme += color_vals
            else: somme += color_vals

    return somme


def boundary(x, y, W, H):
    if BOUNDARY == True:
        if x >= W:
            x = W
        if x < 0:
            x = 0

        if y >= H:
            y = H
        if y < 0:
            y = 0
    

    else:
        if x > W:
            x -= W
        if x < 0:
            x += W

        if y > H:
            y -= H
        if y < 0:
            y += H

    return x, y


class Agents:
    def __init__(self, sensor_angle=pi/8, rotation_angle=pi/4): #30° = π/6,  45° = π/4, 60° = π/3, 90° = π/2
        '''Initializes a random orientation, as well as color'''
        
        self.WIDTH = WIDTH-1
        self.HEIGHT = HEIGHT-1

        if START == 'random':
            self.x = random.randint(0, self.WIDTH)
            self.y = random.randint(0, self.HEIGHT)
        elif START == 'centre':
            self.x = float(self.WIDTH//2)
            self.y = float(self.HEIGHT//2)

        self.orientation = random.random() * 2*pi #random.choice(angle)
        self.SA = sensor_angle
        self.RA = rotation_angle

    def movement(self):
        '''Orientation, interaction with or without other agents, and movement.'''
        
        screen.set_at((round(self.x), round(self.y)), color)

        forward = sense(self, 0.0)
        left = sense(self, self.SA)
        right = sense(self, -self.SA)

        if forward > left and forward > right:
            pass
        
        elif forward < left and forward < right:
            # print('random')
            self.orientation += random.choice((-self.RA, self.RA))
        
        elif left > right:
            # print('left')
            self.orientation += self.RA
            
        elif left < right:
            # print('right')
            self.orientation += -self.RA

        #Normal distribution with the mean=going straight and the standard deviation being how likely it is to turn
        # self.orientation = random.normalvariate(self.orientation, pi/40) #Bell curve

        # self.orientation += random.choice((pi/8, 0, 0, 0, -pi/8))
        # self.x += cos(self.orientation)*SPEED
        # self.y += sin(self.orientation)*SPEED
        # if random.randint(0,100) < 2:
        #     self.orientation += random.choice((self.SA, -self.SA))
        self.x += cos(self.orientation)*SPEED
        self.y += sin(self.orientation)*SPEED
        # self.orientation = tanh(dy - self.y /dx - self.x)

        if BOUNDARY == True:
            if self.x >= self.WIDTH or self.x < 0 or self.y >= self.HEIGHT or self.y < 0:
                self.orientation = random.random() * 2*pi
        self.x, self. y = boundary(self.x, self.y, self.WIDTH, self.HEIGHT)

agents = [Agents() for _ in range(NUMBER)]

while True:
    for event in pygame.event.get():  #For anything that you do with the display window
        if event.type == pygame.QUIT: #If you click on the close button (X on the top right)
            pygame.quit()             #The display window closes
            quit()                    #The program ends


    # screen.blit(test_surface, (200, 100)) #(blit = block image transfer) It displays variable_surface at the coordinates on the display.
    # screen.blit(image_surface, (300, 0))
    # screen.blit(text_surface, (400, 500))
    # screen.blit(animated_surface, (animated_x_pos, 600))
    # animated_x_pos += 1
    # if animated_x_pos > 1280:
    #     animated_x_pos = -100
    for agent in agents:
        agent.movement()

    pygame.display.update()
    clock.tick(60) #This caps the fps to the designated number, which allows us to manipulate the speed of the program



# from multiprocessing import Pool

# from sys import platform
# if platform.startswith('win'): #if the program is being run on windows, the tkinter blurriness is removed
#     from ctypes import windll
#     windll.shcore.SetProcessDpiAwareness(1)
# import tkinter
# root = tkinter.Tk()
# HEIGHT = root.winfo_screenwidth()//6 #NumPy always reads first the vertical values from the
# WIDTH = root.winfo_screenheight()//6 #y axis, and then, the horizontal values from the x axis.
# root.destroy()


#The zeros() function makes a matrix containing only zeros given the matrix’s number of rows and columns. (All bgr values are 0)
# canvas = np.zeros((WIDTH, HEIGHT, channels), dtype='uint8') #3 can be put after width and height to have a colored channel, uint8 is a common image type


# i = 0
# total = 0
# if __name__ == '__main__':
#     while True:
#         start = time.perf_counter()

#         cv.imshow(window, canvas)

#         if lines == False:
#             if color_bool == True:
#                 gray = cv.cvtColor(canvas, cv.COLOR_BGR2GRAY)

#             #The [:,:] stands for everything. Each : stands for the respective dimensions of the array
#             # canvas[:,:] = canvas *.9999
#             value = 1
#             mat = np.ones(canvas.shape, dtype = 'uint8')*value
#             canvas = cv.subtract(canvas,mat)

#             canvas = cv.GaussianBlur(canvas, (3,3), 0)

#         if color_bool == False:
#             gray = canvas

        
#         # for agent in agents1:
#         #     if lines:
#         #         agent.lines_movement(orient_x, orient_y)

#         #     else:
#         #         agent.movement()

#         # for process in processess: process.start()
#         # for process in processess: process.join()
#         # for process in processess: process.terminate()
#         # move(agents1)
#         # p = Pool(processes=2)
#         # for agent in agents1:
#         #     p.map(move, agents)
#         # p.close()
#         move([agent for agent in agents])

#         i += 1
#         # print(i)
#         # time.sleep(0.001)
#         # print([pixel for pixel in canvas])
#         finish = time.perf_counter()
#         total += finish - start
#         if i == 1000: break
#         if cv.waitKey(1) & 0xFF == 27:#ord('q'): #If the key pressed is Q
#             break                 #27 is the Escape key
#     cv.destroyAllWindows() #Destroys all created cv windows
#     print(f'Average: {total/i} seconds per frame, or {1/(total/i)} fps')
#     #Sensor range: 11
#     #Sensor size: 1