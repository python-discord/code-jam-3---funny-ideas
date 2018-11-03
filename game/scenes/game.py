import random

import pygame

from game.constants import Paths
from game.objects import ImageObject, TextShootObject, Timer
from game.objects.bomb import BombObject
from game.objects.npc import NPC
from game.objects.text_shoot import TextShootState
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

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

        # Some random NPCs
        number_of_npcs = random.randint(3, 7)
        npc_slots = [
            (123, 550),
            (211, 550),
            (284, 550),
            (450, 550),
            (570, 550),
            (800, 550),
            (990, 550),
        ]
        random.shuffle(npc_slots)
        self.npcs = []
        for _ in range(number_of_npcs):
            self.npcs.append(
                NPC(npc_slots.pop(-1))
            )

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

    def draw(self):
        self.background.draw()
        timer = Timer(
            (1080, 20),
            self.start_ticks,
            font_path=Paths.fonts / "ObelixPro-Cry-cyr.ttf"
        )
        timer.draw()

        for npc in self.npcs:
            npc.draw()

        if self.new_missile_timer == 0:
            new_missile = BombObject(
                (random.randint(0, self.screen.get_width()), 260),
                random.choice([0.1, 0.2, 0.3, 0.4])
            )

            self.texts.append(
                TextShootObject((0, 0), new_missile)
            )

            self.new_missile_timer = 200
        else:
            self.new_missile_timer -= 1

        for text in self.texts:
            text.draw()
