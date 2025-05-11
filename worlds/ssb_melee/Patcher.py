import os
import re
import shutil
import struct
from collections import OrderedDict

import bsdiff4

from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from BaseClasses import logging


class MeleeProcedurePatch(APProcedurePatch):
    game = "Super Smash Bros. Melee"
    # hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apssbm"
    result_file_ending = ".iso"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        # ("apply_tokens", ["token_data.bin"])
    ]


# Key = target widget, value = tuple of "(tableOffset, gameDefault, tourneyDefault [, str translations])".
# The gameDefault and tourneyDefault integers are indexes, relating to the string portion of the tuple (if it has a string portion).
# If the tuple doesn't have a string portion, then the values are instead the direct value for the setting (e.g. 3 stock or 4 stock).
settingsTableOffset = {'NTSC 1.00': 0x3CFB90, 'NTSC 1.01': 0x3D0D68, 'NTSC 1.02': 0x3D1A48, 'NTSC 1.03': 0x3D1A48,
                       'PAL 1.00': 0x3D20C0}
gameSettingsTable = {
    'gameModeSetting': (2, 0, 1, 'Time', 'Stock', 'Coin', 'Bonus'),  # AA
    'gameTimeSetting': (3, 2, 2),  # BB
    'stockCountSetting': (4, 3, 4),  # CC
    'handicapSetting': (5, 0, 0, 'Off', 'Auto', 'On'),  # DD
    'damageRatioSetting': (6, 1.0, 1.0),  # EE
    'stageSelectionSetting': (7, 0, 0, 'On', 'Random', 'Ordered', 'Turns', 'Loser'),  # FF
    'stockTimeSetting': (8, 0, 8),  # GG
    'friendlyFireSetting': (9, 0, 1, 'Off', 'On'),  # HH
    'pauseSetting': (10, 1, 0, 'Off', 'On'),  # II
    'scoreDisplaySetting': (11, 0, 1, 'Off', 'On'),  # JJ
    'selfDestructsSetting': (12, 0, 0, '-1', '0', '-2'),  # KK
    'itemFrequencySetting': (24, 3, 0, 'None', 'Very Low', 'Low', 'Medium', 'High',
                             'Very High', 'Extremely High'),  # PP
    'itemToggleSetting': (36, 'FFFFFFFF', '00000000'),
    'p1RumbleSetting': (40, 1, 0, 'Off', 'On'),  # R1
    'p2RumbleSetting': (41, 1, 0, 'Off', 'On'),  # R2
    'p3RumbleSetting': (42, 1, 0, 'Off', 'On'),  # R3
    'p4RumbleSetting': (43, 1, 0, 'Off', 'On'),  # R4
    # 'soundBalanceSetting': 	(44, 0, 0),													# MM
    # 'deflickerSetting': 		(45, 1, 1, 'Off', 'On'),									# SS
    # 'languageSetting': 		(46, ),	# Game ignores this in favor of system default?		# LL
    'stageToggleSetting': (48, 'FFFFFFFF', 'E70000B0')  # TT
    # 'bootToSetting':			()
    # 'dbLevelSetting': 		()
}


class Patcher:
    """This class is used to generate the base_patch.bsdiff4"""
    vanilla_iso_path: os.path
    input_iso_path: os.path
    output_iso_path: os.path
    dol_data = ''
    region = ''
    game_id = ''
    disc_version = ''
    offset = ''
    is_valid_melee_iso = False
    version = ''

    def __init__(self):
        base_path = os.path.curdir
        extract_path = os.path.join(base_path, 'extract')
        vanilla_path = os.path.join(extract_path, 'vanilla.iso')
        input_path = os.path.join(extract_path, 'input.iso')
        output_path = os.path.join(extract_path, 'output.iso')
        self.vanilla_iso_path = vanilla_path
        self.input_iso_path = input_path
        self.output_iso_path = output_path
        self.base_patch_bytes = bytes()
        self.base_patch_path = os.path.join(extract_path, 'base_patch.bsdiff4')

    def get_dol_data_from_iso(self, iso_path):
        with open(iso_path, 'rb') as iso:
            self.game_id = iso.read(6).decode('ascii')
            game_id = re.compile('GA[A-Z]E01')
            if not game_id.match(self.game_id): raise FileExistsError('extract/vanilla.iso exists, but it is the wrong game.'
                                                                      f'The provided game id is {self.game_id}.')
            iso.seek(1, 1)
            version_hex = iso.read(1).hex()
            region_code = self.game_id[3]
            ntsc_regions = ('A', 'E', 'J', 'K', 'R', 'W')
            if region_code in ntsc_regions:
                self.region = 'NTSC'
            else:
                self.region = 'PAL'
            self.disc_version = '1.' + version_hex

            iso.seek(0x0420)
            self.offset = struct.unpack('>I', iso.read(4))[0]  # Should be 0x1E800 for SSBM NTSC v1.02
            print(f"Self.offset is {self.offset} and is type {type(self.offset)}")
            toc_offset = struct.unpack('>I', iso.read(4))[0]
            print(f"toc_offset is {toc_offset} and is type {type(toc_offset)}")

            dol_length = toc_offset - self.offset  # Should be 0x438600 for SSBM NTSC v1.02
            # dol_length = self.offset - toc_offset
            print(f"dol_length is {dol_length} and is type {type(dol_length)}")
            iso.seek(self.offset)
            self.dol_data = iso.read(dol_length).hex()
        iso.close()

    def verify_vanilla_iso(self) -> None:
        print('Checking for vanilla.iso...')
        iso = os.path.exists(self.vanilla_iso_path)
        if not iso: raise FileNotFoundError('Error: "extract/vanilla.iso" file not found.')

        self.get_dol_data_from_iso(self.vanilla_iso_path)

        ssbm_string_bytes = bytearray(b'Super Smash Bros. Melee')
        string_loc_bytes = bytearray.fromhex(self.dol_data)
        if string_loc_bytes[0x3B78FB:0x3B7912] == ssbm_string_bytes:
            self.region = 'NTSC'
            self.version = '1.02'  # most common, so checking for it first
        elif string_loc_bytes[0x3B6C1B:0x3B6C32] == ssbm_string_bytes:
            self.region = 'NTSC'
            self.version = '1.01'
        elif string_loc_bytes[0x3B5A3B:0x3B5A52] == ssbm_string_bytes:
            self.region = 'NTSC'
            self.version = '1.00'
        elif string_loc_bytes[0x3B75E3:0x3B75FA] == ssbm_string_bytes:
            self.region = 'PAL'
            self.version = '1.00'
        else:
            self.region = self.version = ''
            return

        self.is_valid_melee_iso = True
        print(f'ISO version detected: {self.region} {self.version}')

    def copy_vanilla_iso(self) -> None:
        self.verify_vanilla_iso()
        if not self.is_valid_melee_iso:
            raise FileExistsError('Error: "extract/vanilla.iso" file exists, but is invalid. '
                                  'Be sure that you use a good dump that is completely unmodified. '
                                  'You can check your vanilla iso\'s dump status at redump.org or '
                                  'by using Dolphin\'s file verification utility.')
        if os.path.exists(self.input_iso_path):
            print('Deleting stale input.iso...')
            os.remove(self.input_iso_path)
        print('Creating input.iso...')
        shutil.copy(self.vanilla_iso_path, self.input_iso_path)

        if os.path.exists(self.output_iso_path):
            print('Deleting stale output.iso...')
            os.remove(self.output_iso_path)
        print('Creating output.iso...')
        shutil.copy(self.vanilla_iso_path, self.output_iso_path)

    def create_base_patch(self):
        ap_text = bytes(b'Archipelago')
        ap_text_length = len(ap_text)
        ap_text_offset = 0x08 + ap_text_length
        diff = bsdiff4.diff(self.dol_data[0x08:0x19], ap_text)
        self.base_patch_bytes.join(diff)


    def patch_cstick_in_regular_match(self, selection: bool):
        if not selection: return
        print('Applying patch: C-Stick in Single-Player')
        input_iso = self.input_iso_path
        diff = bsdiff4.diff(48000008, 60000000)
        patch = bsdiff4.file_patch_inplace(main, diff)


def run(cstick: bool = True):
    patcher = Patcher()
    patcher.copy_vanilla_iso()
    patcher.patch_cstick_in_regular_match(cstick)


def from_cmd_terminal():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('--cstick',
                        action='store_const', const=True,
                        help="add this flag to use the cstick patch")
    args = parser.parse_args()
    run(args.cstick)


if __name__ == '__main__':
    from_cmd_terminal()
