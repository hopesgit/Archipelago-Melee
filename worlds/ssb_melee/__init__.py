# from .MeleeClient import MeleeCommandProcessor
from .MeleeOptions import MeleeOptions
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, icon_paths, launch_subprocess
from .Items import item_table, fighters_table, events_table, progressive_table
from .Locations import locations
from .Logic import get_goals
# from .classes.Event import EventRandomizer

from BaseClasses import CollectionState, List, Dict, Tutorial, MultiWorld
from worlds.AutoWorld import World, WebWorld
from .MeleeOptions import *
import settings


def run_client() -> None:
    """
    Launch the Super Smash Bros Melee client.
    """
    print("Running Super Smash Bros. Melee client.")
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
    class IsoFile(settings.UserFilePath):
        """Path of the Melee .iso file to use."""
        description = "Super Smash Bros. Melee US Revision 2 .iso file"  # displayed in the file browser
        copy_to = "melee.iso"

    iso_file: IsoFile = IsoFile("melee.iso")

    class AutoStart(str):
        """Auto-start the iso when clicked."""
        default = 'true'

    auto_start = AutoStart


class SSBMeleeWeb(WebWorld):
    tutorials = [
        Tutorial(
            "Multiworld Setup Guide",
            "A guide to setting up Super Smash Bros Melee for Archipelago Multiworld",
            "English",
            "setup.md",
            "setup/en",
            ["Kenna Puppers"]
        )
    ]
    theme="partyTime"
    option_groups = option_groups()


class SSBMeleeWorld(World):
    """Super Smash Bros. Melee is a platform fighter party game released in 2001 for the Nintendo GameCube.
    Players can choose any of a handful of Nintendo characters and duke it out in Single- or Multiplayer modes."""
    options_dataclass = MeleeOptions
    options = MeleeOptions
    game = "Super Smash Bros Melee"
    web = SSBMeleeWeb()
    origin_region_name = "Main Menu"
    required_client_version = (0, 6, 1)
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = locations
    settings = MeleeSettings
    item_name_groups = {"Fighters": set(fighters_table.keys()), "Events": set(events_table.keys())}
    #event_rando = EventRandomizer
    goals: dict

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        pass

    def set_goals(self):
        ctx = self.multiworld.state
        player = self.player
        self.goals = get_goals(ctx, player)

    def events_are_progressive(self):
        prog = self.options.progressive_events.value
        if prog == 1:
            self.item_name_groups["Events"] = set(progressive_table.keys())
            for item in self.item_name_to_id:
                if item[0].startswith("Event Gate"):
                   del self.item_name_to_id[item[0]]


    def generate_early(self) -> None:
        self.events_are_progressive()

    def create_regions(self):
        from .Regions import get_regions
        return get_regions(self.multiworld.worlds[self.player], self.player)