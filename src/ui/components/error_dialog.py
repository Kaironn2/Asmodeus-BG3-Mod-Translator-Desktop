from PySide6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QMessageBox


class ErrorDialog(QDialog):
    def __init__(self, error_text, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Error details')
        layout = QVBoxLayout(self)
        text_edit = QTextEdit()
        text_edit.setReadOnly(True)
        text_edit.setPlainText(error_text)
        layout.addWidget(text_edit)
        btn = QPushButton('Close')
        btn.clicked.connect(self.accept)
        layout.addWidget(btn)
        self.resize(700, 400)


def show_error_popup(error_text, parent=None):
    msg = QMessageBox(parent)
    msg.setIcon(QMessageBox.Critical)
    msg.setWindowTitle("Erro inesperado")
    msg.setText("Ocorreu um erro inesperado!")
    msg.setInformativeText("Clique em 'Detalhes...' para ver o erro completo.")
    msg.setDetailedText(error_text)
    msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Open)
    details_button = msg.button(QMessageBox.Open)
    if details_button:
        details_button.setText("Detalhes...")

    ret = msg.exec()
    if ret == QMessageBox.Open:
        dialog = ErrorDialog(error_text, parent)
        dialog.exec()
