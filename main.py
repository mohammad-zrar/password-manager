from tkinter import *  # It imports all the classes
from tkinter import messagebox  # messagebox is not a class that's why you have to import it apart
import random
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Password Generator Project
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]

    random.shuffle(password_list)
    password = "".join(password_list)   # Convert list to string

    if len(password_entry.get()) == 0:
        password_entry.insert(0, password)
    else:
        password_entry.delete(0, END)
        password_entry.insert(0, password)
        pyperclip.copy(password)


# ----------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = web_entry.get().strip()
    email = email_entry.get().strip()
    password = password_entry.get().strip()

    new_data = {website: {"email": email, "password": password}}

    if website == "" or email == "" or password == "":
        messagebox.showinfo(title="Oops", message="Please make sure you haven't left any fields empty!")
    else:
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered: \nEmail: {email}\n"
                                                              f"Password: {password}\n Is it ok to save?")
        if is_ok:
            try:
                with open("data.json", "r") as data_file:
                    # Reading old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                # Updating old data with new data
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # Saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                web_entry.delete(0, END)
                password_entry.delete(0, END)

# -------------------------- Find password ---------------------------- #


def find_password():
    website = web_entry.get()
    if len(website.strip()) != 0:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
            try:
                web_detail = data[website]
                messagebox.showinfo(title=website, message=f"Email: {web_detail['email']} \n"
                                                           f"Password: {web_detail['password']}")
            except KeyError:
                messagebox.showinfo(title=website, message="No detail for the website exists.")
        except FileNotFoundError:
            messagebox.showinfo(title="Oops", message="No Data File Found.")
    else:
        messagebox.showinfo(title="Website", message="Write name of the website.")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.config(padx=50, pady=50)
window.title("Password manager")

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Label

website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

acc_label = Label(text="Email/Username: ")
acc_label.grid(column=0, row=2)

password_label = Label(text="Password: ")
password_label.grid(column=0, row=3)

# Entry

web_entry = Entry(width=32)
web_entry.grid(column=1, row=1, pady=4)
web_entry.focus()

email_entry = Entry(width=32)
email_entry.grid(column=1, row=2, pady=4)
email_entry.insert(0, "primaryacc@gmail.com")
# email_entry.insert(5, "BEFORE")   # Insert at index 5

password_entry = Entry(width=32)
password_entry.grid(column=1, row=3, pady=4)

# Button

gen_pass_button = Button(text="Generate Password", width=15, command=generate_password)
gen_pass_button.grid(column=2, row=3, pady=4)

add_button = Button(text="Add", width=15, padx=5, command=save)
add_button.grid(column=1, row=4, pady=4)

search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
