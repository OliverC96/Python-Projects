# Importing relevant modules and declaring global variables
from tkinter import *
import math
reps = 0
timer = None

# Declaring and initializing constants
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
CHECK_MARK = "✔"


# ---------------------------- TIMER RESET ------------------------------- #
# Resetting widgets and variables to their original state
def reset_timer():

    window.after_cancel(timer)
    canvas.itemconfig(timer_text, text="00:00")
    title_label.config(text="Timer")
    check_mark_label.config(text="")
    global reps
    reps = 0


# ---------------------------- TIMER MECHANISM ------------------------------- #
# Initiates the timer mechanism
def start_timer():

    # Increments the number of repetitions
    global reps
    reps += 1

    # Transforms widgets into the "long break" mode
    if reps % 8 == 0:

        count_down(LONG_BREAK_MIN * 60)
        title_label.config(text="Rest", fg=RED)

    # Transforms widgets into the "short break" mode
    elif reps % 2 == 0:

        count_down(SHORT_BREAK_MIN * 60)
        title_label.config(text="Rest", fg=PINK)

    # Transforms widgets into the "work/study" mode
    else:

        count_down(WORK_MIN * 60)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
# Initiates the countdown mechanism
def count_down(count):

    # Updates the timer with the current number of minutes and seconds
    minutes = count // 60
    seconds = count % 60
    timer_string = "{:02d}:{:02d}".format(minutes, seconds)
    canvas.itemconfig(timer_text, text=timer_string)

    # Continues counting if there is still time remaining
    if count > 0:

        global timer
        timer = window.after(2, count_down, count-1)

    # Progresses onto the next stage in the pomodoro cycle
    else:

        start_timer()
        marks = ''
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            marks += CHECK_MARK
        check_mark_label.config(text=marks)

# ---------------------------- UI SETUP ------------------------------- #
# Creating and formatting the root window object
window = Tk()
window.title("Pomodoro Technique")
window.config(padx=100, pady=50, bg=YELLOW)

# Creating and formatting the canvas object (composed of the image containing the timer inside of it)
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(100, 112, image=tomato_img)
timer_text = canvas.create_text(100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold"))
canvas.grid(column=1, row=1)

# Creating and formatting additional widgets (title, start and reset buttons, and the checkmark symbol)
title_label = Label(text="Timer", bg=YELLOW, fg=GREEN, font=(FONT_NAME, 50))
title_label.grid(column=1, row=0)
start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)
reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)
check_mark_label = Label(text="", bg=YELLOW, fg=GREEN)
check_mark_label.grid(column=1, row=3)

window.mainloop()
