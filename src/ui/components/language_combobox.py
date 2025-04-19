from PySide6.QtWidgets import QComboBox


class LanguageComboBox(QComboBox):
    def __init__(self, languages, parent=None):
        super().__init__(parent)
        self.setFixedHeight(40)
        self.setFixedWidth(160)
        self.addItems(languages)
        self.setCurrentIndex(-1)
        self.setStyleSheet("""
            QComboBox { background: transparent; border: 1px solid #888; padding: 4px 8px; }
            QComboBox:focus { border: 1px solid #888; background: transparent; }
            QComboBox::drop-down { border: none; background: transparent; }
        """)
