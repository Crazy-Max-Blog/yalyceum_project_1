import sys
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QTableWidget,
    QTableWidgetItem,
    QAbstractItemView,
    QTabWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QLineEdit,
    QSpacerItem,
    QSplitter,
    QRadioButton,
    QButtonGroup,
    QSizePolicy,
    QMessageBox
)
from DBTable import DBTableWidget
from RadioList import RadioListWidget
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtSql import QSqlDatabase


paths = {
    "Сборники": [
        "SELECT collection, numOfPages, COUNT(books.name) from collections LEFT JOIN books ON collections.id = books.collectionId GROUP BY collection",
        ["Сборник", "Количество рассказов", "Общее количество страниц"],
    ],
    "Авторы": [
        "SELECT author, COUNT(books.name) from authors LEFT JOIN books ON authors.id = books.authorId LEFT JOIN collections ON collections.id = books.collectionId",
        ["Автор", "Количество рассказов"],
    ],
    "Книги": [
        "SELECT name, author, collection, pagesNum, pageInCollection from books LEFT JOIN authors ON books.authorId = authors.id LEFT JOIN collections ON books.collectionId = collections.id",
        ["Название", "Автор", "Сборник", "К-во страниц", "Номер страницы в сборнике"],
    ],
}


class MainWindow(QWidget):
    def __init__(self, db, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Домашняя библиотека")  # Заголовок окна
        self.setGeometry(100, 100, 800, 600)  # Размеры окна

        self.db = db

        self.main_layout = QVBoxLayout() # Главный лейаут
        self.setLayout(self.main_layout) # Устанавливаем главный лейаут

        # region path layout
        path_layout = QHBoxLayout() # Лейаут строки пути
        self.main_layout.addLayout(path_layout)

        # Стиль для кнопок без фона
        btn_style = """
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 24px;
            }
            QPushButton:hover {
                color: blue;
            }
        """

        h = QPushButton().sizeHint().height() # Стандарная высота кнопки

        # Кнопка назад
        back_btn = QPushButton("🡠")
        back_btn.setFixedSize(h, h) # Делаем кнопку квадратной
        back_btn.setStyleSheet(btn_style) # Устанавливаем стиль
        # back_btn.clicked.connect(lambda: self.w.adjustSize()) # Подключаем обработчик нажатия
        path_layout.addWidget(back_btn) # Добавляем кнопку в лейаут

        # Кнопка перезагрузки данных
        reload_btn = QPushButton("⟳")
        reload_btn.setFixedSize(h, h) # Делаем кнопку квадратной
        reload_btn.setStyleSheet(btn_style) # Устанавливаем стиль
        reload_btn.clicked.connect(self.reload)  # Подключаем обработчик нажатия
        path_layout.addWidget(reload_btn) # Добавляем кнопку в лейаут

        # Поле для ввода пути
        self.path_input = QLineEdit("ghyhnbgfnfb/gtdhtrgf")
        # Установим стиль для поля ввода
        self.path_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdcdc;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #ffffff;
                selection-background-color: #4CAF50;
            }
        """)
        self.path_input.returnPressed.connect(self.reload)
        path_layout.addWidget(self.path_input) # Добавляем поле в лейаут

        # Кнопка добавления
        add_btn = QPushButton("+")
        add_btn.setFixedSize(h, h) # Делаем кнопку квадратной
        add_btn.setStyleSheet(btn_style) # Устанавливаем стиль
        # add_btn.clicked.connect(lambda: self.w.adjustSize()) # Подключаем обработчик нажатия
        path_layout.addWidget(add_btn) # Добавляем кнопку в лейаут

        # Кнопка инфо
        info_btn = QPushButton("🛈")
        info_btn.setFixedSize(h, h) # Делаем кнопку квадратной
        info_btn.setStyleSheet(btn_style) # Устанавливаем стиль
        info_btn.clicked.connect(lambda: self.w.adjustSize()) # Подключаем обработчик нажатия
        path_layout.addWidget(info_btn) # Добавляем кнопку в лейаут

        # region down group
        self.down_group = QSplitter() # Нижняя группа - блок с настройками отображения и таблицей, с передвигающимся раздилителем
        self.main_layout.addWidget(self.down_group) # Добавляем в главный лейаут

        self.agregation_menu_layout = QVBoxLayout() # Лейаут для меню настроек отображения
        # Добавляем кнопки переключения отображения
        btn_1 = QPushButton("Сборники")
        def c_1():
            self.path_input.setText("Сборники")
            self.reload()
        btn_1.clicked.connect(c_1)
        self.agregation_menu_layout.addWidget(btn_1) 

        btn_2 = QPushButton("Авторы")
        def c_2():
            self.path_input.setText("Авторы")
            self.reload()
        btn_2.clicked.connect(c_2)
        self.agregation_menu_layout.addWidget(btn_2) 

        btn_3 = QPushButton("Книги")
        def c_3():
            self.path_input.setText("Книги")
            self.reload()
        btn_3.clicked.connect(c_3)
        self.agregation_menu_layout.addWidget(btn_3) 

        # Меню настроек отображения
        self.select_on_collection = RadioListWidget(
            "При открытии сборника:",
            ["Открывать список авторов", "Открывать список рассказов"],
            lambda v: print(v),
        )
        self.agregation_menu_layout.addLayout(self.select_on_collection) # Добавляем в лейаут
        self.agregation_menu_layout.addStretch(1) # Оставшееся место заполняем пустотой, чтобы сжать всё

        # Добавляем лейаут настроек в нижнюю группу
        self.w = QWidget()
        self.w.setLayout(self.agregation_menu_layout)
        self.down_group.addWidget(self.w)

        # Создаем таблицу
        self.tbl = DBTableWidget(self.db)
        self.down_group.addWidget(self.tbl) # Добавляем таблицу в нижнюю группу
        #self.tbl.setQuery("SELECT collection, numOfPages, COUNT(books.name) from collections LEFT JOIN books ON collections.id = books.collectionId GROUP BY collection")
        self.tbl.clicked.connect(self.openCollectionByRow) # Подключаем обработчик нажатия на строчку

    def reload(self):
        path = self.path_input.text().split("/")
        if (len(path) != 1 and not (len(path) == 2 and path[0] == "Сборники")) or path[0] not in paths.keys():
            self.alert = QMessageBox(QMessageBox.Icon.Critical, "Ошибка", "Неверный путь", QMessageBox.StandardButton.Discard, self)
            self.alert.show()
            return
        if path[0] == "Сборники" and len(path) == 2:
            v = "collection" if self.select_on_collection.getValue() == 0 else "name"
            self.tbl.setQuery(paths["Авторы"][0] + f" WHERE {v}=\"{path[1]}\"")
            return
        v = paths[self.path_input.text()]
        self.tbl.setQuery(v[0])

        # Установим заголовки столбцов
        Qt_Horisontal = Qt.Orientation.Horizontal
        for ind, header in enumerate(v[1]):
            self.tbl.model().setHeaderData(ind, Qt_Horisontal, header)

    def openCollectionByRow(self, v: QModelIndex):
        path = self.path_input.text().split("/")
        if (len(path) > 1 and path[0] != "Сборники") or path[0] not in paths.keys():
            print(123243)
            return
        getCol = lambda column: self.tbl.sqlModel.data(
            self.tbl.sqlModel.index(v.row(), column), Qt.ItemDataRole.DisplayRole
        )
        self.path_input.setText(path[0] + "/" + getCol(0))
        self.reload()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Зададим тип базы данных
    db = QSqlDatabase.addDatabase('QSQLITE')
    # Укажем имя базы данных
    db.setDatabaseName("db.db")
    # И откроем подключение
    db.open()
    table = MainWindow(db)
    table.show()
    sys.exit(app.exec())
