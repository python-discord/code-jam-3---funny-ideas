import pygame

from pathlib import Path
from pygame.surface import Surface
import random
from typing import Tuple

from game.objects import BaseObject


AVATAR_MAX_NUM = 65
AVATAR_PATH = Path("game", "assets", "graphics", "avatars")
AVATAR_SIZE = (64, 64)

HEADLESS_PATH = Path("game", "assets", "graphics", "headless1.png")


class NPC(BaseObject):
    def __init__(self, location: Tuple[int, int]):
        avatar_num = random.randint(0, AVATAR_MAX_NUM)

        avatar_image: Surface = pygame.image.load(str(Path(AVATAR_PATH, f"{avatar_num}.png")))
        headless_image: Surface = pygame.image.load(str(HEADLESS_PATH))

        avatar_image = pygame.transform.smoothscale(avatar_image, AVATAR_SIZE)

        size = (
            headless_image.get_width() + 20,
            avatar_image.get_height() + headless_image.get_height()
        )

        surface = Surface(size)
        surface.blits(
            (
                (headless_image, (0, avatar_image.get_height() + 1)),
                (avatar_image, (23, 11))
            )
        )

        super(NPC, self).__init__(location, surface)
