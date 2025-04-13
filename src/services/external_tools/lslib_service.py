import subprocess
from pathlib import Path
import shutil

from config.paths import DIVINE, UNPACKED, PACKED, TEMP
from src.utils.dir_utils import DirUtils
from src.utils.zip_utils import ZipUtils


class LslibService:

    @staticmethod
    def _list_translation_files(folder: Path, language: str) -> list[Path]:
        xml_files = DirUtils.list_files_by_extension(folder, 'xml')
        loc_files = []
        for xml in xml_files:
            if xml.parent.name == language:
                loc_files.append(xml)
        
        lsx_files = DirUtils.list_files_by_extension(folder, 'lsx')
        for lsx in lsx_files:
            if lsx.name == 'meta.lsx':
                loc_files.append(lsx)
                break

        return loc_files


    @staticmethod
    def unpack_pak_file(file_path: Path, temp: bool = False) -> None:
        file_path = Path(file_path)

        if file_path.suffix == '.zip':
            temp_folder = TEMP / (str(file_path.stem) + '_zip')
            temp_folder.mkdir(parents=True, exist_ok=True)
            ZipUtils.unpack_zip_file(file_path, temp_folder)
            file_path = DirUtils.list_files_by_extension(temp_folder, 'pak')[0]
            clear_temp = True

        if file_path.suffix != '.pak':
            raise ValueError(f'Invalid file type: {file_path.suffix}. Expected .pak or .zip.')


        output_folder = UNPACKED / file_path.stem
        if temp:
            output_folder = TEMP / file_path.stem
        output_folder.mkdir(parents=True, exist_ok=True)

        command = [
            DIVINE, 
            '-g', 'bg3', 
            '-a', 'extract-package', 
            '-s', file_path, 
            '-d', output_folder
        ]

        try:
            subprocess.run(command, check=True)
            if clear_temp:
                shutil.rmtree(temp_folder)

        except subprocess.CalledProcessError as e:
            print(f'An error occurred while unpacking the pak file: {e}')
            raise

        except FileNotFoundError as e:
            print(f'Divine executable not found: {e}')
            raise

    
    @staticmethod
    def unpack_pak_localization_files(file_path: Path, source_language: str) -> list[Path]:
        file_path = Path(file_path)
        LslibService.unpack_pak_file(file_path, temp=True)

        folder_name = file_path.stem
        temp_folder = TEMP / folder_name
        print(temp_folder)
        output_folder = UNPACKED / folder_name
        output_folder.mkdir(parents=True, exist_ok=True)

        loc_files = LslibService._list_translation_files(temp_folder, source_language)

        for file in loc_files:
            relative_path = file.relative_to(temp_folder)
            dest_path = output_folder / relative_path

            dest_path.parent.mkdir(parents=True, exist_ok=True)

            print(f'[DEBUG] Copiando {file} -> {dest_path}')
            shutil.copy2(file, dest_path)
        
        shutil.rmtree(temp_folder)
        return loc_files
