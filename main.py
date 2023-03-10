from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

# ----- PASSWORD GENERATOR ----- #


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(6, 8)
    nr_symbols = random.randint(1, 3)
    nr_numbers = random.randint(1, 3)

    password_list = []

    password_letters = [password_list.append(random.choice(letters)) for _ in range(nr_letters)]
    password_symbols = [password_list.append(random.choice(symbols)) for _ in range(nr_symbols)]
    password_numbers = [password_list.append(random.choice(numbers)) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)

    entry_password.delete(0, "end")
    entry_password.insert(0, password)

    pyperclip.copy(password)

# ----- SEARCH ----- #


def search_in_data():
    website = entry_website.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        open("data.json", "w")
        messagebox.showerror(title="New file created", message="This record is not in the database")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=entry_website.get(), message=f"email: {email}\npassword: {password}")
        else:
            messagebox.showerror(title="Name error", message="This record is not in the database")
        entry_website.delete(0, "end")
        entry_website.focus()


# ----- SAVE PASSWORD ----- #


def save_password():
    website = entry_website.get()
    email = entry_email.get()
    password = entry_password.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if entry_website.get() == "" or entry_password.get() == "" or entry_email.get() == "":
        messagebox.showerror(title="Missing data", message="Webpage or password is missing")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            entry_website.delete(0, "end")
            entry_password.delete(0, "end")
            entry_website.focus()


# ----- UI SETUP ----- #


window = Tk()
window.title("Password manager")
window.config(padx=40, pady=40, bg="#e8e8e8")

canvas = Canvas(width=200, height=200, bg="#e8e8e8", highlightthickness=0)
photo_image = PhotoImage(file="rsz_trezor.png")
canvas.create_image(100, 100, image=photo_image)
canvas.grid(row=0, column=1)

# Labels
label_website = Label(text="Website:", font=("Courier", 11, "bold"), bg="#e8e8e8", highlightthickness=0)
label_website.grid(row=1, column=0, pady=(10, 0), sticky=E)
label_website.config(justify=RIGHT, anchor="e")
label_email = Label(text="Email:", font=("Courier", 11, "bold"), bg="#e8e8e8", highlightthickness=0)
label_email.grid(row=2, column=0, pady=(10, 0), sticky=E)
config = label_email.config(justify=RIGHT, anchor="e")
label_password = Label(text="Password:", font=("Courier", 11, "bold"), bg="#e8e8e8", highlightthickness=0)
label_password.grid(row=3, column=0, pady=(10, 0))
label_password.config(justify=RIGHT, anchor="e")

# Entries
entry_website = Entry()
entry_website.grid(row=1, column=1, sticky="we", pady=(5, 0))
entry_website.focus()

entry_email = Entry()
entry_email.grid(row=2, column=1, sticky="we", pady=(5, 0), columnspan=2)
entry_email.insert(0, "vondrej.kukla@gmail.com")

entry_password = Entry()
entry_password.grid(row=3, column=1, sticky="we", pady=(5, 0))

# Buttons
button_generate_password = Button(text="Generate password", command=generate_password)
button_generate_password.grid(row=3, column=2, padx=5, pady=(5, 0))

button_add = Button(text="Add", command=save_password)
button_add.grid(row=4, column=1, padx=5, pady=(10, 0), sticky="we")

button_search = Button(text="Search", command=search_in_data)
button_search.grid(row=1, column=2, padx=5, pady=(5, 0), sticky="we")

window.mainloop()
