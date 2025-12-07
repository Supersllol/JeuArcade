from __future__ import annotations

from enum import Enum, auto
import pygame, os, random
from AA.AA_utils import settings, misc


class CountryOptions(Enum):
    CAN = "AA_images/Pays/CAN.png"
    QBC = "AA_images/Pays/QBC.png"
    TAN = "AA_images/Pays/TAN.png"
    PNG = "AA_images/Pays/PNG.png"
    USA = "AA_images/Pays/USA.png"
    COR = "AA_images/Pays/COR.png"
    DAN = "AA_images/Pays/DAN.png"
    IRA = "AA_images/Pays/IRA.png"
    MAD = "AA_images/Pays/MAD.png"
    VAT = "AA_images/Pays/VAT.png"


def getRandomCPUCountry(playerCountry: CountryOptions) -> CountryOptions:
    options = [c for c in CountryOptions if c != playerCountry]
    return random.choice(options)


def getCountryFlagSurface(country: CountryOptions):
    img = pygame.image.load(os.path.join(settings.PARENT_PATH, country.value))
    return misc.rescaleSurface(img, (settings.FLAG_WIDTH, None))
