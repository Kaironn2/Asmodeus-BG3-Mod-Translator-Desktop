from pathlib import Path

from src.services.external_tools.lslib_service import LslibService


class OpenAITranslationPipeline:

    def __init__(
        self, 
        source_language: str, 
        target_language: str,
        mod_path: Path,
    ) -> None:
        self.source_language = source_language
        self.target_language = target_language
        self.file_path = mod_path

    
    def mod_unpack(self, file_path: Path, source_language: str):

        loc_files = LslibService.unpack_pak_localization_files(file_path)

        self.xml_files = []
        for loc_file in loc_files:
            if loc_file.name == 'meta.lsx':
                self.meta_file = loc_file
            self.xml_files.append(loc_file)

    
    def create_meta(self, meta_path: Path, author: str, description: str):
        pass