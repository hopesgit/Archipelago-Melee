# from .MeleeClient import MeleeCommandProcessor
from typing import Mapping, Any, TextIO, Set, Optional

from .MeleeOptions import MeleeOptions
from .Items import item_table, fighters_table, events_table, progressive_table, SSBMeleeItem, useful_items_table
from .Locations import *
from .Logic import get_options
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
        md5s = ["0e63d4223b01d9aba596259dc155a174"]


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
    bug_report_page = 'https://github.com/hopesgit/Archipelago-Melee/issues'


class SSBMeleeWorld(World):
    """Super Smash Bros. Melee is a platform fighter party game released in 2001 for the Nintendo GameCube.
    Players can choose any of a handful of Nintendo characters and duke it out in Single- or Multiplayer modes."""
    options_dataclass = MeleeOptions
    options = MeleeOptions
    game = "Super Smash Bros Melee"
    web = SSBMeleeWeb()
    settings = MeleeSettings
    required_client_version = (0, 6, 1)

    origin_region_name = "Main Menu"
    item_name_to_id = {name: data.code for name, data in item_table.items()}
    items = item_table
    item_pool = []
    location_name_to_id = locations
    item_name_groups = {"Fighters": set(fighters_table.keys()), "Events": set(events_table.keys())}
    location_name_groups = {
        "Classic": set(classic_location_table),
        "Adventure": set(adventure_location_table),
        "All-Star": set(all_star_location_table),
        "Total Score": set(total_score_table),
        "Events": set(event_location_table),
        "Special Bonuses": set(bonus_location_table)
    }

    opt_events_goal: bool
    opt_excluded_events: List[int | None]
    opt_progressive_events: bool
    opt_shuffle_events: int
    opt_classic_goal: bool
    opt_classic_total_goal: int
    opt_adv_goal: bool
    opt_adv_total_goal: int
    opt_all_star_goal: bool
    opt_all_star_total_goal: int
    opt_trophy_goal: int
    opt_excluded_fighters: List[str]
    opt_shuffle_starters: bool
    opt_starting_fighter: Set[Dict[str, int]]

    #events_rando = EventRandomizer()

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)

    ### I'm essentially just copying the methods from World in order to make them easier to understand and edit later
    @classmethod
    def stage_assert_generate(cls, multiworld: "MultiWorld") -> None:
        super().stage_assert_generate(multiworld)

    def events_are_progressive(self):
        prog = self.opt_progressive_events
        if prog:
            self.item_name_groups["Events"] = set(progressive_table.keys())
            for item in self.item_name_to_id:
                if item[0].startswith("Event Gate"):
                   del self.item_name_to_id[item[0]]

    def shuffle_starting_fighters(self):
        fighters = []
        starters = ["Mario", "Peach", "Bowser", "Yoshi", "Ice Climbers",
                      "Captain Falcon", "Ness", "Donkey Kong", "Fox", "Samus",
                      "Kirby", "Zelda/Sheik", "Link", "Pikachu"]
        for s in starters:
            fighters.append(self.create_item(s))

        if not self.opt_shuffle_starters:
            for item in fighters:
                item_name = item
                self.multiworld.push_precollected(item_name)
        else:
            choice = self.random.choice(fighters)
            self.multiworld.push_precollected(choice)


    def set_class_attrs_from_options(self):
        opts = get_options(self.multiworld.state, self.player)
        self.opt_events_goal = opts["events_goal"]
        self.opt_excluded_events = opts["excluded_events"]
        self.opt_progressive_events = opts["progressive_events"]
        self.opt_shuffle_events = opts["shuffle_events"]
        self.opt_classic_goal = opts["classic_goal"]
        self.opt_classic_total_goal = opts["classic_total"]
        self.opt_adv_goal = opts["adventure_goal"]
        self.opt_adv_total_goal = opts["adventure_total"]
        self.opt_all_star_goal = opts["all_star_goal"]
        self.opt_all_star_total_goal = opts["all_star_total"]
        self.opt_trophy_goal = opts["trophy_goal"]
        self.opt_shuffle_starters = opts["shuffle_starters"]
        self.opt_starting_fighter = opts["starting_fighter"]
        if len(self.opt_starting_fighter) > 1: raise KeyError('Option "Starting Fighter" does not support selecting multiple choices.')

    def generate_early(self) -> None:
        self.set_class_attrs_from_options()
        # self.set_goals()
        self.events_are_progressive()
        self.shuffle_starting_fighters()

    def create_regions(self) -> None:
        from .Logic import has_all_star

        main_menu = Region(MeleeRegion.Menu.value, self.player, self.multiworld, hint="Special Bonuses can be gained in 1p and Vs, so be careful!")
        # main_menu.locations = generate_loc_objs(self.player, MeleeRegion.Menu.value, main_menu)

        adventure = Region(MeleeRegion.Adventure.value, self.player, self.multiworld, hint="Complete various tasks in Adventure Mode!")
        adventure.locations = generate_loc_objs(self.player, MeleeRegion.Adventure.value, adventure)
        main_menu.connect(adventure)

        all_star = Region(MeleeRegion.All_Star.value, self.player, self.multiworld, hint="Complete various tasks in All-Star Mode!")
        all_star.locations = generate_loc_objs(self.player, MeleeRegion.All_Star.value, all_star)
        main_menu.connect(all_star, "All Star Unlocked", lambda state: has_all_star(self.multiworld.state, self.player))

        classic = Region(MeleeRegion.Classic.value, self.player, self.multiworld, hint="Complete various tasks in Classic Mode!")
        classic.locations = generate_loc_objs(self.player, MeleeRegion.Classic.value, classic)
        main_menu.connect(classic)

        event = Region(MeleeRegion.Event.value, self.player, self.multiworld, hint="Complete the events in Event Match!")
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


    def get_filler_item_name(self) -> str:
        filler_items: List[str] = [name for name, data in useful_items_table.items()]
        return self.random.choice(filler_items)

    # def set_goals(self): -> None:


    def set_rules(self) -> None:
        super().set_rules()

    def generate_basic(self) -> None:
        super().generate_basic()

    # def pre_fill(self) -> None:

    def fill_hook(self,
                  progitempool: List["Item"],
                  usefulitempool: List["Item"],
                  filleritempool: List["Item"],
                  fill_locations: List["Location"]) -> None:
        super().fill_hook(progitempool, usefulitempool, filleritempool, fill_locations)
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

    def create_item(self, name: str) -> "Item":
        return Item(name, ItemClassification.progression, None, self.player)

    @classmethod
    def create_group(cls, multiworld: "MultiWorld", new_player_id: int, players: Set[int]) -> World:
        super().create_group(multiworld, new_player_id, players)

    def collect_item(self, state: "CollectionState", item: "Item", remove: bool = False) -> Optional[str]:
        super().collect_item(state, item, remove)

    def collect(self, state: "CollectionState", item: "Item") -> bool:
        super().collect(state, item)


class MeleeLogicMixin(LogicMixin):
    def melee_test_method(self):
        pass