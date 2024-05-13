from time import time
from tkinter import *
import tkinter
import csv
from tkinter import messagebox

phonelist = []

def login():
    uname = username.get()
    pwd = password.get()

    if uname == '' or pwd == '':
        message.set("Fill in the empty fields!")
    else:
        if uname == "user@gmail.com" and pwd == "123":
            login_screen.destroy()
        else:
            message.set("Wrong username or password! Please try again.")

def Loginform():
    global login_screen
    login_screen = Tk()

    icon = PhotoImage(file='favicon.png')
    login_screen.iconphoto(False, icon)

    login_screen.title("Login Form")
    login_screen.geometry("300x250")

    global message
    global username
    global password
    username = StringVar()
    password = StringVar()
    message = StringVar()
    Label(login_screen, text="Please enter details below!", bg="#f54865", fg="white").pack()
    Label(login_screen, text="Username * ").place(x=20, y=40)
    Entry(login_screen, textvariable=username).place(x=90, y=42)
    Label(login_screen, text="Password * ").place(x=20, y=80)
    Entry(login_screen, textvariable=password, show="*").place(x=90, y=82)
    Button(login_screen, text="Login", width=10, height=1,
           bg="#f54865", command=login).place(x=105, y=130)
    Label(login_screen, textvariable=message, fg="red").place(x=20, y=160)

    login_screen.mainloop()

Loginform()



def ReadCSVFile():
    global header
    with open('DataPengunjung.csv') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter=',')
        header = next(csv_reader)
        for row in csv_reader:
            phonelist.append(row)
    set_select()
    print(phonelist)


def WriteCSVFile(phonelist):
    with open('DataPengunjung.csv', 'w', newline='') as csv_file:
        writeobj = csv.writer(csv_file, delimiter=',')
        writeobj.writerow(header)
        for row in phonelist:
            writeobj.writerow(row)


def SelectedData():
    if len(select.curselection()) == 0:
        messagebox.showerror("Error", "Please select the data you want to view")
    else:
        return int(select.curselection()[0])


def AddDetail():
    if E_name.get() != "" and E_last_name.get() != "" and E_contact.get() != "":
        phonelist.append([E_name.get()+' '+E_last_name.get(), E_contact.get()])
        WriteCSVFile(phonelist)
        set_select()
        DataReset()
        messagebox.showinfo("Confirmation", "Contact added successfully!")

    else:
        messagebox.showerror("Error", "Please enter complete information")


def UpdateDetail():
    if E_name.get() and E_last_name.get() and E_co3ntact.get():
        phonelist[SelectedData()] = [E_name.get()+' '+E_last_name.get(), E_contact.get()]
        WriteCSVFile(phonelist)
        messagebox.showinfo("Confirmation", "Contact updated successfully!")
        DataReset()
        set_select()

    elif not(E_name.get()) and not(E_last_name.get()) and not(E_contact.get()) and not(len(select.curselection()) == 0):
        messagebox.showerror("Error", "Please fill in the information")

    else:
        if len(select.curselection()) == 0:
            messagebox.showerror("Error", "Please select data and press Load button")
        else:
            message1 = """To display all data, \n 
						  please select data and press Load\n.
						  """
            messagebox.showerror("Error", message1)


def DataReset():
    E_name_var.set('')
    E_last_name_var.set('')
    E_contact_var.set('')


def DeleteData():
    if len(select.curselection()) != 0:
        result = messagebox.askyesno(
            'Confirmation', 'Do you want to delete the selected contact?')
        if result == True:
            del phonelist[SelectedData()]
            WriteCSVFile(phonelist)
            set_select()
    else:
        messagebox.showerror("Error", 'Please select a contact')


def LoadData():
    name, phone = phonelist[SelectedData()]
    E_name_var.set(name.split(' ')[0])
    E_last_name_var.set(name.split(' ')[1])
    E_contact_var.set(phone)


def set_select():
    phonelist.sort(key=lambda record: record[1])
    select.delete(0, END)
    i = 0
    for name, phone in phonelist:
        i += 1
        select.insert(END, f"{i}  |    {name}   |   {phone}")


window = Tk()

Frame1 = LabelFrame(window, text="Enter Contact Details")
Frame1.grid(padx=15, pady=15)


Inside_Frame1 = Frame(Frame1)
Inside_Frame1.grid(row=0, column=0, padx=15, pady=15)

l_name = Label(Inside_Frame1, text="Name")
l_name.grid(row=0, column=0, padx=5, pady=5)
E_name_var = StringVar()
E_name = Entry(Inside_Frame1, width=30, textvariable=E_name_var)
E_name.grid(row=0, column=1, padx=5, pady=5)

l_last_name = Label(Inside_Frame1, text="Last Name")
l_last_name.grid(row=1, column=0, padx=5, pady=5)
E_last_name_var = StringVar()
E_last_name = Entry(Inside_Frame1, width=30, textvariable=E_last_name_var)
E_last_name.grid(row=1, column=1, padx=5, pady=5)

l_contact = Label(Inside_Frame1, text="Contact")
l_contact.grid(row=2, column=0, padx=5, pady=5)
E_contact_var = StringVar()
E_contact = Entry(Inside_Frame1, width=30, textvariable=E_contact_var)
E_contact.grid(row=2, column=1, padx=5, pady=5)

Frame2 = Frame(window)
Frame2.grid(row=0, column=1, padx=15, pady=15, sticky=E)

Add_button = Button(Frame2, text="Add Detail", width=15,
                    bg="#f54865", fg="#FFFFFF", command=AddDetail)
Add_button.grid(row=0, column=0, padx=8, pady=8)

Update_button = Button(Frame2, text="Update Detail", width=15,
                       bg="#f54865", fg="#FFFFFF", command=UpdateDetail)
Update_button.grid(row=1, column=0, padx=8, pady=8)

Reset_button = Button(Frame2, text="Reset", width=15,
                      bg="#f54865", fg="#FFFFFF", command=DataReset)
Reset_button.grid(row=2, column=0, padx=8, pady=8)

DisplayFrame = Frame(window)
DisplayFrame.grid(row=1, column=0, padx=15, pady=15)

scroll = Scrollbar(DisplayFrame, orient=VERTICAL)
select = Listbox(DisplayFrame, yscrollcommand=scroll.set, font=("Arial Bold", 10),
                 bg="#282923", fg="#E7C855", width=40, height=10, borderwidth=3, relief="groove")
scroll.config(command=select.yview)
select.grid(row=0, column=0, sticky=W)
scroll.grid(row=0, column=1, sticky=N+S)

ActionFrame = Frame(window)
ActionFrame.grid(row=1, column=1, padx=15, pady=15, sticky=E)

Delete_button = Button(ActionFrame, text="Delete", width=15,
                       bg="#D20000", fg="#FFFFFF", command=DeleteData)
Delete_button.grid(row=0, column=0, padx=5, pady=5, sticky=S)

Loadbutton = Button(ActionFrame, text="Load", width=15,
                    bg="#00FF00", fg="#FFFFFF", command=LoadData)
Loadbutton.grid(row=1, column=0, padx=5, pady=5)

ReadCSVFile()

window.mainloop()