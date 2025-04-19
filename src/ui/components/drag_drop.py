from pathlib import Path

from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFileDialog
from PySide6.QtCore import Qt, Signal


class DragDropWidget(QWidget):
    file_dropped = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setMinimumHeight(120)
        self.setMinimumWidth(120)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet("""
            border: 2px dashed;
            border-radius: 32px;
        """)
        layout = QVBoxLayout(self)
        self.label = QLabel('Drag and drop a ZIP,\n PAK or XML file here\nor click to select a file')
        self.label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.label)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            for url in event.mimeData().urls():
                if url.isLocalFile() and (url.toLocalFile().endswith('.zip') or url.toLocalFile().endswith('.pak')):
                    event.acceptProposedAction()
                    return
        event.ignore()

    def dropEvent(self, event):
        for url in event.mimeData().urls():
            file_path = url.toLocalFile()
            if file_path.endswith('.zip') or file_path.endswith('.pak'):
                self.file_dropped.emit(file_path)
                self.label.setText(f'Drag and drop a ZIP or PAK file here\nor click to select a file')
                break

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            file_path, _ = QFileDialog.getOpenFileName(
                self,
                'Select a file',
                '',
                'Arquivos ZIP/Pak (*.zip *.pak)'
            )
            if file_path:
                self.file_dropped.emit(file_path)
                self.label.setText(f'Arquivo recebido:\n{file_path}')
