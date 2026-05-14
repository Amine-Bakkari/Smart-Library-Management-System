from customtkinter import *
from Book_Component import Book_Component
from CTkMessagebox import CTkMessagebox
from sqlite3 import *

class MainApp(CTk):
    def __init__(self):
        super().__init__()
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}+0+0")

        BooksFrame = CTkScrollableFrame(self, width=500, height=500, fg_color="#404745")
        BooksFrame.pack(padx=10, pady=10)

        DBF = connect("Library-DataBase.db")
        cursor = DBF.cursor()
        books = cursor.execute("SELECT * FROM Books").fetchall()
        for book in books:
            book_component = Book_Component(BooksFrame, book[0], book[3], book[4], book[6], book[7])
            book_component.pack(padx=10, pady=10)
            

        self.mainloop()

MainApp()