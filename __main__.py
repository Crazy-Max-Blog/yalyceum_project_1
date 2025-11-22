import sys
import os

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLineEdit,
    QSplitter,
)

from DBTable import DBTableWidget
from RadioList import RadioListWidget

from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtSql import QSqlDatabase, QSqlQuery

from info import InfoWindow

from selectLang import SelectLangWindow

import styles

import queries

import path_module

from addData import AddDataWindow


class MainWindow(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)

        self.db = db

        self.setWindowTitle("Домашняя библиотека")  # Заголовок окна
        self.setGeometry(100, 100, 800, 600)  # Размеры окна

        self.main_layout = QVBoxLayout()  # Главный лейаут
        self.setLayout(self.main_layout)  # Устанавливаем главный лейаут

        # region path layout
        path_layout = QHBoxLayout()  # Лейаут строки пути
        self.main_layout.addLayout(path_layout)

        h = QPushButton().sizeHint().height()  # Стандарная высота кнопки

        # Кнопка перезагрузки данных
        reload_btn = QPushButton("⟳")
        reload_btn.setFixedSize(h, h)  # Делаем кнопку квадратной
        reload_btn.setStyleSheet(styles.text_btn)  # Устанавливаем стиль
        reload_btn.clicked.connect(self.tblReload)  # Подключаем обработчик нажатия
        path_layout.addWidget(reload_btn)  # Добавляем кнопку в лейаут

        # Поле для ввода пути
        self.path_input = QLineEdit("")
        # Установим стиль для поля ввода
        self.path_input.setStyleSheet(styles.line_path)
        self.path_input.setEnabled(False)
        self.path_input.returnPressed.connect(self.tblReload)
        path_layout.addWidget(self.path_input)  # Добавляем поле в лейаут

        # Кнопка добавления
        add_btn = QPushButton("+")
        add_btn.setFixedSize(h, h)  # Делаем кнопку квадратной
        add_btn.setStyleSheet(styles.text_btn)  # Устанавливаем стиль
        def add():
            self.windowAdd = AddDataWindow()
            self.windowAdd.show()
        add_btn.clicked.connect(add) # Подключаем обработчик нажатия
        path_layout.addWidget(add_btn)  # Добавляем кнопку в лейаут

        # Кнопка инфо
        info_btn = QPushButton("🛈")
        info_btn.setFixedSize(h, h)  # Делаем кнопку квадратной
        info_btn.setStyleSheet(styles.text_btn)  # Устанавливаем стиль
        self.info_window = InfoWindow()

        info_btn.clicked.connect(self.info_window.exec)  # Подключаем обработчик нажатия
        path_layout.addWidget(info_btn)  # Добавляем кнопку в лейаут

        # region down group

        # Нижняя группа - блок с настройками отображения и таблицей, с передвигающимся раздилителем
        self.down_group = QSplitter()
        # Не позволяем дочерним элементам сжиматься до 0
        self.down_group.setChildrenCollapsible(False)
        self.main_layout.addWidget(self.down_group)  # Добавляем в главный лейаут

        # Лейаут для меню настроек отображения
        self.agregation_menu_layout = QVBoxLayout()

        # Добавляем кнопки переключения отображения
        btn_1 = QPushButton("Сборники")

        btn_1.clicked.connect(lambda: path_module.set(self, "collections"))
        self.agregation_menu_layout.addWidget(btn_1)

        btn_2 = QPushButton("Авторы")
        btn_2.clicked.connect(lambda: path_module.set(self, "authors"))
        self.agregation_menu_layout.addWidget(btn_2)

        btn_3 = QPushButton("Рассказы")
        btn_3.clicked.connect(lambda: path_module.set(self, "books"))
        self.agregation_menu_layout.addWidget(btn_3)

        # Меню настроек отображения

        # При открытии сборника...
        self.select_on_collection = RadioListWidget(
            "При открытии сборника:",
            ["Открывать список авторов", "Открывать список рассказов"],
        )
        # Добавляем в лейаут
        self.agregation_menu_layout.addLayout(self.select_on_collection)

        # При открытии автора...

        self.select_on_author = RadioListWidget(
            "При открытии автора:",
            ["Открывать список рассказов", "Открывать список сборников"],
        )
        # Добавляем в лейаут
        self.agregation_menu_layout.addLayout(self.select_on_author)

        # Оставшееся место заполняем пустотой, чтобы сжать всё
        self.agregation_menu_layout.addStretch(1)

        # Добавляем лейаут настроек в нижнюю группу
        self.agregation_menu = QWidget()
        self.agregation_menu.setLayout(self.agregation_menu_layout)
        self.agregation_menu.adjustSize()  # Устанавливаем размер виджета настроек
        # Добавляем виджет настроек в нижнюю группу
        self.down_group.addWidget(self.agregation_menu)

        # Создаем таблицу
        self.tbl = DBTableWidget(self.db)
        self.down_group.addWidget(self.tbl)  # Добавляем таблицу в нижнюю группу
        # Подключаем обработчик нажатия на строчку
        self.tbl.clicked.connect(self.tblClickRow)

    def resizeEvent(self, event):
        super().resizeEvent(event)  # Вызываем базовый метод (пусть будет)
        # Ширина панели настроек и таблицы: у панели ширина дойдёт до минимального
        self.down_group.setSizes([0, self.width()])

    def tblReload(self):
        self.tbl.loadData()

    def tblClickRow(self, v: QModelIndex):
        if path_module._table == "books":
            return
        getCol = lambda column: self.tbl.sqlModel.data(
            self.tbl.sqlModel.index(v.row(), column), Qt.ItemDataRole.DisplayRole
        )
        name = getCol(0)
        table = path_module._table
        if path_module._args != []:
            path_module.set(self, "books", [(table, name)] + path_module._args)
            return
        newName = (
            ["authors", "books"][self.select_on_collection.getValue()]
            if table == "collections"
            else ["books", "collections"][self.select_on_author.getValue()]
        )
        path_module.set(self, newName, path_module._args + [(table, name)])


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not os.path.isfile("settings.json"):
        # Первый запуск
        langSelector = SelectLangWindow()
        langSelector.show()
        app.exec()
        infoWindow = InfoWindow()
        infoWindow.show()

    # Зададим тип базы данных
    db = QSqlDatabase.addDatabase("QSQLITE")
    # Укажем имя базы данных
    db.setDatabaseName("db.db")
    # И откроем подключение
    db.open()
    # Создадим таблицы, если они не существуют
    query = QSqlQuery()
    for i in queries.create:
        query.exec(i)
    # Создадим главное окно
    table = MainWindow(db)
    table.show()
    sys.exit(app.exec())
