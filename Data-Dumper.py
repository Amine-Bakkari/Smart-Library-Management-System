from sqlite3 import *

students = [("C364714335", "ahmed haj", "null"),
            ("B435671257", "jamal jeddari", "null"),
            ("A134683465", "nada kawi", "null"),
            ("D435671257", "mohamed elshazly", "null"),
            ("E134683465", "sara mohamed", "null"),
            ("F435671257", "yousef mohamed", "null"),
            ("G134683465", "ahmed badr", "null"),
            ("H245781326", "fatima hassan", "null"),
            ("I562304781", "karim ali", "null"),
            ("J834672015", "leila amira", "null"),
            ("K128694537", "hassan rashid", "null"),
            ("L456781234", "mona khalid", "null"),
            ("M789012345", "omar hassan", "null"),
            ("N321456789", "aisha mohammed", "null"),
            ("O654321098", "tariq ibrahim", "null"),
            ("P987654321", "dina saleh", "null"),
            ("Q147258369", "rashed samir", "null"),
            ("R369852147", "layla sani", "null"),
            ("S258369741", "amina nasir", "null"),
            ("T741963258", "sameer hamad", "null"),
            ("U852147369", "huda ali", "null"),
            ("V369741852", "bilal fateh", "null"),
            ("W147852963", "noura ahmed", "null"),
            ("X963258741", "samir rashid", "null"),
            ("Y258963147", "mariam ali", "null"),
            ("Z741258963", "mahdi salem", "null"),

]

books = [
    ("Nature", "Sciences", "WEJ435KLK235", 30, 10, 10),
    ("Fluent English", "Language", "WEJ435KLK236", 25, 5, 5),
    ("100 words nature", "Sciences", "WEJ435KLK237", 20, 8, 8),
    ("The ten day draft", "Fiction", "WEJ435KLK238", 15, 6, 6),
    ("Robin hood", "Fiction", "WEJ435KLK239", 10, 12, 12),
    ("Arthur hailey", "Fiction", "WEJ435KLK241", 18, 7, 7),
    ("Nature milestones", "Sciences", "WEJ435KLK240", 35, 4, 4),
    ("Dark psychology", "Psychology", "WEJ435KLK242", 22, 9, 9),
    ("Dirk gently", "Fiction", "WEJ435KLK243", 12, 11, 11),
    ("Mars", "Astronomy", "WEJ435KLK244", 28, 3, 3)
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