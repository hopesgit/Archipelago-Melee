import worlds.ssb_melee.classes.Adventure as Adventure
import worlds.ssb_melee.classes.AllStar as AllStar
import worlds.ssb_melee.classes.Character as Character
import worlds.ssb_melee.classes.Classic as Classic
import worlds.ssb_melee.classes.Event as Event
import worlds.ssb_melee.classes.Gecko as Gecko
import worlds.ssb_melee.classes.Locations as Locations
import MeleeClient
from .MeleeClient import MeleeCommandProcessor
from .MeleeOptions import SSBMeleeOptions
import Regions
import worlds.ssb_melee.classes.Trophies as Trophies
import Patcher
import worlds.ssb_melee.classes.Vs as Vs

import pathlib
import os
import ppc_asm as ppc #package for working with PowerPC architecture (Nintendo GameCube)
import dolphin_memory_engine as dme #memory explorer software for Dolphin
import BaseClasses
from Options import PerGameCommonOptions
from worlds.AutoWorld import World

class SSBMeleeWorld(World):
    """Super Smash Bros Melee is a platform fighter released in 2001 for the Nintendo GameCube.
    Players can choose any of a handful of Nintendo characters and duke it out in Single- or Multiplayer modes."""
    options_dataclass = SSBMeleeOptions
    options = SSBMeleeOptions
    game = "Super Smash Bros. Melee"
    topology_present = False #defaults to false
    origin_region_name = "Main Menu"

# client = MeleeCommandProcessor()
    
