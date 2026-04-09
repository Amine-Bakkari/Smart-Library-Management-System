from customtkinter import *
from Book_Component_Alpha import BookComponent

def hello():
    return CTkLabel(app, text="Hello World").pack()

app = CTk()
app.geometry("500x500")

Book = BookComponent(app, "Nature", 19.99, 5, "Books_Images/Book1.jpg", hello, hello)

app.mainloop()