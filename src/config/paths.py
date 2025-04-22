import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent.parent


DATA = ROOT / 'data'

TEMP = DATA / 'temp'
TEMP_UNPACKED = TEMP / 'unpacked'


CONFIGS = ROOT / 'configs'
JSON_CONFIG = CONFIGS / 'config.json'


EXTERNAL_TOOLS = ROOT / 'external_tools'
LSLIB = EXTERNAL_TOOLS / 'lslib'
DIVINE = LSLIB / 'Divine.exe'


# Paths for dist
DIST_ROOT = ROOT.parent
MODS = DIST_ROOT / 'mods'
UNPACKED = MODS / 'unpacked'
PACKED = MODS / 'packed'
TRANSLATED = MODS / 'translated'


# Resources
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller extrai para uma pasta temporária e coloca o caminho em _MEIPASS
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath('.')
    return os.path.join(base_path, relative_path)
