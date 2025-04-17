from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


DATA = ROOT / 'data'

TEMP = DATA / 'temp'
TEMP_UNPACKED = TEMP / 'unpacked'


EXTERNAL_TOOLS = ROOT / 'external_tools'
LSLIB = EXTERNAL_TOOLS / 'lslib'
DIVINE = LSLIB / 'Divine.exe'


MODS = ROOT / 'mods'
UNPACKED = MODS / 'unpacked'
PACKED = MODS / 'packed'
TRANSLATED = MODS / 'translated'
