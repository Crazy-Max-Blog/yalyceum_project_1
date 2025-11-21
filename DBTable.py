from PyQt6.QtWidgets import (
    QTableView,
    QHeaderView,
    QAbstractItemView,
)
from PyQt6.QtCore import Qt, QSortFilterProxyModel
from PyQt6.QtSql import QSqlQueryModel


class DBTableWidget(QTableView):
    def __init__(self, db, query=None, parent=None):
        super().__init__(parent)

        self.db = db
        self.query = query

        # Настраиваем таблицу:

        # Запрещаем редактирование таблицы
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        # Растягиваем столбцы
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        # Можно выделять только строки
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        # Выделяем нечетные строки
        self.setAlternatingRowColors(True)
        # Включаем сортировку
        self.setSortingEnabled(True)

        # Загружаем данные
        self.connectDB()

    def setDB(self, db):
        self.db = db
        self.connectDB()

    def setQuery(self, query):
        self.query = query
        self.loadData()

    def connectDB(self):
        # Создадим модельку
        self.sqlModel = QSqlQueryModel(self)
        self.sqlModel.setQuery(self.query, self.db)

        # Создадим прокси модель для сортировки
        self.proxyModel = QSortFilterProxyModel(self)
        self.proxyModel.setSourceModel(self.sqlModel)
        self.proxyModel.setSortRole(Qt.ItemDataRole.DisplayRole)

        # Подключим прокси модель к таблице
        self.setModel(self.proxyModel)

    def loadData(self):
        if not self.dbname:
            return

        self.sqlModel.setQuery(self.query, self.db)
