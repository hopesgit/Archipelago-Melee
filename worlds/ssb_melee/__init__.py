# from .MeleeClient import MeleeCommandProcessor
from typing import Mapping, Any, TextIO, Set, Optional

from .MeleeOptions import MeleeOptions
from .Items import item_table, fighters_table, events_table, progressive_table, SSBMeleeItem
from .Locations import *
from .Logic import get_goals
from .MeleeOptions import *
from .Regions import MeleeRegion
# from .classes.Event import EventRandomizer

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, icon_paths, launch_subprocess
from BaseClasses import CollectionState, List, Dict, Tutorial, MultiWorld, Item, Region, ItemClassification
from worlds.AutoWorld import World, WebWorld, LogicMixin
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
    items = item_table
    location_name_to_id = locations
    settings = MeleeSettings
    item_name_groups = {"Fighters": set(fighters_table.keys()), "Events": set(events_table.keys())}
    #event_rando = EventRandomizer
    goals: dict

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    ### I'm essentially just copying the methods from World in order to make them easier to understand and edit later
    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        super().stage_assert_generate(multiworld)

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

    def create_regions(self) -> None:
        from .Logic import has_all_star

        main_menu = Region(MeleeRegion.Menu.value, self.player, self.multiworld)
        main_menu.locations = generate_loc_objs(self.player, MeleeRegion.Menu.value, main_menu)
        main_menu.add_locations(bonus_location_table, MeleeLocation)

        adventure = Region(MeleeRegion.Adventure.value, self.player, self.multiworld)
        adventure.locations = generate_loc_objs(self.player, MeleeRegion.Adventure.value, adventure)
        main_menu.connect(adventure)

        all_star = Region(MeleeRegion.All_Star.value, self.player, self.multiworld)
        all_star.locations = generate_loc_objs(self.player, MeleeRegion.All_Star.value, all_star)
        main_menu.connect(all_star, "All Star Unlocked", lambda state: has_all_star(self.multiworld.state, self.player))

        classic = Region(MeleeRegion.Classic.value, self.player, self.multiworld)
        classic.locations = generate_loc_objs(self.player, MeleeRegion.Classic.value, classic)
        main_menu.connect(classic)

        event = Region(MeleeRegion.Event.value, self.player, self.multiworld)
        event.locations = generate_loc_objs(self.player, MeleeRegion.Event.value, event)
        main_menu.connect(event)

        self.multiworld.regions.append(main_menu)
        self.multiworld.regions.append(adventure)
        self.multiworld.regions.append(all_star)
        self.multiworld.regions.append(classic)
        self.multiworld.regions.append(event)

        victory = MeleeLocation(self.player, "Victory", None)
        victory.parent_region = main_menu
        victory.place_locked_item(SSBMeleeItem("Victory", ItemClassification.progression, None, self.player))


    def create_items(self) -> None:
        super().create_items()

    def set_rules(self) -> None:
        self.set_goals()

    def connect_entrances(self) -> None:
        super().connect_entrances()

    def generate_basic(self) -> None:
        super().generate_basic()

    # skipping fill_hook for now

    def post_fill(self) -> None:
        super().post_fill()

    def generate_output(self, output_directory: str) -> None:
        super().generate_output(output_directory)

    def fill_slot_data(self) -> Mapping[str, Any]:
        super().fill_slot_data()

    def extend_hint_information(self, hint_data: Dict[int, Dict[int, str]]):
        super().extend_hint_information(hint_data)

    def modify_multidata(self, multidata: Dict[str, Any]) -> None:
        super().modify_multidata(multidata)

    def write_spoiler_header(self, spoiler_handle: TextIO) -> None:
        super().write_spoiler_header(spoiler_handle)

    def write_spoiler_end(self, spoiler_handle: TextIO) -> None:
        super().write_spoiler_end(spoiler_handle)

    def write_spoiler(self, spoiler_handle: TextIO) -> None:
        super().write_spoiler(spoiler_handle)

    # def get_filler_item_name(self) -> str:
    #     from .Items import useful_items_table
    #     filler = tuple(useful_items_table.keys())
    #     return self.multiworld.random.choice(filler)

    def create_item(self, name: str) -> "Item":
        super().create_item(name)

    @classmethod
    def create_group(cls, multiworld: "MultiWorld", new_player_id: int, players: Set[int]) -> World:
        super().create_group(multiworld, new_player_id, players)

    def collect_item(self, state: "CollectionState", item: "Item", remove: bool = False) -> Optional[str]:
        super().collect_item(state, item, remove)

    # could use this to "give" the starting fighters (Mario, Bowser, Peach, etc.) until I eventually stop doing that
    def get_pre_fill_items(self) -> List["Item"]:
        super().get_pre_fill_items()

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        super().collect(state, item)


class MeleeLogicMixin(LogicMixin):
    def melee_test_method(self):
        pass