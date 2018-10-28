import keyword
import random
from pathlib import Path
from typing import Tuple

from pygame.font import Font

from game.objects import BaseObject

FONT_COLOUR = (255, 255, 255)
FONT_PATH = Path("game", "assets", "fonts", "FiraMono-Regular.ttf")
FONT_SIZE = 32
FONT = Font(str(FONT_PATH), FONT_SIZE)


class TextObject(BaseObject):
    def __init__(self, location: Tuple[int, int]):
        self.word = random.choice(keyword.kwlist).upper()

        surface = FONT.render(self.word, True, FONT_COLOUR)

        super(TextObject, self).__init__(location, surface)
