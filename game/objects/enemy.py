from pathlib import Path
from typing import Tuple

from game.objects import ImageObject
from game.objects.bomb import BombObject


class EnemyObject(ImageObject):
    """
    Represents the enemy type.
    """

    def __init__(self, scene, location: Tuple[int, int], image_path: Path):

        super().__init__(scene, location, image_path)

    def create_bomb(self, speed: int):
        location = (
            self.location[0] + (self.size[0] / 2),
            self.location[1] + (self.size[1] / 2)
        )
        return BombObject(self.scene, location, speed)
