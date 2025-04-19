from PySide6.QtWidgets import QApplication
from qdarktheme import load_stylesheet

from src.database.connection import create_db_and_tables
from src.ui.app import Window

if __name__ == '__main__':
    create_db_and_tables()
    app = QApplication([])
    app.setStyleSheet(load_stylesheet())
    window = Window()
    window.show()
    app.exec()
