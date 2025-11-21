import sys
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QDialog,
    QVBoxLayout,
    QDialogButtonBox,
    QTextBrowser,
)


class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Инфо")
        self.setGeometry(400, 300, 400, 400)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        text_browser = QTextBrowser()
        with open("info.html", "r", encoding="utf-8") as f:
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
