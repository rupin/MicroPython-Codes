from ble_keyboard import BLEKeyboard
from machine import Pin, TouchPad
import time

# 1. Initialize the Bluetooth Keyboard
kb = BLEKeyboard("ESP32KB") # Naem should be less then 10 characters

# 2. Initialize Touch Pins 
# We use GPIO 4 and GPIO 13 as they are safe to use on almost all ESP32 boards
touch_left = TouchPad(Pin(4))
touch_right = TouchPad(Pin(13))

# 3. Set the Touch Threshold
# Un-touched pins usually read around 500-800.
# Touched pins usually drop below 300. 
# You may need to tweak this number depending on if you use wires vs bare pins!
THRESHOLD = 500 

print("Waiting for Bluetooth connection...")
connection_ready = False

while True:
    if kb.is_connected():
        if not connection_ready:
            print("Connected! Waiting 2 seconds for OS security handshake...")
            time.sleep(2)
            print("Ready to touch!")
            connection_ready = True
            
        try:
            # Read the current capacitance values
            val_left = touch_left.read()
            val_right = touch_right.read()
            #print(val_left)
            #print(val_right)
            
            # Check Left Touch (GPIO 4)
            if val_left < THRESHOLD:
                print(f"Left touched! (Value: {val_left}) -> Sending Left Arrow")
                kb.type_text("C")
                
                # CRITICAL: Wait for the user to let go of the wire
                while touch_left.read() < THRESHOLD:
                    time.sleep_ms(20)
                time.sleep_ms(100) # Debounce after release
                
            # Check Right Touch (GPIO 13)
            elif val_right < THRESHOLD:
                print(f"Right touched! (Value: {val_right}) -> Sending Right Arrow")
                kb.type_text("Z")
                
                # CRITICAL: Wait for the user to let go of the wire
                while touch_right.read() < THRESHOLD:
                    time.sleep_ms(20)
                time.sleep_ms(100) # Debounce after release

        except ValueError:
            # Sometimes touch pins throw a quick ValueError if there is static interference
            pass

    else:
        connection_ready = False
        
    time.sleep_ms(50)

