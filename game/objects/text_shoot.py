import keyword
import random
from enum import Enum
from typing import Tuple

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from game.constants import Paths, Colours
from game.objects import GraphicalObject, TextObject

FONT_PATH = Paths.fonts / "FiraMono-Regular.ttf"
FONT_SIZE = 32
FONT = Font(str(FONT_PATH), FONT_SIZE)


class TextShootState(Enum):
    SUCCESS = 1
    WORD_END = 2
    WRONG_KEY = 3


class TextShootObject(TextObject):
    def __init__(self, location: Tuple[int, int], parent: GraphicalObject = None):
        self.word = random.choice(keyword.kwlist).upper()
        self.typed = 0

        super().__init__(
            location,
            self.word,
            font_path=FONT_PATH,
            font_size=FONT_SIZE,
            font_color=Colours.white
        )

        self.parent = parent

    def key_input(self, key):
        key_name = pygame.key.name(key)

        if self.word[self.typed].lower() == key_name:
            if self.typed == len(self.word) - 1:
                return TextShootState.WORD_END
            self.typed += 1
            return TextShootState.SUCCESS
        return TextShootState.WRONG_KEY

    def draw(self):
        if not self.typed:
            self.surface = FONT.render(self.word, True, Colours.white, Colours.blurple)
        elif self.typed >= len(self.word):
            self.surface = FONT.render(self.word, True, Colours.red, Colours.blurple)
        else:
            typed_text = self.word[:self.typed]
            untyped_text = self.word[self.typed:]

            typed_surface: Surface = FONT.render(typed_text, True, Colours.red, Colours.blurple)
            untyped_surface: Surface = FONT.render(untyped_text, True, Colours.white, Colours.blurple)

            self.surface = Surface(
                (
                    typed_surface.get_width() + untyped_surface.get_width(),
                    max(typed_surface.get_height(), untyped_surface.get_height())
                )
            )

            self.surface.blits(
                (
                    (typed_surface, (0, 0)),
                    (untyped_surface, (typed_surface.get_width(), 0))
                )
            )

        surface = Surface((
            self.surface.get_width() + 20,
            self.surface.get_height()
        ))

        surface.set_colorkey((0, 0, 0))

        pygame.draw.ellipse(
            surface, Colours.blurple,
            Rect(0, 0, 20, surface.get_height())
        )
        pygame.draw.ellipse(
            surface, Colours.blurple,
            Rect(surface.get_width() - 20, 0, 20, surface.get_height())
        )

        surface.blit(self.surface, (10, 0))
        self.surface = surface

        if self.parent:
            half_width = self.surface.get_width() / 2

            self.location = (
                self.parent.location[0] - half_width + self.parent.surface.get_width() / 2,
                self.parent.location[1] - 40
            )

        super(TextObject, self).draw()

        if self.parent:
            self.parent.draw()
