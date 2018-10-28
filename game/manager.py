import sys

import pygame

from game.scenes import MainMenu


class SceneManager:
    """
    A manager that keeps track of which Scene is active,
    listens for generic events, and then runs the event
    handler for the active scene.
    """

    def __init__(self):
        self.active = MainMenu()  # The currently active Scene

    def run(self):

        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.active.draw()
            pygame.display.update()