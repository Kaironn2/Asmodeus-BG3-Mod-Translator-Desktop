from PySide6.QtWidgets import QComboBox

from src.config.config_manager import ConfigManager
from src.database.connection import get_session
from src.database.repositories.language_repository import LanguageRepository


class LanguageComboBox(QComboBox):
    def __init__(self, parent=None, cache=None):
        super().__init__(parent)

        with get_session() as session:
            languages = LanguageRepository.get_all_language_names(session=session)

        self.setFixedHeight(40)
        self.setFixedWidth(190)
        self.addItems(languages)
        self.setCurrentIndex(-1)
        self.setStyleSheet("""
            QComboBox { background: transparent; border: 1px solid #888; padding: 4px 8px; }
            QComboBox:focus { border: 1px solid #888; background: transparent; }
            QComboBox::drop-down { border: none; background: transparent; }
        """)

        if cache == 'source':
            self.setCurrentText(ConfigManager.load_last_languages()[0])
        elif cache == 'target':
            self.setCurrentText(ConfigManager.load_last_languages()[1])
