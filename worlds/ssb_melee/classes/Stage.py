from enum import Enum

STAGES = {
    'Princess Peach\'s Castle': {
        'internalid': 0x02,
        'scenarioid': [4, 86, 108, 110, 155, 190, 222, 255, 279],
    },
    'Rainbow Cruise': {
        'internalid': 0x03,
        'scenarioid': [11, 87, 165, 177, 214, 256],
    },
    'Kongo Jungle (GC)': {
        'internalid': 0x04,
        'scenarioid': [5, 61, 88, 127, 156, 178, 219, ],
    },
    'Jungle Japes': {
        'internalid': 0x05,
        'scenarioid': [12, 89, 166, 196, 218, 253],
    },
    'Great Bay': {
        'internalid': 0x06,
        'scenarioid': [13, 90, 113, 119, 123, 129, 131, 152, 154, 157, 179, 210, 235, 257, 270, 281],
    },
    'Hyrule Temple': {
        'internalid': 0x07,
        'scenarioid': [14, 91, 112, 120, 128, 151, 153, 164, 191, 203, 230, 241, 242, 247, 258, 271, 284],
    },
    'Brinstar': {
        'internalid': 0x08,
        'scenarioid': [6, 92, 133, 180, 209, 221],
    },
    'Brinstar Depths': {
        'internalid': 0x09,
        'scenarioid': [15, 93, 201, 224],
    },
    'Yoshi\'s Story': {
        'internalid': 0x0A,
        'scenarioid': [8, 94, 134, 158, 181, 205, 249, 254],
    },
    'Yoshi\'s Island (GC)': {
        'internalid': 0x0B,
        'scenarioid': [16, 95, 135, 194, 211, 225],
    },
    'Yoshi\'s Island (N64)': {
        'internalid': 0x1D,
        'scenarioid': [29],
    },
    'Fountain of Dreams': {
        'internalid': 0x0C,
        'scenarioid': [2, 96, 137, 162, 167, 192, 207, 231, 238, 277],
    },
    'Green Greens': {
        'internalid': 0x0D,
        'scenarioid': [17, 97, 136, 138, 182, 229],
    },
    'Corneria': {
        'internalid': 0x0E,
        'scenarioid': [7, 70, 71, 98, 121, 140, 183, 217, 233, 260],
    },
    'Venom': {
        'internalid': 0x0F,
        'scenarioid': [22, 99, 122, 197, 228, 268],
    },
    'Pokemon Stadium': {
        'internalid': 0x10,
        'scenarioid': [3, 72, 100, 107, 115, 124, 142, 143, 161, 170, 172, 184, 208, 240, 261, 269, 274, 283],
    },
    'Poke Floats': {
        'internalid': 0x11,
        'scenarioid': [23, 188, 243, 265],
    },
    'Mute City': {
        'internalid': 0x12,
        'scenarioid': [10, 74, 103, 141, 160, 174, 186, 213, 259],
    },
    'Big Blue': {
        'internalid': 0x13,
        'scenarioid': [24, 104, 132, 147, 244],
    },
    'Onett': {
        'internalid': 0x14,
        'scenarioid': [9, 75, 105, 145, 169, 187, 206, 262],
    },
    'Fourside': {
        'internalid': 0x15,
        'scenarioid': [18, 106, 146, 198, 226, 237],
    },
    'Icicle Mountain': {
        'internalid': 0x16,
        'scenarioid': [25, 76, 116, 117, 139, 171, 189, 212, 263],
    },
    'Mushroom Kingdom I': {
        'internalid': 0x18,
        'scenarioid': [19, 101, 118, 130, 144, 163, 185, 232, 250],
    },
    'Mushroom Kingdom II': {
        'internalid': 0x19,
        'scenarioid': [20, 102, 111, 126, 159, 168, 195, 223, 239, 264, 276],
    },
    'Flat Zone': {
        'internalid': 0x1B,
        'scenarioid': [27, 173, 200, 246, 267, 278],
    },
    'Dream Land (N64)': {
        'internalid': 0x1C,
        'scenarioid': [28, 236],
    },
    'Kongo Jungle (N64)': {
        'internalid': 0x1E,
        'scenarioid': [30],
    },
    'Battlefield': {
        'internalid': 0x24,
        'scenarioid': [31, 109, 125, 148, 149, 150, 175, 193, 202, 216, 245, 273, 282, 285],
    },
    'Final Destination': {
        'internalid': 0x25,
        'scenarioid': [32, 114, 176, 199, 220, 251, 252, 266, 272, 275, 280],
    },
    'Snag Trophies!': {
        'internalid': 0x26,
        'scenarioid': [83],
    },
    'Race to the Finish': {
        'internalid': 0x27,
        'scenarioid': [82]
    },
    'Adventure - Mario Adventure': {
        'internalid': 0x1F,
        'scenarioid': [59]
    },
    'Adventure - Underground Maze': {
        'internalid': 0x20,
        'scenarioid': [63]
    },
    'Adventure - Zebes Escape': {
        'internalid': 0x21,
        'scenarioid': [66]
    },
    'Adventure - Grand Prix': {
        'internalid': 0x22,
        'scenarioid': [73]
    },
    'Target Test - Dr. Mario': {
        'internalid': 0x2C,
        'scenarioid': [37]
    },
    'Target Test - Mario': {
        'internalid': 0x28,
        'scenarioid': [33]
    },
    'Target Test - Luigi': {
        'internalid': 0x33,
        'scenarioid': [44]
    },
    'Target Test - Bowser': {
        'internalid': 0x31,
        'scenarioid': [42]
    },
    'Target Test - Peach': {
        'internalid': 0x37,
        'scenarioid': [48]
    },
    'Target Test - Yoshi': {
        'internalid': 0x3D,
        'scenarioid': [54]
    },
    'Target Test - DK': {
        'internalid': 0x2B,
        'scenarioid': [36]
    },
    'Target Test - CF': {
        'internalid': 0x29,
        'scenarioid': [34]
    },
    'Target Test - Ganondorf': {
        'internalid': 0x41,
        'scenarioid': [58]
    },
    'Target Test - Falco': {
        'internalid': 0x2D,
        'scenarioid': [38]
    },
    'Target Test - Fox': {
        'internalid': 0x2E,
        'scenarioid': [39]
    },
    'Target Test - Ness': {
        'internalid': 0x36,
        'scenarioid': [47]
    },
    'Target Test - Ice Climbers': {
        'internalid': 0x2F,
        'scenarioid': [40]
    },
    'Target Test - Kirby': {
        'internalid': 0x30,
        'scenarioid': [41]
    },
    'Target Test - Samus': {
        'internalid': 0x3B,
        'scenarioid': [52]
    },
    'Target Test - Zelda/Sheik': {
        'internalid': 0x3E,
        'scenarioid': [53, 55]
    },
    'Target Test - Link': {
        'internalid': 0x32,
        'scenarioid': [43]
    },
    'Target Test - Young Link': {
        'internalid': 0x2A,
        'scenarioid': [35]
    },
    'Target Test - Pichu': {
        'internalid': 0x38,
        'scenarioid': [49]
    },
    'Target Test - Pikachu': {
        'internalid': 0x39,
        'scenarioid': [50]
    },
    'Target Test - Jigglypuff': {
        'internalid': 0x3A,
        'scenarioid': [51]
    },
    'Target Test - Mewtwo': {
        'internalid': 0x35,
        'scenarioid': [46]
    },
    'Target Test - Game & Watch': {
        'internalid': 0x3F,
        'scenarioid': [56]
    },
    'Target Test - Marth': {
        'internalid': 0x34,
        'scenarioid': [45]
    },
    'Target Test - Roy': {
        'internalid': 0x40,
        'scenarioid': [57]
    },
    'All-Star Rest Area': {
        'internalid': 42,
        'scenarioid': [85]
    },
    'Home Run Contest': {
        'internalid': 0x43,
        'scenarioid': [84]
    },
    'Event - Goomba': {
        'internalid': 0x44,
        'scenarioid': [215]
    },
    'Event - Entei': {
        'internalid': 0x45,
        'scenarioid': [227]
    },
    'Event - Majora\'s Mask': {
        'internalid': 0x46,
        'scenarioid': [248]
    },
}


def get_stage_by_internal_id(id: int):
    for name, ids in STAGES.items():
        if ids['internalid'] == id:
            return name

def get_stage_by_scenario_id(id: int):
    for name, ids in STAGES.items():
        if id in ids['scenarioid']:
            return name