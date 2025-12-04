from __future__ import annotations

from enum import Enum, auto
import pygame, os, random
from AA.AA_utils import settings, misc


class CountryOptions(Enum):
    CAN = "AA_images/CAN.png"
    QBC = "AA_images/QBC.png"
    TAN = "AA_images/TAN.png"
    PNG = "AA_images/PNG.png"
    USA = "AA_images/USA.png"


def getRandomCPUCountry(playerCountry: CountryOptions) -> CountryOptions:
    options = [c for c in CountryOptions if c != playerCountry]
    return random.choice(options)


def getCountryFlagSurface(country: CountryOptions):
    img = pygame.image.load(os.path.join(settings.PARENT_PATH, country.value))
    return misc.rescaleSurface(img, (settings.FLAG_WIDTH, None))
