import queries
from PyQt6.QtCore import Qt

_table = ""
_args = []
def _setTable(new_table):
    global _table, _args
    _table = new_table
    _args = []

def _addArg(name, value):
    _args.append((name, value))

tableToColumn = {
    "authors": "author",
    "collections": "collection",
}

def getQuery():
    tblQuery = queries.paths[_table][0].split(" GROUP BY ")
    result = tblQuery[0]
    if _args != []:
        result += f" WHERE {tableToColumn[_args[0][0]]}=\"{_args[0][1]}\""
        for arg in _args[1:]:
            result += f" AND {tableToColumn[arg[0]]}=\"{arg[1]}\""
    if len(tblQuery) == 2:
        result += " GROUP BY " + tblQuery[1]
    return result

def getText():
    result = _table
    if _args != []:
        result += f" WHERE {_args[0][0]} = \"{_args[0][1]}\""
        for arg in _args[1:]:
            result += f" AND {arg[0]} = \"{arg[1]}\""
    return result

def set(self, tbl, args=[]):
    global _args
    _setTable(tbl)
    _args = args
    self.tbl.setQuery(getQuery())

    # Установим заголовки столбцов
    Qt_Horisontal = Qt.Orientation.Horizontal
    for ind, header in enumerate(queries.paths[_table][1]):
        self.tbl.model().setHeaderData(ind, Qt_Horisontal, header)
    
    self.path_input.setText(getText())

def open(self, name):
    if _args == []:
        new_table = "authors" if _table == "collections" else "collections"
        new_arg = (_table, name)
        set(self, new_table, [new_arg])
    else:
        new_table = "books"
        new_arg = (_table, name)
        set(self, new_table, [new_arg] + _args)
    print(getQuery())