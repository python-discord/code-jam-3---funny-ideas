from pathlib import Path
from typing import NamedTuple


class URLs(NamedTuple):
    api = "https://megalomaniac.seph.club/api"
    scores_api = f"{api}/scores"
    add_score_api = f"{api}/add_score"


class Colors(NamedTuple):
    black = (0, 0, 0)
    blue = (0, 0, 255)
    blurple = (114, 137, 218)
    green = (0, 255, 0)
    red = (255, 0, 0)
    white = (255, 255, 255)
    yellow = (255, 255, 0)
    orange = (255, 165, 0)


class Window(NamedTuple):
    width = 1280
    height = 800
    depth = 32
    title = "Code Jam III: Funny Ideas"


class Avatars(NamedTuple):
    max_number = 58
    offset_x = 23
    offset_y = 10
    size = (64, 64)


class Explosions(NamedTuple):
    destroy_text = (
        "BOOM!",
        "DING!",
        "POP!",
        "NOPE!",
        "GOT'EM!",
        "SUP G?",
        "HA!",
        "BUST!",
        "SMH!",
    )

    ban_text = (
        "BANNED!",
        "KICKED!",
        "MUTED!",
        "PERMABANNED!",
        "DEFCON!",
        "SEE YOU LATER!",
        "HIPHOPIFIED!",
        "SMACK!",
    )


class Paths(NamedTuple):
    """
    Path objects that define the various
    paths we need to interact with for this
    project.
    """
    assets = Path("game", "assets")

    # assets subfolders
    music = assets / "music"
    sfx = assets / "sfx"
    graphics = assets / "graphics"
    fonts = assets / "fonts"

    # Graphics subfolders
    avatars = graphics / "avatars"
    effects = graphics / "effects"
    enemies = graphics / "enemies"
    headless = graphics / "headless"
    items = graphics / "items"
    levels = graphics / "levels"
    ui = graphics / "ui"
    splash = graphics / "splash"


class Words(NamedTuple):
    long = open(Paths.assets / "words_long.txt").read().strip().split("\n")
    single = open(Paths.assets / "words_single.txt").read().strip().split("\n")
