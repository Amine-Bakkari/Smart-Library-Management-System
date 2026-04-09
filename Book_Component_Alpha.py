from customtkinter import *
from PIL import Image

class BookComponent:
    def __init__(self, master, name, price, available, image, BorrowFunction, RetrieveFunction):
        self.book_frame = CTkFrame(master, width=400, height=120, corner_radius=10).pack()
        PIimage = Image.open(image)
        ctkimage = CTkImage(PIimage, size=(75,108))
        self.image_label = CTkLabel(self.book_frame, text="", image=ctkimage).place(x=60, y=5)
        self.name_label = CTkLabel(self.book_frame, text=name, font=("Arial", 25, "bold"), bg_color="#DBDBDB").place(x=240, y=5)
        self.price_label = CTkLabel(self.book_frame, text=f"{price:.2f}$", font=("Arial", 18), text_color="#00D315", bg_color="#DBDBDB").place(x=170, y=40)
        self.available_label = CTkLabel(self.book_frame, text=f"Available: {available}", font=("Arial", 18),text_color="#00D315", bg_color="#DBDBDB").place(x=330, y=40)
        self.book_borrow_button = CTkButton(self.book_frame, text="Borrow", font=("Arial", 14), width=100, corner_radius=10, bg_color="#DBDBDB", command=BorrowFunction).place(x=180, y=80)
        self.book_retrieve_button = CTkButton(self.book_frame, text="Retrieve", font=("Arial", 14), width=100, corner_radius=10, bg_color="#DBDBDB", command=RetrieveFunction).place(x=290, y=80)