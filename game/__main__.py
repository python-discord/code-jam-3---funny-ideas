import pygame
import sys
from game.sequences import IntroSplashSequence

iss = IntroSplashSequence()
iss.run()

# run the game loop
while False:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()