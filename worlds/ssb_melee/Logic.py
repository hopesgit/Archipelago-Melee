from BaseClasses import CollectionState
import worlds.ssb_melee.classes.Locations as Locations
import Container

import worlds.ssb_melee.classes.Classic as Classic
import worlds.ssb_melee.classes.Adventure as Adventure
import worlds.ssb_melee.classes.AllStar as AllStar
import worlds.ssb_melee.classes.Event as Event
import worlds.ssb_melee.classes.Trophies as Trophies
import worlds.ssb_melee.classes.Vs as Vs

import typing
if typing.TYPE_CHECKING:
    from MeleeOptions import SSBMeleeOptions

def _get_options(state: CollectionState, player: int) -> 'SSBMeleeOptions':
    return state.multiworld.worlds[player].options

def goal_includes_events(state: CollectionState, player: int) -> bool:
    events = _get_options(state, player).events_goal.value
    return events

def trim_events_list(state: CollectionState, player: int) -> bool:
    event_goal = goal_includes_events(state, player)
    event_list = Event.EVENTDATA.copy() # copy eventdata list so that we can remove events specified in yaml
    events_to_remove = _get_options(state, player).excluded_events.value
    if event_goal:
        for exclusion in events_to_remove:
            # event = event_list.index(elmnt["num"] == exclusion or elmnt["name"] == exclusion)
            event = map(lambda x: x["num"] == exclusion or x["name"] == exclusion, event_list)
            if event: 
                event_list.remove(event)
        # return revised event list once exceptions are made
    return event_list
    