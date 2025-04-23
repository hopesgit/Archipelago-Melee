class SpecialBonus:
    """Class that handles the special bonuses that are achievable in the
    different modes. Some give more points than others, so watch out!"""
    name: str
    points_given: int
    requirement: str
    repeatable: bool

    def __init__(self, name, points_given, requirement, repeatable):
        self.name = name
        self.points_given = points_given
        self.requirement = requirement
        self.repeatable = repeatable


import csv
from pathlib import Path

current_file_path = Path(__file__).resolve()
parent_dir_path = current_file_path.parent.parent
path = parent_dir_path / "data/Melee Special Bonuses.csv"
bonuses = []
i = 0
with open(path, 'r') as file:
    bonus_csv = csv.reader(file)
    for row in bonus_csv:
        i += 1
        if i == 1: continue
        repeat = False
        amount = row[1]
        try:
            amount = int(amount)
        except ValueError:
            repeat = True
            amount = int(row[1].replace(",", "")[:-3])
        bonus = SpecialBonus(row[0], amount, row[2], repeat)
        bonuses.append(bonus)
BONUSES = bonuses

