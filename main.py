import tkinter as tk

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


root = tk.Tk()
root.resizable(False, True)
root.title("ECEN - 495")
root.configure(bg="#111111")

entry_var = tk.StringVar()

entry = tk.Entry(
    root,
    textvariable=entry_var,
    font=("Arial", 60, "bold"),
    justify="right",
    bd=8,
    bg="#222222",
    fg="#eb0606",
    insertbackground="#eb0606"
)
entry.grid(row=0, column=0, columnspan=3, padx=10, pady=5, sticky="nsew", ipady=80)

buttons = [
    ["1", "1", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"],
    ["CLR", "0", "⌫"]
]

for r, row in enumerate(buttons, start=1):
    for c, text in enumerate(row):
        if text == "CLR":
            cmd = clear
        elif text == "⌫":
            cmd = backspace
        else:
            cmd = lambda t=text: press(t)

        tk.Button(
            root,
            text=text,
            command=cmd,
            font=("Arial", 60, "bold"),
            bg="#333333",             
            fg="#ffffff",              
            activebackground="#555555",
            activeforeground="#ff4444",
            width=5,
            height=2
        ).grid(row=r, column=c, padx=5, pady=5, sticky="nsew")

tk.Button(
    root,
    text="ENTER",
    command=enter,
    font=("Arial", 60, "bold"),
    bg="#8b0000",
    fg="white",
    activebackground="#b22222",
    activeforeground="white",
    height=2
).grid(row=5, column=0, columnspan=3, padx=5, pady=10, sticky="nsew")


for i in range(6):
    root.grid_rowconfigure(i, weight=1)
for i in range(3):
    root.grid_columnconfigure(i, weight=1)

root.mainloop()
