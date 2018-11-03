import random
from typing import Tuple

import pygame
from pygame.surface import Surface

from game.constants import Paths, Colors
from game.objects import GraphicalObject


AVATAR_MAX_NUM = 58
AVATAR_OFFSET_X = 23
AVATAR_OFFSET_Y = 10
AVATAR_SIZE = (64, 64)


class NPC(GraphicalObject):
    """
    Game object representing an NPC - takes our headless image and slaps an
    avatar onto it.
    """

    def __init__(self, location: Tuple[int, int]):
        """
        Construct a new NPC.

        :param location: The top-left coordinate of the object on the screen.
        """

        avatar_num = random.randint(0, AVATAR_MAX_NUM)

        avatar_image: Surface = pygame.image.load(str(Paths.avatars / f"{avatar_num}.png"))
        headless_image: Surface = pygame.image.load(str(Paths.headless / f"headless{avatar_num % 5}.png"))

        print(avatar_num)
        avatar_image = pygame.transform.smoothscale(avatar_image, AVATAR_SIZE)

        # Turn around after x frames
        self.frames_until_turn = random.randint(100, 500)

        size = (
            headless_image.get_width() + 20,
            avatar_image.get_height() + headless_image.get_height() - AVATAR_OFFSET_Y
        )

        surface = Surface(size)
        surface.fill(Colors.black)
        surface.set_colorkey(Colors.black)
        surface.blits(
            (
                (headless_image, (0, avatar_image.get_height() - AVATAR_OFFSET_Y)),
                (avatar_image, (AVATAR_OFFSET_X, 0))
            )
        )

        super(NPC, self).__init__(location, surface)
