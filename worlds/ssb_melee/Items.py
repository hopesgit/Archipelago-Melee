from enum import Enum
from typing import Dict, List, TYPE_CHECKING, Optional, Union
from BaseClasses import Item, ItemClassification, Group
if TYPE_CHECKING:
    from . import SSBMeleeWorld

MELEE_ITEM_ID_BASE = 5000

class ItemData:
    name: str
    code: int
    classification: ItemClassification
    max_capacity: int
    id: int

    def __init__(self, name: str, id: int, progression: ItemClassification, max_capacity: int = 1) -> None:
        self.name = name
        self.id = id
        self.code = id + MELEE_ITEM_ID_BASE
        self.classification = progression
        self.max_capacity = max_capacity

class SSBMeleeItem(Item):
    game: str = "Super Smash Bros Melee"

class MeleeUnlock(Enum):
    # event
    Event_Gate_1 = "Event Gate 1" #unlocks events 11-15
    Event_Gate_2 = "Event Gate 2" #unlocks events 16-20
    Event_Gate_3 = "Event Gate 3" #unlocks events 21-25
    Event_Gate_4 = "Event Gate 4" #unlocks events 26-29
    Event_Gate_5 = "Event Gate 5" #unlocks event 30
    Event_Gate_6 = "Event Gate 6" #unlocks events 31-39
    Event_Gate_7 = "Event Gate 7" #unlocks events 40-50
    Event_Gate_8 = "Event Gate 8" #unlocks event 51
    # modes
    All_Star_Mode = "All-Star Mode" #unlocks All-Star Mode
    # fighters
    Dr_Mario = "Dr. Mario" #unlocks Dr. Mario
    Luigi = "Luigi" #unlocks Luigi
    Ganondorf = "Ganondorf" #unlocks Ganondorf
    Falco = "Falco" #unlocks Falco Lombardi
    Young_Link = "Young Link" # unlocks Young Link
    Pichu = "Pichu" #unlocks Pichu
    Jigglypuff = "Jigglypuff" #unlocks Jigglypuff
    Mewtwo = "Mewtwo" #unlocks Mewtwo
    Mr_Game_and_Watch = "Mr. Game & Watch" #unlocks Game & Watch
    Marth = "Marth" #unlocks Marth
    Roy = "Roy" #unlocks Roy
    # misc unlocks
    Mew = "Mew" #allows Mew to spawn in Poke Balls
    Celebi = "Celebi" #allows Celebi to spawn in Poke Balls
    Score_Display = "Score Display" #unlocks the Score Display option for Vs Mode - shows score during match
    Sound_Test = "Sound Test" #unlocks the Sound Test in the menu
    Random_Stage_Select = "Random Stage Select" #enables random stage select option in Vs rules
    Trophy = "Trophy" # unlocks a random trophy
    # stages
    Brinstar_Depths = "Brinstar Depths"
    Fourside = "Fourside"
    Big_Blue = "Big Blue"
    Poke_Floats = "Poke Floats"
    PS_Dream_Land = "Past Stages - Dream Land"
    PS_Kongo_Jungle = "Past Stages - Kongo Jungle"
    PS_Yoshis_Island = "Past Stages - Yoshi's Island"
    Battlefield = "Battlefield"
    Final_Destination = "Final Destination"
    Flat_Zone = "Flat Zone"
    #traps
    Shock_Trap = "Shock Trap" # 20% damage, stun effect
    Ice_Trap = "Ice Trap" # 20% damage, chance to freeze
    Fire_Trap = "Fire Trap" # 20% damage, burn effect
    Stale_Moves_Trap = "Stale Moves Trap" # all p1 moves are stale for 5 minutes
    Bomb_Rain_Trap = "Bomb Rain Trap" # bombs rain for 280 frames
    Item_Bonanza_Trap = "Item Bonanza Trap" # item spawn rate set to very high for 5 minutes
    #bonuses
    Coins_100 = "100 Coins"
    Coins_500 = "500 Coins"
    Coins_999 = "999 Coins"

    def __str__(self):
        return self.value
    
class ProgressiveUpgrade(Enum):
    Progressive_Event_Gate = "Progressive Event Gate"

    def __str__(self):
        return self.value

PROGRESSIVE_ITEM_MAPPING: Dict[ProgressiveUpgrade, List[MeleeUnlock]] = {
    ProgressiveUpgrade.Progressive_Event_Gate: [
        MeleeUnlock.Event_Gate_1, 
        MeleeUnlock.Event_Gate_2, 
        MeleeUnlock.Event_Gate_3, 
        MeleeUnlock.Event_Gate_4, 
        MeleeUnlock.Event_Gate_5, 
        MeleeUnlock.Event_Gate_6, 
        MeleeUnlock.Event_Gate_7, 
        MeleeUnlock.Event_Gate_8
    ]
}

PROGRESSIVE_ITEM_EXCLUSION_LIST: List[MeleeUnlock] = [
    MeleeUnlock.Event_Gate_1,
    MeleeUnlock.Event_Gate_2,
    MeleeUnlock.Event_Gate_3,
    MeleeUnlock.Event_Gate_4,
    MeleeUnlock.Event_Gate_5,
    MeleeUnlock.Event_Gate_6,
    MeleeUnlock.Event_Gate_7,
    MeleeUnlock.Event_Gate_8,
]

def get_vanilla_item_for_progressive_upgrade(
    upgrade: ProgressiveUpgrade, count: int
) -> Optional[MeleeUnlock]:
    max_count = 8
    if count > max_count:
        count = max_count

    index = count - 1  # 0-indexed
    if upgrade in PROGRESSIVE_ITEM_MAPPING:
        return PROGRESSIVE_ITEM_MAPPING[upgrade][index]
    return None


def get_progressive_upgrade_for_item(item: MeleeUnlock) -> Optional[ProgressiveUpgrade]:
    for upgrade, items in PROGRESSIVE_ITEM_MAPPING.items():
        if item in items:
            return upgrade
    return None

def get_item_for_options(
    world: "SSBMeleeWorld", item: MeleeUnlock
) -> Union[MeleeUnlock, ProgressiveUpgrade]:
    if world.options.progressive_events:
        progressive_upgrade = get_progressive_upgrade_for_item(item)
        if progressive_upgrade is not None:
            return progressive_upgrade
    return item

events_table: Dict[str, ItemData] = {
    MeleeUnlock.Event_Gate_1.value: ItemData(
        MeleeUnlock.Event_Gate_1.value, 0, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_2.value: ItemData(
        MeleeUnlock.Event_Gate_2.value, 1, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_3.value: ItemData(
        MeleeUnlock.Event_Gate_3.value, 2, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_4.value: ItemData(
        MeleeUnlock.Event_Gate_4.value, 3, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_5.value: ItemData(
        MeleeUnlock.Event_Gate_5.value, 4, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_6.value: ItemData(
        MeleeUnlock.Event_Gate_6.value, 5, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_7.value: ItemData(
        MeleeUnlock.Event_Gate_7.value, 6, ItemClassification.progression
    ),
    MeleeUnlock.Event_Gate_8.value: ItemData(
        MeleeUnlock.Event_Gate_8.value, 7, ItemClassification.progression
    )
}

modes_table: Dict[str, ItemData] = {
    MeleeUnlock.Dr_Mario.value: ItemData(
        MeleeUnlock.All_Star_Mode.value, 8, ItemClassification.progression
    )
}

fighters_table: Dict[str, ItemData] = {
    MeleeUnlock.Dr_Mario.value: ItemData(
        MeleeUnlock.Dr_Mario.value, 10, ItemClassification.progression
    ),
    MeleeUnlock.Luigi.value: ItemData(
        MeleeUnlock.Luigi.value, 11, ItemClassification.progression
    ),
    MeleeUnlock.Ganondorf.value: ItemData(
        MeleeUnlock.Ganondorf.value, 12, ItemClassification.progression
    ),
    MeleeUnlock.Falco.value: ItemData(
        MeleeUnlock.Falco.value, 13, ItemClassification.progression
    ),
    MeleeUnlock.Young_Link.value: ItemData(
        MeleeUnlock.Young_Link.value, 14, ItemClassification.progression
    ),
    MeleeUnlock.Pichu.value: ItemData(
        MeleeUnlock.Pichu.value, 15, ItemClassification.progression
    ),
    MeleeUnlock.Jigglypuff.value: ItemData(
        MeleeUnlock.Jigglypuff.value, 16, ItemClassification.progression
    ),
    MeleeUnlock.Mewtwo.value: ItemData(
        MeleeUnlock.Mewtwo.value, 17, ItemClassification.progression
    ),
    MeleeUnlock.Mr_Game_and_Watch.value: ItemData(
        MeleeUnlock.Mr_Game_and_Watch.value, 18, ItemClassification.progression
    ),
    MeleeUnlock.Marth.value: ItemData(
        MeleeUnlock.Marth.value, 19, ItemClassification.progression
    ),
    MeleeUnlock.Roy.value: ItemData(
        MeleeUnlock.Roy.value, 20, ItemClassification.progression
    ),
}

stage_unlocks_table: Dict[str, MeleeUnlock] = {
    MeleeUnlock.Brinstar_Depths.value: ItemData(
        MeleeUnlock.Brinstar_Depths.value, 30, ItemClassification.progression
    ),
    MeleeUnlock.Fourside.value: ItemData(
        MeleeUnlock.Fourside.value, 31, ItemClassification.progression
    ),
    MeleeUnlock.Big_Blue.value: ItemData(
        MeleeUnlock.Big_Blue.value, 32, ItemClassification.progression
    ),
    MeleeUnlock.Poke_Floats.value: ItemData(
        MeleeUnlock.Poke_Floats.value, 33, ItemClassification.progression
    ),
    MeleeUnlock.PS_Dream_Land.value: ItemData(
        MeleeUnlock.PS_Dream_Land.value, 34, ItemClassification.progression
    ),
    MeleeUnlock.PS_Kongo_Jungle.value: ItemData(
        MeleeUnlock.PS_Kongo_Jungle.value, 35, ItemClassification.progression
    ),
    MeleeUnlock.PS_Yoshis_Island.value: ItemData(
        MeleeUnlock.PS_Yoshis_Island.value, 36, ItemClassification.progression
    ),
    MeleeUnlock.Battlefield.value: ItemData(
        MeleeUnlock.Battlefield.value, 37, ItemClassification.progression
    ),
    MeleeUnlock.Final_Destination.value: ItemData(
        MeleeUnlock.Final_Destination.value, 38, ItemClassification.progression
    ),
    MeleeUnlock.Flat_Zone.value: ItemData(
        MeleeUnlock.Flat_Zone.value, 39, ItemClassification.progression
    ),
}


misc_unlocks_table: Dict[str, ItemData] = {
    MeleeUnlock.Mew.value: ItemData(
        MeleeUnlock.Mew.value, 40, ItemClassification.useful
    ),
    MeleeUnlock.Celebi.value: ItemData(
        MeleeUnlock.Celebi.value, 41, ItemClassification.useful
    ),
    MeleeUnlock.Score_Display.value: ItemData(
        MeleeUnlock.Score_Display.value, 42, ItemClassification.filler
    ),
    MeleeUnlock.Sound_Test.value: ItemData(
        MeleeUnlock.Sound_Test.value, 43, ItemClassification.filler
    ),
    MeleeUnlock.Random_Stage_Select.value: ItemData(
        MeleeUnlock.Random_Stage_Select.value, 44, ItemClassification.useful
    ),
    MeleeUnlock.Trophy.value: ItemData(
        MeleeUnlock.Trophy.value, 45, ItemClassification.progression, 290
    ),
}

progressive_table: Dict[str, ItemData] = {
    ProgressiveUpgrade.Progressive_Event_Gate.value: ItemData(
        ProgressiveUpgrade.Progressive_Event_Gate.value, 100, ItemClassification.progression, 8
    ),
}

traps_table: Dict[str, ItemData] = {
    MeleeUnlock.Shock_Trap.value: ItemData(
        MeleeUnlock.Shock_Trap.value, 110, ItemClassification.trap, 10
    ),
    MeleeUnlock.Ice_Trap.value: ItemData(
        MeleeUnlock.Ice_Trap.value, 111, ItemClassification.trap, 10
    ),
    MeleeUnlock.Fire_Trap.value: ItemData(
        MeleeUnlock.Fire_Trap.value, 112, ItemClassification.trap, 10
    ),
    MeleeUnlock.Bomb_Rain_Trap.value: ItemData(
        MeleeUnlock.Bomb_Rain_Trap.value, 113, ItemClassification.trap, 10
    ),
    MeleeUnlock.Stale_Moves_Trap.value: ItemData(
        MeleeUnlock.Stale_Moves_Trap.value, 114, ItemClassification.trap, 10
    ),
    MeleeUnlock.Item_Bonanza_Trap.value: ItemData(
        MeleeUnlock.Item_Bonanza_Trap.value, 115, ItemClassification.trap, 10
    ),
}

useful_items_table: Dict[str, ItemData] = {
    MeleeUnlock.Coins_100.value: ItemData(
        MeleeUnlock.Coins_100.value, 120, ItemClassification.filler, 10
    ),
    MeleeUnlock.Coins_500.value: ItemData(
        MeleeUnlock.Coins_500.value, 121, ItemClassification.filler, 10
    ),
    MeleeUnlock.Coins_999.value: ItemData(
        MeleeUnlock.Coins_999.value, 122, ItemClassification.filler, 5
    ),
}

item_table: Dict[str, ItemData] = {
    **events_table,
    **modes_table,
    **fighters_table,
    **stage_unlocks_table,
    **misc_unlocks_table,
    #**progressive_table,
    **traps_table,
    **useful_items_table
}
