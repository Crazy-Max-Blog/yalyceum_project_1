import sys
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QDialog,
)


class InfoWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Инфо")
        self.setGeometry(100, 100, 200, 200)
        QLabel("Info", self)
        self.setModal(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InfoWindow()
    window.show()
    sys.exit(app.exec())
