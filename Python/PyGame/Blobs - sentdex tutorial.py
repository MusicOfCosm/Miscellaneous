import time    #for error handling information
start_time = time.time()
import pygame
import random      #for movement
import numpy as np #for interaction between objects
import logging #for logging and error handling
import sys     #for error handling information

logging.basicConfig(level=logging.INFO) #Only displays INFO level logging and above (so everything but DEBUG) on the console
'''
About logging: It only outputs something if the code read passes trough it.
DEBUG     Detailed information, typically of interest only when diagnosing problems.
INFO      Confirmation that things are working as expected.
WARNING   An indication that something unexpected happened, or indicative of some problem in the near future (e.g. ‘disk space low’).
          The software is still working as expected.
ERROR     Due to a more serious problem, the software has not been able to perform some function.
CRITICAL  A serious error, indicating that the program itself may be unable to continue running.
'''

def error_handling():                          #exc_info: execption (as in error) information is a tuple containning:
    return 'Error: {}. {}, line: {}'.format(sys.exc_info()[0],           #Error type
                                            sys.exc_info()[1],           #Actual error
                                            sys.exc_info()[2].tb_lineno) #Traceback object (tb_lineno gives us the line number of the traceback)

class Blob: #parent class
    #Python's objects have a bunch of "special methods" often called magic methods, which are between two double underscores (dunders).
    def __init__(self, color, x_boundary=800, y_boundary=600, size_range=(4, 8), movement_range=(-2, 3)): 
        '''The __init__ method (pronounced "dunder init method") is used to specify anything that we want to happen when the Blob object/instance is initialized.
        The "self" argument can actually be called anything you want, but "self" is the convention. It is the instance object (in this case, it's Blob).
        We use "self." to create and access an object's attributes from within the class, as well as outside the class'''
        
        self.x_boundary = x_boundary
        self.y_boundary = y_boundary
        self.x = random.randrange(0, self.x_boundary)  #randrange is from the "random" module
        self.y = random.randrange(0, self.y_boundary) #self.x and self.y will allow us to spawn self in a random location
        self.size = random.randrange(size_range[0], size_range[1]) #The size (radius) of self (the blob) is chosen randomly between 4, 5, 6, and 7 pixels
        self.color = color #This will give self the color we choose once the variable is made
        self.movement_range = movement_range

    def move(self):
        #This block makes the object randomly move in x and y independently from each other, then updates its position
        self.move_x = random.randrange(self.movement_range[0], self.movement_range[1]) 
        self.move_y = random.randrange(self.movement_range[0], self.movement_range[1])
        self.x += self.move_x
        self.y += self.move_y

    def check_bounds(self):
        #These two blocks makes it impossible for the object to go out of the display bounds
        if self.x < 0: self.x = 0
        elif self.x > self.x_boundary: self.x = self.x_boundary
        
        if self.y < 0: self.y = 0
        elif self.y > self.y_boundary: self.y = self.y_boundary

RED_BLOBS_NUMBERS = 5
GREEN_BLOBS_NUMBERS = 20
BLUE_BLOBS_NUMBERS = 3

#We'll use these variables in the classes objects
WIDTH = 800
HEIGHT = 600

#RGB colors
WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

game_display = pygame.display.set_mode((WIDTH, HEIGHT)) #The display that PyGame opens
pygame.display.set_caption('Blob World') #The name of the display, you don't actually have to have one
clock = pygame.time.Clock() #This is just to shorten the function name


class RedBlob(Blob):
    
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, (255, 0, 0), x_boundary, y_boundary)


class GreenBlob(Blob):
    
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, (0, 255, 0), x_boundary, y_boundary)


class BlueBlob(Blob):
    
    def __init__(self, x_boundary, y_boundary):
        Blob.__init__(self, (0, 0, 255), x_boundary, y_boundary)

    def __add__(self, other_blob): #Allows us to use the sum of self + other_blob. Here, it defines interactions between a blue blob and other blobs.
        logging.info('Blob add operation: {} + {} at {} seconds'.format(str(self.color), str(other_blob.color), round((time.time() - start_time), 3)))
        if other_blob.color == (255, 0, 0):
            self.size -= other_blob.size
            other_blob.size -= self.size
            
        elif other_blob.color == (0, 255, 0):
            self.size += other_blob.size
            other_blob.size = 0
            
        elif other_blob.color == (0, 0, 255):
            # for now, nothing. Maybe later it does something more. 
            pass
        else:
            raise Exception('Tried to combine one or multiple blobs of unsupported colors!')


def is_touching(b1, b2):
    return np.linalg.norm(np.array([b1.x,b1.y]) - np.array([b2.x,b2.y])) < (b1.size + b2.size)
    #return True (thanks to <) if, on the 2D plain (the display), the distance between centers of two blobs is smaller than their combined radii

def handle_collisions(blob_list):
    reds, greens, blues = blob_list #harcoding the order of the list
    for blue_id, blue_blob in blues.copy().items(): #Copying and using the blue dict and list
        for other_blobs in reds, greens, blues:
            for other_blob_id, other_blob in other_blobs.copy().items():
                logging.debug('Checking if blobs touching {} + {}'.format(str(blue_blob.color), str(other_blob.color)))
                if blue_blob == other_blob: #Is the blue blob touching itself?
                    pass
                else:
                    if is_touching(blue_blob, other_blob):
                        blue_blob + other_blob
                        if other_blob.size <= 0:
                            del other_blobs[other_blob_id]
                        if blue_blob.size <= 0:
                            del blues[blue_id]
                            
    return reds, greens, blues #returns the new dictionaries

def draw_environment(blob_list): #the blob_list argument is taken from main()
    reds, greens, blues = handle_collisions(blob_list) #
    game_display.fill(BLACK)
    for blob_dict in blob_list:
        for blob_id in blob_dict:
            blob = blob_dict[blob_id]
            pygame.draw.circle(game_display, blob.color, [blob.x, blob.y], blob.size) #Draws a circle on the display, with color, location, and size (radius) as parameters
            blob.move()  #Calling the move() and check_bounds() methods for the blob instances from the Blob class
            blob.check_bounds()
    
    pygame.display.update() #Updates the display to show what you've told the program to do (same as plt.show())
    return reds, greens, blues #returns the new dictionaries

def main(): #We name it "main" because it actually runs the program
    red_blobs = dict(enumerate([RedBlob(WIDTH, HEIGHT) for i in range(RED_BLOBS_NUMBERS)]))       # A dictionary is made where each blob's memory location is assigned a key number.
    green_blobs = dict(enumerate([GreenBlob(WIDTH, HEIGHT) for i in range(GREEN_BLOBS_NUMBERS)])) # In other words, each blob has numbered IDs
    blue_blobs = dict(enumerate([BlueBlob(WIDTH, HEIGHT) for i in range(BLUE_BLOBS_NUMBERS)]))    #In the beggining, we start with these newly generated blobs.
    
    while True:
        try:
            for event in pygame.event.get():  #The following for loops just stops the program if you close the display window (pressing X on the top right)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            red_blobs, green_blobs, blue_blobs = draw_environment([red_blobs, green_blobs, blue_blobs]) #The current blob dictionary are passed to draw_environment()
            clock.tick(60) #This caps the fps to the designated number, which allows us to manipulate the speed of the program

        except Exception:
            logging.critical(error_handling()) #error_handling() is defined on line 18
            pygame.quit()
            quit()
            break

if __name__ == '__main__': #The __name__ variable is the file itself, Python assign a hard-coded string '__main__', such that __name__ = '__main__'
    main()                 #This is mainly so that you don't run functions from importing classes with a file that can be used as a script.