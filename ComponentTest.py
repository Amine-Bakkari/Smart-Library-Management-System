from customtkinter import *
from Book_Component_Alpha import Book_Component
from sqlite3 import *

def hello():
    return CTkLabel(app, text="Hello World").pack()

app = CTk()
app.geometry("500x500")

Frame = CTkScrollableFrame(app, width=400, height=400, bg_color="#5DFFE9", fg_color="#5DFFE9", corner_radius=10)
Frame.pack(padx=10, pady=10)

DBF = connect("Library-DataBase.db")
cursor = DBF.cursor()
books =cursor.execute("SELECT * FROM books").fetchall()
for book in books:
    Book_Component(Frame, book[0], book[3], book[5], book[6], hello, hello).pack(pady=10)
DBF.close()

app.mainloop()