from BaseClasses import Location, List, Dict, Optional, Region
from .Regions import MeleeRegion
import os
import csv

MELEE_LOCATION_BASE = 50311000


class MeleeLocation(Location):
    game: str = "Super Smash Bros Melee"

classic_location_table = {
    'Classic Mode - Mario Clear': MELEE_LOCATION_BASE + 1,
    'Classic Mode - Dr. Mario Clear': MELEE_LOCATION_BASE + 2,
    'Classic Mode - Luigi Clear': MELEE_LOCATION_BASE + 3,
    'Classic Mode - Peach Clear': MELEE_LOCATION_BASE + 4,
    'Classic Mode - Bowser Clear': MELEE_LOCATION_BASE + 5,
    'Classic Mode - Yoshi Clear': MELEE_LOCATION_BASE + 6,
    'Classic Mode - Donkey Kong Clear': MELEE_LOCATION_BASE + 7,
    'Classic Mode - Captain Falcon Clear': MELEE_LOCATION_BASE + 8,
    'Classic Mode - Ganondorf Clear': MELEE_LOCATION_BASE + 9,
    'Classic Mode - Falco Clear': MELEE_LOCATION_BASE + 10,
    'Classic Mode - Fox Clear': MELEE_LOCATION_BASE + 11,
    'Classic Mode - Ness Clear': MELEE_LOCATION_BASE + 12,
    'Classic Mode - Ice Climbers Clear': MELEE_LOCATION_BASE + 13,
    'Classic Mode - Kirby Clear': MELEE_LOCATION_BASE + 14,
    'Classic Mode - Samus Clear': MELEE_LOCATION_BASE + 15,
    'Classic Mode - Zelda Clear': MELEE_LOCATION_BASE + 16,
    'Classic Mode - Link Clear': MELEE_LOCATION_BASE + 17,
    'Classic Mode - Young Link Clear': MELEE_LOCATION_BASE + 18,
    'Classic Mode - Pichu Clear': MELEE_LOCATION_BASE + 19,
    'Classic Mode - Pikachu Clear': MELEE_LOCATION_BASE + 20,
    'Classic Mode - Jigglypuff Clear': MELEE_LOCATION_BASE + 21,
    'Classic Mode - Mewtwo Clear': MELEE_LOCATION_BASE + 22,
    'Classic Mode - Mr Game & Watch Clear': MELEE_LOCATION_BASE + 23,
    'Classic Mode - Marth Clear': MELEE_LOCATION_BASE + 24,
    'Classic Mode - Roy Clear': MELEE_LOCATION_BASE + 25,
}

adventure_location_table = {
    'Adventure Mode - Mario Clear': MELEE_LOCATION_BASE + 26,
    'Adventure Mode - Dr. Mario Clear': MELEE_LOCATION_BASE + 27,
    'Adventure Mode - Luigi Clear': MELEE_LOCATION_BASE + 28,
    'Adventure Mode - Peach Clear': MELEE_LOCATION_BASE + 29,
    'Adventure Mode - Bowser Clear': MELEE_LOCATION_BASE + 30,
    'Adventure Mode - Yoshi Clear': MELEE_LOCATION_BASE + 31,
    'Adventure Mode - Donkey Kong Clear': MELEE_LOCATION_BASE + 32,
    'Adventure Mode - Captain Falcon Clear': MELEE_LOCATION_BASE + 33,
    'Adventure Mode - Ganondorf Clear': MELEE_LOCATION_BASE + 34,
    'Adventure Mode - Falco Clear': MELEE_LOCATION_BASE + 35,
    'Adventure Mode - Fox Clear': MELEE_LOCATION_BASE + 36,
    'Adventure Mode - Ness Clear': MELEE_LOCATION_BASE + 37,
    'Adventure Mode - Ice Climbers Clear': MELEE_LOCATION_BASE + 38,
    'Adventure Mode - Kirby Clear': MELEE_LOCATION_BASE + 39,
    'Adventure Mode - Samus Clear': MELEE_LOCATION_BASE + 40,
    'Adventure Mode - Zelda Clear': MELEE_LOCATION_BASE + 41,
    'Adventure Mode - Link Clear': MELEE_LOCATION_BASE + 42,
    'Adventure Mode - Young Link Clear': MELEE_LOCATION_BASE + 43,
    'Adventure Mode - Pichu Clear': MELEE_LOCATION_BASE + 44,
    'Adventure Mode - Pikachu Clear': MELEE_LOCATION_BASE + 45,
    'Adventure Mode - Jigglypuff Clear': MELEE_LOCATION_BASE + 46,
    'Adventure Mode - Mewtwo Clear': MELEE_LOCATION_BASE + 47,
    'Adventure Mode - Mr Game & Watch Clear': MELEE_LOCATION_BASE + 48,
    'Adventure Mode - Marth Clear': MELEE_LOCATION_BASE + 49,
    'Adventure Mode - Roy Clear': MELEE_LOCATION_BASE + 50,
}

all_star_location_table = {
    'All-Star Mode - Mario Clear': MELEE_LOCATION_BASE + 51,
    'All-Star Mode - Dr. Mario Clear': MELEE_LOCATION_BASE + 52,
    'All-Star Mode - Luigi Clear': MELEE_LOCATION_BASE + 53,
    'All-Star Mode - Peach Clear': MELEE_LOCATION_BASE + 54,
    'All-Star Mode - Bowser Clear': MELEE_LOCATION_BASE + 55,
    'All-Star Mode - Yoshi Clear': MELEE_LOCATION_BASE + 56,
    'All-Star Mode - Donkey Kong Clear': MELEE_LOCATION_BASE + 57,
    'All-Star Mode - Captain Falcon Clear': MELEE_LOCATION_BASE + 58,
    'All-Star Mode - Ganondorf Clear': MELEE_LOCATION_BASE + 59,
    'All-Star Mode - Falco Clear': MELEE_LOCATION_BASE + 60,
    'All-Star Mode - Fox Clear': MELEE_LOCATION_BASE + 61,
    'All-Star Mode - Ness Clear': MELEE_LOCATION_BASE + 62,
    'All-Star Mode - Ice Climbers Clear': MELEE_LOCATION_BASE + 63,
    'All-Star Mode - Kirby Clear': MELEE_LOCATION_BASE + 64,
    'All-Star Mode - Samus Clear': MELEE_LOCATION_BASE + 65,
    'All-Star Mode - Zelda Clear': MELEE_LOCATION_BASE + 66,
    'All-Star Mode - Link Clear': MELEE_LOCATION_BASE + 67,
    'All-Star Mode - Young Link Clear': MELEE_LOCATION_BASE + 68,
    'All-Star Mode - Pichu Clear': MELEE_LOCATION_BASE + 69,
    'All-Star Mode - Pikachu Clear': MELEE_LOCATION_BASE + 70,
    'All-Star Mode - Jigglypuff Clear': MELEE_LOCATION_BASE + 71,
    'All-Star Mode - Mewtwo Clear': MELEE_LOCATION_BASE + 72,
    'All-Star Mode - Mr Game & Watch Clear': MELEE_LOCATION_BASE + 73,
    'All-Star Mode - Marth Clear': MELEE_LOCATION_BASE + 74,
    'All-Star Mode - Roy Clear': MELEE_LOCATION_BASE + 75,
}

total_score_table = {
    'Classic Mode - High Score Total Reached - 1m': MELEE_LOCATION_BASE + 76,
    'Classic Mode - High Score Total Reached - 2m': MELEE_LOCATION_BASE + 77,
    'Classic Mode - High Score Total Reached - 5m': MELEE_LOCATION_BASE + 78,
    'Classic Mode - High Score Total Reached - 10m': MELEE_LOCATION_BASE + 79,
    'Adventure Mode - High Score Total Reached - 1m': MELEE_LOCATION_BASE + 80,
    'Adventure Mode - High Score Total Reached - 2m': MELEE_LOCATION_BASE + 81,
    'Adventure Mode - High Score Total Reached - 5m': MELEE_LOCATION_BASE + 82,
    'Adventure Mode - High Score Total Reached - 10m': MELEE_LOCATION_BASE + 83,
    'All-Star Mode - High Score Total Reached - 1m': MELEE_LOCATION_BASE + 84,
    'All-Star Mode - High Score Total Reached - 2m': MELEE_LOCATION_BASE + 85,
    'All-Star Mode - High Score Total Reached - 5m': MELEE_LOCATION_BASE + 86,
    'All-Star Mode - High Score Total Reached - 10m': MELEE_LOCATION_BASE + 87
}

from .classes.Event import EVENTDATA
event_location_table = {}
event_location_counter = MELEE_LOCATION_BASE + 99
event_counter = 0
for event in EVENTDATA:
    event_counter += 1
    event_location_counter += 1
    event_location_table.update({f"Event Match - Clear Event #{event_counter}": event_location_counter})

trophy_location_table = {}
trophy_location_counter = event_location_counter
path = os.path.join(os.path.dirname(__file__), "data/SSBM Trophies.csv")
with open(path, 'r') as file: 
    trophy_csv = csv.reader(file)
    for row in trophy_csv:
        trophy_location_counter += 1
        trophy_location_table.update({f"{row[1]}": trophy_location_counter})

# from .classes.Fighter import get_unlockable_fighters
# fighter_location_table = {}
# fighter_location_counter = trophy_location_counter
# fighter_counter = trophy_counter
# fighters = await get_unlockable_fighters()
# for fighter in fighters:
#     fighter_location_counter += 1
#     fighter_counter = fighter_counter + 1
#     fighter_location_table.update({f"Win Fighter Unlock Duel - {fighter}": fighter_counter})


from .classes.SpecialBonus import BONUSES
bonus_location_table = {}
bonus_location_counter = trophy_location_counter
bonuses = BONUSES
for bonus in bonuses:
    bonus_location_counter += 1
    bonus_location_table.update({f"First Time Special Bonus - {bonus.name}": bonus_location_counter})


locations: dict[str, int] = {
    **classic_location_table,
    **adventure_location_table,
    **all_star_location_table,
    **total_score_table,
    **event_location_table,
    **trophy_location_table,
    #**fighter_location_table,
    **bonus_location_table
}


def generate_loc_objs(player: int, region: str | None, region_obj: Optional[Region]):
    result = dict()
    result[MeleeRegion.Menu.value] = loc_objs_from_table(player, bonus_location_table)
    result[MeleeRegion.Adventure.value] = loc_objs_from_table(player, adventure_location_table)
    result[MeleeRegion.All_Star.value] = loc_objs_from_table(player, all_star_location_table)
    result[MeleeRegion.Classic.value] = loc_objs_from_table(player, classic_location_table)
    result[MeleeRegion.Event.value] = loc_objs_from_table(player, event_location_table)
    # result[MeleeRegion.HRC.value] = loc_objs_from_table(player, hrc_location_table)
    # result[MeleeRegion.Target_Test.value] = loc_objs_from_table(player, target_location_table)
    # result[MeleeRegion.Multi_Man.value] = loc_objs_from_table(player, multi_man_location_table)
    result[MeleeRegion.Trophies.value] = loc_objs_from_table(player, trophy_location_table)
    # result[MeleeRegion.Vs.value] = loc_objs_from_table(player, fighter_location_table)
    result["High Score"] = loc_objs_from_table(player, total_score_table)
    if region:
        if region_obj:
            for location in result[region]:
                location.parent_region = region_obj
        return result[region]
    return result


def loc_objs_from_table(player, table: Dict[str, int]) -> List[MeleeLocation]:
    result = list()
    for loc, id in table.items():
        newloc = MeleeLocation(player=player, name=loc, address=id)
        print(newloc)
        result.append(newloc)
    return result