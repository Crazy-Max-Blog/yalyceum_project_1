import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QTableView, QHeaderView, QAbstractItemView
from PyQt6.QtCore import Qt, QAbstractTableModel, QSortFilterProxyModel
from PyQt6.QtSql import QSqlDatabase, QSqlQueryModel
         
class DBTableWidget(QTableView):
    def __init__(self, db, query=None, parent=None):
        super().__init__(parent)

        self.db = db
        self.query = query

        # Настраиваем таблицу
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers) # Запрещаем редактирование таблицы
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setSelectionBehavior(QTableView.SelectionBehavior.SelectRows)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)  # Включаем сортировку
        
        # Загружаем данные
        self.connectDB()
    
    def setDB(self, db):
        self.db = db
        self.connectDB()
    
    def setQuery(self, query):
        self.query = query
        self.connectDB()
    
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    table = DBTableWidget()
    window.setCentralWidget(table)
    window.show()
    sys.exit(app.exec())