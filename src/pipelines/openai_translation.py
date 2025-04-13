from pathlib import Path

from src.services.external_tools.lslib_service import LslibService


def openai_translation(file_path: Path, source_language: str):
    loc_files = LslibService.unpack_pak_localization_files(
        file_path=Path(file_path), 
        source_language=source_language,
    )

    xml_files = []
    for loc_file in loc_files:
        if loc_file.suffix == '.xml':
            xml_files.append(loc_file)
        if loc_file.name == 'meta.lsx':
            meta_file = loc_file
    