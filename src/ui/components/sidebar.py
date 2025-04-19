from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QSizePolicy, QLabel, QFrame
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

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
                ('Translate', 'translate', 'src/ui/assets/translation_blue_icon_vetorized.ico'),
                ('Dictionaries', 'dictionaries', 'src/ui/assets/dictionary_icon_orange_vetorized.ico'),
            ]
        )
        self._add_separator()

        # Sessão 2: Tools
        self._add_section(
            title='Tools',
            options=[
                ('Extract Mod', 'extract_mod', 'src/ui/assets/extract_icon_vetorized.ico'),
                ('Create Mod Package', 'create_mod_package', 'src/ui/assets/create_package_icon_vetorized.ico'),
            ]
        )
        self._add_separator()

        # Sessão 3: Configs
        self._add_section(
            title='Configs',
            options=[
                ('Settings', 'settings', 'src/ui/assets/settings.png'),
                ('About', 'about', 'src/ui/assets/about.png'),
                ('Check for Updates', 'check_for_updates', 'src/ui/assets/update.png'),
                ('Buy Me a Coffee', 'buy_me_a_coffee', 'src/ui/assets/coffee.png'),
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
