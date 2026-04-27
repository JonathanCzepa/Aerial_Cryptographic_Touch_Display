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
    # Pimoroni vl53l5cx-ctypes library uses data_ready() and get_data()
    if hasattr(vl53, 'data_ready') and vl53.data_ready():
        if hasattr(vl53, 'get_data'):
            return vl53.get_data()
    # SparkFun library uses check_data_ready() and get_ranging_data()
    if hasattr(vl53, 'check_data_ready') and vl53.check_data_ready():
        if hasattr(vl53, 'get_ranging_data'):
            return vl53.get_ranging_data()
    # Try get_data() (common in other vl53l5cx libraries)
    if hasattr(vl53, 'get_data'):
        return vl53.get_data()
    # Try get_distance() alternative
    elif hasattr(vl53, 'get_distance'):
        return vl53.get_distance()
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
    global last_pressed_button
    
    if not TOF_AVAILABLE:
        return
    
    try:
        data = get_tof_data()
        if data:
            # Get distance data as numpy array
            if hasattr(data, 'distance_mm'):
                # Use numpy directly on the ctypes array
                distances = np.asarray(data.distance_mm[:64])
            elif hasattr(data, 'distance'):
                distances = np.asarray(data.distance[:64])
            else:
                distances = np.asarray(data)[:64]
            
            # Reset all buttons to default
            for btn in button_refs.values():
                btn.config(bg="#333333", fg="#ffffff")
            
            # Find the closest zone with valid reading
            closest_zone = -1
            closest_dist = 9999  # Use int instead of float('inf')
            
            for i in range(64):
                d = int(distances[i])  # Convert to Python int
                if d > 0 and d < closest_dist:
                    closest_dist = d
                    closest_zone = i
            
            # If we found a valid zone, map to button
            if closest_zone != -1:
                zone_x = closest_zone % 8
                zone_y = closest_zone // 8
                btn_idx = get_button_from_zone(zone_x, zone_y)
                btn_num = str(btn_idx + 1)
                
                # Check if it's a press (very close) or hover
                if closest_dist < PRESS_THRESHOLD:
                    # Press - green
                    if btn_num in button_refs:
                        button_refs[btn_num].config(bg="#12CE22", fg="#000000")
                        press(btn_num)
                elif closest_dist < HOVER_THRESHOLD:
                    # Hover - yellow
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
