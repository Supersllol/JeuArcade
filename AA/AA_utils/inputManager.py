from __future__ import annotations

import pygame
from enum import Enum, auto


# Enumerations for logical button names (mapped to keyboard or joystick indices)
class ButtonInputs(Enum):
    A = 0
    B = 1
    C = 2
    D = 3
    L1 = 4
    R1 = 5
    L2 = 6
    R2 = 7
    START = 8
    SELECT = 9


moveBindings = {
    0: ButtonInputs.A,
    1: ButtonInputs.B,
    2: ButtonInputs.C,
    3: ButtonInputs.D
}


# Enumerations for directional axes used by the input system
class AxisInputs(Enum):
    X_LEFT = auto()
    X_RIGHT = auto()
    Y_UP = auto()
    Y_DOWN = auto()


class InputManager:
    """Central input manager that normalizes keyboard and joystick input
    for up to two players. Provides utilities to query newly pressed buttons
    and active axes.
    """

    # Default keyboard mappings for two players. Keys map to ButtonInputs or AxisInputs.
    _playerKeyboards = ({
        ButtonInputs.A: pygame.K_u,
        ButtonInputs.B: pygame.K_j,
        ButtonInputs.D: pygame.K_k,
        ButtonInputs.L1: pygame.K_LEFT,
        ButtonInputs.R1: pygame.K_RIGHT,
        ButtonInputs.R2: pygame.K_i,
        ButtonInputs.START: pygame.K_o,
        ButtonInputs.SELECT: pygame.K_p,
        AxisInputs.X_LEFT: pygame.K_LEFT,
        AxisInputs.X_RIGHT: pygame.K_RIGHT,
        AxisInputs.Y_UP: pygame.K_UP,
        AxisInputs.Y_DOWN: pygame.K_DOWN,
    }, {
        ButtonInputs.A: pygame.K_q,
        ButtonInputs.B: pygame.K_z,
        ButtonInputs.D: pygame.K_x,
        ButtonInputs.L1: pygame.K_a,
        ButtonInputs.R1: pygame.K_d,
        ButtonInputs.R2: pygame.K_e,
        ButtonInputs.START: pygame.K_r,
        ButtonInputs.SELECT: pygame.K_t,
        AxisInputs.X_LEFT: pygame.K_a,
        AxisInputs.X_RIGHT: pygame.K_d,
        AxisInputs.Y_UP: pygame.K_w,
        AxisInputs.Y_DOWN: pygame.K_s,
    })

    def __init__(self, joysticks: list[pygame.joystick.JoystickType]):
        # store connected joysticks for use as controller input
        self._joysticks = joysticks

        # keep previous button states per player to detect new presses
        self._playersPrevBtnStates = tuple(
            {btn: False
             for btn in ButtonInputs} for i in range(2))

        # keep previous axis states per player (boolean active/inactive)
        self._playersPrevAxisStates = tuple(
            {axis: False
             for axis in AxisInputs} for i in range(2))

        # fall back to keyboard input if no joysticks were provided
        self._usingKeyboard = True if len(joysticks) == 0 else False

    def _checkAxisValue(self, axis: AxisInputs,
                        joystick: pygame.joystick.JoystickType):
        """Read a joystick axis and return True if it crosses a threshold
        in the requested direction. Thresholds are hard-coded (~0.75).
        """
        if axis == AxisInputs.X_LEFT:
            return joystick.get_axis(0) < -0.75
        if axis == AxisInputs.X_RIGHT:
            return joystick.get_axis(0) > 0.75
        if axis == AxisInputs.Y_DOWN:
            return joystick.get_axis(1) < -0.75
        if axis == AxisInputs.Y_UP:
            return joystick.get_axis(1) > 0.75

    def update(self):
        """Poll current input state and store it as 'previous' for the next frame.
        Call once per frame after querying getBtnsPressed/getAxesActive to ensure
        edge detection works correctly.
        """
        for player in range(2):
            # load previous states
            playerPrevBtnStates = self._playersPrevBtnStates[player]
            playerPrevAxisStates = self._playersPrevAxisStates[player]

            if self._usingKeyboard:
                # read keyboard state and update stored previous states
                keys = pygame.key.get_pressed()
                keyboard = self._playerKeyboards[player]
                for button in ButtonInputs:
                    if button not in keyboard:
                        continue
                    playerPrevBtnStates[button] = keys[keyboard[button]]
                for axis in AxisInputs:
                    if axis not in keyboard:
                        continue
                    playerPrevAxisStates[axis] = keys[keyboard[axis]]
                continue

            # if using joysticks, ensure a joystick exists for this player
            if (len(self._joysticks) - 1) < player:
                continue
            joystick = self._joysticks[player]
            for button in ButtonInputs:
                # store current button boolean state
                playerPrevBtnStates[button] = joystick.get_button(button.value)
            for axis in AxisInputs:
                # evaluate axis threshold and store boolean active/inactive
                playerPrevAxisStates[axis] = self._checkAxisValue(
                    axis, joystick)

    def getBtnsPressed(self, playerID: int, onlyCheckForNew: bool = True):
        """Return a list of ButtonInputs that are currently pressed.
        If onlyCheckForNew is True, only return buttons that became pressed
        since the last update() call (rising edge detection).
        """
        pressedBtns = []
        for button in ButtonInputs:
            current = False
            prev = False
            if self._usingKeyboard:
                keyboard = self._playerKeyboards[playerID]
                if button not in keyboard:
                    continue
                keys = pygame.key.get_pressed()
                current = keys[keyboard[button]]
                prev = self._playersPrevBtnStates[playerID][button]
            else:
                if (len(self._joysticks) - 1) < playerID:
                    return []
                joystick = self._joysticks[playerID]
                current = joystick.get_button(button.value)
                prev = self._playersPrevBtnStates[playerID][button]

            # add to result if currently pressed and either was not pressed
            # previously (new press) or we allow repeating
            if current and (not prev or not onlyCheckForNew):
                pressedBtns.append(button)

        return pressedBtns

    def getAxesActive(self, playerID: int, onlyCheckForNew: bool = True):
        """Return a list of AxisInputs that are currently active (e.g., left/right/up/down).
        If onlyCheckForNew is True, only return axes that became active since the last update().
        """
        activeAxes = []
        for axis in AxisInputs:
            current = False
            prev = False
            if self._usingKeyboard:
                keyboard = self._playerKeyboards[playerID]
                if axis not in keyboard:
                    continue
                keys = pygame.key.get_pressed()
                current = keys[self._playerKeyboards[playerID][axis]]
                prev = self._playersPrevAxisStates[playerID][axis]
            else:
                if (len(self._joysticks) - 1) < playerID:
                    return []
                joystick = self._joysticks[playerID]
                current = self._checkAxisValue(axis, joystick)
                prev = self._playersPrevAxisStates[playerID][axis]

            if current and (not prev or not onlyCheckForNew):
                activeAxes.append(axis)

        return activeAxes
