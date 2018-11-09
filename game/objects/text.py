from pathlib import Path
from typing import Tuple

from pygame.font import Font

from game.constants import Paths
from game.objects import GraphicalObject


class TextObject(GraphicalObject):
    def __init__(
            self,
            scene,
            location: Tuple[int, int],
            word: str,
            *,
            font_path: Path = None,
            font_size: int = 32,
            font_color: Tuple[int, int, int] = (255, 255, 255),
            highlight_color: Tuple[int, int, int] = (255, 200, 0),
            disabled_color: Tuple[int, int, int] = (100, 100, 100),
            disabled: bool = False,
    ):
        self.font_path = font_path if font_path else Paths.fonts / "FiraMono-Regular.ttf"
        self.word = word
        self.font = Font(str(self.font_path), font_size)
        self.font_color = font_color
        self.highlight_color = highlight_color
        self.highlighted = False
        self.disabled = disabled
        self.disabled_color = disabled_color

        if self.disabled:
            surface = self.font.render(self.word, True, disabled_color)
        else:
            surface = self.font.render(self.word, True, font_color)

        super().__init__(scene, location, surface)

    def highlight(self):
        """
        Changes the font color,
        in order to "highlight" the text
        for example during mouseover.
        """

        if not self.highlighted:
            if not self.disabled:
                self.surface = self.font.render(self.word, True, self.highlight_color)
            self.highlighted = True

    def remove_highlight(self):
        """
        Changes the font color back,
        in order to remove the highlight.
        """

        if self.highlighted:
            if not self.disabled:
                self.surface = self.font.render(self.word, True, self.font_color)
            self.highlighted = False

    def disable(self):
        """
        Changes the font color to
        a grayed out one.
        """
        if not self.disabled:
            self.disabled = True
            self.surface = self.font.render(self.word, True, self.disabled_color)

    def enable(self):
        """
        Returns the font color
        to normal.
        """
        if self.disabled:
            self.disabled = False

            # Do we highlight or not?
            if self.highlighted:
                self.surface = self.font.render(self.word, True, self.highlight_color)
            else:
                self.surface = self.font.render(self.word, True, self.font_color)
