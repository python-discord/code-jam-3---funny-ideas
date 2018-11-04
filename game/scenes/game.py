import random
from typing import List, Tuple

import pygame

from game.constants import Explosions, Paths, Window
from game.objects import Explosion, ImageObject, TextShootObject, Timer
from game.objects.bomb import BombObject
from game.objects.flutterdude import Flutterdude
from game.objects.npc import NPC
from game.objects.text_shoot import TextShootState
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

        self.explosions: List[Explosion] = []
        self.texts: List[TextShootObject] = []
        self.new_missile_timer = 1
        self.lock = None
        self.start_ticks = pygame.time.get_ticks()
        self.milliseconds_left = 600000
        self.game_running = True
        self.you_lose = None
        self.you_win = None

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
        self.you_lose_sfx = pygame.mixer.Sound(str(Paths.sfx / "you_lose.ogg"))

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

        # Flutterdude enemy
        self.flutterdude = Flutterdude(
            (0, 75),
            1.5
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
                    elif result == TextShootState.WORD_END:
                        self.gunshot.play()
                        self.texts.remove(text)
                        self.add_explosion(
                            text.location,
                            random.choice(Explosions.destroy_text),
                            size=125
                        )
                        self.lock = None

            else:
                result = self.lock.key_input(event.key)

                if result == TextShootState.SUCCESS:
                    self.gunshot.play()
                elif result == TextShootState.WORD_END:
                    self.gunshot.play()
                    self.texts.remove(self.lock)
                    self.add_explosion(
                        self.lock.location,
                        random.choice(Explosions.destroy_text),
                        size=125
                    )
                    self.lock = None
                elif result == TextShootState.WRONG_KEY:
                    self.wrong.play()

    def add_explosion(self, location: Tuple[int, int], text: str, size: int = 175, partial: bool = False):
        explosion = Explosion(
            location,
            Paths.fonts / "ObelixPro-Cry-cyr.ttf",
            text,
            size,
        )

        self.explosions.append(explosion)

    def draw(self):
        self.background.draw()

        if self.game_running:
            # Draw the timer
            timer = Timer(
                (1080, 20),
                self.start_ticks,
                font_path=Paths.fonts / "ObelixPro-Cry-cyr.ttf"
            )
            timer.draw()

            # Draw those pesky NPCs
            for npc in self.npcs:
                if npc.frames_until_turn <= 0:
                    npc.flip()
                    npc.frames_until_turn = random.randint(100, 3000)
                else:
                    npc.frames_until_turn -= 1
                npc.draw()

            # Flutterdude movement
            self.flutterdude.draw()

            # Create new missiles periodically
            if self.new_missile_timer == 0 or not self.texts:
                new_missile = self.flutterdude.create_bomb()

                self.texts.append(
                    TextShootObject((0, 0), new_missile)
                )

                self.new_missile_timer = 200
            else:
                self.new_missile_timer -= 1

            # Draw the missiles
            for text in self.texts:
                text_x, text_y = text.location
                y_loc = text_y + text.surface.get_rect().bottomleft[1]
                if y_loc >= 550:

                    # Explode the missile!
                    self.add_explosion(
                        text.location,
                        random.choice(Explosions.ban_text),
                        size=250
                    )
                    self.texts.remove(text)

                    # Murder the NPC!
                    closest_npc = None
                    for npc in self.npcs:
                        if not closest_npc:
                            closest_npc = npc
                        elif abs(npc.location[0] - text_x) < abs(closest_npc.location[0] - text_x):
                            closest_npc = npc
                    self.npcs.remove(closest_npc)

                text.draw()

            # Draw all the explosions
            for explosion in self.explosions.copy():
                explosion.draw()

                if explosion.frame_count >= explosion.frame_length:
                    self.explosions.remove(explosion)

            # Check if we've lost yet
            if not self.npcs:
                self.game_running = False

        # Game is over, and we need to draw some UI.
        else:
            # Player has lost
            if not self.npcs:

                if not self.you_lose:
                    self.you_lose = ImageObject(
                        (0, 0),
                        Paths.ui / "you_lose.png"
                    )
                    image_width = self.you_lose.size[0]
                    center_x = (Window.width / 2) - (image_width / 2)
                    self.you_lose.move_absolute((center_x, 250))
                    self.you_lose_sfx.play()

                self.you_lose.draw()
