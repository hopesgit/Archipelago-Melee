from enum import Enum
from BaseClasses import Region


class MeleeRegion(Enum):
    Menu = "Main Menu"
    Adventure = "1P Adventure Mode"
    All_Star = "1P All-Star Mode"
    Classic = "1P Classic Mode"
    Event = "1P Event Mode"
    Trophies = "Trophies"
    Vs = "MP Versus Mode"

def get_regions(world: 'SSBMeleeWorld', player: int):
    region_names = MeleeRegion
    regions = list()
    for name in region_names:
        region = Region(name, player, world)
        regions.append(region)
    return regions
''