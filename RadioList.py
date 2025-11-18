import sys
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QRadioButton,
    QButtonGroup
)

# Класс виджета RadioListWidget, у которого можно установить заголовок, указать список строк - радиокнопок, и подключить обработчик нажатия на радиокнопку
class RadioListWidget(QVBoxLayout):
    def __init__(self, label="", buttons=[], callback=None, parent=None):
        super().__init__(parent)
        self.label = QLabel(label)
        self.addWidget(self.label)
        self.label.adjustSize()
        print(self.label.width())
        self.__value = 0
        self.button_group = QButtonGroup(self)
        self.btns = []
        for i, button in enumerate(buttons):
            self.btns.append(QRadioButton(button))
            self.addWidget(self.btns[i])
            self.button_group.addButton(self.btns[i], i)
            self.btns[i].adjustSize()
            print(self.btns[i].width())
        self.setCallback(callback)
    
    def onClick(self, v): 
        id = self.button_group.id(v)
        if self.__value != id:
            self.__value = id
            if self.callback:
                self.callback(self.__value)
    
    def setLabel(self, label):
        self.label.setText(label)
    
    def setCallback(self, callback):
        self.callback = callback
        self.button_group.buttonClicked.connect(self.onClick)