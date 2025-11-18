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
    QSizePolicy
)
from DBTable import DBTableWidget
from RadioList import RadioListWidget
from PyQt6.QtCore import Qt, QModelIndex
from PyQt6.QtSql import QSqlDatabase


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Вкладкомания 2.0")  # Заголовок окна
        self.setGeometry(100, 100, 800, 600)  # Размеры окна

        self.tab1_layout = QVBoxLayout()

        vertical_layout = QHBoxLayout()
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
        back_btn = QPushButton("🡠")
        h = back_btn.sizeHint().height() # Стандарная высота кнопки
        back_btn.setFixedSize(h, h) # Делаем кнопку квадратной
        back_btn.setStyleSheet(btn_style)
        back_btn.clicked.connect(lambda: self.w.adjustSize())
        vertical_layout.addWidget(back_btn)
        reload_btn = QPushButton("⟳")
        reload_btn.clicked.connect(lambda: print(self.w.minimumSize().width(), self.w.sizeHint().width(), self.w.width()))
        reload_btn.setFixedSize(h, h) # Делаем кнопку квадратной
        reload_btn.setStyleSheet(btn_style)
        vertical_layout.addWidget(reload_btn)
        l = QLineEdit("ghyhnbgfnfb/gtdhtrgf")
        
        l.setStyleSheet("""
            QLineEdit {
                border: 2px solid #dcdcdc;
                border-radius: 10px;
                padding: 8px 12px;
                font-size: 14px;
                background-color: #ffffff;
                selection-background-color: #4CAF50;
            }
        """)
        vertical_layout.addWidget(l)
        self.tab1_layout.addLayout(vertical_layout)
        
        # Зададим тип базы данных
        self.db = QSqlDatabase.addDatabase('QSQLITE')
        # Укажем имя базы данных
        self.db.setDatabaseName("db.db")
        # И откроем подключение
        self.db.open()

        self.horizontal_layout = QSplitter()

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
        self.tbl.model().setHeaderData(2, Qt_Horisontal, "К-во рассказов")

        self.rlw = RadioListWidget("При открытии сборника", ["Открывать список авторов", "Открывать список рассказов"], lambda v: print(v))
        self.rlw1 = RadioListWidget("При открытии автора", ["Открывать список сборников", "Открывать список рассказов"], lambda v: print(v))

        self.modes_list = QVBoxLayout()
        self.modes_list.addWidget(QPushButton("Сборники"))
        self.modes_list.addWidget(QPushButton("Авторы"))
        self.modes_list.addWidget(QPushButton("Рассказы"))
        self.modes_list.addLayout(self.rlw)
        self.modes_list.addLayout(self.rlw1)
        self.modes_list.addStretch(1)
        self.w = QWidget()
        self.w.setLayout(self.modes_list)
        self.horizontal_layout.addWidget(self.w)
        self.horizontal_layout.addWidget(self.tbl)
        
        self.tab1_layout.addWidget(self.horizontal_layout)

        self.setLayout(self.tab1_layout)

        "SELECT author, COUNT(books.name) from authors LEFT JOIN books ON authors.id = books.authorId GROUP BY author"

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
            f"""К-во рассказов: {getCol(2)}\n"""
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
            f"""К-во рассказов: {getCol(1)}\n"""
        )
        self.w.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    table = MainWindow()
    table.show()
    sys.exit(app.exec())
