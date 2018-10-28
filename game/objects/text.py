from pathlib import Path
from typing import Tuple

from pygame.font import Font

from game.objects import BaseObject


class TextObject(BaseObject):
    def __init__(
            self,
            location: Tuple[int, int],
            word: str,
            *,
            font_path: Path = None,
            font_size: int = 32,
            font_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        self.font_path = font_path if font_path else Path("game", "assets", "fonts", "FiraMono-Regular.ttf")
        self.word = word
        self.font = Font(str(self.font_path), font_size)

        surface = self.font.render(self.word, True, font_color)

        super().__init__(location, surface)
