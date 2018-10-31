import random
from pathlib import Path

from game.constants import Colors
from game.objects import ImageObject
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

        self.missiles = []
        self.new_missile_timer = 0

    def handle_events(self, event):
        pass

    def draw(self):
        self.screen.fill(Colors.black)

        if self.new_missile_timer == 0:
            self.missiles.append(
                ImageObject(
                    (980, 260),
                    Path("game", "assets", "graphics", "kickmissile.png"),
                )
            )
            self.new_missile_timer = random.randint(300, 700)
        else:
            self.new_missile_timer -= 1

        for missile in self.missiles:
            y_direction = random.choice([-1, 1])
            missile.draw()
            missile.move(0.1 * y_direction, 0.1 * y_direction)
