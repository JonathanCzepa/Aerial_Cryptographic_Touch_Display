import tkinter as tk
import random
import numpy as np

shuffleKeys = True

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

# def randKeypad(keypad):
#     if shuffleKeys:
#         flat = [item for row in keypad for item in row]
#         np.random.shuffle(flat)
#         keypad[:] = [flat[i:i+3] for i in range(0, len(flat), 3)]

root = tk.Tk()
root.resizable(False, True)
root.title("ECEN - 495")
root.configure(bg="#111111")

entry_var = tk.StringVar()

# Main outer frame
main_frame = tk.Frame(root, bg="#111111")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Display frame
display_frame = tk.Frame(main_frame, bg="#111111")
display_frame.pack(fill="x", pady=(0, 10))

entry = tk.Entry(
    display_frame,
    textvariable=entry_var,
    font=("Arial", 60, "bold"),
    justify="right",
    bd=8,
    bg="#222222",
    fg="#eb0606",
    insertbackground="#eb0606"
)
entry.pack(fill="x", ipady=40)

# Keypad frame
keypad_frame = tk.Frame(main_frame, bg="#111111")
keypad_frame.pack(fill="both", expand=True)

buttons = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["CLR", "0", "⌫"]
]

# randKeypad(buttons)
button_refs = {}
for r, row in enumerate(buttons):
    for c, text in enumerate(row):
        if text == "CLR":
            cmd = clear
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
        
# Enter button frame
enter_frame = tk.Frame(main_frame, bg="#111111")
enter_frame.pack(fill="x", pady=(10, 0))

enter_button = tk.Button(
    enter_frame,
    text="ENTER",
    command=enter,
    font=("Arial", 60, "bold"),
    bg="#8b0000",
    fg="white",
    activebackground="#12CE22",
    activeforeground="#000000",
    height=2
)
enter_button.pack(fill="x")

# Make keypad resize nicely inside its frame
for i in range(4):
    keypad_frame.grid_rowconfigure(i, weight=1)
for i in range(3):
    keypad_frame.grid_columnconfigure(i, weight=1)

root.mainloop()
