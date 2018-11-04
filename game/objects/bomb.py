import random
from typing import Tuple

from game.constants import Paths
from game.objects import ImageObject


class BombObject(ImageObject):
    """
    Representation of a falling bomb. Handles its own
    movement.
    """

    def __init__(self, location: Tuple[int, int], speed: float):
        self.speed = speed
        self.y_direction = random.uniform(-1.0, 1.0)

        super().__init__(location, Paths.items / "kickmissile.png")

    def draw(self):
        self.move(self.speed * self.y_direction, self.speed)

        super().draw()
