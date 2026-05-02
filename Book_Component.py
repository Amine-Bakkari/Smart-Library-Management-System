from customtkinter import *
from PIL import Image

class Book_Component(CTkFrame):
    def __init__(self, parent, name, price, available, image, BorrowFunction, RetrieveFunction):
        super().__init__(parent)
        PIimage = Image.open(image)
        self.configure(width=415, height=120, corner_radius=10)

        image_label = CTkLabel(self, text="", image=CTkImage(PIimage, size=(75,108)))
        image_label.place(x=10, y=5)

        name_label = CTkLabel(self, text=f"{name}", font=("Arial", 18, "bold"), bg_color="#DBDBDB")
        name_label.place(x=130, y=5, relwidth=0.5)

        price_label = CTkLabel(self, text=f"Price: {price:.2f}$", font=("Arial", 18), text_color="#00D315", bg_color="#DBDBDB")
        price_label.place(x=120, y=40)

        available_label = CTkLabel(self, text=f"Available: {available}", font=("Arial", 18),text_color="#00D315", bg_color="#DBDBDB")
        available_label.place(x=270, y=40)

        book_borrow_button = CTkButton(self, text="Borrow", font=("Arial", 14), width=100, corner_radius=10, bg_color="#DBDBDB", command=BorrowFunction)
        book_borrow_button.place(x=130, y=80)

        book_retrieve_button = CTkButton(self, text="Retrieve", font=("Arial", 14), width=100, corner_radius=10, bg_color="#DBDBDB", command=RetrieveFunction)
        book_retrieve_button.place(x=240, y=80)

