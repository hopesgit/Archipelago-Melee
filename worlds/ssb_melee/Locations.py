from BaseClasses import Location, MultiWorld
from .classes.Event import EVENTDATA
from .classes.Character import get_unlockable_characters
import os
import csv

METROID_PRIME_LOCATION_BASE = 5031100

class MeleeLocation(Location): #Location
    game: str = "Super Smash Bros Melee"

classic_location_table = {
    'Classic Mode - Mario Clear': 0x00000000,
    'Classic Mode - Dr. Mario Clear': 0x00000000,
    'Classic Mode - Luigi Clear': 0x00000000,
    'Classic Mode - Peach Clear': 0x00000000,
    'Classic Mode - Bowser Clear': 0x00000000,
    'Classic Mode - Yoshi Clear': 0x00000000,
    'Classic Mode - Donkey Kong Clear': 0x00000000,
    'Classic Mode - Captain Falcon Clear': 0x00000000,
    'Classic Mode - Ganondorf Clear': 0x00000000,
    'Classic Mode - Falco Clear': 0x00000000,
    'Classic Mode - Fox Clear': 0x00000000,
    'Classic Mode - Ness Clear': 0x00000000,
    'Classic Mode - Ice Climbers Clear': 0x00000000,
    'Classic Mode - Kirby Clear': 0x00000000,
    'Classic Mode - Samus Clear': 0x00000000,
    'Classic Mode - Zelda Clear': 0x00000000,
    'Classic Mode - Link Clear': 0x00000000,
    'Classic Mode - Young Link Clear': 0x00000000,
    'Classic Mode - Pichu Clear': 0x00000000,
    'Classic Mode - Pikachu Clear': 0x00000000,
    'Classic Mode - Jigglypuff Clear': 0x00000000,
    'Classic Mode - Mewtwo Clear': 0x00000000,
    'Classic Mode - Mr Game & Watch Clear': 0x00000000,
    'Classic Mode - Marth Clear': 0x00000000,
    'Classic Mode - Roy Clear': 0x00000000,
    'Classic Mode - High Score Total Reached': 0x00000000
}

adventure_location_table = {
    'Adventure Mode - Mario Clear': 0x00000000,
    'Adventure Mode - Dr. Mario Clear': 0x00000000,
    'Adventure Mode - Luigi Clear': 0x00000000,
    'Adventure Mode - Peach Clear': 0x00000000,
    'Adventure Mode - Bowser Clear': 0x00000000,
    'Adventure Mode - Yoshi Clear': 0x00000000,
    'Adventure Mode - Donkey Kong Clear': 0x00000000,
    'Adventure Mode - Captain Falcon Clear': 0x00000000,
    'Adventure Mode - Ganondorf Clear': 0x00000000,
    'Adventure Mode - Falco Clear': 0x00000000,
    'Adventure Mode - Fox Clear': 0x00000000,
    'Adventure Mode - Ness Clear': 0x00000000,
    'Adventure Mode - Ice Climbers Clear': 0x00000000,
    'Adventure Mode - Kirby Clear': 0x00000000,
    'Adventure Mode - Samus Clear': 0x00000000,
    'Adventure Mode - Zelda Clear': 0x00000000,
    'Adventure Mode - Link Clear': 0x00000000,
    'Adventure Mode - Young Link Clear': 0x00000000,
    'Adventure Mode - Pichu Clear': 0x00000000,
    'Adventure Mode - Pikachu Clear': 0x00000000,
    'Adventure Mode - Jigglypuff Clear': 0x00000000,
    'Adventure Mode - Mewtwo Clear': 0x00000000,
    'Adventure Mode - Mr Game & Watch Clear': 0x00000000,
    'Adventure Mode - Marth Clear': 0x00000000,
    'Adventure Mode - Roy Clear': 0x00000000,
    'Adventure Mode - High Score Total Reached': 0x00000000
}

all_star_location_table = {
    'All-Star Mode - Mario Clear': 0x00000000,
    'All-Star Mode - Dr. Mario Clear': 0x00000000,
    'All-Star Mode - Luigi Clear': 0x00000000,
    'All-Star Mode - Peach Clear': 0x00000000,
    'All-Star Mode - Bowser Clear': 0x00000000,
    'All-Star Mode - Yoshi Clear': 0x00000000,
    'All-Star Mode - Donkey Kong Clear': 0x00000000,
    'All-Star Mode - Captain Falcon Clear': 0x00000000,
    'All-Star Mode - Ganondorf Clear': 0x00000000,
    'All-Star Mode - Falco Clear': 0x00000000,
    'All-Star Mode - Fox Clear': 0x00000000,
    'All-Star Mode - Ness Clear': 0x00000000,
    'All-Star Mode - Ice Climbers Clear': 0x00000000,
    'All-Star Mode - Kirby Clear': 0x00000000,
    'All-Star Mode - Samus Clear': 0x00000000,
    'All-Star Mode - Zelda Clear': 0x00000000,
    'All-Star Mode - Link Clear': 0x00000000,
    'All-Star Mode - Young Link Clear': 0x00000000,
    'All-Star Mode - Pichu Clear': 0x00000000,
    'All-Star Mode - Pikachu Clear': 0x00000000,
    'All-Star Mode - Jigglypuff Clear': 0x00000000,
    'All-Star Mode - Mewtwo Clear': 0x00000000,
    'All-Star Mode - Mr Game & Watch Clear': 0x00000000,
    'All-Star Mode - Marth Clear': 0x00000000,
    'All-Star Mode - Roy Clear': 0x00000000,
    'All-Star Mode - High Score Total Reached': 0x00000000
}

event_location_table = {}
event_location_counter = 5500000
event_counter = 0
for event in EVENTDATA:
    event_counter += 1
    event_location_counter += 1
    event_location_table.update({f"Event Match - Clear Event #{event_counter}": event_location_counter})

trophy_location_table = {}
trophy_counter = event_location_counter
path = os.path.join(os.path.dirname(__file__), "data/SSBM Trophies.csv")
with open(path, 'r') as file: 
    trophy_csv = csv.reader(file)
    for row in trophy_csv:
        trophy_counter = trophy_counter + 1
        trophy_location_table.update({f"Trophy Unlocked - {row[1]}": trophy_counter})

character_location_table = {}
character_counter = trophy_counter
chars = get_unlockable_characters()
for character in chars:
    character_counter = character_counter + 1
    character_location_table.update({f"Win Character Unlock Duel - {character}": character_counter})


locations: dict[str, int] = {
    **classic_location_table,
    **adventure_location_table,
    **all_star_location_table,
    **event_location_table,
    **trophy_location_table,
    **character_location_table
}

# PICKUP_LOCATIONS: list[(int, int)] = [
#     (MetroidPrimeLevel.Chozo_Ruins, 0x0002012d),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00020132),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x0002006b),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00020159),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00080077),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00090028),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00090069),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x0009006e),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x000b003e),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x000c002d),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00100004),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00120004),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x001400ee),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00150336),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x001b001a),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x001c002f),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x001c0061),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x001e0173),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00200058),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x002401dd),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x002528ef),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00253094),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00260009),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00290086),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x002927e7),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x002d0023),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x002d00ae),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00300037),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x0030278b),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00310063),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x0031000c),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x003402df),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x003502c9),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x00390004),
#     (MetroidPrimeLevel.Chozo_Ruins, 0x003d0004),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x0002016f),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x00020177),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x00080258),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x000928ee),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x000a00ac),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x000a0192),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x000e0059),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x000f022d),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x001000e3),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x001801cc),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x00190514),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x001b0012),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x001e02f7),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x001f00a6),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x002704d0),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x0028011d),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x00290188),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x003303e1),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x00330412),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x00350021),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x0035012d),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x003600aa),
#     (MetroidPrimeLevel.Phendrana_Drifts, 0x0037001a),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x00000085),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x0004000e),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x000801fc),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x000d00c7),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x000f00fe),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x001001d5),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x00130137),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x00140016),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x001b0116),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x001e02ed),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x00230054),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x0025000e),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x00270037),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x002a0022),
#     (MetroidPrimeLevel.Tallon_Overworld, 0x002a0235),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00020234),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00050188),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00090005),
#     (MetroidPrimeLevel.Phazon_Mines, 0x000c0027),
#     (MetroidPrimeLevel.Phazon_Mines, 0x000d0341),
#     (MetroidPrimeLevel.Phazon_Mines, 0x000d04f2),
#     (MetroidPrimeLevel.Phazon_Mines, 0x000f008e),
#     (MetroidPrimeLevel.Phazon_Mines, 0x0012010e),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00130767),
#     (MetroidPrimeLevel.Phazon_Mines, 0x001600a8),
#     (MetroidPrimeLevel.Phazon_Mines, 0x001a04b9),
#     (MetroidPrimeLevel.Phazon_Mines, 0x001b04b2),
#     (MetroidPrimeLevel.Phazon_Mines, 0x001f0206),
#     (MetroidPrimeLevel.Phazon_Mines, 0x002005eb),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00240128),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00270080),
#     (MetroidPrimeLevel.Phazon_Mines, 0x00280103),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x0004287d),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x0006010d),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x00080010),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x000a0044),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x000b0038),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x000c0029),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x000e01db),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x000e0240),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x00150020),
#     (MetroidPrimeLevel.Magmoor_Caverns, 0x0017028f),
# ]