from tkinter import *
import pandas
from random import choice

BACKGROUND_COLOR = "#B1DDC6"

current_card = {}
to_learn = {}

try:
    data = pandas.read_csv('./data/words_to_learn.csv')
except FileNotFoundError:
    original_data = pandas.read_csv('./data/database.csv')
    to_learn = original_data.to_dict(orient='records')
else:
    to_learn = data.to_dict(orient='records')

def next_card():
    global current_card, flip_timer
    windows.after_cancel(flip_timer)
    current_card = choice(to_learn)
    
    canvas.itemconfig(card_title, text='Italian', fill='black')
    canvas.itemconfig(card_word, text=current_card['Italian'], fill='black')
    canvas.itemconfig(canvas_image, image=card_front_img)
    flip_timer = windows.after(3000, func=flip_card)

def flip_card():
    canvas.itemconfig(canvas_image, image=card_back_img)
    canvas.itemconfig(card_title, text='English', fill='white')
    canvas.itemconfig(card_word, text=current_card['English'], fill='white')

def is_known():
    to_learn.remove(current_card)
    #print(len(to_learn))

    data = pandas.DataFrame(to_learn)
    data.to_csv('./data/words_to_learn.csv', index=False)

    save_known_word()
    next_card()

def save_known_word():
    global current_card

    words_learned = {}

    try:
        data2 = pandas.read_csv('./data/words_learned.csv')
        
    except FileNotFoundError:
        with open('./data/words_learned.csv', 'w') as data:
            data.write('French,English')
    else:
        words_learned = data2.to_dict(orient='records')

        words_learned.append(current_card)
        #print(f'words learned {len(words_learned)}')

        data2 = pandas.DataFrame(words_learned)
        data2.to_csv('./data/words_learned.csv', index=False)


# UI ==================================================================
windows = Tk()
windows.title("Italian Words")
windows.config(pady=50, padx=50, bg=BACKGROUND_COLOR)

flip_timer = windows.after(3000, func=flip_card)

canvas = Canvas(height=526, width=800)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

card_front_img = PhotoImage(file="./images/card_front.png")

card_back_img = PhotoImage(file="./images/card_back.png")

canvas_image = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, font=('Arial', 40, 'italic'))
card_word = canvas.create_text(
    400, 263, font=('Arial', 60, 'bold'))
canvas.grid(row=0, column=0, columnspan=2)

cross_image = PhotoImage(file="./images/wrong.png")
unknown_button = Button(image=cross_image, command=next_card)
unknown_button.config(highlightthickness=0, bg=BACKGROUND_COLOR)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="./images/right.png")
known_button = Button(image=check_image, command=is_known)
known_button.config(highlightthickness=0, bg=BACKGROUND_COLOR)
known_button.grid(row=1, column=1)

next_card()

windows.mainloop()