from PIL import Image
from customtkinter import *
from sqlite3 import *
import datetime
from CTkMessagebox import CTkMessagebox

BookID = str()

class BookAccess(CTk):
    def __init__(self, BookId):
        super().__init__()
        self.title("Book access")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")
        # self.state("zoomed")
        global BookID
        BookID = BookId
        DBF = connect("Library-DataBase.db")
        cursor = DBF.cursor()
        book = cursor.execute("SELECT * FROM Books WHERE book_serial_number = ?", (BookID,)).fetchone()

        BookInfosFrame = CTkFrame(self, width=1240, height=300, fg_color="#2b2b2b")
        BookInfosFrame.place(x=10, y=10)

        BookIdentity = BookInfosShow(BookInfosFrame, book)
        BookIdentity.pack(padx=10, pady=10)

        RetrieveFrame = CTkScrollableFrame(self, width=1240, height=355, fg_color="#58ffca")
        RetrieveFrame.place(x=10, y=320)

        searchEngine = SearchEngine(RetrieveFrame, searchStudents, keyBind)
        searchEngine.pack(padx=10, pady=10)

        DBF.commit()
        DBF.close()

        StudentShow(AutomaticStudentsSearch(), RetrieveFrame, StudentInfosShowComponent)

        self.mainloop()

def searchStudents(StudentID, master):
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    cursor.execute("SELECT * FROM borrow WHERE student_id = ?, book_id = ?", (StudentID, BookID))
    data = cursor.fetchone()
    if data:
        StudentShow(data, master, StudentInfosShowComponent)
    else:
        CTkMessagebox(title="Info", message="Student not found.", icon="info", options=["OK"], )
        return

    DBF.commit()
    DBF.close()

def StudentShow(BorrowsInfos, master, StudentInfosShowComponent):
    def clear_frame(frame):
        for widget in frame.winfo_children():
            if widget == frame.winfo_children()[0]:
                continue
            else:
                widget.destroy()

    clear_frame(master)
    DBF = connect("Library-DataBase.db")
    cursor = DBF.cursor()

    for BorrowInfos in BorrowsInfos:
        BorrowDate = BorrowInfos[2]
        RetrieveDate = BorrowInfos[3]
        StudentID = BorrowInfos[0]
        Student = cursor.execute("SELECT * FROM Students WHERE student_id = ?", (StudentID,)).fetchone()
        StudentName = Student[1]
        studentDisciplinaryStatus = Student[2]

        StudentInfosFrame = StudentInfosShowComponent(master, StudentName, StudentID, studentDisciplinaryStatus, BorrowDate, RetrieveDate)
        StudentInfosFrame.pack(padx=10, pady=10)
    
    DBF.commit()
    DBF.close()

def keyBind(event, search_query, master):
    event = event.char
    if event == "\r":
        searchStudents(search_query, master, StudentInfosShowComponent)


class BookInfosShow(CTkFrame): #I have to do some changes here to make it compatible with the retrieve front end
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

        bookPrice = CTkLabel(self, text=f"Price:            {BookInfos[5]} $", font=CTkFont(size=20), text_color="White")
        bookPrice.place(x=500, y=230)

def AutomaticStudentsSearch():
    DBF = connect(r"Library-DataBase.db")
    cursor = DBF.cursor()
    Students = cursor.execute("SELECT * FROM borrow WHERE book_id = ? AND return_date = ?", (BookID, "")).fetchall()
    DBF.commit()
    DBF.close()
    return Students

class SearchEngine(CTkFrame):
    def __init__(self, master, SearchEngineFunction, keyBind=keyBind):
        super().__init__(master)

        self.configure(width=580, height=45, fg_color="transparent", corner_radius=50)
        
        SearchEngineEntry = CTkEntry(self, width=500, height=40, placeholder_text="Search for a student", corner_radius=50, font=CTkFont(size=15))
        SearchEngineEntry.place(x=0, y=0)
        SearchEngineEntry.bind("<KeyRelease>", lambda event: keyBind(event, SearchEngineEntry.get(), master))

        SearchEngineButton = CTkButton(self, width=40, height=40, text="", corner_radius=100, fg_color="transparent", border_color="#ffc711", border_width=2, hover_color="#ff9741", command= lambda: SearchEngineFunction(SearchEngineEntry.get(), master, StudentInfosShowComponent), image=CTkImage(Image.open("External Materials/Search.png"), size=(20, 20)))
        SearchEngineButton.place(x=510, y=0)

def CommitRetrieve(StudentID, RetrieveDate):
    global BookID
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    # Verify that the borrow date is before the retrieve date:
    BorrowDate = cursor.execute("SELECT borrow_date FROM borrow WHERE student_id = ? AND book_id = ?", (StudentID, BookID)).fetchone()[0]
    try:
        BorrowDuration = (datetime.datetime.strptime(RetrieveDate, "%Y-%m-%d") - datetime.datetime.strptime(BorrowDate, "%Y-%m-%d")).days
    except ValueError:
        CTkMessagebox(title="Info", message="Invalid date format.", icon="info")
        DBF.close()
        return
    # Verify that the student exists:
    Student = cursor.execute("SELECT * FROM Students WHERE student_id = ?", (StudentID,)).fetchone()
    if not Student:
        CTkMessagebox(title="Info", message="Student not found.", icon="info")
        DBF.close()
        return
    # Verify that the book exists:
    Book = cursor.execute("SELECT * FROM Books WHERE book_serial_number = ?", (BookID,)).fetchone()
    if not Book:
        CTkMessagebox(title="Info", message="Book not found.", icon="info")
        DBF.close()
        return
    # Verify that the book is available:
    BookAvailable = Book[5]
    if not BookAvailable:
        CTkMessagebox(title="Info", message="Book is not available.", icon="info")
        DBF.close()
        return
    # Verify that the student has borrowed the book:
    StudentBorrowedBook = cursor.execute("SELECT * FROM borrow WHERE student_id = ? AND book_id = ? AND return_date = ?", (StudentID, BookID, "")).fetchone()
    if not StudentBorrowedBook:
        CTkMessagebox(title="Info", message="Student has not borrowed this book.", icon="info")
        DBF.close()
        return
    if BorrowDuration < 1:
        CTkMessagebox(title="Info", message="Retrieve date cannot be before borrow date.", icon="info")
        DBF.close()
        return

    cursor.execute("UPDATE borrow SET return_date = ? WHERE student_id = ? AND book_id = ?", (RetrieveDate, StudentID, BookID))

    DBF.commit()
    DBF.close()

class StudentInfosShowComponent(CTkFrame):
    def __init__(self, master, StudentName, StudentID, StudentDisciplinaryStatus, BorrowDate, RetrieveDate):
        super().__init__(master)
        self.configure(width=1080, height=100, fg_color="#745b41", corner_radius=10)

        studentName = CTkLabel(self, text=f"Name: {StudentName}", font=CTkFont(size=20))
        studentName.place(x=10, y=10)

        studentID = CTkLabel(self, text=  f"ID: {StudentID}", font=CTkFont(size=20))
        studentID.place(x=10, y=40)

        studentdisciplinaryStatus = CTkLabel(self, text=f"Disciplinary status: {StudentDisciplinaryStatus.upper()}", font=CTkFont(size=20))
        studentdisciplinaryStatus.place(x=10, y=70)

        BorrowDate = CTkLabel(self,   text=f"Borrow   date:  {BorrowDate}", font=CTkFont(size=20))
        BorrowDate.place(x=400, y=10)

        RetrieveDate = CTkLabel(self, text=f"Retrieve date:  {RetrieveDate}", font=CTkFont(size=20))
        RetrieveDate.place(x=400, y=40)

        ReturnLabel = CTkLabel(self,  text="Return    date:", font=CTkFont(size=20))
        ReturnLabel.place(x=400, y=70)

        ReturndateEntry = CTkEntry(self, width=120, height=30, placeholder_text="Return date", corner_radius=10, font=CTkFont(size=15))
        ReturndateEntry.place(x=530, y=70)
        ReturndateEntry.insert(0, datetime.date.today().strftime("%Y-%m-"))

        RetrieveButton = CTkButton(self, width=100, height=40, text="Retrieve", font=("Arial", 15), corner_radius=10, fg_color="#ffae58", hover_color="#6eff6e", command= lambda: CommitRetrieve(StudentID, ReturndateEntry.get()))
        RetrieveButton.place(x=900, y=30)

def clearBorrowTable():
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    cursor.execute("DELETE FROM borrow")

    DBF.commit()
    DBF.close()

BookAccess("WEJ435KLK239")
# clearBorrowTable()