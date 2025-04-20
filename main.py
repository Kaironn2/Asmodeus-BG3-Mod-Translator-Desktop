from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QFontDatabase
from qdarktheme import load_stylesheet

from src.database.connection import create_db_and_tables
from src.ui.app import Window

if __name__ == '__main__':
    create_db_and_tables()
    app = QApplication([])
    QFontDatabase.addApplicationFont('src/ui/assets/fonts/Lexend.ttf')
    app.setStyleSheet(
        load_stylesheet() +
        """
        * {
            font-family: 'Lexend';
            font-size: 15px;
        }
        """
    )
    window = Window()
    window.show()
    app.exec()
