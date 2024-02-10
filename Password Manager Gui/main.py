# ---------------------------- PASSWORD GENERATOR ------------------------------- #
from tkinter import *
from tkinter import messagebox
import random
import pyperclip


def password_generator():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [random.choice(letters) for _ in range(random.randint(8, 10))]
    password_symbols = [random.choice(symbols) for _ in range(random.randint(2, 4))]
    password_numbers = [random.choice(numbers) for _ in range(random.randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50)


def save():
    username = username_entry.get()
    website = website_entry.get()
    password = password_entry.get()

    if len(username) > 0 and len(website) and len(password):
        is_ok = messagebox.askokcancel(title=website, message=f"These are the details entered:\nEmail\\username: "
                                                              f"{username}\npassword: {password}\nIs it okay to save?")
        if is_ok:
            with open("data.txt", "a") as file:
                file.write(f"\nUsername/Email:{username} | Website:{website} | Password:{password}\n")

    else:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")

    website_entry.delete(0, END)
    password_var.set("")


canvas = Canvas(width=200, height=200, highlightthickness=0)
lock_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock_img)
canvas.grid(column=1, row=0)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

username_label = Label(text="Email/Username:")
username_label.grid(column=0, row=2)

password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

website_entry = Entry(width=35)
website_entry.grid(row=1, column=1, columnspan=2)
website_entry.focus()

username_entry = Entry(width=35)
username_entry.grid(row=2, column=1, columnspan=2)
username_entry.insert(0, "fabiuslihandaachevi@gmail.com")

password_var = StringVar()
password_entry = Entry(width=21, textvariable=password_var, show="*")
password_entry.grid(row=3, column=1)

generate_password_button = Button(text="Generate Password", command=password_generator)
generate_password_button.grid(row=3, column=2)

add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)

window.mainloop()

