import tkinter as tk
import random
import numpy as np
import time
import numpy
import vl53l5cx_ctypes as vl53l5cx
from vl53l5cx_ctypes import STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE

print("Uploading firmware, please wait...")
vl53 = vl53l5cx.VL53L5CX()
print("Done!")
vl53.set_resolution(8 * 8)
vl53.enable_motion_indicator(8 * 8)
# vl53.set_integration_time_ms(50)

# Enable motion indication at 8x8 resolution
vl53.enable_motion_indicator(8 * 8)

# Default motion distance is quite far, set a sensible range
# eg: 40cm to 1.4m
vl53.set_motion_distance(400, 1400)

vl53.start_ranging()

# Try different method names for getting distance data
# The library may have get_data(), get_distance(), or get_ranging_data()
def get_tof_data():
    """Try multiple methods to get TOF data"""
    # Try get_data() first (common in vl53l5cx libraries)
    if hasattr(vl53, 'get_data'):
        return vl53.get_data()
    # Try get_distance() alternative
    elif hasattr(vl53, 'get_distance'):
        return vl53.get_distance()
    # Try get_ranging_data()
    elif hasattr(vl53, 'get_ranging_data'):
        return vl53.get_ranging_data()
    # Fallback: try motion indicator (may work on some versions)
    elif hasattr(vl53, 'get_motion_indicator'):
        return vl53.get_motion_indicator()
    else:
        return None

# =============================================================================
# TOF SENSOR CONFIGURATION - Adjust these values for your hardware setup
# =============================================================================
TOF_AVAILABLE = True  # Set to False to disable TOF sensor

# Distance thresholds (in mm) - ADJUST BASED ON YOUR HARDWARE TESTING
# HOVER: Distance when finger is detected (yellow highlight)
# PRESS: Distance when finger is pressing (green highlight + trigger)
HOVER_THRESHOLD = 300   # Default: 300mm - increase if sensor range is longer
PRESS_THRESHOLD = 100   # Default: 100mm - decrease if sensor needs closer contact

# Sensor orientation - ADJUST IF BUTTONS DON'T MATCH HAND POSITION
# If bottom row buttons highlight when hand is at TOP of display, set to True
INVERT_ROW = True       # True = bottom of display is closer to sensor (sensor below)
# =============================================================================

# Track previous distances to detect press (getting closer)
prev_distances = [0] * 64
last_pressed_button = None

def get_button_from_zone(zone_x, zone_y):
    """
    Map 8x8 zone coordinates to button index (0-8)
    
    Button layout (3x3 grid):
        1  2  3   (top row - furthest from sensor)
        4  5  6   (middle row)
        7  8  9   (bottom row - closest to sensor)
    
    Zone coordinates: (0,0) is top-left, (7,7) is bottom-right of sensor
    """
    col = min(2, zone_x // 3)  # 0, 1, 2
    
    if INVERT_ROW:
        # Sensor is below display: higher zone_y = closer = bottom row
        row = min(2, zone_y // 3)
    else:
        # Sensor is above display: lower zone_y = closer = bottom row
        row = 2 - min(2, zone_y // 3)
    
    return row * 3 + col  # Returns 0-8

def check_tof_hover():
    """Check TOF sensor for finger hover and press over buttons"""
    global prev_distances, last_pressed_button
    
    if not TOF_AVAILABLE:
        return
    
    try:
        data = get_tof_data()
        if data:
            # Try different attribute names for distance data
            if hasattr(data, 'distance_mm'):
                distances = data.distance_mm
            elif hasattr(data, 'distance'):
                distances = data.distance
            elif hasattr(data, 'distances'):
                distances = data.distances
            elif hasattr(data, 'data'):
                distances = data.data
            else:
                # Try as numpy array or list
                distances = np.array(data)
            # distances is 64-element array for 8x8 grid
            
            # Reset all buttons to default
            for btn in button_refs.values():
                btn.config(bg="#333333", fg="#ffffff")
            
            # Check each zone for close object
            hovered_buttons = set()
            pressed_button = None
            
            for i in range(64):
                zone_x = i % 8
                zone_y = i // 8
                dist = distances[i]
                prev_dist = prev_distances[i]
                
                # Detect press: current distance is closer than previous AND within press range
                if dist > 0 and dist < PRESS_THRESHOLD and prev_dist > dist:
                    btn_idx = get_button_from_zone(zone_x, zone_y)
                    pressed_button = btn_idx
                
                # Detect hover: within hover threshold but not pressed
                if dist > 0 and dist < HOVER_THRESHOLD:
                    btn_idx = get_button_from_zone(zone_x, zone_y)
                    hovered_buttons.add(btn_idx)
                
                prev_distances[i] = dist
            
            # Highlight pressed button (green)
            if pressed_button is not None:
                btn_num = str(pressed_button + 1)
                if btn_num in button_refs:
                    button_refs[btn_num].config(bg="#12CE22", fg="#000000")
                    # Trigger button press
                    press(btn_num)
                    last_pressed_button = pressed_button
            # Highlight hovered buttons (yellow) - only if not pressed
            elif hovered_buttons:
                for btn_idx in hovered_buttons:
                    btn_num = str(btn_idx + 1)
                    if btn_num in button_refs:
                        button_refs[btn_num].config(bg="#FFFF00", fg="#000000")
        
        # Check again in 50ms
        root.after(50, check_tof_hover)
    except Exception as e:
        print(f"TOF error: {e}")
        root.after(50, check_tof_hover)

shuffleKeys = False

entry_arr = []

def press(value):
    entry_arr.append(value)
    #current = entry_var.get()
    #entry_var.set(current + value)
    current = entry_var.get()
    entry_var.set(current + "*")
    
    # Auto-enter after 4 digits
    if len(entry_arr) == 4:
        enter()

def clear():
    entry_var.set("")

def backspace():
    current = entry_var.get()
    entry_var.set(current[:-1])

def enter():
    value = "".join(entry_arr) #Retrieve the actual digits entered
    print("Entered:", value)

    if value == "1234":
        entry_var.set("Accepted")
        root.after(1500, lambda: [clear(), entry_arr.clear()])
    else:
        entry_var.set("Wrong Password")
        root.after(1500, lambda: [clear(), entry_arr.clear()])

def randKeypad(keypad):
    if shuffleKeys:
        nums = [str(i) for i in range(1, 10)]  # 1-9 only, no 0
        np.random.shuffle(nums)

        keypad[:] = [
            nums[0:3],
            nums[3:6],
            nums[6:9]
        ]

root = tk.Tk()
root.resizable(True, True)
root.title("Secure Keypad")
root.configure(bg="#111111")
root.attributes("-fullscreen", True)
root.after(1000, lambda: root.attributes('-fullscreen', True))
root.bind("<Escape>", lambda event: root.attributes("-fullscreen", False))

entry_var = tk.StringVar()


main_frame = tk.Frame(root, bg="#111111", pady=70)
main_frame.place(relx=0.5, rely=0.5, anchor="center", relheight=1)


display_frame = tk.Frame(main_frame, bg="#111111")
display_frame.pack(fill="x", pady=(0, 10))

entry = tk.Entry(
    display_frame,
    textvariable=entry_var,
    font=("Arial", 30, "bold"),
    justify="center",
    bd=8,
    bg="#222222",
    fg="#d006eb",
    insertbackground="#eb0693"
)
entry.pack(fill="x", ipady=10)

# Keypad frame
keypad_frame = tk.Frame(main_frame, bg="#111111")
keypad_frame.pack(fill="both", expand=True)

buttons = [
    ["1", "2", "3"],
    ["4", "5", "6"],
    ["7", "8", "9"]
]

randKeypad(buttons)
button_refs = {}
for r, row in enumerate(buttons):
    for c, text in enumerate(row):

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
        btn.grid(row=r, column=c, padx=30, pady=10, sticky="nsew")
        
        # Hover effects
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg="#FFFF00", fg="#000000"))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg="#333333", fg="#ffffff"))
        
        button_refs[text] = btn



for i in range(4):
    keypad_frame.grid_rowconfigure(i, weight=1)
for i in range(3):
    keypad_frame.grid_columnconfigure(i, weight=1)


# Start TOF hover detection
if TOF_AVAILABLE:
    root.after(500, check_tof_hover)  # Wait for sensor to initialize

root.mainloop()
