import keyword
import random
from typing import Tuple

from pygame.font import Font
from pygame.surface import Surface

from game.constants import Paths
from game.objects import TextObject


FONT_COLOUR = (255, 255, 255)
FONT_COLOUR_TYPED = (255, 0, 0)
FONT_PATH = Paths.fonts / "FiraMono-Regular.ttf"
FONT_SIZE = 32
FONT = Font(str(FONT_PATH), FONT_SIZE)


class TextShootObject(TextObject):
    def __init__(self, location: Tuple[int, int]):
        self.word = random.choice(keyword.kwlist).upper()
        self.typed = random.randint(0, len(self.word))

        super().__init__(
            location,
            self.word,
            font_path=FONT_PATH,
            font_size=FONT_SIZE,
            font_color=FONT_COLOUR
        )

    def draw(self):
        if not self.typed:
            self.surface = FONT.render(self.word, True, FONT_COLOUR)
        elif self.typed >= len(self.word):
            self.surface = FONT.render(self.word, True, FONT_COLOUR_TYPED)
        else:
            typed_text = self.word[:self.typed]
            untyped_text = self.word[self.typed:]

            typed_surface: Surface = FONT.render(typed_text, True, FONT_COLOUR_TYPED)
            untyped_surface: Surface = FONT.render(untyped_text, True, FONT_COLOUR)

            self.surface = Surface(
                (
                    typed_surface.get_width() + untyped_surface.get_width(),
                    typed_surface.get_height() + untyped_surface.get_height()
                )
            )

            self.surface.blits(
                (
                    (typed_surface, (0, 0)),
                    (untyped_surface, (typed_surface.get_width(), 0))
                )
            )

        super(TextObject, self).draw()
