from PyQt6.QtWidgets import (
    QVBoxLayout,
    QDialog,
    QDialogButtonBox,
    QLayout,
    QLineEdit,
    QFormLayout,
    QSpinBox,
    QComboBox,
)
from RadioList import RadioListWidget

from PyQt6.QtSql import QSqlQuery

def getValuesInColumn(query: QSqlQuery) -> list:
    res = []
    while query.next():
        res.append(query.value(0))
    return res


class AddDataWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление данных")
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.list = RadioListWidget("Выберите, что нужно добавить:", ["Сборник", "Автора", "Рассказ"])
        self.btns.accepted.connect(self.next)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addLayout(self.list)
        self.mainLayout.addWidget(self.btns)
        # Запрещаем изменение размера окна
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setModal(True)

    def next(self):
        match self.list.getValue():
            case 0:
                self.w = AddCollectionWindow()
                self.w.show()
            case 1:
                self.w = AddAuthorWindow()
                self.w.show()
            case 2:
                self.w = AddBookWindow()
                self.w.show()
        self.close()


class AddCollectionWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление сборника")
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.btns.accepted.connect(self.ok)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.formLayout = QFormLayout()
        self.mainLayout.addLayout(self.formLayout)

        self.name = QLineEdit()
        self.formLayout.addRow("Название сборника:", self.name)

        self.numOfPages = QSpinBox()
        self.numOfPages.setMaximum(10**6)  # Скорее всего больше не будет...
        self.formLayout.addRow("К-во страниц сборника:", self.numOfPages)

        self.mainLayout.addWidget(self.btns)
        # Запрещаем изменение размера окна
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setModal(True)

    def ok(self):
        query = QSqlQuery()
        query.exec(
            f'INSERT INTO collections (collection, numOfPages) VALUES ("{self.name.text()}", {self.numOfPages.value()})'
        )
        self.close()


class AddAuthorWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление автора")
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.btns.accepted.connect(self.ok)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.formLayout = QFormLayout()
        self.mainLayout.addLayout(self.formLayout)

        self.name = QLineEdit()
        self.formLayout.addRow("Имя автора:", self.name)

        self.mainLayout.addWidget(self.btns)
        # Запрещаем изменение размера окна
        self.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.setModal(True)

    def ok(self):
        query = QSqlQuery()
        query.exec(
            f'INSERT INTO authors (author) VALUES ("{self.name.text()}")'
        )
        self.close()



class AddBookWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавление рассказа")
        self.btns = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        self.btns.accepted.connect(self.ok)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)

        self.formLayout = QFormLayout()
        self.mainLayout.addLayout(self.formLayout)

        self.collection = QComboBox()
        self.collection.addItems(getValuesInColumn(QSqlQuery("SELECT collection FROM collections")))
        self.collection.setMinimumWidth(200)
        self.formLayout.addRow("Название сборника:", self.collection)

        self.author = QComboBox()
        self.author.addItems(getValuesInColumn(QSqlQuery("SELECT author FROM authors")))
        self.author.setMinimumWidth(200)
        self.formLayout.addRow("Название сборника:", self.author)

        self.name = QLineEdit()
        self.formLayout.addRow("Название рассказа:", self.name)

        self.numOfPages = QSpinBox()
        self.numOfPages.setMaximum(10**6)  # Скорее всего больше не будет...
        self.formLayout.addRow("К-во страниц рассказа:", self.numOfPages)

        self.pageInCollection = QSpinBox()
        self.pageInCollection.setMaximum(10**6)  # Скорее всего больше не будет...
        self.formLayout.addRow("Номер страницы в сборнике:", self.pageInCollection)

        self.mainLayout.addWidget(self.btns)
        self.setModal(True)

    def ok(self):
        query = QSqlQuery()
        name = self.name.text()
        _author = self.author.currentText()
        _collection = self.collection.currentText()
        numOfPages = self.numOfPages.value()
        pageInCollection = self.pageInCollection.value()
        query.exec(f"SELECT id FROM authors WHERE author = '{_author}'")
        query.next()
        author = query.value(0)
        query.exec(f"SELECT id FROM collections WHERE collection = '{_collection}'")
        query.next()
        collection = query.value(0)
        query.prepare(
            "INSERT INTO books (name, authorId, collectionId, pagesNum, pageInCollection) VALUES (:name, :authorId, :collectionId, :pagesNum, :pageInCollection)"
        )
        query.bindValue(":name", name)
        query.bindValue(":authorId", author)
        query.bindValue(":collectionId", collection)
        query.bindValue(":pagesNum", numOfPages)
        query.bindValue(":pageInCollection", pageInCollection)
        query.exec()
        self.close()
