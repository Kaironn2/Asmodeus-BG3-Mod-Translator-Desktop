from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QStackedWidget
)
from PySide6.QtGui import QIcon

from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository

from src.ui.views.translation.openai_view import OpenaiView
from src.ui.components.translation_topbar import TopNavBar
from src.ui.components.sidebar import Sidebar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Asmodeus - BG3 Translation Tool')
        self.resize(1000, 700)
        self.setWindowIcon(QIcon('src/ui/assets/asmodeus_logo_white_vetorized_256_256.ico'))

        with get_session() as session:
            self.languages = sorted(LanguageRepository.get_all_language_names(session))

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self.select_sidebar)
        self.sidebar.setFixedWidth(200)
        main_layout.addWidget(self.sidebar)

        self.central_stack = QStackedWidget()

        self.translation_widget = QWidget()
        translation_layout = QVBoxLayout(self.translation_widget)
        translation_layout.setContentsMargins(0, 0, 0, 0)
        translation_layout.setSpacing(0)

        self.views = {}
        self.stacked = QStackedWidget()
        self.views['openai_translation'] = OpenaiView(languages=self.languages)
        self.views['google_translator'] = QLabel('View: Google Translator')
        self.views['deepl'] = QLabel('View: DeepL')
        for key, widget in self.views.items():
            self.stacked.addWidget(widget)

        self.top_nav = TopNavBar(self.select_view)
        translation_layout.addWidget(self.top_nav)
        translation_layout.addWidget(self.stacked)

        dictionaries_view = QLabel('View: Dictionary')
        about_view = QLabel('View: Sobre')

        self.central_stack.addWidget(self.translation_widget)  # index 0
        self.central_stack.addWidget(dictionaries_view)        # index 1
        self.central_stack.addWidget(about_view)               # index 2

        main_layout.addWidget(self.central_stack)

        self.setCentralWidget(main_widget)

        self.top_nav.select_nav('openai_translation')
        self.sidebar.select('translate')
        self.select_view('openai_translation')

    def select_sidebar(self, key):
        if key == 'translate':
            self.central_stack.setCurrentIndex(0)
        elif key == 'dictionaries':
            self.central_stack.setCurrentIndex(1)
        elif key == 'about':
            self.central_stack.setCurrentIndex(2)

    def select_view(self, key):
        for k, btn in getattr(self.top_nav, 'buttons', {}).items():
            btn.set_selected(k == key)
        idx = list(self.views.keys()).index(key)
        self.stacked.setCurrentIndex(idx)
