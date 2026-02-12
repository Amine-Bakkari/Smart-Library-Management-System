from sqlite3 import *

students = [("C364714335", "ahmed haj", "null"),
            ("B435671257", "jamal jeddari", "null"),
            ("A134683465", "nada kawi", "null")
]

books = [
    ("rich dad", "financial", "WEJ435KLK235", 30, 10, 10),
    ("universal language", "culture", "NIDG34IJOI42", 50, 20, 20),
    ("the 7 habits", "self development", "KLK435JN2435", 100, 15, 15)
]

dbf = connect("Library-DataBase.db")
cursor = dbf.cursor()

# Create a table named students
cursor.execute("CREATE TABLE IF NOT EXISTS students(student_id TEXT PRIMRARY KEY, student_name TEXT, student_discipline TEXT DEFAULT NULL)")
# Create a table named books
cursor.execute("CREATE TABLE IF NOT EXISTS books(book_title TEXT PRIMARY KEY, book_type TEXT, book_serial_number TEXT, book_price INTEGER, book_possesion_number INTEGER, book_available_number INTEGER)")
# Create a table named borrow
cursor.execute("CREATE TABLE IF NOT EXISTS borrow(student_name TEXT, student_id TEXT, borrow_date TEXT, retrieve_date TEXT, book_title TEXT, return_date TEXT)")
# Insert at least 3 students in the students table
cursor.executemany("INSERT INTO students VALUES(?,?,?)", students)
# Insert at least 3 books in the books table
cursor.executemany("INSERT INTO books VALUES(?,?,?,?,?,?)", books)

dbf.commit()
dbf.close()