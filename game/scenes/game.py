import random

import pygame

from game.constants import Colors, Paths
from game.objects import ImageObject, TextObject, TextShootObject
from game.objects.bomb import BombObject
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
        self.start_ticks = pygame.time.get_ticks()
        self.milliseconds_left = 600000

        # Background image
        background_path = Paths.levels / random.choice(["level_bg.png", "level_bg_2.png"])

        self.background = ImageObject(
            (0, 0), background_path,
        )

        # Music
        pygame.mixer.music.load(str(Paths.music / "pskov_loop.ogg"))
        pygame.mixer.music.play(-1)

        # SFX
        self.gunshot = pygame.mixer.Sound(str(Paths.sfx / "gunshot.ogg"))
        self.wrong = pygame.mixer.Sound(str(Paths.sfx / "wrong_letter.ogg"))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_scene("main_menu")
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

    def draw_timer(self, location, font_name, color):
        """
        Build and draw a timer.
        """

        # Build the timer, and have it pass at double time.
        milliseconds_passed = (pygame.time.get_ticks() * 2) - self.start_ticks
        self.milliseconds_left = 600000 - milliseconds_passed
        minutes = int(self.milliseconds_left / 1000 // 60)
        seconds = int(self.milliseconds_left / 1000) - (minutes * 60)
        milliseconds = int(self.milliseconds_left) - (minutes * 60000) - (seconds * 1000)

        time_display = f"{minutes}:{seconds}.{milliseconds}"

        # Make the timer object
        TextObject(
            location,
            time_display,
            font_path=Paths.fonts / font_name,
            font_color=color
        ).draw()

    def draw(self):
        self.background.draw()
        self.draw_timer(
            (1080, 20),
            "ObelixPro-Cry-cyr.ttf",
            Colors.white
        )

        if self.new_missile_timer == 0:
            new_missile = BombObject(
                (random.randint(0, self.screen.get_width()), 260),
                random.choice([0.1, 0.2, 0.3, 0.4])
            )

            self.missiles.append(new_missile)
            self.texts.append(
                TextShootObject((0, 0), new_missile)
            )

            self.new_missile_timer = 200
        else:
            self.new_missile_timer -= 1

        for text in self.texts:
            text.draw()
