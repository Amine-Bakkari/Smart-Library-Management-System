from customtkinter import *
import json as js

Main = CTk()
Main.geometry("800x500")
Main.title("School Library Management System")

TitleLabel = CTkLabel(Main, text="Welcome to the School Library Management System", font=("Arial", 20))
TitleLabel.pack(pady=10)



LentingFrame = CTkFrame(Main, corner_radius=10, height=250, width=370)
LentingFrame.pack(padx=20, anchor="w")

LentingTitleLabel = CTkLabel(LentingFrame, text="Borrowing", font=("Arial", 15))
LentingTitleLabel.place(x=150, y=3)

BookToLentNameEntry = CTkEntry(LentingFrame, width=215, placeholder_text="Enter book name or serial number")
BookToLentNameEntry.place(x=80, y=50)

LStudentNameEntry = CTkEntry(LentingFrame, width=215, placeholder_text="Enter student name or ID")
LStudentNameEntry.place(x=80, y=90)

DateOfLentLabel = CTkLabel(LentingFrame, text="Date of Borrow:", font=("Arial", 13))
DateOfLentLabel.place(x=60, y=135)
DateOfLentEntry = CTkEntry(LentingFrame, width=100, placeholder_text="DD-MM-YYYY")
DateOfLentEntry.place(x=50, y=160)

DateOfRetrieveLabel = CTkLabel(LentingFrame, text="Date of Retrieve:", font=("Arial", 13))
DateOfRetrieveLabel.place(x=210, y=135)
DateOfRetrieveEntry = CTkEntry(LentingFrame, width=100, placeholder_text="DD-MM-YYYY")
DateOfRetrieveEntry.place(x=210, y=160)

def LentingHandling():
    with open(r"C:\Users\Abdelaziz\Programation\PythonProjects\Smart Library Management System\Library-DataBase.json", "r") as DB:
        DataBase = js.load(DB)
    BookName = BookToLentNameEntry.get()
    StudentName = LStudentNameEntry.get()
    DateLent = DateOfLentEntry.get()
    DateRetrieve = DateOfRetrieveEntry.get()
    if BookName and StudentName and DateLent and DateRetrieve:
        for Book in DataBase["Books"]:
            if Book["Name"] == BookName or Book["SerialNumber"] == BookName:
                if Book["Available"] > 0:
                    ResultLabel.configure(text="Borrow Successfully", text_color="green")
                    DataBase["Books"][DataBase["Books"].index(Book)]["Available"] -= 1
                    DataBase["Books"][DataBase["Books"].index(Book)]["Lented"].append({"LentedTo":StudentName, "LentedDate":DateLent, "RetrievingDate":DateRetrieve})
                    with open(r"C:\Users\Abdelaziz\Programation\PythonProjects\Smart Library Management System\Library-DataBase.json", "w+") as DB:
                        js.dump(DataBase, DB, indent=4)
                    return
                else:
                    ResultLabel.configure(text="Book Not Available", text_color="red")
                    return
    else:
        ResultLabel.configure(text="Error", text_color="red")

LentButton = CTkButton(LentingFrame, text="Lent Book", command=LentingHandling)
LentButton.place(x=110, y=210)

ResultLabel = CTkLabel(LentingFrame, text="", font=("Arial", 14))
ResultLabel.place(x=260, y=210)

#----------------------------------------------------------------------------

RetrievingFrame = CTkFrame(Main, corner_radius=10, height=250, width=370)
RetrievingFrame.place(x=410, y=48)

RetrievingTitleLabel = CTkLabel(RetrievingFrame, text="Retrieving", font=("Arial", 15))
RetrievingTitleLabel.place(x=150, y=5)

BookToRetrieveNameEntry = CTkEntry(RetrievingFrame, width=210, placeholder_text="Enter book name or serial number")
BookToRetrieveNameEntry.place(x=80, y=50)

RStudentNameEntry = CTkEntry(RetrievingFrame, width=210, placeholder_text="Enter student name or ID")
RStudentNameEntry.place(x=80, y=90)

RetrievedDateLabel = CTkLabel(RetrievingFrame, text="Retrieve Date:")
RetrievedDateLabel.place(x=140, y=130)
RetrievedDateEntry = CTkEntry(RetrievingFrame, width=100, placeholder_text="DD-MM-YYYY")
RetrievedDateEntry.place(x=132, y=160)

def RetrievingHandling():
    with open(r"C:\Users\Abdelaziz\Programation\PythonProjects\Smart Library Management System\Library-DataBase.json", "r") as DB:
        DataBase = js.load(DB)
    BookName = BookToRetrieveNameEntry.get()
    StudentName = RStudentNameEntry.get()
    RetrievingDate = RetrievedDateEntry.get()

    for Book in DataBase["Books"]:
        if Book["Name"] == BookName or Book["SerialNumber"] == BookName:
            for LentedRecord in Book["Lented"]:
                if LentedRecord["LentedTo"] == StudentName:
                    DataBase["Books"][DataBase["Books"].index(Book)]["Available"] += 1
                    DataBase["Books"][DataBase["Books"].index(Book)]["Lented"].remove(LentedRecord)
                    with open(r"C:\Users\Abdelaziz\Programation\PythonProjects\Smart Library Management System\Library-DataBase.json", "w+") as DB:
                        js.dump(DataBase, DB, indent=4)
                    RResultLabel.configure(text="Retrieved Successfully", text_color="green")
                    return


RetriveButton = CTkButton(RetrievingFrame, text="Retrieved", command=RetrievingHandling)
RetriveButton.place(x=110, y=210)

RResultLabel = CTkLabel(RetrievingFrame, text="", font=("Arial", 14))
RResultLabel.place(x=260, y=210)

NotificationFrame = CTkFrame(Main, corner_radius=10, height=200)
NotificationFrame.pack(padx=20, pady=15, fill="both")

Main.mainloop()