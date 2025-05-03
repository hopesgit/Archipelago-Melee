import typing
from enum import Enum
from BaseClasses import Region
if typing.TYPE_CHECKING:
    from . import SSBMeleeWorld


class MeleeRegion(Enum):
    Menu = "Main Menu"
    Adventure = "1P Adventure Mode"
    All_Star = "1P All-Star Mode"
    Classic = "1P Classic Mode"
    Event = "1P Event Match"
    HRC = "Home-Run Contest"
    Target_Test = "Target Test"
    Multi_Man = "Multi-Man Melee"
    Trophies = "Trophies/Lottery"
    Vs = "Vs Mode"


def get_regions(world: 'SSBMeleeWorld'):
    region_names = MeleeRegion
    regions = list()
    for item in region_names:
        region = Region(item.value, world.player, world.multiworld)
        regions.append(region)
    return regions