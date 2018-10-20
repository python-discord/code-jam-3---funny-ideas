import pygame, sys
from pygame.locals import *

# set up pygame
pygame.init()

# set up the window
screen = pygame.display.set_mode((1280, 800), 0, 32)
pygame.display.set_caption('Funny ideas')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# set up fonts
basic_font = pygame.font.SysFont(None, 48)

# set up the text
text = basic_font.render('btw I use arch', True, BLACK)
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery

# draw the white background onto the surface
screen.fill(WHITE)

# draw the text's background rectangle onto the surface
pygame.draw.rect(screen, RED, (text_rect.left - 20, text_rect.top - 20, text_rect.width + 40, text_rect.height + 40))

# get a pixel array of the surface
pixArray = pygame.PixelArray(screen)
pixArray[480][380] = BLACK
del pixArray

# draw a logo
logo = pygame.image.load("assets/logo.png")
logo = pygame.transform.scale(logo, (100, 100))

# draw stuff on the screen
screen.blit(text, text_rect)
screen.blit(logo,(0,0))

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()