import os
os.makedirs('data/db', exist_ok=True)

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from qdarktheme import load_stylesheet

from src.config.paths import resource_path
from src.database.connection import create_db_and_tables
from src.ui.app import Window


if __name__ == '__main__':
    create_db_and_tables()
    app = QApplication([])
    QFontDatabase.addApplicationFont(resource_path('src/ui/assets/fonts/Lexend.ttf'))
    app.setStyleSheet(
        load_stylesheet() +
        """
        * {
            font-family: 'Lexend';
            font-size: 15px;
        }
        """
    )
    window = Window('Asmodeus - BG3 Translation Tool - v0.4.1.3')
    window.show()
    app.exec()
