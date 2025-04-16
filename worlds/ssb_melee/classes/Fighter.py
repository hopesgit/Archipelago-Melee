FIGHTERS = {
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

FGROUPS = [
    {
        "name": "starter",
        "fighters": [
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
        "name": "uf1", # first batch of unlockable fighters. Relevant to Event 30
        "fighters": [
            "luigi",
            "jiggly",
            "drmario",
            "falco",
            "ylink"
        ]
    },
    {
        "name": "uf2", # all unlockable fighters
        "fighters": [
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

def get_unlockable_fighters():
    group = FGROUPS[2]["fighters"]
    names = []
    for name in group:
        names.append(FIGHTERS[name])
    return names