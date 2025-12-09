from __future__ import annotations

import os
import sys

# Ensure project root is in sys.path when running this file directly
if __name__ == "__main__":
    project_root = os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

import pygame
from typing import List
from AA.AA_scenes import gameScene
from AA.AA_scenes.sceneClass import Scene
from AA.AA_game import musicTrack, player
from AA.AA_utils import inputManager, musicManager, settings, countries, dbManager, timer


class RuleScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager,
                 dbManager: dbManager.DatabaseManager,
                 players: tuple[player.Player, player.Player]):
        super().__init__(mainApp, inputManager, musicManager, dbManager)

        # Asset base path
        self.players = players
        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")
        rules_dir = os.path.join(images_dir, "AA_rules")
        icon_dir = os.path.join(images_dir, "AA_input_instruction")

        self.bg_image = pygame.image.load(os.path.join(images_dir,
                                                       "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image,
                                               settings.WINDOW_SIZE)

        self._icons = {}
        for key, img in list(self._icons.items()):
            self._icons[key] = pygame.transform.scale(img, (150, 50))

        # Load scroll animation frames
        scroll_anim_dir = os.path.join(images_dir, "AA_scroll_anim")
        self._scroll_frames = []
        for i in range(48):
            frame_path = os.path.join(scroll_anim_dir, f"frame_{i:03d}.png")
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                frame = pygame.transform.scale(
                    frame,
                    (settings.WINDOW_SIZE[0], settings.WINDOW_SIZE[1] * 1.5))
                self._scroll_frames.append(frame)

        # Load sensei animation frames
        sensei_anim_dir = os.path.join(images_dir, "sensei_anim")
        self._sensei_frames = []
        for i in range(3):
            frame_path = os.path.join(sensei_anim_dir, f"tile00{i}.png")
            if os.path.exists(frame_path):
                frame = pygame.image.load(frame_path).convert_alpha()
                self._sensei_frames.append(frame)

        self._main_rule_image = pygame.transform.scale(
            pygame.image.load(os.path.join(rules_dir,
                                           "Règlement.png")).convert_alpha(),
            (settings.WINDOW_SIZE[0] - 500, settings.WINDOW_SIZE[1] - 100))
        self._rule_images = []
        for i in range(1, 8):
            rule_path = os.path.join(rules_dir, f"{i}.png")
            if os.path.exists(rule_path):
                rule_img = pygame.image.load(rule_path).convert_alpha()
                rule_img = pygame.transform.scale(
                    rule_img, (settings.WINDOW_SIZE[0] - 500,
                               settings.WINDOW_SIZE[1] - 100))
                self._rule_images.append(rule_img)

        # Scroll animation state
        self._current_frame_index = 0
        self._scroll_frame_duration = 0.06  # 80ms per frame
        self._animation_playing = False

        # Rule display state
        self._current_rule_index = 0
        self._rule_fade_duration = 0.5
        self._rule_display_duration = 3.0
        self._rule_phase = "idle"
        self._rule_alpha = 0
        # Main rule title fade (first time only)
        self._main_rule_alpha = 0
        self._main_rule_fade_done = False

        # Sensei animation state
        self._sensei_current_frame = 0
        self._sensei_frame_duration = 0.15  # 200ms per frame
        self._sensei_animation_active = False
        self._sensei_timer = timer.Timer()

    def _preload_cached_images(self):
        pass

    def _update_sensei_animation(self):
        """Update sensei animation frame if active"""
        if self._sensei_animation_active and self._sensei_frames:
            if self._sensei_timer.elapsed() >= self._sensei_frame_duration:
                self._sensei_current_frame = (self._sensei_current_frame + 1) % len(self._sensei_frames)
                self._sensei_timer.restart()
    def _draw_sensei(self):
        if self._sensei_frames:
            frame = self._sensei_frames[self._sensei_current_frame]
            # Position in bottom right with some padding
            rect = frame.get_rect(
                bottomright=(settings.WINDOW_SIZE[0] + 100, 
                           settings.WINDOW_SIZE[1] + 70))
            self._mainApp.blit(frame, rect)

    def initScene(self):
        super().initScene()
        if self._scroll_frames:
            self._animation_playing = True
            self._current_frame_index = 0
        else:
            self._animation_playing = False
            self._rule_phase = "fade_in"
            self._current_rule_index = 0
            self._rule_alpha = 0
            self._main_rule_alpha = 0
            self._main_rule_fade_done = False
        
        # Initialize sensei animation
        self._sensei_current_frame = 0
        self._sensei_animation_active = False
        self._stateTimer.restart()

    def loopScene(self, events: List[pygame.event.Event]):
        self._mainApp.blit(
            self.bg_image,
            self.bg_image.get_rect(center=self._mainApp.get_rect().center))

        center_x = settings.WINDOW_SIZE[0] // 2

        a_pressed = False
        for pid in range(2):
            presses = self._inputManager.getBtnsPressed(pid)
            if inputManager.ButtonInputs.A in presses:
                a_pressed = True
                break

        # Handle scroll animation
        if len(self._scroll_frames) > 0 and self._animation_playing:
            # If A pressed, skip scroll anim
            if a_pressed:
                self._animation_playing = False
                self._current_frame_index = len(self._scroll_frames) - 1

                self._rule_phase = "fade_in"
                self._current_rule_index = 0
                self._rule_alpha = 0

                self._main_rule_alpha = 0
                self._main_rule_fade_done = False
                self._sensei_animation_active = True
                self._sensei_timer.restart()
                self._stateTimer.restart()
            else:
                if self._stateTimer.elapsed() >= self._scroll_frame_duration:
                    self._current_frame_index += 1
                    self._stateTimer.restart()

                if self._current_frame_index < len(self._scroll_frames):
                    current_frame = self._scroll_frames[
                        self._current_frame_index]
                    self._mainApp.blit(current_frame, (0, -200))
                else:
                    self._current_frame_index = len(self._scroll_frames) - 1
                    self._animation_playing = False
                    self._rule_phase = "fade_in"
                    self._current_rule_index = 0
                    # Prepare main rule first-time fade
                    self._main_rule_alpha = 0
                    self._main_rule_fade_done = False
                    self._sensei_animation_active = True
                    self._sensei_timer.restart()
                    self._stateTimer.restart()

        elif self._rule_phase != "idle" and len(self._rule_images) > 0:

            if a_pressed:
                if self._rule_phase == "fade_in":
                    self._rule_phase = "display"
                    self._rule_alpha = 255
                    # If main rule hasn't finished its first fade yet, complete it now
                    if not self._main_rule_fade_done:
                        self._main_rule_alpha = 255
                        self._main_rule_fade_done = True
                    self._stateTimer.restart()
                elif self._rule_phase == "display" or self._rule_phase == "fade_out":
                    self._current_rule_index += 1
                    if self._current_rule_index < len(self._rule_images):
                        self._rule_phase = "fade_in"
                        self._rule_alpha = 0
                        # Do not reset main rule fade; it only fades once
                        self._stateTimer.restart()
                    else:
                        self.sceneFinished = True

            if not a_pressed:
                elapsed = self._stateTimer.elapsed()

                if self._rule_phase == "fade_in":
                    progress = min(1.0, elapsed / self._rule_fade_duration)
                    self._rule_alpha = int(255 * progress)
                    # First-time main rule fade
                    if not self._main_rule_fade_done:
                        self._main_rule_alpha = int(255 * progress)

                    if progress >= 1.0:
                        self._rule_phase = "display"
                        if not self._main_rule_fade_done:
                            self._main_rule_alpha = 255
                            self._main_rule_fade_done = True
                        self._stateTimer.restart()

                elif self._rule_phase == "display":
                    self._rule_alpha = 255
                    if not self._main_rule_fade_done:
                        self._main_rule_alpha = 255
                        self._main_rule_fade_done = True

                elif self._rule_phase == "fade_out":
                    progress = min(1.0, elapsed / self._rule_fade_duration)
                    self._rule_alpha = int(255 * (1.0 - progress))

                    if progress >= 1.0:
                        self._current_rule_index += 1
                        if self._current_rule_index < len(self._rule_images):
                            self._rule_phase = "fade_in"
                            self._rule_alpha = 0
                            # Main rule does not fade again
                            self._stateTimer.restart()
                        else:
                            print(
                                "All rules displayed. Transitioning to Game Scene."
                            )
                            self.sceneFinished = True

            if self._current_rule_index < len(self._rule_images):
                # Create a temporary surface with alpha channel for fading
                rule_surface = self._rule_images[
                    self._current_rule_index].copy()
                rule_rect = rule_surface.get_rect(
                    center=self._mainApp.get_rect().center)

                # Draw background elements
                if self._scroll_frames:
                    self._mainApp.blit(
                        self._scroll_frames[self._current_frame_index],
                        (0, -200))

                # Draw main rule image with first-time fade-in
                if self._main_rule_fade_done and self._main_rule_alpha >= 255:
                    self._mainApp.blit(self._main_rule_image,
                                       (rule_rect[0], rule_rect[1] - 50))
                else:
                    temp_title = pygame.Surface(
                        self._main_rule_image.get_size(), pygame.SRCALPHA)
                    temp_title.fill(
                        (255, 255, 255, max(0, min(255,
                                                   self._main_rule_alpha))))
                    temp_title.blit(self._main_rule_image, (0, 0),
                                    special_flags=pygame.BLEND_RGBA_MULT)
                    self._mainApp.blit(temp_title,
                                       (rule_rect[0], rule_rect[1] - 50))

                # Apply alpha to rule image via per-pixel multiply (no set_alpha)
                if self._rule_alpha < 255:
                    temp_surface = pygame.Surface(rule_surface.get_size(),
                                                  pygame.SRCALPHA)
                    temp_surface.fill((255, 255, 255, self._rule_alpha))
                    temp_surface.blit(rule_surface, (0, 0),
                                      special_flags=pygame.BLEND_RGBA_MULT)
                    self._mainApp.blit(temp_surface, rule_rect)
                else:
                    self._mainApp.blit(rule_surface, rule_rect)

        if self._sensei_animation_active:
            self._update_sensei_animation()
        self._draw_sensei()

        return super().loopScene(events)

    def getTransition(self):
        return gameScene.GameScene(self._mainApp, self._inputManager,
                                   self._musicManager, self._dbManager,
                                   musicTrack.GameTracks.SEMI_CHARMED_LIFE,
                                   self.players)


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    pygame.display.set_caption("Dance Dance to the Death - Rule Screen Test")
    clock = pygame.time.Clock()

    input_mgr = inputManager.InputManager([])
    music_mgr = musicManager.MusicManager()
    db = dbManager.DatabaseManager()
    player0 = player.Player("TES", countries.CountryOptions.QBC, 0, screen)
    cpu_player = player0
    track = musicTrack.GameTracks.SEMI_CHARMED_LIFE

    rule_scene = RuleScene(screen, input_mgr, music_mgr, db,
                           (player0, cpu_player))
    rule_scene.initScene()

    print("Rules Screen Test Mode")

    running = True
    while running and not rule_scene.sceneFinished:
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not rule_scene.loopScene(events):
            running = False

        pygame.display.flip()
        clock.tick(settings.FRAMERATE)

    pygame.quit()
    print("Rule screen test ended.")
