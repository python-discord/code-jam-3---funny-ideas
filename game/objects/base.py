from pathlib import Path
from typing import Tuple, Union

import pygame

from game import screen


class BaseObject:
    def __init__(self, height: int, width: int, location: Tuple[int, int], image_path: Union[Path, str]):
        self.height = height
        self.width = width
        self.location = location
        self.image = pygame.image.load(str(image_path))

    def draw(self):
        screen.blit(self.image, self.location)

    def move(self, horizontal: int = 0, vertical: int = 0):
        self.location = (
            self.location[0] + horizontal,
            self.location[1] + vertical
        )
