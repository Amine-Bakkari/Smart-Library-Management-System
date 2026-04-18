from sqlite3 import *

students = [("C364714335", "ahmed haj", "good"),
            ("B435671257", "jamal jeddari", "good"),
            ("A134683465", "nada kawi", "good"),
            ("D435671257", "mohamed elshazly", "good"),
            ("E134683465", "sara mohamed", "good"),
            ("F435671257", "yousef mohamed", "good"),
            ("G134683465", "ahmed badr", "good"),
            ("H245781326", "fatima hassan", "good"),
            ("I562304781", "karim ali", "good"),
            ("J834672015", "leila amira", "good"),
            ("K128694537", "hassan rashid", "good"),
            ("L456781234", "mona khalid", "good"),
            ("M789012345", "omar hassan", "good"),
            ("N321456789", "aisha mohammed", "good"),
            ("O654321098", "tariq ibrahim", "good"),
            ("P987654321", "dina saleh", "good"),
            ("Q147258369", "rashed samir", "good"),
            ("R369852147", "layla sani", "good"),
            ("S258369741", "amina nasir", "good"),
            ("T741963258", "sameer hamad", "good"),
            ("U852147369", "huda ali", "good"),
            ("V369741852", "bilal fateh", "good"),
            ("W147852963", "noura ahmed", "good"),
            ("X963258741", "samir rashid", "good"),
            ("Y258963147", "mariam ali", "good"),
            ("Z741258963", "mahdi salem", "good"),

]

books = [
    ("Nature", "Sciences", "WEJ435KLK235", 30, 10, 10, "Books_Images/Nature.jpg"),
    ("Fluent English", "Language", "WEJ435KLK236", 25, 5, 5, "Books_Images/Fluent English.jpg"),
    ("100 words nature", "Sciences", "WEJ435KLK237", 20, 8, 8, "Books_Images/100 words nature.jpg"),
    ("The ten day draft", "Fiction", "WEJ435KLK238", 15, 6, 6, "Books_Images/The ten day draft.jpg"),
    ("Robin hood", "Fiction", "WEJ435KLK239", 10, 12, 12, "Books_Images/Robin hood.jpg"),
    ("Arthur hailey", "Fiction", "WEJ435KLK241", 18, 7, 7, "Books_Images/Arthur hailey.jpg"),
    ("Nature milestones", "Sciences", "WEJ435KLK240", 35, 4, 4, "Books_Images/Nature milestones.jpg"),
    ("Dark psychology", "Psychology", "WEJ435KLK242", 22, 9, 9, "Books_Images/Dark psychology.jpg"),
    ("Dirk gently", "Fiction", "WEJ435KLK243", 12, 11, 11, "Books_Images/Dirk gently.jpg"),
    ("Mars", "Astronomy", "WEJ435KLK244", 28, 3, 3, "Books_Images/Mars.jpg")
]

dbf = connect("Library-DataBase.db")
cursor = dbf.cursor()

# Create a table named students
cursor.execute("CREATE TABLE IF NOT EXISTS students(student_id TEXT PRIMRARY KEY, student_name TEXT, student_discipline TEXT)")
# Create a table named books
cursor.execute("CREATE TABLE IF NOT EXISTS books(book_title TEXT PRIMARY KEY, book_type TEXT, book_serial_number TEXT, book_price INTEGER, book_possesion_number INTEGER, book_available_number INTEGER, book_image_path TEXT)")
# Create a table named borrow
cursor.execute("CREATE TABLE IF NOT EXISTS borrow(student_id TEXT, book_id TEXT, borrow_date TEXT, retrieve_date TEXT, return_date TEXT)")
# Insert at least 3 students in the students table
cursor.executemany("INSERT INTO students VALUES(?,?,?)", students)
# Insert at least 3 books in the books table
cursor.executemany("INSERT INTO books VALUES(?,?,?,?,?,?,?)", books)

dbf.commit()
dbf.close()