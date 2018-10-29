import sys

import pygame

from game.scenes import Game, MainMenu


class SceneManager:
    """
    A manager that keeps track of which Scene is active,
    listens for generic events, and then runs the event
    handler for the active scene.
    """

    def __init__(self):
        self.active = MainMenu(self)  # The currently active Scene

        self.scenes = {
            "main_menu": MainMenu,
            "game": Game,
        }

    def change_scene(self, scene: str):
        """
        Changes to the requested scene.

        See the self.scenes dictionary in the
        __init__ method for a list of valid scenes.

        :param scene: The name of the scene provided
                      as a snek_case string.
        """

        new_scene = self.scenes.get(scene)

        if new_scene:
            self.active = new_scene(self)

    def run(self):

        # run the game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.active.handle_events()
            self.active.draw()
            pygame.display.update()
