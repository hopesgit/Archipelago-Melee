import io

from typing import Dict
from settings import get_settings

class SSBMPatcher:

    def __init__(self):
        from gclib.gcm import GCM
        from gclib.dol import DOL
        self.iso = GCM(get_settings().ttyd_options.iso_file)
        self.iso.read_entire_disc()
        self.dol = DOL()
        self.dol.read(self.iso.read_file_data('sys/main.dol'))