import json
import sys
from PyQt6.QtWidgets import (
    QApplication,
    QVBoxLayout,
    QWidget,
    QDialog,
    QDialogButtonBox,
)
from RadioList import RadioListWidget


class SelectLangWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Приветствие")
        # self.setGeometry(100, 100, 200, 200)
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.language_list = RadioListWidget(
            "Выберите язык / Select language:", ["Русский", "English"]
        )
        self.btns.accepted.connect(self.next)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.language_list)
        self.mainLayout.addWidget(self.btns)
        self.mainLayout.addStretch(1)

    def next(self):
        with open("settings.json", "w") as f:
            f.write(json.dumps({"lang": ["ru", "eng"][self.language_list.getValue()]}))
