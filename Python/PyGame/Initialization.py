#https://www.youtube.com/watch?v=AY9MnQ4x3zk
import sys
import pygame
pygame.init()

screen = pygame.display.set_mode((1280, 660), pygame.RESIZABLE) #Opens a PyGame window with (Width, Height) under the variable "screen". (1280, 648) is the max for my computer.
pygame.display.set_caption('Display name')   #Names the PyGale window
clock = pygame.time.Clock()


test_surface = pygame.Surface((100, 200)) #Creates a surface under the variable "test_surface" with a width of 100px and a height of 200px
test_surface.fill('Red') #Colors "test_surface" red

image_surface = pygame.image.load("../../Rosace.ico").convert_alpha() #.convert() for easier pygame use, .convert_alpha to remove alpha values

test_font = pygame.font.SysFont('Verdana', 30) #Font and size, .Font(None, size) uses the default pygame font, for anything else, import sys and use .SysFont
text_surface = test_font.render('A string of words', True, 'Black') #Words, make the edges blocky or smooth, and color (can be rgb, so (0, 0, 0) instead of 'Black')

animated_surface = pygame.Surface((100, 40))
animated_surface.fill('Blue')
animated_x_pos = 300

while True:
    for event in pygame.event.get():  #For anything that you do with the display window
        if event.type == pygame.QUIT: #If you click on the close button (X on the top right)
            pygame.quit()             #The display window closes
            quit()                    #The program ends


    screen.fill('White') #If the dispaly isn't colored here, animated_surface will be stretched
    screen.blit(test_surface, (200, 100)) #(blit = block image transfer) It displays test_surface at the coordinates on the display.
    screen.blit(image_surface, (300, 0))
    screen.blit(text_surface, (400, 500))
    screen.blit(animated_surface, (animated_x_pos, 600))
    animated_x_pos += 1
    if animated_x_pos > 1280:
        animated_x_pos = -100

    pygame.display.update()
    clock.tick(60) #This caps the fps to the designated number, which allows us to manipulate the speed of the program