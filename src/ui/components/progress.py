from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar


class ImportProgressDialog(QDialog):
    def __init__(self, window_text: str, text: str, parent=None):
        super().__init__(parent)
        self.setWindowTitle(window_text)
        self.setModal(True)
        self.setFixedSize(350, 100)
        layout = QVBoxLayout(self)
        self.label = QLabel(text, self)
        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)
        layout.addWidget(self.label)
        layout.addWidget(self.progress)
