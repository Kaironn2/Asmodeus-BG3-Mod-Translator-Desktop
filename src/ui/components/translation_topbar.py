from PySide6.QtWidgets import QWidget, QHBoxLayout
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QPushButton


class NavButton(QPushButton):
    def __init__(self, text, key, parent=None):
        super().__init__(text, parent)
        self.key = key
        self.setCursor(Qt.PointingHandCursor)
        self.setFlat(True)
        self.setStyleSheet('''
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                padding: 8px 16px 2px 16px;
                border-radius: 0px;
            }
            QPushButton[selected="true"] {
                border-bottom: 1px solid #1976d2;
                color: #1976d2;
                border-radius: 0px;
            }
        ''')

    def set_selected(self, selected: bool):
        self.setProperty('selected', 'true' if selected else 'false')
        self.style().unpolish(self)
        self.style().polish(self)

class TopNavBar(QWidget):
    def __init__(self, on_nav_selected, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.buttons = {}
        self.on_nav_selected = on_nav_selected

        nav_items = [
            ('OpenAI (GPT)', 'openai_translation'),
            ('Google Translator', 'google_translator'),
            ('DeepL', 'deepl')
        ]

        for text, key in nav_items:
            btn = NavButton(text, key)
            btn.clicked.connect(lambda _, k=key: self.select_nav(k))
            self.layout.addWidget(btn)
            self.buttons[key] = btn

    def select_nav(self, key):
        for k, btn in self.buttons.items():
            btn.set_selected(k == key)
        if self.on_nav_selected:
            self.on_nav_selected(key)
