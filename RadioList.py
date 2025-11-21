from PyQt6.QtWidgets import QVBoxLayout, QLabel, QRadioButton, QButtonGroup


class RadioListWidget(QVBoxLayout):
    """Виджет списка радиокнопок с заголовком и обработчиком событий.

    Args:
        label (str): Текст заголовка виджета.
        buttons (list): Список текстов на радиокнопках.
        callback (function): Функция вызова при смене значения.
        parent (QWidget): Родительский виджет.
    """

    def __init__(self, label="", buttons=[], callback=None, parent=None):
        super().__init__(parent)
        # Заголовок виджета
        self.label = QLabel(label)
        self.addWidget(self.label)
        # Текущее значение выбранной радиокнопки (индекс)
        self.__value = 0
        # Группа радиокнопок
        self.button_group = QButtonGroup(self)
        # Список радиокнопок
        self.btns = []
        if buttons:
            for i, button in enumerate(buttons):
                self.btns.append(QRadioButton(button))
                self.addWidget(self.btns[i])
                self.button_group.addButton(self.btns[i], i)
            # Установка первой кнопки выбранной по умолчанию
            self.btns[0].setChecked(True)
        self.setCallback(callback)

    def onClick(self, v):
        id = self.button_group.id(v)
        if self.__value != id:
            self.__value = id
            if self.callback:
                self.callback(self.__value)

    def getValue(self):
        """Получить текущее значение выбранной радиокнопки (индекс)."""
        return self.__value

    def setLabel(self, label):
        """Установить текст заголовка виджета."""
        self.label.setText(label)

    def setCallback(self, callback):
        """Установить функцию для вызова при смене значения."""
        self.callback = callback
        self.button_group.buttonClicked.connect(self.onClick)
