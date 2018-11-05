import random

import pygame

from game.constants import Paths, Window
from game.objects.enemy import EnemyObject


class PyJet(EnemyObject):
    """
    Represents the PyJet enemy type.
    Handles its own movement to zoom across the screen.
    """

    def __init__(self, left_to_right: bool):

        super().__init__((0, 0), Paths.enemies / "pyjet.png")

        self.left_to_right = left_to_right
        self.bombs_dropped = 0
        self.bomb_drop_locations = (
            random.randint(200, 400),
            random.randint(500, 700),
            random.randint(800, 1000),
        )

        if left_to_right:
            self.flip()
            self.speed = 7.5
            location = (-self.size[0], 75)
        else:
            self.speed = -7.5
            location = (Window.width, 75)

        self.move_absolute(location)

        sound = pygame.mixer.Sound(str(Paths.sfx / "fighter_jet.ogg"))
        sound.play()

    def draw(self):
        self.move(self.speed, 0.05)

        super().draw()
