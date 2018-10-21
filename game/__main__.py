import pygame, sys
from pathlib import Path

from game import screen
from game.constants import Colors

# set up fonts
font_path = Path("game", "assets", "Vera.ttf")
basic_font = pygame.font.Font(str(font_path), 22)

# build some text
text = basic_font.render('btw I use arch', True, Colors.white)
text_rect = text.get_rect()
text_rect.centerx = screen.get_rect().centerx
text_rect.centery = screen.get_rect().centery

# draw the text's background rectangle onto the surface
pygame.draw.rect(
    screen,
    Colors.red,
    (text_rect.left - 20, text_rect.top - 20, text_rect.width + 40, text_rect.height + 40)
)

# get a pixel array of the surface
pix_array = pygame.PixelArray(screen)
pix_array[480][380] = Colors.black
del pix_array

# draw a logo
logo_path = Path("game", "assets", "logo.png")
logo = pygame.image.load(str(logo_path))
logo = pygame.transform.scale(logo, (100, 100))

# blit stuff to the screen
screen.blit(text, text_rect)
screen.blit(logo,(0,0))

# draw the window onto the screen
pygame.display.update()

# run the game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()