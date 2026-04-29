import tkinter as tk
import random
import numpy as np
import time
import qwiic_vl53l5cx
import sys
from math import sqrt

'''
TOF Sensor Initialization
'''
myVL53L5CX = qwiic_vl53l5cx.QwiicVL53L5CX() #Easier name 
distance_array = [] #Empty array to store distance measurements in
print("\nInit VL53L5CX\n")
if myVL53L5CX.is_connected() == False:
    print("The device isn't connected to the system. Please check your connection", file=sys.stderr)
    sys.exit(0)
    
if myVL53L5CX.begin() == False:
    print("Sensor initialization unsuccessful. Exiting...", file=sys.stderr)
    sys.exit(1)

myVL53L5CX.set_resolution(8 * 8)
image_resolution = myVL53L5CX.get_resolution()

image_width = int(sqrt(image_resolution))
myVL53L5CX.start_ranging()

'''
Keypad Setup
'''

shuffleKeys = False #Shuffle the keypad

entry_arr = [] #Empty array for buttons pressed
pressed_keys = set()
last_pressed_button = None
feedback_active = False #Stop system from pressing new keys while visual feedback is active

'''
Ranging values for Rows
'''
ROW_MIN_1 = 110 #Bottom Row
ROW_MAX_1 = 200

ROW_MIN_2 = 205 #Middle Row
ROW_MAX_2 = 260

ROW_MIN_3 = 265 #Top Row
ROW_MAX_3 = 360

'''
Ranging Values for Columns
'''
COL_MIN_1 = 300 #Left Column
COL_MAX_1 = 399

COL_MIN_2 = 400 #Middle Column
COL_MAX_2 = 460

COL_MIN_3 = 465 #Right Column
COL_MAX_3 = 560


'''
Sets a buttons colour
'''
def set_all_buttons(color, text_color="#ffffff"):
    for btn in button_refs.values():
        btn.config(bg=color, fg=text_color)

'''
Removes a buttons colour
'''
def reset_buttons():
    for value, btn in button_refs.items():
        if value in pressed_keys:
            btn.config(bg="#12CE22", fg="#000000")
        else:
            btn.config(bg="#333333", fg="#ffffff")

'''
Flashes the keypad red or green, determined by if the user input proper PIN
'''
def flash_keypad(color, flashes=6):
    global feedback_active

    feedback_active = True

    def flash_step(count):
        global feedback_active

        if count <= 0:
            pressed_keys.clear()
            feedback_active = False
            reset_buttons()
            return

        if count % 2 == 0:
            set_all_buttons(color, "#000000")
        else:
            reset_buttons()

        root.after(100, lambda: flash_step(count - 1))

    flash_step(flashes)

'''
Presses a button via TKINTER invoke
'''
def press(value):
    if feedback_active:
        return

    entry_arr.append(value)
    pressed_keys.add(value)

    if value in button_refs:
        button_refs[value].config(bg="#12CE22", fg="#000000")

        def turn_gray():
            if value in button_refs and not feedback_active:
                button_refs[value].config(bg="#333333", fg="#ffffff")

        root.after(500, turn_gray)

    if len(entry_arr) == 4:
        enter()


'''
Randomize the keypad array
'''
def randKeypad(keypad):
    if shuffleKeys:
        nums = [str(i) for i in range(1, 10)]
        np.random.shuffle(nums)

        keypad[:] = [
            nums[0:3],
            nums[3:6],
            nums[6:9]
        ]

'''
Enter the 4 digit user input (Checks if user input is correct or not
'''
def enter():
    value = "".join(entry_arr)  #String the array
    entry_arr.clear()           #Clear the array
    print("Entered:", value)

    if value == "1471":
        flash_keypad("#12CE22") #Flash Green
        value = ''          #Clear Value String
    else:
        flash_keypad("#FF0000") #Flash Red
        value = ''          #Clear Value string
        
        
'''
Determines the Row (and eventually column) being pressed
'''
def get_row_distance():
    new_array = []

    if myVL53L5CX.check_data_ready():
        measurement_data = myVL53L5CX.get_ranging_data()

        display_row = 1

        #Read the distances from the zones (we have removed unnecessary zones)
        for y in range(0, (image_width * (image_width - 1)) + 1, image_width):
            if display_row in [3, 6]:
                display_row += 1
                continue

            display_col = 1 
            row_array = []
            
            for x in range(image_width - 1, -1, -1):
                if display_col in [1, 2, 3, 5, 6, 7, 8]:
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
        root.after(200, check_sensor)
        return

    distance_array = get_row_distance()

    if len(distance_array) >= 6:
        distances = []
        
        i = 0
        while i < 6:
            base10String = str(distance_array[i])[1:-1] #Cut of brackets
            if (int(base10String) < 400): #If measured value is above 400, ignore it
                distances.append(np.mean(distance_array[i]))
            i += 1
        dist_avg = np.mean(distances)
        
        
        if ROW_MIN_1 < dist_avg < ROW_MAX_1: #Bottom Row
            button_grid[2][0].invoke()
            print(dist_avg)
                
        elif ROW_MIN_2 < dist_avg < ROW_MAX_2: #Middle Row
            button_grid[1][0].invoke()
            print(dist_avg)
                
        elif ROW_MIN_3 < dist_avg < ROW_MAX_3: #Top Row
            button_grid[0][0].invoke()
            print(dist_avg)
        
    root.after(500, check_sensor)



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

'''
Button array referenced by system
'''
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
