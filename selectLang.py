import json
from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
    QDialogButtonBox,
    QLayout,
)
from RadioList import RadioListWidget


class SelectLangWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Welcome")
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.language_list = RadioListWidget(
            "Выберите язык / Select language:", ["Русский", "English"]
        )
        self.btns.accepted.connect(self.next)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.language_list)
        self.mainLayout.addWidget(self.btns)
        # Запрещаем изменение размера окна
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

    def next(self):
        with open("settings.json", "w") as f:
            f.write(json.dumps({"lang": ["ru", "eng"][self.language_list.getValue()]}))
        self.close()
