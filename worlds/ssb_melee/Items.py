from enum import Enum
from typing import Dict, List, TYPE_CHECKING
from BaseClasses import Item, ItemClassification
if TYPE_CHECKING:
    import SSBMeleeWorld

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
        self.code = id + AP_METROID_PRIME_ITEM_ID_BASE
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
    
class ProgressiveUpgrade(Enum):
    Progressive_Event_Gate = "Progressive Event Gate"

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

