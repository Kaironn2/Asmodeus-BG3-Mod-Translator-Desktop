from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QApplication, QStackedWidget
)
from PySide6.QtGui import QIcon

from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository

from src.ui.views.buy_me_a_coffee_view import BuyMeACoffeeView
from src.ui.views.dictionary_view import DictionaryView
from src.ui.views.create_mod_package_view import CreateModPackageView
from src.ui.views.extract_mod_view import ExtractModView
from src.ui.views.translation.manual_view import ManualView
from src.ui.views.translation.openai_view import OpenaiView
from src.ui.components.translation_topbar import TopNavBar
from src.ui.components.sidebar import Sidebar


class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Asmodeus - BG3 Translation Tool - v0.1.0')
        self.resize(1000, 700)
        self.setWindowIcon(QIcon('src/ui/assets/asmodeus_logo_white.ico'))

        with get_session() as session:
            self.languages = sorted(LanguageRepository.get_all_language_names(session))

        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = Sidebar(self.select_sidebar)
        self.sidebar.setFixedWidth(240)
        main_layout.addWidget(self.sidebar)

        self.central_stack = QStackedWidget()

        self.translation_widget = QWidget()
        translation_layout = QVBoxLayout(self.translation_widget)
        translation_layout.setContentsMargins(0, 0, 0, 0)
        translation_layout.setSpacing(0)

        self.views = {}
        self.stacked = QStackedWidget()
        self.views['openai_translation'] = OpenaiView(languages=self.languages)
        self.views['manual_translation'] = ManualView(languages=self.languages)
        self.views['google_translator'] = QLabel('View: Google Translator - coming soon')
        self.views['deepl'] = QLabel('View: DeepL - coming soon')
        for key, widget in self.views.items():
            self.stacked.addWidget(widget)

        self.top_nav = TopNavBar(self.select_view)
        translation_layout.addWidget(self.top_nav)
        translation_layout.addWidget(self.stacked)

        dictionaries_view = DictionaryView()
        extract_mod_view = ExtractModView()
        create_mod_package_view = CreateModPackageView()
        settings_view = QLabel('View: Settings - coming soon')
        about_view = QLabel('View: About - coming soon')
        check_for_updates_view = QLabel('View: Check for Updates - coming soon')
        buy_me_a_cofffe_view = BuyMeACoffeeView()

        self.central_stack.addWidget(self.translation_widget)  # index 0
        self.central_stack.addWidget(dictionaries_view)        # index 1
        self.central_stack.addWidget(extract_mod_view)         # index 2
        self.central_stack.addWidget(create_mod_package_view)  # index 3
        self.central_stack.addWidget(settings_view)            # index 4
        self.central_stack.addWidget(about_view)               # index 5
        self.central_stack.addWidget(check_for_updates_view)   # index 6
        self.central_stack.addWidget(buy_me_a_cofffe_view)     # index 7

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
        elif key == 'extract_mod':
            self.central_stack.setCurrentIndex(2)
        elif key == 'create_mod_package':
            self.central_stack.setCurrentIndex(3)
        elif key == 'settings':
            self.central_stack.setCurrentIndex(4)
        elif key == 'about':
            self.central_stack.setCurrentIndex(5)
        elif key == 'check_for_updates':
            self.central_stack.setCurrentIndex(6)
        elif key == 'buy_me_a_coffee':
            self.central_stack.setCurrentIndex(7)

    def select_view(self, key):
        for k, btn in getattr(self.top_nav, 'buttons', {}).items():
            btn.set_selected(k == key)
        idx = list(self.views.keys()).index(key)
        self.stacked.setCurrentIndex(idx)
