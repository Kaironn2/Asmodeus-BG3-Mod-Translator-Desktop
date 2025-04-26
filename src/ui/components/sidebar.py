from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from src.config.paths import resource_path


class Sidebar(QWidget):
    def __init__(self, on_selected, parent=None):
        super().__init__(parent)
        self.setObjectName('Sidebar')
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 16, 0, 0)
        self.layout.setSpacing(20)
        self.buttons = {}
        self.on_selected = on_selected


        # Sessão 1: Translation
        self._add_section(
            title='Translation',
            options=[
                ('Translate', 'translate', resource_path('src/ui/assets/translation_blue_icon.ico')),
                ('Dictionaries', 'dictionaries', resource_path('src/ui/assets/dictionary_icon_blue.ico')),
                ('Create Dictionary', 'create_dictionary', resource_path('src/ui/assets/dictionary_icon_blue.ico')),
            ]
        )
        self._add_separator()

        # Sessão 2: Tools
        self._add_section(
            title='Tools',
            options=[
                ('Extract Mod', 'extract_mod', resource_path('src/ui/assets/extract_icon.ico')),
                ('Create Mod Package', 'create_mod_package', resource_path('src/ui/assets/create_package_icon.ico')),
            ]
        )
        self._add_separator()

        # Sessão 3: Configs
        self._add_section(
            title='Configs',
            options=[
                ('Settings', 'settings', resource_path('src/ui/assets/settings_white.ico')),
                ('About', 'about', resource_path('src/ui/assets/about_white.ico')),
                ('Check for Updates', 'check_for_updates', resource_path('src/ui/assets/check_for_updates_white.ico')),
                ('Buy Me a Coffee', 'buy_me_a_coffee', resource_path('src/ui/assets/buy_me_a_coffee_red.ico')),
            ]
        )

        self.layout.addStretch(1)

    def _add_section(self, title, options):
        section_layout = QVBoxLayout()
        section_layout.setSpacing(0)
        title_label = QLabel(title)
        title_label.setStyleSheet('color: white; font-size: 18px; font-weight: bold; margin-bottom: 8px;')
        section_layout.addWidget(title_label, alignment=Qt.AlignLeft)
        for idx, (text, key, icon_path) in enumerate(options):
            self._add_sidebar_button(section_layout, text, key, icon_path)
        self.layout.addLayout(section_layout)

    def _add_sidebar_button(self, layout, text, key, icon_path=None):
        btn = QPushButton(text)
        btn.setFlat(True)
        btn.setCursor(Qt.PointingHandCursor)
        btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        btn.setStyleSheet('''
            QPushButton {
                background: transparent;
                color: #eee;
                font-size: 15px;
                padding: 10px 0 10px 12px;
                margin: 0px;
                text-align: left;
                border: none;
            }
            QPushButton:checked {
                font-weight: bold;
                background: #222;
            }
            QPushButton:hover {
                background: #333;
            }
        ''')
        btn.setCheckable(True)
        btn.clicked.connect(lambda _, k=key: self.select(k))
        if icon_path:
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(QSize(36, 36))
        layout.addWidget(btn)
        self.buttons[key] = btn

    def _add_separator(self):
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Plain)
        line.setFixedHeight(1)
        line.setStyleSheet('background: #fff; border: none; margin: 8px 12px;')
        self.layout.addWidget(line)

    def select(self, key):
        for k, btn in self.buttons.items():
            btn.setChecked(k == key)
        if self.on_selected:
            self.on_selected(key)
