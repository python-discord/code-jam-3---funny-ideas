import random

import pygame

from game.constants import Paths
from game.objects import ImageObject, TextShootObject
from game.objects.text_shoot import TextShootState
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

        self.missiles = []
        self.texts = []
        self.new_missile_timer = 1
        self.lock = None

        # Background image
        self.background = ImageObject(
            (0, 0),
            Paths.levels / "level_bg.png",
        )

        # Music
        pygame.mixer.music.load(str(Paths.music / "pskov_loop.ogg"))
        pygame.mixer.music.play(-1)

        # SFX
        self.gunshot = pygame.mixer.Sound(str(Paths.sfx / "gunshot.ogg"))
        self.wrong = pygame.mixer.Sound(str(Paths.sfx / "wrong_letter.ogg"))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.lock:
                for text in self.texts:
                    result = text.key_input(event.key)

                    # If the user hit the right key, lock the word
                    if result == TextShootState.SUCCESS:
                        self.gunshot.play()
                        self.lock = text
                        break
                    elif result == TextShootState.WRONG_KEY:
                        self.wrong.play()
                    elif result == TextShootState.WORD_END:
                        self.gunshot.play()
                        self.lock = None

            else:
                result = self.lock.key_input(event.key)
                if result == TextShootState.SUCCESS:
                    self.gunshot.play()
                elif result == TextShootState.WORD_END:
                    self.gunshot.play()
                    self.texts.remove(self.lock)
                    self.lock = None
                elif result == TextShootState.WRONG_KEY:
                    self.wrong.play()

    def draw(self):
        self.background.draw()

        if self.new_missile_timer == 0:
            new_missile = ImageObject(
                (980, 260),
                Paths.items / "kickmissile.png",
            )

            self.missiles.append(new_missile)
            self.texts.append(
                TextShootObject((0, 0), new_missile)
            )

            self.new_missile_timer = 200
        else:
            self.new_missile_timer -= 1

        for missile in self.missiles:
            y_direction = random.choice([-1, 1])
            missile.move(0.1 * y_direction, 0.1)

        for text in self.texts:
            text.draw()
