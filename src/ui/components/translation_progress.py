from PySide6.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QProgressBar


class TranslationProgressTable(QTableWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setColumnCount(3)
        self.setHorizontalHeaderLabels(['N°', 'Source Text', 'Target Text'])
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setWordWrap(True)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.verticalHeader().setVisible(False)
        self.setColumnWidth(0, 65)
        self.setColumnWidth(1, 770)
        self.setColumnWidth(2, 770)
        self.setStyleSheet("""
            QTableWidget {
                background: #2a2a2a;
                color: #fff;
                font-size: 15px;
            }
            QHeaderView::section {
                background: #fff;
                color: #222;
                font-weight: bold;
                border: 1px solid #ddd;
            }
            QTableWidget QTableCornerButton::section {
                background: #2a2a2a;
                border: 1px solid #ddd;
            }
        """)

    def update_row(self, index, source_text, target_text):
        for row in range(self.rowCount()):
            item = self.item(row, 1)
            if item and item.text() == source_text:
                self.setItem(row, 2, QTableWidgetItem(target_text))
                return
        row = self.rowCount()
        self.insertRow(row)
        self.setItem(row, 0, QTableWidgetItem(str(index)))
        self.setItem(row, 1, QTableWidgetItem(source_text))
        self.setItem(row, 2, QTableWidgetItem(target_text))


class TranslationProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setValue(0)
        self.setTextVisible(True)
        self.setFixedHeight(28)
        self.setStyleSheet("""
            QProgressBar {
                border: 1px solid #888;
                border-radius: 8px;
                background: #222;
                color: #fff;
                font-size: 15px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4caf50;
                border-radius: 8px;
            }
        """)

    def set_progress(self, current, total):
        if total > 0:
            percent = int((current / total) * 100)
            self.setMaximum(total)
            self.setValue(current)
            self.setFormat(f'{current}/{total} ({percent}%)')
        else:
            self.setValue(0)
            self.setFormat('0/0 (0%)')
