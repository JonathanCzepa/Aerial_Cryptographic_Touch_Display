import tkinter as tk
import random
import numpy as np

shuffleKeys = False

def press(value):
    current = entry_var.get()
    entry_var.set(current + value)

def clear():
    entry_var.set("")

def backspace():
    current = entry_var.get()
    entry_var.set(current[:-1])

def enter():
    value = entry_var.get()
    print("Entered:", value)
    clear()
    if value == "123":
        entry_var.set("Accepted")
    else:
        entry_var.set("KYS")

def randKeypad(keypad):
    if shuffleKeys:
        nums = [str(i) for i in range(10)]
        np.random.shuffle(nums)

        keypad[:] = [
            nums[0:3],
            nums[3:6],
            nums[6:9],
            ["⏎", nums[9], "⌫"]
        ]

root = tk.Tk()
root.resizable(False, True)
root.title("ECEN - 495")
root.configure(bg="#111111")
root.attributes("-fullscreen", True)
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

entry_var = tk.StringVar()


main_frame = tk.Frame(root, bg="#111111", pady=70)
main_frame.place(relx=0.5, rely=0.5, anchor="center", relheight=1)


display_frame = tk.Frame(main_frame, bg="#111111")
display_frame.pack(fill="x", pady=(0, 10))

entry = tk.Entry(
    display_frame,
    textvariable=entry_var,
    font=("Arial", 60, "bold"),
    justify="right",
    bd=8,
    bg="#222222",
    fg="#d006eb",
    insertbackground="#eb0693"
)
entry.pack(fill="x", ipady=40)

# Keypad frame
keypad_frame = tk.Frame(main_frame, bg="#111111")
keypad_frame.pack(fill="both", expand=True)

buttons = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["⏎", "0", "⌫"]
]

randKeypad(buttons)
button_refs = {}
for r, row in enumerate(buttons):
    for c, text in enumerate(row):
        if text == "⏎":
            cmd = enter
        elif text == "⌫":
            cmd = backspace
        else:
            cmd = lambda t=text: press(t)

        btn = tk.Button(
            keypad_frame,
            text=text,
            command=cmd,
            font=("Arial", 60, "bold"),
            bg="#333333",
            fg="#ffffff",
            activebackground="#12CE22",
            activeforeground="#000000",
            width=5,
            height=2
        )
        btn.grid(row=r, column=c, padx=5, pady=5, sticky="nsew")
        button_refs[text] = btn

button_refs["ENTER"] = button_refs["⏎"]
button_refs["DELETE"] = button_refs["⌫"]


### Invoking a button ###
#button_refs["1"].invoke()
#button_refs["ENTER"].invoke()
#button_refs["DELETE"].invoke()

### Making a button yellow ###
#button_refs["1"].config(bg="yellow")


for i in range(4):
    keypad_frame.grid_rowconfigure(i, weight=1)
for i in range(3):
    keypad_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
