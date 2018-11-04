import random
from typing import Tuple

from game.constants import Paths, Window
from game.objects import ImageObject
from game.objects.bomb import BombObject


class Flutterdude(ImageObject):
    """
    Represents the Flutterdude enemy type.
    Handles its own movement to fly across the screen and flip.
    """

    def __init__(self, location: Tuple[int, int], speed: float):
        self.speed = speed
        self.facing_right = True

        super().__init__(location, Paths.enemies / "flutterdude.png")

    def draw(self):

        # Set some useful shorthand
        x = self.location[0]
        width = self.size[1]
        swoop_speed = 0.10

        # Check if we've hit the edge on either side
        if x <= 0 and not self.facing_right or (x + width) >= Window.width and self.facing_right:
            self.facing_right = not self.facing_right
            self.flip()

        # Swoop towards middle
        if self.facing_right:
            if x > (Window.width / 2):
                self.move(self.speed, -swoop_speed)
            elif x <= (Window.width / 2):
                self.move(self.speed, swoop_speed)
        else:
            if x > (Window.width / 2):
                self.move(-self.speed, swoop_speed)
            elif x <= (Window.width / 2):
                self.move(-self.speed, -swoop_speed)

        super().draw()

    def create_bomb(self):
        location = (
            self.location[0] + (self.size[0] / 2),
            self.location[1] + (self.size[1] / 2)
        )
        return BombObject(location, random.uniform(0.1, 0.4))
