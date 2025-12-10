from __future__ import annotations

import os, pygame
from enum import Enum, auto
from AA.AA_utils import settings, misc, timer


class Animation:

    def __init__(self, frames: list[pygame.Surface], name: PlayerAnimations):
        self._frames = frames
        self._timer = timer.Timer()
        self._currentFrameID = 0
        self._loop = False
        self._name = name
        self._returnToDefault = False

    @property
    def name(self):
        return self._name

    def getCurrentFrame(self):
        return self._frames[self._currentFrameID]

    def update(self):
        if self.isAnimationFinished():
            if self._loop:
                self._currentFrameID = 0
                self._timer.restart()

        elif self._timer.elapsed() > (1 / settings.ANIMATION_FPS):
            self._currentFrameID += 1
            self._timer.restart()

    def startAnimation(self, loop: bool, returnToDefault=False):
        self._currentFrameID = 0
        self._timer.restart()
        self._loop = loop
        self._returnToDefault = returnToDefault

    def isAnimationFinished(self):
        return (self._currentFrameID == len(self._frames) -
                1) and (self._timer.elapsed() > (1 / settings.ANIMATION_FPS))


def loadFromFolder(folderPath: str, animationName: PlayerAnimations):
    frames: list[pygame.Surface] = []
    for i in range(25):
        frame_path = os.path.join(folderPath, f"tile{i:03d}.png")
        if os.path.exists(frame_path):
            frame = misc.rescaleSurface(pygame.image.load(frame_path),
                                        (None, settings.SPRITE_SIZE[1]))
            frames.append(frame)
    return Animation(frames, animationName)


def loadSpriteSheet(animation: PlayerAnimations, playerID: int):
    if animation == PlayerAnimations.EMPTY:
        return Animation([pygame.Surface((0, 0))], animation)
    if animation == PlayerAnimations.HADOKEN:
        return loadFromFolder(
            os.path.join(settings.PARENT_PATH, "AA_images", "Animations",
                         f"HADOKEN_{playerID}"), PlayerAnimations.HADOKEN)
    # load the sheet (get original size first to support non-square frames)
    suffix = ".png" if animation in (
        PlayerAnimations.STAND, PlayerAnimations.DANCE_0,
        PlayerAnimations.DANCE_1, PlayerAnimations.DANCE_2,
        PlayerAnimations.DANCE_3) else f"_{playerID}.png"
    name = animation.name + suffix
    sheet_path = os.path.join(settings.PARENT_PATH, "AA_images", "Animations",
                              name)

    spriteSheet = pygame.image.load(sheet_path)
    orig_w, orig_h = spriteSheet.get_width(), spriteSheet.get_height()

    # get desired height from SPRITE_SIZE tuple and rescale the sheet
    desired_height = settings.SPRITE_SIZE[1]
    spriteSheet = misc.rescaleSurface(spriteSheet, (None, desired_height))

    # decide per-frame original width (in source pixels) for animations that aren't square
    # (HADOKEN frames are 625x300 in your assets). Add other exceptions here if needed.

    orig_frame_w = orig_h  # default: square frames (width == height)

    # compute scaled frame width after rescale
    scale = spriteSheet.get_height() / float(orig_h) if orig_h != 0 else 1.0
    frame_w = max(1, int(round(orig_frame_w * scale)))

    sheet_height = spriteSheet.get_height()
    sheet_width = spriteSheet.get_width()

    n_frames = sheet_width // frame_w
    if n_frames == 0:
        raise ValueError(
            f"Sprite sheet {name} is too small (width {sheet_width}, height {sheet_height})"
        )

    frames: list[pygame.Surface] = []
    for i in range(n_frames):
        frame = pygame.Surface((frame_w, sheet_height), pygame.SRCALPHA)
        area = (i * frame_w, 0, frame_w, sheet_height)
        frame.blit(spriteSheet, (0, 0), area)
        frames.append(frame.convert_alpha())

    return Animation(frames, animation)


class AnimationManager:

    def __init__(self):
        self._playerAnimations: list[dict[PlayerAnimations, Animation]] = []
        for i in range(2):
            animations = {
                anim: loadSpriteSheet(anim, i)
                for anim in list(PlayerAnimations)
            }
            self._playerAnimations.append(animations)

    def getAnimation(self, animation: PlayerAnimations, playerID: int):
        return self._playerAnimations[playerID][animation]


class PlayerAnimations(Enum):
    STAND = auto()
    TURN_SIDE = auto()
    TURN_FRONT = auto()
    TURN_AROUND = auto()
    WALK = auto()
    FIGHT = auto()
    DAMAGE = auto()
    DEAD = auto()
    PUNCH = auto()
    KICK = auto()
    DOUBLE_PUNCH = auto()
    HADOKEN = auto()
    DANCE_0 = auto()
    DANCE_1 = auto()
    DANCE_2 = auto()
    DANCE_3 = auto()
    EMPTY = auto()


danceMoves = [
    PlayerAnimations.DANCE_0, PlayerAnimations.DANCE_1,
    PlayerAnimations.DANCE_2, PlayerAnimations.DANCE_3
]
