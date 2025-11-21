create = [
    """
CREATE TABLE IF NOT EXISTS authors (
    id     INTEGER PRIMARY KEY
                   UNIQUE
                   NOT NULL,
    author TEXT
);""",
    """
CREATE TABLE IF NOT EXISTS collections (
    id         INTEGER PRIMARY KEY
                       UNIQUE
                       NOT NULL,
    collection TEXT,
    numOfPages INTEGER
);""",
    """
CREATE TABLE IF NOT EXISTS books (
    name             TEXT,
    authorId         INTEGER REFERENCES authors (id),
    pagesNum         INTEGER,
    collectionId     INTEGER REFERENCES collections (id),
    pageInCollection INTEGER
);""",
]

paths = {
    "collections": [
        "SELECT collection, numOfPages, COUNT(books.name) from collections LEFT JOIN books ON collections.id = books.collectionId GROUP BY collection",
        ["Сборник", "Количество рассказов", "Общее количество страниц"],
    ],
    "authors": [
        "SELECT author, COUNT(books.name) from authors LEFT JOIN books ON authors.id = books.authorId LEFT JOIN collections ON collections.id = books.collectionId GROUP BY author",
        ["Автор", "Количество рассказов"],
    ],
    "books": [
        "SELECT name, author, collection, pagesNum, pageInCollection from books LEFT JOIN authors ON books.authorId = authors.id LEFT JOIN collections ON books.collectionId = collections.id",
        ["Название", "Автор", "Сборник", "К-во страниц", "Номер страницы в сборнике"],
    ],
}
