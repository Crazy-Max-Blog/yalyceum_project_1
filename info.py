import os
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QTextBrowser,
)

def get_resource_path(relative_path):
    """ Получает абсолютный путь к ресурсу """
    if hasattr(sys, '_MEIPASS'):
        # Если запущено как exe
        return os.path.join(sys._MEIPASS, relative_path)
    # Если запущено как скрипт
    return os.path.join(os.path.abspath("."), relative_path)


class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Инфо")
        self.setGeometry(400, 300, 400, 400)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        text_browser = QTextBrowser()
        with open(get_resource_path("info.html"), "r", encoding="utf-8") as f:
            text_browser.setHtml(f.read())
        layout.addWidget(text_browser)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        layout.addWidget(self.btns)
        self.btns.accepted.connect(self.close)
        self.setModal(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InfoWindow()
    window.show()
    sys.exit(app.exec())
