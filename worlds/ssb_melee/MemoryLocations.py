MEMORY = {
    'global': {
        0x803B7C08: 'Classic mode continue coin requirements', #0x00 - Very Easy (1 coin required)
        0x803B7C0D: 'Adventure mode continue coin requirements', # same as above
        0x803B7C11: 'All-Star mode continue coin requirements', # same as above (all values in this offset are "0A"
        0x803F0E06: 'P1 Character Select (CSS)',
        0x803F0E2A: 'P2 Character Select (CSS)',
        0x803F0E2C: 'P3 Character Select (CSS)',
        0x803F0E72: 'P4 Character Select (CSS)',
        # above:
        # check offset 0x00 for team info: 00 for Red, 01 for Blue, 02 for Green
        # check 4 bytes at offset 0x02 for each
        # should return something like 0x00010A0A
        # Ex: 00\\01\\0A\\0A
        # Byte 1: Player type: 00 = Human, 01 = CPU, 02 = Demo, 03 = disabled
        # Byte 2: Costume value
        # Byte 3: Character ID
        # Byte 4: Same as byte 3?
    },
    'meleestruct': {
        0x801a583c: {
            "stage_id": 0x0E, #internal stage ID
            "damage_ratio": 0x30, #(float)
            "p1_stocks": 0x62,
            "p1_costume": 0x63,
            "p1_CPU_level": 0x6F
        }
    }
}

