from PIL import Image
from customtkinter import *
from sqlite3 import *
import datetime

from zope import event

class BookAccess(CTk):
    def __init__(self):
        super().__init__()
        self.title("Book access")
        self.geometry("2000x1000+0+0")
        # self.attributes("-fullscreen", True)

        BookInfosFrame = CTkFrame(self, width=1260, height=300, fg_color="#2b2b2b")
        BookInfosFrame.place(x=10, y=10)

        BorrowFrame = CTkScrollableFrame(self, width=1240, height=355, fg_color="#58ffca")
        BorrowFrame.place(x=10, y=320)

        searchEngine = SearchEngine(BorrowFrame)
        searchEngine.pack(padx=10, pady=10)

        # StudentInfosFrame = StudentInfos(BorrowFrame, "John Doe", "123456789")
        # StudentInfosFrame.pack(padx=10, pady=10)

        self.mainloop()

def search(StudentID, master):
    DBF = connect("Library-DataBase.db")

    cursor = DBF.cursor()
    cursor.execute("SELECT * FROM Students WHERE student_id = ?", (StudentID,))
    data = cursor.fetchone()
    if data:
        StudentShow(data, master)
    else:
        print("Student not found.")

    DBF.commit()
    DBF.close()

def StudentShow(StudentInfos, master):
    def clear_frame(frame):
        for widget in frame.winfo_children():
            if widget == frame.winfo_children()[0]:
                continue
            else:
                widget.destroy()

    clear_frame(master)
    StudentName = StudentInfos[0]
    StudentID = StudentInfos[1]
    StudentInfosFrame = StudentInfosShow(master, StudentName, StudentID)
    StudentInfosFrame.pack(padx=10, pady=10)

def keyBind(event, search_query, master):
    event = event.char
    if event == "\r":
        search(search_query, master)

class SearchEngine(CTkFrame):
    def __init__(self, master, SearchEngineFunction=search):
        super().__init__(master)

        self.configure(width=580, height=45, fg_color="transparent", corner_radius=50)
        
        SearchEngineEntry = CTkEntry(self, width=500, height=40, placeholder_text="Search for a student", corner_radius=50, font=CTkFont(size=15))
        SearchEngineEntry.place(x=0, y=0)
        SearchEngineEntry.bind("<KeyRelease>", lambda event: keyBind(event, SearchEngineEntry.get(), master))

        SearchEngineButton = CTkButton(self, width=40, height=40, text="", corner_radius=100, fg_color="transparent", border_color="#ffc711", border_width=2, hover_color="#ff9741", command= lambda: SearchEngineFunction(SearchEngineEntry.get(), master), image=CTkImage(Image.open("External Materials/Search.png"), size=(20, 20)))
        SearchEngineButton.place(x=510, y=0)

class StudentInfosShow(CTkFrame):
    def __init__(self, master, StudentName, StudentID):
        super().__init__(master)
        self.configure(width=1080, height=100, fg_color="#745b41", corner_radius=10)

        studentName = CTkLabel(self, text=f"Name: {StudentName}", font=CTkFont(size=20))
        studentName.place(x=10, y=10)

        studentID = CTkLabel(self, text=  f"ID: {StudentID}", font=CTkFont(size=20))
        studentID.place(x=10, y=40)

        BorrowdateEntry = CTkEntry(self, width=120, height=30, placeholder_text="Borrow date", corner_radius=10, font=CTkFont(size=15))
        BorrowdateEntry.place(x=700, y=10)
        BorrowdateEntry.insert(0, datetime.date.today().strftime("%Y-%m-%d"))

        ReturndateEntry = CTkEntry(self, width=120, height=30, placeholder_text="Return date", corner_radius=10, font=CTkFont(size=15))
        ReturndateEntry.place(x=700, y=50)
        ReturndateEntry.insert(0, datetime.date.today().strftime("%Y-%m-"))

        BorrowButton = CTkButton(self, width=100, height=40, text="Borrow", font=("Arial", 15), corner_radius=10, fg_color="#ffae58", hover_color="#6eff6e")
        BorrowButton.place(x=900, y=30)




BookAccess()