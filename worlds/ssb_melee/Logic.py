from BaseClasses import CollectionState, List, Dict
from .Locations import *

from classes.Event import EVENTDATA

from random import random, choice
from CommonClient import logger

import typing
if typing.TYPE_CHECKING:
    from .MeleeOptions import MeleeOptions

def _get_options(state: CollectionState, player: int) -> 'MeleeOptions':
    return state.multiworld.worlds[player].options

# options logic
## Events
def goal_includes_events(state: CollectionState, player: int) -> bool:
    return _get_options(state, player).events_goal.value

def progressive_events(state: CollectionState, player: int) -> bool:
    return _get_options(state, player).progressive_events.value

def shuffle_events(state: CollectionState, player: int) -> str:
    return _get_options(state, player).shuffle_event_details.value

def trim_events_list(state: CollectionState, player: int) -> Dict:
    event_goal = goal_includes_events(state, player)
    event_list = EVENTDATA.copy() # copy eventdata list so that we can remove events specified in yaml
    events_to_remove = sanitize_event_exclusions(state, player)
    if event_goal and len(events_to_remove) > 0:
        for exclusion in events_to_remove:
            event_list.pop(exclusion)
    return event_list

def sanitize_event_exclusions(state: CollectionState, player: int) -> List[int|None]:
    events_to_remove_from_opts = _get_options(state, player).excluded_events.value
    events_to_remove = list()
    if len(events_to_remove_from_opts) > 0:
        for item in events_to_remove_from_opts:
            try: 
                range = item.split('-')
                r = range(int(range[0]), int(range[1]) + 1)
                for n in r:
                    events_to_remove.append(n)
            except SyntaxError:
                try:
                    n = int(item)
                    events_to_remove.append(n)
                except TypeError:
                    continue
        if len(events_to_remove) > 0:
            events_to_remove = events_to_remove.sort()
    else: 
        return events_to_remove
    
## Classic
def goal_includes_classic(state: CollectionState, player: int) -> bool:
    clear = _get_options(state, player).classic_goal.value
    total = int(_get_options(state, player).classic_total_goal.value) > 0
    return clear or total

## Adventure
def goal_includes_adventure(state: CollectionState, player: int) -> bool:
    clear = _get_options(state, player).adventure_goal.value
    total = int(_get_options(state, player).adventure_total_goal.value) > 0
    return clear or total

## All-Star
def goal_includes_all_star(state: CollectionState, player: int) -> bool:
    clear = _get_options(state, player).all_star_goal.value
    total = int(_get_options(state, player).all_star_total_goal.value) > 0
    return clear or total

def goal_includes_trophies(state: CollectionState, player: int) -> int:
    option = _get_options(state, player).trophy_count_goal.value
    value = 0
    random_values = {
        'low': range(1, 51),
        'mid': range(51, 151),
        'high': range(151, 291),
    }
    split = option.split('-')
    if (split[0] == 'random'):
        if split[1] in random_values.keys():
            value = choice(random_values[split[1]])
        else:
            value = choice(range(1, 291))

    if (value == 0):
        try:
            value = int(split[0])
        except ValueError as e:
            logger('Trophy count logic error: "' + e + '"')
    return value
    
# item logic
def has_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    basic_fighters = ["Mario", "Peach", "Bowser", "Yoshi", "Ice Climbers", 
                      "Captain Falcon", "Ness", "Donkey Kong", "Fox", "Samus", 
                      "Kirby", "Zelda", "Link", "Pikachu"]
    if fighter in basic_fighters:
        return True
    else:
        return state.has(fighter, player)

def has_all_basic_characters(state: CollectionState, player: int) -> bool:
    return True

def has_all_unlockable_characters(state: CollectionState, player: int) -> bool:
    return (has_fighter(state, player, "Dr. Mario") and 
            has_fighter(state, player, "Luigi") and 
            has_fighter(state, player, "Ganondorf") and 
            has_fighter(state, player, "Falco") and 
            has_fighter(state, player, "Young Link") and 
            has_fighter(state, player, "Pichu") and 
            has_fighter(state, player, "Jigglypuff") and 
            has_fighter(state, player, "Mewtwo") and 
            has_fighter(state, player, "Mr. Game and Watch") and 
            has_fighter(state, player, "Marth") and 
            has_fighter(state, player, "Roy"))

def has_event_set_one(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 1", player) or state.has('Progressive Event Gate', player, 1)

def has_event_set_two(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 2", player) or state.has('Progressive Event Gate', player, 2)

def has_event_set_three(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 3", player) or state.has('Progressive Event Gate', player, 3)

def has_event_set_four(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 4", player) or state.has('Progressive Event Gate', player, 4)

def has_event_set_five(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 5", player) or state.has('Progressive Event Gate', player, 5)

def has_event_set_six(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 6", player) or state.has('Progressive Event Gate', player, 6)

def has_event_set_seven(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 7", player) or state.has('Progressive Event Gate', player, 7)

def has_event_set_eight(state: CollectionState, player: int) -> bool:
    state.has("Event Gate 8", player) or state.has('Progressive Event Gate', player, 8)

def has_all_star(state: CollectionState, player: int) -> bool: 
    state.has('All-Star Mode')

def can_do_all_star_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_all_star(state, player) and has_fighter(state, player, fighter)

def can_do_adventure_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_fighter(state, player, fighter)

def can_do_classic_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_fighter(state, player, fighter)

def can_do_hrc_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_fighter(state, player, fighter)

def can_do_btt_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_fighter(state, player, fighter)

def can_do_mmm_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_fighter(state, player, fighter)

def can_do_vs_with_fighter(state: CollectionState, player: int, fighter: str) -> bool:
    has_fighter(state, player, fighter)