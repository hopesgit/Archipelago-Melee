from BaseClasses import CollectionState, List, Dict
from .Locations import *

from classes.Event import EVENTDATA

import typing
if typing.TYPE_CHECKING:
    from .MeleeOptions import MeleeOptions

def _get_options(state: CollectionState, player: int) -> 'MeleeOptions':
    return state.multiworld.worlds[player].options

def basic_or_custom(state: CollectionState, player: int) -> bool:
    goal = _get_options(state, player)

def goal_includes_events(state: CollectionState, player: int) -> bool:
    check = _get_options(state, player).events_goal.value or basic_or_custom(state, player)
    return check

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