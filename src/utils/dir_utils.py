from pathlib import Path


class DirUtils:

    @staticmethod
    def list_files_by_extension(directory: Path, extension: str = 'pak') -> list[Path]:
        return list(directory.rglob(f'*.{extension}'))
