import time
from machine import Pin
import neopixel
from pn532_i2c import PN532_I2C

# --- Configuration ---
# The UID of the "Master" tag (This is the UID from your screenshot!)
AUTHORIZED_UID = "04:3C:40:F2:4E:6D:80"  

NEOPIXEL_PIN = 13  # The ESP32 pin connected to the NeoPixel Data In (DIN)
NUM_PIXELS = 1     # Number of LEDs

# Initialize NeoPixel
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)

def set_color(r, g, b):
    """Helper function to change the NeoPixel color."""
    for i in range(NUM_PIXELS):
        np[i] = (r, g, b)
    np.write()

# Start with the LED turned off
set_color(0, 0, 0)

# Initialize the NFC Reader
reader = PN532_I2C(scl_pin=22, sda_pin=21)

if reader.sam_configure():
    print("Access Control System Ready!")
    
    while True:
        uid = reader.read_passive_target()
        
        if uid:
            uid_hex = ":".join(["{:02X}".format(b) for b in uid])
            print(f"Scanned UID: {uid_hex}")
            
            # --- The Logic ---
            if uid_hex == AUTHORIZED_UID:
                print("Access Granted! Unlocking door...\n")
                set_color(0, 255, 0)  # Green
                time.sleep(2)         # Keep "unlocked" for 2 seconds
                
            else:
                print("Access Denied! Intruder alert!\n")
                set_color(255, 0, 0)  # Red
                time.sleep(2)         # Show red for 2 seconds
                
            # Reset LED and wait before the next scan
            set_color(0, 0, 0) 
            time.sleep(0.5) 
            
        time.sleep(0.1)
else:
    print("Failed to initialize PN532.")
