from PySide6.QtWidgets import QWidget, QVBoxLayout, QFileDialog, QLabel
from src.ui.components.drag_drop import DragDropWidget
from src.services.external_tools.lslib_service import LslibService


class CreateModPackageView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        self.drag_drop = DragDropWidget(
            accepted_extensions=[],
            description_text='Drag and drop your mod folder here\nor click to select'
        )
        self.drag_drop.file_dropped.connect(self.on_folder_dropped)
        layout.addWidget(self.drag_drop)
        self.status_label = QLabel('')
        layout.addWidget(self.status_label)

    def on_folder_dropped(self, folder_path):
        from pathlib import Path

        pak_path, _ = QFileDialog.getSaveFileName(
            self,
            'Select where to save the .pak file',
            'mod.pak',
            'PAK Files (*.pak)'
        )
        if not pak_path:
            self.status_label.setText('Packing cancelled.')
            return

        folder_path = Path(folder_path)
        pak_path = Path(pak_path)

        try:
            self.status_label.setText(f'Packing to: {pak_path}...')
            LslibService._divine_pack(folder_path, pak_path)
            self.status_label.setText(f'Packing finished: {pak_path}')
        except Exception as e:
            self.status_label.setText(f'Packing failed: {e}')
