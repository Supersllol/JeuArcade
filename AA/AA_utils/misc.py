from __future__ import annotations

import pygame, math
from AA.AA_utils import settings


def placeSurfaceInHalf(playerID: int,
                       surface: pygame.Surface,
                       playerHalf: pygame.Surface,
                       p0Midtop: tuple[int, int],
                       mirror: bool = True):
    if playerID == 0:
        placement = surface.get_rect(midtop=p0Midtop)
    else:
        x, y = p0Midtop[0], p0Midtop[1]
        if mirror:
            placement = surface.get_rect(midtop=(playerHalf.get_width() - x,
                                                 y))
        else:
            placement = surface.get_rect(
                midtop=(x + (playerHalf.get_width() -
                             (settings.WINDOW_SIZE[0] / 2)), y))

    playerHalf.blit(surface, placement)


def pixelate_surface(surface, pixel_size):
    """Pixelate an entire surface BUT keep its size the same."""
    if pixel_size is None:
        pixel_size = 1
    pixel_size = max(1, int(pixel_size))

    w, h = surface.get_size()

    # avoid zero dimensions when scaling down
    small_w = max(1, w // pixel_size)
    small_h = max(1, h // pixel_size)

    # Scale down (keep alpha)
    small = pygame.transform.scale(surface, (small_w, small_h))
    # Scale back up (nearest neighbor) to produce the pixelated look
    pixelated = pygame.transform.scale(small, (w, h))

    return pixelated


def pixel_ring(color, radius, pixel_size=3, thickness=3):
    """Return a Surface (diam x diam, SRCALPHA) with a pixelated circle/ring drawn.

    - `color`: RGBA or RGB color used to draw the circle.
    - `center`: ignored for the returned surface (kept for signature compatibility).
    - `radius`: circle radius in pixels (int).
    - `pixel_size`: block size used for pixelation (1 = no pixelation).
    - `thickness`: 0 => filled circle, >0 => ring thickness (in final pixels).

    Usage:
        surf = pixel_ring(None, (255,0,0,255), (x,y), 20, pixel_size=4, thickness=2)
        screen.blit(surf, (x - 20, y - 20))
    """
    radius = int(max(0, radius))
    pixel_size = max(1, int(pixel_size))
    thickness = int(max(0, thickness))

    diam = radius * 2
    if diam == 0:
        # return a tiny transparent surface
        return pygame.Surface((0, 0), pygame.SRCALPHA)

    # Fast path: no pixelation (pixel_size <= 1)
    if pixel_size <= 1:
        out = pygame.Surface((diam, diam), pygame.SRCALPHA)
        out.fill((0, 0, 0, 0))
        if thickness <= 0:
            pygame.draw.circle(out, color, (radius, radius), radius)
        else:
            # draw outer then punch inner transparent circle for consistent ring
            pygame.draw.circle(out, color, (radius, radius), radius)
            inner_r = max(0, radius - thickness)
            if inner_r > 0:
                pygame.draw.circle(out, (0, 0, 0, 0), (radius, radius),
                                   inner_r)
        return out

    # Pixelated path: draw on a tiny surface then scale up with nearest neighbour
    small_size = max(1, math.ceil(diam / pixel_size))
    tiny = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
    tiny.fill((0, 0, 0, 0))
    tiny_center = (small_size // 2, small_size // 2)
    tiny_radius = small_size // 2

    # Draw outer filled circle on tiny surface
    pygame.draw.circle(tiny, color, tiny_center, tiny_radius)

    if thickness > 0:
        # scale thickness down to tiny-space
        scale = small_size / diam
        tiny_thickness = max(1, int(round(thickness * scale)))
        inner_r = tiny_radius - tiny_thickness
        if inner_r > 0:
            pygame.draw.circle(tiny, (0, 0, 0, 0), tiny_center, inner_r)

    # Scale up to exact diameter (nearest-neighbour) to get blocky look
    pixelated = pygame.transform.scale(tiny, (diam, diam))
    return pixelated


def rescaleSurface(surface: pygame.Surface, fixedCoords: tuple[None | int,
                                                               None | int]):
    width, height = surface.get_width(), surface.get_height()
    desiredWidth, desiredHeight = fixedCoords
    originalRatio = width / float(height)
    if desiredWidth and desiredHeight:
        return pygame.transform.smoothscale(
            surface, (desiredWidth, desiredHeight)).convert_alpha()
    if desiredWidth:
        return pygame.transform.smoothscale(
            surface,
            (desiredWidth, int(desiredWidth / originalRatio))).convert_alpha()
    if desiredHeight:
        return pygame.transform.smoothscale(surface, (int(
            desiredHeight * originalRatio), desiredHeight)).convert_alpha()
    return pygame.Surface((0, 0))
