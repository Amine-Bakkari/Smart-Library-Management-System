from customtkinter import *
from PIL import Image



app = CTk()
app.geometry("500x500")
class Product:
    def __init__(self, name, price, image, add_to_cart):
        self.add_to_cart = add_to_cart
        self.product_frame = CTkFrame(app, width=400, height=120)
        self.product_frame.pack(pady=20)
        self.Image = CTkImage(Image.open(image), size=(100, 100))
        self.image_label = CTkLabel(self.product_frame, image=self.Image, text="")
        self.image_label.place(x=10, y=0, relwidth=0.25, relheight=1)
        self.name_label = CTkLabel(self.product_frame, text=name, font=("Arial", 16))
        self.name_label.place(x=120, y=10)
        self.price_label = CTkLabel(self.product_frame, text=f"${price:.2f}", font=("Arial", 14))
        self.price_label.place(x=120, y=50)
        self.add_to_cart_button = CTkButton(self.product_frame, text="Add to Cart", command=self.add_to_cart)
        self.add_to_cart_button.place(x=200, y=40)

def add_to_cart(name):
    print(f"Added {name} to cart")

products_list = [
    {"name": "T-Shirt", "price": 21.99, "image": "T-Shirt.webp"},
    {"name": "Silk-Shirt", "price": 29.99, "image": "Silk-Shirt.webp"},
    {"name": "Summer-Dress", "price": 49.99, "image": "Summer-Dress.webp"}
]
for product in products_list:
    name = product["name"]
    price = product["price"]
    image = product["image"]

    Product(name, price, image, lambda: add_to_cart(name))

# Product1 = Product("T-Shirt", 21.99, "T-Shirt.webp", lambda: add_to_cart("T-Shirt"))
# Product2 = Product("Silk-Shirt", 21.99, "Silk-Shirt.webp", lambda: add_to_cart("Silk-Shirt"))
# Product3 = Product("Summer-Dress", 21.99, "Summer-Dress.webp", lambda: add_to_cart("Summer-Dress"))
app.mainloop()