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
    QPushButton,
    QLabel,
)
from PyQt6.QtCore import Qt, QModelIndex
from DBTable import DBTableWidget
from PyQt6.QtSql import QSqlDatabase


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вкладкомания 2.0")  # Заголовок окна
        self.setGeometry(100, 100, 800, 600)  # Размеры окна
        
        # Зададим тип базы данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        self.db.setDatabaseName("db.db")
        # И откроем подключение
        self.db.open()

        self.tabs = QTabWidget()  # Создаем вкладки
        self.setCentralWidget(self.tabs)

        # region Сборники
        self.collections_tab = QWidget()  # Создаем вкладку "Сборники"
        self.tabs.addTab(self.collections_tab, "Сборники")

        # Создаем таблицу
        self.tbl = DBTableWidget(
            self.db,
            "SELECT collection, numOfPages, COUNT(books.name) from collections LEFT JOIN books ON collections.id = books.collectionId GROUP BY collection",
        )  # Создаем таблицу
        self.tbl.clicked.connect(self.openCollectionByRow)

        # Установим заголовки столбцов
        Qt_Horisontal = Qt.Orientation.Horizontal
        self.tbl.model().setHeaderData(0, Qt_Horisontal, "Название сборника")
        self.tbl.model().setHeaderData(1, Qt_Horisontal, "К-во страниц")
        self.tbl.model().setHeaderData(2, Qt_Horisontal, "К-во книг")

        tab1_layout = QVBoxLayout()  # Центрируем её внутри вкладки
        tab1_layout.addWidget(self.tbl)
        self.collections_tab.setLayout(tab1_layout)

        # region Авторы
        self.authors_tab = QWidget()  # Создаем вкладку "Авторы"
        self.tabs.addTab(self.authors_tab, "Авторы")

        # Создаем таблицу
        self.tbl1 = DBTableWidget(
            self.db,
            "SELECT author, COUNT(books.name) from authors LEFT JOIN books ON authors.id = books.authorId GROUP BY author",
        )  # Создаем таблицу
        self.tbl1.clicked.connect(self.openAuthorByRow)

        # Установим заголовки столбцов
        Qt_Horisontal = Qt.Orientation.Horizontal
        self.tbl1.model().setHeaderData(0, Qt_Horisontal, "Имя автора")
        self.tbl1.model().setHeaderData(1, Qt_Horisontal, "К-во произведений")

        tab2_layout = QVBoxLayout()  # Центрируем её внутри вкладки
        tab2_layout.addWidget(self.tbl1)
        self.authors_tab.setLayout(tab2_layout)

    def openCollectionByRow(self, v: QModelIndex):
        self.w = QWidget()
        self.w.setGeometry(200, 200, 300, 200)
        getCol = lambda column: self.tbl.sqlModel.data(
            self.tbl.sqlModel.index(v.row(), column), Qt.ItemDataRole.DisplayRole
        )
        l = QLabel(self.w)
        self.w.setWindowTitle(getCol(0))
        l.setText(
            f"""Название сборника: {getCol(0)}\n"""
            f"""К-во страниц: {getCol(1)}\n"""
            f"""К-во книг: {getCol(2)}\n"""
        )
        self.w.show()

    def openAuthorByRow(self, v: QModelIndex):
        self.w = QWidget()
        self.w.setGeometry(200, 200, 300, 200)
        getCol = lambda column: self.tbl.sqlModel.data(
            self.tbl1.sqlModel.index(v.row(), column), Qt.ItemDataRole.DisplayRole
        )
        l = QLabel(self.w)
        self.w.setWindowTitle(getCol(0))
        l.setText(
            f"""Название сборника: {getCol(0)}\n"""
            f"""К-во книг: {getCol(1)}\n"""
        )
        self.w.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = MainWindow()
    table.show()
    sys.exit(app.exec())
