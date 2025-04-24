from PySide6.QtWidgets import QLineEdit


class LabeledLineEdit(QLineEdit):
    def __init__(self, placeholder, min_width=240, height=40, parent=None, password=False):
        super().__init__(parent)
        self.setPlaceholderText(placeholder)
        self.setFixedHeight(height)
        self.setMinimumWidth(min_width)
        if password:
            self.setEchoMode(QLineEdit.Password)
