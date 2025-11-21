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
    QMessageBox,
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

        # Кнопка назад
        back_btn = QPushButton("🡠")
        back_btn.setFixedSize(h, h)  # Делаем кнопку квадратной
        back_btn.setStyleSheet(styles.text_btn)  # Устанавливаем стиль

        def go_back():
            t = self.path_input.text()
            self.path_input.setText(
                "/".join(t.split("/")[:-1]) if t.count("/") > 0 else t
            )
            self.reload()

        back_btn.clicked.connect(go_back)  # Подключаем обработчик нажатия
        path_layout.addWidget(back_btn)  # Добавляем кнопку в лейаут

        # Кнопка перезагрузки данных
        reload_btn = QPushButton("⟳")
        reload_btn.setFixedSize(h, h)  # Делаем кнопку квадратной
        reload_btn.setStyleSheet(styles.text_btn)  # Устанавливаем стиль
        reload_btn.clicked.connect(self.reload)  # Подключаем обработчик нажатия
        path_layout.addWidget(reload_btn)  # Добавляем кнопку в лейаут

        # Поле для ввода пути
        self.path_input = QLineEdit("")
        # Установим стиль для поля ввода
        self.path_input.setStyleSheet(styles.line_edit)
        self.path_input.returnPressed.connect(self.reload)
        path_layout.addWidget(self.path_input)  # Добавляем поле в лейаут

        # Кнопка добавления
        add_btn = QPushButton("+")
        add_btn.setFixedSize(h, h)  # Делаем кнопку квадратной
        add_btn.setStyleSheet(styles.text_btn)  # Устанавливаем стиль
        # add_btn.clicked.connect(lambda: self.w.adjustSize()) # Подключаем обработчик нажатия
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

        btn_3 = QPushButton("Книги")
        btn_3.clicked.connect(lambda: path_module.set(self, "books"))
        self.agregation_menu_layout.addWidget(btn_3)

        # Меню настроек отображения
        self.select_on_collection = RadioListWidget(
            "При открытии сборника:",
            ["Открывать список авторов", "Открывать список рассказов"],
            lambda v: print(v),
        )
        # Добавляем в лейаут
        self.agregation_menu_layout.addLayout(self.select_on_collection)
        # Оставшееся место заполняем пустотой, чтобы сжать всё
        self.agregation_menu_layout.addStretch(1)

        # Добавляем лейаут настроек в нижнюю группу
        self.w = QWidget()
        self.w.setLayout(self.agregation_menu_layout)
        self.down_group.addWidget(self.w)

        # Создаем таблицу
        self.tbl = DBTableWidget(self.db)
        self.down_group.addWidget(self.tbl)  # Добавляем таблицу в нижнюю группу
        self.tbl.clicked.connect(
            self.tblClickRow
        )  # Подключаем обработчик нажатия на строчку

    def reload(self):
        path = self.path_input.text().split("/")
        if (len(path) != 1 and not (len(path) == 2 and path[0] == "Сборники")) or path[
            0
        ] not in queries.paths.keys():
            self.alert = QMessageBox(
                QMessageBox.Icon.Critical,
                "Ошибка",
                "Неверный путь",
                QMessageBox.StandardButton.Discard,
                self,
            )
            self.alert.show()
            return
        if path[0] == "Сборники" and len(path) == 2:
            v = "collection" if self.select_on_collection.getValue() == 0 else "name"
            self.tbl.setQuery(queries.paths["Авторы"][0] + f' WHERE {v}="{path[1]}"')
            return
        v = queries.paths[self.path_input.text()]
        self.tbl.setQuery(v[0])

        # Установим заголовки столбцов
        Qt_Horisontal = Qt.Orientation.Horizontal
        for ind, header in enumerate(v[1]):
            self.tbl.model().setHeaderData(ind, Qt_Horisontal, header)

    def tblClickRow(self, v: QModelIndex):
        if path_module._table == "books":
            print("book")
            return
        getCol = lambda column: self.tbl.sqlModel.data(
            self.tbl.sqlModel.index(v.row(), column), Qt.ItemDataRole.DisplayRole
        )
        path_module.open(self, getCol(0))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    if not os.path.isfile("db.db"):
        # Первый запуск
        i = InfoWindow()
        i.show()
        app.exec()
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
