from src.services.external_tools.lslib_service import LslibService
from config import paths

paths.PACKED.mkdir(exist_ok=True, parents=True)

LslibService.mod_pack(
    input_folder='C:\\Users\\jonat\\Desktop\\projects\\Asmodeus-Translator-Desktop\\mods\\translated\\chaos_and_control_sorcerer_equipment_ptbr\\',
    output_folder=paths.PACKED
)