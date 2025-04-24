from pathlib import Path
import os

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog
from PySide6.QtCore import Qt, Signal

class DragDropWidget(QWidget):
    file_dropped = Signal(str)

    def __init__(self, accepted_extensions: list, description_text: str, droped_text: str = 'File received!', parent=None):
        super().__init__(parent)
        self.accepted_extensions = [ext.lower() for ext in accepted_extensions]
        self.description_text = description_text
        self.droped_text = droped_text
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        self.setMinimumWidth(120)
        self.setCursor(Qt.PointingHandCursor)
        self.default_style = """
            border: 2px dashed;
            border-radius: 32px;
        """
        self.active_style = """
            border: 2px solid #1976d2;
            background: #e3f2fd;
            border-radius: 32px;
        """
        self.setStyleSheet(self.default_style)
        layout = QVBoxLayout(self)
        self.label = QLabel(description_text)
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                local_path = url.toLocalFile()
                if os.path.isdir(local_path) or any(local_path.lower().endswith(ext) for ext in self.accepted_extensions):
                    self.setStyleSheet(self.active_style)
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)

    def dropEvent(self, event):
        self.setStyleSheet(self.default_style)
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if os.path.isdir(file_path):
                self.file_dropped.emit(file_path)
                self.label.setText(self.droped_text)
                break
            elif any(file_path.lower().endswith(ext) for ext in self.accepted_extensions):
                self.file_dropped.emit(file_path)
                self.label.setText(self.droped_text)
                break

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if not self.accepted_extensions:
                folder_path = QFileDialog.getExistingDirectory(
                    self,
                    'Select a folder',
                    '',
                )
                if folder_path:
                    self.file_dropped.emit(folder_path)
                    self.label.setText(self.droped_text)
            else:
                filter_str = ' '.join(f'*{ext}' for ext in self.accepted_extensions)
                file_path, _ = QFileDialog.getOpenFileName(
                    self,
                    'Select a file',
                    '',
                    f'Supported files ({filter_str})',
                )
                if file_path:
                    self.file_dropped.emit(file_path)
                    self.label.setText(self.droped_text)

    def reset(self):
        self.label.setText(self.description_text)
        self.setStyleSheet(self.default_style)
