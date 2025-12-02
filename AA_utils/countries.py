from enum import Enum
import pygame, os, random
# from AA_utils import settings


class CountryFlags(Enum):
    Canada = "AA_images/Canada.png"
    Québec = "AA_images/Québec.png"
    USA = "AA_images/USA.png"


def getRandomCPUCountry(playerCountry: CountryFlags) -> CountryFlags:
    options = [c for c in CountryFlags if c != playerCountry]
    return random.choice(options)
