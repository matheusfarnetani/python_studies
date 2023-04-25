from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

DATA_DIRECTORY = "python_password_manager/passwords.json"
LOGO_DIRECTORY = "python_password_manager/logo.png"

def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
               'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
               'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for i in range(randint(8, 10))]
    password_symbols = [choice(symbols) for i in range(randint(2, 4))]
    password_numbers = [choice(numbers) for i in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)

    entry_password.delete(0, END)
    entry_password.insert(END, password)

    pyperclip.copy(password)


def find_password():
    website = entry_website.get()

    try:
        with open(DATA_DIRECTORY, mode = "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="No Data File Found")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {password}\n\nThe password was copied to your clipboard")
            pyperclip.copy(password)
        elif website == "":
            messagebox.showerror(title="Error", message="Please insert a website")
        else:
            messagebox.showerror(title="Error", message=f"There is no data for {website}")


def save():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website:{
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showerror(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open(DATA_DIRECTORY, mode = "r") as file:
                # Reading Old data
                data = json.load(file)
        except FileNotFoundError:
            with open(DATA_DIRECTORY, mode = "a") as file:
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open(DATA_DIRECTORY, mode = "w") as file:
                # Saving updated data
                json.dump(data, file, indent=4)
        finally:
            entry_website.delete(0, END)
            entry_password.delete(0, END)


# User Interface
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
password_img = PhotoImage(file=LOGO_DIRECTORY)
canvas.create_image(100, 100, image=password_img)
canvas.grid(column=1,row=0)

# Labels
lb_website = Label(text="Website:")
lb_website.grid(column=0, row=1)
lb_email = Label(text="Email/Username:")
lb_email.grid(column=0, row=2)
lb_password = Label(text="Password:")
lb_password.grid(column=0, row=3)

# Entrys
entry_website = Entry()
entry_website.grid(column=1, row=1, sticky="EW")
entry_website.focus() # makes the cursor focus in that entry 
entry_email = Entry()
entry_email.grid(column=1, row=2, columnspan=2, sticky="EW")
entry_email.insert(END, "example@gmail.com")
entry_password = Entry()
entry_password.grid(column=1, row=3, sticky="EW")

# Buttons
button_generate = Button(text="Generate Password", command=password_generator)
button_generate.grid(column=2, row=3, sticky="EW")
button_add = Button(text="Add", width=35, command=save)
button_add.grid(column=1, row=4, columnspan=2, sticky="EW")
button_search = Button(text="Search", command=find_password)
button_search.grid(column=2, row=1, sticky="EW")

window.mainloop()
