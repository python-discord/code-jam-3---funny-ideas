import random
from enum import Enum
from typing import Tuple

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from game import screen
from game.constants import Colors, Paths, Words
from game.objects import GraphicalObject, TextObject

FONT_PATH = Paths.fonts / "FiraMono-Regular.ttf"
FONT_SIZE = 32
FONT = Font(str(FONT_PATH), FONT_SIZE)


class TextShootState(Enum):
    SUCCESS = 1
    WORD_END = 2
    WRONG_KEY = 3


class TextShootObject(TextObject):
    def __init__(self, location: Tuple[int, int], parent: GraphicalObject = None, long: bool = False):
        self.is_long = long

        if long:
            self.word = random.choice(Words.long).upper()
        else:
            self.word = random.choice(Words.single).upper()

        self.typed = 0

        super().__init__(
            location,
            self.word,
            font_path=FONT_PATH,
            font_size=FONT_SIZE,
            font_color=Colors.white
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
            self.surface = FONT.render(self.word, True, Colors.white, Colors.blurple)
        elif self.typed >= len(self.word):
            self.surface = FONT.render(self.word, True, Colors.red, Colors.blurple)
        else:
            typed_text = self.word[:self.typed]
            untyped_text = self.word[self.typed:]

            typed_surface: Surface = FONT.render(typed_text, True, Colors.red, Colors.blurple)
            untyped_surface: Surface = FONT.render(untyped_text, True, Colors.white, Colors.blurple)

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
            surface, Colors.blurple,
            Rect(0, 0, 20, surface.get_height())
        )
        pygame.draw.ellipse(
            surface, Colors.blurple,
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

        if self.location[0] <= 0 or self.location[0] + self.surface.get_width() >= screen.get_width():
            self.parent.y_direction = -self.parent.y_direction

        super(TextObject, self).draw()

        if self.parent:
            self.parent.draw()
