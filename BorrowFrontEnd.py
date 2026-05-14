from PIL import Image
from customtkinter import *
from sqlite3 import *
import datetime
from CTkMessagebox import CTkMessagebox


BookID = str()

class BookBorrowAccess(CTk):
    def __init__(self, BookId):
        super().__init__()
        self.title("Book access")
        self.geometry("2000x1000+0+0")
        global BookID
        BookID = BookId
        DBF = connect("Library-DataBase.db")
        cursor = DBF.cursor()
        book = cursor.execute("SELECT * FROM Books WHERE book_serial_number = ?", (BookID,)).fetchone()

        BookInfosFrame = CTkFrame(self, width=1240, height=300, fg_color="#2b2b2b")
        BookInfosFrame.place(x=10, y=10)

        BookIdentity = BookInfosShow(BookInfosFrame, book)
        BookIdentity.pack(padx=10, pady=10)

        BorrowFrame = CTkScrollableFrame(self, width=1240, height=355, fg_color="#58ffca")
        BorrowFrame.place(x=10, y=320)

        searchEngine = SearchEngine(BorrowFrame, searchStudents, keyBind)
        searchEngine.pack(padx=10, pady=10)

        DBF.commit()
        DBF.close()

        self.mainloop()

def searchStudents(StudentID, master):
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    cursor.execute("SELECT * FROM Students WHERE student_id = ?", (StudentID,))
    data = cursor.fetchone()
    if data:
        StudentShow(data, master, StudentInfosShow)
    else:
        CTkMessagebox(title="Info", message="Student not found.", icon="info", options=["OK"], )
        return

    DBF.commit()
    DBF.close()

def StudentShow(StudentInfos, master, StudentInfosShow):
    def clear_frame(frame):
        for widget in frame.winfo_children():
            if widget == frame.winfo_children()[0]:
                continue
            else:
                widget.destroy()

    clear_frame(master)
    StudentName = StudentInfos[1]
    StudentID = StudentInfos[0]
    studentDisciplinaryStatus = StudentInfos[2]
    StudentInfosFrame = StudentInfosShow(master, StudentName, StudentID, studentDisciplinaryStatus)
    StudentInfosFrame.pack(padx=10, pady=10)

def keyBind(event, search_query, master):
    event = event.char
    if event == "\r":
        searchStudents(search_query, master)


class BookInfosShow(CTkFrame):
    def __init__(self, master, BookInfos):
        super().__init__(master)
        self.configure(width=1242, height=300, fg_color="#2b2b2b", corner_radius=10)

        bookImage = CTkLabel(self, text="", image=CTkImage(Image.open(BookInfos[7]), size=(217, 290)))
        bookImage.place(x=10, y=0)

        bookTitle = CTkLabel(self, text=f"{BookInfos[0]}", font=CTkFont(size=40), text_color="White")
        bookTitle.place(x=500, y=10)

        bookAuthor = CTkLabel(self, text=f"Author:        {BookInfos[1]}", font=CTkFont(size=20), text_color="White")
        bookAuthor.place(x=500, y=110)

        bookGenre = CTkLabel(self, text=f"Genre:          {BookInfos[2]}", font=CTkFont(size=20), text_color="White")
        bookGenre.place(x=500, y=150)

        bookAvailable = CTkLabel(self, text=f"Available:    {BookInfos[6]}", font=CTkFont(size=20), text_color="White")
        bookAvailable.place(x=500, y=190)

        bookPrice = CTkLabel(self, text=f"Price:            {BookInfos[5]}$", font=CTkFont(size=20), text_color="White")
        bookPrice.place(x=500, y=230)

class SearchEngine(CTkFrame):
    def __init__(self, master, SearchEngineFunction=searchStudents, keyBind=keyBind):
        super().__init__(master)

        self.configure(width=580, height=45, fg_color="transparent", corner_radius=50)
        
        SearchEngineEntry = CTkEntry(self, width=500, height=40, placeholder_text="Search for a student", corner_radius=50, font=CTkFont(size=15))
        SearchEngineEntry.place(x=0, y=0)
        SearchEngineEntry.bind("<KeyRelease>", lambda event: keyBind(event, SearchEngineEntry.get(), master))

        SearchEngineButton = CTkButton(self, width=40, height=40, text="", corner_radius=100, fg_color="transparent", border_color="#ffc711", border_width=2, hover_color="#ff9741", command= lambda: SearchEngineFunction(SearchEngineEntry.get(), master), image=CTkImage(Image.open("External Materials/Search.png"), size=(20, 20)))
        SearchEngineButton.place(x=510, y=0)

def CommitBorrow(StudentID, BorrowDate, RetrieveDate):
    global BookID
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    # Verify that the borrow date is before the retrieve date:
    try:
        BorrowDuration = (datetime.datetime.strptime(RetrieveDate, "%Y-%m-%d") - datetime.datetime.strptime(BorrowDate, "%Y-%m-%d")).days
    except ValueError:
        CTkMessagebox(title="Info", message="Invalid date format.", icon="info")
        DBF.close()
        return
    
    # Verify that the student exists:
    Student = cursor.execute("SELECT * FROM Students WHERE student_id = ?", (StudentID,)).fetchone()
    # StudentDisciplinaryStatus = StudentExist[2]
    # Verify that the book exists:
    BookExist = cursor.execute("SELECT * FROM Books WHERE book_serial_number = ?", (BookID,)).fetchone()
    # Verify that the book is available:
    BookAvailable = BookExist[5]
    # Verify that the student doesn't have already borrowed the book or any other book:
    StudentBorrowedBooks = cursor.execute("SELECT * FROM borrow WHERE student_id = ? AND return_date = ?", (StudentID, "")).fetchall()
    
    if Student and BookExist and BookAvailable > 0 and not StudentBorrowedBooks and BorrowDuration <= 7 and BorrowDuration >= 1:
        cursor.execute("INSERT INTO borrow(student_id, book_id, borrow_date, retrieve_date, return_date) VALUES (?, ?, ?, ?, ?)", (StudentID, BookID, BorrowDate, RetrieveDate, ""))
    elif not BookExist:
        CTkMessagebox(title="Info", message="Book not found.", icon="info")
    elif BookAvailable == 0:
        CTkMessagebox(title="Info", message="Book not available.", icon="info")
    elif BorrowDuration < 1:
        CTkMessagebox(title="Info", message="Borrow duration cannot be less than 1 day.", icon="info")
    elif StudentBorrowedBooks:
        CTkMessagebox(title="Info", message="Student already has a borrowed book.", icon="info")
    elif BorrowDuration > 7:
        CTkMessagebox(title="Info", message="Borrow duration cannot exceed 7 days.", icon="info")
    else:
        CTkMessagebox(title="Info", message="An error occurred.", icon="info")

    DBF.commit()
    DBF.close()

class StudentInfosShow(CTkFrame):
    def __init__(self, master, StudentName, StudentID, StudentDisciplinaryStatus):
        super().__init__(master)
        self.configure(width=1080, height=100, fg_color="#745b41", corner_radius=10)

        studentName = CTkLabel(self, text=f"Name: {StudentName}", font=CTkFont(size=20))
        studentName.place(x=10, y=10)

        studentID = CTkLabel(self, text=  f"ID: {StudentID}", font=CTkFont(size=20))
        studentID.place(x=10, y=40)

        studentdisciplinaryStatus = CTkLabel(self, text=f"Disciplinary status: {StudentDisciplinaryStatus.upper()}", font=CTkFont(size=20))
        studentdisciplinaryStatus.place(x=10, y=70)

        BorrowdateEntry = CTkEntry(self, width=120, height=30, placeholder_text="Borrow date", corner_radius=10, font=CTkFont(size=15))
        BorrowdateEntry.place(x=700, y=10)
        BorrowdateEntry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        ReturndateEntry = CTkEntry(self, width=120, height=30, placeholder_text="Return date", corner_radius=10, font=CTkFont(size=15))
        ReturndateEntry.place(x=700, y=50)
        ReturndateEntry.insert(0, datetime.date.today().strftime("%Y-%m-"))

        BorrowButton = CTkButton(self, width=100, height=40, text="Borrow", font=("Arial", 15), corner_radius=10, fg_color="#ffae58", hover_color="#6eff6e", command= lambda: CommitBorrow(StudentID, BorrowdateEntry.get(), ReturndateEntry.get()))
        BorrowButton.place(x=900, y=30)

def clearBorrowTable():
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    cursor.execute("DELETE FROM borrow")

    DBF.commit()
    DBF.close()

# BookBorrowAccess("WEJ435KLK238")
# clearBorrowTable()