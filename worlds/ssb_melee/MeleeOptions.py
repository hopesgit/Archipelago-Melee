from enum import Enum
from Options import DeathLink, DefaultOnToggle, OptionDict, OptionList, TextChoice, Toggle, Range, ItemDict, StartInventoryPool, Choice, PerGameCommonOptions, Visibility
from dataclasses import dataclass

class MinimalGoal(Choice):
    """Basic chooses the following options: Events Goal, 51 required events; no other goals. 
    
    In order to win, you must complete all 51 events and obtain all characters.

    Custom allows you to choose your own goals."""
    default = "Basic"
    options = ["Basic", "Custom"]

class EventsGoal(Toggle):
    """Adds Event Mode to the goal. This can be used with other goals. In order to complete your seed, you must clear Event 51.
    If you exclude Event 51, the highest numbered Event that is still included will be the target Event to clear."""
    display_name = "Event Mode Goal"
    default = True

class EventsRequired(Range):
    """The number of events the player must clear in order to complete an Events goal.
    Ignored if Event Mode Goal is False."""
    display_name = "Number of Required Events"
    range_start = 1
    range_end = 51
    default = 51

class ProgressiveEvents(Toggle):
    """By default, Event mode unlocks as you gather more characters and complete a specified number of events.
    Set this to true, and events will instead be gated by Event Gate items.
    Set this to false, and events will require certain characters as well as a specified number of cleared events to unlock later events.
    Ignored if Event Mode Goal is False."""
    display_name = "Progressive Events"
    default = False

class ExcludedEvents(OptionList):
    """Events to exclude from the Events goal. Events can be excluded by name or number.
    Ignored if Event Mode Goal is False.
    Note: excluding events from the logic could mean that you still have to clear some excluded events in order for the game to allow access to more events."""
    display_name = "Exclude Events"
    default = []

class ClassicGoal(Toggle):
    """Adds Classic Mode to the goal. This can be used with other goals. In order to complete your seed, you must complete Classic with all characters."""
    display_name = "Classic Mode Goal"
    default = False

class ClassicTotalGoal(Range):
    """Adds Classic Mode to the goal. Adds Classic Mode to the goal if Classic Mode Goal isn't selected. In order to complete your goal, you must reach the given amount of total points between all characters.
    This option will be ignored if set to 0."""
    display_name = "Classic Mode High Score Total Goal"
    default = 0
    range_start = 0
    range_end = 100000000

class AdventureGoal(Toggle):
    """Adds Adventure Mode to the goal. This can be used with other goals. In order to complete your seed, you must complete Adventure with all characters."""
    display_name = "Adventure Mode Goal"
    default = False

class AdventureTotalGoal(Range):
    """Adds Adventure Mode to the goal. Adds Adventure Mode to the goal if Adventure Mode Goal isn't selected. In order to complete your goal, you must reach the given amount of total points between all characters.
    This option will be ignored if set to 0."""
    display_name = "Adventure Mode High Score Total Goal"
    default = 0
    range_start = 0
    range_end = 100000000

class AllStarGoal(Toggle):
    """Adds All-Star Mode to the goal. This can be used with other goals. In order to complete your seed, you must complete All-Star with all characters.
    You can unlock All-Star Mode by unlocking all playable characters."""
    display_name = "All-Star Mode Goal"
    default = False

class AllStarTotalGoal(Range):
    """Adds All-Star Mode to the goal. Adds All-Star Mode to the goal if All-Star Mode Goal isn't selected. In order to complete your goal, you must reach the given amount of total points between all characters.
    This option will be ignored if set to 0."""
    display_name = "All-Star Mode High Score Total Goal"
    default = 0
    range_start = 0
    range_end = 100000000

class TrophyCountGoal(Range):
    """Adds collecting trophies to the goal. This can be used with other goals. In order to complete your seed, you must get the number of trophies specified.
    This option will be ignored if set to 0. 
    Excludes the Olimar and Japan-only trophies.
    For more information: https://www.ssbwiki.com/List_of_trophies_by_unlock_criteria_(SSBM)"""
    display_name = "Trophy Collector Goal"
    default = 0
    range_start = 0
    range_end = 290

class ExcludeCharacters(OptionList):
    """Exludes specific characters from any goals you've chosen. Good for if you just really don't vibe with a character."""
    display_name = "Exclude Characters from Goals"
    default = []

class EasyVsModeUnlocks(Range):
    """Completely optional. Sets the vs mode battle counters to whatever value specified. Can make getting stages, characters, and trophies very easy and/or quick."""
    display_name = "Easy Vs Mode Unlocks"
    default = 0
    range_start = 0
    range_end = 1000

class CStickInSinglePlayer(Toggle):
    """By default, the C-Stick moves the camera in single-player. This option changes the controls so that the C-Stick performs Smash attacks, like in Vs Mode."""
    display_name = "Enable C-Stick in Single Player"
    default = True

class DeathLinkMode(Choice):
    """Set what happens when death link activates."""
    display_name = 'Death Link Mode'
    default = 'Lose Stock'
    options = ['Lose Stock', 'Lose All Stocks', 'Lose Without Continue']


@dataclass
class MeleeOptions(PerGameCommonOptions):
    # goals
    minimal_goal: MinimalGoal
    events_goal: EventsGoal
    events_required: EventsRequired
    progressive_events: ProgressiveEvents
    excluded_events: ExcludedEvents
    classic_goal: ClassicGoal
    classic_total_goal: ClassicTotalGoal
    adventure_goal: AdventureGoal
    adventure_total_goal: AdventureTotalGoal
    all_star_goal: AllStarGoal
    all_star_total_goal: AllStarTotalGoal
    trophy_count__goal: TrophyCountGoal

    # optional/QoL
    exclude_characters: ExcludeCharacters
    easy_vs_mode_unlocks: EasyVsModeUnlocks
    c_stick_in_single_player: CStickInSinglePlayer
    death_link_mode: DeathLinkMode

    # generic
    death_link: DeathLink
