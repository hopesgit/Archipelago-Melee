# from .MeleeClient import MeleeCommandProcessor
from .MeleeOptions import MeleeOptions
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, icon_paths, launch_subprocess
from .Items import item_table
from .Locations import locations

import BaseClasses
from Options import PerGameCommonOptions
from worlds.AutoWorld import World

def run_client() -> None:
    """
    Launch the Super Smash Bros Melee client.
    """
    print("Running Super Smash Bros Melee client.")
    from .MeleeClient import main

    launch_subprocess(main, name="MeleeClient")

components.append(
    Component(
        "Super Smash Bros. Melee Client",
        func=run_client,
        component_type=Type.CLIENT,
        file_identifier=SuffixIdentifier(".apssbm"),
        icon="Melee",
    )
)
icon_paths["Melee"] = "ap:worlds.ssb_melee/img/melee.png"

class SSBMeleeWorld(World):
    """Super Smash Bros. Melee is a platform fighter released in 2001 for the Nintendo GameCube.
    Players can choose any of a handful of Nintendo characters and duke it out in Single- or Multiplayer modes."""
    options_dataclass = MeleeOptions
    options = MeleeOptions
    game = "Super Smash Bros. Melee"
    topology_present = False #defaults to false
    origin_region_name = "Main Menu"
    # required_client_version = "0.6.1"
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = locations


# client = MeleeCommandProcessor()
    
