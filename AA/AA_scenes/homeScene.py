from __future__ import annotations

import os
import sys

# Ensure parent directory is in sys.path when running this file directly
if __name__ == "__main__":
    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)

import pygame
import math
from typing import List

from AA.AA_scenes.sceneClass import Scene
from AA.AA_utils import inputManager, musicManager, settings


class HomeScene(Scene):

    def __init__(self, mainApp: pygame.Surface,
                 inputManager: inputManager.InputManager,
                 musicManager: musicManager.MusicManager):
        super().__init__(mainApp, inputManager, musicManager)

        # Asset base path
        images_dir = os.path.join(settings.PARENT_PATH, "AA_images")
        icon_dir = os.path.join(images_dir, "AA_input_instruction")

        # Load background and scale to window
        self.bg_image = pygame.image.load(os.path.join(images_dir, "dojo.jpg")).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, settings.WINDOW_SIZE)

        # Load title, scale, and anchor near top center
        self.title_image = pygame.image.load(os.path.join(images_dir, "Title.png")).convert_alpha()
        self.title_image = pygame.transform.scale(self.title_image, (700, 300))
        # Keep an original reference for crisp rescaling each frame
        self._title_base_image = self.title_image.copy()
        self._title_base_size = self._title_base_image.get_size()
        # Position title at the very top of the screen
        self.title_rect = self.title_image.get_rect(centerx=settings.WINDOW_SIZE[0] // 2, top=-20)

        self._icons = {
            "a": pygame.image.load(os.path.join(icon_dir, "Valider - A.png")).convert_alpha(),
            "select": pygame.image.load(os.path.join(icon_dir, "Quitter - Select.png")).convert_alpha(),
            "joystick": pygame.image.load(os.path.join(icon_dir, "Déplacer - Joystick.png")).convert_alpha()
        }
        # Scale input icons uniformly
        for key, img in list(self._icons.items()):
            self._icons[key] = pygame.transform.scale(img, (150, 50))

        # Heartbeat animation parameters
        self._heart_time = 0.0
        self._heart_bpm = 70  # beats per minute
        self._heart_scale_min = 1.0
        self._heart_scale_max = 1.10  # bump size
        self._heart_vertical_bump_px = 6  # slight vertical pop
        # Pattern: two quick pulses ("lub-dub") then rest
        self._heart_dub_spacing = 0.30  # seconds between the two pulses
        self._heart_pulse_width = 0.40  # width of each pulse in seconds

        # Load raw button images and normalize their sizes
        btn_images_raw = [
            pygame.image.load(os.path.join(images_dir, "Solo.png")).convert_alpha(),
            pygame.transform.scale(pygame.image.load(os.path.join(images_dir, "Face-a-Face.png")).convert_alpha(), (400, 200)),
            pygame.transform.scale(pygame.image.load(os.path.join(images_dir, "Record mondial.png")).convert_alpha(), (400, 200))
        ]

        # Scale all buttons to the same size
        self.btn_images = [
            pygame.transform.scale(img, (350, 100)) for img in btn_images_raw
        ]
        self.btn_size = self.btn_images[0].get_size()

        # Button labels + selection index
        self.btn_names = ["Solo", "Face à Face", "Record Mondial"]
        self.selected_index = 0
        
        # Vertical layout for buttons (start Y and spacing)
        self.btn_start_y = 380
        self.btn_spacing = 140
        
        # Animation values for selected button glow
        self.animation_time = 0
        self.glow_speed = 3  # Speed of pulsing effect

        # Preload cached images for performance
        self._preload_cached_images()

        # Cache indices for sequential access
        self._title_cache_index = 0
        self._glow_cache_index = 0

    def _preload_cached_images(self):

        self._title_cache = []
        seconds_per_beat = 60.0 / max(self._heart_bpm, 1)
        num_samples = 15

        base_w, base_h = self._title_base_size

        for i in range(num_samples):
            t = (i / num_samples) * seconds_per_beat
            hb_scale = self._heartbeat_scale(t)

            scaled_w = max(1, int(base_w * hb_scale))
            scaled_h = max(1, int(base_h * hb_scale))
            scaled_img = pygame.transform.smoothscale(self._title_base_image, (scaled_w, scaled_h))

            vertical_bump = int((hb_scale - self._heart_scale_min) /
                               (self._heart_scale_max - self._heart_scale_min + 1e-6) *
                               self._heart_vertical_bump_px)

            self._title_cache.append((scaled_img, vertical_bump))

        self._glow_cache = []
        glow_samples = 15
        width, height = self.btn_size
        glow_padding = 2

        for i in range(glow_samples):
            pulse = math.sin((i / glow_samples) * 2 * math.pi) * 0.5 + 0.5  # 0 to 1
            glow_intensity = int(pulse * 100 + 100)
            border_thickness = int(3 + pulse * 2)
            border_color = (255, 215, 0, glow_intensity)


            glow_surface = pygame.Surface((width + glow_padding * 2,
                                          height + glow_padding * 2),
                                         pygame.SRCALPHA)

            for layer in range(2):
                alpha = glow_intensity // (layer + 1)
                layer_offset = layer * border_thickness // 5
                glow_rect = pygame.Rect(layer_offset, layer_offset,
                                       width + glow_padding * 2 - layer_offset * 2,
                                       height + glow_padding * 2 - layer_offset * 2)
                pygame.draw.rect(glow_surface, (*border_color[:3], alpha), glow_rect,
                               border_thickness - layer)

            tint_overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            tint_color = (255, 215, 0, int(pulse * 40))
            tint_overlay.fill(tint_color)

            self._glow_cache.append((glow_surface, tint_overlay, glow_padding))

    def initScene(self):
        super().initScene()
        # Reset animation timer on scene init
        self.animation_time = 0
        self._heart_time = 0.0
        self._title_cache_index = 0
        self._glow_cache_index = 0
        # Play menu music if available? (Not requested yet)

    def _heartbeat_scale(self, t: float) -> float:
        # Compute lub-dub pulse strength between 0 and 1
        seconds_per_beat = 60.0 / max(self._heart_bpm, 1)
        # Time within the beat cycle
        phase = t % seconds_per_beat

        # Single pulse shaping function (Gaussian-like bump)
        def pulse(x: float, center: float, width: float) -> float:
            # Normalize distance from center
            d = (x - center) / max(width, 1e-6)
            # Sharp peak that falls off smoothly
            return math.exp(-d * d * 3.5)

        # First pulse at 0, second pulse shortly after
        p1 = pulse(phase, 0.0, self._heart_pulse_width)
        p2 = pulse(phase, self._heart_dub_spacing, self._heart_pulse_width)
        strength = max(p1, p2)

        # Map strength to scale range
        return self._heart_scale_min + (self._heart_scale_max - self._heart_scale_min) * strength

    def loopScene(self, events: List[pygame.event.Event]):
        # Advance animation time based on target FPS
        self.animation_time += 1 / settings.FRAMERATE
        self._heart_time += 1 / settings.FRAMERATE

        # Increment cache indices
        self._title_cache_index = (self._title_cache_index + 1) % len(self._title_cache)
        self._glow_cache_index = (self._glow_cache_index + 1) % len(self._glow_cache)

        # Input: navigate with up/down, confirm with A/Start
        for i in range(2): # Check both players
            new_axes = self._inputManager.getAxesActive(i, onlyCheckForNew=True)
            if inputManager.AxisInputs.Y_UP in new_axes:
                self.selected_index = (self.selected_index - 1) % len(self.btn_images)
            elif inputManager.AxisInputs.Y_DOWN in new_axes:
                self.selected_index = (self.selected_index + 1) % len(self.btn_images)
            
            new_btns = self._inputManager.getBtnsPressed(i, onlyCheckForNew=True)
            if inputManager.ButtonInputs.A in new_btns:
                # Trigger action
                print(f"Selected: {self.btn_names[self.selected_index]}")
                # TODO: Implement transition based on selection

        # Draw: background + title
        self._mainApp.blit(self.bg_image, (0, 0))

        # Use cached heartbeat title images - just get next frame
        self.title_image, vertical_bump = self._title_cache[self._title_cache_index]
        self.title_rect = self.title_image.get_rect(centerx=settings.WINDOW_SIZE[0] // 2, top=-20 - vertical_bump)

        self._mainApp.blit(self.title_image, self.title_rect)

        center_x = settings.WINDOW_SIZE[0] // 2
        
        for i, img in enumerate(self.btn_images):
            is_selected = i == self.selected_index
            
            # Compute rect position for this button
            y_pos = self.btn_start_y + (i * self.btn_spacing)
            rect = img.get_rect(centerx=center_x, centery=y_pos)

            # If selected, use cached glow effects
            if is_selected:
                # Get cached glow - just use next frame
                glow_surface, tint_overlay, glow_padding = self._glow_cache[self._glow_cache_index]

                # Blit cached glow
                glow_pos = (rect.x - glow_padding, rect.y - glow_padding)
                self._mainApp.blit(glow_surface, glow_pos)
                
                # Add cached tint overlay to the button
                tint_surface = img.copy()
                tint_surface.blit(tint_overlay, (0, 0))
                
                self._mainApp.blit(tint_surface, rect)
            else:
                self._mainApp.blit(img, rect)

        # Button input instructions at bottom
        # A input
        self._mainApp.blit(self._icons["joystick"], (40, settings.WINDOW_SIZE[1] - 180))
        # Select input
        self._mainApp.blit(self._icons["a"], (45, settings.WINDOW_SIZE[1] - 120))
        # Joystick input
        self._mainApp.blit(self._icons["select"], (30, settings.WINDOW_SIZE[1] - 60))

        return super().loopScene(events)

    def getTransition(self):
        # Default transition passthrough
        return super().getTransition()


# Standalone test harness
if __name__ == "__main__":
    # Initialize pygame
    pygame.init()
    screen = pygame.display.set_mode(settings.WINDOW_SIZE)
    pygame.display.set_caption("Dance Dance to the Death - Home Screen Test")
    clock = pygame.time.Clock()
    
    # Create dummy managers for testing
    # InputManager needs a list of joysticks (empty list defaults to keyboard)
    input_mgr = inputManager.InputManager([])  # Empty list = keyboard mode
    music_mgr = musicManager.MusicManager()  # No arguments needed
    
    # Create home scene
    home_scene = HomeScene(screen, input_mgr, music_mgr)
    home_scene.initScene()
    
    # Main loop
    running = True
    print("Home Screen Test Mode")
    print("Controls: Arrow keys (UP/DOWN) to navigate, ENTER/SPACE to select, ESC to quit")
    
    while running:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Run scene loop
        if not home_scene.loopScene(events):
            running = False
        
        # Update display
        pygame.display.flip()
        clock.tick(settings.FRAMERATE)
    
    pygame.quit()
    print("Home screen test ended.")
