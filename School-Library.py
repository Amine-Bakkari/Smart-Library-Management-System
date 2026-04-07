from customtkinter import *
import json as js

with open(r"C:\Users\Abdelaziz\Programation\PythonProjects\Smart Library Management System\Library-DataBase.json", "r") as DB:
    DataBase = js.load(DB)

Main = CTk()
Main.geometry("800x500")
Main.title("School Library Management System")

TitleLabel = CTkLabel(Main, text="Welcome to the School Library Management System", font=("Arial", 20))
TitleLabel.pack(pady=10 )

SearchingFrame = CTkFrame(Main, corner_radius=10, height=250)
SearchingFrame.pack(padx=20, fill="both")

SearchEntry = CTkEntry(SearchingFrame, width=215, placeholder_text="Enter book name or serial number")
SearchEntry.pack(pady=10)

def SearchHandling():
    Name = SearchEntry.get()
    for Book in DataBase["Books"]:
        if Book["Name"] == Name or Book["SerialNumber"] == Name:
            Name_label.configure(text=Book["Name"], text_color="green")
            Type_label.configure(text=Book["Type"], text_color="green")
            Price_label.configure(text=str(Book["Price"]) + " $", text_color="green")
            Possesion_label.configure(text=str(Book["PossesionNumber"]), text_color="green")
            return
        else: 
            Name_label.configure(text="Not Found", text_color="red")
            Type_label.configure(text="Not Found", text_color="red")
            Price_label.configure(text="Not Found", text_color="red")
            Possesion_label.configure(text="Not Found", text_color="red")

SearchTrigger = CTkButton(SearchingFrame, text="Search", command=SearchHandling)
SearchTrigger.pack(pady=10)

ResultFrame = CTkFrame(Main, corner_radius=10, height=110)
ResultFrame.pack(padx=20, pady=5, fill="both")

ResultNameLabel = CTkLabel(ResultFrame, text="Name:", font=("Arial", 14))
ResultNameLabel.place(x=50, y=10)
ResultTypeLabel = CTkLabel(ResultFrame, text="Type:", font=("Arial", 14))
ResultTypeLabel.place(x=50, y=70)

Name_label = CTkLabel(ResultFrame, text="", font=("Arial", 14))
Name_label.place(x=150, y=10)

Type_label = CTkLabel(ResultFrame, text="", font=("Arial", 14))
Type_label.place(x=150, y=70)

ResultPriceLabel = CTkLabel(ResultFrame, text="Price:", font=("Arial", 14))
ResultPriceLabel.place(x=500, y=10)
ResultPossesionLabel = CTkLabel(ResultFrame, text="Possession:", font=("Arial", 14))
ResultPossesionLabel.place(x=500, y=70)

Price_label = CTkLabel(ResultFrame, text="", font=("Arial", 14))
Price_label.place(x=600, y=10)

Possesion_label = CTkLabel(ResultFrame, text="", font=("Arial", 14))
Possesion_label.place(x=600, y=70)

SuggestionFrame = CTkFrame(Main, corner_radius=10, height=220)
SuggestionFrame.pack(padx=20, pady=5, fill="both")

TypeSuggestionEntry = CTkComboBox(SuggestionFrame, values=["SienceFiction", "Aventure", "Letterature", "Relegion"], width=200)
TypeSuggestionEntry.place(x=50, y=10)

PriceSuggestionEntry = CTkComboBox(SuggestionFrame, values=["<20$", "20$-30$", ">30$"], width=200)
PriceSuggestionEntry.place(x=500, y=10)

def SuggestionHandling():
    Type = TypeSuggestionEntry.get()
    PriceRange = PriceSuggestionEntry.get()
    Suggestions = []
    for Book in DataBase["Books"]:
        if Book["Type"] == Type:
            if PriceRange == "<20$" and Book["Price"] < 20:
                Suggestions.append(Book["Name"])
            elif PriceRange == "20$-30$" and 20 <= Book["Price"] <= 30:
                Suggestions.append(Book["Name"])
            elif PriceRange == ">30$" and Book["Price"] > 30:
                Suggestions.append(Book["Name"])
    if Suggestions:
        Suggestion_Label.configure(text_color="green", text= Suggestions)
    else:
        Suggestion_Label.configure(text_color="red", text="No suggestions found.")    

SuggestionTrigger = CTkButton(SuggestionFrame, text="Get Suggestions", command=SuggestionHandling)
SuggestionTrigger.place(x=311, y=10)

SuggestionLabel = CTkLabel(SuggestionFrame, text="Suggestions:", font=("Arial", 14))
SuggestionLabel.place(x=50, y=70)

Suggestion_Label = CTkLabel(SuggestionFrame, text="Based on your preferences, we suggest the following books:", font=("Arial", 14))
Suggestion_Label.place(x=150, y=70)

Main.mainloop()