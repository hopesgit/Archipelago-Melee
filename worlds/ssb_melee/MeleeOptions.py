from enum import Enum
from Options import DeathLink, DefaultOnToggle, OptionDict, OptionList, TextChoice, Toggle, Range, ItemDict, \
    StartInventoryPool, Choice, PerGameCommonOptions, Visibility, OptionGroup, ProgressionBalancing, Accessibility, ItemSet
from dataclasses import dataclass
from BaseClasses import List
from .Items import fighters_table


class EventsGoal(DefaultOnToggle):
    """Adds Event Mode to the goal. This can be used with other goals. In order to complete your seed, you must clear Event 51.

    If you exclude Event 51, the highest numbered Event that is still included will be the target Event to clear."""
    display_name = "Event Mode Goal"


class ProgressiveEvents(Toggle):
    """By default, Event mode unlocks as you receive Event Gate items.

    Set this to true, and events will be unlocked in a set order.\n
    Set this to false, and events will require certain fighters as well as a specified number of cleared events to unlock later events.

    Ignored if Event Mode Goal is False."""
    display_name = "Progressive Events"
    default = False


class ShuffleEventDetails(Choice):
    """By default, an event has a set P1 fighter (if applicable), set enemies and allies, a set stage, and other restrictions or AI routines.

    You can choose your level of randomization for events.

    If the player fighter is randomized, the event will logically require that fighter in order to count its completion.

    NOT YET IMPLEMENTED"""
    display_name = "Shuffle Event Details"
    default = 3
    option_ShufflePlayerChar = 0
    option_ShuffleEnemyChar = 1
    option_ShuffleBoth = 2
    option_Vanilla = 3


class ExcludedEvents(OptionList):
    """Events to exclude from the Events goal. Events can be excluded by name or number.

    Ignored if Event Mode Goal is False.

    Note: excluding events from the logic could mean that you still have to clear some excluded events in order for the game to allow access to more events."""
    display_name = "Exclude Events"
    default = []


class ClassicGoal(Toggle):
    """Adds Classic Mode to the goal. This can be used with other goals. In order to complete your seed, you must complete Classic with all fighters."""
    display_name = "Classic Mode Goal"
    default = False


class ClassicTotalGoal(Range):
    """Adds Classic Mode to the goal. Adds Classic Mode to the goal if Classic Mode Goal isn't selected. In order to complete your goal, you must reach the given amount of total points between all fighters.

    Your selection will be multiplied by 1 million to get your score requirement.

    This option will be ignored if set to 0."""
    display_name = "Classic Mode High Score Total Goal"
    default = 0
    range_start = 0
    range_end = 999


class AdventureGoal(Toggle):
    """Adds Adventure Mode to the goal. This can be used with other goals. In order to complete your seed, you must complete Adventure with all fighters."""
    display_name = "Adventure Mode Goal"
    default = False


class AdventureTotalGoal(Range):
    """Adds Adventure Mode to the goal. Adds Adventure Mode to the goal if Adventure Mode Goal isn't selected. In order to complete your goal, you must reach the given amount of total points between all fighters.

    Your selection will be multiplied by 1 million to get your score requirement.

    This option will be ignored if set to 0."""
    display_name = "Adventure Mode High Score Total Goal"
    default = 0
    range_start = 0
    range_end = 999


class AllStarGoal(Toggle):
    """Adds All-Star Mode to the goal. This can be used with other goals. In order to complete your seed, you must complete All-Star with all fighters."""
    display_name = "All-Star Mode Goal"
    default = False


class AllStarTotalGoal(Range):
    """Adds All-Star Mode to the goal. Adds All-Star Mode to the goal if All-Star Mode Goal isn't selected. In order to complete your goal, you must reach the given amount of total points between all fighters.

    Your selection will be multiplied by 1 million to get your score requirement.

    This option will be ignored if set to 0."""
    display_name = "All-Star Mode High Score Total Goal"
    default = 0
    range_start = 0
    range_end = 999


class TrophyCountGoal(Range):
    """Adds collecting trophies to the goal. This can be used with other goals. In order to complete your seed, you must get the number of trophies specified.

    This option will be ignored if set to 0.

    Excludes the Olimar and Japan-only trophies.
    For more information: https://www.ssbwiki.com/List_of_trophies_by_unlock_criteria_(SSBM)"""
    display_name = "Trophy Collection Goal"
    default = 0
    range_start = 0
    range_end = 290


class ExcludeFighters(ItemSet):
    """Excludes specific fighters from any goals you've chosen.

    This does not prevent you from obtaining your selected fighter, and neither does it prevent you from clearing various modes with them. This only prevents goals from considering their contributions."""
    display_name = "Exclude Fighters from Goals"
    valid_keys = {name: data.code for name, data in fighters_table.items()}
    convert_name_groups = False


class ShuffleStartingFighters(Toggle):
    """By default, you begin with Mario, Yoshi, Kirby, Fox, Samus, Link, etc. Turn this on to add those fighters to the randomization."""
    display_name = "Shuffle Starting Fighters"
    default = False


class StartingFighter(ItemSet):
    """Ignored unless Shuffle Starting Fighters is on. This fighter will be the only one you can select until you receive more.

    Choose ONE fighter only.

    If Shuffle Starting Fighters is Yes, but this is left blank, a starter will be randomly chosen for you."""
    display_name = "Starting Fighter"
    valid_keys = {name: data.code for name, data in fighters_table.items()}
    convert_name_groups = False


class EasyVsModeUnlocks(DefaultOnToggle):
    """Can make getting stages, fighters, and trophies very easy and quick."""
    display_name = "Easy Vs Mode Unlocks"


class CStickInSinglePlayer(DefaultOnToggle):
    """By default, the C-Stick moves the camera in single-player. This option changes the controls so that the C-Stick performs Smash attacks, like in Vs Mode."""
    display_name = "Enable C-Stick in Single Player"


class DisableTapJump(DefaultOnToggle):
    """By default, you can flick the control stick up quickly to jump. Set this option to true to disable that behavior."""
    display_name = "Disable Tap Jumping"


class DeathLinkMode(Choice):
    """Set what happens when death link activates.

    LoseStock: Lose a single stock when someone else sends a deathlink signal.\n
    LoseAllStocks: Lose all stocks when someone else sends a deathlink signal. In Vs, you lose. In 1P, you'll be taken to the Continue screen.\n
    LoseWithoutContinue: Same as LoseAllStocks, but you don't get a chance to Continue. Game over!
    """
    display_name = 'Death Link Mode'
    default = 0
    option_LoseStock = 0
    option_LoseAllStocks = 1
    option_LoseWithoutContinue = 2


@dataclass
class MeleeOptions(PerGameCommonOptions):
    # goals
    events_goal: EventsGoal
    progressive_events: ProgressiveEvents
    shuffle_event_details: ShuffleEventDetails
    excluded_events: ExcludedEvents
    classic_goal: ClassicGoal
    classic_total_goal: ClassicTotalGoal
    adventure_goal: AdventureGoal
    adventure_total_goal: AdventureTotalGoal
    all_star_goal: AllStarGoal
    all_star_total_goal: AllStarTotalGoal
    trophy_count_goal: TrophyCountGoal
    shuffle_starting_fighters: ShuffleStartingFighters
    starting_fighter: StartingFighter

    # optional/QoL
    exclude_fighters: ExcludeFighters
    easy_vs_mode_unlocks: EasyVsModeUnlocks
    c_stick_in_single_player: CStickInSinglePlayer
    disable_tap_jump: DisableTapJump
    death_link_mode: DeathLinkMode

    # generic
    death_link: DeathLink


def option_groups() -> List[OptionGroup]:
    groups = list()
    groups.append(OptionGroup('Goals and Logic', [
        ProgressionBalancing,
        Accessibility,
        EventsGoal,
        ProgressiveEvents,
        ShuffleEventDetails,
        ExcludedEvents,
        ClassicGoal,
        ClassicTotalGoal,
        AdventureGoal,
        AdventureTotalGoal,
        AllStarGoal,
        AllStarTotalGoal,
        TrophyCountGoal,
        ShuffleStartingFighters,
        StartingFighter,
    ]))
    groups.append(OptionGroup('Quality of Life', [
        ExcludeFighters,
        EasyVsModeUnlocks,
        CStickInSinglePlayer,
        DisableTapJump,
        DeathLink,
        DeathLinkMode,
    ]))
    return groups