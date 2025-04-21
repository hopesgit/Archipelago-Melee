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

import pycdlib
import os

import worlds
base_path = worlds.user_path()
print(base_path)


def extract_iso(iso_path, extract_path):
    """Extracts the contents of an ISO file to a specified directory."""
    iso = pycdlib.PyCdlib()
    iso.open(iso_path)

    for root, dirs, files in iso.walk():
        for directory in dirs:
            target_dir = os.path.join(extract_path, *root[1:], directory.name())
            os.makedirs(target_dir, exist_ok=True)
        for file in files:
            target_file = os.path.join(extract_path, *root[1:], file.name())
            with open(target_file, 'wb') as f:
                iso.get_file_from_iso_fp(f, iso_path=os.path.join(*root[1:], file.name()))
    iso.close()

# Example usage

iso_file_path = 'melee.iso'
# extraction_path = 'worlds/ssb_melee/unpack/'
# extract_iso(iso_file_path, extraction_path)