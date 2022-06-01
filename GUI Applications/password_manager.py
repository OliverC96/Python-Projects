# Importing relevant modules
from tkinter import *
import string
import random
import json

# Declaring constants
LIGHT_GREY = '#d3d3d3'
DARK_GREY = '#161a1d'
JSON_FILE = "data.json"
FONT = ("Lato", 16, "bold")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
# Generating a (pseudo)random password
def generate_password():

    # Separating numbers, letters, and special symbols
    lower_letters = list(string.ascii_lowercase)
    upper_letters = list(string.ascii_uppercase)
    numbers = [str(i) for i in range(10)]
    special_symbols = [chr(i) for i in range(33,39)]
    strong_password = []

    # Shuffling each subclass of characters
    random.shuffle(lower_letters)
    random.shuffle(upper_letters)
    random.shuffle(numbers)
    random.shuffle(special_symbols)

    # Adding three upper- and three lower-case letters to the password
    for i in range(3):

        strong_password.append(lower_letters[i])
        strong_password.append(upper_letters[i])

    # Adding two numbers and two special symbols to the password
    for i in range(2):

        strong_password.append(numbers[i])
        strong_password.append(special_symbols[i])

    # Shuffling the password once more, then inserting it into the entry widget
    random.shuffle(strong_password)
    password_entry.delete(0, END)
    password_entry.insert(0, ''.join(strong_password))

    # Adding the newly generated password to the user's clipboard
    window.clipboard_clear()
    window.clipboard_append(''.join(strong_password))
    window.update()


# ---------------------------- SAVE PASSWORD ----------------------------- #
# Saving the account info (website, username/email and password) to a JSON file
def save_password():

    website = website_entry.get()
    user_name = user_name_entry.get()
    password = password_entry.get()

    # Will proceed with the saving operation only if all three entry fields are not empty
    if website not in ['', ' '] and user_name not in [' ', ''] and password not in [' ', '']:

        # Creating a nested dictionary compatible with the JSON structure
        new_data = {
            website: {
                "email": user_name,
                "password": password
            }
        }

        # Determining whether or not the JSON file currently exists (or if it needs to be created)
        try:

            with open(JSON_FILE, "r") as in_file:

                # Retrieving the current data in the JSON file
                data = json.load(in_file)
                data.update(new_data)

        except (IOError, FileNotFoundError):

            data = new_data

        finally:

            with open(JSON_FILE, "w") as out_file:

                # Writing the nested data dictionary to the JSON file; resetting the three entry fields
                json.dump(data, out_file, indent=4)
                website_entry.delete(0, END)
                user_name_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- SEARCH DATA ------------------------------- #
# Searching the JSON database for a password associated with the specified website
def search_data():

    # Creating a top level widget (popup window)
    search_result = Toplevel()
    search_result.config(padx=20, pady=20)

    # Creating the password logo
    pass_logo = PhotoImage(file="lock.png")
    pass_img = Label(search_result, image=pass_logo)
    pass_img.grid(row=0, column=0, rowspan=2)
    pass_img.image = pass_logo

    # Creating the text widget containing the results of the password search
    account_info = Text(search_result, height=3, width=25, font=("Lato", 13, "bold"))
    account_info.grid(row=0, column=1, rowspan=3, columnspan=2)

    # Creating a button to exit the top level window (return to the root/main/base window)
    ok = Button(search_result, text="Ok", padx=25, command=search_result.destroy)
    ok.grid(row=2, column=4)

    with open(JSON_FILE, 'r') as data_file:

        # Retrieving the information contained within the JSON file in the form of a nested dictionary
        data_dict = json.load(data_file)

        # Iterating through the contents of the data_dict
        for key, value in data_dict.items():

            # Password is found, text widget is updated accordingly
            if key.lower() == website_entry.get().lower():

                account_email = data_dict[key]["email"]
                account_password = data_dict[key]["password"]
                info = "Email: {}\nPassword: {}".format(account_email, account_password)
                account_info.insert(END, info)
                break

        # Executes if the password is not found in the JSON file
        else:

            info = "Account not found\nEmail: N/A\nPassword: N/A"
            account_info.insert(END, info)
            account_info.grid_configure(rowspan=2)


# ---------------------------- UI SETUP ------------------------------- #
# Creating and formatting the root window object
window = Tk()
window.title("Password Manager")
window.config(padx=40, pady=40, bg=LIGHT_GREY)

# Creating and formatting the canvas object (which contains the logo)
canvas = Canvas(height=200, width=200, bg=LIGHT_GREY, highlightthickness=0)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=0, row=0, columnspan=3)

# Creating and formatting additional widgets (entry fields, labels, and buttons)
website_label = Label(text="Website:", bg=LIGHT_GREY, fg=DARK_GREY, font=FONT)
website_label.grid(column=0, row=1, sticky="w")
website_entry = Entry(width=20, borderwidth=0)
website_entry.grid(row=1, column=1)

search_button = Button(text="Search", width=15, command=search_data)
search_button.grid(column=2, row=1)

user_name_label = Label(text="Email/Username:", bg=LIGHT_GREY, fg=DARK_GREY, font=FONT)
user_name_label.grid(column=0, row=2)
user_name_entry = Entry(width=36, borderwidth=0)
user_name_entry.grid(row=2, column=1, columnspan=2)

password_label = Label(text="Password:", bg=LIGHT_GREY, fg=DARK_GREY, font=FONT)
password_label.grid(column=0, row=3, sticky="w")
password_entry = Entry(width=20, borderwidth=0)
password_entry.grid(row=3, column=1)

generate_button = Button(text="Generate Password", width=15, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text="Add Account Info", width=37, command=save_password)
add_button.grid(row=4, column=1, columnspan=2)

window.mainloop()
