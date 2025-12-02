import math
import pygame
from AA_utils import settings


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


def pixel_ring(surface, color, center, radius, pixel_size=3, thickness=3):
    """Draw a pixelated filled circle centered at `center` on `surface`.

    Implementation:
    - Render a filled circle on a tiny temporary surface (size = diameter / pixel_size)
    - Scale that tiny surface back up to the desired diameter with pygame.transform.scale
      (nearest-neighbour) so you get a blocky / pixelated circle with clean blocks.
    """
    radius = int(max(0, radius))
    pixel_size = max(1, int(pixel_size))
    if radius == 0:
        return

    diam = radius * 2

    # If pixel_size == 1, draw normally (no pixelation)
    if pixel_size <= 1:
        pygame.draw.circle(surface, color, (int(center[0]), int(center[1])),
                           radius, thickness)
        return

    # Compute small surface size (preserve aspect ratio; use ceil to avoid too small)
    small_size = max(1, math.ceil(diam / pixel_size))

    # Create tiny surface and draw a circle there
    tiny = pygame.Surface((small_size, small_size), pygame.SRCALPHA)
    tiny.fill((0, 0, 0, 0))
    tiny_radius = small_size // 2
    pygame.draw.circle(tiny, color, (tiny_radius, tiny_radius), tiny_radius,
                       thickness)

    # Scale up to the exact requested diameter using nearest-neighbour (pixelated look)
    pixelated = pygame.transform.scale(tiny, (diam, diam))

    # Blit centered at the requested position
    blit_x = int(center[0] - radius)
    blit_y = int(center[1] - radius)
    surface.blit(pixelated, (blit_x, blit_y))
