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
            font_path: Path = Path("game", "assets", "fonts", "FiraMono-Regular.ttf"),
            font_size: int = 32,
            font_color: Tuple[int, int, int] = (255, 255, 255),
    ):
        self.word = word
        self.font = Font(str(font_path), font_size)

        surface = self.font.render(self.word, True, font_color)

        super().__init__(location, surface)
