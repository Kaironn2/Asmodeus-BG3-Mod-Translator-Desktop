import zipfile


class ZipUtils:

    @staticmethod
    def unpack_zip_file(file_path: str, destination: str) -> None:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
