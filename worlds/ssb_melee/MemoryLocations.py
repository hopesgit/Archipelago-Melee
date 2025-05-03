# if you insert a blr command at 80173eec, special messages die

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
    },
    'p1data': 0x80453080,
    'p2data': 0x80453f10,
    'p3data': 0x8045ADA0,
    'p4data': 0x80455c30,
    'p5data': 0x80456ac0,
    'p6data': 0x80457950,
    'player_offsets': { # apply these to thee pxdata sets above
        0x00: int, # player state. 0x02 for in-game (including dead). 0x00 otherwise.
        0x04: int, # player character (external id)
        0x0A: int, # slot type. 0x00 for human, 0x01 for cpu, 0x02 for demo, 0x03 for n/a
        0x38: float, # model scale - factors into damage?
        0x44: bytes, # costume id
        0x47: bytes, # team id. 00 = red, 01 = blue, 02 = green
        0x48: bytes, # player id. Not really sure what this is supposed to do
        0x50: float, # attack ratio
        0x54: float, # knockback ratio
        0x58: float, # damage defense ratio
        0x68: int, # falls
        0x70: int, # p1 KOs
        0x74: int, # p2 KOs
        0x78: int, # p3 KOs
        0x7c: int, # p4 KOs
        0x80: int, # p5 KOs
        0x84: int, # p6 KOs
        0x8c: int, # self-destructs
        0xac: bytes, # 0x40 = true
        0xbc: int, # stale move table write index
        0xc0: bytes, # not really sure on this one. 1st short is move ID, 2nd short is # of action states. anyway, SM index 0
        0xc4: bytes, # stale moves index 1
        0xc8: bytes, # stale moves index 2
        0xcc: bytes, # stale moves index 3
        0xd0: bytes, # stale moves index 4
        0xd4: bytes, # stale moves index 5
        0xd8: bytes, # stale moves index 6
        0xdc: bytes, # stale moves index 7
        0xe0: bytes, # stale moves index 8
        0xe4: bytes, # stale moves index 9
    },
    'stage_struct': {
        0x8049e6c8: {
            0x88: bytes, # internal stage id
            0x6D4: bytes, # number of targets remaining in BTT
            0x6e0: float, # HRC distance. This is a coordinate offset rather than the distance normally seen
            # which coordinate? maybe the p2 spawn point, or maybe the right edge of the platform
        }
    },
    'hrc': 80472e48, # no notes given
}

