from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap, QCursor
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices

from src.config.paths import resource_path


class BuyMeACoffeeView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.kofi_label = QLabel()
        pixmap = QPixmap(resource_path('src/ui/assets/kaironn_kofi.png'))
        self.kofi_label.setPixmap(pixmap)
        self.kofi_label.setCursor(QCursor(Qt.PointingHandCursor))
        self.kofi_label.setAlignment(Qt.AlignCenter)
        self.kofi_label.mousePressEvent = self.open_kofi
        layout.addWidget(self.kofi_label)

        spacer = QLabel()
        spacer.setFixedHeight(24)
        layout.addWidget(spacer)

        pt_text = (
            "<b>Olá! Eu sou um desenvolvedor brasileiro :)</b><br>"
            "Se você gosta do meu trabalho, pode contribuir com qualquer valor que não lhe faça falta.<br>"
            "Tenho muitas features para adicionar ainda!<br>"
            "Se for brasileiro e quiser apoiar diretamente, meu pix é: <b>kaironn2021@gmail.com</b><br>"
            "Você pode clicar na imagem acima para ir ao meu Ko-fi, ou acessar diretamente: "
            "<a href='https://ko-fi.com/kaironn2'>https://ko-fi.com/kaironn2</a><br>"
            "Também é possível doar pela Nexus se preferir.<br>"
        )
        pt_label = QLabel(pt_text)
        pt_label.setWordWrap(True)
        pt_label.setOpenExternalLinks(True)
        layout.addWidget(pt_label)

        en_text = (
            "<b>Hello! I'm a Brazilian developer :)</b><br>"
            "If you enjoy my work, you can support me with any amount that won't make a difference for you.<br>"
            "I have many features to add!<br>"
            "If you're Brazilian and want to support me directly, my pix is: <b>kaironn2021@gmail.com</b><br>"
            "You can click the image above to go to my Ko-fi, or visit: "
            "<a href='https://ko-fi.com/kaironn2'>https://ko-fi.com/kaironn2</a><br>"
            "You can also donate through Nexus if you prefer.<br>"
        )
        en_label = QLabel(en_text)
        en_label.setWordWrap(True)
        en_label.setOpenExternalLinks(True)
        layout.addWidget(en_label)

    def open_kofi(self, event):
        QDesktopServices.openUrl(QUrl("https://ko-fi.com/kaironn2"))
