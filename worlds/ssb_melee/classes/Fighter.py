from BaseClasses import logging
from typing import List


FIGHTERS = None


class Fighter:
    name: str
    shortname: str
    internal_id: int
    external_id: int
    groups: List[str]
    has_trophies: bool
    selectable: bool


    def __init__(self, name: str, shortname: str, internal_id: int, external_id: int, groups: List, has_trophies=True, selectable=True):
        self.name = name
        self.shortname = shortname
        self.internal_id = internal_id
        self.external_id = external_id
        self.groups = groups
        self.has_trophies = has_trophies
        self.selectable = selectable


    def __getitem__(self, item):
        match item:
            case "name":
                return self.name
            case "shortname":
                return self.shortname
            case "internal_id":
                return self.internal_id
            case "external_id":
                return self.external_id
            case "has_trophies":
                return self.has_trophies
            case "selectable":
                return self.selectable
            case "groups":
                return self.groups


def create_fighters() -> List[Fighter]:
    fighters = list()
    fighters.append(Fighter("Dr. Mario", "drmario", 0x15, 0x16, ["unlock1", "unlock2"]))
    fighters.append(Fighter("Mario", "mario", 0x00, 0x08, ["starter"]))
    fighters.append(Fighter("Luigi", "luigi", 0x11, 0x07, ["unlock1", "unlock2"]))
    fighters.append(Fighter("Peach", "peach", 0x09, 0x0C, ["starter"]))
    fighters.append(Fighter("Bowser", "bowser", 0x05, 0x05, ["starter"]))
    fighters.append(Fighter("Yoshi", "yoshi", 0x0E, 0x11, ["starter"]))
    fighters.append(Fighter("Donkey Kong", "dk", 0x03, 0x01, ["starter"]))
    fighters.append(Fighter("Captain Falcon", "cf", 0x02, 0x00, ["starter"]))
    fighters.append(Fighter("Ganondorf", "ganon", 0x19, 0x19, ["unlock2"]))
    fighters.append(Fighter("Falco", "falco", 0x16, 0x14, ["unlock1", "unlock2"]))
    fighters.append(Fighter("Fox", "fox", 0x01, 0x02, ["starter"]))
    fighters.append(Fighter("Ness", "ness", 0x08, 0x0B, ["starter"]))
    fighters.append(Fighter("Ice Climbers", "ic", 0x0A, 0x0E, ["starter"]))
    fighters.append(Fighter("Kirby", "kirby", 0x03, 0x04, ["starter"]))
    fighters.append(Fighter("Samus", "samus", 0x0D, 0x10, ["starter"]))
    fighters.append(Fighter("Zelda", "zelda", 0x13, 0x12, ["starter"]))
    fighters.append(Fighter("Sheik", "sheik", 0x07, 0x13, ["starter"], selectable=False))
    fighters.append(Fighter("Link", "link", 0x06, 0x06, ["starter"]))
    fighters.append(Fighter("Young Link", "ylink", 0x14, 0x15, ["unlock1", "unlock2"]))
    fighters.append(Fighter("Pichu", "pichu", 0x17, 0x18, ["unlock2"]))
    fighters.append(Fighter("Pikachu", "pika", 0x0C, 0x0D, ["starter"]))
    fighters.append(Fighter("Jigglypuff", "puff", 0x0F, 0x0F, ["unlock1", "unlock2"]))
    fighters.append(Fighter("Mewtwo", "mew2", 0x10, 0x0A, ["unlock2"]))
    fighters.append(Fighter("Mr. Game and Watch", "mgaw", 0x18, 0x03, ["unlock2"]))
    fighters.append(Fighter("Marth", "marth", 0x12, 0x09, ["unlock2"]))
    fighters.append(Fighter("Roy", "roy", 0x1A, 0x17, ["unlock2"]))
    fighters.append(Fighter("Choose", "choose", 0x21, 0x21, ["locked"], has_trophies=False, selectable=False)) # used for Event Match
    fighters.append(Fighter("Giga Bowser", "giga", 0x1F, 0x1D, ["special"], has_trophies=False, selectable=False))
    fighters.append(Fighter("Master Hand", "master", 0x1B, 0x1A, ["special"], has_trophies=False, selectable=False))
    fighters.append(Fighter("Crazy Hand", "crazy", 0x1C, 0x1E, ["special"], has_trophies=False, selectable=False))
    fighters.append(Fighter("Sandbag", "sandbag", 0x20, 0x1F, ["special"], has_trophies=False, selectable=False))
    fighters.append(Fighter("Male Wireframe", "mwire", 0x1D, 0x1B, ["special"], has_trophies=False, selectable=False))
    fighters.append(Fighter("Female Wireframe", "fwire", 0x1E, 0x1C, ["special"], has_trophies=False, selectable=False))
    logging.info(f"Fighter.py - create_fighters - fighters obj is: {fighters}")
    return fighters


def query_fighter_list(field: str, query):
    """Possible fields:

    - name
    - shortname
    - internal_id
    - external_id
    - groups
    - has_trophies
    - selectable

    If groups is the field, pass in a group name as query to search for that group.

    Acceptable groups:

    - starter
    - unlock1
    - unlock2
    - locked
    - special"""
    field_list = ["name", "shortname", "internal_id", "external_id", "has_trophies", "selectable", "groups"]
    names = []
    fighters = setup()
    logging.info(f"Fighter.py - query_fighter_list - fighters obj is: {fighters}")
    if field in field_list:
        if field != "groups" and query:
            for f in fighters:
                if f[field] == query:
                    names.append(f.name)
        elif field == "groups" and query:
            for f in fighters:
                if query in f.groups:
                    names.append(f.name)
    return names


def get_fighter_from_internal_id(id: int):
    query_fighter_list("internal_id", id)


def get_fighter_from_external_id(id: int):
    query_fighter_list("external_id", id)


def get_fighters_with_trophies():
    query_fighter_list("has_trophies", True)


def get_starter_fighters():
    query_fighter_list("groups", "starter")


def get_unlockable_fighters():
    query_fighter_list("groups", "unlock2")

def setup():
    fighters = create_fighters()
    return fighters