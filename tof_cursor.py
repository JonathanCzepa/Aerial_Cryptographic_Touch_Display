"""
Aerial Display - TOF Sensor Cursor Control
==========================================
This module tracks finger position using the VL53L5CX ToF sensor
and moves the mouse cursor to match.

Hardware Setup:
- VL53L5CX sensor mounted below the display
- 8x8 resolution provides 64 zones of detection

Configuration - ADJUST FOR YOUR HARDWARE:
"""
import tkinter as tk
import numpy as np
import time
import vl53l5cx_ctypes as vl53l5cx
from vl53l5cx_ctypes import STATUS_RANGE_VALID, STATUS_RANGE_VALID_LARGE_PULSE
import pyautogui

# =============================================================================
# TOF SENSOR CONFIGURATION - Adjust these values for your hardware setup
# =============================================================================
TOF_AVAILABLE = True  # Set to False to disable TOF sensor

# Distance threshold (mm) - closer than this = finger detected
# INCREASE if sensor doesn't detect far enough
# DECREASE if sensor detects too far
DETECTION_THRESHOLD = 300

# Screen mapping - ADJUST BASED ON YOUR DISPLAY SIZE
# These define the screen area that maps to the 8x8 sensor grid
SCREEN_LEFT = 200    # X position for sensor column 0
SCREEN_TOP = 200     # Y position for sensor row 0
SCREEN_WIDTH = 1400  # Width of active area
SCREEN_HEIGHT = 900  # Height of active area

# Smoothing - higher = smoother but more lag
# Lower = more responsive but jittery
SMOOTHING = 0.3

# Cursor update rate (ms) - lower = faster but more CPU
UPDATE_INTERVAL = 30

# Press detection - ADJUST FOR YOUR HARDWARE
# Distance (mm) closer than this = finger is pressing
PRESS_THRESHOLD = 80
# How much closer finger must move to register as a "press" (mm)
PRESS_DELTA = 20
# Cooldown between clicks (ms) - prevents double-clicks
CLICK_COOLDOWN = 500
# =============================================================================



# Tracking variables
prev_x = None
prev_y = None
prev_closest_dist = None
last_click_time = 0
prev_motion_zones = None


def initialize_sensor():
    """Initialize the VL53L5CX ToF sensor"""
    if not TOF_AVAILABLE:
        return None
    
    print("Uploading firmware, please wait...")
    vl53 = vl53l5cx.VL53L5CX()
    print("Done!")
    
    vl53.set_resolution(8 * 8)
    vl53.enable_motion_indicator(8 * 8)
    vl53.set_motion_distance(400, 1400)  # 40cm to 1.4m range
    vl53.start_ranging()
    
    return vl53


def get_closest_point(distances):
    """
    Find the closest point in the 8x8 sensor grid.
    Returns (zone_x, zone_y, distance) or None if nothing detected.
    """
    closest_dist = float('inf')
    closest_x, closest_y = -1, -1
    
    for i in range(64):
        zone_x = i % 8
        zone_y = i // 8
        dist = distances[i]
        
        # Skip invalid readings (0 = no detection)
        if dist > 0 and dist < closest_dist and dist < DETECTION_THRESHOLD:
            closest_dist = dist
            closest_x = zone_x
            closest_y = zone_y
    
    if closest_x >= 0:
        return (closest_x, closest_y, closest_dist)
    return None


def map_to_screen(zone_x, zone_y):
    """
    Map 8x8 sensor zone to screen coordinates.
    Assumes sensor is below display: higher zone_y = closer to bottom = higher Y
    """
    # Convert zone (0-7) to position (0.0-1.0)
    norm_x = zone_x / 7.0
    norm_y = zone_y / 7.0
    
    # Map to screen coordinates
    screen_x = SCREEN_LEFT + (norm_x * SCREEN_WIDTH)
    screen_y = SCREEN_TOP + (norm_y * SCREEN_HEIGHT)
    
    return int(screen_x), int(screen_y)


def smooth_cursor(new_x, new_y):
    """Apply smoothing to cursor movement"""
    global prev_x, prev_y
    
    if prev_x is None:
        prev_x, prev_y = new_x, new_y
        return new_x, new_y
    
    # Interpolate with previous position
    smoothed_x = int(prev_x + (new_x - prev_x) * SMOOTHING)
    smoothed_y = int(prev_y + (new_y - prev_y) * SMOOTHING)
    
    prev_x, prev_y = smoothed_x, smoothed_y
    
    return smoothed_x, smoothed_y


def check_tof_cursor(vl53, root):
    """Main loop - check sensor and move cursor"""
    global prev_x, prev_y, prev_closest_dist, last_click_time
    
    if not TOF_AVAILABLE or not PYAUTOGUI_AVAILABLE:
        root.after(UPDATE_INTERVAL, lambda: check_tof_cursor(vl53, root))
        return
    
    try:
        data = vl53.get_motion_indicator()
        
        if data:
            distances = data.distance_mm
            
            # Find closest finger point
            result = get_closest_point(distances)
            
            if result:
                zone_x, zone_y, dist = result
                
                # Map to screen coordinates
                screen_x, screen_y = map_to_screen(zone_x, zone_y)
                
                # Apply smoothing
                smooth_x, smooth_y = smooth_cursor(screen_x, screen_y)
                
                # Move cursor
                pyautogui.moveTo(smooth_x, smooth_y)
                
                prev_motion_zones = None
                # Gesture-based click detection
                def initialize_sensor():
                    """Initialize the VL53L5CX ToF sensor"""
                    if not TOF_AVAILABLE:
                        return None
    
                    print("Uploading firmware, please wait...")
                    vl53 = vl53l5cx.VL53L5CX()
                    print("Done!")
    
                    vl53.set_resolution(8 * 8)
                    vl53.enable_motion_indicator(8 * 8)
                    vl53.set_motion_distance(400, 1400)  # 40cm to 1.4m range
                    vl53.start_ranging()
    
                    return vl53


                def get_motion_center(data):
                    """
                    Find the center of all zones with motion detected.
                    Returns (zone_x, zone_y) or None if no motion.
    
                    Uses both motion flag and distance for more accurate detection.
                    """
                    motion_zones = data.motion_indicator.motion
                    distances = data.distance_mm
    
                    total_x = 0
                    total_y = 0
                    count = 0
    
                    for i in range(64):
                        zone_x = i % 8
                        zone_y = i // 8
        
                        # Check if motion detected AND valid distance
                        if motion_zones[i] and distances[i] > 0 and distances[i] < DETECTION_THRESHOLD:
                            total_x += zone_x
                            total_y += zone_y
                            count += 1
    
                    if count > 0:
                        # Return center of motion
                        return (total_x // count, total_y // count)
                    return None


                def check_tof_cursor(vl53, root):
                    """Main loop - check sensor and move cursor"""
                    global prev_x, prev_y, prev_motion_zones, last_click_time
    
                    if not TOF_AVAILABLE or not PYAUTOGUI_AVAILABLE:
                        root.after(UPDATE_INTERVAL, lambda: check_tof_cursor(vl53, root))
                        return
    
                    try:
                        data = vl53.get_motion_indicator()
        
                        if data:
                            # Find center of motion
                            result = get_motion_center(data)
            
                            if result:
                                zone_x, zone_y = result
                
                                # Map to screen coordinates
                                screen_x, screen_y = map_to_screen(zone_x, zone_y)
                
                                # Apply smoothing
                                smooth_x, smooth_y = smooth_cursor(screen_x, screen_y)
                
                                # Move cursor
                                pyautogui.moveTo(smooth_x, smooth_y)
                
                                # Motion-based click detection
                                # Click when NEW motion starts in a zone (finger enters)
                                current_time = time.time() * 1000  # ms
                                current_motion = data.motion_indicator.motion
                
                                if prev_motion_zones is not None:
                                    # Check for new motion zones
                                    for i in range(64):
                                        if current_motion[i] and not prev_motion_zones[i]:
                                            # New motion detected - this is a "tap"
                                            if current_time - last_click_time > CLICK_COOLDOWN:
                                                pyautogui.click()
                                                last_click_time = current_time
                                                print(f"CLICK! New motion at zone {i % 8},{i // 8}")
                                                break
                
                                prev_motion_zones = list(current_motion)
                
                                # Optional: print debug info
                                # print(f"Motion at: ({zone_x}, {zone_y}) -> Screen: ({smooth_x}, {smooth_y})")
        
                        # Schedule next check
                        root.after(UPDATE_INTERVAL, lambda: check_tof_cursor(vl53, root))
        
                    except Exception as e:
                        print(f"TOF error: {e}")
                        root.after(UPDATE_INTERVAL, lambda: check_tof_cursor(vl53, root))
    except Exception as e:
        print(f"TOF error: {e}")
