import pathlib
# from ppc_asm.dol_file import DolFile # type: ignore
# from ppc_asm.assembler.ppc import * # type: ignore
#
# dol_file = DolFile(pathlib.Path("main.dol"))
# dol_file.set_editable(True)
# with dol_file:
#     dol_file.write_instructions(
#         0x800857F0,
#         [
#             li(r3, 1),
#             bl(0x80023f28)
#         ]
#     )

import copy
import os
import struct
from typing import TYPE_CHECKING, Dict, List, Tuple

from pycdlib import PyCdlib
import worlds
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes
from settings import get_settings

import pycdlib

from docutils.nodes import literal
from BaseClasses import logging

base_path = worlds.user_path()
print(base_path)


class MeleeProcedurePatch(APProcedurePatch):
    game = "Super Smash Bros. Melee"
    # hash = "605b89b67018abcea91e693a4dd25be3"
    patch_file_ending = ".apssbm"
    result_file_ending = ".iso"

    procedure = [
        ("apply_bsdiff4", ["base_patch.bsdiff4"]),
        ("apply_tokens", ["token_data.bin"])
    ]


class Patcher:
    output_path: literal
    extracted_folder_path: str
    logger: logging.Logger

    def extract_iso(self, iso_path, extract_path):
        """Extracts the contents of an ISO file to a specified directory."""
        self.logger.info('Extracting files from iso...')
        iso = pycdlib.PyCdlib()
        iso.open(iso_path)
        os.mkdir(extract_path)

        for root, dirs, files in iso.walk():
            for directory in dirs:
                target_dir = os.path.join(extract_path, *root[1:], directory.name())
                os.makedirs(target_dir, exist_ok=True)
            for file in files:
                target_file = os.path.join(extract_path, *root[1:], file.name())
                with open(target_file, 'wb') as f:
                    iso.get_file_from_iso_fp(f, iso_path=os.path.join(*root[1:], file.name()))
        iso.close()

    def patch_cstick_in_regular_match(self):
        self.logger.info('Applying patch: C-Stick in Single-Player')
        with os.open(os.path.join(self.extracted_folder_path, "main.dol"), flags=os.O_WRONLY) as dol:
            diff = bsdiff4.diff(48000008, 60000000)
            patch = bsdiff4.file_patch_inplace()

    # def reassemble_iso(self):
    #     iso = PyCdlib.write()


def run():
    iso_file_path = 'melee.iso'
    extraction_path = os.path.curdir + 'unpack/'
    patcher = Patcher()
    patcher.extract_iso(iso_file_path, extraction_path)