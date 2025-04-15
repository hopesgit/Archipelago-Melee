CHARACTERS = {
    "drmario": "Dr. Mario",
    "mario": "Mario",
    "luigi": "Luigi",
    "peach": "Peach",
    "bowser": "Bowser",
    "yoshi": "Yoshi",
    "dk": "Donkey Kong",
    "cf": "Captain Falcon",
    "ganon": "Ganondorf",
    "falco": "Falco",
    "fox": "Fox",
    "ness": "Ness",
    "ic": "Ice Climbers",
    "kirby": "Kirby",
    "samus": "Samus",
    "zelda": "Zelda",
    "link": "Link",
    "ylink": "Young Link",
    "pichu": "Pichu",
    "pikachu": "Pikachu",
    "jiggly": "Jigglypuff",
    "mew2": "Mewtwo",
    "mgaw": "Mr Game & Watch",
    "marth": "Marth",
    "roy": "Roy"
}

CHARGROUPS = [
    {
        "name": "starter",
        "chars": [
            "mario",
            "yoshi",
            "dk",
            "fox", 
            "kirby",
            "link",
            "pikachu",
            "samus",
            "bowser",
            "cf",
            "ic",
            "ness",
            "peach",
            "zelda"
        ]
    },
    {
        "name": "uchar1", # first batch of unlockable characters. Relevant to Event 30
        "chars": [
            "luigi",
            "jiggly",
            "drmario",
            "falco",
            "ylink"
        ]
    },
    {
        "name": "uchar2", # all unlockable chars
        "chars": [
            "luigi",
            "jiggly",
            "drmario",
            "falco",
            "ylink",
            "ganon",
            "marth",
            "roy",
            "mew2",
            "mgaw",
            "pichu",
        ]
    }
]

def get_unlockable_characters():
    group = CHARGROUPS[2]["chars"]
    names = []
    for name in group:
        names.append(CHARACTERS[name])
    return names