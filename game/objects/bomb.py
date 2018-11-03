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

        super().__init__(location, Paths.items / "kickmissile.png")

    def draw(self):
        y_direction = random.choice([-1, 1])
        self.move(self.speed * y_direction, self.speed)

        super().draw()
