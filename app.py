import sqlite3
db = sqlite3.connect("books-library.db")
cursor = db.cursor()
cursor.execute("CREATE TABLE books (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL UNIQUE, author varchar(250) "
               "NOT NULL, rating FLOAT NOT NULL)")
