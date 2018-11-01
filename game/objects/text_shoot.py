import keyword
import random
from typing import Tuple

import pygame
from pygame.font import Font
from pygame.rect import Rect
from pygame.surface import Surface

from game.constants import Paths
from game.objects import GraphicalObject, TextObject

BACKGROUND_COLOUR = (125, 125, 125, 0.5)

FONT_COLOUR = (255, 255, 255)
FONT_COLOUR_TYPED = (255, 0, 0)
FONT_PATH = Paths.fonts / "FiraMono-Regular.ttf"
FONT_SIZE = 32
FONT = Font(str(FONT_PATH), FONT_SIZE)


class TextShootObject(TextObject):
    def __init__(self, location: Tuple[int, int], parent: GraphicalObject = None):
        self.word = random.choice(keyword.kwlist).upper()
        self.typed = random.randint(0, len(self.word))

        super().__init__(
            location,
            self.word,
            font_path=FONT_PATH,
            font_size=FONT_SIZE,
            font_color=FONT_COLOUR
        )

        self.parent = parent

    def draw(self):
        if not self.typed:
            self.surface = FONT.render(self.word, True, FONT_COLOUR, BACKGROUND_COLOUR)
        elif self.typed >= len(self.word):
            self.surface = FONT.render(self.word, True, FONT_COLOUR_TYPED, BACKGROUND_COLOUR)
        else:
            typed_text = self.word[:self.typed]
            untyped_text = self.word[self.typed:]

            typed_surface: Surface = FONT.render(typed_text, True, FONT_COLOUR_TYPED, BACKGROUND_COLOUR)
            untyped_surface: Surface = FONT.render(untyped_text, True, FONT_COLOUR, BACKGROUND_COLOUR)

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

        pygame.draw.ellipse(
            surface, BACKGROUND_COLOUR,
            Rect(0, 0, 20, surface.get_height())
        )
        pygame.draw.ellipse(
            surface, BACKGROUND_COLOUR,
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
