from pathlib import Path
from typing import Tuple

import pygame

from game.constants import Colors
from game.objects import TextObject


class Timer(TextObject):
    def __init__(
            self,
            location: Tuple[int, int],
            start_ticks: int,
            speed_multiplier: float = 30,
            *,
            font_path: Path = None,
            font_size: int = 32,
            font_color: Tuple[int, int, int] = Colors.white,
    ):

        # Build the timer, and have it pass at extra speed
        milliseconds_passed = (pygame.time.get_ticks() * speed_multiplier) - start_ticks
        self.milliseconds_left = 600000 - milliseconds_passed
        minutes = int(self.milliseconds_left / 1000 // 60)
        seconds = int(self.milliseconds_left / 1000) - (minutes * 60)
        milliseconds = int(self.milliseconds_left) - (minutes * 60000) - (seconds * 1000)

        time_display = f"{minutes}:{seconds}.{milliseconds}"

        # Make the TextObject
        super().__init__(
            location,
            time_display,
            font_path=font_path,
            font_size=font_size,
            font_color=font_color
        )
