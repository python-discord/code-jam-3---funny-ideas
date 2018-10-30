import inspect
import sys

import pygame

import game.scenes
import game.scenes.splash_screens


class SceneManager:
    """
    A manager that keeps track of which Scene is active,
    listens for generic events, and then runs the event
    handler for the active scene.
    """

    def __init__(self):

        scenes = []
        for location in (game.scenes, game.scenes.splash_screens):
            for scene in inspect.getmembers(location):
                if not scene[0].startswith("__") and str(scene[1]).startswith("<class"):
                    scenes.append(scene[1])

        self.scenes = {
            scene.name: scene for scene in scenes
        }
        self.active = self.scenes.get("pydis")(self)

    def change_scene(self, scene: str):
        """
        Changes to the requested scene.

        See the self.scenes dictionary in the
        __init__ method for a list of valid scenes.

        :param scene: The name of the scene provided
                      as a snek_case string.
        """

        self.active.teardown()
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

                self.active.handle_events(event)

            self.active.draw()
            pygame.display.update()
