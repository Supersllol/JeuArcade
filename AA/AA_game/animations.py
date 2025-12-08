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

    @property
    def name(self):
        return self._name

    def getCurrentFrame(self):
        return self._frames[self._currentFrameID]

    def update(self):
        if self._timer.elapsed() > (1 / settings.ANIMATION_FPS):
            if self.isAnimationFinished():
                if self._loop:
                    self._currentFrameID = 0
                    self._timer.restart()
                else:
                    self._timer.stop()
            else:
                self._currentFrameID += 1
                self._timer.restart()

    def startAnimation(self, loop: bool):
        self._currentFrameID = 0
        self._timer.restart()
        self._loop = loop

    def isAnimationFinished(self):
        return self._currentFrameID == len(self._frames) - 1


def loadSpriteSheet(animation: PlayerAnimations, playerID: int):
    # load and scale the sheet to the correct height (use SPRITE_SIZE[1])
    suffix = ".png" if animation == PlayerAnimations.STAND else f"_{playerID}.png"
    name = animation.name + suffix
    sheet_path = os.path.join(settings.PARENT_PATH, "AA_images", "Animations",
                              name)
    spriteSheet = pygame.image.load(sheet_path)
    # get desired height from SPRITE_SIZE tuple
    desired_height = settings.SPRITE_SIZE[1]
    spriteSheet = misc.rescaleSurface(spriteSheet, (None, desired_height))

    frames: list[pygame.Surface] = []
    sheet_height = spriteSheet.get_height()
    sheet_width = spriteSheet.get_width()

    # number of frames (integer); if width is not multiple of height, use floor
    n_frames = sheet_width // sheet_height
    if n_frames == 0:
        raise ValueError(
            f"Sprite sheet {name} is too small (width {sheet_width}, height {sheet_height})"
        )

    for i in range(n_frames):
        # create an empty surface with alpha, blit the correct region from the sprite sheet
        frame = pygame.Surface((sheet_height, sheet_height), pygame.SRCALPHA)
        area = (i * sheet_height, 0, sheet_height, sheet_height)
        # blit the sheet onto the frame (source = spriteSheet)
        frame.blit(spriteSheet, (0, 0), area)
        frames.append(frame)

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
    # ULTIMATE = auto()
