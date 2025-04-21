# from .MeleeClient import MeleeCommandProcessor
from .MeleeOptions import MeleeOptions
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, icon_paths, launch_subprocess
from .Items import item_table
from .Locations import locations
# from .Logic import get_goals
from .classes.Event import EventRandomizer

from BaseClasses import CollectionState, List, Dict
from Options import PerGameCommonOptions
from worlds.AutoWorld import World
import settings


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


class MeleeSettings(settings.Group):
    class IsoFile(settings.SNESRomPath):
        """Path of the Melee .iso file to use."""
        description = "Super Smash Bros. Melee US Revision 2 .iso file"  # displayed in the file browser
        copy_to = "melee.iso"  # instead of storing the path, copy to AP dir
        crc32 = "5365c84b"
        sha1 = "d4e70c064cc714ba8400a849cf299dbd1aa326fc"
        sha5 = "0e63d4223b01d9aba596259dc155a174"

    iso_file: IsoFile = IsoFile("MyGame.sfc")  # definition and default value

    class AutoStart(settings.Bool):
        """Auto-start the iso when clicked."""
        default = True

    auto_start = AutoStart


class SSBMeleeWorld(World):
    """Super Smash Bros. Melee is a platform fighter party game released in 2001 for the Nintendo GameCube.
    Players can choose any of a handful of Nintendo characters and duke it out in Single- or Multiplayer modes."""
    options_dataclass = MeleeOptions
    options = MeleeOptions
    game = "Super Smash Bros. Melee"
    topology_present = False #defaults to false
    origin_region_name = "Main Menu"
    required_client_version = (0, 6, 1)
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = locations
    #completion_condition = get_goals()
    settings = MeleeSettings
    event_rando = EventRandomizer

    def override_item_classifications(self):
        pass




# client = MeleeCommandProcessor()
    
