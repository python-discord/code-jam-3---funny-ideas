import pygame

from game.constants import Colors, Window

# set up pygame
pygame.init()

# set up the window
screen = pygame.display.set_mode((Window.width, Window.height), 0, Window.depth)
pygame.display.set_caption(Window.title)

# draw the white background onto the surface
screen.fill(Colors.black)
