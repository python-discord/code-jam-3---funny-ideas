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
            highlight_color: Tuple[int, int, int] = (255, 200, 0),
    ):
        self.font_path = font_path if font_path else Path("game", "assets", "fonts", "FiraMono-Regular.ttf")
        self.word = word
        self.font = Font(str(self.font_path), font_size)
        self.font_color = font_color
        self.highlight_color = highlight_color
        self.highlighted = False

        surface = self.font.render(self.word, True, font_color)

        super().__init__(location, surface)

    def highlight(self):
        """
        Changes the font color,
        in order to "highlight" the text
        for example during mouseover.
        """

        if not self.highlighted:
            self.surface = self.font.render(self.word, True, self.highlight_color)
            self.highlighted = True

    def remove_highlight(self):
        """
        Changes the font color back,
        in order to remove the highlight.
        """

        if self.highlighted:
            self.surface = self.font.render(self.word, True, self.font_color)
            self.highlighted = False
