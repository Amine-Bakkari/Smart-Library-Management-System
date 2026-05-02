from customtkinter import *
from PIL import Image

class SearchEngine(CTkFrame):
    def __init__(self, master, SearchEngineFunction, keyBind):
        super().__init__(master)

        self.configure(width=580, height=45, fg_color="transparent", corner_radius=50)
        
        SearchEngineEntry = CTkEntry(self, width=500, height=40, placeholder_text="Search for a student", corner_radius=50, font=CTkFont(size=15))
        SearchEngineEntry.place(x=0, y=0)
        SearchEngineEntry.bind("<KeyRelease>", lambda event: keyBind(event, SearchEngineEntry.get(), master))

        SearchEngineButton = CTkButton(self, width=40, height=40, text="", corner_radius=100, fg_color="transparent", border_color="#ffc711", border_width=2, hover_color="#ff9741", command= lambda: SearchEngineFunction(SearchEngineEntry.get(), master), image=CTkImage(Image.open("External Materials/Search.png"), size=(20, 20)))
        SearchEngineButton.place(x=510, y=0)