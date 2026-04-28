import tkinter as tk
import random
import numpy as np
import time
import qwiic_vl53l5cx
import sys
from math import sqrt

distance_array = []

ROW_MIN_1 = 150
ROW_MAX_1 = 200

ROW_MIN_2 = 220
ROW_MAX_2 = 260

ROW_MIN_3 = 300
ROW_MAX_3 = 500

def set_all_buttons(color, text_color="#ffffff"):
    for btn in button_refs.values():
        btn.config(bg=color, fg=text_color)

def reset_buttons():
    for value, btn in button_refs.items():
        if value in pressed_keys:
            btn.config(bg="#12CE22", fg="#000000")
        else:
            btn.config(bg="#333333", fg="#ffffff")

def flash_keypad(color, flashes=6):
    global feedback_active

    feedback_active = True

    def flash_step(count):
        global feedback_active

        if count <= 0:
            entry_arr.clear()
            pressed_keys.clear()
            feedback_active = False
            reset_buttons()
            return

        if count % 2 == 0:
            set_all_buttons(color, "#000000")
        else:
            reset_buttons()

        root.after(200, lambda: flash_step(count - 1))

    flash_step(flashes)

shuffleKeys = False

entry_arr = []
pressed_keys = set()
last_pressed_button = None
feedback_active = False

def press(value):
    if feedback_active:
        return

    entry_arr.append(value)
    pressed_keys.add(value)

    if value in button_refs:
        button_refs[value].config(bg="#12CE22", fg="#000000")
        

    if len(entry_arr) == 4:
        enter()

def clear():
    entry_arr.clear()
    pressed_keys.clear()
    reset_buttons()

def backspace():
    if len(entry_arr) > 0:
        removed = entry_arr.pop()

        if removed not in entry_arr and removed in pressed_keys:
            pressed_keys.remove(removed)

        reset_buttons()

def enter():
    value = "".join(entry_arr)
    print("Entered:", value)

    if value == "1234":
        flash_keypad("#12CE22")
    else:
        flash_keypad("#FF0000")

def randKeypad(keypad):
    if shuffleKeys:
        nums = [str(i) for i in range(1, 10)]
        np.random.shuffle(nums)

        keypad[:] = [
            nums[0:3],
            nums[3:6],
            nums[6:9]
        ]

def get_distance_array():
    new_array = []

    if myVL53L5CX.check_data_ready():
        measurement_data = myVL53L5CX.get_ranging_data()

        display_row = 1

        for y in range(0, (image_width * (image_width - 1)) + 1, image_width):
            if display_row in [3, 6]:
                display_row += 1
                continue

            display_col = 1
            row_array = []

            for x in range(image_width - 1, -1, -1):
                if display_col in [1, 2, 3]:
                    display_col += 1
                    continue

                row_array.append(measurement_data.distance_mm[x + y])

                display_col += 1

            new_array.append(row_array)
            display_row += 1

    return new_array

def check_sensor():
    global distance_array, last_pressed_button

    if feedback_active:
        root.after(50, check_sensor)
        return

    distance_array = get_distance_array()

    if len(distance_array) >= 6:
        #Distances
        
        col_1_distance = np.min(distance_array[0])

        
        col_2_distance = np.min(distance_array[3])
        
        col_3_distance = np.min(distance_array[5])
        
        #Col 1
        if ROW_MIN_1 < col_1_distance < ROW_MAX_1:
            if last_pressed_button != "bottom_left":
                button_grid[2][0].invoke()
                last_pressed_button = "bottom_left"
                
        elif ROW_MIN_2 < col_1_distance < ROW_MAX_2:
            if last_pressed_button != "middle_left":
                button_grid[1][0].invoke()
                last_pressed_button = "middle_left"
                
        elif ROW_MIN_3 < col_1_distance < ROW_MAX_3:
            if last_pressed_button != "top_left":
                button_grid[0][0].invoke()
                last_pressed_button = "top_left"
                
        #Col 2
        elif ROW_MIN_1 < col_2_distance < ROW_MAX_1:
            if last_pressed_button != "bottom_middle":
                button_grid[2][1].invoke()
                last_pressed_button = "bottom_middle"
                
        elif ROW_MIN_2 < col_2_distance < ROW_MAX_2:
            if last_pressed_button != "center":
                button_grid[1][1].invoke()
                last_pressed_button = "center"
                
        elif ROW_MIN_3 < col_2_distance < ROW_MAX_3:
            if last_pressed_button != "top_middle":
                button_grid[0][1].invoke()
                last_pressed_button = "top_middle"
        
        #Col 3
        elif ROW_MIN_1 < col_3_distance < ROW_MAX_1:
            if last_pressed_button != "bottom_right":
                button_grid[2][2].invoke()
                last_pressed_button = "bottom_right"
                
        elif ROW_MIN_2 < col_3_distance < ROW_MAX_2:
            if last_pressed_button != "middle_right":
                button_grid[1][2].invoke()
                last_pressed_button = "middle_right"
                
        elif ROW_MIN_3 < col_3_distance < ROW_MAX_3:
            if last_pressed_button != "bottom_right":
                button_grid[0][2].invoke()
                last_pressed_button = "bottom_right"
        
        else:
            last_pressed_button = None

    root.after(50, check_sensor)

myVL53L5CX = qwiic_vl53l5cx.QwiicVL53L5CX()

print("\nInit VL53L5CX\n")

if myVL53L5CX.is_connected() == False:
    print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(0)

print("Initializing sensor board. This can take up to 10s. Please wait.")

if myVL53L5CX.begin() == False:
    print("Sensor initialization unsuccessful. Exiting...", file=sys.stderr)
    sys.exit(1)

myVL53L5CX.set_resolution(8 * 8)
image_resolution = myVL53L5CX.get_resolution()

image_width = int(sqrt(image_resolution))
myVL53L5CX.start_ranging()

root = tk.Tk()
root.resizable(True, True)
root.title("Secure Keypad")
root.configure(bg="#111111")
root.attributes("-fullscreen", True)
root.after(1000, lambda: root.attributes("-fullscreen", True))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

main_frame = tk.Frame(root, bg="#111111")
main_frame.place(relx=0.5, rely=0.5, anchor="center", relheight=1)

keypad_frame = tk.Frame(main_frame, bg="#111111")
keypad_frame.pack(fill="both", expand=True, pady=(0, 180))

buttons = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]

randKeypad(buttons)

button_refs = {}
button_grid = []

for r, row in enumerate(buttons):
    button_grid.append([])

    for c, text in enumerate(row):
        cmd = lambda t=text: press(t)

        btn = tk.Button(
            keypad_frame,
            text=text,
            command=cmd,
            font=("Times", 60),
            bg="#333333",
            fg="#ffffff",
            activebackground="#12CE22",
            activeforeground="#000000",
            width=2,
            height=2
        )

        btn.grid(row=r, column=c, padx=30, pady=10, sticky="nsew")

        button_refs[text] = btn
        button_grid[r].append(btn)

for i in range(4):
    keypad_frame.grid_rowconfigure(i, weight=1)

for i in range(3):
    keypad_frame.grid_columnconfigure(i, weight=1)

root.after(50, check_sensor)

root.mainloop()
