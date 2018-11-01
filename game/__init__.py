import pygame
from pygame.surface import Surface

from game.constants import Colors, Window

# set up pygame
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()

# set up the window
screen: Surface = pygame.display.set_mode((Window.width, Window.height), 0, Window.depth)
pygame.display.set_caption(Window.title)
screen.fill(Colors.black)
