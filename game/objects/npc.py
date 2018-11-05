import random
from typing import Tuple

import pygame
from pygame.surface import Surface

from game.constants import Avatars, Colors, Paths
from game.objects import GraphicalObject


class NPC(GraphicalObject):
    """
    Game object representing an NPC - takes our headless image and slaps an
    avatar onto it.
    """

    avatars_in_use = []

    def __init__(self, location: Tuple[int, int]):
        """
        Construct a new NPC.

        :param location: The top-left coordinate of the object on the screen.
        """

        # Crash proof scaling
        while True:
            try:
                avatar_num = random.randint(0, Avatars.max_number)

                # Prevent duplicate avatars
                if avatar_num in self.avatars_in_use:
                    continue
                else:
                    self.avatars_in_use.append(avatar_num)

                avatar_image: Surface = pygame.image.load(str(Paths.avatars / f"{avatar_num}.png"))
                headless_image: Surface = pygame.image.load(str(Paths.headless / f"headless{avatar_num % 5}.png"))
                avatar_image = pygame.transform.smoothscale(avatar_image, Avatars.size)
            except ValueError:
                print(f"ERROR: Avatar {avatar_num} is not 24 or 32bit")
            else:
                break

        # Turn around after x frames
        self.frames_until_turn = random.randint(100, 500)

        size = (
            headless_image.get_width() + 20,
            avatar_image.get_height() + headless_image.get_height() - Avatars.offset_y
        )

        surface = Surface(size)
        surface.fill(Colors.black)
        surface.set_colorkey(Colors.black)
        surface.blits(
            (
                (headless_image, (0, avatar_image.get_height() - Avatars.offset_y)),
                (avatar_image, (Avatars.offset_x, 0))
            )
        )

        super(NPC, self).__init__(location, surface)
