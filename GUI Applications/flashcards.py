# Importing relevant modules
from tkinter import *
import random

# Declaring constants and global variables
WORD_FILE = "german_to_english.csv"
LIGHT = "#edf2f4"
MED = "#8d99ae"
DARK = "#2b2d42"
all_words = []

# Parsing information from the CSV file and using it to construct a list
with open(WORD_FILE, 'r') as in_file:

    lines = in_file.readlines()

    for line in lines:

        line = line.strip().split(',')
        all_words.append(line)

    random.shuffle(all_words)

# Keeping track of the current, and previous, word pairs
curr_word = all_words[0]
prev_word = []


# Flips the flashcard onto its rear, displaying the current word's english translation
def flip_card():

    global curr_word
    global prev_word
    back_card_img = PhotoImage(file="back_card.png")
    canvas.itemconfig(card_container, image=back_card_img)
    canvas.itemconfig(language_label, text="English", fill=DARK)
    canvas.itemconfig(word_label, text=curr_word[1], fill=DARK)
    canvas.imgref = back_card_img
    prev_word = curr_word
    all_words.remove(prev_word)
    curr_word = all_words[0]


# Starts the 3s (3000ms) timer, flips the card when the time is up
def start_timer():

    front_card_img = PhotoImage(file="front_card.png")
    canvas.itemconfig(card_container, image=front_card_img)
    canvas.itemconfig(language_label, text="German", fill=LIGHT)
    canvas.itemconfig(word_label, text=curr_word[0], fill=LIGHT)
    canvas.imgref = front_card_img
    window.after(3000, flip_card)


# Removes the current card from the deck, and proceeds on to the next one
def correct():

    start_timer()


# Moves the current card to the back of the deck, and proceeds on to the next one
# Note: deck will not be empty until the user has guessed all of the words correctly
def incorrect():

    start_timer()
    all_words.append(prev_word)


# Setting up the UI for the program using the tkinter module/library
window = Tk()
window.title("Flashy")
window.config(bg=MED)
window.geometry("900x575+200+100")

canvas = Canvas(width=720, height=400, highlightthickness=0, bg=MED)
start_card_img = PhotoImage(file="front_card.png")
card_container = canvas.create_image(380, 190, image=start_card_img)
language_label = canvas.create_text(350, 90, text="Language", font=("Ariel", 40, "italic"), fill=LIGHT)
word_label = canvas.create_text(350, 200, text="Word", font=("Ariel", 60, "bold"), fill=LIGHT)
canvas.grid(column=0, row=0, columnspan=2, padx=(90, 0), pady=(60, 0))

check_image = PhotoImage(file="check_mark_ps.png")
known_button = Button(image=check_image, width=62, height=62, bd=0, borderwidth=0, highlightthickness=0, command=correct)
known_button.grid(column=1, row=1, padx=(0, 90), pady=(5,0))

cross_image = PhotoImage(file="cross_icon_ps.png")
unknown_button = Button(image=cross_image, width=50, height=50, bd=0, borderwidth=0, highlightthickness=0, command=incorrect)
unknown_button.grid(column=0, row=1, padx=(170, 0), pady=(5,0))

window.mainloop()
