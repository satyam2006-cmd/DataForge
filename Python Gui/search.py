from tkinter import *
import wikipedia

# Robust search function 
def get_data():
    entry_value = entry.get().strip()
    answer.delete(1.0, END)

    if not entry_value:
        answer.insert(INSERT, "⚠ Please enter a search term.")
        return

    try:
        # Try fetching a short summary
        answer_value = wikipedia.summary(entry_value, sentences=4)
        answer.insert(INSERT, answer_value)

    except wikipedia.DisambiguationError as e:
        # Handle ambiguous queries by suggesting options
        answer.insert(INSERT, "⚠ This query is ambiguous. Did you mean:\n\n")
        for option in e.options[:10]:  # show top 10 suggestions
            answer.insert(INSERT, f"• {option}\n")

    except wikipedia.PageError:
        answer.insert(INSERT, "⚠ Page not found. Try another search term.")

    except Exception as e:
        answer.insert(INSERT, f"⚠ ERROR: {str(e)}")


# GUI 
win = Tk()
win.title("Wikipedia Search")
win.geometry("650x550")
win.config(bg="#f4f6f7")

# Heading
title_label = Label(
    win,
    text="🔎 Wikipedia Search",
    font=("Arial", 18, "bold"),
    bg="#f4f6f7",
    fg="#2c3e50"
)
title_label.pack(pady=15)

# Top Frame
topframe = Frame(win, bg="#f4f6f7")
entry = Entry(topframe, font=("Arial", 14), width=40, bd=2, relief=GROOVE)
entry.pack(side=LEFT, padx=10, pady=10)

button = Button(
    topframe,
    text="Search",
    command=get_data,
    font=("Arial", 12, "bold"),
    bg="#2ecc71",
    fg="white",
    activebackground="#27ae60",
    padx=10,
    pady=5,
    relief=RAISED
)
button.pack(side=LEFT, padx=5)
topframe.pack()

# Bottom Frame (Text + Scroll)
bottomframe = Frame(win, bg="#f4f6f7")

scroll = Scrollbar(bottomframe)
scroll.pack(side=RIGHT, fill=Y)

answer = Text(
    bottomframe,
    width=70,
    height=25,
    font=("Arial", 12),
    wrap=WORD,
    yscrollcommand=scroll.set,
    bd=2,
    relief=GROOVE
)
scroll.config(command=answer.yview)
answer.pack(side=LEFT, padx=10, pady=10)

bottomframe.pack(pady=10)

win.mainloop()
