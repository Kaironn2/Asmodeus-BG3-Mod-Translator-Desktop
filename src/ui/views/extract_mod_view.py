from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QLabel
from src.ui.components.drag_drop import DragDropWidget

from src.services.external_tools.lslib_service import LslibService


class ExtractModView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.drag_drop = DragDropWidget(
            accepted_extensions=['.zip', '.pak'],
            description_text='Drag and drop your\n .ZIP or .PAK file here\nor click to select'
        )
        self.drag_drop.file_dropped.connect(self.on_file_dropped)
        layout.addWidget(self.drag_drop)
        self.status_label = QLabel('')
        layout.addWidget(self.status_label)

    def on_file_dropped(self, file_path):
        from pathlib import Path
        import shutil
        from src.config import paths
        from src.utils.zip_utils import ZipUtils
        from src.utils.dir_utils import DirUtils

        dest_dir = QFileDialog.getExistingDirectory(
            self,
            'Select extraction folder'
        )
        if not dest_dir:
            self.status_label.setText('Extraction cancelled.')
            return

        file_path = Path(file_path)
        subfolder_name = file_path.stem
        final_dest = Path(dest_dir) / subfolder_name
        final_dest.mkdir(parents=True, exist_ok=True)

        try:
            self.status_label.setText(f'Extracting to: {final_dest}...')
            if file_path.suffix == '.zip':
                temp_dir = paths.TEMP_UNPACKED
                temp_dir.mkdir(parents=True, exist_ok=True)
                ZipUtils.unpack_zip_file(file_path, temp_dir)
                pak_files = DirUtils.list_files_by_extension(temp_dir, 'pak')
                if not pak_files:
                    self.status_label.setText('No .pak file found inside the zip archive.')
                    shutil.rmtree(temp_dir, ignore_errors=True)
                    return
                pak_path = pak_files[0]
                LslibService._divine_unpack(pak_path, final_dest)
                shutil.rmtree(temp_dir, ignore_errors=True)
            elif file_path.suffix == '.pak':
                LslibService._divine_unpack(file_path, final_dest)
            else:
                self.status_label.setText('Unsupported file type.')
                return
            self.status_label.setText(f'Extraction finished: {final_dest}')
        except Exception as e:
            self.status_label.setText(f'Extraction failed: {e}')
