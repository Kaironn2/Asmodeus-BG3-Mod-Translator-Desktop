from PySide6.QtWidgets import QPushButton, QFileDialog


class ActionButton(QPushButton):
    def __init__(self, text, parent=None, on_click=None):
        super().__init__(text, parent)
        self.setFixedWidth(90)
        self.setFixedHeight(32)
        self.setStyleSheet("""
            QPushButton {
                background-color: #444;
                color: #fff;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #666;
            }
        """)
        if on_click:
            self.clicked.connect(on_click)

    def get_file_path(self, parent=None, caption='Select file', filter='All Files (*)'):
        file_path, _ = QFileDialog.getOpenFileName(parent or self, caption, '', filter)
        return file_path