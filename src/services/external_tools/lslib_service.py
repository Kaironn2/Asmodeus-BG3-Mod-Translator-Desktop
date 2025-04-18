from pathlib import Path
import subprocess
import shutil
import zipfile

from sqlmodel import Session

from config import paths
from src.database.repositories.language_repository import LanguageRepository
from src.helpers.validators import Validators
from src.utils.dir_utils import DirUtils
from src.utils.zip_utils import ZipUtils


class LslibService:

    @classmethod
    def mod_unpack(
        cls, mod_path: Path, mod_name: str, just_localization: bool, 
        session: Session, source_language: str, target_language: str
        ) -> tuple[list[Path], Path]:

        paths.TEMP_UNPACKED.mkdir(exist_ok=True, parents=True)

        mod_path = Path(mod_path)

        if mod_path.suffix == '.zip':
            ZipUtils.unpack_zip_file(mod_path, paths.TEMP_UNPACKED)
            mod_path = DirUtils.list_files_by_extension(paths.TEMP_UNPACKED, 'pak')[0]

        if mod_path.suffix != '.pak':
            raise ValueError(f'Invalid file type: {mod_path.suffix}. Expected .pak or .zip.')
        
        if not just_localization:
            cls._divine_unpack(mod_path, paths.UNPACKED / mod_name)
            shutil.rmtree(paths.TEMP_UNPACKED)
            return

        cls._divine_unpack(mod_path, paths.TEMP_UNPACKED)
        xml_files, meta_file = cls._list_localization_files(paths.TEMP_UNPACKED, source_language, session)

        target_language = LanguageRepository.find_language_by_code(session, target_language).replace(' ', '')


        output_path = paths.UNPACKED / mod_name / 'Mods' / mod_name
        xml_outputs = []
        for xml in xml_files:
            xml_name = str(xml.name).replace('.loca', '')
            xml_output_path = output_path / 'Localization' / target_language / xml_name
            xml_output_path.parent.mkdir(parents=True, exist_ok=True)
            xml_outputs.append(xml_output_path)
            shutil.copy2(xml, xml_output_path)
        
        meta_output_file = output_path / 'meta.lsx'
        shutil.copy2(meta_file, meta_output_file)
        shutil.rmtree(paths.TEMP_UNPACKED)
        return xml_outputs, meta_output_file
    

    @classmethod
    def mod_pack(cls, input_folder: Path, output_folder: Path):
        input_folder = Path(input_folder)
        output_folder = Path(output_folder)
        output_folder.mkdir(exist_ok=True, parents=True)

        if not input_folder.exists() or not input_folder.is_dir():
            raise ValueError(f'Invalid input folder: {input_folder}')

        if not output_folder.exists() or not output_folder.is_dir():
            raise ValueError(f'Invalid output folder: {output_folder}')

        mod_name = input_folder.name
        mod_path = output_folder / f'{mod_name}.pak'
        zip_path = output_folder / f'{mod_name}.zip'

        cls._divine_pack(input_folder, mod_path)

        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(mod_path, arcname=mod_path.name)

        return mod_path


    @classmethod
    def _divine_unpack(cls, mod_path: Path, output_folder: Path):
        command = [
            paths.DIVINE, 
            '-g', 'bg3', 
            '-a', 'extract-package', 
            '-s', mod_path, 
            '-d', output_folder,
        ]

        try:
            subprocess.run(command, check=True)

        except subprocess.CalledProcessError as e:
            print(f'An error occurred while unpacking the pak file: {e}')
            raise

        except FileNotFoundError as e:
            print(f'Divine executable not found: {e}')
            raise

    
    @classmethod
    def _divine_pack(cls, mod_folder: Path, output_folder: Path):
        command = [
            paths.DIVINE, 
            '-g', 'bg3', 
            '-a', 'create-package', 
            '-s', mod_folder, 
            '-d', output_folder,
        ]

        try:
            subprocess.run(command, check=True)

        except subprocess.CalledProcessError as e:
            print(f'An error occurred while packing the pak file: {e}')
            raise

        except FileNotFoundError as e:
            print(f'Divine executable not found: {e}')
            raise

    
    @classmethod
    def _list_localization_files(cls, folder: Path, source_language: str, session: Session) -> tuple[list[Path], Path]:
        source_language = LanguageRepository.find_language_by_code(session, source_language)
        
        xml_files = DirUtils.list_files_by_extension(folder, 'xml')
        loc_files = []
        for xml in xml_files:
            if xml.parent.name == source_language:
                loc_files.append(xml)
        
        lsx_files = DirUtils.list_files_by_extension(folder, 'lsx')
        for lsx in lsx_files:
            if lsx.name == 'meta.lsx':
                meta_file = lsx

        return loc_files, meta_file
