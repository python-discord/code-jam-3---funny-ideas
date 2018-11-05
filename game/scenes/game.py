import random
from typing import List, Tuple

import pygame

from game.constants import Explosions, Paths, Window
from game.objects import Explosion, ImageObject, TextObject, TextShootObject, Timer
from game.objects.flutterdude import Flutterdude
from game.objects.npc import NPC
from game.objects.pyjet import PyJet
from game.objects.text_shoot import TextShootState
from game.scenes.base.scene import Scene


class Game(Scene):

    name = "game"

    def __init__(self, manager):
        super().__init__(manager)

        self.accuracy = None
        self.speed_multiplier = 3
        self.explosions: List[Explosion] = []
        self.texts: List[TextShootObject] = []
        self.new_missile_timer = 200
        self.new_jet_timer = random.randint(450, 1200)

        self.lock = None
        self.start_ticks = pygame.time.get_ticks()
        self.game_running = True
        self.you_lose = None
        self.you_win = None
        self.wpm = None
        self.letters_typed = 0
        self.letters_missed = 0

        self.restart_game_text = TextObject(
            (600, 600),
            "Restart game",
            font_path=Paths.fonts / "ObelixPro-cyr.ttf",
            font_size=60
        )
        self.wpm_text = None
        self.accuracy_text = None

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
        self.gunshot.set_volume(0.4)
        self.wrong = pygame.mixer.Sound(str(Paths.sfx / "wrong_letter.ogg"))
        self.you_lose_sfx = pygame.mixer.Sound(str(Paths.sfx / "you_lose.ogg"))
        self.you_win_sfx = pygame.mixer.Sound(str(Paths.sfx / "you_win.ogg"))

        # Some random NPCs
        number_of_npcs = 7

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

        # Enemies
        self.flutterdude = Flutterdude(
            (0, 75),
            1.5
        )

        self.pyjet = None

    def handle_events(self, event):

        restart_game = self.restart_game_text

        if not self.game_running and restart_game.mouseover():
            if not restart_game.highlighted:
                restart_game.highlight()

            if pygame.mouse.get_pressed()[0]:
                self.manager.change_scene("game")

        elif not self.game_running and not restart_game.mouseover():
            restart_game.remove_highlight()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.manager.change_scene("main_menu")
            elif event.key == pygame.K_F5:  # YOU LOSE
                self.game_running = False
                self.npcs = []
            elif event.key == pygame.K_F6:  # YOU WIN
                self.game_running = False
                self.npcs = ["something"]
            elif event.key == pygame.K_BACKSPACE and self.lock:
                if self.lock.typed > 0:
                    self.lock.typed -= 1
                else:
                    self.lock = None

            if not self.lock:
                for text in self.texts:
                    result = text.key_input(event.key)

                    # If the user hit the right key, lock the word
                    if result == TextShootState.SUCCESS:
                        self.letters_typed += 1
                        self.gunshot.play()
                        self.lock = text

                        # Move the locked element to the end so it always renders on top of everything else.
                        self.texts.append(self.texts.pop(self.texts.index(self.lock)))

                        break
                    elif result == TextShootState.WORD_END:
                        self.letters_typed += 1
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
                    self.letters_typed += 1
                    self.gunshot.play()
                elif result == TextShootState.WORD_END:
                    self.letters_typed += 1
                    self.gunshot.play()
                    self.texts.remove(self.lock)
                    self.add_explosion(
                        self.lock.location,
                        random.choice(Explosions.destroy_text),
                        size=125
                    )
                    self.lock = None
                elif result == TextShootState.WRONG_KEY:
                    self.letters_missed += 1
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
            self.timer = Timer(
                (1080, 20),
                self.start_ticks,
                speed_multiplier=self.speed_multiplier,
                font_path=Paths.fonts / "ObelixPro-Cry-cyr.ttf"
            )
            self.timer.draw()

            # Draw those pesky NPCs
            for npc in self.npcs:
                if npc.frames_until_turn <= 0:
                    npc.flip()
                    npc.frames_until_turn = random.randint(100, 3000)
                else:
                    npc.frames_until_turn -= 1
                npc.draw()

            # Draw the flutterdude
            self.flutterdude.draw()

            # Create new flutterdude missiles periodically
            if self.new_missile_timer == 0 or not self.texts:
                new_missile = self.flutterdude.create_bomb(random.uniform(0.1, 0.4))

                self.texts.append(
                    TextShootObject((0, 0), new_missile)
                )

                if self.new_missile_timer == 0:
                    self.new_missile_timer = 200
            else:
                self.new_missile_timer -= 1

            # Create jet periodically
            if self.new_jet_timer == 0:
                self.pyjet = PyJet(
                    left_to_right=random.choice((True, False))
                )
                self.new_jet_timer = random.randint(450, 1200)
            else:
                self.new_jet_timer -= 1

            # Fly the jet! Rocket maaan!
            if self.pyjet:
                pyjet_x = self.pyjet.location[0]
                pyjet_width = self.pyjet.size[0]
                off_screen = (
                    (pyjet_x + pyjet_width) <= 0
                    and not self.pyjet.left_to_right
                    or pyjet_x >= Window.width
                    and self.pyjet.left_to_right
                )

                if off_screen:
                    self.pyjet = None
                else:
                    if not self.pyjet.bombs_dropped == len(self.pyjet.bomb_drop_locations):
                        drop_bomb_left = (
                            pyjet_x >= self.pyjet.bomb_drop_locations[self.pyjet.bombs_dropped - 1]
                            and self.pyjet.left_to_right
                        )

                        drop_bomb_right = (
                            pyjet_x <= self.pyjet.bomb_drop_locations[-(self.pyjet.bombs_dropped + 1)]
                            and not self.pyjet.left_to_right
                        )

                        if drop_bomb_left or drop_bomb_right:
                            new_missile = self.pyjet.create_bomb(random.uniform(0.6, 1.2))

                            self.texts.append(
                                TextShootObject((0, 0), new_missile)
                            )

                            self.pyjet.bombs_dropped += 1

                    self.pyjet.draw()

            # Draw all the explosions
            for explosion in self.explosions.copy():
                explosion.draw()

                if explosion.frame_count >= explosion.frame_length:
                    self.explosions.remove(explosion)

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

                    # Remove it from lock if it was locked.
                    if text == self.lock:
                        self.lock = None

                text.draw()

            # Check if we've lost yet
            if not self.npcs:
                self.game_running = False

            # Check if we've won (timer finished)
            if self.timer.milliseconds_left <= 0:
                self.game_running = False

        # Game is over, and we need to draw some UI.
        else:
            # Calculate WPM
            if self.wpm is None:
                total_letters = self.letters_typed + self.letters_missed
                self.wpm = int((total_letters / 5) / self.timer.minutes_passed)
                self.wpm_text = TextObject(
                    (1045, 15),
                    f"WPM: {self.wpm}",
                    font_path=Paths.fonts / "ObelixPro-cyr.ttf",
                    font_size=35
                )

            if self.accuracy is None:
                total_letters = self.letters_typed + self.letters_missed

                if total_letters:
                    self.accuracy = int(
                        100 - ((self.letters_missed / total_letters) * 100)
                    )
                else:
                    self.accuracy = 0

                self.accuracy_text = TextObject(
                    (938, 70),
                    f"Accuracy: {self.accuracy}%",
                    font_path=Paths.fonts / "ObelixPro-cyr.ttf",
                    font_size=35
                )

            # Player has lost
            if not self.npcs:
                if not self.you_lose:
                    self.you_lose = ImageObject(
                        (0, 0),
                        Paths.ui / "you_lose.png"
                    )
                    image_width = self.you_lose.size[0]
                    center_x = (Window.width / 2) - (image_width / 2)
                    self.you_lose.move_absolute((center_x, 220))
                    self.you_lose_sfx.play()
                    self.restart_game_text.move_absolute((
                        (Window.width / 2) - (self.restart_game_text. size[0] / 2),
                        450
                    ))

                self.you_lose.draw()

            # Player has won
            else:
                if not self.you_win:
                    self.you_win = ImageObject(
                        (0, 0),
                        Paths.ui / "winner.png"
                    )
                    image_width = self.you_win.size[0]
                    center_x = (Window.width / 2) - (image_width / 2)
                    self.you_win.move_absolute((center_x, 100))
                    self.you_win_sfx.play()
                    self.restart_game_text.move_absolute((
                        (Window.width / 2) - (self.restart_game_text.size[0] / 2),
                        450
                    ))

                self.you_win.draw()

            self.restart_game_text.draw()
            self.wpm_text.draw()
            self.accuracy_text.draw()
